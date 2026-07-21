# Spatial-disorder band-edge program

**Program issue:** #195  
**Status:** specification only  
**Authorized stage:** Stage 1 — measurement-kernel-aware spatial disorder  
**Stage 2:** closed pending the gate in Section 14  
**Relationship to the flagship:** follow-on program; the merged distributional-observation manuscript remains scientifically frozen

## 1. Decision statement

The next research increment should resolve a specific missing variable in the present theory: spatial scale.

The current repository can propagate a scalar composition or gap distribution through absorption, detector-cutoff, carrier-filling, and structural-identifiability operators. It does not yet distinguish two specimens or fields having the same point variance but different correlation lengths, and it does not yet state how a finite optical, electrical, or depth kernel transforms the latent disorder before a reported edge is extracted.

Stage 1 will therefore treat the Cd fraction as a spatial random field and the instrument as a declared observation kernel. The first publication target is not a new bandgap law and not a microscopic disorder theory. It is a falsifiable, scale-dependent measurement theory for HgCdTe in which point disorder amplitude, correlation length, probe size, penetration depth, absorber thickness, and nonlinear edge extraction remain distinct.

## 2. Scientific question

Can controlled variation of measurement scale separate the point composition-disorder amplitude `sigma_x` from the spatial correlation length `xi`, and can one underlying HgCdTe field produce predictably different apparent edge widths under different measurement modalities?

The minimum non-identifiability to eliminate is

```text
large point variance + short correlation length
```

versus

```text
small point variance + long correlation length
```

when both yield the same variance after one measurement kernel.

## 3. Scope and claim boundary

### 3.1 Authorized claims

Stage 1 may establish, subject to derivation and tests:

1. exact variance filtering for declared covariance and measurement-kernel families;
2. structural and practical identifiability of disorder amplitude and correlation length from multiscale measurements;
3. controlled weak-disorder closures connecting filtered composition variance to filtered gap variance;
4. modality-specific forward predictions for the existing absorption-edge and detector-cutoff operators;
5. experimental designs that can falsify a stationary covariance family;
6. source-bounded estimates or bounds when raw maps and instrument kernels are available.

### 3.2 Claims explicitly outside Stage 1

Stage 1 must not claim:

- a universal HgCdTe covariance law;
- a universal mapping among composition variance, Urbach energy, PL linewidth, detector cutoff, and quasiparticle linewidth;
- that a nominal aperture equals the specimen-plane point-spread function;
- that optically inferred composition is independent evidence for an optical gap law;
- that local opposite-sign gap probability establishes mixed topological domains;
- that finite correlation length changes the Kane spectrum before a dedicated Stage 2 calculation;
- that replacing `sigma_x` by one effective scalar is exact for every nonlinear observation operator.

## 4. Latent-field contract

Let

```text
x(r) = x_bar + delta_x(r)
E[delta_x(r)] = 0
C_x(r, r') = E[delta_x(r) delta_x(r')]
```

The first implementation is stationary:

```text
C_x(r, r') = C_x(h),  h = r - r'
```

with point variance

```text
C_x(0) = sigma_x^2.
```

All lengths use SI units internally. Public constructors may accept documented units only through explicit conversion helpers. Covariance amplitude is dimensionless squared because Cd fraction is dimensionless.

A covariance model must declare:

- dimensionality;
- point variance;
- correlation-length convention;
- anisotropy axes or covariance tensor;
- smoothness convention;
- whether the model is stationary;
- whether a closed-form spectral density is available.

### 4.1 Gaussian covariance

The reference parameterization is

```text
C_x(h) = sigma_x^2 exp[-0.5 h^T Lambda^-1 h]
```

where `Lambda` is positive definite. The square roots of its eigenvalues are Gaussian correlation standard deviations. Along a principal axis, the covariance falls to `exp(-1/2)` at one declared correlation scale and to `exp(-1)` at `sqrt(2)` times that scale.

### 4.2 Exponential covariance

The reference isotropic form is

```text
C_x(h) = sigma_x^2 exp(-||h||/xi).
```

Here `xi` is the `1/e` correlation length. An anisotropic form replaces the Euclidean norm with a declared positive-definite metric.

### 4.3 Matérn covariance

Matérn models are permitted only with an explicit parameterization fixing variance, metric, smoothness `nu`, and correlation-length convention. Because multiple incompatible length conventions exist, no unqualified `xi` argument is allowed in the future API.

## 5. Measurement-kernel contract

For a normalized linear kernel `w(r)`,

```text
integral w(r) dr = 1
x_w = integral w(r) x(r) dr.
```

The exact filtered variance is

```text
Var[x_w] = double_integral w(r) w(r') C_x(r-r') dr dr'.
```

