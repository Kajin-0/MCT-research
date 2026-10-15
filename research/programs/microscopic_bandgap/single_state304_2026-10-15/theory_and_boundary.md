# One-state Galerkin result and its precise boundary

PROVEN UNDER ASSUMPTIONS: in the finite native plane-wave Hilbert space let
V*V=I, A=V*HV and R=HV−VA. For a supported density D=VdV*,

    ||[H,D]||F² = ||[A,d]||F² + 2||Rd||F².

A Galerkin Fermi matrix d=fσ(A−μ) removes only the first term. Its whole-space
stationarity still requires Rfσ(A−μ)=0. A small in-space eigensolver residual,
charge root, symmetry or entropy does not imply that condition. The new native
304 result supplies R directly, so this is a measurable obstruction, not an
inference from disagreement between two separate operators.

For finite Hermitian H and any μ, [H,fσ(H−μ)]=0. Thus

    ||D−fσ(H−μ)||p >= ||[H,D]||p /(2||H||op), p=2,F.

The native conservative operator bound is very loose; these are conditional
finite-model bounds, not outward-rounded interval arithmetic or material error
bars. Full-space Fermi charge also depends on the unobserved complement.
A perfect invariant Ritz block R=0 cannot exclude an occupied orthogonal state:
append an uncoupled level below μ. All observed A/actions remain unchanged.
No amount of extra decimal precision in A excludes that counterexample.

Let C=QHQ in the orthogonal complement, dimension m. If independently C>=L,
then its block-diagonal fixed-μ Fermi charge obeys

    Tr fσ(C−μ) <= m/[1+exp((L−μ)/σ)].

This is a conditional support/order bound, not a common spectral gap and not a
fact established by positive auxiliary Ritz eigenvalues. It also does not
settle the *coupled* whole-H charge or adjusted full-space μ. To make this one
complement contribution <=1e-8e at the measured μ requires L>=.694438129Ry;
no such certificate is presently available.

For a fixed μ, block diagonal H0=A⊕C and E=H−H0, scalar divided differences and
the Hilbert–Schmidt identity give

    ||fσ(H−μ)−fσ(H0−μ)||F <= ||E||F/(4σ)
                                    = sqrt(2)||R||F/(4σ).

Proof: expand in the two eigenbases; each matrix element of f(H)−f(H0) equals
the scalar divided difference times the corresponding H−H0 element. Scalar FD
slope is bounded by 1/(4σ); square and sum. No operator-Lipschitz assertion in
spectral norm is made. The actual bound is ~64266 and therefore uninformative.

PROVEN UNDER ASSUMPTIONS: at fixed A, fixed charge and temperature σ the
Galerkin Fermi matrix minimizes Tr(Ad)−σS(d) over 0<=d<=I. Its lower band/free
energy is NOT the nonlinear HSE energy difference: Hartree, screened Fock and
semilocal XC must be recomputed consistently after a density change. Likewise,
assigning the six high-G coverage directions solved-band occupations is invalid.

CALCULATED: actual FD304 charge144e and entropy4log2, with a nearly half-filled
quartet, remain cubic/Theta invariant under the original1e-8 gate. Whole-space
commutator .50357023RyF and Fermi residual .02378468Ry explicitly fail native
stationarity. The 304-space is useful new input, not a qualified SCF bridge.
No native H[D1], Cd or nonlinear state update is released from this acquisition.

Next independent physical input for a stationary source is a symmetry-preserving
full-H occupied eigenstate solve with certified occupied/complement error, followed
by same-state H[D1]/energy/charge/entropy. More auxiliary high-energy Ritz rows do
not by themselves supply it. Continue a distinct read-only finite-resolution
resolvent test using the now complete one-state actions; it can be bounded
without inventing a spectral gap or claiming an FD/HSE fixed point.
