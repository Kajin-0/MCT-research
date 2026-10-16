"""Prospective predicates only. NO service/launch/native-admission entry point.

Actual peers/pidfds, model terminal snapshots. The production caller/native
final hook is absent; passing these tests cannot authorize QE or any process.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import os
import sys

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'qe75_streaming_2026-10-11'
for folder in ['runtime_admission','checkpoint_phase','cgroup_owned_2026-10-13']:
    sys.path.insert(0,str(OLD/folder))
spec=importlib.util.spec_from_file_location('_r07_pinned_retirement',OLD/'terminal_owner_2026-10-14/retirement.py')
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
Peer,Refusal=legacy.Peer,legacy.Refusal
GIB=1<<30


class Attempt:
    """Error latch for ONE modeled attempt; never native execution authority.

    Production must use this lifecycle rule for every active gate and discard
    an acquisition after refusal. Independent predicate tests may catch errors
    and continue to evaluate different counterfactual branches.
    """
    def __init__(self,policy):
        self.policy=policy
        self.failed=False

    def call(self,method,*args):
        if self.failed:raise Refusal('attempt already REFUSED; cannot resurrect')
        try:return getattr(self.policy,method)(*args)
        except Exception:
            self.failed=True
            raise


class Policy:
    def __init__(self,cgroup,unit,invocation,job,profile,nonce,begin_exe,complete_exe):
        self.cgroup,self.unit,self.invocation=cgroup,unit,invocation
        self.job,self.profile,self.nonce=job,profile,nonce
        self.exe={1:Path(begin_exe).resolve(),10:Path(complete_exe).resolve()}
        self.exe_sha={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in self.exe.items()}
        self.ranks,self.final={},set()
        self.pending=False

    def receipt(self,conn):
        peer=Peer(conn,os.getuid(),self.cgroup)
        try:
            raw=b''
            while not raw.endswith(b'\n') and len(raw)<=2048:
                b=conn.recv(2048)
                if not b:raise Refusal('incomplete live receipt')
                raw+=b
            packet=json.loads(raw)
            rank,action=packet.get('rank'),packet.get('action')
            if (type(packet.get('version')) is not int or packet['version']!=1 or
                type(rank) is not int or rank not in [0,1] or type(action) is not int or action not in [1,10]):
                raise Refusal('typed rank/action')
            expected=dict(version=1,rank=rank,action=action,job=self.job,profile=self.profile,nonce=self.nonce)
            if packet!=expected:raise Refusal('wrong JOB/PROFILE/nonce; no historical receipts')
            peer.live_identity()
            executable=Path(f'/proc/{peer.pid}/exe').resolve(strict=True)
            if executable!=self.exe[action] or hashlib.sha256(executable.read_bytes()).hexdigest()!=self.exe_sha[action]:
                raise Refusal('live kernel ELF mismatch')
            if action==1:
                if self.pending or rank in self.ranks or peer.pid in [p.pid for p in self.ranks.values()]:
                    raise Refusal('duplicate/replaced rank or pending acquisition')
                self.ranks[rank]=peer;peer=None
            else:
                if set(self.ranks)!={0,1} or rank in self.final:raise Refusal('missing/duplicate final pair')
                registered=self.ranks[rank];registered.live_identity()
                if (peer.pid,peer.start_ticks)!=(registered.pid,registered.start_ticks):
                    raise Refusal('different kernel process final')
                self.final.add(rank)
            conn.sendall(b'OK\n')
        finally:
            if peer is not None:peer.close()

    def inventory_failure(self,pid,error):
        if not isinstance(error,(PermissionError,FileNotFoundError,ProcessLookupError)):
            raise Refusal('non-FD failure cannot enter retirement')
        candidates=[p for p in self.ranks.values() if p.pid==pid]
        if len(candidates)!=1 or self.final!={0,1}:raise Refusal('unbound task or missing LIVE final pair')
        if not candidates[0].exited():raise Refusal('FD denial for STILL LIVE registered rank')
        self.pending=True
        return 'TERMINAL_PENDING_NOT_ACCEPTED'

    def terminal_model(self,manager,cgroup_state,resources):
        """Injected observations ONLY; not an authenticated manager API.

        Production must read retained-unit/CG inode/FD/accounting itself. A
        caller's JSON or these model snapshots never grant a launch/omission.
        """
        if not self.pending or self.final!={0,1} or set(self.ranks)!={0,1}:
            raise Refusal('terminal transition not established')
        if not all(p.exited() for p in self.ranks.values()):raise Refusal('terminal rank still live')
        expected=dict(Id=self.unit,InvocationID=self.invocation,LoadState='loaded',ActiveState='inactive',
            SubState='dead',Result='success',ExecMainCode='1',ExecMainStatus='0',MainPID='0',Restart='no',Delegate='no')
        if any(manager.get(k)!=v for k,v in expected.items()):raise Refusal('manager identity/exit mismatch')
        if cgroup_state not in ['ABSENT_PINNED_INVOCATION','EMPTY_SAME_INODE']:
            raise Refusal('unknown/reused/populated cgroup')
        caps=dict(memory_max=12*GIB,swap_max=0,tasks_max=12)
        if any(type(resources.get(k)) is not int or resources[k]!=v for k,v in caps.items()):
            raise Refusal('hard caps changed/unknown')
        required=['rss_B','host_available_B','disk_available_B','output_B','elapsed_s','oom_events','task_events']
        integer_fields=[k for k in required if k!='elapsed_s']
        if any(type(resources.get(k)) is not int or not 0<=resources[k]<2**63 for k in integer_fields):
            raise Refusal('resource integer64 observation incomplete/overflow')
        if type(resources.get('elapsed_s')) not in [int,float] or not math.isfinite(resources['elapsed_s']):
            raise Refusal('elapsed observation incomplete/nonfinite')
        if not (0<=resources['rss_B']<=12*GIB and resources['host_available_B']>=4*GIB
            and resources['disk_available_B']>=10*GIB and 0<=resources['output_B']<=14*GIB
            and 0<=resources['elapsed_s']<600 and resources['oom_events']==resources['task_events']==0):
            raise Refusal('resource threshold/event failure')
        return 'MODEL_CONJUNCTION_ONLY_NO_NATIVE_AUTHORITY'

    def close(self):
        for p in self.ranks.values():p.close()
