# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #167  
**Active milestone:** #177  
**Execution mode:** independent, public-data-first, reproducible computation

## Completed Paper I

The observation-model uncertainty manuscript is scientifically frozen:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

It establishes that historical composition uncertainty, specimen state, source lineage, carrier/defect state, and edge-definition choice dominate the sub-meV ordering among common empirical gap laws. Remaining work is submission administration, not scientific expansion.

## Flagship objective

The active research product is:

> **A distributional, observation-aware theory of HgCdTe band-edge observables.**

The controlling chain is:

```text
latent mean signed gap
-> composition/gap distribution
-> carrier and defect state
-> intrinsic, tail, and free-carrier response
-> thickness/instrument response
-> declared observation operator
-> reported gap observable
```

A reported edge is not assumed to equal `Eg(mean x,T)`.

## Distributional transition results

At nominal `x=0.155`, `T=77 K` under the reconstructed Laurenti law:

```text
sigma_x=0.001 -> sigma_E=1.719 meV, sigma_Tc=4.463 K
sigma_x=0.005 -> sigma_E=8.596 meV, sigma_Tc=22.316 K
```

Exact bounded-Gaussian quadrature gives:

```text
Laurenti central Tc                 77.1241 K
Hansen central Tc                   52.0438 K
archived Hansen-Pade central Tc     52.5937 K
central latent-law span             25.0803 K
```

At `sigma_x=0.001`, exact composition-induced widths are `3.804-4.560 K`; latent-law uncertainty dominates.

At `sigma_x=0.005`, conditional widths are `18.345-22.290 K`, and `0.36-1.30%` of the declared composition model remains normal throughout `0-300 K`.

At `sigma_x=0.010`, `8.60-14.12%` remains normal throughout the window. Conditional means shift by `5.52-11.05 K`, while local linearization overestimates conditional width by `6.68-9.66 K` because no-crossing compositions censor the root distribution.

Conditional transition moments must be reported with crossing probability.

## Gaussian-gap spectral operator

For the Herrmann convention `sigma_G=sqrt(2)*s`, the source-aligned square-root convolution over `1-100 cm^-1` gives:

```text
W_fit / s = 0.50504
R^2       = 0.99570
```

The same spectrum gives:

```text
fit window       W_fit / s    R^2
0.1-100          0.46096      0.99307
1-100            0.50504      0.99570
10-100           0.56806      0.99836
10-500           0.66828      0.99190
100-500          0.80871      0.99738
```

Changing only the fit window increases the inferred tail energy by `60.1%`. An observed `W_fit=4 meV` permits `sigma_G=6.995-12.661 meV` across the declared operator family.

Authorized conclusion: a Gaussian gap distribution can generate an Urbach-like tail and reproduce the Herrmann scale under source-aligned conditions.

Unauthorized conclusion: an Urbach energy does not uniquely identify `sigma_G`, `sigma_x`, or one microscopic mechanism.

## Chang detector-cutoff operator

The source-bounded Chang shape is propagated through

```text
R(E,d)=1-exp[-alpha(E)d]
alpha_target=-ln(1-R_target)/d
```

On the tail branch:

```text
E_cut=E_join+W ln(alpha_target/alpha_join)
E_cut(d2)-E_cut(d1)=-W ln(d2/d1)
```

For declared synthetic parameters `Eg=0.100 eV`, `W=0.012 eV`, `b=0.100 eV`, and amplitude `50000 cm^-1`, 50% response gives:

```text
thickness   energy       wavelength   branch
1 um        147.269 meV   8.419 um     intrinsic
2 um        112.794 meV  10.992 um     intrinsic
5 um         99.629 meV  12.445 um     tail
10 um        91.312 meV  13.578 um     tail
20 um        82.994 meV  14.939 um     tail
```

The source-valid 5-to-20 um change shifts the apparent cutoff by `-16.636 meV` or `+2.494 um` without changing latent `Eg`.

Every tail cutoff has form

```text
E_cut_i=C(Eg,W,A,b)+W*L_i
```

so `rank(J_tail)<=2` for `(Eg,W,ln A,ln b)` regardless of the number of tail-only observations.

Nine tail observations give singular values:

```text
4.7561439
1.0049619
1.16e-12
4.86e-13
```

A mixed tail/intrinsic design restores rank four but has condition number `199.81`.

Authorized conclusion: repeated tail-only cutoffs identify `W` and one intercept combination but cannot separately identify `Eg`, amplitude, and `b`.

Chang Figure 2 remains blocked for material validation because native data, calibration, consistent temperature, same-specimen `W` and `b`, and effective-thickness provenance are unavailable.

## Degenerate carrier-filled edge operator

The declared zero-temperature model is:

```text
k_F=(3*pi^2*n/g_v)^(1/3)
E_par=hbar^2*k_F^2/(2*m_edge)
E_c*(1+alpha*E_c)=E_par
Delta_E_BM=E_c+hbar^2*k_F^2/(2*m_valence)
E_opt=Eg0+Delta_E_BM+Delta_E_BGR+Delta_E_obs
```

The exact conduction solution is

```text
E_c=2*E_par/(1+sqrt(1+4*alpha*E_par))
```

and the parabolic relative overestimate is

```text
(E_par-E_c)/E_c=(sqrt(1+4*q)-1)/2
q=alpha*E_par
```

For the declared Dingrong-density sensitivity case:

```text
n          = 7.0e17 cm^-3
Eg0        = 0.100 eV
m_edge     = 0.010 m0
alpha      = 7.5 eV^-1
m_valence  = 0.35 m0
C_BGR      = 0.020 eV at 1e18 cm^-3
```

results are:

