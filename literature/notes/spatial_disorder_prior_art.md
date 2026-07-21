# Prior-art and novelty matrix for spatial-disorder band-edge measurements

**Program issue:** #195  
**Audit date:** 2026-07-21  
**Purpose:** distinguish established mathematics and HgCdTe results from the proposed repository contribution before implementation begins

## 1. Audit rule

A claim is not treated as novel merely because the repository has not implemented it. The relevant comparison is against:

1. generic random-field and signal-processing theory;
2. spatially resolved HgCdTe measurement literature;
3. HgCdTe alloy-disorder and band-edge literature;
4. random-mass Kane or Dirac disorder literature;
5. the repository's already merged scalar distributional-observation work.

Every proposed claim is labeled as one of:

- **established** — directly present in prior art or standard mathematics;
- **new combination** — established pieces assembled into an HgCdTe-specific measurement theory not located as one existing result;
- **potentially novel** — plausible novelty target requiring a broader search and a completed technical result;
- **not authorized** — unsupported or contradicted by current evidence.

## 2. Primary source set

### P1 — Chang et al. 2005: infrared microscope mapping

Y. Chang, G. Badano, E. Jiang, J. W. Garland, J. Zhao, C. H. Grein, and S. Sivananthan, “Composition and thickness distribution of HgCdTe molecular beam epitaxy wafers by infrared microscope mapping,” *Journal of Crystal Growth* 277, 78–84 (2005).  
DOI: `10.1016/j.jcrysgro.2005.01.051`

Source-established:

- transmission microscopy plus automated fitting can produce spatial maps of inferred HgCdTe composition and thickness;
- one reported CdZnTe-substrate map had mean composition `x=0.2182` and standard deviation `0.0006`;
- inferred composition is obtained from the intrinsic absorption edge through an adopted gap relation;
- thickness is inferred from interference structure;
- the method can use finite adjustable apertures and is intended for wafer-uniformity characterization.

Limitations for this program:

- the composition map is not independent of the optical model and gap calibration;
- nominal aperture is not automatically a complete specimen-plane PSF;
- wafer-scale gradients and corner effects violate simple stationarity;
- the paper does not invert point variance and correlation length from multiple controlled kernels.

### P2 — Phillips et al. 2003: detector-scale infrared spectromicroscopy

J. D. Phillips, K. Moazzami, J. Kim, D. D. Edwall, D. L. Lee, and J. M. Arias, “Uniformity of optical absorption in HgCdTe epilayer measured by infrared spectromicroscopy,” *Applied Physics Letters* 83, 3701–3703 (2003).  
DOI: `10.1063/1.1625776`

Source-established:

- spatial absorption spectra were measured with a reported `9 micrometre` infrared beam;
- line scans and area maps were used to quantify detector-scale variation;
- the reported standard deviation in absorption near turn-on was below `3%` for the studied material;
- extracted composition standard deviation was reported near `3e-4` under the source model.

Limitations for this program:

- one beam scale does not separate disorder amplitude from correlation length;
- extracted composition remains conditioned on the optical inversion;
- the source does not supply a multiscale covariance inversion.

### P3 — Herrmann et al. 1992: Gaussian gap broadening and multimodal edges

K. H. Herrmann, K.-P. Möllmann, and J. W. Tomm, “Broadening Mechanisms Near the E0 Transition in Narrow-Gap Hg1-xCdxTe (0.2 < x < 0.6),” *Journal of Crystal Growth* 117, 758–762 (1992).  
DOI: `10.1016/0022-0248(92)90851-9`

Source-established:

- a Gaussian-like gap distribution can produce an approximately exponential absorption tail over a relevant interval;
- absorption, photoconductive, and luminescence observables contain distinct broadening contributions;
- alloy, temperature, shallow-level, and defect contributions cannot be universally collapsed into one width.

Limitations for this program:

- the distribution is scalar rather than a measured spatial covariance field;
- no explicit probe-size or penetration-depth inversion is given;
- the result does not establish a universal map from spatial composition covariance to Urbach energy.

### P4 — Chang et al. 2007: absorption and detector-cutoff observation operators

Y. Chang et al., “Absorption of Narrow-Gap HgCdTe Near the Band Edge Including Nonparabolicity and the Urbach Tail,” *Journal of Electronic Materials* 36, 1000–1006 (2007).  
DOI: `10.1007/s11664-007-0162-0`

Source-established:

- near-edge absorption requires a model including nonparabolicity and an Urbach branch in the stated regime;
- detector `50%` cutoff depends on effective absorber thickness and is not identical to a material gap;
- transmissivity and photoconductivity can be measured at the same specimen location.

Limitations for this program:

- the source does not introduce spatial covariance or measurement-kernel inversion;
- fitted tail parameters are source- and specimen-conditioned;
- lateral averaging and depth sensitivity are not formulated as a general random-field operator.

### P5 — Chen et al. 2023: band-edge-transition PL mapping

X. Chen, M. Wang, L. Zhu, H. Xie, L. Chen, and J. Shao, “Mid-infrared modulated photoluminescence mapping to investigate in-plane distributions of bandedge transitions in As-doped HgCdTe,” *Applied Physics Letters* 123, 151105 (2023).  
DOI: `10.1063/5.0164195`

