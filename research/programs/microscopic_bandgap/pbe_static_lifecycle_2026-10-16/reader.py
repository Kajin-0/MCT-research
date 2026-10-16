"""Strict lifecycle-only readback. Never imports a QE/science packet reader."""
import json
import os
from pathlib import Path
from protocol import Refusal,sha

KIND='R07_MPI_LIFECYCLE_NON_SCIENCE_V1'
KEYS={'kind','scope','rank','size','pid','uid','start_ticks','invocation','job','profile','nonce',
      'cgroup','sum','gather','collective_error'}

def decode(path):
    path=Path(path)
    if path.is_symlink() or not 0<path.stat().st_size<=3072:raise Refusal('lifecycle packet extent/type')
    def unique(pairs):
        result={}
        for k,v in pairs:
            if k in result:raise Refusal('duplicate lifecycle key')
            result[k]=v
        return result
    j=json.loads(path.read_bytes(),object_pairs_hook=unique)
    if (set(j)!=KEYS or j['kind']!=KIND or j['scope']!=1601 or j['size']!=2
        or type(j['rank']) is not int or j['rank'] not in [0,1]
        or any(type(j[k]) is not int for k in ['pid','uid','start_ticks','scope','size','sum','collective_error'])
        or j['sum']!=3 or j['gather']!=[0,1] or j['collective_error']!=0):
        raise Refusal('not a valid NON_SCIENCE lifecycle packet')
    return j

def inspect(root,profile,peers):
    # JOB/PROFILE/invocation/nonce are authenticated in the actual socket
    # protocol as well. Compare packet copies independently to fresh JOB here.
    job=json.loads((root/'JOB.json').read_text())
    rows={}
    for rank in [0,1]:
        path=root/'pilot'/f'H.rank{rank}';j=decode(path);p=peers[rank]
        expected=dict(rank=rank,pid=p.pid,uid=os.getuid(),start_ticks=p.start_ticks,cgroup=p.cgroup,
            profile=job['profile_sha256'],job=job['job_sha256'],nonce=job['nonce'])
        if any(j[k]!=v for k,v in expected.items()):raise Refusal('lifecycle packet kernel/JOB mismatch')
        if j['invocation']!=profile['_live_invocation']:raise Refusal('lifecycle packet invocation mismatch')
        rows[str(rank)]=dict(packet=j,sha256=sha(path))
    return dict(kind=KIND,science_release=False,ranks=rows)
