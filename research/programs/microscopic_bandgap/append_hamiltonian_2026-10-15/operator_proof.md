# Why the append refers to the SAME native operator

No binary/source build or EXX/ACE change. Accepted native run_pwscf enters
r07_same_density_H immediately after init_run and returns before electrons.
It imports evc,wg and trials separately. sum_band's temporary fixed_occ branch
uses ONLY the imported natural evc/wg to construct D0; all trial arrays are
independent. Then native exxinit(false) activates HSE and constructs the Gamma/
q1 exchange source, v_of_rho/set_vrs/newd rebuild its local/nonlocal state,
g2_kin sets the kinetic operator. vloc_psi_nc,calbec/add_vuspsi,vexx apply those
fixed linear operators to trials. Native h_psi checks six unchanged probes.

Thus changing trial columns does not change D0 or H[D0]. For this assertion
the following dependencies are essential, not just equality of a small matrix:
exact source/wg and native physical reciprocal embedding; identical PP/ions/
cell/spin axes and ELF/backends/MPIlayout; identical actual rhoG/r,vrs,FFT/G/k;
native checked q1 mapping and exchange fraction/screening/cutoff; unchanged
exxinit and Coulomb/SOC construction at that same state. All are pinned,
source-checked or read back. Actual independent probes must also reproduce
bitwise. This is finite native-model equality, not a material error theorem.

Accepted old 152HQ columns and residual L are hashed. Full304basis V is NOT
assumed to preserve Q columns' QR phases. C=V*[Q,L] is invertible by the measured
Gram gate; HV=[HQ,HL] C^-1 follows linearly. Cross-block Q*HL=(L*HQ)* is an
independent Hermitian test; it is never imposed by symmetrizing bad data.
Only after the1e-8Hermiticity gate may a floating Hermitian part be passed to
eigh; archive the raw matrix and its defect. No symmetry averaging/force closure.

The source finite-natural weights stay1/.5/0; the new query L vectors are
auxiliary directions with NO assigned native solved-band occupations. FD in
304is a projected response of H[D0]; outer stationarity requires H evaluated
at the resulting density as well as controlled complement/tail information.
