#!/usr/bin/env python3
"""One foreground approved pair member, never a queue or detached supervisor.

Creates only a fresh contained native output; prepared/dirty/source files and
existing supervisors are immutable. Cd admission requires an explicit passed
host gate, not merely JOB DONE. No retry, restart or alternate physical inputs.
"""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from mct_dft.process_family import ProcessFamily

PAIR = ROOT/"calculations/r07/cd_in_hg_pair_n2_k2_q2_e90_f120_prepare"
GIB = 1024**3


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(262144),b''): h.update(chunk)
    return h.hexdigest()


def memory():
    return {k:int(v)*1024 for k,v in re.findall(r'^(\w+):\s+(\d+) kB$',Path('/proc/meminfo').read_text(),re.M)}


def mpi_rows():
    rows=[]
    text=subprocess.check_output(['ps','-eo','pid=,comm='],text=True)
    for line in text.splitlines():
        pid,comm=line.split(maxsplit=1)
        if comm in {'pw.x','prterun','mpirun','mpiexec','prted','orted'}:
            rows.append({'pid':int(pid),'comm':comm})
    return rows


def changed_input(source, outdir):
    if re.search(r'(?m)^\s*nstep\s*=\s*0',source):
        raise ValueError('Never execute a dry deck as an SCF')
    target=re.sub(r"(?m)^\s*outdir\s*=.*$",f"   outdir = '{outdir}'",source)
    target=re.sub(r'(?m)^\s*max_seconds\s*=.*$', '   max_seconds = 3600.0',target)
    strip=lambda t: re.sub(r'(?m)^\s*(outdir|max_seconds)\s*=.*\n','',t)
    if strip(source)!=strip(target): raise ValueError('Physical input changed')
    return target


