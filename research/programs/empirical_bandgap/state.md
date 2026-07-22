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
- #260 — Camassel deterministic composition-envelope evaluation.

## Completed foundations

- executable historical and provisional gap laws;
- composition-aware fitting with independent or shared-specimen composition covariance;
- leakage-safe specimen and source holdouts;
- uncertainty, rank, and conditioning diagnostics;
- explicit measurement-class and provenance labels;
- signed-gap evaluation usable by downstream programs;
- specimen-level Seiler 1990 TPMA reconstruction;
- specimen- and modality-resolved Camassel 1988 Cd-rich reconstruction;
- bounded Camassel forward evaluation without parameter fitting.

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

This was an in-sample reproduction because Seiler derived the relation from the same series.

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

The executable result contains 39 observation-model evaluations and zero fitted parameters. Exact CSV and compact-JSON regeneration pass. The focused workflow and complete Python 3.11/3.13 suites pass on the audited pre-ledger head, with `965` tests in each full suite.

A final CI run is required on the state-ledger commit before Issue #260 is closed.

## Unresolved scientific questions

- what datum-level evidence and edge definitions Hansen actually fitted;
- which static composition law can predict the Camassel within-domain observations without source-lineage leakage or unjustified flexibility;
- whether the Hansen/Camassel discrepancy persists for an independently measured observable closer to Hansen’s historical cutoff definitions;
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

The Seiler and Camassel results do not authorize manuscript writing by themselves.

## Authorized next gates

- continue the Hansen source-by-source specimen reconstruction;
- seek an independent low-temperature static-composition source that is not in the Camassel/Laurenti lineage;
- test simple predeclared static laws under source-level holdout only after an independent source exists;
- construct an explicit reflectivity-versus-absorption observation model only if another dataset can constrain it;
- obtain additional independently composed temperature series or author data;
- quantify whether model separations exceed composition and edge-definition uncertainty;
- audit close prior art before any novelty claim for a replacement static law or the provisional thermal reparameterization.

## Unsupported claims

This program does not currently support:

- a new universal HgCdTe bandgap equation;
- production use of the provisional Hansen–Padé model;
- universal rejection of Hansen for every measurement definition;
- independent validation of Laurenti by Camassel 1988;
- Gaussian significance, p-values, or chi-square from the deterministic Camassel composition envelope;
- treating composition as the only uncertainty in Camassel Table I;
- sub-meV superiority inferred from heterogeneous or dependent compositions;
- treating samples 1 and 2 as independent Seiler composition-law validation;
- treating Figure 7 digitization bounds as experimental covariance;
- treating Camassel’s `0.005` standard composition accuracy as Gaussian one-sigma without an explicit modeling decision;
- treating MCT49 or MCT47 dual-modality rows as independent specimens;
- pooling Camassel reflectivity and absorption classes without an observation model;
- assigning Table I pointwise energy covariance not reported by the source;
- using Camassel as an independent held-out source against Laurenti 1990;
- identifying `alpha` or `tau` as microscopic phonon parameters;
- treating optical cutoff, PL peak, TPMA gap, reflectivity exciton-polariton gap, absorption excitonic gap, and intrinsic gap as interchangeable;
- fitting additional flexibility without held-out evidence;
- production-equation, manuscript, or submission readiness from the current source set.

## Shared dependencies

Gap-law code, provenance records, uncertainty tools, literature ledgers, and validation datasets are shared with the distributional, spatial-disorder, and Kane programs.

## Pause criterion

Pause model expansion when primary-data reconstruction or independent validation—not model flexibility—is the limiting factor.
