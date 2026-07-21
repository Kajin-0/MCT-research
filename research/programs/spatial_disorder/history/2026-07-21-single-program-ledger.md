# Archived snapshot: single-program spatial-disorder ledger

**Snapshot date:** 2026-07-21  
**Historical source:** `research/active_program_state.md` before portfolio reorganization  
**Status:** preserved historical program record; not repository-wide governance

This file preserves the detailed spatial-disorder state that previously occupied the global compatibility path. Its scientific content remains relevant to the spatial-disorder workstream, but its former `sole controlling ledger` semantics are retired.

## Publication state at snapshot

The manuscript and submission package produced through PR #194 had been judged scientifically superseded and removed by PR #205.

At this snapshot the repository had no active manuscript PDF and no submission-ready paper for this workstream. Named manuscript source/PDF, cover letter and personal metadata, dashboard-style figures, and SST submission tooling had been retired. Any future manuscript was to be anonymous and gated by scientific significance.

## Preserved scientific foundations

The workstream retained four complementary layers:

1. **Gaussian covariance/kernel core**
   - anisotropic covariance matrices;
   - anisotropic Gaussian probes;
   - stable log-determinant variance evaluation;
   - validated isotropic two-scale inversion.
2. **Finite-depth kernels**
   - Beer--Lambert depth weighting;
   - finite-slab averaging and asymptotic checks.
3. **Multiscale recoverability diagnostics**
   - exact variance predictions;
   - analytical log-parameter Jacobian;
   - Cholesky-whitened Fisher information;
   - rank, condition number, parameter correlation, and null-direction diagnostics.
4. **Exact theorem and HgCdTe propagation layer**
   - one-scale non-identifiability family;
   - arbitrary-dimensional two-scale inverse;
   - closed two-scale condition number;
   - exact Gaussian and exponential top-hat formulas;
   - second-order gap propagation;
   - first-order cutoff-spread propagation.

Controlling files at the snapshot included:

```text
src/mct_research/spatial_disorder.py
src/mct_research/spatial_disorder_depth.py
src/mct_research/spatial_disorder_inference.py
src/mct_research/spatial_disorder_theorems.py
docs/derivations/010_scale_dependent_spatial_disorder.md
data/validation/spatial_disorder_theorem_extension.json
literature/notes/scale_dependent_disorder_prior_art.md
```

## Active scientific question at snapshot

> How does a spatially correlated HgCdTe composition field combine with finite optical, electrical, diffusion, and depth kernels to determine the apparent band-edge width, and what multiscale measurements are required to recover microscopic disorder amplitude and correlation length?

The forward chain was

```text
microscopic composition random field
-> covariance / power spectrum
-> lateral and depth measurement kernels
-> probe-averaged composition distribution
-> signed HgCdTe gap distribution
-> optical or detector observation operator
-> reported edge, linewidth, or cutoff spread
```

## Exact observation law

For stationary composition covariance `C_x` and normalized kernel `w`,

```text
Var(X_w)
=
int int w(r) w(r') C_x(r-r') dr dr'.
```

Equivalently,

```text
Var(X_w)
=
(2 pi)^(-D) int S_x(k) |W(k)|^2 dk.
```

A finite experiment reports a filtered spatial spectrum rather than microscopic point variance `C_x(0)`.

For isotropic Gaussian covariance and a `D`-dimensional Gaussian probe,

```text
V(a)
=
sigma_x^2 (1 + 2 a^2/ell^2)^(-D/2).
```

## One-scale no-go result

For one measured variance `V*` at one scale `a*`, every positive correlation length can be paired with

```text
sigma_x^2(ell)
=
V* (1 + 2 a*^2/ell^2)^(D/2)
```

to produce the same observation.

Therefore one width at one resolution cannot separately identify microscopic disorder amplitude and correlation length under the declared model.

## Exact two-scale inverse

For distinct scales, define

```text
q = (V1/V2)^(2/D).
```

Then

```text
ell^2 = 2 (a2^2 - q a1^2)/(q - 1)
```

and

