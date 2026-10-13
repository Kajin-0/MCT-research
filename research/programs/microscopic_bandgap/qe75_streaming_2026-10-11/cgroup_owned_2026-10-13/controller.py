"""Foreground controller for unique short-lived systemd user units, no QE/MPI."""
import json
import fcntl
import os
from pathlib import Path
import select
import signal
import socket
import struct
import subprocess
import sys
import time
from contracts import *
from family_runtime import durable_bytes,sync_dir

LEDGER=PRIVATE/'CURRENT_UNIT.json'


def restore_legacy(record):
    if 'legacy_saved_hex' not in record:return
    current=json.loads(REGISTRY.read_text())
    if current.get('phase')!='CGROUP_RUNNING' or current.get('job_sha256')!=record['job_sha256']:
        raise Refusal('foreign legacy registry refuses recovery overwrite')
    saved=bytes.fromhex(record['legacy_saved_hex'])
    if len(saved)>65536 or json.loads(saved)['phase']!='FINISHED':raise Refusal('legacy closed-state escrow invalid')
    path=REGISTRY.with_name(REGISTRY.name+'.'+record['unit']+'.restore')
    durable_bytes(path,saved);os.replace(path,REGISTRY);sync_dir(REGISTRY.parent)


def closed(record):
    # A disappeared/empty owned cgroup + retired witnessed process identities
    # is necessary; a released flock or dead systemd-run client alone is not.
    fields=show(record['unit']);rel=record.get('cgroup')
    if fields.get('LoadState')!='not-found' and fields.get('ActiveState') not in ['inactive','failed']:
        return False
    if fields.get('InvocationID') not in ['',record.get('invocation')]:raise Refusal('unit invocation reuse')
    if rel:
        cg=cgroup_path(rel)
        if cg.exists():
            if cg.stat().st_ino!=record['cgroup_inode']:raise Refusal('cgroup inode reused')
            try:
                if counters(cg)['cgroup_events']['populated'] or members(cg):return False
            except FileNotFoundError:
                if cg.exists():raise Refusal('partial live cgroup interface disappeared')
    for identity in record.get('members',[]):
        try:
            row=proc(identity['pid'])
            if row['start_ticks']==identity['start_ticks'] and row['state']!='Z':return False
        except (FileNotFoundError,ProcessLookupError):pass
    return True


def clear_owned_failure(record):
    terminal=show(record['unit'])
    if terminal.get('LoadState')=='loaded' and terminal.get('ActiveState')=='failed':
        if terminal.get('Id')!=record['unit'] or terminal.get('InvocationID') not in ['',record.get('invocation')]:
            raise Refusal('failed unit reuse refuses metadata cleanup')
        if record.get('root'):
            root=Path(record['root'])
            if root.parent!=PRIVATE or root.is_symlink():raise Refusal('owned recovery evidence root')
            atomic_json(root/'MANAGER_RECOVERY.json',terminal)
        r=ctl(record['unit'],'reset-failed')
        if r.returncode:raise Refusal('owned failed unit cleanup: '+r.stderr)
    return terminal


def recover_closed():
    if not LEDGER.exists():return
    prior=json.loads(LEDGER.read_text())
    if prior['phase']=='FINISHED':return
    if not closed(prior):raise Refusal('previous owned unit not proven closed; no restart')
    clear_owned_failure(prior)
    restore_legacy(prior)
    atomic_json(LEDGER,{**prior,'phase':'FINISHED','recovery':'verified empty/disappeared cgroup and retired identities'})


