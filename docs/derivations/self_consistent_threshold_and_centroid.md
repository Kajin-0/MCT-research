# Threshold self-consistency and the exact Gamma spectral centroid

**PROVEN:** conditional identities and asymptotics in the stated scalar CPA
benchmark and linear-substitution lattice Hamiltonian. **CALCULATED:** full
numerical CPA solutions and explicit random-alloy spectra. **HYPOTHESIS:**
which threshold channels and environment response apply to physical HgCdTe.
No measured alloy-gap coefficients are used.

## A divergent isolated-host T prime does not fix the composition power

The earlier [threshold audit](impurity_reference_and_threshold.md) gives an
independent-host pole correction proportional to x^(3/2). Its derivation is
correct for that approximation. It is not a prediction for a self-consistent
medium. The following calculation is a counterexample to that extrapolation.

Use a scalar binary onsite model with potential 0 or v, probabilities 1-x
and x, and a regular three-dimensional quadratic lower host threshold at 0:

\[
g(w)=g_0+c\sqrt{-w}+O(w),\qquad c>0.
\]

Here w=E-Sigma is the energy measured in the coherent medium, rather than
the unshifted host energy E. The retarded square root has negative imaginary
part for w in the upper half plane. Assume a nonresonant weak attractive
impurity, v<0 and D_0=1-vg_0>0. Define

\[
t_0=\frac{v}{D_0},\quad a=c t_0^2,\quad
b=-\frac{g_0 t_0^2}{D_0}.
\]

Dimensions are [t_0]=[b]=energy and [a]=sqrt(energy).
The exact scalar binary CPA equation at fixed w is

\[
g(w)\Sigma^2+[1-vg(w)]\Sigma-xv=0.
\]

Choose its branch continuous from Sigma=0 at x=0. Expansion gives

\[
\Sigma(w,x)=xt_0+xa\sqrt{-w}+x^2b
+O(xw,x^2\sqrt{-w},x^3).
\]

Self-consistency places the threshold layer at w=O(x^2), rather than the
O(x) host detuning of the independent-host pole. Set

\[
w=x^2u,\qquad E=xt_0+x^2\zeta.
\]

Then the leading inner equation is

\[
\boxed{\zeta=u+a\sqrt{-u}+b.}
\]

The real gap-side fold obeys dE/dw=0. Therefore

\[
u_{\rm edge}=-\frac{a^2}{4},\qquad
\boxed{E_{\rm CPA\ edge}=xt_0+
 \left(b+\frac{a^2}{4}\right)x^2+O(x^3).}
\]

This is an edge of the CPA density of states. It is not an exact random-alloy
spectral-support edge or a mobility edge; localized tails are not included.

For the normalized DOS used in the executable benchmark,
rho(epsilon)=3 sqrt(epsilon)/(2 Lambda^(3/2)), 0<epsilon<Lambda,

\[
g_0=-3/\Lambda,\qquad c=3\pi/(2\Lambda^{3/2}).
\]

The independent-host closure instead gives
E_ATA=xt_0+a sqrt(-t_0) x^(3/2)+O(x^2). Thus a singular bare T prime does
not by itself establish a fractional physical composition law, nor prove
that self-consistent endpoint second concentration derivatives must diverge.

### General conditional threshold power

The same balance applies if the reduced scalar host function has
g(-delta)=g0+c delta^nu+o(delta^nu), with 0<nu<1 and c>0, and its derivative
has the differentiated asymptotic form. Let Sigma0(x) be the exact fixed-g0
CPA branch, so all regular powers in concentration remain in the baseline.
Then for a=c t0^2,

\[
E(-\delta,x)=\Sigma_0(x)-\delta+ax\delta^\nu+
 o(x\delta^\nu).
\]

The fold condition supplies

\[
\delta_*=(a\nu x)^{1/(1-\nu)}[1+o(1)],\qquad
E_{\rm CPA\ edge}-\Sigma_0(x)
=\frac{1-\nu}{\nu}(a\nu x)^{1/(1-\nu)}[1+o(1)].
\]

Thus the conditional self-consistent threshold exponent is 1/(1-nu),
compared with the independent-host exponent 1+nu. The square-root case
nu=1/2 gives the displayed x^2 result. For a scalar channel whose low-energy
weighted DOS behaves as epsilon^nu, this is a regularity test for endpoint
derivatives. A noninteger threshold power between two derivative orders can
allow the lower endpoint hierarchy and obstruct the higher one. The
statement requires the scalar nonresonant CPA closure and differentiated
host asymptotics; it is not a theorem about a full multiband alloy or
connected clusters. The logarithmic case nu=0 and a threshold resonance
require different balances.

## DOS edge, Gamma spectral maximum and real-denominator zero differ

For p=zeta-b-a^2/4>0, the causal solution of the inner equation is

\[
u=p-\frac{a^2}{4}+ia\sqrt p.
\]

At the host Gamma threshold the averaged Green function is 1/w. Hence

\[
\boxed{-\operatorname{Im}G_\Gamma(E)=
 \frac{a}{x^2}\frac{\sqrt p}{(p+a^2/4)^2}.}
\]

The spectral density includes an additional factor 1/pi. Its maximum occurs
at p=a^2/12:

\[
\boxed{E_{\Gamma\ peak}=xt_0+
 \left(b+\frac{a^2}{3}\right)x^2+O(x^3).}
\]

