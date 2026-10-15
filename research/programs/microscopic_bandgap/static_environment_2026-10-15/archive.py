"""Focused source/raw/protected-state checks, preserving native owner failure."""
from pathlib import Path
import ast,json,hashlib,subprocess,sys
HERE=Path(__file__).resolve().parent;DFT=Path('/home/User/opencode_workspace/DFT');ROOT=DFT/'.local/qe75_lowram_20261011/p16h_20261015'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    target=HERE/'evidence_manifest.json'
    if target.exists():raise FileExistsError('preserve first final archive')
    frozen=json.loads((HERE/'frozen_protocol.json').read_text())
    for p,h in frozen['profile']['pins'].items():assert sha(p)==h
    before=json.loads((HERE/'protected_before.json').read_text())
    assert subprocess.check_output(['git','-C',str(DFT),'status','--short'],text=True)==before['DFT_status']
    assert hashlib.sha256(subprocess.check_output(['git','-C',str(DFT),'diff','--binary'])).hexdigest()==before['DFT_tracked_diff_sha256']
    for p,h in before['files'].items():assert sha(p)==h
    root=ROOT/'jobs/unshared';g=json.loads((root/'GUARD_RESULT.json').read_text());assert not g['pass_guard'] and 'unbound/incomplete' in g['error'];assert not (Path('/sys/fs/cgroup')/g['cgroup'].lstrip('/')).exists()
    assert not (ROOT/'jobs/shared/LAUNCH.json').exists() and not (root/'FINAL.json').exists()
    for name in ['pw.static','pw.x','mpirun','prterun']:
        v=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True);assert v.returncode==1 and not v.stdout
    for member,files in frozen['profile']['copied_saves'].items():
        for p,row in files.items():assert sha(p)==row['sha256'] and sha(row['source'])==row['sha256']
    for p in HERE.glob('*.py'):ast.parse(p.read_text())
    ev=HERE/'evidence';ev.mkdir();records={}
    for name in ['pw.in','pw.out','JOB.json','READY.json','RANKS.json','LAUNCH.json','REFERENCED.json','GUARD_RESULT.json','TERMINAL.json','launch_stderr.json','launch_stdout.json','telemetry.jsonl']:
        p=root/name;dst=ev/name;dst.write_bytes(p.read_bytes());records[str(p)]=dict(sha256=sha(p),archived=str(dst.relative_to(HERE)))
    for p in (root/'pilot').iterdir():records[str(p)]=dict(sha256=sha(p),bytes=p.stat().st_size,private_raw_retained=True)
    allocated=sum(p.stat().st_blocks*512+4096 for p in ROOT.rglob('*') if p.is_file());assert allocated<14*2**30
    build=json.loads((HERE/'build_result.json').read_text());assert sha(DFT/'.local/qe-env/lib/libqe_pw.a')==build['stock_archive_sha256']
    diagnostic=json.loads((HERE/'unshared_diagnostic.json').read_text());assert diagnostic['science']['scientific_pass'] and not diagnostic['owner_accepted']
    result=dict(status='PASS evidence/source/protected checks; native OWNER FAIL remains; shared NOT RUN',raw=records,all_frozen_source_input_PP_ELF_pins_unchanged=True,DFT_protected_exact=True,copied_saves_and_originals_unchanged=True,stock_archive_unchanged=True,owned_cgroup_gone_and_known_MPI_absent=True,all_private_output_block_metadata_charge_B=allocated,readback_import_defect_preserved_and_manual_diagnostic_only=True,no_pair_or_material_validation=True,HSE_converged=False,physical_xc=None,source_sha256=sha(Path(__file__)))
    target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='raw'},indent=2))


if __name__=='__main__':main()
