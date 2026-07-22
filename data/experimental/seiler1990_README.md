# Seiler 1990 TPMA dataset reconstruction

**Primary source:** D. G. Seiler, J. R. Lowney, C. L. Littler, and M. R. Loloee, “Temperature and composition dependence of the energy gap of Hg1-xCdxTe by two-photon magnetoabsorption techniques,” *Journal of Vacuum Science & Technology A* **8**, 1237–1244 (1990).  
**DOI:** `10.1116/1.576952`  
**Audited PDF SHA256:** `5bc624ca8292fcba72ae55d13c5be03d07af03b57afc4584c2314ca08e459a49`

The source PDF is available to the research workflow but is not committed to this repository. Numerical records retain the source hash so future audits can detect substitution or re-rendering.

## Observable

The reported gap is obtained from resonant two-photon magnetoabsorption detected through photoconductive response and interpreted with a modified Pidgeon–Brown Landau-level model.

The measurement class is recorded as

```text
two_photon_magnetoabsorption_modified_Pidgeon_Brown_gap
```

It remains distinct from:

- one-photon absorption thresholds;
- detector cutoff energies;
- excitonic optical edges;
- photoluminescence peaks;
- simplified-Kane signed gaps.

The source reports approximately `1%` absolute magnetic-field accuracy, better than `0.01%` relative field accuracy, and sample-temperature accuracy of approximately `+/-0.2 K`. Those article-level statements are not silently assigned as independent pointwise Figure 7 covariance.

## Files and roles

### `seiler1990_specimens.csv`

Canonical Table I specimen registry with electrical properties, composition provenance, Figure 7 eligibility, low-temperature gap anchors, and admissibility flags.

### `seiler1990_figure7_digitized.csv`

Merged in PR #57. Contains 34 direct open-circle markers from Figure 7:

```text
sample 1 / panel a   14 markers
sample 2 / panel b   11 markers
sample 3 / panel c    9 markers
```

The solid fitted curves are excluded. Pixel coordinates, axis calibration, and digitization half-widths are retained. The recorded digitization half-widths are coordinate-extraction bounds, not experimental uncertainty.

### `seiler1990_table2_low_temperature_magneto_optical.csv`

Contains the complete Table II transcription used by the historical screen, including inherited literature rows and the four present-work Table II points. Only present-work samples 3–5 have independently reported composition values and uncertainties suitable for a low-temperature composition-law check.

## Canonical specimen admissibility

| Sample | Reported composition | Composition provenance | Figure 7 use | Low-temperature use | Absolute `Eg(x)` validation |
|---:|---:|---|---|---|---|
| 1 | 0.239 | infrared-cutoff derived | thermal shape | Table II anchor | no |
| 2 | 0.253 | chosen for HSC high-temperature consistency | thermal shape | 146.5 +/- 1.0 meV at 7 K from text | no |
| 3 | 0.259 +/- 0.0015 | independent supplier value tied to wet chemistry | thermal shape and absolute series | Table II anchor | yes, with shared specimen composition uncertainty |
| 4 | 0.277 +/- 0.0010 | independent supplier value tied to wet chemistry | none | Table II anchor | yes, low-temperature point only |
| 5 | 0.300 +/- 0.0035 | independent supplier value tied to wet chemistry | none | Table II anchor | yes, low-temperature point only |

The printed sample-4 composition is `0.277`. The value `0.217` produced by some OCR renderings is incorrect and must not enter any dataset.

## What the data identify

### Figure 7

Samples 1–3 identify within-specimen thermal shape after profiling one additive energy offset per specimen. Samples 1 and 2 cannot validate the absolute composition law because their reported compositions depend on an optical cutoff or HSC consistency. Sample 3 is the only independently composed Figure 7 temperature series.

PR #57 reproduced the low-temperature plateau and the improvement of the published nonlinear Seiler shape over Hansen’s fixed linear-temperature shape. This was an in-sample reproduction of data used by Seiler to derive the relation.

Subsequent leakage-safe specimen holdouts established that a nonlinear low-temperature shape transfers across the three Figure 7 specimens, but the individual Seiler rational parameters remain correlated and are not independently identified.

### Table II present-work anchors

Samples 3–5 provide three independently composed low-temperature TPMA anchors:

```text
sample 3   x=0.259 +/- 0.0015   Eg=158.5 +/- 1 meV
sample 4   x=0.277 +/- 0.0010   Eg=195.0 +/- 1 meV
sample 5   x=0.300 +/- 0.0035   Eg=224.0 +/- 2 meV
```

The source reports the present-work Table II temperature as `2–10 K`. These three points test the static composition law plus a negligible low-temperature increment. They do not identify a temperature-dependent model’s thermal coefficients.

Sample 1 also appears in Table II but its composition is cutoff-derived. Sample 2’s explicit `146.5 +/- 1.0 meV at 7 K` result appears in the narrative rather than the present-work Table II subset.

## Existing model analyses

The source records already support:

- the PR #57 direct-marker reconstruction;
- the specimen-offset thermal-shape analysis;
- the PR #110 two-parameter zero-anchored Hansen–Padé screen;
- an independent absolute Figure 7 test on sample 3;
- an independent low-temperature composition check on samples 3–5.

The provisional Hansen–Padé model remains a research candidate, not a production equation. Its thermal shape is fitted primarily from three Seiler Figure 7 specimens, and only sample 3 supplies an independently composed absolute temperature series.

## Prohibited interpretations

- Treating all five reported compositions as independent composition metrology.
- Using samples 1 or 2 to validate an absolute `Eg(x)` law.
- Treating Figure 7 digitization bounds as experimental covariance.
- Counting repeated temperatures from sample 3 as independent composition determinations.
- Using Table II samples 3–5 to identify thermal coefficients.
- Pooling TPMA gaps with detector cutoff, ordinary absorption, PL, or simplified-Kane gaps without explicit measurement-class handling.
- Claiming universal superiority or manuscript readiness from the Seiler source alone.