Source-established:

- modulated mid-infrared PL can map in-plane variation of band-edge-related transitions in As-doped HgCdTe;
- spatial nonuniformity can be relevant to array performance.

Limitations for this program:

- a PL map includes excitation, collection, recombination, diffusion, defect, and carrier-distribution kernels;
- a PL transition map is not a direct composition map;
- this source does not establish the proposed multiscale covariance inversion.

### P6 — Sobieski et al. 2024: depth composition oscillations and annealing

J. Sobieski et al., “Impact of Residual Compositional Inhomogeneities on the MCT Material Properties for IR Detectors,” *Sensors* 24, 2837 (2024).  
DOI: `10.3390/s24092837`

Source-established:

- interdiffused-multilayer MOCVD HgCdTe can retain depth composition oscillations with a characteristic growth-period scale;
- post-growth annealing can reduce those oscillations;
- electrical, lifetime, and responsivity properties change with processing.

Limitations for this program:

- the observed profile is nonstationary and process-periodic rather than a generic stationary random field;
- SIMS depth response must be treated as a convolution kernel;
- annealing changes multiple material variables, so improved response cannot be attributed only to reduced composition variance.

### P7 — Teppe et al. 2016: near-critical Kane regime

F. Teppe et al., “Temperature-Driven Massless Kane Fermions in HgCdTe Crystals,” *Nature Communications* 7, 12576 (2016).  
DOI: `10.1038/ncomms12576`

Source-established:

- the inferred Kane mass changes sign as temperature tunes a near-critical HgCdTe crystal through the inverted/normal transition;
- a characteristic Kane velocity near `1.07e6 m/s` is reported over the studied range;
- inherent Cd-composition fluctuations are identified as an obstacle to fine tuning by composition.

Limitations for this program:

- no specimen-resolved composition covariance is supplied;
- nominal composition is not a local field measurement;
- local sign probability does not by itself determine a bulk topological invariant.

### P8 — Krishtopenko, Antezza, and Teppe 2022: uncorrelated HgCdTe disorder

S. S. Krishtopenko, M. Antezza, and F. Teppe, “Disorder-induced topological phase transition in HgCdTe crystals,” *Physical Review B* 106, 115203 (2022).  
DOI: `10.1103/PhysRevB.106.115203`

Source-established:

- an HgCdTe Kane model with self-consistent Born approximation treats uncorrelated disorder from random impurities and Cd-composition fluctuations;
- disorder-renormalized mass, density of states, and a disorder-driven topological transition are analyzed;
- uncorrelated composition disorder in a Kane framework is therefore established HgCdTe prior art.

Limitations for this program:

- the model explicitly addresses uncorrelated disorder;
- it does not supply the proposed measurement-kernel inversion of a finite-correlation spatial field;
- it blocks novelty claims based only on “adding disorder to a Kane model.”

### P9 — Takeda and Ichinose 2002: correlated random-mass Dirac physics

K. Takeda and I. Ichinose, “Effects of Long-Range Correlations in Random-Mass Dirac Fermions,” *Journal of the Physical Society of Japan* 71, 2216–2223 (2002).  
DOI: `10.1143/JPSJ.71.2216`

Source-established:

- random-mass Dirac systems with nonlocal correlations have been studied;
- localization length and density of states can depend materially on the correlation structure.

Limitations for this program:

- the setting and dimensionality are not bulk HgCdTe Kane crystals;
- generic correlated random-mass effects cannot be claimed as new;
- transfer to HgCdTe requires a separate controlled model and evidence that the correlation regime matters.

## 3. Claim-level novelty matrix