```text
sigma_x^2 = V1 (1 + 2 a1^2/ell^2)^(D/2).
```

Algebraic identifiability does not guarantee practical recoverability.

For logarithmic parameters, Jacobian row `i` is

```text
[1, D(2 a_i^2/ell^2)/(1 + 2 a_i^2/ell^2)].
```

The inverse is poorly conditioned when scales are nearly equal or all probes occupy the same small- or large-scale asymptote. Useful designs span the transition around `a/ell ~ 1`.

## HgCdTe propagation

For filtered composition variance `V_a`, a quadratic expansion gives

```text
E[Eg] ~= Eg(xbar,T) + 0.5 Eg_xx V_a
```

and

```text
Var(Eg) ~= Eg_x^2 V_a + 0.5 Eg_xx^2 V_a^2.
```

The variance expression is exact for a quadratic composition dependence and Gaussian probe-averaged composition.

For `lambda_c = hc/E_c`,

```text
sigma_lambda ~= lambda_c sigma_E / |E_c|.
```

## First significance screen

Declared model-conditioned case:

```text
D                                  2
point composition sigma            0.005
correlation length                 5 um
local |dEg/dx|                     1.7191085 eV
reference cutoff                   10 um
```

Results:

```text
probe sigma     apparent gap sigma     apparent cutoff sigma
1 um             8.271 meV              0.6671 um
5 um             4.963 meV              0.4003 um
10 um            2.865 meV              0.2311 um
100 um           0.304 meV              0.02450 um
```

The same declared microscopic field appeared `27.2336x` narrower in standard deviation when probe sigma increased from `1 um` to `100 um`.

This was recorded as a potentially important sensitivity calculation for comparisons among micro-FTIR, wafer FTIR, PL, cutoff maps, and pixel/device distributions—not as a specimen calibration or proof of publication significance.

## Prior-art boundary at snapshot

Established elements included:

- general covariance filtering;
- Gaussian convolution;
- finite-aperture HgCdTe mapping;
- spatially resolved PL and transmission;
- disorder-induced optical shifts;
- effective-thickness-dependent detector cutoff.

The candidate contribution was the combined HgCdTe observation layer, exact information limits, scale-selection design, and quantitative device consequence.

Novelty was not frozen pending full-text audits of:

```text
10.1016/j.jcrysgro.2005.01.051
10.1007/s11664-005-0022-8
10.1364/JOT.91.000077
```

## Validation state at snapshot

PR #205 had passed:

- focused spatial-disorder theorem workflow;
- complete Python 3.11 suite;
- complete Python 3.13 suite;
- Dingrong Table 1 reproduction;
- external-validation gate.

The equations were implemented and regression-tested. Paper-level claims were not authorized.

## Required milestones recorded at snapshot

1. complete the three-paper full-text prior-art audit;
2. propagate realistic measurement uncertainty through the nonlinear two-scale inverse;
3. quantify covariance-family misspecification using three or more probe scales;
4. combine lateral and depth kernels in representative HgCdTe measurement geometries;
5. connect the spatial layer to the Herrmann absorption operator without identifying tail energy with microscopic variance;
6. connect the spatial layer to mapped detector cutoff with explicit optical/electrical kernels;
7. determine whether the scale effect survives plausible nuisance parameters and experimental errors;
8. construct theorem-centered figures;
9. write an anonymous manuscript only after the significance gate passes.

## Workstream-specific restrictions recorded at snapshot

- no named manuscript or named PDF for this workstream;
- no cover letter, journal package, or personal metadata before authorization;
- no restoration of the superseded PR #194 manuscript;
- no treatment of the sensitivity case as a fitted material result;
- no claim that general covariance filtering is new mathematics;
- no equation of microscopic composition variance, filtered variance, Urbach energy, PL linewidth, and cutoff spread;
- no inference of correlation length from historical spectra without spatial covariance evidence;
- no journal selection or submission packaging before the scientific gate;
- no requirement for collaborators or expensive first-principles work without a result-changing need.

These restrictions apply to the archived spatial-disorder program state. They are not repository-wide prohibitions on unrelated programs.