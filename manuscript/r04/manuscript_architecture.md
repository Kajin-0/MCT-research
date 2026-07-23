# R04 manuscript architecture

**Status:** architecture only; not full manuscript prose  
**Issue:** #330  
**Authorization:** `AUTHORIZE_RESTRICTED_MANUSCRIPT` from #327 / PR #329  
**Architecture decision:** `ARCHITECTURE_READY_FOR_DRAFTING`

## Provisional title

> What Finite-Resolution HgCdTe Maps Can Identify: Measurement Kernels,
> Calibration, and Correlated-Raster Information

## Central claim

> Finite-resolution HgCdTe maps identify a kernel-filtered and
> calibration-limited spatial field whose recoverable variance, correlation
> scale, covariance-family closure, and effective information require explicit
> treatment of the measurement kernel, finite field of view, and same-raster
> cross-scale dependence.

This is an integrated measurement-information claim. It is not a claim that
finite-aperture mapping, Gaussian filtering, quadratic-form moments, Fisher
information, or optimal design are individually new.

## Paper logic in one line

```text
finite kernel
-> scale-dependent apparent variance
-> limited recoverability and calibration floor
-> need for third-scale family closure
-> finite-map and same-raster information loss
-> restricted real-map demonstration
-> reporting and experiment-design rules
```

## Main-text ceiling

```text
main result groups     4
main figures           4
main tables            0 preferred; 1 claim-boundary table maximum
new scientific result  none
new data search         none
R05                     excluded
```

The paper should remain approximately theorem-centered. Instrument stress grids,
operation-order details, and allocation tables are supporting material rather
than separate main-text stories.

---

## Abstract

### Purpose

State the measurement problem, integrated method, minimum analytical results,
restricted real-map demonstration, hard limitation, and practical consequence.

### Inputs

- authorized one-sentence claim;
- `manuscript/r04/abstract_plan.json`;
- immutable CdSeTe result;
- public HgCdTe data-stop record.

### Outputs

A six-function abstract with exactly:

```text
problem
method
analytical result
real-map demonstration
limitation
practical consequence
```

### Mandatory content

- finite-resolution HgCdTe map values are kernel dependent;
- one scale does not identify both variance and correlation scale;
- a third informative scale supplies the first family-closure test;
- common scale calibration limits absolute correlation-length recovery;
- numerical scales from one raster are dependent;
- the CdSeTe example is a cross-material method demonstration;
- no HgCdTe specimen covariance family or physical correlation length is
  reported.

### Prohibited content

- “experimentally validated in HgCdTe”;
- “source-native hyperspectral CdSeTe cube”;
- “composition map” for Figure 3e source data;
- “independent held-out validation” for the numerically smoothed one-pixel
  scale;
- selection of Matérn `nu=3/2` as a material law.

---

## 1. Introduction and prior-art boundary

### Section purpose

Define the engineering problem and narrow the contribution before any theorem is
presented.

### Required logic

1. HgCdTe uniformity is often assessed with finite-aperture transmission, PL,
   or related spatial mapping.
2. The reported field depends on aperture, optical response, pixel/bin
   integration, depth weighting, preprocessing, and observation operator.
3. Finite-aperture and spatially resolved mapping are established prior art.
4. Existing audited full texts do not supply the closed multiscale covariance,
   calibration, finite-map, and same-raster information hierarchy developed in
   R04.
5. The paper asks what such maps can identify, not how to build the first map.

### Source inputs

- `literature/notes/finite_aperture_hgcdte_mapping_audit.md`;
- Chang et al. 2005 full-text audit;
- Furstenberg et al. 2005 full-text audit;
- Ruzhevich 2024 abstract-bounded record;
- public-data recovery decision from PR #308.

### Candidate topic sentences

- “A spatial map is not a pointwise material field when each reported value is
  formed through a finite measurement kernel.”
- “The unresolved question is therefore not whether HgCdTe can be mapped, but
  which properties of an underlying spatial field remain identifiable from
  finite-resolution observations.”

### Section output

A precise contribution paragraph containing:

```text
established prior art
established mathematics
candidate integrated R04 contribution
restricted validation state
paper roadmap
```

### Claim boundary

Do not claim exhaustive novelty. Use “candidate distinct contribution,”
“integrated framework,” or narrower wording until the final pre-submission claim
audit.

### Figure support

Figure 1a only. The panel must label finite-aperture mapping as established
context.

