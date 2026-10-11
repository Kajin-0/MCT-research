# Continuum bounds: explicit constants and uncertainty

All S1–S8 results are **PROVEN UNDER ASSUMPTIONS** below. They concern the
observables in this package, not a replacement certificate for the original
sharp mass root. Uniform hypotheses must hold over the specified compositions.
Energies, eta and window widths are in eV; x is dimensionless.

## S1. Bounded functionals and measure errors

For bounded real f define F_f^eta(mu)=integral f(E) A^eta(E)dE.
Fubini gives F_f^eta(mu)=integral (P_eta*f)(t)dmu(t). Positivity and unit
mass imply ||P_eta*f||_infinity<=||f||_infinity. Hence

```text
|F_f^eta(mu)-F_f^eta(mu_tilde)| <= ||f||_infinity tau,
tau=||mu-mu_tilde||_TV.
```

TV means total variation mass, not half the total variation. Tau<=2 for two
probability measures. The bound is independent of eta, any density regularity,
the energy support and an energy moment. It is useful only if tau is certified;
two nearby but distinct atoms have TV=2. If a coupling of mu and mu_tilde has
finite mean displacement W1, bounded Lipschitz f instead gives error <=Lip(f)W1:
Poisson convolution preserves Lip(f), and integrate its difference against the
coupling. No implication from causality alone to small tau or W1 is asserted.

## S2. Certified operator, projector, law and kernel errors

On matched spaces suppose ||H_omega-H_tilde_omega||<=delta uniformly, and
||rho-rho_tilde||_1<=q. A configuration-law difference has TV mass <=t.
Resolvent norm <=1/eta and the resolvent identity yield, for k=0,1,...,

```text
|partial_E^k(g-g_tilde)|
 <= (k+1)! delta/eta^(k+2) + k! (q+t)/eta^(k+1) = b_k,
||partial_E^k(A-A_tilde)||_infinity <= b_k/pi.
```

Proof: partial_E^k R=(-1)^k k! R^(k+1); telescope the difference of the
(k+1) powers and apply ||R-R_tilde||<=delta/eta^2. The projector and law
terms follow by trace duality and integration. This comparison does not need
H bounded, only a common self-adjoint domain and a bounded difference, or the
corresponding valid resolvent estimate. Ensemble laws and projector choices
must be matched before attributing delta to the material. No volume-uniform
delta or composition-law TV bound is inferred from a finite-cell control.

An alternative causal Dyson input is a uniform denominator error epsilon_D
at E+i eta. If both exact and candidate kernels have -Im K>=0, then
|g-g_tilde|<=epsilon_D/eta^2 by subtracting their inverses. This is a
complex-energy value estimate, not the failed real-energy common/mass
contraction. An approximation's causality alone does not certify unit spectral
mass; a local linear kernel must not supply fictitious global normalization.

Operator errors worsen as eta decreases. This is the price of a continuum
certificate, not a concealed gap-domain hypothesis or proof of eta->0 control.

## S3. Resolution changes and the Cauchy-tail obstruction

Let ||f||_infinity<=M and Lip(f)<=L. Splitting the Poisson integral at |u|=a,
for any a>0,

```text
||P_eta*f-f||_infinity
 <= (L eta/pi) log[1+(a/eta)^2] + (4M/pi) atan(eta/a).
```

Integrate L|u| on the central interval and bound the remaining difference by
2M. For Holder exponent 0<beta<1 and seminorm H_beta, the simpler bound is
H_beta eta^beta/cos(pi beta/2), from the beta integral of |u|^beta P_eta(u).
Neither needs regularity of mu. These bounds concern smooth test functions,
not pointwise recovery of a spectral density or an argmax.

Also ||P_eta-P_eta_tilde||_1<=|log(eta/eta_tilde)|: differentiate P in eta,
use |partial_eta P|<=P/eta, and integrate along the positive eta interval.
Multiply by M to bound the functional resolution uncertainty. This is useful
at fixed resolutions, not an intrinsic-linewidth estimate.

A universal O(eta) estimate from Lip(f) alone is false. For
f(u)=min(|u|,1), f(0)=0 and mu=delta_0,
F_f^eta includes (eta/pi)log(1+eta^(-2)); its ratio to eta diverges.
Even delta_0 produces a Cauchy A^eta with divergent absolute first moment.
Thus an unwindowed broadened centroid is undefined, although mu itself has
an exact first moment. Principal-value cancellation is not a physical centroid.

## S4. Omitted spectral tails and finite observational windows

Let f be supported in I, J contain I with distance b>0 between I and R\J,
and mu(R\J)<=sigma. Using only positivity,

```text
||A_tail^eta||_(infinity,I) <= sigma eta/[pi(b^2+eta^2)],
|F_f^eta(mu_tail)| <= ||f||_1 sigma eta/[pi(b^2+eta^2)].
```

This is support separation of the *omitted far tail from the observation
window*, not support-free D near the retained energy. Spectral support may
fill I and J completely. If no b is known, use the weaker universal bound
sigma/(pi eta). Missing nearby spectral weight then remains consequential.
Derivative tails satisfy ||partial_E A_tail||_(infinity,I)
<=2sigma eta/(pi b^3), from the explicit Poisson derivative.

For measured intensity only inside a covered window I, take f supported there.
Unknown backgrounds/response errors contribute their independently bounded
functional residual. Weight outside I cannot be inferred from a plotted null;
normalization of a fully specified canonical projection, or a separate tail
certificate, supplies sigma. A numerical band prefix must not be renormalized
to one, hiding its omitted weight.

