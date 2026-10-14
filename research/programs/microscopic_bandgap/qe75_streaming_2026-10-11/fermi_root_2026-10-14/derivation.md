# Safeguarded cold Fermi root: scope, proof and physical meaning

Here mu is the chemical potential used for computational occupations. It is NOT
R07's renormalized Kane mass or its common-mode crossing reference energy.

## PROVEN: a finite complete domain for any ideal cold charge zero

f(x)=erf(x−1/sqrt2)/2+exp(−(x−1/sqrt2)^2)/sqrt(2pi)+1/2 is positive,
its maximum is f(sqrt2)<1.1, and f(x)>1 for x>=sqrt2. The latter follows from
Mills' inequality erfc(y)<exp(−y²)/(y sqrt(pi)) at y>=1/sqrt2.
f is increasing below sqrt2; f(−10)<1e−49. The unchanged QE exponent clamp adds
at most exp(−200)/sqrt(2pi), explicitly absorbed by the numerical oracle pad.

Sort all weighted levels epsilon_j, each retaining its positive k weight. Let
jL be the first index whose cumulative weight reaches Ne/1.1 and jU the first
reaching Ne. Then all ideal roots lie strictly between

    L=epsilon_jL−10sigma, U=epsilon_jU+sqrt2 sigma.

Below L, preceding levels have total weight<Ne/1.1 and at most1.1 occupancy;
all remaining levels contribute<=f(−10). In this binary-fraction48band/3k
fixture the finite charge margin is much larger than the tail. Above U, the
first jU levels each have occupancy>1 and cumulative weight>=Ne; the remaining
positive occupations cannot reduce the charge. Thus no root is excluded by
arbitrarily selecting a small interval around a Gaussian or old-solver guess.
This bound requires nonnegative cold f; it is not a general MP-smearing theorem.

## PROVEN UNDER EXPLICIT ORACLE ASSUMPTIONS: bounded root certification

1. Strict signed endpoint brackets and bisection preserve a charge zero by
   continuity even without global monotonicity. After n iterations, bracket
   width is at most(U−L)/2^n. The code uses at most256iterations and refuses
   midpoint stagnation or inadequate residual; a tiny chemical-potential STEP
   is never a charge certificate.
2. Certify an increasing neighborhood [a,b] around the computed zero with
   N'(mu)>=m>1e−6 electrons/Ry and N(a)<Ne<N(b). It contains exactly one root.
   A residual r then bounds its root error by(|r|+oracle_error)/m.
3. Exclude every other zero on [L,a] and [b,U] by a complete adaptive interval
   cover, not a sampled sign scan. Over each band interval the minimum of f is
   at an endpoint; its maximum is at an endpoint or sqrt2. The extrema of f'
   are at x=(3±sqrt5)/(2sqrt2), plus the endpoints. Weighted sums of these
   scalar enclosures bound N and N'. An interval either excludes Ne by N bounds,
   excludes a zero by monotonicity and endpoint signs, reveals a competing zero,
   or is subdivided. At most8192nodes; unresolved/competing roots refuse.

Numerical N enclosures are padded1e−11 electrons and derivative enclosures
1e−8 electrons/Ry, under stated function/roundoff assumptions. Native inputs
are finite, sorted, |epsilon|<=100Ry, sigma.001,48bands,3k, exact binary weights
(.125,.5,.375), one pool, Ne36, one chemical potential. The large-|x| source
w0gauss clamp is not literally the derivative of clamped wgauss; its tiny tail
difference is covered by the finite-domain pad. We do not claim universally
correctly rounded libm or a formally verified processor. Every actual completed
native state's charge/function value is checked independently at high precision.

## CALCULATED: necessary negative cases and all retained physical-model states

All18 retained complete control snapshots were inventoried/rehashed BEFORE the
new native attempt: old12outer states, later5states and failed-observer step2.
Unmodified source reproduces their old WG exactly. The biased step5 and
negative-response old6–12 are retained failures/diagnostics, not passed history.

Each admits one increasing root in the complete domain. The corrected step5
root is about0.669963365Ry, versus its nonneutral stationary minimum near
0.671485944Ry. Later old near-flat chemical potentials also move; small old charge
residual did not certify positive response or the same occupation distribution.
Changing the root solver intentionally changes some WG and SCF trajectories;
this is distinct from stream/control equivalence, tested only with BOTH new
members using the same solver.

Independent120-digit analytic occupation/charge and derivative checks plus an
independent bisection verify all18 spectra. Actual native helper and stock-QE
wgauss/w0gauss/w1gauss OBJECTS give exactly the same mu/certificates as source
checks. Maximum charge residual9.567457937e−11e, below the1e−8 acceptance.
The first shared-library link of the native helper failed because its existing
object was non-PIC; a non-MPI scalar EXECUTABLE then linked and genuinely passed
without recompiling/misrepresenting those native objects. No MPI init or SCF
was used in that check.

A synthetic48band spectrum with35levels at0Ry, one at.004Ry and12at.02Ry has
competing roots at fixed Ne36/sigma.001. The candidate refuses it (code6), rather
than assuming generic uniqueness. Nonfinite/out-of-range input refuses. An
independent homogeneous1Ry energy shift preserves occupations within the
predeclared scalar error allowance; it does not impose an empirical alignment.

## Physical interpretation and remaining limitations

Exact particle number and positive local charge response supply a defensible
cold-regularization branch for these uniquely certified spectra. They do not
turn cold smearing into physical finite-temperature Fermi-Dirac occupations,
prove absolute insulating mu observability, prove a true thermodynamic solution,
or select among several genuine branches. Such ambiguity is an explicit NO-GO.
Likewise a charge-root certificate proves neither whole-SCF contraction nor
converged HSE or physical alloy x_c. The native pair keeps independent energy,
wave/charge/local-potential/density and endpoint-resource gates. Old empirical
alloy laws are not inputs.
