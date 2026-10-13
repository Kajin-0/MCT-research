# Minimum input at the EXX operator boundary

**PROVEN UNDER ASSUMPTIONS; established exchange-functional identity, not novelty.**
For the norm-conserving, fixed-cell spinor HSE operator, with fixed periodic
screened kernel, q mesh, symmetry maps and basis/FFT convention,

    gamma_{ss'}(r,r') = sum_{nk} w_k f_{nk} psi_{nks}(r) psi*_{nks'}(r')
    K[gamma]_{ss'}(r,r') = -alpha W_SR(r-r') gamma_{ss'}(r,r').

The local potential vrs is not an independent input of this fixed-orbital Fock
operator. It influences orbitals through SCF. Identical STARTUP orbitals therefore
do not certify identical operator inputs AFTER a preliminary SCF. A tiny local
potential difference also need not preserve the byte representation of a
near-degenerate orbital basis. No gap or topology statement follows.

For fixed trial columns Phi, V=K Phi and G=Phi†V, if G is invertible,
K_ACE=V G^{-1} V†. In QE's negative-definite Gram/Cholesky case this is
-Xi Xi†. Thus the minimal isolated operator comparison requires the canonical
source orbitals/occupations across all k/q, basis/symmetry/kernel conventions,
and trial inputs at the EXX boundary. It does not require a completed SCF or
matching unrelated histories. Floating-point implementations still require
measured action/Gram/energy checks; this identity is not a validation result.

The new control before-packets contain the actual Phi, occupation array and
native layout, and the FFT descriptors are retained. A proposed next scoped
fixture could consume those canonical inputs directly with authenticated native
readback and completeness checks, avoiding another control SCF and the observed
startup rho(real)/vrs reconstruction drift. The sufficiency of those packets
for ALL QE source-q mappings must be proven before implementation/execution.
This would be a new isolated operator acceptance claim; it cannot silently
promote the current failed full common-state gate or validate SCF/restart.

No further native experiment was run after the observed common-state mismatch.
