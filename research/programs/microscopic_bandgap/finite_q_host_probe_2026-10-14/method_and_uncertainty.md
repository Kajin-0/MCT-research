# Fixed Γ-frame finite-q host probe

This is a calculation on retained native HgTe HSE+SOC wavefunctions, not a new
DFT run. It deliberately defines a coherent-host wavepacket probe rather than
pretending to possess a Cd substitution potential. Previous physical-projection,
directional-covariance, finite-cell/T-matrix and threshold negatives remain.

## Observable and alignment

Take the previously Td-qualified Γ6 doublet and Γ8 quartet from the accepted
primitive HgTe f120/k4/q4 reference. Denote their normalized cell-periodic
spinors by χ_a. For every retained k, specify the representative fractional k
in [-1/2,1/2); relabel reciprocal vectors so G+k is unchanged. The probe fiber is
exp(ik·r)χ_a. Thus it defines a particular wavepacket in the direct sum of the
64 Bloch fibers, with amplitude sqrt(w_k). It is not the physical inner product
of different-k eigenstates, which are orthogonal. The existing same-k NC helper
still refuses such cross-k eigenstate overlaps; this calculation does not
weaken it. Changing the wavepacket convention can change the observable.

Let B_k be the native plane-wave space, Q_k its projection, and u_nk the native
cell-periodic eigenvectors. Compute A_an(k)=<Q_k χ_a|u_nk> on common Fourier
vectors. No discarded component is renormalized. For sector α of dimension d,

    p_αnk = Σ_(a in α) |A_an(k)|²/d,
    μ_α^ret = Σ_k w_k Σ_(n<=44) p_αnk δ_(ε_nk).

These positive measures produce a Stieltjes resolvent and its η-smoothed
spectral density. They do not identify an atomic W(k,q), impurity T, disorder
self-energy or finite-q susceptibility A. A finite-q symmetry label is not
assigned merely because a Γ reference was used as the probe.

Use the predeclared r=(E_Γ6+E_Γ8)/2, W=0.5 eV and η=0.025 eV. With
w(t)=[1-(t/W)²]² on |t|<=W and zero otherwise,

    m_α = ∫ w(t) A_α^η(r+t) dt,
    n_α = ∫ t w(t) A_α^η(r+t) dt,
    C_α = n_α/m_α,  Ω = C_6-C_8.

η is analytical resolution, not intrinsic linewidth. Ω is not the original
signed Γ gap, a sharp pole crossing, absorption edge or topological invariant.
The actual Γ gap and this wavepacket Ω differ substantially in the same native
dataset. A negative Ω here cannot imply an alloy x_c.

## Conditional completion bound without a real spectral gap

Under exact native-eigenpair/NC-metric assumptions, the unresolved probability
has two parts per k: geometry loss g_αk=1-Tr(χ†Q_kχ)/d and uncomputed native-band
weight s_αk=Tr(χ†Q_kχ)/d-Σ_n p_αnk. The former has no assigned energy; the latter
is above the last retained ordered native eigenvalue L_k. Here
L_k-r-W>=4.949481 eV for every k.

**PROVEN UNDER ASSUMPTIONS:** for d_k=L_k-r-W>0, positivity gives

    δm_α <= Σ_k w_k [g_αk+s_αk η (16W/15)/(π d_k²)] = τ_α,
    |δn_α| <= W δm_α,
    |C_α^complete-C_α^ret| <= (W+|C_α^ret|) τ_α/m_α^ret.

The bound uses ∫w=16W/15 and the maximum Lorentzian over the fixed window for
an energy above L_k. It needs no common support-free real-energy domain D.
It is an energy-separated completion bound, not a claim that the physical
Hamiltonian preserves the truncated native plane-wave space. Source residuals
and operator/model changes remain separate unknown errors.

The reported calculation includes a 1e-9 added-mass arithmetic allowance and
2e-9/m centroid allowance. These are stated numerical-input allowances, not an
interval audit of native complex dot products or the complete DFT solver. The
tail interval is conditional on the reported contractions, spectral ordering,
metric and evaluation assumptions; it is not a total material error bar.
The tiny observed Gram/independent-integral errors support numerical consistency
without certifying every assumption as material physics.

## Independent checks and limits

Positive-node 1024-point integration agrees with the 70-digit analytic
antiderivative to 9.215e-15 in mass and 1.347e-15 eV in moment across all retained
atoms. Actual-spinor sector-unitary, common-origin and reciprocal-relabel checks
pass; probability closure counts every missing component. An allowed positive
scalar tail completion lies within the derived bound. These completion tests
are mathematical counterchecks, not invented high-band observations.

Both retained window masses (0.012575 and 0.021068) are below the earlier
chemical-pilot p=0.05 gate. That physical acquisition gate is preserved, not
passed by this different diagnostic. Numerical tail control alone neither
qualifies a material sign nor removes the missing impurity packet.

| Error or uncertainty | Status |
|---|---|
| Omitted spectral completion, stated exact-input model | ≤1.428131 meV combined centroid bound |
| Native quadrature/metric consistency | Measured discrepancies; no universal floating-point proof |
| True native eigenpair and operator residual | Not certified |
| 64-point grid → bulk continuum | Unknown; no interpolation/thermodynamic-limit certificate |
| Probe convention → actual substitution vertex | Unknown; cannot be supplied by binary energies |
| Cd-induced self-consistent density/overlaps | Absent from inspected sources |
| Core, many-body, strain/zero-point/material errors | Unknown |

No novelty claim is made: the spectral positivity and tail inequalities are
standard mathematics. The new evidence is the actual native finite-q contraction
and its measured coverage/conditioning in this specified HgTe probe.