def run(root,action=None):
    recover_closed();job,profile=load_job(root);root=Path(root)
    if flock_owner(LOCK):raise Refusal('original exclusive owner lease busy')
    guard=LinuxGuard(LIB)
    if guard.probe(root)['available_bytes']<11*(1<<30) or memory()['MemAvailable']<4*(1<<30):raise Refusal('tiny service preflight headroom')
    listener=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET)
    listener.bind('\0r07-owner-'+job['id']);listener.listen(1);listener.settimeout(4)
    atomic_json(root/'OWNER.json',{'pid':os.getpid(),'start_ticks':proc(os.getpid())['start_ticks'],'run_pid':0})
    record={'unit':job['unit'],'root':str(root),'phase':'STARTING','job_sha256':digest(job),'profile_sha256':digest(profile),'members':[]}
    atomic_json(LEDGER,record)
    # systemd-run/guard diagnostics are bounded separately from worker stdout.
    p=subprocess.Popen(launch_command(root,job),env=manager_env(),stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE,stderr=subprocess.STDOUT,close_fds=True)
    run_identity=Identity(p.pid);connection=None;reason='PASS';hello=None;owned=None;last={};samples=[];diag=bytearray();escrow_fd=None
    started=time.monotonic();cancelled=[]
    for number in [signal.SIGTERM,signal.SIGINT]:signal.signal(number,lambda s,f:cancelled.append(s))
    try:
        connection,_=listener.accept();connection.settimeout(2)
        pid,uid,_=struct.unpack('3i',connection.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
        hello=json.loads(connection.recv(65536));owned=Identity(pid)
        if uid!=os.getuid() or hello['pid']!=pid or hello['start_ticks']!=owned.start_ticks:raise Refusal('guard kernel peer identity')
        interpreter=Path(os.readlink(f'/proc/{pid}/exe')).resolve()
        if interpreter!=Path(sys.executable).resolve() or artifact_sha256(interpreter)!=job['files'][str(interpreter)]:raise Refusal('guard interpreter mismatch')
        command=Path(f'/proc/{pid}/cmdline').read_bytes().rstrip(b'\0').split(b'\0')
        if command!=[os.fsencode(interpreter),os.fsencode(HERE/'guard.py'),os.fsencode(root)]:raise Refusal('guard command mismatch')
        if hello['job_sha256']!=digest(job) or hello['profile_sha256']!=digest(profile):raise Refusal('guard dual binding')
        fields=show(job['unit']);cg,kernel=verify_unit(job,fields,pid,hello['invocation'])
        if hello['cgroup']!=fields['ControlGroup'] or hello['cgroup_inode']!=cg.stat().st_ino:raise Refusal('guard cgroup receipt mismatch')
        record.update(phase='RUNNING',cgroup=hello['cgroup'],cgroup_inode=hello['cgroup_inode'],invocation=hello['invocation'],members=[owned.record()])
        atomic_json(LEDGER,record)
        connection.send(encode({'action':'AUTHORIZE_ABI_NO_MPI','hello_sha256':digest(hello),
                               'run_pid':run_identity.pid,'run_start_ticks':run_identity.start_ticks}))
        receipt_raw,ancillary,flags,_=connection.recvmsg(65536,socket.CMSG_SPACE(4),socket.MSG_CMSG_CLOEXEC)
        receipt=json.loads(receipt_raw)
        received=[]
        for level,kind,data in ancillary:
            if level==socket.SOL_SOCKET and kind==socket.SCM_RIGHTS:
                received.extend(struct.unpack('i'*(len(data)//4),data))
        if len(received)!=1 or flags & (socket.MSG_TRUNC|socket.MSG_CTRUNC):
            for fd in received:os.close(fd)
            raise Refusal('lease escrow fd extent')
        escrow_fd=received[0];fstat=os.fstat(escrow_fd);lockstat=LOCK.stat()
        if (fstat.st_dev,fstat.st_ino)!=(lockstat.st_dev,lockstat.st_ino) or flock_owner(LOCK)!=[pid]:raise Refusal('kernel lease fd/holder mismatch')
        if receipt!={'action':'LEASE_HELD','hello_sha256':digest(hello),'pid':pid,'start_ticks':owned.start_ticks,
                     'job_sha256':digest(job),'profile_sha256':digest(profile)}:raise Refusal('lease escrow dual binding')
        saved=REGISTRY.read_bytes()
        if json.loads(saved)['phase']!='FINISHED':raise Refusal('legacy owner unfinished')
        record['legacy_saved_hex']=saved.hex();record['escrow_guard']=owned.record();atomic_json(LEDGER,record)
        atomic_json(REGISTRY,{'phase':'CGROUP_RUNNING','version':1,'job_sha256':digest(job),
                             'unit':job['unit'],'cgroup':hello['cgroup'],'invocation':hello['invocation'],'members':[]})
        connection.send(encode({'action':'RUN_ABI_NO_MPI','receipt_sha256':digest(receipt)}))
        connection.setblocking(False)
        acted=False
        while p.poll() is None:
            if cg.exists():
                try:
                    last=counters(cg);rows=members(cg);record['members']=[{'pid':pid,'start_ticks':r['start_ticks']} for pid,r in rows.items()]
                    samples.append({'elapsed':time.monotonic()-started,**last});samples=samples[-512:]
                    atomic_json(LEDGER,record)
                except FileNotFoundError:
                    # The whole unique cgroup can disappear between exists()
                    # and reads during normal manager cleanup. This loses a
                    # sample, never proves success. Final manager/identity/
                    # empty-group checks below still decide closure.
                    if cg.exists():raise Refusal('partial live cgroup interface disappeared')
            if (cancelled or action=='cancel') and not acted:
                connection.send(encode({'action':'CANCEL'}));acted=True
            if action=='owner_crash' and not acted and (root/'GUARD_ACTIVE.json').exists():
                os._exit(76)
            if time.monotonic()-started>job['limits']['wall_seconds']+6:raise Refusal('controller wall+cleanup deadline')
            ready,_,_=select.select([p.stdout],[],[],.02)
            if ready:
                data=os.read(p.stdout.fileno(),4096);diag+=data
                if len(diag)>16384:raise Refusal('exact controller diagnostic log cap')
        p.wait(timeout=1)
        while True:
            data=os.read(p.stdout.fileno(),4096)
            if not data:break
            diag+=data
            if len(diag)>16384:raise Refusal('controller diagnostic log cap')
        if p.returncode!=0:reason='unit nonzero '+str(p.returncode)
    except BaseException as e:reason=str(e)
    finally:
        if connection:connection.close()
        listener.close()
        # Stop only the unique invocation acquired and independently verified.
        # Unit-name reuse by a malicious same-UID manager client is outside
        # this cooperative workload contract; unexpected reuse is refused.
        fields=show(job['unit'])
        if fields.get('LoadState')!='not-found' and fields.get('ActiveState') not in ['inactive','failed']:
            if hello and fields.get('InvocationID')==hello['invocation'] and fields.get('ControlGroup')==hello['cgroup']:
                ctl(job['unit'],'stop')
            else:reason+='; unbound unit refuses stop'
        try:p.wait(timeout=3)
        except subprocess.TimeoutExpired:
            run_identity.send(signal.SIGKILL);p.wait(timeout=1);reason+='; run-client deadline'
        deadline=time.monotonic()+3
        while not closed(record) and time.monotonic()<deadline:time.sleep(.02)
        empty=closed(record)
        if empty:
            restore_legacy(record)
            atomic_json(LEDGER,{**record,'phase':'FINISHED'})
        else:atomic_json(LEDGER,{**record,'phase':'ORPHANED'})
        terminal=show(job['unit'])
        # Persist manager result BEFORE dropping a failed transient unit.
        atomic_json(root/'MANAGER_TERMINAL.json',terminal)
        clear_owned_failure(record)
        lease_held_until_closed=escrow_fd is not None
        escrow_exclusive_after_guard_exit=False
        if escrow_fd is not None:
            if not empty:raise Refusal('unverified cgroup retains durable marker; no new launch')
            checkfd=os.open(LOCK,os.O_RDWR|os.O_NOFOLLOW)
            try:
                try:fcntl.flock(checkfd,fcntl.LOCK_EX|fcntl.LOCK_NB)
                except BlockingIOError:escrow_exclusive_after_guard_exit=True
                else:raise Refusal('escrow lost exclusive flock before verified release')
            finally:os.close(checkfd)
            os.close(escrow_fd);escrow_fd=None
        lease=flock_owner(LOCK)
        result={'reason':reason,'unit_returncode':p.returncode,'hello':hello,'samples':samples,'last_kernel_sample':last,
                'systemd_diagnostics':diag.decode(errors='replace'),'owned_unit_closed':empty,'lease_holders_after':lease,
                'manager_terminal':terminal,'lease_fd_escrow_until_verified_empty':lease_held_until_closed,
                'escrow_exclusive_after_guard_exit':escrow_exclusive_after_guard_exit,
                'controller_elapsed_seconds':time.monotonic()-started,'native_QE_MPI_HSE_executed':False,
                'hostwide_inventory_scanned':False,'hostwide_exclusivity_proven':False}
        if (root/'GUARD_RESULT.json').exists():result['guard']=json.loads((root/'GUARD_RESULT.json').read_text())
        result['passed']=reason=='PASS' and empty and not lease and result.get('guard',{}).get('passed',False)
        atomic_json(root/'CONTROLLER_RESULT.json',result)
        if owned:owned.close()
        run_identity.close();p.stdout.close()
    return result


if __name__=='__main__':
    result=run(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)
    print(json.dumps({'passed':result['passed'],'reason':result['reason'],'closed':result['owned_unit_closed']}))
    raise SystemExit(0 if result['passed'] else 1)
