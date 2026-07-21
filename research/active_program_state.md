# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #196  
**Active program:** scale-dependent spatial disorder in HgCdTe observables  
**Execution mode:** independent, analytical-first, anonymous-only

This is the sole controlling research ledger. `research/active_progress.md` remains retired.

## Publication state

The manuscript and submission package produced through PR #194 are scientifically superseded and were removed by PR #205.

The repository currently has **no active manuscript PDF** and **no submission-ready paper**.

The following are explicitly retired:

- named manuscript source and PDF;
- the weak anonymous manuscript source and PDF;
- cover letter and personal/affiliation metadata;
- dashboard-style manuscript figures;
- SST submission builders, tests, and workflows;
- journal-readiness gates tied to the rejected draft.

Any future manuscript is anonymous only. No new `.tex` or PDF is authorized until the scientific significance gate passes.

## Preserved scientific foundations

The repository retains four complementary spatial-disorder layers:

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

Controlling files:

```text
src/mct_research/spatial_disorder.py
src/mct_research/spatial_disorder_depth.py
src/mct_research/spatial_disorder_inference.py
src/mct_research/spatial_disorder_theorems.py
docs/derivations/010_scale_dependent_spatial_disorder.md
data/validation/spatial_disorder_theorem_extension.json
literature/notes/scale_dependent_disorder_prior_art.md
```

## Active scientific question

> How does a spatially correlated HgCdTe composition field combine with finite optical, electrical, diffusion, and depth kernels to determine the apparent band-edge width, and what multiscale measurements are required to recover microscopic disorder amplitude and correlation length?

The active forward chain is

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

A finite experiment reports a filtered spatial spectrum, not the microscopic point variance `C_x(0)`.

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

Therefore one width at one resolution cannot separately identify microscopic disorder amplitude and correlation length. This is exact structural non-identifiability under the declared covariance and kernel model.

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

The inverse is poorly conditioned when scales are nearly equal or when all probes occupy the same small- or large-scale asymptote. Useful designs span the transition around `a/ell ~ 1`.

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

The same declared microscopic field appears `27.2336x` narrower in standard deviation when probe sigma increases from `1 um` to `100 um`.

This is potentially important for comparisons among micro-FTIR, wafer FTIR, PL, cutoff maps, and pixel/device distributions. It remains a sensitivity calculation, not a specimen calibration or proof of publication significance.

## Prior-art boundary

Established elements include:

- general covariance filtering;
- Gaussian convolution;
- finite-aperture HgCdTe mapping;
- spatially resolved PL and transmission;
- disorder-induced optical shifts;
- effective-thickness-dependent detector cutoff.

The candidate contribution is the combined HgCdTe observation layer, exact information limits, scale-selection design, and quantitative device consequence.

Novelty is not frozen until the following full texts are audited:

```text
10.1016/j.jcrysgro.2005.01.051
10.1007/s11664-005-0022-8
10.1364/JOT.91.000077
```

## Current validation state

PR #205 passed:

- focused spatial-disorder theorem workflow;
- complete Python 3.11 suite;
- complete Python 3.13 suite;
- Dingrong Table 1 reproduction;
- external-validation gate.

The equations are implemented and regression-tested. The paper-level claim is not yet authorized.

## Required next milestones

1. complete the three-paper full-text prior-art audit;
2. propagate realistic measurement uncertainty through the nonlinear two-scale inverse;
3. quantify covariance-family misspecification using three or more probe scales;
4. combine lateral and depth kernels in representative HgCdTe measurement geometries;
5. connect the spatial layer to the Herrmann absorption operator without identifying tail energy with microscopic variance;
6. connect the spatial layer to mapped detector cutoff with explicit optical/electrical kernels;
7. determine whether the scale effect survives plausible nuisance parameters and experimental errors;
8. construct 4--6 theorem-centered figures;
9. write a new equation-dense anonymous manuscript only after the significance gate passes.

## Explicitly unauthorized

- named manuscript or named PDF;
- cover letter, journal package, or personal metadata;
- restoring the superseded PR #194 manuscript;
- treating the present sensitivity case as a fitted material result;
- claiming general covariance filtering as new mathematics;
- equating microscopic composition variance, filtered variance, Urbach energy, PL linewidth, and cutoff spread;
- inferring a correlation length from historical spectra without spatial covariance evidence;
- journal selection or submission packaging before the scientific gate;
- dashboard-style figure collections;
- requiring collaborators or expensive first-principles work without a result-changing need.
