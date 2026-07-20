# Observation-model uncertainty and identifiability in HgCdTe bandgap extraction

**Working manuscript draft — not yet submission formatted**

## Abstract

Band-gap relations for Hg(1-x)Cd(x)Te are often compared at the few-meV level, although an absorption-derived edge is not a direct observation of a unique latent material gap. The inferred value also depends on the observation model, fit window, operational absorption threshold, spectral-tail treatment, calibration, composition provenance, carrier state, and defect state. We apply a fail-closed edge-extraction ensemble to two calibrated primary-figure infrared spectroscopic ellipsometry spectra reported for HgCdTe at 300 K: x=0.226 with thickness 15.40 um and x=0.310 with thickness 4.95 um. The records contain 125 and 115 digitized spectral points, respectively, and preserve explicit calibration and missing-metadata status.

The fitted ensemble includes a free fractional-power model, fixed fractional powers, the source-panel exponent, and the provenance-bound Chu 1994 Kane-region form. Fitted observation-model choice produces edge spans of 6.414 and 6.830 meV. Coherent perturbation of the digitization coordinates moves every fitted-model edge by less than 0.891 meV, so the multi-meV model dependence is not explained by the declared digitization uncertainty. Fixed absorption crossings produce substantially wider operational envelopes and change the nominal closest material-gap comparator. The published Seiler relation is nominally closest for every fitted-model edge, but its advantage over Hansen is only 0.177-0.255 meV. Because specimen-level composition uncertainty is unreported and both spectra come from one source study, that ordering is descriptive rather than an identified material-law ranking.

We formalize the absorption-derived edge as a latent gap plus method, carrier, vacancy, and measurement terms, and use this decomposition to define an audit-grade paired 2x2x2 acquisition design. The results show that meV-scale HgCdTe gap comparisons require explicit propagation of the observation definition and specimen state. They do not support a universal absorption correction, a selected production edge, or a universal replacement for Hansen.

## 1. Introduction

The composition- and temperature-dependent band gap of HgCdTe controls infrared cutoff wavelength, carrier statistics, transport, and the interpretation of optical and magneto-optical measurements. Multiple empirical relations are available, including the widely used Hansen expression and later temperature-dependent forms. Their numerical predictions can differ by only a few meV over parts of the technologically relevant composition range.

A comparison at that scale is meaningful only when the measured quantity is defined with comparable precision. An absorption spectrum does not contain a unique model-independent point labeled as the band gap. The reported edge may be obtained from a power-law extrapolation, a fixed absorption crossing, a Kane-region fit, a tail-corrected model, or another operational rule. Carrier filling, vacancies, composition error, calibration, and spectral resolution can shift or reshape the observed onset. A narrow numerical fit uncertainty therefore does not by itself identify the latent material gap.

This work treats edge extraction as an observation-model problem. The objective is not to fit another universal HgCdTe polynomial. Instead, we ask three narrower questions:

1. How much does the extracted edge move under admissible observation definitions on real spectra?
2. Can that movement change the apparent ranking of established material-gap relations?
3. What paired measurements and specimen metadata are required to separate the latent gap from observation-specific contributions?

The repository analysis is deliberately fail-closed. Every candidate, exclusion, boundary-limited result, calibration assumption, and missing metadata field is exported. No candidate is promoted as the corrected or production edge.

## 2. Observation model and methods

### 2.1 Latent gap and measured edge

For a specimen with independently measured composition x and temperature T, we write a magneto-optical observation schematically as

```text
y_MO = Eg(x,T) + epsilon_MO
```

and an intrinsic-absorption-derived edge as

```text
y_abs = Eg(x,T)
        + Delta_method
        + Delta_carrier
        + Delta_vacancy
        + epsilon_abs.
```

The terms are an identifiability decomposition, not universal correction functions. `Delta_method` includes the fit family, fit window, threshold, tail treatment, and calibration convention. `Delta_carrier` represents carrier-state contributions such as filling effects. `Delta_vacancy` represents defect-state contributions that can alter the optical edge. On the same specimen, a paired difference removes the common latent term:

```text
y_abs - y_MO
  = Delta_method + Delta_carrier + Delta_vacancy + noise.
```

Without paired modalities and independent specimen-state measurements, these contributions can remain aliased.

### 2.2 Experimental spectra and provenance

