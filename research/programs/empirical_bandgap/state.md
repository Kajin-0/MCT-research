# Program state: empirical bandgap reconstruction

**Portfolio contribution:** R01  
**State:** active foundation; primary-data reconstruction and external validation dependent

## Objective

Reconstruct the provenance, specimen definitions, observables, and fitted datasets behind historical HgCdTe composition- and temperature-dependent bandgap equations, then compare candidate analytical laws under controlled, specimen-preserving validation.

## Controlling issues

- #1 — Hansen reconstruction;
- #8 — common analytical benchmark;
- #17 — Seiler two-photon magnetoabsorption dataset;
- #20 — Camassel LPE composition series;
- #256 — Seiler source-state and specimen-provenance reconciliation;
- #258 — Camassel Table I specimen and excitonic-edge reconstruction;
- #260 — Camassel deterministic composition-envelope evaluation;
- #265 — Scott 1969 fixed-absorption optical-edge source audit;
- #267 — Blue 1964 seven-sample optical-gap reconstruction;
- #269 — Blue 1964 signed-gap non-commensurability certificate;
- #273 — Groves 1967 signed HgTe magnetoreflection endpoint audit;
- #277 — Schmit and Stelzer 1969 Table III detector-cutoff reconstruction.

## Completed foundations

- executable historical and provisional gap laws;
- composition-aware fitting with independent or shared-specimen composition covariance;
- leakage-safe specimen and source holdouts;
- uncertainty, rank, and conditioning diagnostics;
- explicit measurement-class and provenance labels;
- signed-gap evaluation usable by downstream programs;
- specimen-level Seiler 1990 TPMA reconstruction;
- specimen- and modality-resolved Camassel 1988 Cd-rich reconstruction;
- bounded Camassel forward evaluation without parameter fitting;
- source-level Scott 1969 metrology and Figure 1 specimen audit with a fail-closed digitization gate;
- seven-row Blue 1964 theory-conditioned positive optical-gap reconstruction;
- executable Blue 1964 signed-gap non-commensurability certificate with zero fitted parameters and zero correction coefficients;
- provenance-controlled Groves 1967 signed HgTe endpoint and conditional Kane-parameter audit;
- complete Schmit and Stelzer 1969 eight-specimen, 56-row detector-cutoff reconstruction.

## Hansen reconstruction state

The Hansen 1982 primary paper and its 22-study citation graph are reconstructed. Sixteen numerical Table I cutoff observations are transcribed, but the raw specimen-level evidence behind the staged temperature-slope and 80 K composition fits remains incomplete.

Important limitations remain:

- the source combined multiple optical and magneto-optical observables;
- composition calibration methods differ materially across sources;
- datum-level weights and coefficient covariance are not reported;
- the reported 13 meV standard error is not a test of low-temperature curvature because each temperature series was first compressed into a linear slope and normalized 80 K value;
- composition behavior above approximately `x=0.6` was acknowledged as conjectural.

No pseudo-data sampled from the published polynomial may be treated as the historical dataset.

## Seiler 1990 source reconstruction

The primary Seiler full text is available to the research workflow and audited under PDF SHA256

```text
5bc624ca8292fcba72ae55d13c5be03d07af03b57afc4584c2314ca08e459a49
```

The binary source is not committed, but all numerical records preserve the source hash.

Canonical source files are:

```text
data/experimental/seiler1990_specimens.csv
data/experimental/seiler1990_figure7_digitized.csv
data/experimental/seiler1990_table2_low_temperature_magneto_optical.csv
data/experimental/seiler1990_README.md
```

### Specimen provenance

| Sample | Reported composition | Composition status | Figure 7 | Low-temperature role |
|---:|---:|---|---:|---|
| 1 | 0.239 | infrared-cutoff derived; not independent | 14 markers | Table II anchor, shape only |
| 2 | 0.253 | selected for HSC consistency; not independent | 11 markers | 146.5 +/- 1.0 meV at 7 K from narrative, shape only |
| 3 | 0.259 +/- 0.0015 | independently composition calibrated | 9 markers | Figure 7 absolute/shape series and Table II anchor |
| 4 | 0.277 +/- 0.0010 | independently composition calibrated | none | Table II anchor |
| 5 | 0.300 +/- 0.0035 | independently composition calibrated | none | Table II anchor |

The printed sample-4 composition is `0.277`; the OCR artifact `0.217` is rejected.

Samples 1 and 2 may constrain within-specimen thermal shape after profiling an additive offset. They cannot validate an absolute `Eg(x)` law. Sample 3 is the only independently composed Figure 7 temperature series. Samples 3–5 provide three independent low-temperature composition anchors but do not identify thermal coefficients.

### Figure 7 direct-marker result

PR #57 committed 34 direct open-circle markers from Figure 7 and excluded the fitted curves. Pixel coordinates, axis calibration, and coordinate-extraction half-widths are retained.

The digitization half-widths are approximately:

```text
sample 1   0.381 K, 0.125 meV
sample 2   0.381 K, 0.125 meV
sample 3   0.191 K, 0.100 meV
```

They are digitization bounds, not pointwise experimental covariance. Figure 7 does not report pointwise gap covariance.