| ID | Proposed claim | Status | Prior-art boundary | Required evidence before use |
|---|---|---|---|---|
| C1 | A normalized measurement kernel filters a stationary covariance through a double integral or power-spectrum weighting. | established | Standard random-field and linear-systems mathematics. | Derivation under declared Fourier and normalization conventions; exact tests. |
| C2 | Gaussian covariance plus Gaussian probe gives a determinant-form effective variance. | established mathematics / repository benchmark | Follows from Gaussian integration and covariance of the difference of two kernel draws. | Independent derivation; real-space and Fourier numerical agreement. |
| C3 | One probe scale cannot separately identify point variance and correlation length. | established inverse-problem consequence | Follows from parameter collapse in a one-number observation. | Structural-rank proof for each declared covariance family. |
| C4 | Two noiseless Gaussian probe scales permit exact inversion of `sigma_x` and `xi` in the isotropic Gaussian model. | new combination, not broad novelty | Algebraic consequence of C2; likely not publishable alone. | Exact derivation, domain restrictions, uncertainty conditioning. |
| C5 | Three or more controlled scales can falsify a two-parameter covariance family. | established model-testing principle / new HgCdTe design | Generic experimental-design logic. | Residual test, uncertainty model, same-field or validated coarse-graining protocol. |
| C6 | HgCdTe edge widths should decrease with probe size according to the Gaussian benchmark in a stationary weak-disorder regime. | potentially novel HgCdTe prediction | Spatial HgCdTe mapping exists, but this exact scale-law application was not located in the audited sources. | Same specimen, known kernels, controlled modality, alternative broadening audit. |
| C7 | One latent HgCdTe field can produce different apparent disorder widths under absorption and detector-cutoff operators because averaging and edge extraction do not commute. | new combination / potentially novel | Scalar broadening and detector geometry are established separately. | Operation-order-correct forward model and quantified difference above uncertainty. |
| C8 | Replacing `sigma_x` by `sigma_x,eff` is exact for nonlinear optical transmission or cutoff extraction. | not authorized | Nonlinear exponentiation and threshold extraction generally break this identity. | Could only be used as a controlled approximation with an error map. |
| C9 | Front/back illumination and penetration depth can identify depth correlation length. | potentially novel design | Depth profiles and optical kernels exist separately. | Finite-slab forward model, known absorption depth, same specimen, conditioning analysis. |
| C10 | PL-map variance directly measures composition covariance. | not authorized | PL includes localization, diffusion, defects, doping, and recombination physics. | Independent composition measurement and a declared PL transport kernel. |
| C11 | Optically inferred composition maps independently validate the adopted `E_g(x,T)` law. | not authorized | Circular because the map may be produced from that law. | Independent composition metrology or explicit circularity-limited use. |
| C12 | Uncorrelated composition disorder in HgCdTe Kane physics is new. | contradicted | P8 already treats it using SCBA. | None; claim prohibited. |
| C13 | Correlated random-mass physics is generically new. | contradicted | P9 and related Dirac literature establish correlated random-mass effects. | None; claim prohibited. |
| C14 | Finite-correlation disorder materially changes a bulk HgCdTe Kane observable in an experimentally relevant regime. | potentially novel | Not established by P8 or P9 together. | Independent `sigma_E` and `xi` bounds, `kappa` gate, calculation showing a change above uncertainty. |
| C15 | Local regions with opposite signed gap establish mixed topological domains. | not authorized | Local mass sign and bulk topology are not interchangeable. | Spatially resolved spectral model, domain coupling, and valid invariant or observable. |
| C16 | Annealing-induced detector improvement proves homogenization of random composition disorder. | not authorized | P6 shows simultaneous changes in composition profile and electronic properties. | Controlled covariates and independent defect/doping/lifetime measurements. |
| C17 | A source-bounded high-resolution map can predict lower-resolution variance by convolution with validated kernels. | established method / valuable validation | Generic coarse-graining is established; HgCdTe application may be useful. | Raw map, map-transfer function, boundary treatment, direct-resolution cross-check if available. |
| C18 | The combined covariance–kernel–modality–identifiability framework is a publishable HgCdTe contribution. | potentially novel | No single audited source supplies the full chain. | Complete analytical result plus one falsifiable modality prediction and preferably source-bounded validation. |

## 4. Strongest defensible novelty target

The strongest current target is not the filtered-variance identity. It is:

> A measurement-kernel-aware HgCdTe forward and inverse framework that predicts how one spatial composition covariance field produces scale- and modality-dependent reported band-edge observables, and that states when point variance and correlation length are recoverable or non-identifiable.

This target is viable only if the work includes all four elements:

1. exact analytical normalization and benchmarks;
2. operation-order-correct HgCdTe observation operators;
3. structural and practical recoverability analysis;
4. a falsifiable same-field multiscale or controlled coarse-graining test.

Without elements 2–4, the result is generic mathematics rather than a strong HgCdTe research contribution.

## 5. Prior-art search gaps

Before publication, search specifically for:

- multiscale spot-size studies of HgCdTe absorption, PL, ellipsometry, or detector cutoff;
- variogram, autocorrelation, power-spectrum, or correlation-length extraction from HgCdTe composition maps;
- explicit PSF-aware coarse-graining of HgCdTe wafer maps;
- finite-correlation composition disorder in bulk Kane or 8-band HgCdTe calculations;
- correlations among composition, thickness, strain, doping, and defect maps on the same specimen;
- SIMS deconvolution and depth-resolution limits for HgCdTe composition oscillations;
- diffusion-length corrections in HgCdTe PL mapping.

Absence from this initial audit is not evidence of absence. Claim C18 must remain “potentially novel” until this search is completed at manuscript stage.

## 6. Authorized citation use

- P1 and P2: evidence that spatially resolved optical mapping exists; not independent proof of point composition covariance.
- P3 and P4: observation-operator prior art and warning against equating reported widths.
- P5: later PL modality target with an explicit transport-kernel caveat.
- P6: depth-structured and processing-conditioned inhomogeneity case; not a stationary random-field validation by default.
- P7: near-critical motivation and velocity scale; not correlation-length evidence.
- P8: hard novelty boundary for uncorrelated HgCdTe disorder in a Kane framework.
- P9: hard novelty boundary for generic correlated random-mass Dirac physics.

## 7. Publication stop rule

Do not present the Stage 1 work as a novel materials result if it stops at C1–C5. A paper-level claim requires C6, C7, C9, C14, C17, or C18 to be established with evidence and uncertainty sufficient to change interpretation or measurement design.