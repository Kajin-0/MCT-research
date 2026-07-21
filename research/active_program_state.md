# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #196  
**Active milestone:** scale-dependent spatial-disorder theorem  
**Execution mode:** independent, analytical-first, anonymous-only

This is the sole controlling research ledger. `research/active_progress.md` remains retired.

## Superseded submission state

The manuscript and submission bundle merged through PR #194 are scientifically superseded. They are not submission-ready.

The prior document assembled valid component calculations, but it did not develop one result deeply enough to carry a theoretical paper. Its figures operated as milestone dashboards rather than evidence for a central theorem.

The active branch removes:

- named manuscript source and PDF;
- cover letter and personal/affiliation metadata;
- the weak anonymous review source and PDF;
- dashboard-style submission figures;
- SST bundle builders, tests, and workflow.

Future manuscript artifacts are anonymous only.

## Preserved scientific base

Commit `2b740c4a881b7944e674fe75a1eb43cbfe7b2b29` remains the computational foundation. It provides:

- anisotropic Gaussian composition covariance matrices;
- anisotropic Gaussian measurement kernels;
- stable log-determinant evaluation of filtered variance;
- an exact validated two-scale inverse for the isotropic two-dimensional case;
- 699 passing tests and 6 skips on Python 3.11 and 3.13 at merge.

The active work extends that implementation rather than replacing it.

## Active scientific question

> How does spatially correlated HgCdTe composition disorder combine with a finite optical or device kernel to determine the apparent band-edge width, and what probe scales are required to recover microscopic disorder amplitude and correlation length?

The active chain is

```text
microscopic composition random field
-> covariance / power spectrum
-> optical, electrical, or diffusion kernel
-> probe-averaged composition distribution
-> signed HgCdTe gap distribution
-> optical or detector operator
-> reported width or cutoff spread
```

## Exact observation operator

For stationary covariance `C_x` and normalized kernel `w_a`,

```text
Var(X_a)
=
int int w_a(r) w_a(r') C_x(r-r') dr dr'.
```

Equivalently,

```text
Var(X_a)
=
(2 pi)^(-D) int S_x(k) |W_a(k)|^2 dk.
```

A finite measurement reports a filtered spatial spectrum, not the point variance `C_x(0)`.

## Gaussian theorem

For

```text
C_x(h) = sigma_x^2 exp[-|h|^2/(2 ell^2)]
```

and a normalized `D`-dimensional Gaussian probe of coordinate standard deviation `a`,

```text
Var(X_a)
=
sigma_x^2 (1 + 2 a^2/ell^2)^(-D/2).
```

The anisotropic core evaluates

```text
sigma_x^2 sqrt(det(Lambda)/det(Lambda + 2 Sigma_w)).
```

## One-scale no-go result

At one declared probe scale `a*`, every positive `ell` can be paired with

```text
sigma_x^2(ell)
=
V* (1 + 2 a*^2/ell^2)^(D/2)
```

to reproduce the same observed variance `V*`.

Therefore one measured width cannot separately identify point disorder variance and correlation length. This is exact structural non-identifiability under the declared model.

## Arbitrary-dimensional two-scale inverse

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

The inverse is algebraically exact but model conditional.

## Conditioning and measurement design

For

```text
y_i = ln V_i
theta = (ln sigma_x^2, ln ell),
```

Jacobian row `i` is

```text
[1, g_i]

g_i = D [2 a_i^2/ell^2]/[1 + 2 a_i^2/ell^2].
```

The inverse is poorly conditioned when:

- the scales are equal or nearly equal;
- both probes are much smaller than `ell`;
- both probes are much larger than `ell`.

A useful pair samples opposite sides of the correlation length.

For `D=2`, `ell=5 um`:

```text
probe pair       condition number
5, 5.05 um       632.90
0.5, 50 um         2.683
2.5, 10 um         4.838
50, 500 um       1011.13
```

## Alternative top-hat kernels

For a normalized one-dimensional top-hat of length `L`,

```text
V_L = (2/L^2) int_0^L (L-h) C_x(h) dh.
```

Closed forms are implemented for Gaussian and exponential covariance and are verified against independent numerical quadrature. Their finite-scale curves differ, so covariance-family misspecification is a real inverse risk.

## HgCdTe gap propagation

For filtered composition variance `V_a`, a quadratic expansion gives

```text
E[Eg] ~= Eg(xbar,T) + 0.5 Eg_xx V_a
```

and

```text
Var(Eg) ~= Eg_x^2 V_a + 0.5 Eg_xx^2 V_a^2.
```

The variance expression is exact for a quadratic composition dependence and Gaussian composition.

For a cutoff `lambda_c=hc/E_c`,

```text
sigma_lambda ~= lambda_c sigma_E/|E_c|.
```

## Quantitative significance screen

Declared sensitivity assumptions:

```text
D                                  2
point composition sigma            0.005
correlation length                 5 um
local |dEg/dx|                     1.7191085 eV
reference cutoff                   10 um
```

Results:

```text
probe a        effective sigma_x     sigma_gap     sigma_cutoff
1 um           0.004811              8.271 meV     0.6671 um
5 um           0.002887              4.963 meV     0.4003 um
10 um          0.001667              2.865 meV     0.2311 um
100 um         0.0001767             0.304 meV     0.02450 um
```

The same declared microscopic field appears `27.2336x` narrower in standard deviation when probe sigma increases from `1 um` to `100 um`.

This is large enough to alter comparisons among micro-FTIR, wafer FTIR, PL, cutoff mapping, and pixel/device distributions. It is a sensitivity calculation, not a specimen calibration.

## Prior-art boundary

Established work includes:

- finite-aperture HgCdTe composition/thickness mapping;
- spatially resolved PL and transmission;
- apparent absorption tails generated by local-gap distributions;
- PL localization at composition fluctuations;
- effective-thickness-dependent detector cutoff;
- general random-field covariance filtering.

The candidate contribution is the combined HgCdTe spatial observation layer, exact information limits, scale-selection design, and quantitative device consequence. No novelty claim is frozen until the highest-value spatial-mapping papers are fully audited.

## Active files

```text
src/mct_research/spatial_disorder.py
src/mct_research/spatial_disorder_inference.py
tests/test_spatial_disorder.py
tests/test_spatial_disorder_inference.py
docs/derivations/010_scale_dependent_spatial_disorder.md
data/validation/spatial_disorder_theorem_extension.json
literature/notes/scale_dependent_disorder_prior_art.md
```

## Required next milestones

1. pass focused and complete Python 3.11/3.13 workflows;
2. complete full-text audit of the most relevant spatial-mapping papers;
3. propagate realistic measurement uncertainty through the two-scale inverse;
4. quantify covariance-family misspecification with three or more probe scales;
5. connect the spatial layer to Herrmann absorption without equating tail energy with microscopic variance;
6. connect it to mapped detector-cutoff statistics with explicit optical/electrical kernels;
7. build 4-6 theorem-centered figures rather than dashboards;
8. write a new equation-dense anonymous manuscript;
9. commit an anonymous review PDF only after the scientific significance gate passes.

## Explicitly unauthorized

- named manuscript or named PDF;
- cover letter or submission package;
- personal or commercial metadata in the manuscript path;
- treating the PR #194 draft as submission-ready;
- dashboard-style figure collections;
- claiming general covariance convolution as new mathematics;
- equating point composition variance, probe-averaged variance, Urbach energy, PL linewidth, and cutoff spread;
- inferring correlation length from sources without spatial covariance evidence;
- journal selection or DOI packaging before the scientific gate;
- requiring collaborators or new experiments;
- expensive first-principles work without a result-changing need.