The direct-marker reproduction found:

```text
pooled Figure 7 shape RMSE
Hansen fixed linear temperature term       1.824 meV
published Seiler nonlinear relation         1.061 meV
```

This was an in-sample reproduction because Seiler derived the same series.

A later leave-one-specimen-out shape test found that nonlinear low-temperature curvature transfers across the three specimens and materially improves on Hansen’s fixed linear shape. However, the rational-family parameters are correlated, every fold trains on only two specimens, and generic smooth curvature also transfers reasonably well.

### Provisional Hansen–Padé result

PR #110 implemented the zero-anchored candidate

$$
E_g(x,T)=E_{g,\mathrm{Hansen}}(x,0)
+\alpha(1-2x)\frac{T^3}{T^2+\tau^2},
$$

with provisional defaults

```text
alpha = 5.918273117836612e-4 eV/K
tau   = 18.059294367159467 K
```

Reference results include:

```text
pooled held-out shape RMSE
Hansen linear                 1.824 meV
published Seiler              1.061 meV
trained Seiler                0.786 meV
provisional Hansen-Pade       0.813 meV

independently composed sample-3 absolute RMSE
Hansen linear                 1.846 meV
published Seiler              1.404 meV
provisional Hansen-Pade       1.040 meV

independent low-temperature samples 3-5 RMSE
Hansen linear                 3.887 meV
published Seiler              4.914 meV
Laurenti                     11.750 meV
provisional Hansen-Pade       4.176 meV
```

The candidate is the zero-anchored constrained member of Seiler’s rational thermal family, not a new functional family. It remains provisional and is not a production equation.

The controlling limitation is now the inherited zero-temperature composition law and broader independent validation—not absence of the Seiler source or another need for thermal-model flexibility.

## Camassel 1988 Cd-rich source reconstruction

The Camassel primary paper is available in the user File Library. The binary was not materialized in the active runtime, so its SHA256 remains explicitly unavailable. The DOI, working filename, page, table, source identity, and hash status are preserved without fabricating a digest.

Canonical source files are:

```text
data/experimental/camassel1988_specimens.csv
data/experimental/camassel1988_table1_observations.csv
data/experimental/camassel1988_README.md
```

### Specimen and uncertainty structure

Table I provides eleven specimens at approximately 2 K:

```text
10 LPE epitaxial layers
1 THM bulk reference
0.50 <= x <= 1.00
```

All specimen compositions were determined by ionic microprobe analysis. The source reports a standard composition accuracy of approximately `0.5 composition percentage points`, encoded as `0.005` in fractional `x` units with semantics

```text
source_reported_standard_accuracy_not_asserted_gaussian_sigma
```

The source identifies composition calibration as its dominant experimental limitation and gives a typical gap sensitivity of approximately `20 meV` per composition percentage point. On that source scale, composition accuracy alone corresponds to roughly `10 meV` gap ambiguity.

MCT56 and MCT61 are distinct specimens even though both are printed as `x=0.710`.

### Modality-resolved Table I observations

The reconstruction contains thirteen observations from eleven specimens:

```text
6 reflectivity exciton-polariton gap rows
7 absorption/derivative-absorption excitonic gap rows
```

Clear reflectivity structures were reported over approximately `0.78 <= x <= 1.00`. Transmission and first-derivative absorption supplemented the lower-composition range.

MCT49 (`x=0.880`) and MCT47 (`x=0.780`) have both modalities and retain one shared specimen/composition group. They must not be counted as four independent composition anchors.

The Table I binding-energy alignment is closed explicitly:

```text
reflectivity-only MCT48, MCT83, bulk, MCT51
Eg = ET + theoretical binding energy

MCT49, MCT47, and lower-x absorption rows
Eg = ET + experimental binding energy
```

Examples:

```text
MCT49 reflectivity   1.3440 + 0.0080 = 1.3520 eV
MCT49 absorption     1.3420 + 0.0080 = 1.3500 eV
MCT47 reflectivity   1.1260 + 0.0065 = 1.1325 eV
MCT47 absorption     1.1435 + 0.0065 = 1.1500 eV
```

Table I does not report pointwise energy covariance. The reconstructed energy-uncertainty fields remain empty with explicit status. The tabulated gaps are exciton-model-conditioned observations, not raw interchangeable intrinsic gaps.

### Source composition-law result

Camassel et al. reported a constant bowing parameter

```text
C = 0.132 eV
```

with a maximum `33 meV` departure from linear interpolation at `x=0.5`. A cubic term with coefficient `D=0.033 eV` contributed at most `1.56 meV`; the reported fit standard deviation changed only from approximately `1.77 meV` to `1.73 meV`. The source judged that improvement insignificant relative to composition accuracy.

This is an in-source fit result. The Camassel data are useful independent Cd-rich anchors relative to the earlier Hansen compilation, but they are not an independent held-out validation of the later Laurenti 1990 Cd-rich relation because they belong to the same experimental lineage.

## Camassel deterministic composition-envelope result

Issue #260 and draft PR #264 evaluate the published equations without fitting any coefficient, source offset, modality offset, or composition shift.

For every Table I observation, each model is evaluated over

