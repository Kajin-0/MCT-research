"""Actual C wire -> production dispatcher/reader gate/retirement components.

NO MPI/QE/service. Terminal manager/cgroup snapshots are explicitly mocked;
the positive fixture reader accepts NON_MPI_FIXTURE, never native physics.
"""
from pathlib import Path
import fcntl
import hashlib
import importlib.util
import json
import os
import select
import socket
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3]
sys.path.insert(0,str(HERE))
import owner
from protocol import Protocol,Refusal,kernel,sha
import reader
GIB=1<<30
results={};observations=[]


def refused(fn,word=None):
    try:fn()
    except Exception as e:
        if word is not None:assert word in str(e),repr(e)
        return type(e).__name__+': '+str(e)
    raise AssertionError('expected refusal')


def fixture_reader(root,profile,peers):
    for r in [0,1]:
        if (root/'pilot'/f'H.rank{r}').read_bytes()!=b'NON_MPI_FIXTURE!':raise ValueError('fixture readback failed')
    return {'COMPONENT_FIXTURE_ONLY_NOT_NATIVE_H':True}


class Case:
    def __init__(self,base,worker,name,modes=('normal','normal'),readback=fixture_reader,pre_ack=lambda:None):
        self.path=base/name;self.path.mkdir();self.root=self.path/'unshared';self.root.mkdir();(self.root/'pilot').mkdir()
        self.address=str(self.root/'s');assert len(self.address.encode())<=107
        self.server=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);self.server.bind(self.address);self.server.listen(4);self.server.setblocking(False)
        self.lockpath=self.path/'owner.lock';self.lockfd=os.open(self.lockpath,os.O_RDWR|os.O_CREAT|os.O_EXCL,0o600);fcntl.flock(self.lockfd,fcntl.LOCK_EX)
        self.children=[];self.worker=worker;self.modes=modes
        self.profile={'elf':str(worker),'elf_sha256':sha(worker)}
        self.job=dict(job_sha256='b'*64,profile_sha256='c'*64,nonce='d'*32,
            argv={str(r):[str(worker),str(r),str(self.root),modes[r]] for r in [0,1]})
        self.cg=kernel.own_cgroup(os.getpid())
        with patch.object(owner,'inspect',readback):
            self.p=owner.make_protocol(self.root,self.job,self.profile,self.cg,'e'*32,pre_ack)
        self.account=owner.Account(self.root,1<<20,0,None,self.p)
    def spawn(self,r,mode=None):
        mode=self.modes[r] if mode is None else mode
        env=dict(os.environ,R07_STATIC_SOCKET=self.address,R07_STATIC_JOB='b'*64,R07_STATIC_PROFILE='c'*64,
            R07_STATIC_NONCE='d'*32,R07_STATIC_OWNER=str(os.getpid()),
            R07_STATIC_OWNER_TICKS=str(kernel.proc(os.getpid())['start_ticks']),
            R07_STATIC_LOCK=str(self.lockpath),INVOCATION_ID='e'*32)
        env.pop('R07_STATIC_INVOCATION',None) # exercise actual service-env fallback
        child=subprocess.Popen([str(self.worker),str(r),str(self.root),mode],stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env,cwd=self.path)
        self.children.append(child);return child
    def pump(self,predicate):
        end=time.monotonic()+3
        while not predicate():
            owner.service(self.server,self.p)
            if time.monotonic()>=end:raise TimeoutError('bounded component wait')
            time.sleep(.001)
    def line(self,child,expected):
        if not select.select([child.stdout],[],[],3)[0]:raise TimeoutError('worker line missing')
        assert child.stdout.readline().strip()==expected
    def begin(self):
        for r in [0,1]:self.spawn(r)
        self.pump(lambda:len(self.p.peers)==2 and not self.p.waiting)
        for child in self.children:self.line(child,'READY')
    def go(self):
        for c in self.children[:2]:c.stdin.write('go\n');c.stdin.flush()
    def complete(self):
        self.go();self.pump(lambda:self.p.finals=={0,1})
        for c in self.children[:2]:self.line(c,'FINAL')
    def exit(self):
        for c in self.children[:2]:c.stdin.write('x\n');c.stdin.flush();c.wait(timeout=2)
        assert all(c.returncode==0 for c in self.children[:2])
    def sample(self):
        identities={p.pid:p for p in self.p.peers.values()}
        return owner.sample_owned(self.p,[self.account],list(identities),identities,self.root)
    def close(self):
        self.p.close();self.server.close();os.close(self.lockfd)
        for c in self.children:
            if c.poll() is None:c.kill() # our own still-unreaped direct child only
            c.wait(timeout=2)
            for s in [c.stdin,c.stdout,c.stderr]:s.close()


