"""Transient user-service guard. Executable whitelist: tiny C fixtures ONLY."""
import fcntl
import json
import os
from pathlib import Path
import select
import selectors
import resource
import signal
import socket
import struct
import subprocess
import sys
import time
from contracts import *
from process_identity import subreaper,reap


def main(root):
    job,profile=load_job(root,expect_absent=False);root=Path(root)
    owner=json.loads((root/'OWNER.json').read_text());owner_identity=Identity(owner['pid'])
    if owner_identity.start_ticks!=owner['start_ticks']:raise Refusal('owner PID reused')
    life=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);life.settimeout(3)
    life.connect('\0r07-owner-'+job['id'])
    peer,uid,gid=struct.unpack('3i',life.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
    if peer!=owner_identity.pid or uid!=os.getuid():raise Refusal('owner socket kernel identity')
    own=Identity(os.getpid());fields=show(job['unit']);invocation=fields['InvocationID']
    cg,kernel=verify_unit(job,fields,os.getpid(),invocation);inode=cg.stat().st_ino
    fsize=resource.getrlimit(resource.RLIMIT_FSIZE);core=resource.getrlimit(resource.RLIMIT_CORE)
    if fsize!=(job['limits']['file_max'],)*2 or core!=(0,0):raise Refusal('kernel per-file/core rlimit mismatch')
    status=Path('/proc/self/status').read_text()
    if 'NoNewPrivs:\t1' not in status:raise Refusal('kernel NoNewPrivileges missing')
    hello={'job_sha256':digest(job),'profile_sha256':digest(profile),'pid':own.pid,'start_ticks':own.start_ticks,
           'unit':job['unit'],'invocation':invocation,'cgroup':fields['ControlGroup'],'cgroup_inode':inode,
           'kernel':kernel,'rlimit_fsize':list(fsize),'rlimit_core':list(core),'scope':'ABI_NO_MPI'}
    life.send(encode(hello))
    grant=json.loads(life.recv(65536))
    if grant.get('action')!='AUTHORIZE_ABI_NO_MPI' or grant.get('hello_sha256')!=digest(hello):raise Refusal('live owner grant mismatch')
    run_identity=Identity(grant['run_pid'])
    if run_identity.start_ticks!=grant['run_start_ticks'] or proc(run_identity.pid)['ppid']!=owner_identity.pid:
        raise Refusal('foreground systemd-run identity mismatch')
    owner['run_pid']=run_identity.pid
    life.setblocking(False);subreaper();stopped=[]
    for number in [signal.SIGTERM,signal.SIGINT]:signal.signal(number,lambda s,f:stopped.append(s))
    lease=os.open(LOCK,os.O_RDWR|os.O_NOFOLLOW);fcntl.flock(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if json.loads(REGISTRY.read_text())['phase']!='FINISHED':raise Refusal('original owner ledger not closed')
    lease_receipt={'action':'LEASE_HELD','hello_sha256':digest(hello),'pid':own.pid,'start_ticks':own.start_ticks,
                   'job_sha256':digest(job),'profile_sha256':digest(profile)}
    life.settimeout(3)
    life.sendmsg([encode(lease_receipt)],[(socket.SOL_SOCKET,socket.SCM_RIGHTS,struct.pack('i',lease))])
    start=json.loads(life.recv(65536))
    if start!={'action':'RUN_ABI_NO_MPI','receipt_sha256':digest(lease_receipt)}:raise Refusal('live lease escrow acknowledgement missing')
    marker=json.loads(REGISTRY.read_text())
    if marker.get('phase')!='CGROUP_RUNNING' or marker.get('job_sha256')!=digest(job):raise Refusal('durable cross-owner marker missing')
    life.setblocking(False)
    server=None;workers=[];identities={};ranks={};checked=set();wire=[];reservations=[];selector=selectors.DefaultSelector()
    logs=open(root/'logs/workers.log','xb',buffering=0);logged=0;reason='PASS';peak_rss=0;last=kernel
    beginning=time.monotonic();guard=LinuxGuard(LIB)
    def measure():
        nonlocal peak_rss,last
        if not owner_identity.live():raise Refusal('owner disappeared')
        if own_cgroup(os.getpid())!=fields['ControlGroup'] or cg.stat().st_ino!=inode:raise Refusal('guard cgroup identity changed')
        last=counters(cg)
        for key,value in [('memory_max',job['limits']['memory_max']),('swap_max',0),('tasks_max',16),('oom_group',1)]:
            if last[key]!=str(value):raise Refusal('kernel limit changed')
        rows=members(cg);rss=sum(row['rss_bytes'] for row in rows.values())
        # External foreground controller and systemd-run client are NOT inside
        # memory.max; explicitly include them in the RSS stop predicate.
        for p in [owner_identity.pid,owner['run_pid']]:
            try:rss+=proc(p)['rss_bytes']
            except (FileNotFoundError,ProcessLookupError):pass
        peak_rss=max(peak_rss,rss)
        if memory()['MemAvailable']<4*(1<<30) or guard.probe(root)['available_bytes']<10*(1<<30):raise Refusal('host RAM/disk floor')
        if rss>12*(1<<30):raise Refusal('summed RSS guard (distinct from memory.max)')
        if time.monotonic()-beginning>=job['limits']['wall_seconds']:raise Refusal('guard monotonic wall')
        allocated=0;seen=set()
        for p in root.rglob('*'):
            if p.is_symlink():raise Refusal('unregistered symlink output')
            if p.is_file():
                s=p.stat();key=(s.st_dev,s.st_ino)
                if key not in seen:allocated+=s.st_blocks*512;seen.add(key)
        if allocated>job['limits']['output_max']:raise Refusal('sampled aggregate output envelope')
        return rows
    try:
        if memory()['MemAvailable']<4*(1<<30) or guard.probe(root)['available_bytes']<11*(1<<30):raise Refusal('tiny unit headroom')
        for r,n in enumerate(job['limits']['rank_bytes']):
            p=root/'scratch'/f'rank{r}.stream';fd=os.open(p,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
            try:
                for q in guard.probe_fd(fd)['quotas']:quota_headroom(q)
                import ctypes
                allocated=ctypes.c_int64();err=guard.lib.qe_reserve_fd(fd,integer(n),ctypes.byref(allocated))
                if err:raise Refusal('64-bit owned reservation errno '+str(err))
                s=os.fstat(fd);reservations.append({'rank':r,'requested':n,'allocated':allocated.value,'inode':s.st_ino,'dev':s.st_dev})
                if s.st_size!=n or allocated.value<round_blocks(n,4096):raise Refusal('reservation logical/allocated extent')
            finally:os.close(fd)
        server=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET)
        address='r07-cgroup-'+job['id'];server.bind('\0'+address);server.listen(4)
        env=manager_env();env.update(QE75_LEASE_SOCKET=address,QE75_LEASE_LOCK=str(LOCK),
            QE75_LEASE_PID=str(os.getpid()),QE75_LEASE_TICKS=str(own.start_ticks),
            QE75_JOB_SHA256=digest(job),QE75_PROFILE_SHA256=digest(profile))
        for r in [0,1]:
            p=subprocess.Popen([str(WORKER),str(r),job['case'],str(root)],env=env,
                               stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,close_fds=True)
            workers.append(p);identities[p.pid]=Identity(p.pid);selector.register(p.stdout,selectors.EVENT_READ)
        while True:
            rows=measure()
            if stopped:raise Refusal('systemd/user stop')
            ready,_,_=select.select([life,server],[],[],.01)
            if life in ready:
                data=life.recv(65536)
                if not data:raise Refusal('owner lifeline closed')
                if json.loads(data).get('action')=='CANCEL':raise Refusal('owner cancellation')
            if server in ready:
                c,_=server.accept();c.settimeout(.2);challenge=bytes(32);status=22
                try:
                    pid,uid,_=struct.unpack('3i',c.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
                    raw=c.recv(REQUEST.size+1)
                    if len(raw)!=REQUEST.size:raise Refusal('wire extent')
                    magic,version,action,rank,size,jh,ph,challenge=REQUEST.unpack(raw)
                    if uid!=os.getuid() or magic!=MAGIC or version!=VERSION or size!=2 or rank not in [0,1]:raise Refusal('kernel peer/wire header')
                    if jh.decode()!=digest(job) or ph.decode()!=digest(profile):raise Refusal('wire JOB/PROFILE mismatch')
                    if pid not in rows or own_cgroup(pid)!=fields['ControlGroup']:raise Refusal('peer outside owned cgroup')
                    if Path(os.readlink(f'/proc/{pid}/exe')).resolve()!=WORKER:raise Refusal('worker executable mismatch')
                    if artifact_sha256(WORKER)!=job['executable_sha256']:raise Refusal('worker executable changed')
                    argv=Path(f'/proc/{pid}/cmdline').read_bytes().rstrip(b'\0').split(b'\0')
                    if argv!=[os.fsencode(WORKER),str(rank).encode(),job['case'].encode(),os.fsencode(root)]:raise Refusal('fixed tiny worker command mismatch')
                    identity=pin_descendant(pid,os.getpid(),rows)
                    try:
                        if action==1:
                            if rank in ranks and ranks[rank].record()!=identity.record():raise Refusal('rank replacement')
                            if rank not in ranks:ranks[rank]=identity;identity=None
                            status=0
                        elif action==2:
                            if rank not in ranks or ranks[rank].pid!=pid:raise Refusal('unregistered peer')
                            status=0 if set(ranks)=={0,1} and all(i.live() for i in ranks.values()) else 11
                            if status==0:checked.add(rank)
                        else:raise Refusal('unknown action')
                        wire.append({'peer':identities[pid].record(),'rank':rank,'action':action,'status':status,
                                     'invocation':invocation,'cgroup_inode':inode,'scope':'ABI_NO_MPI'})
                    finally:
                        if identity:identity.close()
                except (OSError,ValueError,Refusal):status=22
                c.send(REPLY.pack(MAGIC,VERSION,status,SCOPE_ABI_NO_MPI,challenge));c.close()
            for key,_ in selector.select(0):
                data=os.read(key.fileobj.fileno(),4096)
                if not data:selector.unregister(key.fileobj);key.fileobj.close();continue
                remaining=job['limits']['log_max']-logged
                logs.write(data[:remaining]);logged+=min(len(data),remaining)
                if len(data)>remaining:raise Refusal('exact aggregate worker log cap')
            if checked=={0,1} and not (root/'out/actors.go').exists():
                ready=[root/'out'/f'rank{r}.ready' for r in [0,1]]
                if all(p.is_file() for p in ready):
                    if any(p.is_symlink() or p.read_text()!=str(ranks[r].pid) or not ranks[r].live() for r,p in enumerate(ready)):
                        raise Refusal('actor release identity mismatch')
                    atomic_json(root/'out/actors.go',{'invocation':invocation,'ranks':{r:i.record() for r,i in ranks.items()}})
            if checked=={0,1} and not (root/'GUARD_ACTIVE.json').exists():
                atomic_json(root/'GUARD_ACTIVE.json',{'ranks':{r:i.record() for r,i in ranks.items()},'hello':hello})
            if job['case']=='guard_crash' and checked=={0,1}:
                atomic_json(root/'CRASH_WITNESS.json',{'ranks':{r:i.record() for r,i in ranks.items()},'hello':hello})
                os._exit(77) # This explicitly tests systemd cleanup after guard death.
            if all(p.poll() is not None for p in workers):
                if any(p.returncode!=0 for p in workers):raise Refusal('compiled worker nonzero: '+str([p.returncode for p in workers]))
                if set(ranks)!={0,1}:raise Refusal('all-rank lease receipt absent')
                alive=[row for pid,row in members(cg).items() if pid!=os.getpid() and row['state']!='Z']
                if alive:raise Refusal('rank exited with live detached descendant')
                break
    except BaseException as e:reason=str(e)
    finally:
        # The user manager independently enforces KillMode=control-group. Here
        # signal only already pinned direct workers; never numeric PGID/foreign
        # cgroup guesses. Detached children are handled by unit stop as well.
        for i in identities.values():i.send(signal.SIGKILL)
        for p in workers:
            try:p.wait(timeout=.5)
            except subprocess.TimeoutExpired:pass
        try:last=counters(cg)
        except FileNotFoundError:pass
        report={'passed':reason=='PASS','reason':reason,'hello':hello,'kernel_final':last,
                'peak_summed_RSS_bytes':peak_rss,'ranks':{r:i.record() for r,i in ranks.items()},'wire':wire,
                'log_written_bytes':logged,'reservations':reservations,'native_MPI_QE_executed':False,
                'hostwide_exclusivity_proven':False,'cgroup_memory_is_not_RSS':True}
        atomic_json(root/'GUARD_RESULT.json',report)
        logs.close();selector.close()
        if server:server.close()
        for i in ranks.values():i.close()
        for i in identities.values():i.close()
        run_identity.close();owner_identity.close();own.close();os.close(lease);life.close()
    return 0 if reason=='PASS' else 1


if __name__=='__main__':raise SystemExit(main(sys.argv[1]))
