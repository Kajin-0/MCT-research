# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #196  
**Active milestone:** exact scale-dependent spatial-disorder theorem  
**Execution mode:** independent, public-data-first, analytical-first, anonymous-only

This is the sole controlling research ledger. `research/active_progress.md` remains retired.

## Superseded manuscript state

The merged PR #194 manuscript and SST packaging are scientifically superseded.

The superseded draft dispersed attention across multiple sensitivity studies and did not develop one result deeply enough for submission. It is not submission-ready and must not be cited as a finished paper.

The following are removed on the active branch:

- named manuscript source and PDF;
- anonymous superseded manuscript source and PDF;
- cover letter;
- personal, affiliation, correspondence, and commercial-interest metadata;
- dashboard-style submission figures;
- named/anonymous SST bundle builders and tests;
- submission packaging workflow.

All future manuscript artifacts are anonymous only.

## Active scientific question

> How does the spatial correlation structure of HgCdTe composition disorder combine with a finite measurement kernel to determine the apparent band-edge width, and what measurement scales are required to recover microscopic disorder amplitude and correlation length?

The active chain is

```text
microscopic composition random field
-> spatial covariance / power spectrum
-> declared measurement kernel
-> probe-averaged composition distribution
-> signed HgCdTe gap distribution
-> optical or detector observation operator
-> reported width or cutoff spread
```

## Exact general operator

For a stationary composition field with covariance `C_x` and normalized measurement kernel `w_a`,

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

A finite measurement reports a filtered covariance or power-spectrum integral, not the microscopic point variance `C_x(0)`.

## Exact Gaussian theorem

For

```text
C_x(h) = sigma_x^2 exp[-|h|^2/(2 ell^2)]
```

and a normalized `D`-dimensional Gaussian probe with coordinate standard deviation `a`,

```text
Var(X_a)
=
sigma_x^2 (1 + 2 a^2/ell^2)^(-D/2).
```

The standard deviation is

```text
sigma_x,a
=
sigma_x (1 + 2 a^2/ell^2)^(-D/4).
```

The general convolution identity is established random-field mathematics. The project-specific contribution must be the HgCdTe observation consequence, exact inverse design, quantitative magnitude, and source-grounded measurement prescription.

## Exact one-scale no-go result

At one declared probe scale `a*`, every positive correlation length `ell` can be paired with

```text
sigma_x^2(ell)
=
V* (1 + 2 a*^2/ell^2)^(D/2)
```

to produce the same observed variance `V*`.

Therefore one measured width at one probe scale cannot separately identify microscopic disorder amplitude and correlation length. This is exact structural non-identifiability under the declared model, not a noise or optimization failure.

## Exact two-scale inverse

For distinct scales `a1` and `a2`, define

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

The inverse is algebraically exact but can be poorly conditioned.

For logarithmic outputs and parameters,

```text
y_i = ln V_i
theta = (ln sigma_x^2, ln ell)
```

Jacobian row `i` is

```text
(1, g_i)

g_i = D [2 a_i^2/ell^2]/[1 + 2 a_i^2/ell^2].
```

The inverse is singular for equal scales and poorly conditioned when both probes are much smaller than `ell` or both are much larger than `ell`. Useful scale pairs straddle the correlation length.

## Exact top-hat results

For a normalized one-dimensional top-hat window of length `L`,

```text
V_L = (2/L^2) int_0^L (L-h) C_x(h) dh.
```

Gaussian covariance gives

```text
V_L,G
=
(2 sigma_x^2/L^2)
[
L ell sqrt(pi/2) erf(L/(sqrt(2) ell))
- ell^2 (1 - exp(-L^2/(2 ell^2)))
].
```

Exponential covariance gives

```text
V_L,E
=
(2 sigma_x^2/L^2)
[
L ell - ell^2 (1 - exp(-L/ell))
].
```

These exact alternatives make the covariance-model dependence explicit.

## Propagation through a signed gap law

For probe-averaged composition variance `V_a`, a quadratic expansion gives

```text
E[Eg]
~= Eg(xbar,T) + 0.5 Eg,xx V_a
```

and

```text
Var(Eg)
~= Eg,x^2 V_a + 0.5 Eg,xx^2 V_a^2.
```

The variance expression is exact for a quadratic composition dependence and Gaussian probe-averaged composition.

## First quantitative significance case

Declared sensitivity assumptions:

```text
D                                  2
microscopic sigma_x                0.005
correlation length                 5 um
local gap slope                    1.7191085 eV/composition
reference cutoff                   10 um
```

Exact Gaussian-probe results:

```text
probe a        sigma_x,a        sigma_gap
1 um           0.004811         8.271 meV
5 um           0.002887         4.963 meV
10 um          0.001667         2.865 meV
100 um         0.0001767        0.304 meV
```

The same microscopic field appears `27.23x` narrower in standard deviation between 1 and 100 um probe scales. The corresponding first-order cutoff spread around 10 um changes from approximately `0.667 um` to `0.0245 um`.

This is large enough to alter comparisons among micro-FTIR, wafer FTIR, PL, cutoff mapping, and pixel/device distributions. It remains a sensitivity result, not a specimen calibration.

## Source and prior-art position

Established HgCdTe work already shows:

- composition and thickness mapping by IR microscopy with adjustable apertures down to tens of micrometres;
- spatially resolved PL and transmission mapping;
- apparent absorption tails generated by distributions of local gap energies;
- localization and PL shifts associated with compositional fluctuations;
- detector cutoff dependence on effective absorber thickness.

The active novelty audit asks whether prior work has already derived and applied the explicit probe-scale covariance law, one-scale no-go result, and two-scale inversion to HgCdTe band-edge observables. No novelty claim is authorized until that audit is complete.

## Active files

```text
src/mct_research/spatial_disorder.py
tests/test_spatial_disorder.py
docs/derivations/010_scale_dependent_spatial_disorder.md
data/validation/scale_dependent_disorder_reference.json
.github/workflows/scale-dependent-disorder.yml
```

## Required next milestones

1. pass the focused and complete Python 3.11/3.13 workflow matrix;
2. complete a targeted primary-source prior-art audit;
3. add verified numerical covariance quadrature and Monte Carlo cross-checks;
4. add Matérn covariance support and model-discrimination analysis;
5. connect the spatial operator to the Herrmann absorption convolution without equating tail energy with microscopic variance;
6. connect the operator to mapped detector-cutoff statistics with explicit optical/electrical kernels;
7. quantify whether two experimentally realistic probe scales can recover `ell` under plausible uncertainty;
8. write a new equation-dense anonymous manuscript around this theorem hierarchy;
9. commit an anonymous review PDF only after the scientific significance gate passes.

## Explicitly unauthorized

- named manuscript or named PDF;
- cover letter or journal submission package;
- author, affiliation, correspondence, ORCID, postal, telephone, or commercial metadata in the anonymous manuscript path;
- treating the superseded PR #194 draft as submission-ready;
- dashboard-style figure collections;
- claiming the general covariance convolution as new probability theory;
- equating microscopic composition variance, probe-averaged variance, Urbach energy, PL linewidth, and cutoff spread without a forward operator;
- inferring a specimen correlation length from Herrmann, Chang, Dingrong, or Ivanov-Omskii without spatially resolved data;
- journal selection or DOI packaging before the scientific gate;
- collaborators or new experiments as a prerequisite;
- expensive first-principles work without a result-changing analytical need.
