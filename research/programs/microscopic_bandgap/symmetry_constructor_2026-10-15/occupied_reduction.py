"""Read-only natural-occupation reduction of the NEW ensemble, not old-run repair."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh

HERE=Path(__file__).resolve().parent


def main():
    measured=json.loads((HERE/'numerical_result.json').read_text());assert measured['scientific_pass']
    data=np.load(HERE/'operator_matrices.npz');H=data['positive_Gram'];D=data['constrained_density']
    occupation,V=eigh((D+D.conj().T)/2)
    # Explicit native eps_occ threshold, chosen before seeing new reduction.
    keep=occupation>1e-8; C=V[:,keep]; omitted=occupation[~keep]
    n=len(H);J=np.kron(np.eye(n//2),np.array([[0.,-1.],[1.,0.]]))
    TC=J@C.conj();leak=float(np.linalg.norm(TC-C@(C.conj().T@TC),2))
    hc=C.conj().T@H@C;he=eigh((hc+hc.conj().T)/2,eigvals_only=True)
    # Small-coordinate form of full, source-exact positive compression.
    W=H@C
    Hc=W@np.linalg.solve(hc,W.conj().T)
    Dkeep=(C*occupation[keep])@C.conj().T
    exact_action=float(np.linalg.norm(Hc@C-H@C)/max(1.,np.linalg.norm(H@C)))
    tr_error=float(np.linalg.norm(Hc-J@Hc.conj()@J.T,2))
    energy_full=float(-np.trace(D@H).real/2)
    energy_compressed=float(-np.trace(D@Hc).real/2)
    omitted_positive_charge=float(sum(np.maximum(omitted,0)))
    tail_energy_bound=.5*measured['operator_norm_upper_Ry']*omitted_positive_charge
    assert sum(keep)==146 and leak<1e-10 and min(he)>1e-6
    assert exact_action<1e-10 and tr_error<1e-10
    assert abs(energy_full-energy_compressed)<=tail_energy_bound+1e-11
    result=dict(status='CALCULATED post-acquisition occupied-ensemble reduction; no new native SCF or acceptance revision',
        occupation_threshold=1e-8,retained_natural_rank=int(sum(keep)),
        retained_charge_e=float(sum(occupation[keep])),discarded_positive_charge_e=omitted_positive_charge,
        retained_occupation_min=float(min(occupation[keep])),retained_occupation_max=float(max(occupation[keep])),
        dropped_density_op_upper=float(max(abs(omitted))),
        occupied_support_TR_leakage_op=leak,positive_Gram_min_Ry=float(min(he)),positive_Gram_condition=float(max(he)/min(he)),
        occupied_source_exact_action_relative=exact_action,coordinate_compression_TR_error_op_Ry=tr_error,
        full_density_half_Fock_Ry=energy_full,compressed_half_Fock_Ry=energy_compressed,
        energy_change_Ry=energy_compressed-energy_full,conditional_discarded_density_energy_upper_Ry=tail_energy_bound,
        original_density_not_preserved=True,natural_occupations_not_native_FD_of_old_Hamiltonian=True,
        native_ACE_integrated=False,joint_Td_translation_symmetry_not_qualified=True,HSE_converged=False,physical_xc=None)
    np.savez(HERE/'occupied_reduction_matrices.npz',occupied_basis_in_Q=C,occupations=occupation[keep],occupied_density_in_Q=Dkeep)
    (HERE/'occupied_reduction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