---

## 2. Measurement model and kernel-filtered covariance

### Section purpose

Define the latent spatial field, complete observation kernel, and filtered
covariance before discussing inference.

### Minimum definitions

Let `x(r)` be a stationary latent field with covariance `C_x(Delta r)`. A
normalized linear observation is

```text
X_w = integral w(r) x(r) dr
```

or its lateral/depth extension. Then

```text
Var(X_w) = double integral w(r) w(r') C_x(r-r') dr dr'.
```

For Gaussian covariance and Gaussian probe in the isotropic two-dimensional
benchmark:

```text
V(s) = A / (1 + 2 s^2 / xi^2).
```

### Instrument bridge

State that a practical kernel may combine:

```text
optical excitation/collection PSF
pixel or scan-bin integration
depth weighting
```

The composite-kernel stress-grid result belongs in Appendix A. The main text
needs only enough evidence to justify retaining the kernel explicitly.

### Observation-operator boundary

Linear kernel filtering does not by itself resolve nonlinear transmission,
cutoff, PL fitting, or composition-conversion operators. Those effects are
acknowledged and placed in Appendix A / Supplementary Note S1.

### Section output

- the exact filtered-variance definition;
- the Gaussian benchmark used for analytical identifiability;
- an explicit statement that Gaussian covariance is a benchmark family, not a
  universal HgCdTe law.

### Figure support

Figure 1a and 1b.

### Claim boundary

Do not present the composite representative instrument as a universal device
model or substitute nominal pitch for a measured PSF.

---

## 3. Recoverability and absolute scale calibration

### Section purpose

Show the minimum information content of one and two scales and the distinct role
of absolute calibration.

### Required results

#### 3.1 One-scale non-identifiability

One value `V(s)` contains one constraint on `A` and `xi`; both cannot be
identified without additional information.

#### 3.2 Two-scale Gaussian recovery

Two distinct admissible scales recover the two Gaussian benchmark parameters in
an exact noiseless model. This is parameter estimation, not family validation.

#### 3.3 Calibration confounding

Use the sensitivity identity

```text
partial V / partial log s = - partial V / partial log xi
```

to show that a common multiplicative scale error is confounded with absolute
correlation length. State the variance decomposition only under its declared
conditions.

#### 3.4 Nonlinear posterior qualification

Briefly state that the exact convolution result extends beyond local Fisher
analysis under translation-invariant absolute-length priors, while active
bounded priors can break factorization.

### Section output

A compact hierarchy:

```text
one scale        insufficient for A and xi
two scales       estimate Gaussian benchmark
relative scales  control relative xi information
absolute scale   imposes absolute xi floor
repeats          cannot remove common calibration error
```

### Figure support

Figure 1b and 1c.

### Claim boundary

No specimen-specific `A` or `xi` is reported. The plotted posteriors are
controlled analytical/synthetic examples.

---

## 4. Three-scale family closure and misspecification

### Section purpose

Separate estimating a chosen covariance model from testing whether that family
is compatible with the scale dependence.

### Required results

#### 4.1 Reciprocal linearity

For the Gaussian benchmark:

```text
1/V(s) = 1/A + [2/(A xi^2)] s^2.
```

Two points determine a line. A third provides the first exact closure residual.

#### 4.2 Supported alternatives

Use half-integer Matérn alternatives only as controlled families demonstrating
that different covariance shapes can produce different scale curves.

#### 4.3 Wrong-family parameter drift

Show that forcing Matérn truth through a Gaussian inverse produces pairwise
variation in fitted `A` and `xi` and a global surrogate whose meaning depends on
scale design and loss.

#### 4.4 Fit-convention boundary

State that weighted log-variance and reciprocal-variance fitting can yield
meaningfully different parameters under misspecification even if a coarse
resolved/unresolved classification remains stable.

### Section output

A rule:

> Report Gaussian parameters only after a declared closure test and with the
> scale grid and fitting loss stated explicitly.

### Figure support

Figure 2a–2d.

### Claim boundary

- failure to reject Gaussian is not proof of Gaussian covariance;
- pairwise drift is not a confidence interval;
- synthetic Matérn calculations do not identify a real HgCdTe family.

---

## 5. Finite-map information and same-raster covariance

### Section purpose

Show why map dimensions and scale count do not equal independent information.

### Required definitions

For a Gaussian map vector `y ~ N(0,C)` with centering matrix `P`:

```text
E[s_naive^2] = tr(P C)/(n-1)
Var(s_naive^2) = 2 tr[(P C)^2]/(n-1)^2.
```

For two scales observed at common centers:

```text
Cov(q_i,q_j) = 2 tr(P C_ij P C_ji)/(n-1)^2.
```

### Required results

#### 5.1 Effective information

Dense resampling at fixed field of view can increase nominal pixels while adding
negligible map-mean information.

#### 5.2 Naive variance bias

Mean subtraction on a correlated finite map can suppress the ordinary sample
variance relative to the marginal filtered variance.

#### 5.3 Same-raster dependence

Variance estimates from related scales can have high cross-correlation. The
full covariance, not an independent-scale diagonal approximation, must enter
inference.

#### 5.4 Controlled uncertainty consequence

Use the existing controlled covariance-volume result as an illustration, while
stating that the numerical factor is design specific.

### Section output

A second rule:

> Count independent realizations or covariance-weighted information, not nominal
> pixels or numerical resolutions.

### Figure support

Figure 3a–3d.

### Claim boundary

- moment-matched effective degrees of freedom are not exact general chi-square
  degrees of freedom;
- delta-method log covariance is not exact joint log-normal behavior;
- deterministic bias correction does not add information.

---

## 6. Restricted CdSeTe real-map demonstration

### Section purpose

Show that the R04 workflow detects the predicted measurement-scale and
finite-field issues on one public semiconductor observation field, without
claiming HgCdTe validation.

### Source contract

```text
source              Bowman et al. 2024
material            CdSe_xTe_1-x thin film
field               Gaussian-fitted PL peak wavelength
map                  24 x 24
coordinates          0 to 12.545 micrometres on each axis
native sample PSF    unmeasured and unbounded
raw per-pixel cube   unavailable in public archive
```

### Frozen protocol

```text
added sigma pixels   [0, 0.5, 1, 2, 4]
primary boundary     reflect
training scales      [0, 0.5, 2, 4]
held-out scale       1 pixel
central crop         16 x 16
```

### Main results

1. Variance falls from `13.7373 nm^2` to `1.54435 nm^2`, retaining `11.24%` at
   four added pixels.
2. The descriptive Matérn `nu=3/2` fit has the smallest frozen residual, but this
   is not family identification.
3. Same-raster low-scale correlations are near one under the fitted descriptive
   Gaussian model.
4. Boundary and crop changes reach approximately `72.7%`, larger than the
   descriptive family separation.
5. A phase-randomized surrogate preserves the periodic smoothing curve, showing
   the role of power spectrum and finite nonperiodic boundary interaction.

### Section output

A restricted demonstration statement:

> The real map reproduces the scale suppression, shared-raster dependence, and
> finite-field sensitivity anticipated by the analytical framework; it does not
> validate HgCdTe material covariance or yield a physical correlation length.

### Figure support

Figure 4a–4d. Full covariance matrix and phase-randomized control move to
Supplementary Figure S4.

### Claim boundary

Use “PL peak-wavelength observation field” throughout. Do not call the field
composition, intrinsic gap, or an HgCdTe analogue that validates material
physics.

---

## 7. Measurement-design consequences

### Section purpose

Translate the four result groups into a minimal reporting and design protocol.

### Main-text requirements

A credible multiscale study should report:

1. measured or bounded lateral PSF and pixel/bin integration;
2. depth weighting or an explicit statement that it is negligible;
3. at least three informative calibrated scales for family closure;
4. common and relative scale-calibration covariance;
5. registered sample-center geometry;
6. within-map and cross-scale covariance or justified independent separation;
7. independent-map or covariance-weighted information counts;
8. predeclared field of view, edge convention, detrending, and stopping
   threshold;
9. observation-operator and fitting definitions;
10. the scale grid and fitting loss used for reported parameters.

### Allocation result placement

The endpoint precision theorem and interior-scale falsification compromise are
summarized in one paragraph. Numerical allocation tables go to Appendix B or
Supplementary Figure S2.

### Section output

A compact checklist or one-column boxed protocol, not a fifth figure.

### Claim boundary

No universal physical probe sizes, pixel pitch, repeat count, or scan pattern are
prescribed.

---

## 8. Limitations

### Section purpose

State every blocked inference before the discussion can be read as a material
validation claim.

### Mandatory limitations

