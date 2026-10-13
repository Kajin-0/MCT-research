"""ONE actual production launch-gate probe, deliberately NON-MPI.

Verify actual UID/user-unit/cgroup/AS/memory/swap/tasks and source pins, then
send cancellation instead of the one permitted MPI launch receipt. Nothing
can pass into mpirun; terminal failure is the expected test result.
"""
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import sys
import time
import uuid

from owned_pair import (PRIVATE,HERE,DFT,MEMORY,AS,TASKS,manager_env,show,ctl,
                        cgroup_path,own_cgroup,counters,members,atomic_json,sha)


def main():
    root=PRIVATE/'control'; owner=json.loads((root/'OWNER.json').read_text()) if (root/'OWNER.json').exists() else None
    if owner is not None or (root/'BOOTSTRAP_RESULT.json').exists():raise RuntimeError('one-shot probe preserved')
    job=json.loads((root/'JOB.json').read_text());job['environment']={}
    atomic_json(root/'JOB_LAUNCH.json',job)
    ident=uuid.uuid4().hex;unit='r07-owned-'+ident+'.service'
    endpoint=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);endpoint.bind('\0r07-bootstrap-'+ident);endpoint.listen(1);endpoint.settimeout(5)
    from owned_pair import digest
    atomic_json(root/'OWNER.json',dict(pid=os.getpid(),gate_socket='r07-bootstrap-'+ident,job_sha256=digest(json.loads((root/'JOB.json').read_text()))))
    props=dict(Type='exec',MemoryMax=str(MEMORY),MemorySwapMax='0',TasksMax=str(TASKS),LimitAS=str(AS),
        LimitFSIZE=str(1<<30),LimitCORE='0',OOMPolicy='kill',KillMode='control-group',Delegate='no',
        Restart='no',RuntimeMaxSec='600s',TimeoutStopSec='1s',NoNewPrivileges='yes',WorkingDirectory=str(root))
    cmd=['/usr/bin/systemd-run','--user','--pipe','--wait','--quiet','--unit='+unit]
    for k,v in props.items():cmd+=['--property='+k+'='+v]
    cmd += [str(Path(sys.executable).resolve()),str(HERE/'launcher_gate.py'),str(root)]
    started=time.monotonic();p=subprocess.Popen(cmd,env=manager_env(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    cg=None;inv=None;report=dict(passed=False,MPI_QE_executed=False,unit=unit)
    try:
        c,_=endpoint.accept()
        with c:
            pid,uid,_=struct.unpack('3i',c.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12));msg=json.loads(c.recv(4096))
            fields=show(unit);inv=fields['InvocationID']
            if pid!=int(fields['MainPID']) or uid!=1001 or msg['pid']!=pid:raise RuntimeError('kernel unit peer')
            if own_cgroup(pid)!=fields['ControlGroup']:raise RuntimeError('effective cgroup')
            cg=cgroup_path(fields['ControlGroup']); kernel=counters(cg)
            import resource
            rlimit=resource.prlimit(pid,resource.RLIMIT_AS)
            if rlimit!=(AS,AS):raise RuntimeError('effective hard AS')
            for key,value in [('memory_max',MEMORY),('swap_max',0),('tasks_max',TASKS),('oom_group',1)]:
                if int(kernel[key])!=value:raise RuntimeError('kernel limit '+key)
            if fields['KillMode']!='control-group' or fields['Restart']!='no':raise RuntimeError('lifecycle')
            report.update(actual_peer=dict(pid=pid,uid=uid),invocation=inv,fields=fields,kernel=kernel,
                effective_AS=list(rlimit),live_JOB_challenge=msg)
            # The fixed gate accepts only EXECUTE_PINNED_FIRST_ACE. Explicit
            # cancellation proves this actual production path refuses execution.
            c.send(json.dumps(dict(action='CANCEL_NON_MPI_PROBE',challenge=msg['challenge'],job=msg['job'])).encode())
        output=p.communicate(timeout=5)[0].decode(errors='replace')
        terminal=show(unit)
        empty=not cg.exists() or (not counters(cg)['cgroup_events']['populated'] and not members(cg))
        report.update(returncode=p.returncode,output=output,terminal=terminal,owned_group_empty=empty,
                      passed=p.returncode!=0 and 'live owner launch refusal' in output and empty)
    finally:
        endpoint.close()
        fields=show(unit)
        if fields['LoadState']=='loaded' and fields['ActiveState'] not in ['failed','inactive']:
            if inv and fields['InvocationID']==inv:ctl(unit,'stop')
        p.wait(timeout=4)
        fields=show(unit)
        if fields['LoadState']=='loaded' and fields['ActiveState']=='failed' and fields['InvocationID']==inv:ctl(unit,'reset-failed')
        report['elapsed_seconds']=time.monotonic()-started
        atomic_json(root/'BOOTSTRAP_RESULT.json',report);atomic_json(HERE/'bootstrap_result.json',report)
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