```text
x_true in [x_reported - 0.005, x_reported + 0.005]
```

clipped to `[0,1]`.

This interval is a deterministic source-accuracy sensitivity envelope. It is not a Gaussian distribution, standard-deviation posterior, likelihood, or confidence interval.

The immutable outputs are:

```text
validation/camassel1988_composition_envelope_reference.json
validation/camassel1988_composition_envelope_records.csv
docs/insights/0028_camassel_composition_envelope.md
```

### Hansen within-domain external check

Hansen’s fitted composition evidence was approximately `0 <= x <= 0.6` plus the CdTe endpoint, with the high-Cd composition behavior described as conjectural. The primary fair external checks are therefore the Camassel absorption-derived excitonic gaps at `x=0.50` and `x=0.55`.

| Reported x | Camassel gap | Hansen nominal residual | Hansen minimum absolute residual over full x envelope |
|---:|---:|---:|---:|
| 0.50 | 0.6280 eV | +63.500 meV | 54.779646 meV |
| 0.55 | 0.7010 eV | +48.208 meV | 39.234326 meV |

Positive residual means `Camassel observed gap - model prediction > 0`.

Neither residual can reach zero anywhere inside the declared source composition interval. Under the Camassel absorption-derived excitonic-gap definition, Hansen underpredicts both external within-domain observations by tens of meV even after the complete source-reported composition allowance is used.

The result is source- and observable-conditioned. It is not a universal rejection of Hansen for every operational gap definition.

### Provisional thermal-law diagnostic

The provisional Hansen–Padé minimum residuals are:

```text
x=0.50   54.769089 meV
x=0.55   39.118204 meV
```

At 2 K, the nonlinear thermal term is negligible and does not repair the inherited Hansen static composition discrepancy. This does not retract the Seiler thermal-shape result; it establishes that the zero-temperature composition polynomial is the controlling transfer limitation for these Camassel observations.

### Laurenti lineage boundary

Laurenti is descriptively closer across the reconstructed rows:

```text
all-observation nominal MAE
Hansen 1982              39.578 meV
Laurenti 1990            10.469 meV
provisional Hansen-Pade  39.430 meV
```

This is not an independent validation of Laurenti. Camassel belongs to the experimental lineage used to construct the later Laurenti Cd-rich relation. The admissible interpretation is descriptive consistency within that source lineage.

### Measurement-class dependence

The two dual-modality specimens differ by:

```text
MCT49, x=0.88   reflectivity - absorption = +2.0 meV
MCT47, x=0.78   reflectivity - absorption = -17.5 meV
```

The `17.5 meV` same-specimen difference is larger than many proposed refinements to analytical gap laws. Reflectivity and absorption observations cannot be pooled as interchangeable independent gaps without an explicit observation model.

### Validation state

The executable result contains 39 observation-model evaluations and zero fitted parameters. Exact CSV and compact-JSON regeneration pass. The focused workflow and complete Python 3.11/3.13 suites pass on the audited final result head, with `965` tests in each full suite. Issue #260 is closed as a completed bounded forward-evaluation task.

## Scott 1969 fixed-absorption optical-edge source audit

Issue #265 and draft PR #266 establish the source contract for one of Hansen’s fitted optical-absorption datasets.

Canonical source files are:

```text
data/experimental/scott1969_source_metadata.csv
data/experimental/scott1969_figure1_specimens.csv
data/experimental/scott1969_README.md
```

The primary PDF is available in the user File Library as `scott1969.pdf`. The source binary is not materialized in the active runtime, so the SHA256 remains explicitly unavailable.

### Material and composition metrology

Scott used specimens cut from modified-Bridgman ingots. Nominal composition was obtained by density measurement with stated precision

```text
+/- 0.005 in fractional x.
```

Electron-beam microprobe measurements checked the composition profile on the optical specimen or on adjacent ingot slices. The maximum reported variation across the illuminated area was approximately `0.02` in `x`, with typical variation described as lower.

The source later describes the approximate uncertainty in the plotted gap-versus-composition comparison as generally

```text
1–2 mole % CdTe
+/- 0.01 eV in energy.
```

These statements are article-level approximate bounds, not independent pointwise Gaussian standard deviations or a reported covariance matrix.

### Optical apparatus and operational edge

The specimens were polished to approximately `50 um`, with thickness measured by micrometer and interference fringes. The source used a Perkin-Elmer model 112 infrared spectrometer with CaF2, NaCl, or KBr prisms, measurable transmittance down to approximately `1e-4`, and spectral resolution of `0.01 eV` or better. The cryostat capability was `4.2–300 K`.

Scott defined the temperature-dependent optical edge as the photon energy at

```text
alpha = 500 cm^-1.
```

The thick specimens limited the highest measurable absorption coefficient to approximately

```text
alpha = 1000 cm^-1,
```

so the usual `(alpha h nu)^2` extrapolation could not be applied over a sufficiently broad range.

The stored measurement class is

```text
fixed_absorption_optical_edge_alpha_500_cm_inverse.
```

It remains distinct from the Camassel exciton-conditioned gaps, Seiler TPMA gaps, detector cutoffs, and a model-independent intrinsic gap.

