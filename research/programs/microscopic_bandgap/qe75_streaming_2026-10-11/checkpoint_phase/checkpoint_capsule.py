"""GPL-2.0-or-later. Durable no-copy EXX checkpoint *storage* transaction.

This does not manufacture missing QE state or authorize QE restart. Callers must
export the complete old operator/occupations/ACE and native state in frozen
sidecars and prove the capture boundary. Native qualification is deliberately
false until the separately audited QE state bridge exists.

All state is under a newly owned DFT/.local namespace. Streams are hard-linked,
not copied. Only one CURRENT checkpoint is permitted. Consumption explicitly
retires it before a new full generation; loss of last-checkpoint recovery at
that point is declared, not hidden. No supervisor, MPI or QE launch path.
"""
from __future__ import annotations
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import uuid

BASE=Path('/home/User/opencode_workspace/DFT/.local').resolve()
VERSION='r07-exx-capsule-v1'
MAX_META=1024*1024
REQUIRED=('stream','exx_state','native_state')


class Refusal(RuntimeError): pass
class InjectedFailure(RuntimeError): pass


def encode(obj):
    return (json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def sync_dir(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try: os.fsync(fd)
    finally: os.close(fd)


def no_symlink(path):
    p=Path(path)
    if p.is_symlink(): raise Refusal('symlink refused')
    if p.resolve()!=p.absolute(): raise Refusal('noncanonical path refused')
    return p


def digest_file(path):
    """1 MiB memory, no stream duplication; refuse changing or nonregular inode."""
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        initial=os.fstat(fd)
        if not stat.S_ISREG(initial.st_mode) or initial.st_uid!=os.getuid():
            raise Refusal('foreign/nonregular checkpoint member')
        sha=hashlib.sha256()
        while True:
            chunk=os.read(fd,1024*1024)
            if not chunk: break
            sha.update(chunk)
        final=os.fstat(fd)
        if (initial.st_size,initial.st_mtime_ns,initial.st_ino)!=(final.st_size,final.st_mtime_ns,final.st_ino):
            raise Refusal('member changed during hashing')
        return {'sha256':sha.hexdigest(),'bytes':final.st_size,'dev':final.st_dev,'ino':final.st_ino}
    finally: os.close(fd)


def durable_bytes(path,payload):
    if len(payload)>MAX_META: raise Refusal('metadata extent exceeded')
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:
        view=memoryview(payload)
        while view:
            written=os.write(fd,view)
            if not written: raise Refusal('short metadata write')
            view=view[written:]
        os.fsync(fd)
    finally: os.close(fd)


def read_meta(path):
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        size=os.fstat(fd).st_size
        if size>MAX_META: raise Refusal('oversized checkpoint metadata')
        with os.fdopen(fd,'rb',closefd=False) as file:
            try: return json.loads(file.read())
            except (ValueError,UnicodeDecodeError) as exc: raise Refusal('malformed metadata') from exc
    finally: os.close(fd)


class Capsule:
    def __init__(self,root,create=False):
        self.root=Path(root).absolute()
        if not self.root.is_relative_to(BASE): raise Refusal('DFT project-local root required')
        no_symlink(self.root.parent)
        if create:
            self.root.mkdir(mode=0o700,exist_ok=False)
            durable_bytes(self.root/'OWNER.json',encode({'version':VERSION,'uid':os.getuid(),'owner':uuid.uuid4().hex}))
            (self.root/'live').mkdir(mode=0o700)
            sync_dir(self.root); sync_dir(self.root.parent)
        no_symlink(self.root)
        self.owner=read_meta(self.root/'OWNER.json')
        if self.owner.get('version')!=VERSION or self.owner.get('uid')!=os.getuid():
            raise Refusal('incompatible or foreign checkpoint owner')

    @contextmanager
    def locked(self):
        fd=os.open(self.root/'LOCK',os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
        try:
            try: fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError as exc: raise Refusal('checkpoint already owned by another writer') from exc
            yield
        finally: os.close(fd)

    def member(self,rank,role):
        if not isinstance(rank,int) or rank<0 or role not in REQUIRED: raise Refusal('invalid rank or role')
        return self.root/'live'/f'rank{rank:06d}.{role}'

    def _hit(self,fail_at,point):
        if fail_at==point: raise InjectedFailure(point)

    def publish(self,layouts,provenance,fail_at=None):
        """All ranks must be quiescent/sealed. One coordinator calls this.

        The global atomic CURRENT rename is the commit point. A return value
        certifies storage integrity only; semantics of opaque state must be
        established by an audited native bridge, not filename presence.
        """
        with self.locked():
            no_symlink(self.root/'live')
            if (self.root/'CURRENT.json').exists(): raise Refusal('current checkpoint must be consumed/retired first')
            if not layouts or set(map(int,layouts))!=set(range(len(layouts))): raise Refusal('missing rank layout')
            if len(layouts)>64: raise Refusal('bounded rank metadata limit')
            if not isinstance(provenance,dict) or not provenance: raise Refusal('provenance required')
            plans=[]
            for rank in range(len(layouts)):
                for role in REQUIRED:
                    source=self.member(rank,role); no_symlink(source)
                    if not source.exists(): raise Refusal('incomplete old-operator/native closure member set')
                    plans.append({'rank':rank,'role':role,'name':source.name,**digest_file(source)})
            gen=uuid.uuid4().hex
            directory=self.root/('generation-'+gen); directory.mkdir(mode=0o700)
            payload={'version':VERSION,'owner':self.owner['owner'],'generation':gen,
                     'layouts':{str(k):v for k,v in layouts.items()},'provenance':provenance,
                     'native_QE_restart_qualified':False,'members':[]}
            durable_bytes(directory/'OWNER.json',encode({'owner':self.owner['owner'],'generation':gen,'members':plans}))
            for item in plans:
                source=self.member(item['rank'],item['role'])
                fd=os.open(source,os.O_RDWR|os.O_NOFOLLOW)
                try: os.fsync(fd)
                finally: os.close(fd)
                target=directory/source.name
                os.link(source,target,follow_symlinks=False)
                stamp=digest_file(target)
                if any(stamp[k]!=item[k] for k in ['sha256','bytes','dev','ino']):
                    raise Refusal('source changed or checkpoint link is not same inode')
                payload['members'].append(item)
                self._hit(fail_at,'after_link')
            self._hit(fail_at,'after_data_sync')
            durable_bytes(directory/'MANIFEST.json',encode(payload)); sync_dir(directory); sync_dir(self.root)
            self._hit(fail_at,'after_manifest_sync')
            manifest_stamp=digest_file(directory/'MANIFEST.json')
            pointer={'version':VERSION,'owner':self.owner['owner'],'generation':gen,
                     'manifest_sha256':manifest_stamp['sha256']}
            staged=self.root/('CURRENT-'+gen+'.tmp'); durable_bytes(staged,encode(pointer))
            self._hit(fail_at,'before_commit')
            os.replace(staged,self.root/'CURRENT.json')
            self._hit(fail_at,'after_commit')
            sync_dir(self.root)
            self._hit(fail_at,'after_commit_sync')
            return pointer

    def _verify(self,layouts,provenance):
        pointer=read_meta(self.root/'CURRENT.json')
        if pointer.get('version')!=VERSION or pointer.get('owner')!=self.owner['owner']:
            raise Refusal('incompatible checkpoint version/owner')
        gen=pointer.get('generation','')
        if not re.fullmatch('[0-9a-f]{32}',gen): raise Refusal('invalid checkpoint generation')
        directory=self.root/('generation-'+gen); no_symlink(directory)
        if digest_file(directory/'MANIFEST.json')['sha256']!=pointer.get('manifest_sha256'):
            raise Refusal('manifest checksum mismatch')
        manifest=read_meta(directory/'MANIFEST.json')
        if manifest.get('version')!=VERSION or manifest.get('generation')!=gen or manifest.get('owner')!=self.owner['owner']:
            raise Refusal('manifest identity mismatch')
        if manifest.get('layouts')!={str(k):v for k,v in layouts.items()}: raise Refusal('MPI/FFT/band/q/native layout mismatch')
        if manifest.get('provenance')!=provenance: raise Refusal('source/input/PP/state provenance mismatch')
        wanted={(r,s) for r in range(len(layouts)) for s in REQUIRED}
        actual=set()
        for item in manifest['members']:
            key=(item['rank'],item['role'])
            if key in actual or key not in wanted: raise Refusal('duplicate/foreign member')
            actual.add(key)
            expected=f"rank{item['rank']:06d}.{item['role']}"
            if item['name']!=expected: raise Refusal('member path traversal/role mismatch')
            stamp=digest_file(directory/item['name'])
            if any(stamp[k]!=item[k] for k in ['sha256','bytes','dev','ino']): raise Refusal('member corruption/replacement')
        if actual!=wanted: raise Refusal('incomplete rank member set')
        return directory,manifest

    def verify(self,layouts,provenance,require_native=False):
        with self.locked():
            directory,manifest=self._verify(layouts,provenance)
            if require_native:
                raise Refusal('native QE capture/import bridge not qualified; storage integrity is insufficient')
            return directory,manifest

    def adopt(self,layouts,provenance):
        """Restore missing active links, preserving immutable committed generation.

        Returned active paths are read-only by contract. They must not be reused
        for producer writes. The native bridge must consume before a new store.
        """
        with self.locked():
            no_symlink(self.root/'live')
            directory,manifest=self._verify(layouts,provenance)
            for item in manifest['members']:
                active=self.member(item['rank'],item['role']); source=directory/item['name']
                if active.exists():
                    if active.is_symlink() or active.stat().st_ino!=source.stat().st_ino:
                        raise Refusal('unrelated active member prevents adoption')
                else: os.link(source,active,follow_symlinks=False)
            sync_dir(self.root/'live')
            return manifest

    def consume(self,layouts,provenance,fail_at=None):
        """Retire checkpoint durably BEFORE allowing replacement producer data.

        Crash after this boundary means no checkpoint available, not fallback to
        partly overwritten old data. Does not promise last-checkpoint recovery
        while arbitrary new data occupy the same bounded scratch capacity.
        """
        with self.locked():
            no_symlink(self.root/'live')
            directory,manifest=self._verify(layouts,provenance)
            destination=self.root/('CONSUMED-'+manifest['generation']+'.json')
            os.rename(self.root/'CURRENT.json',destination); sync_dir(self.root)
            self._hit(fail_at,'after_retire')
            for item in manifest['members']:
                active=self.member(item['rank'],item['role']); source=directory/item['name']
                if active.exists() and not active.is_symlink() and active.stat().st_ino==item['ino']:
                    active.unlink()
                source.unlink()
            sync_dir(self.root/'live'); sync_dir(directory)
            return manifest

    def cleanup_orphan(self,generation):
        """Remove only recorded owned names. Unexpected files prevent cleanup."""
        with self.locked():
            if not re.fullmatch('[0-9a-f]{32}',generation): raise Refusal('invalid generation cleanup')
            if (self.root/'CURRENT.json').exists() and read_meta(self.root/'CURRENT.json').get('generation')==generation:
                raise Refusal('cannot cleanup current checkpoint')
            directory=self.root/('generation-'+generation); no_symlink(directory)
            owner=read_meta(directory/'OWNER.json')
            if owner.get('owner')!=self.owner['owner'] or owner.get('generation')!=generation: raise Refusal('foreign generation')
            planned={i['name']:i for i in owner.get('members',[])}
            allowed={'OWNER.json','MANIFEST.json'}|set(planned)
            entries=list(directory.iterdir())
            staged=self.root/('CURRENT-'+generation+'.tmp')
            if staged.exists():
                pointer=read_meta(staged)
                if pointer.get('version')!=VERSION or pointer.get('owner')!=self.owner['owner'] or pointer.get('generation')!=generation:
                    raise Refusal('unrelated staged pointer; refuse cleanup')
            for entry in entries:
                if entry.name not in allowed:
                    raise Refusal('unrelated file in generation; refuse cleanup')
                if entry.is_symlink() or not entry.is_file(): raise Refusal('nonregular cleanup target')
                if entry.name in planned:
                    stamp=digest_file(entry)
                    if any(stamp[k]!=planned[entry.name][k] for k in ['sha256','bytes','dev','ino']):
                        raise Refusal('cannot prove cleanup member ownership/integrity')
            for entry in entries: entry.unlink()
            if staged.exists(): staged.unlink()
            directory.rmdir(); sync_dir(self.root)