The leading peak-minus-CPA-edge difference is a^2 x^2/12. The zero of
Re(w), often used as a real quasiparticle equation, instead gives
xt_0+(b+a^2/2)x^2. These are distinct observables at the same concentration
order; neither may silently substitute for the other in a gap derivation.

More generally, write a scalar branch inverse Green function as F(E)+i Gamma(E).
Direct differentiation of its spectral density gives the exact maximum condition

\[
\Gamma'(F^2-\Gamma^2)-2\Gamma F F'=0.
\]

A real-denominator root F=0 is a spectral extremum only if Gamma'=0 or
Gamma=0. An exact real mass-zero theorem for sharp poles must therefore be
distinguished from a peak-crossing criterion when the two branches have
energy-dependent continuum damping. This issue is additional to any error
in estimating their static self-energies.

For the artificial benchmark v=-0.1 eV, Lambda=1 eV, the exact constants are
t_0=-0.1428571 eV, a=0.0961712 sqrt(eV), b=0.0874636 eV.
The predicted x^2 coefficients are 0.0897758 eV (CPA edge) and 0.0905465 eV
(Gamma peak). Full numerical CPA solutions at x=10^-5 give coefficients
within 2e-6 eV of these limits. These numbers are not HgCdTe parameters.

## Self-consistency does not supply a small cluster parameter at this edge

For a translational scalar host, the exact resolvent identity is

\[
\sum_{R\ne0}G_{0R}G_{R0}=-g'(w)-g(w)^2.
\]

A conventional leading dilute applicability indicator for off-site cluster
scattering is

\[
\mathcal R=x\left|t(w)^2[-g'(w)-g(w)^2]\right|,
\qquad t(w)=v/[1-vg(w)].
\]

This is a heuristic indicator, not a rigorous CPA error bound. Near the
threshold, g'=-c/[2 sqrt(-w)]+O(1), so in the same inner layer

\[
\mathcal R=\frac{a}{2\sqrt{|u|}}+O(x).
\]

Consequently,

\[
\boxed{\mathcal R_{\rm CPA\ edge}\longrightarrow1,
\qquad \mathcal R_{\Gamma\ peak}\longrightarrow\frac{\sqrt3}{2}.}
\]

Reducing concentration does not make this indicator small at either
observable. Therefore the x^2 CPA regularization is not a controlled theorem
about the exact random alloy. It resolves the independent-host inference
within CPA while retaining a separate need for cluster/real-space validation.
It does not invalidate exact finite-neighbor configurational identities.

The threshold applicability issue and the same off-site indicator are
established in [Skrypnyk, Phys. Rev. B 70, 212201 (2004)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.70.212201),
particularly the author-uploaded paper's Eqs. (5) and (8). Its discussion also
explicitly records unity at the CPA edge as an earlier established result.
That paper discusses why CPA misses the immediate edge region and gives a
heuristic criterion. This project does not claim priority for this framework.
**NOVELTY CANDIDATE:** the explicit observable-dependent coefficients and
their use in the HgCdTe endpoint-closure audit are a synthesis to investigate;
historical novelty has not been established.

## An exact sum rule for the reconstructed alloy

The explicit lattice diagnostic has

\[
H(\eta)=H_H+\sum_R\eta_R W_R,
\qquad \sum_R W_R=H_C-H_H,
\]

where the substitution star W_R is a lattice translation of a fixed operator.
Let U_Gamma uniformly embed a primitive-cell spinor into a periodic box of
N cells, normalized by 1/sqrt(N). The zero-momentum projection of each star
is the same. For every configuration with x=N_Cd/N,

\[
\boxed{U_\Gamma^\dagger H(\eta)U_\Gamma
 =(1-x)H_H(0)+xH_C(0)=H_{\rm VCA}(0).}
\]

For a unit VCA Gamma eigenvector a, the spectral measure
A_a(E)=<U_Gamma a|delta(E-H)|U_Gamma a> satisfies

\[
\int A_a(E)dE=1,\qquad
\int E A_a(E)dE=E_a^{\rm VCA}.
\]

No configurational average is needed. The first identity is spectral
normalization; the second is the exact first moment of this linear model.
They do not constrain the maximum of A_a to the VCA eigenvalue. A shift of
the main peak is compensated by spectral weight elsewhere.

This makes centroid-versus-peak separation an especially useful consistency
check: an alloy Hamiltonian can have a correct uniform endpoint interpolation
and very different disorder-renormalized peaks. It also means centroid
agreement is not independent validation of its physical impurity potential.
The theorem does not cover a nonlinear self-consistent environment response.

## Consequences for the HgCdTe program

**CALCULATED:** explicit random supercells of the frozen Schindler-derived
quarter-share vertex give a signed Gamma spectral-peak separation -0.138 eV
at x=0.179977 and approximately zero at x=0.299769. The VCA inversion of
the same model is x=0.181661. This cannot be attributed solely to the
endpoint interpolation because the interior Hamiltonian is solved directly.
These are finite-size, finite-broadening peak observables, not a proof of a
topological transition or an exact physical gap.

The decision is to stop using this bare vertex as a physical predictive
candidate while retaining it as an executable diagnostic. The required
material input remains a common-gauge self-consistent substitution potential.
The positive dynamic sign and exact configurational closures remain useful,
but a finite constant A and a smooth endpoint hierarchy need a definition
of the spectral observable and channel-specific regularity checks.