### Figure 1 specimen inventory

The ten room-temperature absorption labels are retained exactly as printed, in mole percent CdTe:

```text
21, 23, 25, 31, 35, 38.5, 40.5, 46, 53, 61
```

Source-specific quality flags are retained without correction or nuisance fitting:

- specimens `38.5` and `53` have kinked absorption edges attributed to composition nonuniformity;
- specimen `25` has high residual absorption attributed mainly to inhomogeneity rather than free carriers;
- no additional specimen-specific quality exclusion is inferred for the remaining labels.

### Source equation and Hansen lineage

Scott reported

$$
E_g(x,T)=-0.303+1.73x+5.6\times10^{-4}(1-2x)T+0.25x^4,
$$

with strict intended range approximately

```text
x <= 0.6
100 K <= T <= 300 K.
```

The equation is a historical source result. Sampling it does not reconstruct the experimental marker dataset.

Scott is confirmed as Hansen fitted source `HSC_R02`. It cannot independently validate Hansen. Its value is as an observation-definition bridge between the historical `alpha=500 cm^-1` edge and later exciton-conditioned or magneto-optical gaps.

### Fail-closed digitization state

The source text and Figure 1 composition labels are auditable. Calibrated Figure 2 and Figure 5 marker coordinates are not currently recoverable from the active file interface.

Accordingly:

- no Figure 2 or Figure 5 gap coordinate is committed;
- no marker count is inferred from connecting curves or the source equation;
- no equation-required fitted composition is substituted for a measured density composition;
- all pointwise gap and pointwise uncertainty fields remain empty;
- no source-level uncertainty statement is assigned independently to every future marker.

A future digitization requires a rendered source asset and must retain marker centers, axis calibration, extraction uncertainty, specimen grouping, source uncertainty separately from digitization uncertainty, and measured-versus-fit composition labels.

### Validation state

The focused Scott workflow verifies the exact source contract, ten Figure 1 labels, quality flags, empty pointwise fields, absent Figure 2/5 marker ledgers, and tranche file boundary. The stack-aware Camassel workflow independently regenerates its 39-row immutable result on the same descendant head. Complete Python 3.11 and 3.13 suites pass with `973` tests on the audited final Scott head. Issue #265 is closed as a completed source audit; Figure 2/5 numerical reconstruction remains blocked.

## Blue 1964 theory-conditioned optical-gap reconstruction

Issue #267 and draft PR #268 reconstruct a seven-row historical numerical table outside the reconstructed Hansen 22-source fitted graph.

Canonical source files are:

```text
data/experimental/blue1964_source_metadata.csv
data/experimental/blue1964_table2_optical_gaps.csv
data/experimental/blue1964_README.md
```

The primary PDF is available in the user File Library as `blue1964.pdf`. The binary is not materialized in the active runtime, so the SHA256 remains explicitly unavailable.

### Material preparation and composition

Blue prepared HgTe and HgTe–CdTe ingots from purified elements sealed in cleaned and baked quartz. The material was held above the calculated melting point for more than 30 hours, slowly cooled, then reheated in a vertical Bridgman furnace and translated at approximately

```text
2 mm/h.
```

Chemical analyses of Hg, Te, and Cd were performed at several positions along each ingot because of segregation. Transmission specimens were cut normal to the ingot axis from known-composition sections. Typical thickness was approximately `20 um`; specimens thinner than `6 um` could be prepared. Reflectance measurements used adjacent polished sections.

The paper describes composition accuracy as better than one percent and later as one percent assumed. It does not establish whether this is an absolute atomic-percentage-point bound, a relative percentage, a statistical standard deviation, or a deterministic interval. The repository therefore records

```text
one_percent_as_reported_scale_ambiguous_not_sigma_x
```

and does not construct `sigma_x`.

### Optical apparatus and temperature context

Measurements used a Perkin-Elmer model 112 infrared spectrometer with NaCl and KBr optics over approximately `1–25 um`. The apparatus covered approximately `90–373 K`.

The seven numerical alloy observations are associated with the room-temperature Figure 6 curves. The repository records

```text
temperature_context = room_temperature
temperature_k = unknown
```

rather than assigning an exact kelvin value.

### Printed seven-row table

The article narrative identifies the numerical source as Table II, while OCR renders the Roman numeral inconsistently.

| CdTe atomic % | Fractional x | Positive optical-fit gap | Printed fit uncertainty |
|---:|---:|---:|---:|
| 0 | 0.000 | 0.030 eV | 0.020 eV |
| 0.5 | 0.005 | 0.040 eV | 0.020 eV |
| 14 | 0.140 | 0.120 eV | 0.040 eV |
| 22 | 0.220 | 0.220 eV | 0.020 eV |
| 25 | 0.250 | 0.250 eV | 0.020 eV |
| 28 | 0.280 | 0.280 eV | 0.020 eV |
| 32 | 0.320 | 0.365 eV | 0.010 eV |

The row uncertainties are source-reported bounds estimated from agreement with theoretical absorption curves. They are not silently asserted to be Gaussian one-sigma values, and no pointwise covariance is reported.

### Observation and sign semantics