The present application uses the solid infrared spectroscopic ellipsometry traces in Moazzami et al., Journal of Electronic Materials 34, 773-778 (2005), DOI 10.1007/s11664-005-0019-3, Figure 6.

- Figure 6a: x=0.226, T=300 K, thickness 15.40 um, 125 digitized points.
- Figure 6b: x=0.310, T=300 K, thickness 4.95 um, 115 digitized points.

The curves were recovered from embedded bitmap objects in the primary PDF. The committed calibration records preserve axis anchors, curve masks, centerline rules, point spacing, uncertainty floors, and source hashes. Copyrighted source pages and source figures are not committed. Specimen-level composition uncertainty, carrier type, and carrier density were not reported in the article and remain explicitly missing.

### 2.3 Edge-extraction ensemble

The fitted candidate ensemble contains:

1. a free fractional-power model,
2. fixed fractional powers p=0.5, 0.7, the source-panel fitted exponent, and 1.0,
3. the Chu 1994 Kane-region candidate within its declared composition and temperature domain.

The fractional-power family is

```text
alpha(E) = A (E-Eg)^p / E,   E > Eg.
```

The Chu candidate is retained as a provenance-bound historical observation model:

```text
alpha(E) = alpha_g exp[sqrt(beta(x,T)(E-Eg))].
```

It is enabled only for 0.170 <= x <= 0.443 and 77 <= T <= 300 K. A fit that reaches a declared search bound is exported as boundary-limited rather than identified.

Operational fixed-threshold candidates are defined as the first interpolated crossings from 400 to 5000 cm^-1. These crossings are observation definitions, not assumed estimators of the latent gap. Precision comparisons use thresholds through 4000 cm^-1 because the 5000 cm^-1 crossing for one specimen exceeds the declared coordinate-sensitivity gate.

### 2.4 Digitization-coordinate sensitivity

Four coherent perturbation corners were evaluated from plus/minus the declared energy-axis uncertainty and plus/minus the pointwise logarithmic absorption uncertainty. The point population in the base fitted window was held fixed so that the audit isolates coordinate uncertainty rather than changes in fit-window membership.

The digitization stop rule is 5 meV. Fitted-model conclusions are treated as stable only when their coordinate shifts remain below 1 meV. Fixed-threshold precision claims are restricted to crossings whose coordinate shifts remain below 5 meV.

### 2.5 Material-gap comparators

Four material-gap relations are evaluated at each reported composition and temperature:

- Hansen,
- the published Seiler 1990 rational-temperature relation,
- the reconstructed Laurenti relation,
- the provisional constrained Hansen-Pade relation.

The published Seiler comparator is

```text
Eg(x,T) = Eg_Hansen(x,0)
          + 5.35e-4 (1-2x) (A+T^3)/(B+T^2),
A = -1822 K^3,
B = 255.2 K^2.
```

The provisional Hansen-Pade relation remains a constrained Seiler-family parameterization, not a new functional family or production equation. No zero-temperature replacement for Hansen is evaluated or authorized here.

For each observation candidate, the nominal closest material comparator is the model with the smallest absolute residual. A strict material-law ranking is authorized only if the ordering remains identified after observation-model and specimen-metadata uncertainty. That condition is not met by the present data.

### 2.6 Paired acquisition-design analysis

A local linearized identifiability model contains five coefficients: latent intercept, latent composition slope, absorption-class offset, carrier contribution, and vacancy contribution. The validated acquisition oracle evaluates the full two-level factorial over composition, carrier proxy, and vacancy proxy. Each of the eight specimen states receives paired magneto-optical and intrinsic-absorption measurements at a low-temperature block and at 300 K.

Per temperature block, the design contains 16 observations, rank 5/5, 11 residual degrees of freedom, condition number 2.618, and maximum leverage 0.4375. The full two-temperature design contains 32 gap observations. The result establishes the unique audit-grade subset only within the declared two-level 2^3 candidate family and declared numerical gates; it is not a universal optimal-design proof.

## 3. Results

### 3.1 Fitted observation-model spread

For x=0.226, the fitted fractional-power and Chu candidates span 181.086-187.500 meV, a full range of 6.414 meV. The p=0.5 and Chu candidates reach the upper edge-search boundary and are flagged as boundary-limited.

For x=0.310, the fitted candidates span 289.670-296.500 meV, a full range of 6.830 meV. The Chu candidate is boundary-limited.

