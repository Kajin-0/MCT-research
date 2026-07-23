# Manuscript addendum: local reconstruction sensitivity and fit-window leverage

**Status:** controlling addendum for PR #338 until the complete manuscript source is regenerated in the selected journal template.

This addendum supplements `manuscript_draft.md`. It does not alter the reconstructed coordinates, select a corrected edge, or assign a physical mechanism to a local spectral irregularity.

## Two-point reconstruction irregularity

The reconstructed Moazzami 2005 Figure 6a solid IRSE trace contains one adjacent source-pixel direction reversal inside the declared `600-5000 cm^-1` fit population:

```text
energy_eV       source_pixel_y_center
0.196491228     160.0
0.197543860     163.0
```

Increasing source-image pixel `y` corresponds to decreasing reconstructed absorption. These two adjacent bitmap-derived coordinates therefore reverse the expected local direction. Nondecreasing isotonic reconstruction pools the violation and produces the short visible plateau near `0.198 eV`.

This pair is a feature of the reconstruction record, not an identified material feature. The available bitmap cannot distinguish a physical fluctuation from instrument response, source processing, printed-line thickness, rasterization, or coordinate extraction effects.

The committed coordinates remain unchanged. No smoothing, interpolation, point replacement, local baseline correction, or deletion is applied to the nominal analysis.

## Two-point sensitivity check

As a secondary robustness check, exactly the two adjacent coordinates are omitted while the rest of the declared fit population remains unchanged. Every fitted extraction model is recomputed on the same deterministic 4,001-point edge grid.

The omission is also combined with the four coherent coordinate-perturbation cases used in the manuscript digitization audit. Boundary-limited candidates remain in the machine record but are excluded from stability interpretation because a parameter pinned at a search bound can appear artificially insensitive.

For the `x=0.226` spectrum:

```text
maximum non-boundary shift, two-point omission          0.116875 meV
maximum non-boundary shift, omission + coordinate cases 0.959441 meV
non-boundary model span after omission                   5.121875 meV
```

For the five smaller source-pixel reversal pairs in the `x=0.310` spectrum:

```text
maximum non-boundary shift, two-point omission          0.139125 meV
maximum non-boundary shift, omission + coordinate cases 0.705191 meV
```

The relevant result is the continuous magnitude of the change, not whether it crosses a selected pass/fail threshold. For Figure 6a, the nominal change is approximately `0.12 meV`, and the combined omission-plus-coordinate change is approximately `0.96 meV`, compared with a `5.12 meV` non-boundary fitted-model span after omission. The pair therefore does not account for the multi-meV model-form dependence.

Full numerical precision is retained in machine-readable records. Narrative text and display tables should use precision commensurate with the figure-derived coordinates.

## Global contiguous-window leverage stress test

The two-point check is supplemented by an adversarial fit-window leverage audit. Every possible contiguous one-, three-, and five-point window is omitted in turn from the fixed `600-5000 cm^-1` fit population. The omitted interval is not refilled, interpolated, or replaced, and all models are refitted on the same deterministic edge grid.

This deletion ensemble is not a random sample, experimental covariance model, confidence interval, posterior distribution, or assertion that the omitted coordinates are erroneous. It is a deterministic leverage stress test.

| Specimen | Leave-one-out max (meV) | Three-point max (meV) | Five-point max (meV) | Minimum non-boundary model span (meV) | Minimum span / Hansen-Seiler |
|---|---:|---:|---:|---:|---:|
| `x=0.226` | 0.901 | 2.331 | 3.596 | 4.984 | 19.6 |
| `x=0.310` | 1.034 | 3.008 | 4.505 | 3.385 | 19.2 |

The largest multi-point shifts occur in the free-exponent fractional-power fit when the earliest admitted fit points are omitted. The stress test therefore identifies practical low-energy fit-window conditioning. It does not invalidate those coordinates or authorize a revised spectrum.

Even under every tested one-, three-, and five-point omission, the minimum non-boundary fitted-model spans remain more than nineteen times the corresponding Hansen-Seiler equation differences. This ratio is a secondary scale comparison; the absolute meV spans are the primary result.

## Required manuscript interpretation

The manuscript must distinguish four quantities:

1. coordinate sensitivity of the reconstructed figure;
2. the secondary two-point reconstruction sensitivity check;
3. global fit-window leverage under contiguous omission stress; and
4. fitted-model dependence across declared extraction models.

These quantities have different semantics and must not be combined into one standard deviation, confidence interval, or general measurement-uncertainty statement.

The two-point result supports only the limited statement that the visible plateau is not responsible for the central multi-meV fitted-model spread. The global stress result separately requires disclosure that the free-exponent model is conditioned by lower fit-window membership.

## Figure consequence

The main spectrum figure must:

- identify the trace as a reconstruction of a published bitmap rather than native instrument-export data;
- retain the committed coordinates unchanged;
- display fitted curves only over the declared fit population;
- keep the legend outside the data axes; and
- avoid highlighting the two-point irregularity as though it were a physical, excluded, or central spectral region.

A small supplementary zoom may show the raw source-pixel reversal pair and the isotonic reconstruction when documentation of the audit is necessary. It must be labeled as a reconstruction diagnostic, not as a material feature.

## Authorized claims

- omission of the questioned Figure 6a pair changes non-boundary fitted edges by about `0.12 meV` nominally and by at most about `0.96 meV` in the combined coordinate cases;
- no correction of the nominal reconstructed trace is warranted by this sensitivity check;
- flexible fitted edges exhibit material low-energy fit-window leverage;
- the fitted-model-span versus Hansen-Seiler scale comparison survives all tested contiguous window omissions;
- the results are deterministic and conditional on two reconstructed spectra and the declared model family.

## Prohibited claims

- the plateau is proven physical or proven artifactual;
- the two coordinates define a physical `core`, transition, defect, or material region;
- the source coordinates may be smoothed, replaced, or deleted in the nominal analysis;
- the sliding-window ranges are confidence intervals, experimental covariance, or probability distributions;
- all fitted models are stable under arbitrary fit-window changes;
- a boundary-limited fit is identified because it remains pinned at a search bound;
- the result generalizes to native spectra, other specimens, temperatures, laboratories, or extraction-model families without additional evidence.

## Reproducibility

Controlling assets and tests include:

```text
tools/audit_moazzami2005_local_feature_sensitivity.py
tools/audit_moazzami2005_pixel_reversal_core.py
tools/build_moazzami_local_feature_reference.py
data/validation/moazzami2005_local_feature_sensitivity_reference.json
data/validation/moazzami2005_local_feature_sensitivity_summary.csv
tests/test_moazzami2005_local_feature_sensitivity.py
tests/test_moazzami2005_pixel_reversal_core.py
tests/test_moazzami2005_local_feature_reference.py
```

Internal filenames retain the earlier `reversal_core` identifier for reproducibility. Public-facing manuscript language should use `source-pixel reversal pair` or `two-point reconstruction irregularity`.

The repeated-grid implementation is algebraically vectorized for tractability and must reproduce the controlling scalar 4,001-point grid to within `1e-12 eV` at each nominal spectrum before sensitivity results are accepted.
