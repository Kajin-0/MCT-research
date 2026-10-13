"""Read-only permission evidence. UNKNOWN is never permission to launch MPI."""
from pathlib import Path
from datetime import datetime,timezone
import errno
import os
from production_transport import Refusal
from process_identity import table,proc,mpi_inventory


def inventory_evidence():
    unknown=[];readable=0;vanished=0
    for pid,row in table().items():
        if row['state']=='Z': continue
        try:
            Path(f'/proc/{pid}/maps').read_text();readable+=1
        except (FileNotFoundError,ProcessLookupError): vanished+=1
        except PermissionError as error:
            # Metadata may establish PID identity/UID, never the absence of a
            # hidden MPI mapping. No cmdline/environment content is collected.
            try:
                now=proc(pid)
                if now['start_ticks']!=row['start_ticks']: vanished+=1;continue
                status={k:v.strip() for k,v in (line.split(':',1) for line in
                        Path(f'/proc/{pid}/status').read_text().splitlines() if ':' in line)}
                item={'pid':pid,'start_ticks':now['start_ticks'],'ppid':now['ppid'],
                      'comm':status.get('Name'),'UIDs':status.get('Uid'),'Kthread':status.get('Kthread'),
                      'maps_errno':error.errno,'maps_error':'PermissionError',
                      'kernel_identity_only':True,'MPI_absence_proven':False}
                try: item['exe_basename']=Path(os.readlink(f'/proc/{pid}/exe')).name
                except OSError as denied: item['exe_errno']=denied.errno
                unknown.append(item)
            except (FileNotFoundError,ProcessLookupError): vanished+=1
    self_status={k:v.strip() for k,v in (line.split(':',1) for line in
                 Path('/proc/self/status').read_text().splitlines() if ':' in line)}
    try: mpi_inventory(require_global=True)
    except Refusal as error: strict={'passed':False,'reason':str(error)}
    else: strict={'passed':True,'reason':'readable snapshot only; not continuous global exclusion'}
    counts={}
    for item in unknown:
        uid=item['UIDs'].split()[1];counts[uid]=counts.get(uid,0)+1
    report={'timestamp_UTC':datetime.now(timezone.utc).isoformat(),'unreadable':unknown,
            'unreadable_count':len(unknown),'unreadable_effective_UID_counts':counts,
            'readable_count':readable,'vanished_during_snapshot':vanished,
            'self_UIDs':self_status['Uid'],'self_CapEff':self_status['CapEff'],
            'CAP_SYS_PTRACE_effective':bool(int(self_status['CapEff'],16)&(1<<19)),
            'yama_ptrace_scope':Path('/proc/sys/kernel/yama/ptrace_scope').read_text().strip(),
            'strict_global_check':strict,'readable_namespace_MPI':mpi_inventory(),
            'native_inventory_gate':'UNKNOWN_REFUSE' if unknown or not strict['passed'] else 'SNAPSHOT_ONLY',
            'permissions_changed':False,'unrelated_processes_signalled':False,
            'owned_family_control':'pidfd-pinned observed descendants only; no authority over unreadable foreign processes',
            'decision':'STOP before any native fixture' if unknown or not strict['passed'] else 'Other native gates still required'}
    return report


if __name__=='__main__':
    import json
    from production_transport import BUILD
    report=inventory_evidence()
    (BUILD/'inventory.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ['timestamp_UTC','unreadable_count',
          'unreadable_effective_UID_counts','strict_global_check','native_inventory_gate']}))