## S5. A finite-window centroid certificate

Let 0<=chi<=1 be a compact window in |E-r|<=W; use the same chi and r in both
sectors. Define m=F_chi^eta and n=F_(E-r)chi^eta, C=r+n/m. Require a certified
m,m_tilde>=p>0. If |m-m_tilde|<=epsilon_m and |n-n_tilde|<=epsilon_n,

```text
|C-C_tilde| <= (epsilon_n+W epsilon_m)/p.
```

Proof: n/m-n_tilde/m_tilde=[n-n_tilde-(n_tilde/m_tilde)(m-m_tilde)]/m,
and |n_tilde/m_tilde|<=W by positive window weight. A candidate window mass
m_tilde with m_tilde-epsilon_m>=p certifies the true floor. Positivity of the
candidate spectrum is necessary for the displayed numerator bound; otherwise
certify |n_tilde/m_tilde| separately. Both normalized centroids lie in the
window, so the bound can be capped by 2W.

For Omega_C=C6-C8, add the two sector bounds. S1 gives
epsilon_m<=tau and epsilon_n<=W tau, so each error <=2W tau/p.
For a spectral error epsilon_A on I, use
epsilon_m<=||chi||_1 epsilon_A and
epsilon_n<=||(E-r)chi||_1 epsilon_A. Tail, resolution, quadrature, response,
projector and physical-model errors enter these budgets once each. Units:
m,p are dimensionless, n and epsilon_n are eV, epsilon_A is eV^(-1).
An arbitrary unknown p destroys the certificate; finite eta only makes m>0,
not bounded away from zero uniformly across models.

## S6. Isolated peak location: height and derivative certificates

Let a=A_alpha^eta on a compact search interval I. Its selected global maximum
p0 lies in the interior of a smaller interval I0. Assume

```text
a(p0)-sup_(I\I0) a >= Delta>0,
-a''(E)>=kappa>0 for E in I0,
||a-a_tilde||_(infinity,I)<=epsilon_0, 2epsilon_0<Delta.
```

Any maximizer p_tilde of a_tilde in I lies in I0: comparison with p0 and
the isolation margin excludes its complement. Strong concavity and a'(p0)=0
give kappa|p_tilde-p0|^2/2<=a(p0)-a(p_tilde)<=2epsilon_0. Thus

```text
|p_tilde-p0| <= 2 sqrt(epsilon_0/kappa).
```

If a_tilde is differentiable and p_tilde is interior, with derivative error
<=epsilon_1, then a_tilde'(p_tilde)=0 and strong concavity instead gives
|p_tilde-p0|<=epsilon_1/kappa. The height bound requires no candidate derivative.
It does not guarantee a unique candidate maximum; all candidates satisfy it.
The stronger bound uses an independently qualified derivative residual, not
height accuracy alone. Add the sector bounds for Omega_P=p6-p8.
Delta,epsilon_0 are eV^(-1), kappa eV^(-3), epsilon_1 eV^(-2).
Finite eta ensures smoothness but supplies neither Delta nor kappa.

## S7. Composition crossing bounds, for the *declared* observable

Let Omega mean Omega_C or a uniquely isolated/tracked Omega_P on [a,b].
Require continuity. Weakly continuous probability measures and continuous
physical/window/reference transport imply continuity of bounded window
functionals at fixed eta, if m>=p>0. For peaks, uniform continuity of spectra
and unique isolated maxima imply continuity by compactness of the maximizers.
These are explicit composition hypotheses, not consequences of energy causality.

If |Omega-Omega_tilde|<=epsilon uniformly, opposite candidate signs at a,b
with margins >epsilon certify at least one zero by the intermediate-value
theorem. Independently assayed composition intervals [a-,a+],[b-,b+] widen
this existence bracket to [a-,b+] for a+<b-. Identical strain/carrier/state
families are essential; two specimens do not establish a continuous path.

For uniqueness and a root-location bound additionally require, for y>x,

```text
Omega(y)-Omega(x)>=omega(y-x),
omega(h)>0, increasing for h>0, omega(0)=0.
```

Then Omega is strictly increasing. For a candidate zero x_tilde and a true
zero x_star, omega(|x_tilde-x_star|)<=epsilon; use the generalized inverse
of omega. A linear modulus mh gives |x_tilde-x_star|<=epsilon/m. With a
root-relative modulus c h^p one obtains (epsilon/c)^(1/p) instead.
If the computed candidate composition is itself uncertain by q_x, the safe
location bound is q_x+omega^(-1)(epsilon), when the uniform certificate holds
at its actual composition. Sign brackets alone require no lower modulus.

This is an operational spectral-ordering root, not physical x_c. Finite point
data do not prove a uniform epsilon or positive lower modulus. Eta does not
bound concentration derivatives, and no material m is inserted here.

## S8. Conditional input precision, without a material precision claim

For equal sector budgets epsilon_m,epsilon_n and mass floor p, an operational
root tolerance Delta_x under a qualified linear modulus m requires

```text
2(epsilon_n+W epsilon_m)/p <= m Delta_x.
```

For equal measure TV budgets tau, this becomes 4W tau/p<=m Delta_x. Equal
peak height errors instead require 4sqrt(epsilon_0/kappa)<=m Delta_x;
equal derivative errors require 2epsilon_1/kappa<=m Delta_x. This explains
why windowed functionals are the lower-input candidate when peak isolation
is unqualified. None of p, m, kappa, Delta or a physical residual is currently
known for HgCdTe. Additional micro-eV host precision cannot supply them.