```text
k_F                              0.0274688 A^-1
parabolic conduction energy      287.476 meV
nonparabolic conduction energy   140.154 meV
valence recoil                     8.214 meV
nonparabolic BM shift             148.367 meV
parabolic BM shift                295.690 meV
parabolic overestimate            147.323 meV
q                                  2.1561
```

These parameters are not inferred for the Dingrong specimen.

One edge at one density has rank one for five declared carrier/gap parameters. A five-density series restores local rank five but has condition number `11034.75`.

Formal full rank does not support a reliable unconstrained inversion. Independent Hall, mass, low-density-gap, and renormalization constraints remain necessary.

## Unified spectrum structural-rank theorem

Issue #177 composes:

```text
alpha_local(E|G)=A*max(E-G,0)^p
G~Normal(Eg0+Delta_carrier,sigma_G^2)
R(E)=1-exp[-alpha(E)*d]
```

### Base single-state model

The five nominal parameters

```text
Eg0
Delta_carrier
ln sigma_G
ln A
ln d
```

enter only through

```text
Eg0 + Delta_carrier
sigma_G
A * d
```

so

```text
dR/dEg0 = dR/dDelta_carrier
dR/dlnA = dR/dlnd
rank(J) <= 3
```

for an arbitrarily dense spectrum.

Exact counterexample:

```text
set 1: Eg0=0.100 eV, Delta=0.030 eV, sigma=0.010 eV,
       A=30000, d=10 um

set 2: Eg0=0.120 eV, Delta=0.010 eV, sigma=0.010 eV,
       A=15000, d=20 um
```

Across 281 points from `0.08` to `0.22 eV`, the maximum absolute response difference is `2.22e-16`.

Dense-spectrum singular values:

```text
2.10943527e2
3.12774161e0
3.79499126e-1
3.36022167e-11
4.59184616e-14
```

and numerical rank is three.

Known carrier shift alone leaves the amplitude/thickness null. Known thickness alone leaves the gap/carrier null. Constraining both leaves `(Eg0, ln sigma_G, ln A)`, which are locally full rank.

### Nontranslational carrier marker

Add the generic diagnostic feature

```text
alpha_marker=B*Delta_carrier*(E_ref/E)^2
```

with an absolute scale independent of the interband amplitude. It is not the Dingrong free-carrier absorption law.

The marker breaks both simple pairwise identities but leaves one combined invariance. The marked spectrum depends on:

```text
Eg0 + Delta_carrier
sigma_G
A * d
Delta_carrier * d
```

For any `c>0`, the transformation

```text
d -> c*d
A -> A/c
Delta_carrier -> Delta_carrier/c
Eg0 -> Eg0 + Delta_carrier*(1-1/c)
```

leaves the spectrum unchanged.

The infinitesimal null vector in coordinates `(Eg0, Delta_carrier, ln sigma_G, ln A, ln d)` is

```text
(Delta_carrier, -Delta_carrier, 0, -1, +1)
```

At the declared marker scale, singular values are

```text
2.05808179e2
6.76801242e0
3.05553476e0
3.57325799e-1
3.58461331e-11
```

and numerical rank is four. The combined-null Jacobian residual is `2.28e-11`.

Independently known effective thickness removes the remaining null and leaves `(Eg0, Delta_carrier, ln sigma_G, ln A)` locally full rank in the declared marked design.

Authorized conclusion:

> No improvement in signal-to-noise or spectral sampling can recover parameters combined exactly by the forward model. The unmarked model requires independent carrier-state and effective-thickness information. A calibrated nontranslational carrier feature raises rank but still requires one external scale to remove the remaining combined invariance.

The immutable record is `data/validation/unified_spectrum_structural_rank.json`.

## Static and finite-temperature methods

The selected-band CdTe static post-processing result remains independently reproducible on the same immutable physical artifact. It is a mathematical and software component, not a converged HgCdTe material prediction.

The present CdTe polar response remains unsuitable for production AHC. New AHC, SQS, CPA, SCBA, or alloy production calculations require a decision-changing observable, a published validation target, and a predeclared termination criterion.

## Deferred collaboration package

The paired same-specimen acquisition protocol remains a rigorous future validation design. Outreach and facility access are inactive and are not dependencies of the current program.

## Authorized next work

1. complete CI validation and merge the unified spectrum theorem;
2. begin the flagship manuscript analytical core using the merged distributional, spectral, cutoff, carrier, and structural-rank results;
3. identify one calibrated real spectrum or same-specimen multi-state dataset for external validation;
4. recover source-native Dingrong free-carrier equations only when missing definitions can be documented explicitly;
5. test whether one distributional state model can jointly explain Ivanov-Omskii PL displacement and FWHM changes;
6. build cross-modal recoverability and operator-induced rank-reversal maps.

## Explicitly unauthorized

- reopening unconstrained empirical gap fitting;
- selecting one edge without an operator declaration;
- identifying `sigma_x`, `sigma_E`, Herrmann `s`, Urbach energy, PL FWHM, and quasiparticle linewidth as equivalent;
- reporting conditional transition moments without crossing probability;
- treating high log-linear `R^2` as proof of one tail mechanism;
- treating detector cutoff as a direct material gap;
- treating physical film thickness as effective absorbing thickness without validation;
- transferring Chang `b` or Dingrong carrier corrections between specimens without provenance;
- conflating Burstein-Moss filling with band-gap renormalization;
- treating the generic carrier marker as a physical free-carrier law;
- claiming the marker identifies all five parameters without an external scale;
- claiming dense sampling removes exact forward-model invariances;
- assigning illustrative carrier parameters to the Dingrong specimen;
- requiring real collaborators before independent progress can continue;
- escalating to expensive atomistic or first-principles work without a decision-changing validation target;
- expanding Paper I with unrelated mechanisms.
