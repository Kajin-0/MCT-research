# A conditional Gamma8 threshold coefficient, rather than a finite endpoint A

**PROVEN under the assumptions below:** for a normal insulating host with
an isolated quadratic Gamma8 valence maximum and a finite nonzero
single-impurity forward amplitude tau_8, the gap-side energy derivative
contains a positive inverse-square-root threshold contribution. A finite
static mass difference does not remove that contribution.

The assumptions are an energy-independent Hermitian impurity potential,
real E in the host gap, a short-range smooth scattering amplitude, no
impurity threshold resonance, and no linear term dominating the Gamma8
dispersion. The generic threshold phenomenon is established; see
[Wigner (1948)](https://journals.aps.org/pr/abstract/10.1103/PhysRev.73.1002).
No historical-priority claim is made for the following specialization.

## Matrix-valued infrared kernel

In an orthonormal Gamma8 quartet, let the small-q Hamiltonian be

    H_8(q) = E_v I_4 - q^2 alpha(n) + O(q^3), n=q/|q|,

where alpha(n) is positive Hermitian uniformly over the sphere. The
quadratic multiband starting description is the Luttinger model; the
calculation here retains its full directional matrix rather than assigning
one scalar hole mass. Use Bloch normalization Omega_c/(2 pi)^3, with
Omega_c the volume per cation. For E=E_v+delta, delta>0,

    -G_8'(E) ~ K_8/sqrt(delta),
    K_8 = Omega_c/(32 pi^2) integral_S2 dOmega alpha(n)^(-3/2).

This follows by diagonalizing alpha at each direction and evaluating

    integral_0^infinity q^2 dq / (delta+a q^2)^2
      = pi/(4 a^(3/2) sqrt(delta)).

The leading coefficient is independent of an ultraviolet cutoff. For a
complete cubic angular integral, K_8 commutes with the Gamma8 irreducible
representation, and Schur's lemma gives K_8=k_8 I_4. This does not require
spherical heavy/light curvatures. In the spherical special case,

    k_8 = Omega_c/(16 pi) [a_HH^(-3/2)+a_LH^(-3/2)].

Each rank-two heavy/light projector contributes half of the quartet's
angular average. The angular and radial normalization factors are checked
independently in the numerical tests.

## Exact impurity resummation preserves the leading divergence

The embedded derivative is -g'=P G^2 P*, not g^2. Exact scattering gives

    -T' = T P G^2 P* T.

In the low-q sector the forward Gamma8 scattering block of a
tetrahedrally symmetric substitution is tau_8 I_4. Smoothness lets the
incoming/outgoing block tend to this value as q tends to zero. Therefore

    -partial_E tau_8(E_v+delta)
       ~ tau_8(E_v)^2 k_8/sqrt(delta),

provided the threshold amplitude exists and is nonzero. Additional regular
spectral contributions cannot cancel a positive off-continuum norm's
leading positive coefficient. At a resonance, or if the leading amplitude
vanishes, a different asymptotic calculation is required.

In particular, tau_6 approximately equal to tau_8 makes the static mass
projection (tau_6-tau_8)/2 small, but does not make either forward amplitude
small. A positive symmetric average of raw endpoint branch derivatives
cannot then be equated to a finite A_slope obtained from finite endpoint
concentration slopes. A reduced constant-A law would require an explicitly
regularized/self-consistent spectral reduction with the intended gap
observable, rather than the unqualified isolated-host endpoint T' limit.
This does not prevent computing the finite impurity values first for the
mass-route inversion calculation.

## Calculated binary kernel and applicability check

**CALCULATED:** the reconstructed Schindler CdTe Hamiltonian gives

    k_8 = 0.5119895494464 eV^(-3/2).

The fcc geometry uses a=1, Omega_c=1/4 and momenta in a^-1. Restoring a
physical lattice multiplies alpha by a^2 and Omega_c by a^3, so the scalar
coefficient is unchanged. The kernel is derived from all remote Gamma
bands via the degenerate second-order coefficient

    B_ij = U_8* [H_ij/2 + H_i Q(E_v-Q H Q)^(-1)Q H_j] U_8,
    alpha(n) = -sum_ij n_i n_j B_ij.

This Gamma expansion computes the infrared asymptote, not a full atomic
finite-q alloy vertex. Direct small-q binary eigenvalues verify its
directional curvatures. Angular quadratures 24x48 and 32x64 differ in k_8
by 4.9e-14; the final nonscalar matrix defect is 2.4e-15. These are numerical
integration checks of this fixed approximate model, not material-accuracy
error bars. The source model's projected Gamma8 linear term is below
1e-12 eV a, so its quadratic threshold limit is internally applicable.

The source neglects d spin-orbit coupling and other possible microscopic
terms. Real zincblende Gamma8 bands can have linear bulk-inversion-
asymmetry splitting, discussed in the authors' account by
[Cardona, Christensen and Fasol (1987)](https://www2.fkf.mpg.de/andersen/docs/pub/abstract/and1987-10.html).
Such a term changes the lowest-q problem and must be checked in the
physical relativistic host before taking delta to zero. It does not
automatically establish a finite susceptibility. The inverted HgTe endpoint
also lacks the insulating off-continuum setting assumed here.

The [frozen kernel record](../../data/calculated/gamma8_quadratic_threshold_20261011.json)
contains source and code hashes, quadrature matrices and omitted terms.
No experimental alloy input, fitted DOS amplitude or measured bowing
coefficient enters the calculation. No physical total A or new inversion
composition is claimed.

**HYPOTHESIS:** none needed for the conditional coefficient; its applicability
to a physical HgCdTe endpoint requires the stated band-structure checks.
**NOVELTY CANDIDATE:** none established. The result makes the existing
threshold warning quantitative for the published Gamma8 binary model.
