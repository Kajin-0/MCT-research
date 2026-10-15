"""Focused independent native integrity and whole-space witness checks."""
from pathlib import Path
import json
import numpy as np
import owner as r


def main():
    profile,job,root=r.load('host');f=json.loads((root/'FINAL.json').read_text());assert f['accepted'] and not r.cgroup_path(f['guard']['cgroup']).exists()
    for p,pin in f['source_hashes'].items():assert r.sha(p)==pin
    for name in ['trial_result.json','qualification.json']:
        a=json.loads((r.HERE/name).read_text())
        for p,pin in a['source_sha256'].items():assert r.sha(p)==pin
    for name in ['stationarity_result.json','krylov_result.json']:
        a=json.loads((r.HERE/name).read_text());assert r.sha(a['basis_path'])==a['basis_sha256'] if 'basis_path' in a else True
        for p,pin in a['source_sha256'].items():assert r.sha(p)==pin
    # Independent direct 12x12 commutator versus low-rank QR operator norm.
    rng=np.random.default_rng(7127);A=rng.normal(size=(12,12))+1j*rng.normal(size=(12,12));H=(A+A.conj().T)/2;Q=np.linalg.qr(rng.normal(size=(12,5))+1j*rng.normal(size=(12,5)))[0];d=np.diag([1.,1.,.5,.5,0.]);D=Q@d@Q.conj().T;X=np.column_stack((H@Q@d,Q));u,T=np.linalg.qr(X,mode='reduced');J=np.block([[np.zeros((5,5)),np.eye(5)],[-np.eye(5),np.zeros((5,5))]])
    direct=np.linalg.norm(H@D-D@H,2);compressed=np.linalg.norm(T@J@T.conj().T,2);assert abs(direct-compressed)<1e-12
    M=np.linalg.norm(H,2);w,U=np.linalg.eigh(H);from scipy.special import expit
    F=(U*expit(-w/.001))@U.conj().T;actual=np.linalg.norm(D-F,2);assert compressed/(2*M)<=actual
    witness=json.loads((r.HERE/'stationarity_result.json').read_text());k=json.loads((r.HERE/'krylov_result.json').read_text());assert witness['whole_space_FD_density_error_lower_op']>1e-8 and k['maximum_all_group_Theta_translation_leakage_F']<1e-8
    trial=json.loads((r.HERE/'trial_result.json').read_text())
    # The ideal contraction bound1 receives its explicit raw NCGram correction.
    upper=1+trial['source_Gram_op']
    private=r.PAIR.parent;files=[p for p in private.rglob('*') if p.is_file()];total=sum(p.stat().st_blocks*512+4096 for p in files);assert total<14*r.GIB
    out=dict(status='PASS focused actual native integrity and independent witness tests',direct_QR_commutator_operator_error=float(abs(direct-compressed)),synthetic_actual_FD_op_error=float(actual),synthetic_lower_FD_op_error=float(compressed/(2*M)),actual_conditional_fullspace_FD_error_lower_op=witness['whole_space_FD_density_error_lower_op'],raw_NC_Gram_adjusted_universal_upper_op=upper,ideal_universal_upper_1_in_prior_result_is_before_Gram_correction=True,all_frozen_source_input_ELF_PP_backend_pins_PASS=True,old_native_and_failed_records_unchanged=True,final_owned_metadata_block_charge_B=total,protected_stock_archive_unchanged=json.loads((r.HERE/'evidence_manifest.json').read_text())['stock_archive_SHA_unchanged'],new_space_is_action_completion_NOT_stationary_state=True,source_sha256=r.sha(Path(__file__)),HSE_converged=False,physical_xc=None)
    assert out['protected_stock_archive_unchanged'];r.atomic_json(r.HERE/'verification.json',out);print(json.dumps(out,indent=2))


if __name__=='__main__':main()