With Fourier convention

```text
W(k) = integral w(r) exp(-i k.r) dr
C_x(h) = integral S_x(k) exp(i k.h) dk/(2*pi)^d,
```

the equivalent spectral form is

```text
Var[x_w] = integral S_x(k) |W(k)|^2 dk/(2*pi)^d.
```

The implementation must test Parseval consistency between real-space and spectral routes.

A kernel must declare:

- specimen-plane normalization;
- dimensionality and support;
- lateral point-spread function;
- depth sensitivity;
- front- or back-side illumination where relevant;
- whether the kernel is measured, manufacturer-specified, inferred, or assumed;
- wavelength, temperature, numerical aperture, and confocal settings when they alter the kernel.

## 6. Exact Gaussian benchmark

For Gaussian covariance

```text
C_x(h) = sigma_x^2 exp[-0.5 h^T Lambda^-1 h]
```

and a normalized Gaussian kernel with covariance `Sigma_w`,

```text
w(r) = N(0, Sigma_w),
```

the exact result is

```text
Var[x_w]
  = sigma_x^2 det(I + 2 Sigma_w Lambda^-1)^(-1/2)
  = sigma_x^2 sqrt(det(Lambda)/det(Lambda + 2 Sigma_w)).
```

Required limits are

```text
Sigma_w -> 0      => Var[x_w] -> sigma_x^2
Lambda -> infinity => Var[x_w] -> sigma_x^2
probe >> correlation scale => self-averaging asymptote.
```

For an isotropic two-dimensional field and Gaussian probe standard deviation `s`,

```text
V_x(s) = sigma_x^2 / (1 + 2 s^2/xi^2).
```

The future numerical implementation must match the determinant expression to relative error below `1e-10` wherever the reference result is above numerical underflow and the involved matrices have condition number below the declared stable-domain limit.

## 7. Weak-disorder propagation to gap

For a local gap law `E_g(x,T)`, expand about `x_bar`:

```text
E_g(x,T) ~= E_g(x_bar,T)
          + E_x delta_x
          + 0.5 E_xx delta_x^2.
```

The first-order filtered gap variance is

```text
Var[E_g,w] ~= E_x^2 Var[x_w].
```

The dimensionless curvature diagnostic is

```text
chi_w = |E_xx| sqrt(Var[x_w]) / |E_x|.
```

A first-order closure is admissible only when a declared threshold on `chi_w` is satisfied and comparison against bounded quadrature shows acceptable error. The repository must not silently substitute `sigma_x,eff` into nonlinear operators without this audit.

For Gaussian covariance and kernel in the linear-gap regime,

```text
sigma_G,eff(s)
  ~= |E_x| sigma_x / sqrt(1 + 2 s^2/xi^2).
```

## 8. Noncommutation with nonlinear measurement operators

The filtered-variance identity is exact for a linear weighted field average. Optical and detector observables are generally nonlinear and must preserve operation order.

For lateral kernel `w_xy` and depth-dependent absorption,

```text
T_meas(E)
  = integral w_xy(r_xy)
      exp[-integral alpha(E, x(r_xy,z), ...) dz]
    d r_xy.
```

In general,

```text
T_meas(E)
  != exp[-d alpha(E, x_w, ...)].
```

Likewise, an extracted cutoff or tail parameter is not the kernel average of local cutoffs or local tail parameters.

Stage 1 therefore contains two distinct model levels:

1. **linear-kernel benchmark:** exact statistics of `x_w` and controlled propagation to `E_g,w`;
2. **modality forward operator:** apply local physics, depth integration, lateral intensity averaging, and reported-edge extraction in the physically correct order.

The scalar replacement `sigma_x -> sigma_x,eff` is a closure to test, not a universal identity.

## 9. Depth-kernel benchmarks

For a semi-infinite exponential sensitivity

```text
w(z) = a exp(-a z),  z >= 0,  a = 1/delta,
```

### 9.1 Exponential depth covariance

For

```text
C_x(dz) = sigma_x^2 exp(-|dz|/xi_z),
```

the exact ratio is

```text
Var[x_w]/sigma_x^2 = a xi_z/(1 + a xi_z).
```

### 9.2 Gaussian depth covariance

For

```text
C_x(dz) = sigma_x^2 exp[-dz^2/(2 xi_z^2)],
```

the exact ratio is

```text
Var[x_w]/sigma_x^2
  = sqrt(pi/2) a xi_z exp[(a xi_z)^2/2]
    erfc(a xi_z/sqrt(2)).
```

A finite-thickness implementation must reduce to these limits as thickness tends to infinity and must distinguish front-side from back-side sensitivity.