Blue obtained the values by comparing measured high-absorption curves, approximately above `10^3 cm^-1`, with theoretical direct-transition absorption curves.

The measurement class is

```text
theory_conditioned_positive_optical_gap_parameter.
```

The table reports positive values for HgTe and the `0.5 atomic % CdTe` alloy. These values are not modern signed `Gamma6-Gamma8` gaps and are marked

```text
signed_gap_eligible = false
observable_sign_semantics = positive_parameter_not_signed_Gamma6_minus_Gamma8
```

They cannot be silently negated, interpreted as absolute values of a signed modern gap, or pooled with signed magneto-optical observations without an explicit observation operator.

### Preserved source inconsistency

The abstract describes alloy measurements up to `28% CdTe`, while Figure 6 and the printed numerical table include a `32% CdTe` specimen. Both statements are retained without deleting the row or revising the abstract.

### Hansen lineage and admissibility

Blue is not present in the reconstructed Hansen 22-source fitted graph. It predates Scott and Hansen and may serve as a historical external comparator for observation-model and sign-convention studies.

It is not treated as a blinded modern holdout, and its theory-conditioned positive optical-fit parameter is not directly commensurate with every Hansen input observable or with signed-gap laws.

### Validation state

The focused Blue workflow verifies the exact source contract, seven rows, room-temperature-without-invented-kelvin status, positive non-signed semantics, printed uncertainty values, ambiguous composition-accuracy semantics, preserved `28%`/`32%` conflict, absent covariance, unavailable source hash, and absence of Figure 6 pseudo-data. Complete Python 3.11 and 3.13 suites pass with `981` tests on the audited final Blue source head. Issue #267 is closed as a completed primary-table reconstruction.

## Blue 1964 signed-gap non-commensurability certificate

Issue #269 and draft PR #270 test whether Blue's positive optical-fit parameter can be treated as a modern signed `Gamma6-Gamma8` gap without an independently validated observation operator.

The executable and immutable records are:

```text
tools/audit_blue1964_sign_identifiability.py
validation/blue1964_sign_identifiability_reference.json
docs/insights/0029_blue1964_signed_gap_noncommensurability.md
```

### Source two-scale counterexample

Blue explicitly distinguishes the actual absorption-edge gap from the positive band-curvature scale used to reproduce the nonparabolic absorption shape. The source gives the hypothetical example

```text
actual energy gap at 50 K = 0
band shape corresponds to a gap scale = 0.03 eV
```

so the positive curve-shape scale is not identical to the actual edge gap even at the zero-gap boundary.

### High-energy magnitude near-degeneracy

For room-temperature HgTe, the source compares theoretical absorption curves generated with positive scales

```text
0.02 eV
0.03 eV
0.04 eV
```

and reports essentially the same higher-photon-energy result because the density-of-states contributions are similar.

The seven Table II values were selected by comparison with theory at absorption approximately above `10^3 cm^-1`, the same regime where the source reports weak discrimination among nearby curvature scales.

### Identifiability decision

Under Blue's declared observation model:

```text
source parameterization represents signed band order = false
Blue parameter equals actual edge gap = false
sign of modern Gamma6-Gamma8 identified = false
one-to-one gap magnitude identified = false
direct signed residual ranking authorized = false
external validated observation operator required = true
universal numerical correction identified = false
```

The deterministic audit performs:

```text
fitted parameters = 0
correction coefficients = 0
signed model evaluations = 0
source rows modified = 0
```

The Blue table remains useful for historical absorption-model and observation-operator studies, but it is excluded from direct residual ranking of signed gap laws.

### Cross-source context

Later signed-band-ordering work, including Scott 1969 and Groves 1967, treats HgTe with a negative signed separation, while Blue reports a positive room-temperature curve-fit parameter. This establishes non-commensurability of the observables; it does not establish a universal offset, sign flip, scale factor, or nonlinear correction.

### Validation state

The focused certificate workflow passes exact source assertions, immutable JSON regeneration, zero-fit/zero-correction enforcement, and the tranche file boundary. Complete Python 3.11 and 3.13 suites pass with `988` tests on the audited final certificate head. Issue #269 is closed as a completed observation-contract result.

## Groves 1967 signed HgTe magnetoreflection endpoint audit

Issue #273 and draft PR #274 establish a provenance-controlled signed HgTe endpoint from interband magnetoreflection.

Canonical source files are:

```text
data/experimental/groves1967_source_metadata.csv
data/experimental/groves1967_band_parameter_ledger.csv
data/experimental/groves1967_README.md
```

The primary PDF is available in the user File Library as `groves1967.pdf`. The source binary is not materialized in the active runtime, so the SHA256 remains explicitly unavailable.

### Signed observable and band-ordering convention

Groves, Brown, and Pidgeon observed high-energy `Gamma6 -> Gamma8` and lower-energy `Gamma8 -> Gamma8` magnetoreflection transition families. The high-energy transitions were fitted with a coupled `Gamma6-Gamma7-Gamma8` Kane/Luttinger magnetic-field model.

The stored observable is

```text
signed_Gamma6_minus_Gamma8_interaction_gap
E_g = E(Gamma6) - E(Gamma8)
E_g < 0 means inverted ordering
```

