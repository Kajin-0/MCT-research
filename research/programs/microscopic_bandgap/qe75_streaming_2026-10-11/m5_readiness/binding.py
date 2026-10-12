"""Typed dual-digest lease contract. Component evidence never grants QE admission."""
from pathlib import Path
import hashlib
import os
import re
import socket
import struct
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'runtime_admission'))
from family_runtime import encode,read_meta,Refusal
from native_bundle import artifact_sha256
from process_identity import Identity,proc,pin_descendant,table

REQUEST=struct.Struct('!4sIIII64s64s32s')
REPLY=struct.Struct('!4sIII32s')
MAGIC=b'R07L';VERSION=1
REGISTER=1;CHECK=2
SCOPE_ABI_NO_MPI=1;SCOPE_NATIVE=2


def digest(value): return hashlib.sha256(encode(value)).hexdigest()


def pair(job,profile):
    if type(job.get('version')) is not int or job['version']!=2 or type(job.get('binding_version')) is not int or job['binding_version']!=1:
        raise Refusal('typed JOB version missing')
    if job.get('profile_sha256')!=digest(profile): raise Refusal('PROFILE/JOB binding mismatch')
    if type(job.get('rank_count')) is not int or job['rank_count']!=2: raise Refusal('two native world ranks required')
    if not re.fullmatch('[0-9a-f]{64}',job['profile_sha256']): raise Refusal('PROFILE digest encoding')
    return {'job_sha256':digest(job),'profile_sha256':digest(profile)}


def load_pair(root):
    root=Path(root)
    return pair(read_meta(root/'JOB.json'),read_meta(root/'PROFILE.json'))


class RankRegistry:
    """Actual kernel peers, exact compiled executable, two live unique identities.

    This component server issues only ABI_NO_MPI receipts. The compiled native
    QE wrapper demands NATIVE, so these receipts cannot release it into SCF.
    Native admission remains absent until all retained gates are qualified.
    """
    def __init__(self,job,profile,parent_pid,executable):
        self.identities=pair(job,profile)
        if job['kind']!='EXPLICIT_COMPILED_ABI_NO_MPI': raise Refusal('native admission unissued')
        self.parent=parent_pid;self.exe=Path(executable).resolve();self.exe_sha=artifact_sha256(self.exe)
        if job.get('executable_sha256')!=self.exe_sha: raise Refusal('compiled peer executable pin mismatch')
        self.ranks={};self.history=[]

    def handle(self,peer_uid,peer_pid,raw):
        if len(raw)!=REQUEST.size: raise Refusal('wire extent mismatch')
        magic,version,action,rank,size,jhash,phash,challenge=REQUEST.unpack(raw)
        if magic!=MAGIC or version!=VERSION: raise Refusal('wire version/magic')
        if (jhash.decode('ascii'),phash.decode('ascii'))!=(self.identities['job_sha256'],self.identities['profile_sha256']):
            raise Refusal('wire JOB/PROFILE digest mismatch')
        if peer_uid!=os.getuid(): raise Refusal('kernel UID mismatch')
        if size!=2 or rank not in [0,1]: raise Refusal('world rank/size mismatch')
        exe=Path(os.readlink(f'/proc/{peer_pid}/exe')).resolve()
        if exe!=self.exe or artifact_sha256(exe)!=self.exe_sha: raise Refusal('kernel compiled executable mismatch')
        identity=pin_descendant(peer_pid,self.parent,table())
        try:
            record=identity.record()
            if action==REGISTER:
                if rank in self.ranks and self.ranks[rank].record()!=record: raise Refusal('rank identity replacement')
                if any(r!=rank and ident.record()==record for r,ident in self.ranks.items()):
                    raise Refusal('one process cannot register two world ranks')
                if rank not in self.ranks: self.ranks[rank]=identity;identity=None
            elif action==CHECK:
                if rank not in self.ranks or self.ranks[rank].record()!=record: raise Refusal('unregistered checking peer')
                if set(self.ranks)!={0,1} or not all(p.live() for p in self.ranks.values()):
                    return REPLY.pack(MAGIC,VERSION,11,SCOPE_ABI_NO_MPI,challenge)
            else: raise Refusal('wire operation')
            self.history.append({'peer':record,'world_rank':rank,'action':action,'scope':'ABI_NO_MPI'})
            return REPLY.pack(MAGIC,VERSION,0,SCOPE_ABI_NO_MPI,challenge)
        finally:
            if identity is not None: identity.close()

    def close(self):
        for identity in self.ranks.values(): identity.close()


def native_admission():
    raise Refusal('M5 native admission unissued: actual two-rank collectives, state/common-wave/layout/inventory gates not qualified')
