# Fixed physical trials and a spectral-window error certificate

**PROVEN under the stated finite-basis assumptions:** the same fixed trial
functions can define host and impurity projected resolvents without equating
their independently projected Wannier orbitals. The omitted spectral norm
provides a quantitative error bound. This is a standard spectral/Feshbach
construction, not a novelty claim or a calculated impurity potential.

## A common physical projector

Let the columns of g be fixed physical trial functions in the same
orthonormal plane-wave space, with positive Gram S=g* g. Define

    Phi = g S^(-1/2), Phi* Phi=I.

For host and impurity Hermitian operators H_j in that same physical space,

    R_j(z) = Phi* (z-H_j)^(-1) Phi.

The spectral representation is

    R_j(z) = sum_n b_jn* b_jn / (z-epsilon_jn),
    b_jn = <psi_jn|Phi>.

It includes every part of the chosen static operator, including nonlocal
HSE exchange. No replacement by a difference of local scalar potentials
is made. Electrostatic alignment and isolation from periodic impurity
images are still needed before comparing physical host and impurity data.

The common-projector effective inverse difference is

    Delta_j(z) = R_0(z)^(-1)-R_j(z)^(-1).

This reproduces the projected resolvent through

    R_j = [R_0^(-1)-Delta_j]^(-1).

Equivalently, Delta_j is the difference of the two Feshbach effective
Hamiltonians in Phi. It is generally energy dependent because their
complements differ. It is not automatically Phi* (H_j-H_0) Phi, or the
ambient physical single-impurity T-matrix projected into Phi. If the host
Phi space is not invariant, those distinctions matter. In particular, an
energy-dependent effective vertex must not silently be used in the
energy-independent-potential positivity theorem.

The exact projected difference uses one fixed physical Gram S. Replacing
it separately by each resolved-band Gram creates different physical
orbitals and returns to the invalid same-label subtraction problem.

## Omitted spectral weight

Suppose only a spectral band set B_j is computed. Its resolved projector
in the fixed trial space and omitted norm are

    W_j = sum_(n in B_j) b_jn* b_jn,
    N_j = I-W_j >=0.

Let d_j(z)>0 be a rigorous lower bound on the distance from z to every
omitted eigenvalue. Then, for the truncated spectral sum R_j^B,

    ||R_j-R_j^B|| <= ||N_j||/d_j,
    ||partial_z^r (R_j-R_j^B)|| <= r! ||N_j||/d_j^(r+1).

To prove this, factor the omitted sum as B_Q* f(H_Q) B_Q and use
||B_Q||^2=||N_j|| and ||f(H_Q)|| <= r!/d_j^(r+1). The bound applies
off the omitted spectrum; at complex z it also permits d_j >= |Im z|.
For a contiguous interior band window, the excluded low and high band
boundaries supply a sharper spectral distance when their ordering is
established. A gap in computed band indices must not be ignored.

Write e_j=||N_j||/d_j and K_j=||(R_j^B)^(-1)||. If K_j e_j<1, the
resolvent inverse perturbation identity gives

    ||R_j^(-1)-(R_j^B)^(-1)||
       <= K_j^2 e_j/(1-K_j e_j).

Adding the host and impurity bounds certifies their effective inverse
difference. If K_j e_j>=1, this certificate is inconclusive; it does not
prove the omitted correction is large. More bands, better-suited fixed
trials, or direct operator evaluation can then be tested. A small gap
error by itself is not a certificate for this inverse matrix.

## Native numerical evidence

**CALCULATED:** the companion QE 7.5 accurate-empty CdTe control allows
the fixed plane-wave trial coefficients to be reconstructed independently.
They reproduce native Gamma and X amplitudes to about 7e-13. The
standalone interface interprets the numeric radial input 1.0 in atomic
units; the earlier inverse-Angstrom metadata description was inaccurate.
The [DFT audit](/home/User/opencode_workspace/DFT/docs/r07_projected_host_frame.md)
records the source convention and native checks.

At Gamma the least-captured fixed physical direction has fractions
0.143972 in bands 19-44 and 0.570120 in all 44 supplied bands. At X those
fractions are 0.0162204 and 0.469856. These are trial-space spectral
projector eigenvalues, not band-edge orbital weights, gap errors,
linewidths, or physical disorder amplitudes.

This explicitly separates full rank from physical trial capture. The
fixed-trial resolvent construction provides an alternative extraction
route if its spectral-window bound can be made adequate; it has not yet
produced a converged physical HgCdTe impurity coefficient. No experimental
alloy-gap inputs are used. Temperature remains deferred.

**HYPOTHESIS:** none needed for the bounds. Whether this route is efficient
for the physical impurity requires the actual two operators and convergence
checks. **NOVELTY CANDIDATE:** none established.