The source's zero thermal-energy gap at the cubic `Gamma8` degeneracy remains distinct from the finite negative `Gamma6-Gamma8` interaction gap. These two quantities must not be collapsed into one gap definition.

### Published fit and conditional parameter set

The abstract-level fitted values are

```text
E_g = -0.283 +/- 0.001 eV
E_p = 18 +/- 1 eV
```

The source states that the quoted errors reflect uncertainty in the higher-band parameters. They are not pointwise experimental Gaussian standard deviations and no transition-level covariance matrix is reported.

The representative detailed calculation retains

```text
E_g = -0.2833 eV
E_p = 18.13 eV
Delta = 1.0 eV
H1 = -5.0
G = -1.0
L_prime = -2.0
A_prime = 0
M = -5.0
L_minus_M_minus_N = 7.0
```

This is a conditional historical parameterization for the declared higher-band assumptions. It is not an independently measured universal modern eight-band parameter vector. No `P` value is derived from `E_p` in this tranche because the conversion requires an explicit convention and constants.

### Temperature ledger

The note added in proof says the paper's `0.283 eV` value was estimated to have been determined at approximately

```text
30 K.
```

This is stored as a source-note estimate, not a directly logged setpoint.

The same note reports continued measurements giving

```text
|E_g| near 0.30 eV at 1.5 K.
```

Only the magnitude is printed in that statement. The source interpretation remains inverted, but the repository does not silently replace the printed magnitude with a newly reported signed value. The two statements do not identify a temperature law.

A later Cu-doped Ge detector operated at `4.2 K`. That detector temperature is not assigned to the sample or to the main fit. The primary fit must not be relabeled as 4.2 K or 5.5 K.

### Specimen, protocol, and figure boundary

The magnetoreflection specimen was high-purity but polycrystalline HgTe, slowly grown by Bridgman in an Hg-rich environment at approximately `0.25 cm/day`. Reflected light sampled several orientations. The sample was mounted on a helium-Dewar cold finger, and attempts near `77 K` did not resolve the oscillations.

The reflective surface was prepared with a `5-10%` bromine-in-methanol etch followed by a methanol rinse. Measurements used fixed photon energy with magnetic-field sweeps; increasing- and decreasing-field resonance positions were averaged to reduce response-time error.

Figures 4 and 5 contain experimental points and theoretical curves, but this tranche contains no calibrated marker coordinates, inferred point count, sampled theory curve, or refitted transition data.

### Admissibility and validation state

Groves 1967 is not one of the reconstructed Hansen 22 fitted alloy studies. It is an endpoint/sign source, not a composition series. It can anchor the inverted sign of HgTe under its declared magnetoreflection model, but it cannot determine alloy bowing or independently validate a complete `E_g(x,T)` law.

The focused Groves workflow verifies the exact signed values, the conditional detailed parameter set, the 30 K/1.5 K/4.2 K separation, specimen and protocol metadata, absent covariance, absent Figure 4/5 ledgers, and the tranche file boundary. Complete Python 3.11 and 3.13 suites pass with `996` tests on the audited final Groves head. Issue #273 is closed as a completed signed-endpoint source audit.

## Schmit and Stelzer 1969 Table III detector-cutoff reconstruction

Issue #277 and draft PR #278 reconstruct the complete numerical table from Hansen fitted source `HSC_R01`.

Canonical source files are:

```text
data/experimental/schmit1969_source_metadata.csv
data/experimental/schmit1969_specimens.csv
data/experimental/schmit1969_table3_cutoff_observations.csv
data/experimental/schmit1969_README.md
```

The primary PDF is available in the user File Library as `schmit1969.pdf`. The source binary is not materialized in the active runtime, so the SHA256 remains explicitly unavailable.

### Eight-specimen composition ledger

Table III contains eight detectors with nominal source compositions and separate values adjusted during the source empirical fit:

| Specimen | Nominal x | Printed limit | Fit-adjusted x | Rows |
|---|---:|---:|---:|---:|
| SS69_S01 | 0.600 | 0.030 | 0.599 | 4 |
| SS69_S02 | 0.580 | 0.050 | 0.572 | 6 |
| SS69_S03 | 0.325 | 0.010 | 0.329 | 8 |
| SS69_S04 | 0.266 | 0.003 | 0.262 | 6 |
| SS69_S05 | 0.217 | 0.006 | 0.223 | 8 |
| SS69_S06 | 0.195 | 0.006 | 0.201 | 6 |
| SS69_S07 | 0.180 | 0.006 | 0.183 | 10 |
| SS69_S08 | 0.170 | 0.006 | 0.174 | 8 |

The nominal compositions are source measurements. The adjusted values are fit-dependent nuisance quantities and are recorded as

```text
adjusted_x_is_independently_measured = false
adjusted_x_is_eligible_for_held_out_composition_validation = false
```

The fact that the adjustments were generally within the composition limits does not convert them into new measurements.

### Printed observation table and operational edge

The reconstruction retains all `56` printed Table III rows, including source table order, temperature, half-peak cutoff wavelength, and source-converted cutoff energy.

The measurement class is

