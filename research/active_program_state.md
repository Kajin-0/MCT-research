# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #167  
**Active milestone:** #173  
**Execution mode:** independent, public-data-first, reproducible computation

## Completed Paper I

The observation-model uncertainty manuscript is scientifically frozen:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

It establishes that historical composition uncertainty, specimen state, source lineage, carrier/defect state, and edge-definition choice dominate the sub-meV ordering among common empirical gap laws. Remaining work on that manuscript is submission administration, not expansion of the scientific scope.

## Active flagship program

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

A reported gap is not assumed to equal `Eg(mean x, T)`.

## Distributional transition results

### Local propagation

At nominal `x=0.155`, `T=77 K` under the reconstructed Laurenti law:

```text
sigma_x=0.001 -> sigma_E=1.719 meV, sigma_Tc=4.463 K
sigma_x=0.005 -> sigma_E=8.596 meV, sigma_Tc=22.316 K
```

These are precision diagnostics, not asserted specimen widths or topological invariants.

### Exact bounded-Gaussian quadrature

At mean `x=0.155`, the existing latent laws give:

```text
Laurenti reconstructed              77.1241 K
Hansen-Schmit-Casselman             52.0438 K
archived provisional Hansen-Pade    52.5937 K
central model span                  25.0803 K
```

At `sigma_x=0.001`, exact composition-induced critical-temperature widths are `3.804-4.560 K`; latent-law uncertainty dominates.

At `sigma_x=0.005`, exact conditional widths are `18.345-22.290 K`, and `0.36-1.30%` of the declared composition model remains normal throughout `0-300 K`.

At `sigma_x=0.010`, `8.60-14.12%` remains normal throughout the window. Conditional means shift by `5.52-11.05 K`, while local linearization overestimates conditional width by `6.68-9.66 K` because no-crossing compositions censor the root distribution.

Conditional transition moments must be reported with crossing probability.

## Gaussian-gap spectral operator

`mct_research.spectral_convolution` propagates a Gaussian local-gap distribution through

```text
alpha(E | G) = A * max(E-G, 0)^p
```

and fits an exponential tail only over a declared absorption range.

Herrmann et al. 1992 Eq. (8) uses

```text
sigma_G=sqrt(2)*s
```

For the source-aligned square-root edge and `1-100 cm^-1` fit range:

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

Changing only the fit window increases the inferred tail energy by `60.1%` between the source and upper windows. An observed `W_fit=4 meV` permits `sigma_G=6.995-12.661 meV` across the declared operator family.

Authorized conclusion: a Gaussian gap distribution can generate an Urbach-like tail and reproduce the Herrmann scale under source-aligned conditions.

Unauthorized conclusion: an Urbach energy does not uniquely identify `sigma_G`, `sigma_x`, or one microscopic mechanism.

## Chang detector-cutoff operator

Issue #173 extends the source-bounded Chang 2006 nonparabolic-Urbach shape into a single-pass response operator:

```text
R(E,d) = 1-exp[-alpha(E)d]
alpha_target = -ln(1-R_target)/d
```

On the tail branch:

```text
E_cut = E_join + W ln(alpha_target/alpha_join)
E_cut(d2)-E_cut(d1) = -W ln(d2/d1)
```

For the declared synthetic parameters

```text
Eg        = 0.100 eV
W         = 0.012 eV
b         = 0.100 eV
amplitude = 50000 cm^-1
```

50% response gives:

```text
thickness   energy       wavelength   branch
1 um        147.269 meV   8.419 um     intrinsic
2 um        112.794 meV  10.992 um     intrinsic
5 um         99.629 meV  12.445 um     tail
10 um        91.312 meV  13.578 um     tail
20 um        82.994 meV  14.939 um     tail
```

The source-valid 5-to-20 um change shifts the apparent cutoff by `-16.636 meV` or `+2.494 um` without changing the latent `Eg`.

### Structural identifiability result

For Chang tail cutoffs,

```text
E_cut_i = C(Eg,W,A,b) + W * L_i
```

where `L_i` depends only on thickness and response criterion. Therefore every Jacobian row lies in the span of two vectors and

```text
rank(J_tail) <= 2
```

for parameters `(Eg, W, ln A, ln b)`, regardless of the number of tail-only cutoff observations.

Nine tail-only synthetic observations give singular values:

```text
4.7561439
1.0049619
1.92e-12
9.75e-13
```

and numerical rank two.

A mixed tail/intrinsic design gives:

```text
4.5297860
0.7024186
0.1983685
0.0226704
rank = 4
condition number = 199.81
```

Intrinsic crossings restore local rank, but the inversion remains weak in one parameter direction.

Authorized conclusion: repeated tail-only detector cutoffs can identify `W` and one intercept combination but cannot separately identify `Eg`, amplitude, and `b`.

Unauthorized conclusion: the synthetic parameters are not inferred for Chang Figure 2 or any real specimen.

The immutable record is `data/validation/chang_2006_cutoff_identifiability.json`.

## Source and validation boundary

Chang Figure 2 remains blocked for quantitative material validation because:

- native numeric data and calibration are unavailable;
- the caption and body report inconsistent temperature;
- same-specimen `W` and `b` are not tabulated;
- the reported `b=103+/-2 meV` belongs to a separate `x=0.23`, `77 K` calculation;
- effective absorbing thickness and carrier-state provenance are incomplete.

The current result is a synthetic structural-identifiability theorem and forward-operator validation, not real-specimen parameter extraction.

## Static and finite-temperature methods

The selected-band CdTe static post-processing result remains independently reproducible on the same immutable physical artifact. It is retained as a mathematical and software component, not as a converged HgCdTe material prediction.

The present CdTe polar response remains unsuitable for a production AHC result. New AHC, SQS, CPA, SCBA, or alloy production calculations require a decision-changing observable, a published validation target, and a predeclared termination criterion.

## Deferred collaboration package

The paired same-specimen acquisition protocol remains a rigorous future validation design. Outreach and facility access are inactive and are not dependencies of the current program.

## Authorized next work

1. complete CI validation and merge the Chang detector-cutoff operator;
2. search for a calibrated multi-thickness or full-spectrum dataset with effective-thickness provenance;
3. implement a carrier-filled optical branch and test it against Dingrong's degenerate specimen;
4. test whether one distributional state model can jointly explain Ivanov-Omskii PL displacement and FWHM changes;
5. build cross-modal recoverability and operator-induced rank-reversal maps;
6. begin the flagship manuscript once the first real-spectrum reproduction passes.

## Explicitly unauthorized

- reopening unconstrained empirical gap fitting;
- selecting one edge without an operator declaration;
- identifying `sigma_x`, `sigma_E`, Herrmann `s`, Urbach energy, PL FWHM, and quasiparticle linewidth as equivalent;
- reporting conditional transition moments without crossing probability;
- treating high log-linear `R^2` as proof of one tail mechanism;
- inferring a gap-distribution width without intrinsic-branch, normalization, and fit-window provenance;
- treating detector cutoff as a direct material gap;
- treating physical film thickness as effective absorbing thickness without validation;
- extrapolating Chang outside its source-relative energy domain;
- transferring the source `x=0.23` value of `b` to another specimen;
- requiring real collaborators before independent progress can continue;
- escalating to expensive atomistic or first-principles work without a decision-changing validation target;
- expanding Paper I with unrelated mechanisms.
