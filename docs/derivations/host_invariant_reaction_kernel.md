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

## Native physical-overlap control

**CALCULATED:** the companion DFT implementation now matches NC plane-wave
coefficients by their physical reciprocal vectors, allowing reordered
Miller lists and integer Bloch relabeling. It rejects differing cells,
reciprocal axes, physical plane-wave spaces and nonorthonormal NC metrics.
Synthetic dense-state checks verify unitary covariance of the projected
reaction kernel, including invariance of a degenerate sector trace.

The native irreducible and expanded-grid Gamma files of the same SG15
CdTe HSE host give K_P norm 2.5819e-15 eV, full T_P norm 2.5874e-15 eV,
and projected resolvent error 4.2102e-15 eV^-1. The six physical host
Gamma6/Gamma8 spinors have unresolved supplied-window weight 3.6086e-15.
This is a same-operator negative control, not a physical impurity shift
or an upgrade of binary/grid accuracy. The [native control protocol](/home/User/opencode_workspace/DFT/docs/r07_invariant_host_control.md)
records the exact files, potential hashes and remaining gates.

## Why localized substitution can have a small omitted host-projector weight

For one of the fixed physical host eigenstates Phi_a with energy E_a,
the exact static-operator identity H=H0+V gives, for an impurity eigenstate,

    (epsilon_n-E_a) <psi_n|Phi_a> = <psi_n|V|Phi_a>.

Suppose the omitted eigenvalues are all at least Lambda, with
Lambda>max_a E_a. For the unresolved host-projector weight N_B,

    ||N_B|| <= trace(N_B)
             <= sum_a ||V Phi_a||^2/(Lambda-E_a)^2.

**PROVEN:** multiply each exact eigenstate identity by its conjugate,
sum over the omitted states, use the positive denominator bound, and
bound that omitted norm by the complete norm of V Phi_a. This is a
conditional upper bound; no unknown matrix element is assigned a number.

If Phi_a is an extended normalized host Bloch state in Ncell primitive
cells and the static substitution V remains localized with a cell-size
independent square-summable scattering cloud, ||V Phi_a||^2=O(1/Ncell).
Consequently the unresolved fixed-edge-projector norm is O(1/Ncell) at
a fixed positive spectral separation. This assumption must be checked
for the actual self-consistent screened-exchange substitution; it is not
established by the current binary calculations.

This explains a potential computational advantage over fixed local atomic
trials: in the absence of substitution, any supplied prefix containing
the selected host eigenstates captures their norm exactly. A localized
substitution introduces an unresolved norm proportional to its scattering
cloud rather than the unrelated high-energy tail of an atomic trial.
The measurable matrix I-B*B still supplies the operative window certificate.
Neither the 1/Ncell scaling nor multiplying K_P by Ncell establishes a
few-meV dilute-limit error by itself. A continuum or near-resonant response
can amplify the inverse, and electrostatic alignment, eigenpair errors,+self-consistent periodic-image effects and volume convergence remain
separate checks.