```text
detector_half_peak_spectral_response_cutoff
```

with row-level semantics

```text
energy field = cutoff_energy_ev
energy origin = source_converted_from_half_peak_cutoff_wavelength
signed_gap_eligible = false
intrinsic_gap_eligible_without_observation_operator = false
```

The source defines cutoff at half of peak detector response and states that it was generally about ten percent longer in wavelength than the response peak. This is source context, not a universal conversion to an intrinsic or signed gap.

The printed energy values remain authoritative. The focused test verifies consistency with `1.23984/lambda_um` within less than `0.6 meV`, reflecting printed rounding, but does not overwrite the source column.

### Detector, metrology, and uncertainty boundaries

The `x=0.572` specimen is explicitly photovoltaic and the `x=0.329` specimen explicitly photoconductive. The detector types of the other six are not inferred.

The `x=0.262` detector received greater source-fit weight because of its composition uniformity and density-based composition accuracy.

Composition was evaluated using density and electron-beam microprobe measurements. The source gives a microprobe limit of approximately `+/-0.006` mole fraction. Temperature-control stability of approximately `+/-0.5 K` remains separate from absolute temperature accuracy believed better than `10 K`. Cutoff wavelength and converted energy precision are described as better than one percent of the listed value. None of these source-level statements is silently converted to independent pointwise Gaussian covariance.

### Source relation and Hansen lineage

The source relation is retained as historical fit metadata:

```text
E_cutoff(eV) = 1.59*x - 0.25
             + 5.233e-4*T*(1 - 2.08*x)
             + 0.327*x^3
```

The source identifies its strongest range as approximately `0.17 < x < 0.33` and `T > 77 K`. No equation samples or refitted coefficients are committed in this tranche.

Schmit and Stelzer is Hansen source `HSC_R01` and therefore cannot independently validate Hansen. Hansen later excluded the four lowest-composition specimens because of mercury inclusions. That downstream rule is recorded for `SS69_S05` through `SS69_S08` without deleting any primary-source rows or silently converting it into a Schmit source statement.

### Validation state

The focused workflow verifies the exact eight specimens, all 56 observations, wavelength-energy consistency, operational cutoff semantics, measured-versus-adjusted composition distinction, detector-type boundary, uncertainty semantics, HSC_R01 lineage, downstream Hansen exclusions, absent Figure 1 pseudo-data, and the six-file tranche boundary. Complete Python 3.11 and 3.13 suites pass with `1007` tests on the audited pre-ledger Schmit head.

A final CI run is required on this state-ledger commit before Issue #277 is closed.

## Unresolved scientific questions

- what datum-level evidence and edge definitions Hansen actually fitted across the remaining source graph;
- whether calibrated Scott Figure 2/5 markers can be recovered from a rendered source asset;
- whether the Hansen/Camassel discrepancy persists when compared against Scott’s historical `alpha=500 cm^-1` observation definition rather than an exciton-conditioned gap;
- whether an independently validated forward observation operator can relate Blue’s positive curve-shape parameter to a signed gap; Blue's source alone does not identify one;
- whether the Blue `28%` abstract limit and printed `32%` row can be resolved from another primary asset or author record;
- whether calibrated Groves Figure 4/5 transition markers can be reconstructed with detector/run labels and experimental uncertainty separated from the fitted curves;
- whether the approximate Groves 30 K and 1.5 K endpoint statements can be independently reproduced before any HgTe endpoint temperature law is inferred;
- what observation operator relates Schmit half-peak detector cutoffs to intrinsic or signed gaps across detector types and geometry;
- whether Schmit nominal compositions can support specimen-preserving analyses without leakage from the fit-adjusted compositions;
- which static composition law can predict independent observations without source-lineage leakage or unjustified flexibility;
- whether independently composed fixed-specimen temperature series beyond Seiler sample 3 preserve the current thermal ranking;
- what observation model explains the Camassel reflectivity–absorption difference;
- how composition calibration, carrier state, compensation, strain, and measurement class affect residuals;
- whether any analytical evolution transfers across independent sources rather than one laboratory lineage.

## Manuscript status

No active manuscript is recorded for this program.

A future paper requires:

1. a reconstructed or explicitly bounded primary dataset;
2. specimen-preserving held-out validation;
3. composition and measurement-class uncertainty propagated at the claim level;
4. evidence stronger than another unconstrained polynomial or a fit to one source family;
5. an independently validated replacement or a decisive limitation theorem with appropriate external anchors.

The Seiler, Camassel, Scott, Blue, Groves, and Schmit source results do not authorize manuscript writing by themselves.

## Authorized next gates

