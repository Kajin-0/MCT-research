"""Combine immutable local-only and provisional relativistic nonlocal R08 Γ matrices.
No native computation or changes to archived raw data.
"""
from pathlib import Path
import json
import numpy as np
p=Path(__file__).resolve().parent
l=json.loads((p/"bare_local_gamma_result.json").read_text())
n=json.loads((p/"nonlocal_gamma_provisional.json").read_text())
def complex_matrix(a):
    x=np.asarray(a,dtype=float)
    assert x.shape==(6,6,2)
    return x[:,:,0]+1j*x[:,:,1]
L=complex_matrix(l["matrix_eV"])
N=complex_matrix(n["nonlocal_delta_matrix"])
T=L+N
def contrast(x):
    return float(np.trace(x[:2,:2]).real/2-np.trace(x[2:,2:]).real/4)
assert max(abs(T-T.conj().T).flatten())<2e-12
assert abs(contrast(L)-l["gamma6_minus_gamma8_local_eV"])<1e-12
assert abs(contrast(N)-n["nonlocal_Cd_minus_Hg"]["sector_contrast"])<1e-12
assert abs(contrast(T)-contrast(L)-contrast(N))<1e-12
out={
"status":"PROVISIONAL_BARE_IONIC_COMMON_BASIS__INDEPENDENT_QE_ACTION_UNVERIFIED",
"local_trace_difference_eV":contrast(L),
"nonlocal_trace_difference_eV":contrast(N),
"total_trace_difference_eV":contrast(T),
"total_Gamma6_mean_eV":float(np.trace(T[:2,:2]).real/2),
"total_Gamma8_mean_eV":float(np.trace(T[2:,2:]).real/4),
"total_Gamma6_Gamma8_cross_block_fro_eV":float(np.linalg.norm(T[:2,2:])),
"full_6x6_eV":[[[float(z.real),float(z.imag)] for z in row] for row in T],
"vca_parent_identity_max_abs_eV":n["vca_identity_max_abs_eV"],
"parent_operator_independent_QE_action_validation":False,
"strict_native_density_symmetry_gate":"FAIL 1e-8",
"physics_not_claimed":["nonempirical bandgap derivative","screened impurity potential","alloy linewidth","disorder-renormalized mass","physical x_c"]
}
(p/"complete_bare_gamma_provisional.json").write_text(json.dumps(out,indent=2)+"\n")
print({k:v for k,v in out.items() if k.endswith("_eV") and not isinstance(v,list)})
