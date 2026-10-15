"""Focused result, provenance and protected-state validation; no native execution."""
from pathlib import Path
import ast,datetime,hashlib,json,subprocess
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
DFT=Path('/home/User/opencode_workspace/DFT')


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    target=HERE/'validation.json'
    if target.exists():raise FileExistsError('retain first final validation')
    for p in HERE.glob('*.py'):ast.parse(p.read_text(),filename=str(p))
    for p in HERE.glob('*.json'):json.loads(p.read_text())
    for name in ['result.json','derivative_result.json','tail_information.json']:
        for p,pin in json.loads((HERE/name).read_text())['source_sha256'].items():assert sha(p)==pin
    g=json.loads((HERE/'geometry_check.json').read_text());assert sha(HERE/'geometry_check.py')==g['source_sha256']
    v=json.loads((HERE/'verification.json').read_text());assert sha(HERE/'verify.py')==v['source_sha256']
    rows=json.loads((HERE/'result.json').read_text());f=np.load(HERE/'matrix_differences.npz');assert len(f.files)==18
    for row in rows['rows']:
        k=f"t{row['t_from_each_own_Fermi_eV']}_eta{row['eta_eV']}_deltaH";assert abs(np.linalg.norm(f[k],2)-row['deltaH_norm_eV'])<1e-13
    m=json.loads((HERE/'metadata_correction.json').read_text());assert sha(HERE/m['preserved_code_snapshot'])==m['old_code_sha256']
    old=json.loads((BASE/'same_density_hamiltonian_2026-10-15/protected_after.json').read_text())
    assert subprocess.check_output(['git','-C',str(DFT),'rev-parse','HEAD'],text=True).strip()==old['DFT_HEAD']
    assert subprocess.check_output(['git','-C',str(DFT),'status','--short'],text=True)==old['DFT_status']
    assert hashlib.sha256(subprocess.check_output(['git','-C',str(DFT),'diff','--binary'])).hexdigest()==old['DFT_tracked_diff_sha256']
    for p,pin in old['files'].items():assert sha(p)==pin
    native=BASE/'same_density_hamiltonian_2026-10-15';actual=DFT/'.local/qe75_lowram_20261011/h8h_20261015/p1/host/FINAL.json';assert sha(actual)==sha(native/'evidence/FINAL.json')
    final=json.loads(actual.read_text());assert final['accepted'] and not (Path('/sys/fs/cgroup')/final['guard']['cgroup'].lstrip('/')).exists()
    stock=json.loads((native/'build_results.json').read_text());assert sha(DFT/'.local/qe-env/lib/libqe_pw.a')==stock['stock_archive_sha256']
    output=dict(status='PASS focused retained physics/provenance/protected-state validation',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),retained_nine_matrix_arrays_match=True,all_primary_frozen_sources_match=True,geometry_two_orbits_and_independent_tail_checks_PASS=True,preserved_metadata_draft_matches=True,DFT_tracked_and_dirty_state_unchanged=True,stock_ELF_archive_unchanged=True,accepted_native_result_unchanged_and_cgroup_gone=True,new_native_jobs_in_this_package=0,HSE_converged=False,physical_xc=None,source_sha256=sha(Path(__file__)),files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name not in ['validation.log','validation.json']})
    target.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k!='files'},indent=2))


if __name__=='__main__':main()