- obtain a rendered Scott 1969 asset and apply a calibrated Figure 2/5 digitization gate;
- apply a calibrated Groves Figure 4/5 digitization gate only if transition-family, detector/run, field, and energy uncertainties can be retained;
- continue the Hansen source-by-source specimen reconstruction;
- use Schmit nominal compositions rather than fit-adjusted compositions for any held-out composition analysis;
- require an explicit detector-response observation operator before pooling Schmit cutoffs with intrinsic, excitonic, or magneto-optical gaps;
- seek an independently validated observation operator before any signed-gap use of Blue's positive optical-fit parameters;
- seek an independent low-temperature static-composition source that is not in the Camassel/Laurenti lineage;
- compare published HgTe endpoint values only after signed-observable convention and source temperature are aligned;
- test simple predeclared static laws under source-level holdout only after a commensurate independent source exists;
- construct explicit reflectivity-versus-absorption or high-absorption-fit observation models only if another dataset can constrain them;
- obtain additional independently composed temperature series or author data;
- quantify whether model separations exceed composition and edge-definition uncertainty;
- audit close prior art before any novelty claim for a replacement static law or the provisional thermal reparameterization.

## Unsupported claims

This program does not currently support:

- a new universal HgCdTe bandgap equation;
- production use of the provisional Hansen–Padé model;
- universal rejection of Hansen for every measurement definition;
- independent validation of Laurenti by Camassel 1988;
- independent validation of Hansen by Scott 1969;
- direct signed-gap validation or rejection using Blue 1964’s positive optical-fit parameters;
- converting Blue’s positive HgTe-rich values into negative signed gaps without an independently validated observation model;
- treating the Blue parameter as the absolute value of a modern signed gap;
- applying a universal sign flip, offset, scale factor, or nonlinear correction to Blue's parameters;
- claiming a unique Blue curve-shape magnitude from the stated high-energy comparison;
- treating Blue’s one-percent composition statement as a numerical `sigma_x`;
- treating Blue’s row fit uncertainties as Gaussian one-sigma values without justification;
- assigning an exact kelvin temperature to Blue’s room-temperature table;
- resolving Blue’s `28%`/`32%` source inconsistency by deleting or changing a row;
- sampling Blue’s theoretical curves and presenting the samples as observations;
- treating Groves's approximate `30 K` main-fit assignment as an exact logged sample setpoint;
- assigning the Cu-doped Ge detector's `4.2 K` operating temperature to the HgTe sample;
- converting the proof-update magnitude `|E_g| near 0.30 eV` into a newly printed signed datum without an explicit inference label;
- fitting a Groves endpoint temperature law from the approximate 30 K and 1.5 K statements;
- treating the Groves detailed higher-band parameter set as a universal modern eight-band parameter vector;
- deriving or publishing a `P` value from Groves's `E_p` without an explicit convention and constants;
- treating Groves 1967 as an alloy composition-series validation or bowing constraint;
- claiming that Groves Figure 4 or Figure 5 has been digitized on the current branch;
- treating Groves's quoted parameter errors as pointwise experimental covariance;
- treating Schmit fit-adjusted compositions as independently measured composition values;
- using Schmit fit-adjusted compositions in a nominally held-out composition validation without leakage disclosure;
- treating Schmit half-peak detector cutoff energies as intrinsic signed gaps;
- applying the source's approximate ten-percent peak-to-cutoff statement as a universal correction law;
- converting Schmit temperature accuracy, temperature stability, composition limits, or one-percent cutoff precision into independent pointwise Gaussian errors without an explicit model;
- deleting the four low-composition Schmit specimens from the primary-source archive because Hansen later excluded them;
- treating Hansen's mercury-inclusion exclusion as a Schmit source statement;
- sampling the Schmit empirical equation and presenting those samples as observations;
- claiming that Schmit Figure 1 has been digitized on the current branch;
- using Schmit 1969 as independent validation of Hansen;
- Gaussian significance, p-values, or chi-square from the deterministic Camassel composition envelope;
- treating composition as the only uncertainty in Camassel Table I;
- treating Scott’s article-level `+/-0.01 eV` or `1–2 mole %` statements as independent pointwise Gaussian errors;
- sampling Scott’s empirical equation and presenting the samples as experimental markers;
- claiming that Scott Figure 2 or Figure 5 has been digitized on the current branch;
- sub-meV superiority inferred from heterogeneous or dependent compositions;
- treating samples 1 and 2 as independent Seiler composition-law validation;
- treating Figure 7 digitization bounds as experimental covariance;
- treating Camassel’s `0.005` standard composition accuracy as Gaussian one-sigma without an explicit modeling decision;
- treating MCT49 or MCT47 dual-modality rows as independent specimens;
- pooling Camassel reflectivity and absorption classes without an observation model;
- assigning Table I pointwise energy covariance not reported by the source;
- using Camassel as an independent held-out source against Laurenti 1990;
- identifying `alpha` or `tau` as microscopic phonon parameters;
- treating theory-conditioned positive optical-fit parameter, fixed-alpha optical edge, detector half-peak spectral-response cutoff, optical cutoff, PL peak, TPMA gap, interband-magnetoreflection interaction gap, reflectivity exciton-polariton gap, absorption excitonic gap, zero thermal gap, and intrinsic signed gap as interchangeable;
- fitting additional flexibility without held-out evidence;
- production-equation, manuscript, or submission readiness from the current source set.

## Shared dependencies

Gap-law code, provenance records, uncertainty tools, literature ledgers, and validation datasets are shared with the distributional, spatial-disorder, and Kane programs.

## Pause criterion

Pause model expansion when primary-data reconstruction or independent validation—not model flexibility—is the limiting factor.