## 10. Multiscale identifiability

For the isotropic two-dimensional Gaussian benchmark,

```text
V_x(s) = sigma_x^2 xi^2/(xi^2 + 2 s^2).
```

For two distinct probe scales,

```text
R = V_x(s1)/V_x(s2)
  = (xi^2 + 2 s2^2)/(xi^2 + 2 s1^2),
```

so that

```text
xi^2 = 2 (s2^2 - R s1^2)/(R - 1).
```

### 10.1 Structural statements

- One scale identifies only one effective variance combination.
- Two noiseless distinct scales are structurally sufficient for `sigma_x^2` and `xi` under the declared covariance family.
- At least three scales are required to test rather than assume the two-parameter covariance family.
- Four or more logarithmically spaced scales are recommended for practical estimation and residual diagnostics.

### 10.2 Practical degeneracies

If every `s_i << xi`, then all measurements approach the point variance and correlation length is weakly constrained.

If every `s_i >> xi`, then

```text
V_x(s_i) ~= sigma_x^2 xi^2/(2 s_i^2),
```

and only the product `sigma_x^2 xi^2` is well constrained.

The experiment must therefore include scales spanning `s/xi = O(1)` or must report only bounds.

### 10.3 Fisher-information requirement

For observations `y_i` with covariance `Sigma_y` and model vector `mu(theta)`,

```text
F(theta) = J(theta)^T Sigma_y^-1 J(theta),
J_ij = partial mu_i / partial theta_j.
```

The future inference module must report singular values, parameter correlation, local condition number, and profile likelihood or an equivalent non-Gaussian diagnostic. A numerical optimizer returning a point estimate is not evidence of identifiability.

## 11. First falsifiable prediction

For the same specimen region, temperature, processing state, illumination geometry, depth sensitivity, and edge operator, the linear stationary Gaussian model predicts

```text
V_G(s) = V_G,0/(1 + 2 s^2/xi^2).
```

The simplest interpretation is falsified or shown incomplete when one of the following occurs outside uncertainty:

1. variance fails to decrease as the effective Gaussian probe radius increases;
2. three or more probe scales cannot be fit by one covariance family;
3. inferred `xi` changes materially with spectral fitting window after the local physics is held fixed;
4. front- and back-side measurements cannot be reconciled with one depth covariance and declared kernels;
5. coarse-graining a high-resolution map does not predict direct lower-resolution measurements on the same field.

A constant linewidth alone is not sufficient evidence for absent composition disorder because homogeneous, lifetime, defect, carrier, strain, and instrument contributions can dominate.

## 12. Validation hierarchy

### Level A — exact mathematics

- determinant benchmark;
- real-space versus spectral equivalence;
- exponential-depth and Gaussian-depth closed forms;
- point-probe, large-probe, infinite-correlation, and thin/thick limits.

### Level B — synthetic fields

- Gaussian random fields generated from known power spectra;
- direct convolution versus analytical variance;
- anisotropy recovery;
- finite-map and boundary-bias study;
- detrending sensitivity;
- noise and point-spread-function misspecification.

### Level C — source-bounded reconstruction

- digitized or native raw map with spatial coordinates;
- map provenance and processing state;
- reported or reconstructable specimen-plane PSF;
- controlled coarse-graining of one map;
- uncertainty and nonstationarity audit.

### Level D — cross-modality prediction

- same specimen region where feasible;
- absorption map and detector response first;
- PL and magneto-optical data only after their transport and selection kernels are specified.

No experimental correlation length may be claimed below Level C.

## 13. Data provenance schema

Every spatial dataset must record:

```text
specimen_id
wafer_or_layer_id
growth_method
processing_state
temperature
measurement_modality
raw_or_derived_quantity
x_coordinate
y_coordinate
z_coordinate_or_depth_support
pixel_pitch
nominal_aperture
specimen_plane_psf
psf_provenance
spectral_resolution
illumination_side
penetration_depth_model
fit_window
latent_gap_law
composition_calibration
uncertainty_model
detrending_method
missing_data_mask
source_citation
source_license_or_access_boundary
```

Derived composition maps must retain the gap law and optical model used to infer composition. Such maps cannot independently validate that same law without a circularity analysis.

## 14. Stage 2 gate: correlated random-mass Kane regime

Define the disorder energy scale `sigma_E`, Kane velocity `v_K`, and

```text
ell_K = 2 hbar v_K/sigma_E
kappa = xi/ell_K.
```

Stage 2 becomes eligible only when near-critical HgCdTe evidence independently establishes or tightly bounds both `sigma_E` and `xi` and one of the following holds:

