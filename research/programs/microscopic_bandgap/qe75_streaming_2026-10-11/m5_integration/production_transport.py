"""M4 guardian adapter for the compiled native wire ABI and owned child hooks.

Only ABI_NO_MPI is currently admissible. Native admission is a separate,
fail-closed gate; a PROFILE flag or a serialized receipt cannot grant it.
"""
from pathlib import Path
import os
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'m5_readiness'))
from binding import (RankRegistry,REQUEST,REPLY,MAGIC,VERSION,SCOPE_ABI_NO_MPI,
                     load_pair,native_admission,digest)
from family_runtime import Refusal,read_meta,encode,PRIVATE,LIB
from native_bundle import artifact_sha256
from process_identity import proc,table

BUILD=PRIVATE.parent/'m5_integration'
KIND='EXPLICIT_COMPILED_ABI_NO_MPI'


def required_files():
    runtime=HERE.parent/'runtime_admission'
    return [HERE/'production_transport.py',HERE/'fixture_launcher.py',HERE/'fixture_hook.py',HERE/'rank_worker.c',
            HERE.parent/'m5_readiness/binding.py',HERE.parent/'m5_readiness/lease_client.c',
            runtime/'family_runtime.py',runtime/'process_identity.py',runtime/'runtime_client.py',
            runtime/'exec_worker.py',Path(sys.executable).resolve(),BUILD/'rank_worker',LIB]


def verify_typed_job(root,job):
    if job.get('kind')=='QEF_QE75_NATIVE_FIXTURE':
        native_admission() # no issued native policy; never a Boolean bypass
    if job.get('kind')!=KIND: raise Refusal('typed job kind unregistered')
    binding=load_pair(root)
    profile=read_meta(Path(root)/'PROFILE.json')
    expected={'kind':'PRODUCTION_TRANSPORT_ABI_NO_MPI','rank_count':2,'native_qualified':False,
              'executable_sha256':artifact_sha256(BUILD/'rank_worker')}
    if profile!=expected: raise Refusal('exact transport PROFILE mismatch')
    if job.get('executable_sha256')!=expected['executable_sha256']:
        raise Refusal('compiled transport executable mismatch')
    if set(job.get('files',{}))!=set(map(str,required_files())):
        raise Refusal('exact transport source/backend allowlist mismatch')
    if job.get('scenario') not in ['normal','hold','native_scope','bad_job','bad_profile',
                                  'bad_ticks','duplicate','dead_rank','forged_hook']:
        raise Refusal('unregistered transport scenario')
    if job.get('fault') is not None: raise Refusal('transport fault must be an explicit worker scenario')
    if job.get('rank_shapes')!=[[3,2,2],[3,2,2]] or job.get('output_envelope_bytes')!=262144:
        raise Refusal('transport fixture allocation cannot be enlarged')
    if job.get('bridge_owner')!=job.get('id'): raise Refusal('typed bridge ownership mismatch')
    return binding


