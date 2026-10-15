"""GPL-2.0-or-later. Strict, bounded resource admission and tiny reservation tests.

No MPI/QE launch. An unreadable quota is UNKNOWN and refuses native admission.
Kernel reservation tests alone do not certify residual quota headroom for QE's
other output/state. No interpretation of EPERM as 'unlimited' is allowed.
"""
from __future__ import annotations
import ctypes
import errno
import math
import os
from pathlib import Path
import stat

from checkpoint_capsule import Refusal,BASE

I64=(1<<63)-1
GIB=1<<30
MIN_DISK_RESERVE=10*GIB
MAX_FAMILY_RAM=12*GIB
SYSTEM_RAM_RESERVE=4*GIB
MAX_WALL_SECONDS=600


class Quota(ctypes.Structure):
    _fields_=[('error',ctypes.c_int32),('active',ctypes.c_int32),
              ('used_bytes',ctypes.c_uint64),('hard_blocks_1024',ctypes.c_uint64),
              ('soft_blocks_1024',ctypes.c_uint64),('valid',ctypes.c_uint32),('padding',ctypes.c_uint32),
              ('limit_error',ctypes.c_int32),('status_error',ctypes.c_int32)]


class Storage(ctypes.Structure):
    _fields_=[('fs_type',ctypes.c_uint64),('block_bytes',ctypes.c_uint64),
              ('available_blocks',ctypes.c_uint64),('available_bytes',ctypes.c_uint64),
              ('quotas',Quota*3),('project_error',ctypes.c_int32),('project_id',ctypes.c_uint32)]


def integer(value):
    if type(value) is not int or not 0<=value<=I64: raise Refusal('invalid/overflow signed 64-bit extent')
    return value


def add(a,b):
    value=integer(a)+integer(b)
    return integer(value)


def multiply(a,b):
    value=integer(a)*integer(b)
    return integer(value)


