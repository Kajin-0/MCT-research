"""Bounded compile/link only, in NEW ignored MCT scratch. Never execute QE."""
from pathlib import Path
import hashlib
import json
import os
import resource
import shutil
import subprocess
import time

HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3]
OLD=HERE.parent/'static_environment_2026-10-15'
PRIVATE=REPO/'.tmp/r07spc16';BUILD=PRIVATE/'build2'
DFT=Path('/home/User/opencode_workspace/DFT')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    previous=json.loads((OLD/'build_result.json').read_text())
    frozen=json.loads((OLD/'frozen_protocol.json').read_text())
    for p,h in frozen['profile']['pins'].items():
        if sha(p)!=h:raise ValueError('old pin changed: '+p)
    stock=DFT/'.local/qe-env/lib/libqe_pw.a';before=sha(stock)
    if before!=previous['stock_archive_sha256']:raise ValueError('stock archive changed')
    mem=int(next(s.split()[1] for s in Path('/proc/meminfo').read_text().splitlines() if s.startswith('MemAvailable:')))*1024
    free=shutil.disk_usage(REPO).free
    if mem<4*(1<<30) or free<11*(1<<30):raise ValueError('compile resource floor')
    if BUILD.exists():raise FileExistsError('fresh private build only; no retries')
    BUILD.mkdir(parents=True,mode=0o700)
    packet_reader=HERE.parent/'pbe_static_admission_2026-10-16/packet_reader.py'
    (HERE/'packet_reader.py').write_bytes(packet_reader.read_bytes())
    pristine=next(Path(p) for p in previous['source_pins'] if p.endswith('pristine_run_pwscf.f90'))
    source=pristine.read_text();anchor='  CALL init_run()\n  !\n  !  read external force'
    assert source.count(anchor)==1
    source=source.replace(anchor,'  CALL r07_static_phase(1,0_8)\n  CALL init_run()\n  CALL r07_static_H()\n'
        '  exit_status=0\n  CALL qexsd_set_status(exit_status)\n  RETURN ! saved-density static actions only\n  !\n  !  read external force')
    probe=(OLD/'native_probe.inc').read_text()
    oldprefix='/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/p16h_20261015/jobs/'
    assert probe.count(oldprefix)==1
    probe=probe.replace(oldprefix,str(PRIVATE/'jobs')+'/')
    probe=probe.replace('INTEGER(8)::header(16),h(16),fft(14,2)','INTEGER(8)::header(16),h(16),fft(14,2),packet_bytes')
    anchor=' CLOSE(u)\n CALL mp_barrier(intra_bgrp_comm)'
    assert probe.count(anchor)==1
    probe=probe.replace(anchor," FLUSH(u,IOSTAT=ios)\n IF(ios/=0)CALL errore('staticH','packet flush',1)\n"
        " INQUIRE(UNIT=u,SIZE=packet_bytes,IOSTAT=ios)\n"
        " IF(ios/=0.OR.packet_bytes<1_8.OR.packet_bytes>1073741824_8)CALL errore('staticH','packet size',1)\n"
        " CLOSE(u,IOSTAT=ios)\n IF(ios/=0)CALL errore('staticH','packet close',1)\n"
        " CALL mp_barrier(intra_bgrp_comm)\n CALL r07_static_phase(10,packet_bytes)")
    # A saved-wfc fallback must not pass the separately pinned source contract.
    probe=probe.replace('USE starting_scf,ONLY:starting_pot','USE starting_scf,ONLY:starting_pot,starting_wfc')
    probe=probe.replace("starting_pot/='file'.OR.","starting_pot/='file'.OR.starting_wfc/='file'.OR.")
    (HERE/'native_probe.inc').write_text(probe)
    source+='\n'+probe+'\n'+(HERE/'native_phase.inc').read_text()
    src=BUILD/'run_pwscf.f90';src.write_text(source)
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(BUILD))
    def limits():
        resource.setrlimit(resource.RLIMIT_AS,(2*(1<<30),2*(1<<30)))
        resource.setrlimit(resource.RLIMIT_CPU,(60,60))
        resource.setrlimit(resource.RLIMIT_FSIZE,(512*(1<<20),512*(1<<20)))
        resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    records=[]
    def run(cmd):
        start=time.monotonic()
        r=subprocess.run(cmd,cwd=BUILD,env=env,capture_output=True,text=True,timeout=90,preexec_fn=limits)
        records.append(dict(command=cmd,returncode=r.returncode,wall_s=time.monotonic()-start,stdout=r.stdout,stderr=r.stderr))
        (HERE/'build_result.json').write_text(json.dumps(dict(passed=False,records=records),indent=2)+'\n')
        if r.returncode:raise RuntimeError(r.stderr)
    cmd=previous['records'][0]['command'].copy()
    cmd[cmd.index('-J')+1]=str(BUILD);cmd[cmd.index('-c')+1]=str(src);cmd[cmd.index('-o')+1]=str(BUILD/'run_pwscf.f90.o')
    run(cmd)
    cc='/usr/bin/cc';run([cc,'-std=c11','-O2','-Wall','-Wextra','-Werror','-c',str(HERE/'native_lease.c'),'-o',str(BUILD/'native_lease.o')])
    lib=BUILD/'libqe_pw_static.a';shutil.copy2(stock,lib)
    run(['/usr/bin/ar','r',str(lib),str(BUILD/'run_pwscf.f90.o')])
    link=previous['records'][2]['command'].copy()
    link[link.index(previous['records'][1]['command'][2])]=str(lib)
    link.insert(2,str(BUILD/'native_lease.o'));link[link.index('-o')+1]=str(BUILD/'pw.static_completion.UNEXECUTED')
    run(link)
    symbols=subprocess.check_output(['/usr/bin/nm','-g','--defined-only',str(BUILD/'pw.static_completion.UNEXECUTED')],text=True)
    assert all(v in symbols for v in ['r07_static_phase_','r07_static_lease','r07_static_h_'])
    assert sha(stock)==before
    originals={**frozen['profile']['pins'],**previous['source_pins'],**previous['backends']}
    assert all(sha(p)==h for p,h in originals.items())
    pins={str(p):sha(p) for p in [pristine,src,HERE/'native_probe.inc',HERE/'native_phase.inc',HERE/'native_lease.c',
        BUILD/'run_pwscf.f90.o',BUILD/'native_lease.o',BUILD/'pw.static_completion.UNEXECUTED',Path(cmd[0]),Path(cc).resolve()]}
    out=dict(passed=True,records=records,binary=str(BUILD/'pw.static_completion.UNEXECUTED'),
        binary_sha256=sha(BUILD/'pw.static_completion.UNEXECUTED'),source_object_ELF_pins=pins,
        unchanged_originals=originals,stock_archive_sha256=before,replaced_archive_member='run_pwscf.f90.o',
        additional_object='native_lease.o',native_QE_MPI_execution=False,
        actual_collective_runtime_qualification=False,build_RLIMIT_AS_B=2*(1<<30),
        build_outputs_bytes=sum(p.stat().st_size for p in BUILD.iterdir() if p.is_file()),
        host_before=dict(MemAvailable_B=mem,free_disk_B=free),future_pair_root=str(PRIVATE/'jobs'))
    (HERE/'build_result.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['passed','binary_sha256','native_QE_MPI_execution','actual_collective_runtime_qualification']},indent=2))


if __name__=='__main__':main()
