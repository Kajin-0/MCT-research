# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #167  
**Active milestone:** #175  
**Execution mode:** independent, public-data-first, reproducible computation

## Completed Paper I

The observation-model uncertainty manuscript is scientifically frozen:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

It establishes that historical composition uncertainty, specimen state, source lineage, carrier/defect state, and edge-definition choice dominate the sub-meV ordering among common empirical gap laws. Remaining work is submission administration, not scientific expansion.

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

A reported gap is not assumed to equal `Eg(mean x,T)`.

## Distributional transition results

At nominal `x=0.155`, `T=77 K` under the reconstructed Laurenti law:

```text
sigma_x=0.001 -> sigma_E=1.719 meV, sigma_Tc=4.463 K
sigma_x=0.005 -> sigma_E=8.596 meV, sigma_Tc=22.316 K
```

Exact bounded-Gaussian quadrature gives central critical temperatures:

```text
Laurenti reconstructed              77.1241 K
Hansen-Schmit-Casselman             52.0438 K
archived provisional Hansen-Pade    52.5937 K
central model span                  25.0803 K
```

At `sigma_x=0.001`, exact composition-induced widths are `3.804-4.560 K`; latent-law uncertainty dominates.

At `sigma_x=0.005`, exact conditional widths are `18.345-22.290 K`, and `0.36-1.30%` of the declared composition model remains normal throughout `0-300 K`.

At `sigma_x=0.010`, `8.60-14.12%` remains normal throughout the window. Conditional means shift by `5.52-11.05 K`, while local linearization overestimates conditional width by `6.68-9.66 K` because no-crossing compositions censor the root distribution.

Conditional transition moments must be reported with crossing probability.

## Gaussian-gap spectral operator

For the Herrmann source convention `sigma_G=sqrt(2)*s`, the source-aligned square-root convolution over `1-100 cm^-1` gives:

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

For the declared synthetic parameters `Eg=0.100 eV`, `W=0.012 eV`, `b=0.100 eV`, and amplitude `50000 cm^-1`, 50% response gives:

```text
thickness   energy       wavelength   branch
1 um        147.269 meV   8.419 um     intrinsic
2 um        112.794 meV  10.992 um     intrinsic
5 um         99.629 meV  12.445 um     tail
10 um        91.312 meV  13.578 um     tail
20 um        82.994 meV  14.939 um     tail
```

The source-valid 5-to-20 um change shifts the apparent cutoff by `-16.636 meV` or `+2.494 um` without changing the latent `Eg`.

Every tail cutoff has the form

```text
E_cut_i=C(Eg,W,A,b)+W*L_i
```

so

```text
rank(J_tail)<=2
```

for `(Eg,W,ln A,ln b)`, regardless of the number of tail-only observations.

Nine tail observations give singular values:

```text
4.7561439
1.0049619
1.16e-12
4.86e-13
```

A mixed tail/intrinsic design restores rank four but has condition number `199.81`.

Authorized conclusion: repeated tail-only cutoffs identify `W` and one intercept combination but cannot separately identify `Eg`, amplitude, and `b`.

Chang Figure 2 remains blocked for material validation because native numeric data, calibration, consistent temperature, same-specimen `W` and `b`, and effective-thickness provenance are unavailable.

## Degenerate carrier-filled edge operator

Issue #175 adds the declared zero-temperature model:

```text
k_F=(3*pi^2*n/g_v)^(1/3)
E_par=hbar^2*k_F^2/(2*m_edge)
E_c*(1+alpha*E_c)=E_par
Delta_E_BM=E_c+hbar^2*k_F^2/(2*m_valence)
E_opt=Eg0+Delta_E_BM+Delta_E_BGR+Delta_E_obs
```

The exact nonparabolic conduction solution is

```text
E_c=2*E_par/(1+sqrt(1+4*alpha*E_par))
```

and the parabolic relative overestimate is

```text
(E_par-E_c)/E_c=(sqrt(1+4*q)-1)/2
q=alpha*E_par
```

### Dingrong-density sensitivity case

Declared illustrative parameters:

```text
n          = 7.0e17 cm^-3
Eg0        = 0.100 eV
m_edge     = 0.010 m0
alpha      = 7.5 eV^-1
m_valence  = 0.35 m0
C_BGR      = 0.020 eV at 1e18 cm^-3
```

These are not inferred for the Dingrong specimen.

Results:

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

The fully parabolic filling shift is `1.993` times the nonparabolic result. For the declared parameter set, the conduction-energy error grows from `0.0046 meV` at `1e14 cm^-3` to `147.323 meV` at `7e17 cm^-3`; a 5% error occurs near `2.66e15 cm^-3`.

### Carrier-edge identifiability

One edge at one density has rank one for parameters:

```text
ln Eg0
ln m_edge
ln alpha
ln m_valence
ln C_BGR
```

A five-density series at `1e16, 3e16, 1e17, 3e17, 7e17 cm^-3` has local rank five but singular values:

```text
2.55477493e-1
6.63828971e-2
4.64192311e-3
1.81849453e-4
2.31520896e-5
```

and condition number:

```text
11034.75
```

Formal full rank does not support a reliable unconstrained inversion. Independent Hall, mass, low-density-gap, and renormalization constraints remain necessary.

The current Dingrong result is a bounded high-density sensitivity anchor, not a full source-spectrum reproduction. The free-carrier background and two-mode phonon scattering remain unimplemented.

## Static and finite-temperature methods

The selected-band CdTe static post-processing result remains independently reproducible on the same immutable physical artifact. It is a mathematical and software component, not a converged HgCdTe material prediction.

The present CdTe polar response remains unsuitable for production AHC. New AHC, SQS, CPA, SCBA, or alloy production calculations require a decision-changing observable, a published validation target, and a predeclared termination criterion.

## Deferred collaboration package

The paired same-specimen acquisition protocol remains a rigorous future validation design. Outreach and facility access are inactive and are not dependencies of the current program.

## Authorized next work

1. complete CI validation and merge the carrier-filled edge foundation;
2. recover source-native Dingrong equations/spectra or implement only explicitly available free-carrier terms;
3. combine carrier filling with the distributed-gap and detector-cutoff operators;
4. test whether one distributional state model can jointly explain Ivanov-Omskii PL displacement and FWHM changes;
5. build cross-modal recoverability and operator-induced rank-reversal maps;
6. begin the flagship manuscript once the first real-spectrum reproduction passes.

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
- treating free-carrier absorption as the interband edge;
- assigning the illustrative carrier parameters to the Dingrong specimen;
- requiring real collaborators before independent progress can continue;
- escalating to expensive atomistic or first-principles work without a decision-changing validation target;
- expanding Paper I with unrelated mechanisms.
