# Theorem and proposition index

## Purpose

This index assigns stable labels to the analytical claims used by the flagship manuscript. It separates exact statements from numerical demonstrations and source-conditioned reproductions.

The labels below are manuscript-facing. The controlling derivations remain in `docs/derivations/008` through `013`.

## Proposition 1 — Local composition-to-gap propagation

Let a local composition variable satisfy

$$
X=\bar x+\delta x,
\qquad
\mathbb E[\delta x]=0,
\qquad
\operatorname{Var}(X)=\sigma_x^2.
$$

For a twice-differentiable latent gap law and sufficiently narrow composition variation,

$$
\mathbb E[E_g(X,T)]
=
E_g(\bar x,T)
+\frac12E_{g,xx}(\bar x,T)\sigma_x^2
+O(\mathbb E|\delta x|^3),
$$

and

$$
\operatorname{Var}[E_g(X,T)]
=E_{g,x}(\bar x,T)^2\sigma_x^2+O(\mathbb E|\delta x|^3).
$$

### Proof summary

Apply a second-order Taylor expansion around `x=bar x`, take expectations, and use the declared zero mean of `delta x`.

### Claim class

Exact asymptotic proposition under the declared regularity and narrow-distribution assumptions.

### Controlling implementation

- `src/mct_research/distributional_gap.py`
- `docs/derivations/008_distributional_bandgap_propagation.md`

## Proposition 2 — Local critical-temperature amplification

Suppose a simple transition root satisfies

$$
E_g(x,T_c(x))=0,
\qquad
E_{g,T}\ne0.
$$

Then

$$
\frac{dT_c}{dx}
=-\frac{E_{g,x}}{E_{g,T}},
$$

and the local composition-induced transition width is

$$
\sigma_{T_c}
\approx
\left|\frac{E_{g,x}}{E_{g,T}}\right|\sigma_x.
$$

### Proof summary

Differentiate the implicit transition equation with respect to composition and apply first-order variance propagation.

### Boundary

This local approximation does not include no-crossing compositions, multiple roots, bounded-alloy truncation, or conditional-root censoring. Exact bounded-Gaussian quadrature controls those cases.

## Proposition 3 — Gaussian-gap scale form

For the declared local edge

$$
\alpha_{\rm loc}(E\mid G)=A(E-G)_+^p
$$

and

$$
G\sim\mathcal N(\mu_G,\sigma_G^2),
$$

the convolved absorption has the scale form

$$
\bar\alpha(E)
=A\sigma_G^p
F_p\!\left(\frac{E-\mu_G}{\sigma_G}\right),
$$

where

$$
F_p(z)=\int_{-\infty}^{z}(z-u)^p\phi(u)\,du.
$$

### Proof summary

Substitute `G=mu_G+sigma_G u` in the Gaussian convolution and factor out `sigma_G^p`.

### Consequence

The spectral coordinate is controlled by `(E-mu_G)/sigma_G`, while amplitude contains the product `A sigma_G^p`.

## Source reproduction 1 — Herrmann tail scale

Herrmann et al. use

$$
P(G)=\frac{1}{2s\sqrt\pi}
\exp\left[-\frac{(G-\bar G)^2}{4s^2}\right],
$$

so

$$
\sigma_G=\sqrt2\,s.
$$

For the source-aligned square-root local edge, normalization, and `1-100 cm^-1` fit interval, the repository obtains

$$
W_{\rm fit}/s=0.50504,
\qquad
R^2=0.99570.
$$

### Status

Source-conditioned reproduction, not a theorem that `W=s/2` universally.

### Non-uniqueness result

Changing only the fit interval from `1-100` to `100-500 cm^-1` changes `W_fit/s` from `0.50504` to `0.80871`, a `60.1%` increase.

## Theorem 1 — Exponential-tail thickness law

For a single-pass response

$$
R(E,d)=1-\exp[-\alpha(E)d]
$$

and a target response `R_t`, the target absorption is

$$
\alpha_t=-\frac{\ln(1-R_t)}{d}.
$$

If the crossing lies on

$$
\alpha(E)=\alpha_j\exp[(E-E_j)/W],
$$

then

$$
E_c=E_j+W\ln(\alpha_t/\alpha_j),
$$

and therefore

$$
\boxed{E_c(d_2)-E_c(d_1)=-W\ln(d_2/d_1)}.
$$

### Proof summary

Invert the Beer–Lambert target response, substitute the exponential tail, and subtract the two cutoff equations.

### Controlling implementation

- `src/mct_research/detector_cutoff.py`
- `docs/derivations/011_thickness_dependent_cutoff_identifiability.md`

## Theorem 2 — Tail-only cutoff rank bound

For the source-bounded Chang tail, every declared cutoff can be written

$$
E_{c,i}=C(E_g,W,A,b)+WL_i,
$$

where `L_i` depends only on effective thickness and response criterion.

For parameters

$$
\theta=(E_g,W,\ln A,\ln b),
$$

every Jacobian row lies in the span of `grad C` and `grad W`. Hence

$$
\boxed{\operatorname{rank}(J_{\rm tail})\le2}.
$$

### Proof summary