The model-family spread is similar for both compositions despite their different nominal gaps and film thicknesses. No single fitted edge is selected.

### 3.2 Digitization sensitivity does not explain the model spread

Across both spectra, the maximum coherent coordinate-induced shift of any fitted-model edge is 0.891 meV. This is substantially smaller than the 6.414-6.830 meV fitted-model spans. The observation-model dependence therefore survives the declared digitization uncertainty.

Every fixed threshold through 4000 cm^-1 remains below the 5 meV coordinate-shift gate. The 5000 cm^-1 crossing for x=0.310 shifts by 5.694 meV and is excluded from precision plots and threshold-based claims.

### 3.3 Observation definition changes the nominal material comparator

For all fitted fractional-power and Chu candidates, the published Seiler relation is nominally closest for both specimens. Fixed absorption crossings produce a different result.

For x=0.226, published Seiler is nominally closest at 400 and 600 cm^-1, Laurenti is closest near 800-1000 cm^-1, and the provisional Hansen-Pade relation is closest at higher crossings.

For x=0.310, published Seiler remains nominally closest through 1000 cm^-1, the provisional Hansen-Pade relation is closest at 2000 cm^-1, and Laurenti is closest at 3000 cm^-1 and above.

Thus, a material-model ranking can be reversed by changing only the declared observation definition. This does not imply that the high-threshold crossings are better estimates of the latent gap. It demonstrates that the ranking is conditional on what was called the edge.

### 3.4 The Seiler-Hansen fitted-edge ordering is not identified

At x=0.226 and 300 K, the Hansen and published Seiler predictions are 190.366 and 190.112 meV, respectively, a separation of 0.255 meV. At x=0.310 and 300 K, the predictions are 304.235 and 304.059 meV, a separation of 0.177 meV.

Published Seiler is therefore nominally closer to every fitted-model edge, but the margin over Hansen is sub-meV. The source does not report specimen-level composition uncertainty, and the two spectra are not independent cross-laboratory records. The data do not identify a strict Seiler-over-Hansen material-law ranking.

### 3.5 Audit-grade acquisition target

The paired design in Figure 5 separates the common latent gap from observation-class, carrier, and vacancy terms by construction. The eight specimen states are repeated at low and room temperature, and both modalities are applied to every specimen. Independent composition metrology, Hall state, a vacancy-sensitive proxy, raw absorption data, extraction covariance, and processing history are required.

The design does not assume that the five-term local model is physically complete. It supplies the minimum redundancy needed to test that model under the declared gates.

## 4. Discussion

### 4.1 Numerical precision is not physical identification

A fitted edge may be numerically stable while remaining physically ambiguous. In the present spectra, coordinate perturbations move fitted edges by less than 1 meV, but admissible fitted observation models differ by approximately 6-7 meV. Reporting only the optimizer uncertainty would therefore understate the dominant model dependence.

### 4.2 Fixed thresholds answer an operational question

A fixed absorption crossing can be useful for reproducible device or process comparisons when the threshold and calibration are held constant. It is not automatically the latent band gap. The large threshold envelopes in the present analysis show that an unspecified threshold can dominate a few-meV comparison between material relations.

### 4.3 Composition and carrier metadata are part of the measurement

The sub-meV Seiler-Hansen separation cannot be interpreted independently of composition uncertainty. Carrier state is also missing for both specimens, so filling-related contributions cannot be separated from the optical extraction. These are not ancillary metadata omissions; they are identifiability limits.

### 4.4 Scope of the material-model comparison

The analysis does not establish a preferred universal HgCdTe gap equation. Published Seiler is the nominal fitted-edge winner in this specific two-spectrum application, while fixed thresholds change that ordering. The provisional Hansen-Pade relation is retained only as a constrained research comparator. Laurenti is retained with explicit reconstruction limitations. Hansen remains the zero-temperature baseline used by the provisional relation.

### 4.5 Experimental consequence

Further progress requires paired measurements rather than additional unpaired edge tables. The most informative next experiment measures magneto-optical and intrinsic-absorption gaps on the same specimens while independently controlling or measuring composition, carrier state, and vacancy state. The paired factorial design converts the qualitative confounding diagram into a testable acquisition program.

## 5. Limitations

