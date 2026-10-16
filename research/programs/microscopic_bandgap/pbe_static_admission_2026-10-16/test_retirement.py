"""Bounded real child/pidfd/FD tests, explicitly modeled manager/CG tests."""
from pathlib import Path
import json
import os
import select
import socket
import subprocess
import sys
import tempfile
from retirement_model import Policy,Attempt,Peer,Refusal,legacy,GIB

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]


def refused(f,contains=None):
    try:f()
    except (Refusal,PermissionError,FileNotFoundError,ProcessLookupError) as e:
        if contains:assert contains in str(e),repr(e)
        return type(e).__name__+': '+str(e)
    raise AssertionError('expected fail-closed refusal')


def main():
    base=REPO/'.tmp/r07ps16';base.mkdir(parents=True,exist_ok=True)
    cases={};children=[];policy=None;observations={}
    with tempfile.TemporaryDirectory(prefix='owner-',dir=base) as td:
        address=str(Path(td)/'s');assert len(address.encode())<=107
        server=socket.socket(socket.AF_UNIX);server.bind(address);server.listen(8);server.settimeout(3)
        cg=legacy.own_cgroup(os.getpid())
        exe=Path(sys.executable).resolve()
        policy=Policy(cg,'r07-model-only.service','a'*32,'b'*64,'c'*64,'d'*32,exe,exe)
        def spawn(rank,job='b'*64):
            p=subprocess.Popen([sys.executable,'-B',str(HERE/'worker.py'),address,str(rank),job,'c'*64,'d'*32],
                stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                cwd=td,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
            children.append(p);return p
        def accept():
            conn,_=server.accept();conn.settimeout(3)
            try:policy.receipt(conn)
            finally:conn.close()
        try:
            for rank in [0,1]:spawn(rank);accept()
            assert set(policy.ranks)=={0,1}
            observations['registered_kernel_peers']={str(r):dict(pid=p.pid,start_ticks=p.start_ticks,
                cgroup=p.cgroup,pidfd_device_inode=p.fd_identity,exit_poll_mask=legacy.exit_events(p.fd))
                for r,p in policy.ranks.items()}
            cases['both_live_fresh_kernel_peer_registrations']=True
            # Neither a historical JSON file nor JOBDONE creates a live receipt.
            (Path(td)/'fake_FINAL.json').write_text('{"accepted":true,"JOBDONE":true}')
            cases['fake_success_file']=refused(lambda:policy.inventory_failure(children[0].pid,PermissionError()),'missing LIVE final pair')
            for field in ['version','rank','action']:
                packet=dict(version=1,rank=0,action=1,job='b'*64,profile='c'*64,nonce='d'*32)
                packet[field]=True
                client=socket.socket(socket.AF_UNIX);client.settimeout(3);client.connect(address)
                try:
                    client.sendall(json.dumps(packet).encode()+b'\n')
                    cases['boolean_wire_'+field]=refused(accept,'typed rank/action')
                finally:client.close()
            foreign=spawn(0,job='e'*64)
            cases['wrong_job_wire']=refused(accept,'wrong JOB/PROFILE')
            foreign.wait(timeout=4)
            assert foreign.returncode!=0
            # A correctly typed final must still come from the original process.
            rogue=spawn(0)
            cases['duplicate_rank_new_kernel_peer']=refused(accept,'duplicate/replaced rank')
            rogue.wait(timeout=4)
            for p in children[:2]:
                p.stdin.write('final\n');p.stdin.flush();accept()
            assert policy.final=={0,1}
            observations['after_live_final_exit_masks']={str(r):legacy.exit_events(p.fd) for r,p in policy.ranks.items()}
            cases['both_live_kernel_bound_final_receipts']=True
            cases['unregistered_task_fd_denial']=refused(lambda:policy.inventory_failure(os.getpid(),PermissionError()),'unbound task')
            cases['unknown_output_path_NOT_retirement']=refused(lambda:policy.inventory_failure(children[0].pid,RuntimeError('unknown output path')),'non-FD failure')
            # PID-reuse identity mismatch: injected proc observation, not a
            # claim of forcing an actual kernel PID reuse in this small test.
            oldproc=legacy.proc
            def changed(pid):
                v=oldproc(pid);v['start_ticks']+=1;return v
            legacy.proc=changed
            try:cases['injected_PID_reuse']=refused(lambda:policy.ranks[1].live_identity(),'replaced/moved')
            finally:legacy.proc=oldproc
            p=children[0];p.stdin.write('deny\n');p.stdin.flush()
            assert select.select([p.stdout],[],[],3)[0]
            assert p.stdout.readline().strip()=='DUMPABLE0'
            try:list(Path(f'/proc/{p.pid}/fd').iterdir())
            except PermissionError as error:
                observations['live_denial']=dict(pid=p.pid,path=str(error.filename),errno=error.errno,
                    exit_poll_mask=legacy.exit_events(policy.ranks[0].fd))
            else:raise AssertionError('real live FD denial NOT reproduced')
            assert not policy.ranks[0].exited()
            denied_attempt=Attempt(policy)
            cases['REAL_EACCES_with_live_pidfd']=refused(lambda:denied_attempt.call('inventory_failure',p.pid,PermissionError('actual live EACCES')),'STILL LIVE')
            p.stdin.write('exit\n');p.stdin.flush();p.wait(timeout=4)
            assert policy.ranks[0].exited()
            cases['live_denied_attempt_STAYS_REFUSED_after_REAL_exit']=refused(
                lambda:denied_attempt.call('inventory_failure',p.pid,FileNotFoundError()),'cannot resurrect')
            # Independent counterfactual predicate branch, NOT resurrection of
            # the denied attempt. In production any Refusal is absorbing.
            cases['REAL_dead_rank_only_pending']=policy.inventory_failure(p.pid,FileNotFoundError('post-exit proc disappearance'))
            assert cases['REAL_dead_rank_only_pending']=='TERMINAL_PENDING_NOT_ACCEPTED'
            manager=dict(Id=policy.unit,InvocationID=policy.invocation,LoadState='loaded',ActiveState='inactive',
                SubState='dead',Result='success',ExecMainCode='1',ExecMainStatus='0',MainPID='0',Restart='no',Delegate='no')
            resources=dict(memory_max=12*GIB,swap_max=0,tasks_max=12,rss_B=GIB,
                host_available_B=8*GIB,disk_available_B=20*GIB,output_B=GIB,elapsed_s=5,oom_events=0,task_events=0)
            cases['one_live_rank_terminal_refused']=refused(lambda:policy.terminal_model(manager,'EMPTY_SAME_INODE',resources),'still live')
            q=children[1];q.stdin.write('exit\n');q.stdin.flush();q.wait(timeout=4)
            assert all(peer.exited() for peer in policy.ranks.values())
            observations['after_actual_exit']={str(r):dict(pid=p.pid,exit_poll_mask=legacy.exit_events(p.fd),
                child_returncode=children[r].returncode) for r,p in policy.ranks.items()}
            cases['REAL_two_process_exits']=True
            oldfailure=json.loads((HERE.parent/'static_environment_2026-10-15/evidence/TERMINAL.json').read_text())
            cases['original_failed_manager_REFUSED']=refused(lambda:policy.terminal_model(oldfailure['manager'],'EMPTY_SAME_INODE',resources),'manager identity/exit')
            for key,value in [('ExecMainStatus','3'),('InvocationID','f'*32)]:
                bad=dict(manager,**{key:value})
                cases['modeled_bad_'+key]=refused(lambda:policy.terminal_model(bad,'EMPTY_SAME_INODE',resources),'manager identity/exit')
            for state in ['UNKNOWN','REUSED_INODE','POPULATED']:
                cases['modeled_cgroup_'+state]=refused(lambda:policy.terminal_model(manager,state,resources),'cgroup')
            for key,value in [('elapsed_s',600),('host_available_B',4*GIB-1),('disk_available_B',10*GIB-1),
                ('output_B',14*GIB+1),('rss_B',12*GIB+1),('swap_max',1),('swap_max',False),
                ('output_B',2**63),('host_available_B',True),('elapsed_s',float('nan'))]:
                bad=dict(resources,**{key:value})
                cases['modeled_limit_'+key+'_'+str(value)]=refused(lambda:policy.terminal_model(manager,'EMPTY_SAME_INODE',bad))
            cases['modeled_complete_terminal_conjunction']=policy.terminal_model(manager,'EMPTY_SAME_INODE',resources)
            assert cases['modeled_complete_terminal_conjunction']=='MODEL_CONJUNCTION_ONLY_NO_NATIVE_AUTHORITY'
            # A closed/reused pidfd must not become omission authority.
            peer=policy.ranks[0];fd=peer.fd
            os.close(fd)
            null=os.open('/dev/null',os.O_RDONLY)
            if null!=fd:os.dup2(null,fd);os.close(null)
            cases['REAL_pidfd_descriptor_reuse']=refused(peer.exited,'descriptor reused')
        finally:
            for p in children:
                if p.poll() is None:p.kill()  # only our own unreaped direct child
                p.wait(timeout=4)
                for stream in [p.stdin,p.stdout,p.stderr]:stream.close()
            if policy:policy.close()
            server.close()
    out=dict(status='PASS bounded non-MPI component tests; PRODUCTION OWNER NOT QUALIFIED',
        cases=cases,kernel_observations=observations,real_kernel_tests=['SO_PEERPIDFD/process pidfd identity','live EACCES',
            'both child exits','pidfd descriptor reuse'],
        injected_tests=['PID-start mismatch','manager/CG/limit observations'],
        live_systemd_unit_or_empty_cgroup_measured=False,
        native_final_receipt_hook_in_PBE_binary=False,production_owner_integrated=False,
        scratch_only=True,all_test_children_reaped=True,native_jobs=0,DFT_writes=0,native_admission=False)
    (HERE/'owner_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