Differentiate `E_c,i=C+W L_i`. Each row is `grad C + L_i grad W`, so the row space has dimension at most two regardless of the number of cutoff observations.

### Numerical verification

Nine tail-only observations give two finite singular values and two relative singular directions near `10^-13`.

## Proposition 4 — Exact Kane-type nonparabolic filling solution

For

$$
E_c(1+\alpha E_c)=E_{\rm par},
$$

the positive solution is

$$
\boxed{
E_c=
\frac{2E_{\rm par}}
{1+\sqrt{1+4\alpha E_{\rm par}}}
}.
$$

Let

$$
q=\alpha E_{\rm par}.
$$

Then the relative parabolic overestimate is

$$
\boxed{
\frac{E_{\rm par}-E_c}{E_c}
=\frac{\sqrt{1+4q}-1}{2}
}.
$$

### Proof summary

Solve the quadratic in `E_c` and rationalize the positive root. Substitute the solution into `(E_par-E_c)/E_c`.

### Boundary

This is a declared isotropic zero-temperature carrier-filling model, not a full finite-temperature Dingrong spectrum reproduction.

## Proposition 5 — Single-edge carrier identifiability

One scalar optical edge measured at one density has local Jacobian rank at most one, irrespective of the number of physical parameters entering the scalar edge model.

### Proof summary

The Jacobian of one scalar observation is one row. Its rank cannot exceed one.

### Numerical result

A five-density series for `(ln Eg0, ln m_edge, ln alpha, ln m_valence, ln C_BGR)` is locally full rank in the declared design but has condition number `11034.75`.

## Theorem 3 — Unified unmarked-spectrum structural rank

Let

$$
G\sim\mathcal N(E_g^{(0)}+\Delta_c,\sigma_G^2)
$$

and

$$
R(E)=1-\exp\left\{
-Ad\,\sigma_G^p
F_p\left[
\frac{E-E_g^{(0)}-\Delta_c}{\sigma_G}
\right]
\right\}.
$$

For parameters

$$
\theta=(E_g^{(0)},\Delta_c,\ln\sigma_G,\ln A,\ln d),
$$

the complete single-state spectrum depends only on

$$
E_g^{(0)}+\Delta_c,
\qquad
\sigma_G,
\qquad
Ad.
$$

Therefore

$$
\frac{\partial R}{\partial E_g^{(0)}}
=
\frac{\partial R}{\partial\Delta_c},
$$

$$
\frac{\partial R}{\partial\ln A}
=
\frac{\partial R}{\partial\ln d},
$$

and

$$
\boxed{\operatorname{rank}(J)\le3}.
$$

### Proof summary

Read the three invariant combinations directly from the scale-form response. The two pairwise Jacobian identities follow by differentiation.

### Exact counterexample

The parameter sets

```text
Eg0=0.100 eV, Delta=0.030 eV, sigma=0.010 eV, A=30000, d=10 um
Eg0=0.120 eV, Delta=0.010 eV, sigma=0.010 eV, A=15000, d=20 um
```

preserve the translated mean and `A*d`. Their 281-point response spectra differ by at most `2.22e-16`.

## Theorem 4 — Marked-spectrum combined invariance

Add an absolutely calibrated carrier-dependent marker

$$
\alpha_m(E)=B\Delta_c(E_r/E)^2.
$$

The marked response depends on four combinations:

$$
E_g^{(0)}+\Delta_c,
\qquad
\sigma_G,
\qquad
Ad,
\qquad
\Delta_c d.
$$

For any positive scale `c`, the transformation

$$
d\to cd,
\qquad
A\to A/c,
\qquad
\Delta_c\to\Delta_c/c,
$$

$$
E_g^{(0)}
\to
E_g^{(0)}+\Delta_c(1-1/c)
$$

leaves all four combinations unchanged. The infinitesimal null vector in coordinates

$$
(E_g^{(0)},\Delta_c,\ln\sigma_G,\ln A,\ln d)
$$

is

$$
\boxed{(\Delta_c,-\Delta_c,0,-1,1)}.
$$

### Consequence

The marked spectrum has structural rank at most four. In the declared numerical design it reaches rank four, and independently known effective thickness removes the remaining null direction.

### Boundary

The marker is an identifiability diagnostic, not the physical free-carrier absorption law of Dingrong et al.

## Corollary — Minimum external information for latent-gap recovery

Under the unmarked unified model, a single-state spectrum cannot separately recover the latent zero-density gap and a rigid carrier translation, nor absorption amplitude and effective thickness.

At minimum, latent-gap recovery requires:

1. independent carrier-state information plus a validated carrier-shift model;
2. independently calibrated effective thickness or absorption amplitude;
3. a full calibrated spectrum with sufficient range to resolve the remaining spectral combinations.

A calibrated nontranslational carrier feature replaces the two simple null directions with one combined null direction, but one independent scale remains necessary.

## Publication boundary

Theorems 1–4 are forward-model statements. They do not establish that the controlled Gaussian, power-law, Chang, or generic carrier-marker models are complete microscopic descriptions of a specific HgCdTe specimen. External material validation remains a separate claim class.