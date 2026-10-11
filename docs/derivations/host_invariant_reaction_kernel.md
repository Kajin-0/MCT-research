# Host edge spinors, exact amputation and the finite-volume reaction kernel

**PROVEN under the assumptions below:** choosing actual eigenstates of the
pure host as a physical projector makes its projected Green function exact
without a Wannier gauge or a local trial-band normalization. The impurity's
projected spectrum then determines both the finite-volume projected T and
a kernel with propagation in that host subspace removed. This is standard
resolvent/Feshbach mathematics, not a novelty claim or a physical HgCdTe
coefficient calculation.

## Exact physical projector

Let H0 be the chosen finite Hermitian host operator and H=H0+V the static
self-consistent substitution operator in the same physical Hilbert space.
The ion geometry, energy alignment, basis cutoff and physical metric must
match. V includes every part of the operator difference; for HSE this
includes nonlocal exchange. After self-consistency the two operators are
held fixed, not regenerated at every spectral evaluation energy.

Choose orthonormal host eigenvectors as columns of Phi:

    H0 Phi = Phi h0, Phi* Phi=I,
    P=Phi Phi*, PH0Q=0, Q=I-P.

For target Gamma sectors, h0 is diagonal in the chosen host edge spinors.
This is a physical host-invariant projector. Assigning the same atomic or
Wannier labels to different projected states does not establish it.

The exact host and substitution projected resolvents are

    R0(z)=(z-h0)^(-1),
    R(z)=Phi* (z-H)^(-1) Phi
        = sum_n b_n* b_n/(z-epsilon_n),
    b_n=<psi_n^imp|Phi>.

Native NC plane-wave coefficients can provide these cross-overlaps after
matching reciprocal vectors and spin components. No export that omits
the Fock operator is needed: the full static operator is represented by
its spectrum. Finite supplied bands still need an omitted-window bound.

Rotating the host spinors unitarily inside a degenerate Gamma sector
conjugates R, T_P and K_P by that same unitary. The sector trace divided
by its dimension is invariant. If the isolated substitution and its fixed
environment preserve Td, Schur's lemma makes the Gamma6 and Gamma8 blocks
scalar. This gives a clean matrix treatment of the fourfold sector without
choosing one arbitrary eigenvector as its impurity shift. Broken-symmetry
periodic images or unconverged host spinors do not satisfy this premise.

## Two different exact matrices

Write A=z-h0. Dyson's identity gives the ambient finite-volume T projected
into this invariant subspace:

    T_P(z)=A R(z) A-A.

Separately define the P-irreducible reaction kernel

    K_P(z)=A-R(z)^(-1).

Feshbach elimination proves

    K_P = V_PP + V_PQ (z-QHQ)^(-1) V_QP.

Therefore

    R=(A-K_P)^(-1),
    T_P=K_P[1-R0 K_P]^(-1).

Unlike the general fixed-local-trial inverse difference, this K_P eliminates
only the impurity Q response: the host P is invariant and has no host
Feshbach coupling to subtract. K_P is energy dependent and must not be
relabelled as an energy-independent bare impurity potential. It includes
all Q states, including Kane-derived states at finite folded momenta;
it is not a remote-only Gamma partition.

For real E away from QHQ eigenvalues,

    -K_P'(E)=V_PQ(E-QHQ)^(-2)V_QP >=0.

This is the specified eliminated-Q norm. Continuum retarded projections
require a separate continuation and do not inherit this real Hermitian
statement without its assumptions.

## Why an exact finite-box on-shell T can be misleading

Consider one normalized host Bloch edge in N primitive cells and a rank-one
local impurity v. Its local host Green function is

    g_N(z)=1/[N(z-Ea)]+g_Q,N(z).

The projected full T and reaction kernel are

    T_P,N = (v/N)/[1-v g_N(z)],
    K_P,N = (v/N)/[1-v g_Q,N(z)].

At fixed finite N, z approaches Ea and **T_P,N tends to zero**, even
though K_P,N(Ea) is generally finite. Repeated propagation through the
one exact host pole causes this limit. Multiplication by N does not fix
the wrong order of limits. The local thermodynamic amplitude instead
requires N to grow before the real-energy limit, or an explicitly
P-irreducible finite-volume construction with a checked convergence limit.

Under localization of V, nonresonance and convergence of the Q lattice
resolvent to the specified retarded/principal-value thermodynamic host,

    lim_(N->infinity) N K_P,N(Ea)
       = the corresponding forward impurity amplitude.

For several Gamma edge states, all relevant host poles and their symmetry
channels must be handled together. Inverted HgTe can have continuum
weight at the common energy; the order of eta and cell-size limits remains
part of the physical definition. The rank-one example proves the finite-box
pitfall, not convergence of the real HgCdTe impurity.

## Spectral-window certificate and practical route

The [fixed-trial spectral bound](fixed_trial_resolvent.md) applies to R.
Here R0 is already exact in the chosen P, so only the impurity's omitted
spectral sum enters the window error. If ||delta R||<=e and
L=||R_B^(-1)|| with Le<1,

    ||delta K_P|| <= L^2 e/(1-Le),
    ||delta T_P|| <= ||A||^2 e.

The second bound's small value near a finite-box host pole cannot be
mistaken for an accurately predicted physical on-shell impurity amplitude;
that full finite-volume T itself has the artificial zero just derived.
Eigenpair residuals and SCF/grid errors are additional to these window bounds.

**CALCULATED verification:** the companion implementation reproduces the
ambient dense T and the independent exact Q-block inverse of a six-state
Hermitian Hamiltonian to numerical precision. A two-state local-impurity
control verifies that full on-shell finite-box T vanishes while the reaction
kernel stays finite. These are code/theorem checks, not HgCdTe predictions.

The physical computational route is now: converge the matched pure host
and substituted operator; identify the physical host Gamma spinors; project
the impurity spectrum onto those same spinors; certify the spectral window;
then examine reaction-kernel cell-size and continuation limits. The prepared
16-atom periodic fraction 1/8 alone is not a dilute calculation. Any limiting
forward shifts are full host-referenced shifts; subtract the binary chord
contrast before using them as residual mass-bowing inputs.

**HYPOTHESIS:** this route is computationally more effective for endpoint
mass values than constructing a complete common-Wannier substitution matrix
first. The actual self-consistent paired spectra are still required.
**NOVELTY CANDIDATE:** none established. No empirical alloy coefficient or
temperature input is used.
