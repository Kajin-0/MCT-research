"""Private bridge candidate: bind closed native files after punch, no data copies.

No QE/MPI launch entry point. Qualification is deliberately false until a native
action/energy/restart comparison passes. CLI is called only by a gated private
source hook; tests use explicitly synthetic native-file stand-ins.
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
import struct
import sys
import uuid
import ctypes
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'checkpoint_phase'))
from checkpoint_capsule import (Refusal, InjectedFailure, BASE, digest_file,
                                durable_bytes, encode, read_meta, no_symlink, sync_dir)
from resource_guard import LinuxGuard, admission,quota_headroom,integer,live_limits

VERSION='qe75-native-bridge-candidate-v2'
MAGIC=b'QE75-EXX-STATE02'
SENTINEL=0x0102030405060708


def artifact_sha256(path):
    """Read-only fingerprint for system/private code, not payload ownership."""
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        before=os.fstat(fd)
        if not stat.S_ISREG(before.st_mode): raise Refusal('nonregular runtime artifact')
        value=hashlib.sha256()
        while True:
            chunk=os.read(fd,1024*1024)
            if not chunk: break
            value.update(chunk)
        after=os.fstat(fd)
        if (before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_ino,after.st_size,after.st_mtime_ns):
            raise Refusal('runtime artifact changed during fingerprint')
        return value.hexdigest()
    finally: os.close(fd)


def packet_header(path):
    """Inspect bounded metadata only; payload integrity is checked separately."""
    with open(path,'rb') as f:
        raw=f.read(152)
        if len(raw)!=152 or raw[:16]!=MAGIC: raise Refusal('packet magic/extent')
        h=struct.unpack('=9q',raw[16:88])
        if h[0]!=2 or h[1]!=SENTINEL: raise Refusal('packet version/native byte order')
        if any(x<=0 or x>10000000 for x in h[2:]): raise Refusal('packet shape bounds')
        if h[2]>2000000: raise Refusal('layout metadata limit')
        fingerprint=raw[88:152].decode('ascii')
        if not re.fullmatch('[0-9a-f]{64}',fingerprint): raise Refusal('packet fingerprint')
        raw=f.read(h[2]*8+16+72)
        if len(raw)!=h[2]*8+88: raise Refusal('packet header truncated')
        layout=struct.unpack('='+str(h[2])+'q',raw[:h[2]*8])
        mode,iteration=struct.unpack('=2q',raw[h[2]*8:h[2]*8+16])
        scalars=struct.unpack('=9d',raw[h[2]*8+16:])
        import math
        if mode not in (1,2) or iteration<0 or not all(map(math.isfinite,scalars)):
            raise Refusal('packet stop/outer state')
        size=16+72+64+8*h[2]+16+72+8*h[3]*h[4]+16*h[5]*h[6]+16*h[7]*h[5]*h[8]
        if size>=2**63 or os.fstat(f.fileno()).st_size!=size: raise Refusal('packet exact extent')
        return {'fingerprint':fingerprint,'layout':list(layout[:20]),
                'layout_sha256':hashlib.sha256(raw[:h[2]*8]).hexdigest(),'nlayout':h[2],'mode':mode,
                'iteration':iteration,'scalars':list(scalars),'shape':list(h[3:])}


class NativeBundle:
    def __init__(self,root):
        self.root=Path(root).absolute()
        if not self.root.is_relative_to(BASE): raise Refusal('project-local root required')
        no_symlink(self.root)
        self.owner=read_meta(self.root/'BRIDGE_OWNER.json')
        if self.owner.get('version')!=VERSION or self.owner.get('uid')!=os.getuid():
            raise Refusal('owner/version refused')
        self.profile=read_meta(self.root/'PROFILE.json')
        self.out=self.root/'out'
        no_symlink(self.out)
        if self.profile.get('native_qualified') is not False: raise Refusal('unearned native qualification')
        if not re.fullmatch('[a-zA-Z0-9_-]{1,40}',self.profile['prefix']): raise Refusal('prefix refused')
        if type(self.profile['ranks']) is not int or not 1<=self.profile['ranks']<=6: raise Refusal('rank bound')
        if not self.profile.get('provenance'): raise Refusal('missing provenance')

    @classmethod
    def create(cls,root,profile):
        root=Path(root).absolute()
        if not root.is_relative_to(BASE): raise Refusal('project-local root required')
        no_symlink(root.parent)
        root.mkdir(mode=0o700,exist_ok=False)
        durable_bytes(root/'BRIDGE_OWNER.json',encode({'version':VERSION,'uid':os.getuid(),'id':uuid.uuid4().hex}))
        durable_bytes(root/'PROFILE.json',encode(profile))
        (root/'out').mkdir(mode=0o700)
        sync_dir(root);sync_dir(root.parent)
        return cls(root)

    @contextmanager
    def locked(self):
        fd=os.open(self.root/'BRIDGE_LOCK',os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
        try:
            try: fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError as e: raise Refusal('bridge already owned') from e
            yield
        finally: os.close(fd)

    def inventory(self):
        p=self.profile['prefix']; ranks=self.profile['ranks']
        files=[]; packets=[]
        save=self.out/(p+'.save');no_symlink(save)
        if not save.is_dir(): raise Refusal('post-punch native save absent')
        for path in sorted(save.rglob('*')):
            no_symlink(path)
            if path.is_file(): files.append(path)
            elif not path.is_dir(): raise Refusal('nonregular native save')
        # State closure requires native density/schema and each k's waves+ACE.
        names={path.name for path in files}
        if 'data-file-schema.xml' not in names: raise Refusal('native schema absent')
        if not any(n in names for n in ['charge-density.dat','charge-density.hdf5']):
            raise Refusal('native density absent')
        if not self.profile.get('pseudopotentials'): raise Refusal('PP provenance absent')
        for name,sha256 in self.profile['pseudopotentials'].items():
            if '/' in name or not name.endswith('.UPF'): raise Refusal('PP filename refused')
            if digest_file(save/name)['sha256']!=sha256: raise Refusal('native saved PP mismatch')
        for k in range(1,self.profile['nks']+1):
            for role in ['wfc','ace']:
                if not any(role+str(k)+ext in names for ext in ['.dat','.hdf5']):
                    raise Refusal('collected current waves/old ACE absent')
        for rank in range(ranks):
            for role in ['exx_qstream','exx_state']:
                path=self.out/f'{p}.{role}.{rank}'
                if not path.is_file(): raise Refusal('missing rank/operator packet')
                no_symlink(path);files.append(path)
            packets.append(packet_header(self.out/f'{p}.exx_state.{rank}'))
        fingerprint=hashlib.sha256(encode(self.profile)).hexdigest()
        if any(packet['fingerprint']!=fingerprint for packet in packets):
            raise Refusal('packet/profile mismatch')
        # Counters and old outer scalars are replicated, not rank-dependent.
        common=['mode','iteration','scalars']
        if any(any(a[k]!=packets[0][k] for k in common) for a in packets):
            raise Refusal('cross-rank outer state mismatch')
        for rank,packet in enumerate(packets):
            # Exact stream shape comes from native packet's actual layout.
            layout=packet['layout']
            if len(layout)<20 or layout[0]!=rank or layout[1]!=ranks:
                raise Refusal('rank/layout mismatch')
            extent=16*layout[2]*layout[3]*layout[4]
            if extent<=0 or extent>=2**63 or (self.out/f'{p}.exx_qstream.{rank}').stat().st_size!=extent:
                raise Refusal('operator extent mismatch')
        for path in sorted(self.out.iterdir()):
            # Native mixing and restart_scf/k are closed at capture. Raw wfc
            # direct-access buffers remain open; use collected waves instead.
            if re.fullmatch(re.escape(p)+r'\.(mix|restart_scf|restart_k)(\d*)',path.name):
                no_symlink(path);files.append(path)
        if packets[0]['mode']==1:
            for rank in range(ranks):
                suffix='' if rank==0 else str(rank+1)
                if not (self.out/f'{p}.restart_scf{suffix}').is_file():
                    raise Refusal('inner SCF counter/threshold absent')
                # Iteration 0 has no mixing history; it is a native cold inner
                # resume, with unchanged old operator, not a vanished history.
                counter=(self.out/f'{p}.restart_scf{suffix}').read_text().split()[0]
                if int(counter)>0 and not (self.out/f'{p}.mix{rank+1}').is_file():
                    raise Refusal('inner mixing history absent')
        elif any(re.fullmatch(re.escape(p)+r'\.(mix|restart_scf|restart_k)(\d*)',path.name)
                 for path in self.out.iterdir()):
            raise Refusal('stale inner history at outer boundary')
        return files,packets

    def guard(self):
        # The library is private DFT build output, never an installed system lib.
        library=Path(self.profile['guard_library'])
        guard=LinuxGuard(library)
        mem={k:int(v.split()[0])*1024 for k,v in
             (line.split(':',1) for line in Path('/proc/meminfo').read_text().splitlines())}
        admission(guard.probe(self.out),[1],1024*1024,mem['MemAvailable'])

    def publish(self,fail_at=None):
        with self.locked():
            if (self.root/'CURRENT_NATIVE.json').exists(): raise Refusal('unconsumed native checkpoint')
            self.guard()
            files,packets=self.inventory()
            gen=uuid.uuid4().hex; directory=self.root/('native-'+gen)
            directory.mkdir(mode=0o700)
            members=[]
            for path in files:
                relative=str(path.relative_to(self.out))
                stamp=digest_file(path)
                members.append({'path':relative,**stamp})
            plan={'version':VERSION,'owner':self.owner['id'],'generation':gen,'members':members,
                  'profile':self.profile,'packets':packets,'native_qualified':False}
            durable_bytes(directory/'PLAN.json',encode(plan))
            for item in members:
                source=self.out/item['path'];target=directory/'tree'/item['path']
                target.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
                fd=os.open(source,os.O_RDONLY|os.O_NOFOLLOW)
                try: os.fsync(fd)
                finally: os.close(fd)
                os.link(source,target,follow_symlinks=False)
                if digest_file(target)!={k:item[k] for k in ['sha256','bytes','dev','ino']}:
                    raise Refusal('concurrent native member mutation')
                if fail_at=='member': raise InjectedFailure('member')
            # Every newly created hierarchy needs directory fsync, bottom up.
            for path in sorted((p for p in directory.rglob('*') if p.is_dir()),key=lambda p:len(p.parts),reverse=True):
                sync_dir(path)
            for path in sorted((p for p in self.out.rglob('*') if p.is_dir()),key=lambda p:len(p.parts),reverse=True):
                sync_dir(path)
            sync_dir(self.out)
            durable_bytes(directory/'MANIFEST.json',encode(plan));sync_dir(directory);sync_dir(self.root)
            if fail_at=='manifest': raise InjectedFailure('manifest')
            pointer={'generation':gen,'manifest_sha256':digest_file(directory/'MANIFEST.json')['sha256']}
            stage=self.root/('POINTER-'+gen+'.tmp');durable_bytes(stage,encode(pointer))
            if fail_at=='before_commit': raise InjectedFailure('before_commit')
            os.replace(stage,self.root/'CURRENT_NATIVE.json')
            if fail_at=='after_commit': raise InjectedFailure('after_commit')
            sync_dir(self.root)
            if fail_at=='after_sync': raise InjectedFailure('after_sync')
            return pointer

    def _verify(self):
        pointer=read_meta(self.root/'CURRENT_NATIVE.json');gen=pointer.get('generation','')
        if not re.fullmatch('[0-9a-f]{32}',gen): raise Refusal('generation refused')
        directory=self.root/('native-'+gen);no_symlink(directory)
        if digest_file(directory/'MANIFEST.json')['sha256']!=pointer.get('manifest_sha256'):
            raise Refusal('manifest checksum')
        manifest=read_meta(directory/'MANIFEST.json')
        if manifest.get('profile')!=self.profile or manifest.get('owner')!=self.owner['id']:
            raise Refusal('profile/owner changed')
        if manifest.get('generation')!=gen: raise Refusal('manifest generation mismatch')
        if manifest.get('version')!=VERSION or manifest.get('native_qualified') is not False:
            raise Refusal('version/qualification refused')
        actual,packets=self.inventory()
        if packets!=manifest['packets'] or set(map(lambda p:str(p.relative_to(self.out)),actual))!=set(i['path'] for i in manifest['members']):
            raise Refusal('native inventory changed')
        for item in manifest['members']:
            relative=Path(item['path'])
            if relative.is_absolute() or '..' in relative.parts: raise Refusal('member traversal')
            for path in [directory/'tree'/relative,self.out/relative]:
                no_symlink(path)
                if digest_file(path)!={k:item[k] for k in ['sha256','bytes','dev','ino']}:
                    raise Refusal('native member corruption/replacement')
        return directory,manifest

    def verify(self):
        with self.locked(): return self._verify()

    def consume_for_import(self,fail_at=None):
        """Verify before first QE read; retire BEFORE any native in-place write.

        Live names remain. Only snapshot hardlinks are unlinked. No rollback
        checkpoint is promised after this boundary; no payload is ever copied.
        """
        with self.locked():
            directory,manifest=self._verify()
            self.guard()
            gen=manifest['generation']
            if (self.root/'IMPORT.json').exists():
                old=read_meta(self.root/'IMPORT.json')
                if old.get('owner')!=self.owner['id']: raise Refusal('foreign import receipt')
                (self.root/'IMPORT.json').unlink();sync_dir(self.root)
            os.rename(self.root/'CURRENT_NATIVE.json',self.root/('RETIRED-'+gen+'.json'))
            sync_dir(self.root)
            if fail_at=='retired': raise InjectedFailure('retired')
            for item in manifest['members']: (directory/'tree'/item['path']).unlink()
            for path in sorted((p for p in directory.rglob('*') if p.is_dir()),key=lambda p:len(p.parts),reverse=True):
                sync_dir(path)
            sync_dir(directory)
            # No IMPORT receipt on partial retirement: early native hook refuses.
            receipt={'version':VERSION,'generation':gen,'owner':self.owner['id'],
                     'profile_sha256':hashlib.sha256(encode(self.profile)).hexdigest(),
                     'members':manifest['members'],'consumed_before_QE_read':True,'native_qualified':False}
            durable_bytes(self.root/'IMPORT.json',encode(receipt));sync_dir(self.root)
            return receipt

    def reserve_streams(self):
        """Exact per-rank native requests, checked ext4/quota blocks, no copies."""
        with self.locked():
            if (self.root/'CURRENT_NATIVE.json').exists(): raise Refusal('available checkpoint must be consumed before producer')
            p=self.profile['prefix'];fingerprint=hashlib.sha256(encode(self.profile)).hexdigest()
            requests=[];sizes=[]
            for rank in range(self.profile['ranks']):
                path=self.out/f'{p}.stream_request.{rank}';no_symlink(path)
                if path.stat().st_size>128: raise Refusal('reservation request too large')
                lines=path.read_text().splitlines()
                if len(lines)!=2 or lines[0]!=fingerprint: raise Refusal('reservation request profile')
                if not re.fullmatch('[0-9]{1,19}',lines[1]): raise Refusal('reservation extent encoding')
                size=integer(int(lines[1]))
                if size<=0: raise Refusal('empty stream reservation')
                requests.append(path);sizes.append(size)
            guard=LinuxGuard(self.profile['guard_library'])
            mem={k:int(v.split()[0])*1024 for k,v in
                 (line.split(':',1) for line in Path('/proc/meminfo').read_text().splitlines())}
            admission(guard.probe(self.out),sizes,integer(self.profile['output_envelope_bytes']),mem['MemAvailable'])
            created=[]
            try:
                for rank,size in enumerate(sizes):
                    path=self.out/f'{p}.exx_qstream.{rank}'
                    fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
                    created.append((path,fd,os.fstat(fd).st_ino))
                    for quota in guard.probe_fd(fd)['quotas']: quota_headroom(quota)
                    allocated=ctypes.c_int64()
                    code=guard.lib.qe_reserve_fd(fd,size,ctypes.byref(allocated))
                    if code: raise Refusal('native stream fallocate refused: errno='+str(code))
                    if guard.probe(self.out)['available_bytes']<10*(1<<30): raise Refusal('post-reservation disk floor')
                sync_dir(self.out)
                # Only closed, owned requests are retired after all ranks reserve.
                for path in requests: path.unlink()
                sync_dir(self.out)
            except BaseException:
                for path,fd,inode in created:
                    if path.exists() and not path.is_symlink() and path.stat().st_ino==inode: path.unlink()
                sync_dir(self.out)
                raise
            finally:
                for path,fd,inode in created: os.close(fd)
            return [{'rank':rank,'bytes':size,'inode':created[rank][2]} for rank,size in enumerate(sizes)]

    def cleanup_orphan(self,generation):
        """Only remove recorded snapshot names, never live state or foreign files."""
        with self.locked():
            if not re.fullmatch('[0-9a-f]{32}',generation): raise Refusal('cleanup generation')
            current=self.root/'CURRENT_NATIVE.json'
            if current.exists() and read_meta(current).get('generation')==generation:
                raise Refusal('cannot clean available checkpoint')
            directory=self.root/('native-'+generation);no_symlink(directory)
            plan=read_meta(directory/'PLAN.json')
            if (plan.get('owner')!=self.owner['id'] or plan.get('generation')!=generation
                or plan.get('profile')!=self.profile or plan.get('version')!=VERSION):
                raise Refusal('cleanup ownership/profile mismatch')
            recorded={item['path']:item for item in plan['members']}
            allowed={'PLAN.json','MANIFEST.json'}|{'tree/'+p for p in recorded}
            allowed_dirs={'tree'}
            for name in recorded:
                allowed_dirs.update(str(parent) for parent in Path('tree',name).parents if str(parent)!='.')
            files=[]
            for path in directory.rglob('*'):
                no_symlink(path)
                relative=str(path.relative_to(directory))
                if path.is_dir():
                    if relative not in allowed_dirs: raise Refusal('unrelated orphan directory')
                    continue
                if relative not in allowed: raise Refusal('unrelated orphan file')
                if relative.startswith('tree/'):
                    item=recorded[relative[5:]]
                    if digest_file(path)!={k:item[k] for k in ['sha256','bytes','dev','ino']}:
                        raise Refusal('orphan member ownership/integrity')
                files.append(path)
            stage=self.root/('POINTER-'+generation+'.tmp')
            if stage.exists():
                no_symlink(stage)
                staged=read_meta(stage)
                if staged.get('generation')!=generation: raise Refusal('foreign staged pointer')
            # Validate everything before deleting the first owned name.
            for path in files: path.unlink()
            for path in sorted((p for p in directory.rglob('*') if p.is_dir()),key=lambda p:len(p.parts),reverse=True):
                path.rmdir()
            if stage.exists(): stage.unlink()
            directory.rmdir();sync_dir(self.root)


def main():
    root=os.environ.get('QE75_BRIDGE_ROOT','')
    if not root: raise Refusal('owned bridge root missing')
    bundle=NativeBundle(root)
    if os.environ.get('QE75_BRIDGE_FINGERPRINT')!=hashlib.sha256(encode(bundle.profile)).hexdigest():
        raise Refusal('environment/profile fingerprint mismatch')
    # No launch or self-certification. The original runtime monitor must supply
    # a current owned-family receipt, not merely set an environment boolean.
    if bundle.profile.get('runtime_authorized') is not True:
        raise Refusal('bridge runtime not qualified for bounded fixture: admission not issued')
    if (bundle.profile['provenance'].get('kind')!='QEF_QE75_NATIVE_FIXTURE' or
        bundle.profile['provenance'].get('qe_commit')!='770a0b2d12928a67048e2f3da8d10d057e52179e'):
        raise Refusal('synthetic/unqualified source provenance cannot enter native runtime')
    expected_exe=bundle.profile.get('candidate_executable_sha256','')
    if not re.fullmatch('[0-9a-f]{64}',expected_exe): raise Refusal('native executable fingerprint absent')
    receipt=read_meta(bundle.root/'MONITOR.json')
    fingerprint=hashlib.sha256(encode(bundle.profile)).hexdigest()
    if receipt.get('owner')!=bundle.owner['id'] or receipt.get('profile_sha256')!=fingerprint:
        raise Refusal('monitor ownership/profile mismatch')
    if not 0<=time.monotonic()-receipt['monotonic']<=2: raise Refusal('stale monitor receipt')
    # Verify the monitor remains the same live process and this hook is inside
    # its explicitly owned launch ancestry. PID alone cannot establish ownership.
    monitor_pid=int(receipt['pid'])
    raw=Path(f'/proc/{monitor_pid}/stat').read_text().rsplit(')',1)[1].split()
    if raw[19]!=str(receipt['start_ticks']): raise Refusal('monitor PID reused')
    launch=Path('/proc/'+str(int(receipt['launch_pid']))+'/stat').read_text().rsplit(')',1)[1].split()
    if launch[19]!=str(receipt['launch_start_ticks']): raise Refusal('owned launch PID reused')
    pid=os.getpid();seen=set();native_pid=None
    while pid not in seen and pid>1 and pid!=int(receipt['launch_pid']):
        seen.add(pid)
        exe=Path(os.readlink(f'/proc/{pid}/exe'))
        # Only the explicitly private candidate can supply the old-state packet.
        if exe.is_relative_to(BASE) and artifact_sha256(exe)==expected_exe:
            native_pid=pid
        raw=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
        pid=int(raw[1])
    if pid!=int(receipt['launch_pid']): raise Refusal('hook outside owned MPI family')
    if native_pid is None: raise Refusal('running native binary fingerprint mismatch')
    pinned=bundle.profile.get('runtime_file_sha256',{})
    if not pinned: raise Refusal('native backend file fingerprints absent')
    loaded=set()
    for line in Path(f'/proc/{native_pid}/maps').read_text().splitlines():
        fields=line.split(maxsplit=5)
        if len(fields)==6 and fields[5].startswith('/'):
            if fields[5].endswith(' (deleted)'): raise Refusal('deleted/replaced loaded backend')
            path=Path(fields[5]).resolve()
            if '.so' in path.name: loaded.add(str(path))
    if not loaded.issubset(pinned): raise Refusal('unregistered loaded native backend')
    for name,expected in pinned.items():
        if artifact_sha256(Path(name))!=expected: raise Refusal('source/backend fingerprint mismatch')
    guard=LinuxGuard(bundle.profile['guard_library'])
    live_limits(guard.probe(bundle.out),receipt['mem_available_bytes'],receipt['family_rss_bytes'],receipt['elapsed_seconds'])
    deck=Path(os.environ.get('QE75_BRIDGE_INPUT_PATH',''))
    mode=os.environ.get('QE75_BRIDGE_MODE','')
    if bundle.profile.get('matched_decks',{}).get(digest_file(deck)['sha256'])!=mode:
        raise Refusal('native input not in preregistered matched deck set')
    control=deck.read_text().split('&CONTROL',1)
    if len(control)!=2: raise Refusal('scoped CONTROL deck convention required')
    control='\n'.join(line.split('!',1)[0] for line in control[1].split('&SYSTEM',1)[0].splitlines())
    # Deliberately narrow accepted template: one literal absolute outdir/prefix;
    # no variables, expressions or ambiguous duplicate declarations.
    for key,wanted in [('outdir',str(bundle.out)),('prefix',bundle.profile['prefix'])]:
        hits=re.findall(r'\b'+key+r"\s*=\s*['\"]([^'\"]+)['\"]",control,flags=re.I)
        if len(hits)!=1 or hits[0].rstrip('/')!=wanted.rstrip('/'):
            raise Refusal('native deck ownership path/prefix refused')
    action=sys.argv[1] if len(sys.argv)==2 else ''
    if action=='pre_import':
        if mode=='restart': bundle.consume_for_import()
        elif mode=='fresh' and not (bundle.root/'CURRENT_NATIVE.json').exists(): bundle.guard()
        else: raise Refusal('restart mode/checkpoint mismatch')
    elif action=='post_punch': bundle.publish()
    elif action=='retire_operator': bundle.reserve_streams()
    else: raise Refusal('unknown native bridge action')


if __name__=='__main__': main()