class ProductionTransport:
    def __init__(self,family):
        verify_typed_job(family.root,family.job)
        self.family=family
        self.registry=RankRegistry(family.job,read_meta(family.root/'PROFILE.json'),
                                   os.getpid(),BUILD/'rank_worker')
        self.binding=self.registry.identities
        self.hooks=[]

    def wire(self,uid,pid,raw):
        # This is called inside the real guardian, with SO_PEERCRED identity.
        self.family.discover()
        if pid not in self.family.members or not self.family.members[pid].live():
            raise Refusal('wire peer outside pinned guardian family')
        reply=self.registry.handle(uid,pid,raw)
        self.family.ranks={rank:identity.record() for rank,identity in self.registry.ranks.items()}
        self.family.measure()
        return reply

    def hook(self,pid,payload):
        f=self.family;f.discover()
        if pid not in f.members or not f.members[pid].live(): raise Refusal('hook outside pinned owned family')
        if payload.get('action')!='bridge_authorize': raise Refusal('typed hook operation refused')
        for key,value in self.binding.items():
            if payload.get(key)!=value: raise Refusal('hook JOB/PROFILE digest mismatch')
        if set(self.registry.ranks)!={0,1} or not all(i.live() for i in self.registry.ranks.values()):
            raise Refusal('hook requires two live registered ranks')
        command=Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
        script=HERE/'fixture_hook.py'
        if len(command)<3 or os.fsdecode(command[1])!=str(script) or os.fsdecode(command[2])!=str(f.root):
            raise Refusal('hook command not allowlisted')
        executable=Path(os.readlink(f'/proc/{pid}/exe')).resolve()
        if executable!=Path(sys.executable).resolve() or artifact_sha256(executable)!=f.job['files'][str(executable)]:
            raise Refusal('hook interpreter mismatch')
        if artifact_sha256(script)!=f.job['files'][str(script)]: raise Refusal('hook source changed')
        # No argv rank, Boolean, environment token or stored MONITOR file is
        # ancestry authority. Every parent identity is rechecked against the
        # guardian's pinned family, ending at an actual registered C process.
        ranks={identity.pid:rank for rank,identity in self.registry.ranks.items()}
        current=pid;seen=set();rank=None
        while current!=os.getpid():
            if current in seen: raise Refusal('cyclic hook lineage')
            seen.add(current)
            identity=f.members.get(current)
            row=identity.row() if identity else None
            if row is None or row['state']=='Z': raise Refusal('hook lineage changed or unpinned')
            if current in ranks:
                rank=ranks[current];break
            current=row['ppid']
        if rank is None: raise Refusal('hook not descended from a live registered rank')
        guardian=proc(os.getpid());leader=f.launch_identity
        if not leader.live(): raise Refusal('owned launcher disappeared')
        measured=f.measure()
        receipt={'ok':True,**measured,**self.binding,'scope':SCOPE_ABI_NO_MPI,
                 'owner':f.job['bridge_owner'],'pid':guardian['pid'],'start_ticks':guardian['start_ticks'],
                 'launch_pid':leader.pid,'launch_start_ticks':leader.start_ticks,
                 'native_pid':self.registry.ranks[rank].pid,'world_rank':rank,'rank_registration':f.ranks}
        self.hooks.append({'peer':f.members[pid].record(),'world_rank':rank,'scope':'ABI_NO_MPI',
                           'job_sha256':self.binding['job_sha256'],'profile_sha256':self.binding['profile_sha256']})
        return receipt

    def close(self): self.registry.close()


def create_job(root,scenario='normal',wall=3.):
    import uuid
    from family_runtime import no_symlink,durable_bytes,sync_dir
    root=Path(root).absolute();no_symlink(root.parent)
    if not root.is_relative_to(PRIVATE): raise Refusal('private runtime root required')
    root.mkdir(mode=0o700,exist_ok=False)
    profile={'kind':'PRODUCTION_TRANSPORT_ABI_NO_MPI','rank_count':2,'native_qualified':False,
             'executable_sha256':artifact_sha256(BUILD/'rank_worker')}
    ident=uuid.uuid4().hex
    job={'version':2,'binding_version':1,'kind':KIND,'id':ident,'bridge_owner':ident,
         'uid':os.getuid(),'root':str(root),'rank_count':2,'rank_shapes':[[3,2,2],[3,2,2]],
         'rank_bytes':[192,192],'output_envelope_bytes':262144,'wall_seconds':wall,
         'rss_cap_bytes':256*(1<<20),'scenario':scenario,'fault':None,
         'profile_sha256':digest(profile),'executable_sha256':profile['executable_sha256'],
         'files':{str(p):artifact_sha256(p) for p in required_files()}}
    durable_bytes(root/'PROFILE.json',encode(profile));durable_bytes(root/'JOB.json',encode(job))
    for name in ['scratch','out','logs']: (root/name).mkdir(mode=0o700)
    sync_dir(root);return job