1. The experimental application contains two 300 K spectra from one source study.
2. The data were recovered from calibrated primary-figure bitmaps rather than native instrument exports.
3. Specimen-level composition uncertainty is unreported.
4. Carrier type and density are unreported.
5. Several fitted candidates are boundary-limited and are not interpreted as identified edges.
6. The highest fixed threshold fails the coordinate-sensitivity gate for one specimen.
7. The observation decomposition is local and diagnostic; it is not a universal physical correction model.
8. The acquisition-design minimum is established only within the declared two-level candidate family and audit gates.
9. Independent low-temperature and cross-laboratory validation remain desirable strengthening evidence, but are not used as fit authority here.

## 6. Conclusions

Real HgCdTe absorption spectra support a clear distinction between numerical fit precision and physical gap identification. For two calibrated 300 K spectra, fitted observation-model choice contributes 6.414-6.830 meV of edge spread, while declared digitization uncertainty moves the fitted edges by at most 0.891 meV. Fixed absorption definitions change the nominal closest material-gap relation. Published Seiler is nominally closest for the fitted edges, but only by 0.177-0.255 meV over Hansen, which is not identifiable without composition uncertainty and independent evidence.

Few-meV HgCdTe gap comparisons should therefore report the complete observation definition, calibration, fit domain, composition provenance, carrier state, defect state, and candidate envelope. The present work authorizes neither a universal absorption correction nor a selected production edge. A paired 2x2x2 acquisition design provides a concrete route to separating the latent material gap from method, carrier, and vacancy contributions.

## Data and code availability

All derived spectra, calibration records, candidate definitions, analysis code, deterministic figure generators, tables, claim-boundary records, and SHA-256 manifests are stored in the repository. Copyrighted source pages and figures are not redistributed. Every frozen manuscript asset is required to reproduce byte-for-byte from committed inputs.

## Figure captions

**Figure 1.** Digitized Moazzami 2005 Figure 6a IRSE spectrum at x=0.226 and 300 K with all fitted observation-model candidates. Boundary-limited candidates are retained as diagnostics. No fitted curve is selected as the latent material gap.

**Figure 2.** Extracted edge versus observation definition for x=0.226 and x=0.310. The upper group contains fitted fractional-power and Chu candidates; the lower group contains fixed absorption crossings. Open markers denote boundary-limited fits.

**Figure 3.** Residual intervals relative to Hansen, published Seiler, Laurenti, and provisional Hansen-Pade predictions. Narrow dark intervals show the fitted-model envelope; wider gray intervals show stable 400-4000 cm^-1 threshold definitions. The intervals are observation-definition sensitivity, not statistical confidence intervals.

**Figure 4.** Identifiability diagram separating the latent material gap from method, carrier, vacancy, and measurement terms. Same-specimen magneto-optical and absorption observations remove the common latent term in the paired difference. The decomposition does not authorize a universal correction.

**Figure 5.** Audit-grade paired 2x2x2 acquisition design. Eight composition-carrier-vacancy specimen states receive paired magneto-optical and absorption measurements in low- and room-temperature blocks, producing 32 observations. Numerical diagnostics are read directly from the validated design oracle.

## Table captions

**Table 1.** Specimen, measurement, source, calibration, composition, carrier-metadata, point-count, and input-hash provenance.

**Table 2.** Observation-candidate definitions and source-supported domains.

**Table 3.** Complete 28-edge ensemble with boundary flags, digitization-coordinate shifts, and nominal material comparators.

**Table 4.** Hansen, published Seiler, Laurenti, and provisional Hansen-Pade predictions with fitted-model residual intervals. Strict ranking is not authorized.

**Table 5.** Authorized, descriptive-only, and unauthorized manuscript claims.

## References requiring final bibliography formatting

1. Hansen, Schmit, and Casselman, HgCdTe band-gap relation, 1982. **[Verify complete primary citation from repository source ledger.]**
2. Seiler et al., published rational-temperature HgCdTe relation, 1990, DOI 10.1116/1.576952.
3. Laurenti et al., HgCdTe temperature-dependent gap relation, 1990. **[Complete primary metadata and reconstruction note required.]**
4. Chu et al., Kane-region absorption model, 1994, DOI 10.1063/1.356464.
5. Moazzami et al., Journal of Electronic Materials 34, 773-778 (2005), DOI 10.1007/s11664-005-0019-3.
6. **[Add primary references for carrier-filling and vacancy-edge mechanisms only after exact source verification.]**
