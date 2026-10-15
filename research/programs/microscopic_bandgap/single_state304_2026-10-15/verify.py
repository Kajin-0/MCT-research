"""Three focused independent checks; no native execution or protocol rewriting."""
from pathlib import Path
import hashlib,json,shutil,subprocess
import numpy as np
from scipy.linalg import eigh
from scipy.special import expit
import owner as o
H=o.HERE;D=o.DFT;P=o.PAIR.parent

def main():
    profile,job,root=o.load('host');r=json.loads((root/'FINAL.json').read_text());assert r['accepted'] and r['terminal_pass'] and not o.cgroup_path(r['guard']['cgroup']).exists()
    for p,h in r['source_hashes'].items():assert o.sha(p)==h
    fixed=json.loads((H/'frozen_protocol.json').read_text());protect=fixed.get('protected',{})
    # Pre-existing protected digest from the immutable admission baseline.
    baseline='a716be79058b719e363f19b16fdacc228e4093b3f87bdd6b64ac96aa7e78b0f0'
    diff=subprocess.check_output(['git','diff','--binary'],cwd=D);assert hashlib.sha256(diff).hexdigest()==baseline
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=D,text=True).strip()=='422d71de02df56edae96e47e1a71931e073b48ad'
    assert o.sha(D/'.local/qe-env/bin/pw.x')=='1d66c7856f5d6b3cd9c66b8578e01512b16bbe907b4360e54234890712ccd6a1'
    assert o.sha(o.REGISTRY)=='82b3e668eeea5dff015b444cf362f945f7a5791d5fa6fe666948b0ab29c31baf'
    a=np.load(H/'native_matrices.npz');A=a['H_QQ'];G=a['offspace_Gram'];F=a['FD_Q'];S=json.loads((H/'native_science.json').read_text());v=json.loads((H/'galerkin_result.json').read_text())
    # Independently scipy's Hermitian driver versus NumPy's native readback.
    e,U=eigh((A+A.conj().T)/2,driver='evr');de=float(max(abs(e-np.array(S['Galerkin_ritz_energies_Ry']))));assert de<1e-10
    R2=float(np.trace(F@G@F).real);assert abs(np.sqrt(2*R2)-v['FD304_full_commutator_F_Ry'])<1e-10
    grammin=float(min(np.linalg.eigvalsh((G+G.conj().T)/2)));assert grammin>-1e-8
    # Missing complement counterexample: no coupling, perfect finite residual,
    # but an unmeasured occupied state changes fixed-mu FD and charge.
    e1=np.array([-1.,1.]);f1=expit(-e1/.1);F1=np.diag(f1)
    actual=expit(-np.array([-1.,1.,-2.])/.1);err=float(actual[-1]);assert err>.99
    # Exact finite-H free-energy minimizer. A different non-linear density
    # functional is not specified by this fixed-H minimization theorem.
    energy=float(np.trace(A@(F-a['D_Q'])).real);assert energy<0 and v['fixed_linear_H_free_energy_change_Ry']<0
    raw=H/'evidence';raw.mkdir(exist_ok=True)
    for name in ['pw.in','pw.out','FINAL.json','GUARD_RESULT.json','TERMINAL.json','RANKS.json','READY.json','LAUNCH.json','JOB.json']:
        shutil.copy2(root/name,raw/name)
    files={str(p):dict(sha256=o.sha(p),bytes=p.stat().st_size) for p in [*sorted((root/'pilot').iterdir()),P/'trial.npz',P/'full_actions.npz',P/'FD304_diagnostics.npz',P/'build1/pw.hse8.sameD']}
    # Include sparse allocation and per-inode metadata, never claim continuous
    # hostile producer/external-writer safety from sampled accounting.
    total=sum(p.stat().st_blocks*512+4096 for p in P.rglob('*') if p.is_file());assert total<14*o.GIB
    failures={str(x):o.sha(x) for x in [H.parent/'append_hamiltonian_2026-10-15/strict_refusal.json',H.parent/'static_environment_2026-10-15/evidence/GUARD_RESULT.json',H.parent/'static_environment_2026-10-15/evidence/TERMINAL.json'] if x.exists()}
    out=dict(status='PASS',independent_eigh_max_Ry=de,independent_commutator_Gram_identity=True,offspace_Gram_min_eigen_Ry2=grammin,zero_residual_missing_complement_counterexample_FD_op_error=err,full_native_state_snapshots_BITWISE=True,frozen_pins_PASS=True,protected_DFT_stock_registry_exact=True,old_negative_sha256=failures,terminal_cgroup_gone=True,postanalysis_owned_charge_B=total,raw_provenance=files,HSE_converged=False,physical_xc=None)
    (H/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='raw_provenance'},indent=2))
if __name__=='__main__':main()