def main():
    base=REPO/'.tmp/r07spc16';base.mkdir(exist_ok=True)
    version=sha(HERE/'test_integration.py')[:12]
    build=base/('component-build-'+version+'-'+str(time.time_ns()));build.mkdir(exist_ok=False)
    worker=build/'wire_worker'
    cmd=['/usr/bin/cc','-std=c11','-O2','-Wall','-Wextra','-Werror',str(HERE/'wire_worker.c'),str(HERE/'native_lease.c'),'-o',str(worker)]
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=30);assert r.returncode==0,r.stderr
    cases=[]
    with tempfile.TemporaryDirectory(prefix='t-',dir=base) as td:
        root=Path(td)
        def case(name,**kw):
            c=Case(root,worker,name,**kw);cases.append(c);return c
        try:
            a=case('normal');a.begin();a.complete()
            results['real_C_wire_production_dispatch_both_live_finals']=True
            observations.append({'case':'normal','ranks':{str(r):{'pid':p.pid,'ticks':p.start_ticks,
                'pidfd_dev_inode':p.fd_identity,'kernel_exit_mask':kernel.exit_events(p.fd),'cgroup':p.cgroup}
                for r,p in a.p.peers.items()}})
            results['production_reader_rejects_fixture_NOT_material']=refused(lambda:reader.decode(a.root/'pilot/H.rank0'),'truncated')
            a.exit();assert all(p.exited() for p in a.p.peers.values())
            try:a.p.inventory_failure(a.children[0].pid,FileNotFoundError('actual exited rank'))
            except kernel.TerminalPending:pass
            else:raise AssertionError('not terminal pending')
            results['actual_kernel_exits_only_PENDING']=True
            # Terminal snapshots are modeled, not new systemd/cgroup evidence.
            cg=a.path/'modeled_cgroup';cg.mkdir();(cg/'cgroup.events').write_text('populated 0\nfrozen 0\n');(cg/'cgroup.procs').write_text('')
            ss=cg.stat();identity=(ss.st_dev,ss.st_ino)
            manager=dict(Id='r07-modeled.service',InvocationID='e'*32,LoadState='loaded',ActiveState='inactive',SubState='dead',
                Result='success',ExecMainCode='1',ExecMainStatus='0',MainPID='0',Restart='no',Delegate='no')
            class Client:
                def poll(self):return 0
            class Account:
                def sample(self):return {}
            def terminal(m=manager,ci=identity):
                with patch.object(kernel,'show',return_value=m),patch.object(kernel,'cgroup_path',return_value=cg),patch.object(kernel,'own_cgroup',return_value='/modeled/outside-holder'):
                    return a.p.terminal(Client(),'r07-modeled.service',ci,Account(),lambda:None)
            # Independent failure branches, not resurrection of a failed run.
            original_refusal=a.p.refused
            (a.root/'pw.out').write_text('COMPONENT ONLY R07_STATIC_H_COMPLETE\nJOB DONE.\n')
            results['modeled_manager_mismatch']=refused(lambda:terminal(dict(manager,InvocationID='f'*32)),'manager')
            a.p.refused=original_refusal
            results['modeled_nonzero_exit']=refused(lambda:terminal(dict(manager,ExecMainStatus='14')),'manager')
            a.p.refused=original_refusal
            results['modeled_cgroup_identity_mismatch']=refused(lambda:terminal(ci=(0,0)),'cgroup replaced')
            a.p.refused=original_refusal
            (a.root/'pw.out').unlink()
            results['lost_log_is_fatal']=refused(terminal,'log')
            a.p.refused=original_refusal
            (a.root/'pw.out').write_text('COMPONENT ONLY R07_STATIC_H_COMPLETE\nJOB DONE.\n')
            results['modeled_terminal_conjunction_component']=terminal()['terminal']
            a.p.refused=original_refusal
            pidfd=a.p.peers[0].fd;os.close(pidfd);null=os.open('/dev/null',os.O_RDONLY)
            if null!=pidfd:os.dup2(null,pidfd);os.close(null)
            results['real_descriptor_reuse']=refused(a.p.peers[0].exited,'reused')
            b=case('live-denied');b.begin();b.complete()
            c=b.children[0];c.stdin.write('deny\n');c.stdin.flush();b.line(c,'DUMPABLE0')
            try:list(Path(f'/proc/{c.pid}/fd').iterdir())
            except PermissionError as error:
                denied=dict(pid=c.pid,path=error.filename,errno=error.errno,
                    pidfd_mask=kernel.exit_events(b.p.peers[0].fd))
                assert denied['errno']==13 and denied['pidfd_mask']==0
            else:raise AssertionError('real live EACCES not observed')
            results['actual_live_FD_EACCES_absorbing']=refused(b.sample,'STILL LIVE')
            observations.append(dict(case='live-denied',**denied))
            b.exit();results['later_actual_exit_does_NOT_retropass']=refused(b.p.live,'absorbing')
            c=case('premature',modes=('premature','normal'));c.spawn(0)
            results['premature_native_final']=refused(lambda:c.pump(lambda:False),'premature')
            c=case('incomplete',modes=('incomplete','normal'));c.begin();c.go()
            results['incomplete_closed_packet']=refused(lambda:c.pump(lambda:False),'incomplete')
            c=case('reader-fail',readback=lambda *args:(_ for _ in ()).throw(ValueError('injected native readback failure')))
            c.begin();c.go();results['failed_readback_blocks_final_ack']=refused(lambda:c.pump(lambda:False),'readback')
            c=case('resource-before-grant',pre_ack=lambda:(_ for _ in ()).throw(ValueError('pre-ACK resource failure')))
            c.spawn(0);c.spawn(1)
            results['resource_failure_prevents_grant']=refused(lambda:c.pump(lambda:False),'resource failure')
            c=case('identity');c.begin()
            # Final from a third fresh native C process; same ELF/UID/group is
            # insufficient. Give it the pinned final argv to reach PID check.
            c.job['argv']['0']=[str(worker),'0',str(c.root),'foreign'];c.spawn(0,'foreign')
            results['foreign_process_final_refused']=refused(lambda:c.pump(lambda:False),'different kernel')
            c=case('lost',modes=('lost','normal'));c.begin();c.go();c.children[0].wait(timeout=2)
            results['JOBDONE_lost_rank_no_authority']=refused(lambda:c.p.inventory_failure(c.children[0].pid,FileNotFoundError()),'final pair')
            c=case('burst',modes=('burst','normal'));c.begin();c.children[0].stdin.write('go\n');c.children[0].stdin.flush();c.line(c.children[0],'BURST')
            results['real_allocated_output_burst_absorbing']=refused(c.sample,'budget')
            results['native_release_load_refuses']=refused(lambda:owner.load('unshared'),'no native execution release')
        finally:
            for c in cases:c.close()
    # Real isolated import, not AST-only or warmed module cache.
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1');env.pop('PYTHONPATH',None)
    with tempfile.TemporaryDirectory(prefix='i-',dir=base) as td:
        program='import sys;sys.path.insert(0,sys.argv[1]);import owner,reader;print("PRODUCTION_IMPORT_OK")'
        ok=subprocess.run([sys.executable,'-B','-c',program,str(HERE)],cwd=td,env=env,capture_output=True,text=True,timeout=15)
        assert ok.returncode==0,ok.stderr
        clone=Path(td)/'reader.py';clone.write_text((HERE/'reader.py').read_text())
        program='import importlib.util,sys;s=importlib.util.spec_from_file_location("isolated",sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)'
        missing=subprocess.run([sys.executable,'-B','-c',program,str(clone)],cwd=td,env=env,capture_output=True,text=True,timeout=15)
        assert missing.returncode and 'packet_reader.py' in missing.stderr
        (Path(td)/'packet_reader.py').write_text('# corrupt fixture\n')
        corrupt=subprocess.run([sys.executable,'-B','-c',program,str(clone)],cwd=td,env=env,capture_output=True,text=True,timeout=15)
        assert corrupt.returncode and 'corrupt pinned' in corrupt.stderr
    results['clean_production_owner_and_reader_import']=True
    results['missing_and_corrupt_dependency_fail_before_launch']=True
    out=dict(status='PASS compiled NON_MPI wire and integrated handler components; NATIVE_RUNTIME_NOT_QUALIFIED',
        tests=results,kernel_observations=observations,component_compile=dict(command=cmd,returncode=r.returncode,stderr=r.stderr),
        source_sha256={str(p):sha(p) for p in [worker,HERE/'wire_worker.c',HERE/'native_lease.c']},
        terminal_manager_cgroup_and_fixture_reader_MOCKED=True,actual_systemd_unit_or_MPI=False,
        whole_production_owner_loop_executed=False,all_children_reaped=all(p.poll() is not None for c in cases for p in c.children),
        no_native_Hamiltonian_or_old_refused_packet_used=True,native_QE_MPI_SCF=0,DFT_writes=0,
        live_user_manager_terminal_admission=False,physical_xc=None)
    (HERE/'component_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
