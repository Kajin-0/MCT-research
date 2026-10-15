# Domain and accounting of the auxiliary native actions

The physical-G spinor norm uses the unchanged NC inner product. T maps up/down
at G to conjugate down/minus-up at -G, globally across ranks. The actual paired
cover and its independently stored reverse source are prepared before launch.
Only AFTER init_run, before electrons/punch, the private driver imports Phi,
et/wg, labels and all trials. Thus preliminary local rho/v/waves from native
initialization do not enter a solved Hamiltonian or the direct Fock equation.
The old full-Hamiltonian reconstruction byte-refusal remains applicable there.

Unchanged native exxinit/type2 with negrp1 copies evc into evc_exx, constructs
the same Gamma/q1 FFT source store and x_occupation=wg/wk. Actual identity q/k
maps,60³FFT, physical B/k/G,176/2spinor dimensions, source146occupation bound
and HSE fraction/screening/Fock cutoff are captured/checked. Source2 overwrites
evc with exactly TPhi before regenerating the same single store. Both orders
use IDENTICAL unchanged occupation cutoff/weights; retained discarded tails
are reported, not assigned auxiliary occupations.

Each native vexx call has m<=176, preserving max_ibands/ibands initialization.
No matcalc with nonexistent auxiliary occupations, xi resize or native ACE
arithmetic modification occurs. All returned actions are actual direct exchange.
Offline symmetrization uses actual V[D] and V[TD] calls, not inferred missing
actions. Native covariance is tested on the entire cover and independent probes.
The mathematical linearity statement is exact for the same actual truncated D
and TD; floating implementation equivalence is measured, not assumed bitwise.

For a grid convolution with real nonnegative Fourier eigenvalues c_G and inverse
FFT phi_j(r)=sum_G phi_j(G) exp(iG.r), its scaled exchange is a sum of congruences
by multiplication with source spinors. Therefore

    ||-V|| <= alpha max_G(c_G) max_r sum_j w_j||phi_j(r)||²/Omega.

Finite PW restriction is an orthogonal projection and cannot increase this norm.
Capture both native source orders' maximum grid density and convolution extrema
after direct calls. This norm bound and measured cover residual bound off-cover
source action and quadratic exchange trace error; they do not bound missing
material, k/q, finite-cell or self-consistency errors. If the actual Fourier
spectrum is negative/unknown or dimensions change, refuse this certificate.

The new TR-constrained ensemble is Dbar=(D+TD)/2. Its exchange energy is
.5Tr Dbar V[Dbar]; evaluate original source and time-reversed source weighted
contractions separately and compare with the small-matrix density contraction.
The fixed source occupations are unchanged in both calls; the ensemble generally
has different natural eigenvalues. No FD-of-new-H claim or occupation SCF is made.
Forces/stress and ionic movement are explicitly excluded. The constrained
functional/force derivative and source-exact compression proof are in the prior
antiunitary_closure/theory.md, with independent small-matrix derivative checks.
Native force implementation/variational stationarity are NOT qualified here.

Stock library/executable, native exchange/ACE bodies, old source/state/FAIL
evidence and DFT tracked dirty state remain pinned. The new norm control cannot
supersede the refused old BYTE control. Native owner and kernel limits certify
only this finite local owned-family acquisition, not host-wide MPI absence.