def round_blocks(bytes_,block):
    bytes_=integer(bytes_); block=integer(block)
    if block<=0 or bytes_<=0: raise Refusal('nonpositive reservation extent/block')
    return multiply(bytes_//block+(bytes_%block!=0),block)


def quota_headroom(quota):
    if quota['error']==errno.ESRCH and not quota['active']: return None # type not enabled
    if quota['error'] or not quota['active']: raise Refusal('quota status UNKNOWN: errno='+str(quota['error']))
    # Linux QIF_BLIMITS=1 and QIF_SPACE=2 must both be returned.
    if quota['valid']&3!=3: raise Refusal('incomplete quota limit/usage fields')
    used=integer(quota['used_bytes'])
    limits=[multiply(x,1024) for x in [quota['hard_blocks_1024'],quota['soft_blocks_1024']] if x]
    if not limits: return None # queried active quota with zero block limits
    return max(0,min(limits)-used) # no reliance on soft-limit grace


def admission(info,rank_bytes,output_envelope_bytes,mem_available_bytes,family_rss_bytes=0):
    if info.get('probe_errno',0): raise Refusal('filesystem probe refused: errno='+str(info['probe_errno']))
    if info['fs_type']!=0xef53: raise Refusal('tmpfs/unknown/non-ext4 backend refused')
    if info['project_error']: raise Refusal('project identity UNKNOWN')
    block=integer(info['block_bytes'])
    available=multiply(info['available_blocks'],block)
    if available!=info['available_bytes']: raise Refusal('inconsistent block accounting')
    if not rank_bytes or len(rank_bytes)>64: raise Refusal('invalid bounded rank set')
    total=round_blocks(output_envelope_bytes,block)
    for value in rank_bytes: total=add(total,round_blocks(value,block))
    required=add(total,MIN_DISK_RESERVE)
    if available<required: raise Refusal('10-GiB physical disk reserve would be violated')
    if len(info['quotas'])!=3: raise Refusal('incomplete quota type inventory')
    for kind,quota in zip(['user','group','project'],info['quotas']):
        headroom=quota_headroom(quota)
        if headroom is not None and headroom<total: raise Refusal(kind+' quota admission failed')
    if integer(mem_available_bytes)<add(MAX_FAMILY_RAM,SYSTEM_RAM_RESERVE):
        raise Refusal('insufficient physical RAM for 12-GiB family + 4-GiB system reserve')
    if integer(family_rss_bytes)>MAX_FAMILY_RAM: raise Refusal('12-GiB family RAM cap crossed')
    return {'admitted':True,'rounded_reservation_bytes':total,'min_disk_reserve_bytes':MIN_DISK_RESERVE,
            'max_family_ram_bytes':MAX_FAMILY_RAM,'max_wall_seconds':MAX_WALL_SECONDS}


def live_limits(info,mem_available_bytes,family_rss_bytes,elapsed_seconds):
    if info.get('probe_errno',0): raise Refusal('runtime filesystem probe failed')
    if integer(info['available_bytes'])<MIN_DISK_RESERVE: raise Refusal('runtime disk reserve crossed')
    if integer(family_rss_bytes)>MAX_FAMILY_RAM: raise Refusal('runtime family RAM cap crossed')
    if integer(mem_available_bytes)<SYSTEM_RAM_RESERVE: raise Refusal('runtime system RAM reserve crossed')
    if not math.isfinite(elapsed_seconds) or elapsed_seconds<0: raise Refusal('invalid wall telemetry')
    if elapsed_seconds>=MAX_WALL_SECONDS: raise Refusal('runtime wall cap crossed')


class LinuxGuard:
    def __init__(self,library):
        library=Path(library).resolve()
        if not library.is_relative_to(BASE): raise Refusal('project-local library required')
        self.lib=ctypes.CDLL(str(library))
        self.lib.qe_storage_probe.argtypes=[ctypes.c_int,ctypes.POINTER(Storage)]
        self.lib.qe_storage_probe.restype=ctypes.c_int
        self.lib.qe_reserve_fd.argtypes=[ctypes.c_int,ctypes.c_int64,ctypes.POINTER(ctypes.c_int64)]
        self.lib.qe_reserve_fd.restype=ctypes.c_int

    def probe_fd(self,fd):
        result=Storage(); code=self.lib.qe_storage_probe(fd,ctypes.byref(result))
        return {'probe_errno':code,**{k:getattr(result,k) for k in ['fs_type','block_bytes','available_blocks','available_bytes','project_error','project_id']},
                'quotas':[{k:getattr(q,k) for k,t in Quota._fields_ if k!='padding'} for q in result.quotas]}

    def probe(self,path):
        fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try: return self.probe_fd(fd)
        finally: os.close(fd)

    def reserve(self,capsule,rank_bytes,output_envelope_bytes,mem_available_bytes):
        """One serialized coordinator, exact per-rank files, no silent fallback.

        Sidecars/native output must stay inside the separately bounded envelope;
        this is not a quota guarantee for unbounded QE output. Unknown inventory
        refuses before creating any rank store. Only newly owned inodes roll back.
        """
        with capsule.locked():
            info=self.probe(capsule.root/'live')
            policy=admission(info,rank_bytes,output_envelope_bytes,mem_available_bytes)
            created=[]
            try:
                for rank,size in enumerate(rank_bytes):
                    path=capsule.member(rank,'stream')
                    fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
                    record={'path':path,'fd':fd,'ino':os.fstat(fd).st_ino}; created.append(record)
                    # Query actual new inode's owner/group/project, not only parent.
                    actual=self.probe_fd(fd)
                    for quota in actual['quotas']: quota_headroom(quota)
                    allocated=ctypes.c_int64()
                    code=self.lib.qe_reserve_fd(fd,integer(size),ctypes.byref(allocated))
                    if code: raise Refusal('reservation refused: errno='+str(code))
                    record['logical_bytes']=size; record['allocated_bytes']=allocated.value
                    if self.probe(capsule.root/'live')['available_bytes']<MIN_DISK_RESERVE:
                        raise Refusal('post-reservation disk reserve crossed')
                return {**policy,'rank_files':[{k:str(v) if isinstance(v,Path) else v for k,v in item.items() if k!='fd'} for item in created]}
            except BaseException:
                for item in created:
                    path=item['path']
                    if path.exists() and not path.is_symlink() and path.stat().st_ino==item['ino']:
                        path.unlink()
                raise
            finally:
                for item in created: os.close(item['fd'])