1. `kappa = O(1)` over a credible uncertainty interval;
2. finite-correlation theory predicts a change above both `5%` and the best available experimental uncertainty in a declared observable;
3. the correlation model changes a scientific conclusion that the uncorrelated SCBA cannot answer.

Terminate before a real-space or full Kane calculation when:

- all credible bounds place `kappa < 0.1` or `kappa > 10` and a controlled asymptotic treatment answers the question;
- predicted finite-correlation corrections are below both `5%` and experimental uncertainty;
- correlation length is inferred only from the same optical observable being explained;
- no same-specimen or source-bounded near-critical dataset exists.

Even after the gate opens, the first Stage 2 model must be the smallest one capable of testing the decision-changing claim. Full 8-band real-space calculations are not the default starting point.

## 15. Proposed future module and API namespace

No executable module is authorized by this specification PR. The planned namespace is

```text
src/mct_research/spatial_disorder.py
```

with the following conceptual interfaces.

### 15.1 Covariance models

```python
class SpatialCovariance(Protocol):
    dimension: int
    variance: float
    def covariance(self, displacement): ...
    def spectral_density(self, wavevector): ...

@dataclass(frozen=True)
class GaussianCovariance: ...

@dataclass(frozen=True)
class ExponentialCovariance: ...

@dataclass(frozen=True)
class MaternCovariance: ...
```

### 15.2 Measurement kernels

```python
class MeasurementKernel(Protocol):
    dimension: int
    def real_space(self, position): ...
    def fourier(self, wavevector): ...
    def normalization(self): ...

@dataclass(frozen=True)
class GaussianKernel: ...

@dataclass(frozen=True)
class BoxKernel: ...

@dataclass(frozen=True)
class ExponentialDepthKernel: ...

@dataclass(frozen=True)
class CompositeKernel: ...
```

### 15.3 Core functions

```python
effective_variance(covariance, kernel, *, method="auto")
gaussian_gaussian_effective_variance(covariance, kernel)
propagate_gap_moments(gap_model, x_mean, temperature, filtered_variance)
multiscale_variance_curve(covariance, kernels)
identifiability_report(model, design, observation_covariance)
coarse_grain_map(values, coordinates, kernel, boundary_policy)
```

The API must return values plus method, normalization checks, numerical error estimates, units, and provenance. Silent clipping of non-positive covariance matrices or negative spectral densities is prohibited.

## 16. Test plan for implementation PRs

The first executable PR must include tests for:

1. Gaussian determinant identity in 1D, 2D, and 3D;
2. rotated anisotropic covariance and kernel tensors;
3. real-space and Fourier agreement;
4. exponential-depth exact result;
5. Gaussian-depth exact result;
6. point-probe and large-probe asymptotes;
7. two-scale inversion recovery;
8. rank loss in both `s << xi` and `s >> xi` regimes;
9. failure on non-positive covariance tensors;
10. normalization failure for malformed kernels;
11. finite-grid convergence and boundary bias;
12. regression that existing scalar distributional APIs remain unchanged.

## 17. Implementation issue sequence

After this specification merges, implementation should proceed through separate issues and PRs:

1. **Covariance core and exact Gaussian benchmark**  
   Implement normalized covariance/kernel contracts and analytical tests only.
2. **Depth kernels and finite slabs**  
   Add front/back illumination, penetration-depth weighting, and exact semi-infinite limits.
3. **Multiscale recoverability**  
   Add two-scale inversion, Fisher information, profile diagnostics, and experiment-design maps.
4. **Absorption-edge coupling**  
   Preserve nonlinear operation order and quantify the error of the scalar effective-width closure.
5. **Detector-cutoff coupling**  
   Propagate the same field through effective thickness and response extraction.
6. **Source-bounded map validation**  
   Reconstruct or ingest a spatial dataset, audit PSF and circularity, and perform controlled coarse-graining.
7. **Stage 1 publication decision**  
   Decide analytical methods paper, source-bounded HgCdTe result, or terminate for insufficient evidence.
8. **Formal Stage 2 gate**  
   Compute `kappa` bounds and record proceed/terminate before any correlated Kane calculation.

Each PR must close one scientific risk and preserve the frozen flagship manuscript.

## 18. Completion criteria for Stage 1

Stage 1 is complete when the repository contains:

- a normalized covariance and kernel implementation;
- exact analytical validation;
- structural and practical identifiability results;
- one falsifiable multiscale measurement design;
- an operation-order-correct absorption or detector prediction;
- a source-bounded validation result or an explicit no-data termination record;
- a publication decision;
- a formal Stage 2 proceed/terminate record.

The program should terminate early if scale dependence cannot be distinguished from instrument uncertainty, nonstationarity, or other broadening mechanisms with available data.