- no qualifying public source-native HgCdTe multiresolution package was found
  under the declared public-only audit;
- private or unindexed data may exist;
- no specimen-specific HgCdTe `A`, `xi`, or covariance family is reported;
- the CdSeTe native sample-plane kernel is unmeasured;
- added numerical sigma is not the native effective PSF;
- PL peak wavelength is not composition;
- numerical scales from one field are dependent;
- model-conditioned Gaussian covariance is not empirical repeat covariance;
- the exact finite-map moments rely on joint Gaussian assumptions;
- the representative instrument and covariance families are not universal;
- no R05 random-mass or topological conclusion is included.

### Section output

An explicit unsupported-claims box matching `claim_ledger.json` and the
manuscript authorization record.

---

## 9. Discussion and conclusion

### Section purpose

Return to the engineering question: what can a finite-resolution map support?

### Required synthesis

- Point variance and correlation scale are not directly observable at one
  resolution.
- Absolute length inference is only as good as common scale calibration.
- Two scales estimate a selected two-parameter model; a third begins family
  testing.
- Finite field of view and same-raster dependence can dominate nominal sample
  count.
- Real-map edge and crop sensitivity can exceed family differences.
- The practical output is a measurement and reporting framework, not a
  specimen-specific material law.

### Candidate final sentence function

End with the decision rule: multiresolution maps should be interpreted through
calibrated kernels and full covariance before microscopic disorder parameters
are reported.

### Claim boundary

Do not end with a promise of HgCdTe validation, a new mechanism, or R05 work.

---

## Appendices and supplementary placement

### Appendix A — Instrument and observation operators

- elliptical optical PSF, pixel/bin integration, finite-depth exponential;
- moment-matched Gaussian error and stress grid;
- transmission and cutoff operation-order results;
- source-specific observation-operator cautions.

### Appendix B — Measurement allocation

- endpoint D-optimal theorem;
- interior-scale efficiency/falsification compromise;
- common scale-calibration floor;
- no universal allocation prescription.

### Appendix C — Derivations and numerical implementation

- determinant form of Gaussian filtering;
- Fisher and sensitivity expressions;
- finite-map quadratic-form moments;
- same-raster cross-scale covariance;
- numerical tolerances and reproducibility contract.

### Supplementary Figure S1

Composite-kernel stress grid.

### Supplementary Figure S2

Allocation results.

### Supplementary Figure S3

Joint instrument/family/fit/operator identifiability envelope.

### Supplementary Figure S4

Full CdSeTe covariance matrix, edge-mode curves, crop curves, and phase-randomized
control.

---

## Citation-role map

| Citation role | Required source class | Manuscript use |
|---|---|---|
| Finite-aperture HgCdTe transmission mapping | Primary HgCdTe mapping paper | Establish prior art and model-conditioned inversion boundary |
| Spatially resolved HgCdTe PL/transmission | Primary HgCdTe PL/transmission paper | Establish prior art and excitation/collection/optical-path ambiguities |
| Source-specific optical observation operators | Primary HgCdTe absorption, transmission, PL, and cutoff papers | Prevent latent-field and measured-observable conflation |
| Gaussian random fields and linear filtering | Standard primary texts or canonical references | Attribute established covariance-filtering mathematics |
| Gaussian quadratic-form moments | Standard statistical references | Attribute exact mean/variance/covariance identities |
| Fisher information and optimal design | Canonical design references | Attribute established design mathematics |
| Matérn covariance families | Canonical spatial-statistics references | Define controlled alternative families |
| CdSeTe article and dataset | Bowman et al. article plus Zenodo record | Attribute the restricted real-map field and reuse license |

Full bibliography selection and formatting belong to the drafting tranche. No
citation role in this architecture constitutes an exhaustive novelty search.

---

## Drafting order

Draft sections in this sequence to preserve claim control:

```text
2 measurement model
3 recoverability and calibration
4 closure and misspecification
5 finite-map information
6 real-map demonstration
8 limitations
1 introduction
7 design consequences
9 discussion and conclusion
abstract last
```

The introduction and abstract should not be drafted first because their claim
language must be constrained by the completed technical and limitations
sections.

## Architecture decision

```text
ARCHITECTURE_READY_FOR_DRAFTING
```

The authorized results form one coherent theorem-to-measurement-design argument
under the four-result and four-figure ceiling. Full section drafting may begin,
but submission remains prohibited until a separate final claim audit.
