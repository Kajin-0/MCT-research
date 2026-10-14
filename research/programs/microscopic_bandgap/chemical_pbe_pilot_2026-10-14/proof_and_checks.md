# What the measured response and its bounds mean

**CALCULATED:** native self-consistent PBE8 host and substituted spinor spectra.
**PROVEN UNDER ASSUMPTIONS:** positive-measure completion and nearby-projector
uncertainty bounds. No claim of novel mathematics or material validation.

For phi(t)=exp[-t²/(2W²)], 0<=phi<=1 and sup|t phi|=W/sqrt(e)=B.
Let retained Gaussian mass M and moment N, c=N/M. A normalized rank-d host
projector defines positive spectral weights Tr(P Pi_n)/d. Omitted probability r
gives tail mass 0<=a<=r and moment |b|<=rB, irrespective of unbounded energies.
Thus |(N+b)/(M+a)-c|<=r(B+|c|)/M. This bounds the **specified smoothed functional**;
it cannot bound an unsmoothed full first moment (a missing probability r at
arbitrarily large energy supplies an arbitrarily large moment).

For same-rank Q with ||Q-P||<=epsilon, rank(P-Q)<=2d and
||P-Q||_1/d<=2epsilon. Spectral functional calculus gives signed mass/moment
perturbations |deltaM|<=2epsilon and |deltaN|<=2epsilon B. Let rho_round bound
the arithmetic/normalization functional errors in the same normalized form.
For any positive completion AND projector/arithmetic perturbation together,

    M_final >= M-2epsilon-rho_round = m > 0,
    |c_final-c| <= (r+2epsilon+rho_round)(B+|c|)/m.

Every budget term uses this SAME denominator. An independent prepublication
audit found that adding sequential bounds with separate denominators omitted
a cross term. Preliminary numerical_result is retained as preaudit_numerical_result;
the final interval uses the joint denominator. Native spectra/weights and all
historical gates are unchanged. This is an analytical bound correction, not a
tolerance adjustment or a new QE run.

Nearby Td projector epsilon comes from the already-derived finite-group twirl
theorem and its conditional IEEE model, not from empirical HgCdTe gaps. Actual
host translation probabilities and complex characters determine the physical
near-edge Gamma6/Gamma8 labels. The theory does not promote the arbitrary
substituted individual eigenstates to primitive Gamma irreps. The HSE reference
is used only to locate candidates; discarded high-G reference norm is explicitly
recorded. Final PBE projectors are full native40Ry host spans.

Independent checks use retained complex overlaps, direct scalar integration of
actual spectra, unitary/relabel invariance, charge reconstruction by expit, and
positive-tail/signed-perturbation extremizers on small matrices. Native PBE
eigenpair accuracy beyond reported SCF/diagonalization diagnostics is NOT
rigorously bounded. The conditional interval is not a material error bar.

Further obstructions: self-consistent periodic x=.25 charge/chemistry is not
an isolated impurity; Gamma-only supercell sampling is not Brillouin-zone
convergence; PBE host ordering differs substantially from accepted HSE. No
operator-norm cutoff, finite-size, functional or relaxation error is available.
Numerical centroid sign therefore cannot locate physical x_c or certify a bulk
topological phase. The next material acquisition would need matched HSE-quality
host/Cd data or independently controlled functional/cell/grid errors, not an
empirical gap coefficient. The private48band root still cannot operate on the
original352band/288electron target, and its memory failure remains unchanged.

Established primary methods: [QE PW input/FD+SOC](https://www.quantum-espresso.org/Doc/INPUT_PW.html),
[spinor bands/irrep analysis](https://www.quantum-espresso.org/Doc/INPUT_BANDS.html),
[SOC angular-momentum-resolved orbital projections](https://www.quantum-espresso.org/Doc/INPUT_PROJWFC.html).
This package uses saved complex NC plane-wave overlaps and independent group
operations instead of a new projwfc job; it is not a new electronic-structure
method. Primary documentation checked2026-10-14; no novelty claim.
