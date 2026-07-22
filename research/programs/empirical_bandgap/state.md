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
- #256 — Seiler source-state and specimen-provenance reconciliation.

## Completed foundations

- executable historical and provisional gap laws;
- composition-aware fitting with independent or shared-specimen composition covariance;
- leakage-safe specimen and source holdouts;
- uncertainty, rank, and conditioning diagnostics;
- explicit measurement-class and provenance labels;
- signed-gap evaluation usable by downstream programs.

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

## Unresolved scientific questions

- what datum-level evidence and edge definitions Hansen actually fitted;
- whether the static zero-temperature composition law can be improved out of sample;
- whether independently composed fixed-specimen temperature series beyond Seiler sample 3 preserve the current thermal ranking;
- how composition calibration, carrier state, compensation, and measurement class affect residuals;
- whether any analytical evolution outperforms historical relations across independent sources rather than one laboratory lineage.

## Manuscript status

No active manuscript is recorded for this program.

A future paper requires:

1. a reconstructed or explicitly bounded primary dataset;
2. specimen-preserving held-out validation;
3. composition and measurement-class uncertainty propagated at the claim level;
4. evidence stronger than another unconstrained polynomial or a fit to one source family.

The Seiler reconstruction alone does not authorize manuscript writing.

## Authorized next gates

- continue the Hansen source-by-source specimen reconstruction;
- transcribe and audit Camassel 1988 Table I as an independent Cd-rich composition anchor;
- obtain additional independently composed temperature series or author data;
- compare static composition laws under source/specimen holdouts;
- quantify whether model separations exceed composition and edge-definition uncertainty;
- audit close prior art before any novelty claim for the provisional thermal reparameterization.

## Unsupported claims

This program does not currently support:

- a new universal HgCdTe bandgap equation;
- production use of the provisional Hansen–Padé model;
- sub-meV superiority inferred from heterogeneous or dependent compositions;
- treating samples 1 and 2 as independent Seiler composition-law validation;
- treating Figure 7 digitization bounds as experimental covariance;
- identifying `alpha` or `tau` as microscopic phonon parameters;
- treating optical cutoff, PL peak, TPMA gap, magneto-optical gap, and intrinsic gap as interchangeable;
- fitting additional flexibility without held-out evidence;
- manuscript or submission readiness from one source family.

## Shared dependencies

Gap-law code, provenance records, uncertainty tools, literature ledgers, and validation datasets are shared with the distributional, spatial-disorder, and Kane programs.

## Pause criterion

Pause model expansion when primary-data reconstruction or independent validation—not model flexibility—is the limiting factor.