"""Archive one completed native H query, exact protected state and components."""
from pathlib import Path
import fcntl,json,os,subprocess
import numpy as np
import owner as r
from readback import decode


def main():
    if (r.HERE/'evidence_manifest.json').exists():raise FileExistsError('immutable evidence archive')
    p,j,root=r.load('host');final=json.loads((root/'FINAL.json').read_text());assert final['accepted'] and final['terminal_pass']
    assert not r.cgroup_path(final['guard']['cgroup']).exists()
    out=(root/'pw.out').read_text();assert 'R07_SAME_D_FULL_H_COMPLETE' in out and 'JOB DONE.' in out
    old=json.loads((r.HERE.parent/'pair_environment_2026-10-15/protected_after.json').read_text())
    assert subprocess.check_output(['git','-C',str(r.DFT),'status','--short'],text=True)==old['DFT_status']
    assert r.hashlib.sha256(subprocess.check_output(['git','-C',str(r.DFT),'diff','--binary'])).hexdigest()==old['DFT_tracked_diff_sha256']
    for path,pin in old['files'].items():assert r.sha(path)==pin
    for name in ['pw.x','mpirun','prterun']:
        v=subprocess.run(['pgrep','-a','-x',name],text=True,capture_output=True);assert v.returncode==1 and not v.stdout
    lock=os.open(r.LOCK,os.O_RDONLY|os.O_CLOEXEC)
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:os.close(lock)
    registry=r.sha(r.REGISTRY);assert registry==json.loads((r.HERE/'preflight.json').read_text())['old_registry_sha256']
    ev=r.HERE/'evidence';ev.mkdir();files={}
    for name in ['pw.in','pw.out','JOB.json','READY.json','REFERENCED.json','LAUNCH.json','RANKS.json','GUARD_RESULT.json','TERMINAL.json','FINAL.json','telemetry.jsonl','launch_stderr.json']:
        src=root/name;dst=ev/name;dst.write_bytes(src.read_bytes());assert r.sha(src)==r.sha(dst);files[str(src)]=dict(sha256=r.sha(src),archived=str(dst.relative_to(r.HERE)))
    for file in (root/'pilot').iterdir():files[str(file)]=dict(sha256=r.sha(file),bytes=file.stat().st_size,private_native_raw_retained=True)
    private=r.PAIR.parent;inventory=[dict(path=str(f),allocated_B=f.stat().st_blocks*512,bytes=f.stat().st_size,sha256=r.sha(f)) for f in private.rglob('*') if f.is_file()];charged=sum(a['allocated_B']+4096 for a in inventory);assert charged<14*r.GIB
    basis=np.load(private/'trial.npz');P=basis['P'];N=len(basis['G']);lookup={tuple(g):i for i,g in enumerate(basis['G'])};comp={k:np.zeros((2*N,6),complex) for k in ['kin','loc','nl','fock']}
    for rank in [0,1]:
        b=decode(root/'pilot'/f'H.rank{rank}');n,pw=int(b['h'][5]),int(b['h'][4]);active=np.r_[np.arange(n),np.arange(pw,pw+n)];ix=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[ix,N+ix]
        for k in comp:comp[k][glob]=b[k][active,152:158]
    blocks={k:P.conj().T@v for k,v in comp.items()};H=sum(blocks.values());saved=np.load(r.HERE/'native_matrices.npz')['H_reference'];assert np.max(abs(H-saved))<1e-12
    data={}
    for k,h in blocks.items():
        g6=np.trace(h[:2,:2])/2;g8=np.trace(h[2:,2:])/4;data[k]=dict(Gamma6_trace_Ry=float(g6.real),Gamma8_trace_Ry=float(g8.real),ordering_component_eV=float((g6-g8).real*13.605693122994),not_a_separate_gap=True)
    spectrum=np.linalg.eigvalsh((H[2:,2:]+H[2:,2:].conj().T)/2)
    r.atomic_json(r.HERE/'projection_components.json',dict(components=data,sum_ordering_eV=sum(v['ordering_component_eV'] for v in data.values()),projected_Gamma8_block_eigenvalues_Ry=spectrum.tolist(),projected_Gamma8_block_spread_eV=float(np.ptp(spectrum)*13.605693122994),full_H_sum_check_abs_Ry=float(np.max(abs(H-saved))),not_native_SCF_eigenvalues=True))
    r.atomic_json(r.HERE/'protected_after.json',old)
    r.atomic_json(r.HERE/'evidence_manifest.json',dict(raw=files,all_private_files=inventory,final_owned_allocated_metadata_charge_B=charged,protected_DFT_exact=True,stock_archive_SHA_unchanged=r.sha(r.DFT/'.local/qe-env/lib/libqe_pw.a')==json.loads((r.HERE/'build_results.json').read_text())['stock_archive_sha256'],old_registry_sha256=registry,no_live_known_MPI_QE=True,archive_code_sha256=r.sha(Path(__file__))))
    print(json.dumps(dict(all_native_owner_science_pass=True,protected_exact=True,owned_total_B=charged,component_sum_eV=sum(v['ordering_component_eV'] for v in data.values()),projected_Gamma8_spread_eV=float(np.ptp(spectrum)*13.605693122994)),indent=2))


if __name__=='__main__':main()