def native_terminal(text, err, returncode, exit_requested, forced, remaining):
    accuracy=re.findall(r'estimated scf accuracy\s*<\s*([0-9.eE+\-]+)\s*Ry',text)
    final_accuracy=float(accuracy[-1]) if accuracy else None
    result={'returncode':returncode,'job_done':'JOB DONE' in text,
            'inner_scf_converged':'convergence has been achieved' in text,
            'exx_converged':'EXX self-consistency reached' in text,
            'native_time_limit':('Maximum CPU time exceeded' in text or 'Calculation (EXX) stopped after iteration' in text),
            'native_error_detected':('Error in routine' in text or 'MPI_ABORT' in err),
            'final_reported_scf_accuracy_Ry':final_accuracy,
            'exit_requested':exit_requested,'forced_termination':forced,
            'all_native_processes_terminated':not remaining}
    result['accepted_scf']=bool(returncode==0 and result['job_done'] and result['inner_scf_converged']
        and result['exx_converged'] and not exit_requested and not forced and not remaining
        and not result['native_error_detected'] and not result['native_time_limit']
        and final_accuracy is not None and final_accuracy<=1e-10)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_pair',type=Path)
    parser.add_argument('member',choices=['host','impurity'])
    args=parser.parse_args()
    root=args.output_pair.resolve()
    if not root.is_relative_to(ROOT/'calculations/r07') or root==PAIR:
        raise ValueError('A separate contained output pair is required')
    source=PAIR/args.member/'pw.in'
    prepared=json.loads((PAIR/'preparation.json').read_text())
    if digest(source)!=prepared['inputs_sha256'][args.member]['pw.in']:
        raise ValueError('Prepared deck changed')
    for element,expected in prepared['pp_sha256'].items():
        if digest(ROOT/f'pseudopotentials/{element}_sg15_pbe_fr_v12.UPF')!=expected:
            raise ValueError('Potential checksum changed')
    if args.member=='impurity':
        gate=json.loads((root/'host/host_gate.json').read_text())
        prior=json.loads((root/'host/result.json').read_text())
        if not gate.get('accepted_for_substitution') or not prior.get('accepted_scf'):
            raise ValueError('Host scientific gate has not passed')
    (ROOT/'.tmp').mkdir(exist_ok=True)
    lock=(ROOT/'.tmp/r07_explicit_approved_pair.lock').open('a+')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if mpi_rows(): raise RuntimeError('Existing MPI family; no launch')
    mem=memory();disk=shutil.disk_usage(ROOT)
    estimate={'host':21.27,'impurity':21.32}[args.member]
    if mem['MemAvailable']<(1.2*estimate+2)*GIB or disk.free<8*GIB:
        raise RuntimeError('Immediate resource guard failed; no launch')
    run=root/args.member
    run.mkdir(parents=True,exist_ok=False)
    (run/'out').mkdir()
    (run/'pw.in').write_text(changed_input(source.read_text(),run/'out'))
    states=[ROOT/'calculations/r07/fock_followthrough_5eed5ea4/state.json',
            ROOT/'calculations/r07/reference_queue_5eed5ea4_recovered/state.json']
    pinned={str(p):digest(p) for p in [source,PAIR/'preparation.json',*states]}
    rss_limit=min(.85*mem['MemTotal'],mem['MemAvailable']-2*GIB)
    command=[str(ROOT/'.local/qe-env/bin/mpirun'),'-np','6',str(ROOT/'.local/qe-env/bin/pw.x'),'-in','pw.in']
    record={'claim_status':'CALCULATED native numerical pilot only; physical impurity/material accuracy not validated',
            'member':args.member,'run':str(run),'command':command,'mpi_ranks':6,
            'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'driver_sha256':digest(__file__),'process_family_module_sha256':digest(ROOT/'src/mct_dft/process_family.py'),
            'input_sha256':digest(run/'pw.in'),'prepared_input_sha256':digest(source),
            'pp_sha256':prepared['pp_sha256'],'source_and_supervisor_hashes':pinned,
            'started_utc':datetime.now(timezone.utc).isoformat(),'RAM_preflight_bytes':mem,
            'disk_free_at_launch_bytes':disk.free,'process_family_RSS_limit_bytes':rss_limit,
            'seconds':3600,'grace_seconds':1800,'empirical_alloy_gap_inputs':[],
            'RSS_scope':'launcher plus identity-tracked recursive descendants; summation may overcount shared pages',
            'sampling_seconds':2,'physical_xc':None}
    (run/'provenance.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    start=time.monotonic();forced=False;exit_requested=False;reason=None
    min_available=mem['MemAvailable'];min_disk=disk.free
    env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    print(json.dumps({'START':str(run),'RSS_limit_GiB':rss_limit/GIB}),flush=True)
    with (run/'pw.out').open('w') as out,(run/'pw.err').open('w') as err,(run/'telemetry.jsonl').open('w') as telemetry:
        proc=subprocess.Popen(command,cwd=run,stdout=out,stderr=err,env=env,start_new_session=True)
        family=ProcessFamily(proc.pid)
        (run/'process.json').write_text(json.dumps({'launcher_pid':proc.pid,'started_utc':record['started_utc']})+'\n')
        try:
            while proc.poll() is None:
                elapsed=time.monotonic()-start
                global_mpi=mpi_rows()
                snap=family.snapshot();current=memory();space=shutil.disk_usage(ROOT)
                min_available=min(min_available,current['MemAvailable']);min_disk=min(min_disk,space.free)
                own=set(snap['processes'])
                foreign=[p for p in global_mpi if p['pid'] not in own and Path(f"/proc/{p['pid']}").exists()]
                row={'elapsed_seconds':elapsed,'RSS_bytes':snap['RSS_bytes'],'process_count':len(own),
                     'available_RAM_bytes':current['MemAvailable'],'disk_free_bytes':space.free,
                     'foreign_MPI':foreign}
                telemetry.write(json.dumps(row)+'\n');telemetry.flush()
                if not exit_requested and (elapsed>3600 or current['MemAvailable']<4*GIB or space.free<8*GIB):
                    (run/'out/r07.EXIT').touch();exit_requested=True
                    reason='native_time_or_soft_resource_stop'
                if snap['RSS_bytes']>rss_limit or current['MemAvailable']<2*GIB or space.free<4*GIB or elapsed>5400 or foreign:
                    forced=True
                    reason=('foreign_MPI_ownership_conflict' if foreign else 'hard_resource_or_time_stop')
                    family.stop(proc);break
                time.sleep(2)
        except BaseException:
            family.stop(proc)
            raise
    proc.wait();remaining=family.snapshot()['processes']
    text=(run/'pw.out').read_text();err=(run/'pw.err').read_text()
    record.update(native_terminal(text,err,proc.returncode,exit_requested,forced,remaining))
    record.update(wall_seconds=time.monotonic()-start,termination_reason=reason,
                  QE_version_line=next((line.strip() for line in text.splitlines() if 'Program PWSCF' in line),None),
                  measured_peak_process_family_RSS_bytes=family.peak_RSS_bytes,
                  measured_peak_process_family_count=family.peak_process_count,
                  minimum_sampled_available_RAM_bytes=min_available,minimum_sampled_disk_free_bytes=min_disk,
                  output_bytes=sum(p.stat().st_size for p in run.rglob('*') if p.is_file()),
                  stdout_sha256=digest(run/'pw.out'),stderr_sha256=digest(run/'pw.err'),
                  source_and_supervisor_hashes_unchanged=all(digest(p)==h for p,h in pinned.items()),
                  finished_utc=datetime.now(timezone.utc).isoformat())
    (run/'result.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:record[k] for k in ['run','wall_seconds','accepted_scf','termination_reason',
        'measured_peak_process_family_RSS_bytes','minimum_sampled_available_RAM_bytes','minimum_sampled_disk_free_bytes']}),flush=True)


if __name__=='__main__': main()
