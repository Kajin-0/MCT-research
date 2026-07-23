# Manuscript addendum: localized reconstruction influence and fit-window leverage

**Status:** controlling addendum for PR #338 until the complete manuscript source is regenerated in the selected journal template.

This addendum supplements `manuscript_draft.md`. It does not alter the original reconstructed coordinates, select a corrected edge, or assign a physical mechanism to any local spectral irregularity.

## Source-coordinate irregularity

The reconstructed Moazzami 2005 Figure 6a solid IRSE trace contains one objectively defined source-pixel monotonicity reversal inside the declared `600-5000 cm^-1` fit population:

```text
energy_eV       source_pixel_y_center
0.196491228     160.0
0.197543860     163.0
```

Increasing source-image pixel `y` corresponds to decreasing reconstructed absorption. The three-pixel reversal is therefore the source-coordinate origin of the visible short plateau near `0.198 eV` after nondecreasing isotonic reconstruction. The available bitmap does not distinguish a physical feature from instrument response, source processing, printed-line thickness, rasterization, or digitization effects.

The committed reconstructed coordinates are retained unchanged. No smoothing, interpolation, point replacement, or local baseline correction is performed.

## Exact feature-core influence audit

The primary feature-specific audit removes exactly the adjacent two-coordinate reversal core while leaving the remainder of the declared fit population unchanged. Every fitted observation operator is recomputed on the same deterministic 4,001-point edge grid.

The exact pair deletion is then combined with the four coherent coordinate-perturbation corners already used for the manuscript digitization audit. Boundary-limited candidates remain in the machine record but are excluded from stability certification because a parameter pinned at a search bound can appear artificially insensitive.

For the `x=0.226` spectrum:

```text
maximum non-boundary shift, exact pair deletion       0.116875 meV
maximum non-boundary shift, deletion + corners        0.959441 meV
non-boundary operator span after pair deletion         5.121875 meV
```

For the five smaller objectively defined source-pixel reversal pairs in the `x=0.310` spectrum:

```text
maximum non-boundary shift, exact pair deletion       0.139125 meV
maximum non-boundary shift, deletion + corners        0.705191 meV
```

Under the declared `1 meV` fitted-edge stability criterion, the questioned Figure 6a feature does not control the multi-meV observation-model result. This conclusion is an influence statement, not an identification of the feature's physical origin.

## Global contiguous-window leverage stress test

The exact feature-core test is supplemented by an adversarial fit-window leverage audit. Every possible contiguous one-, three-, and five-point window is removed in turn from the fixed `600-5000 cm^-1` fit population. The window is not refilled, interpolated, or replaced, and all operators are refitted on the same deterministic edge grid.

This deletion ensemble is not a random sample, experimental covariance model, confidence interval, posterior distribution, or assertion that the removed coordinates are erroneous. It is a deterministic leverage stress test.

| Specimen | Leave-one-out max (meV) | Three-point max (meV) | Five-point max (meV) | Minimum non-boundary operator span (meV) | Minimum span / Hansen-Seiler |
|---|---:|---:|---:|---:|---:|
| `x=0.226` | 0.900625 | 2.330625 | 3.595625 | 4.984375 | 19.5764 |
| `x=0.310` | 1.033500 | 3.007750 | 4.505000 | 3.385375 | 19.1746 |

The largest multi-point shifts occur in the free-exponent fractional-power fit when the earliest admitted fit points are removed. The stress test therefore identifies practical low-energy fit-window conditioning. It does not invalidate those coordinates or authorize a revised spectrum.

Even under every tested one-, three-, and five-point omission, the minimum non-boundary observation-operator spans remain more than nineteen times the corresponding Hansen-Seiler equation differences. The central comparison between observation-model spread and fine empirical-equation disagreement therefore survives the leverage audit.

## Required manuscript interpretation

The manuscript must distinguish four quantities:

1. coordinate perturbation of the reconstructed figure;
2. exact influence of the objectively defined reversal core;
3. global fit-window leverage under contiguous deletion stress; and
4. observation-operator spread across scientifically declared edge definitions.

These quantities have different semantics and must not be combined into a single standard deviation or confidence interval.

The feature-specific result supports the statement that the visible Figure 6a plateau does not control the central result. The global stress result requires a separate disclosure that the free-exponent operator is practically conditioned by lower fit-window membership.

## Figure consequence

The revised spectrum figure must:

- identify the trace as a reconstruction of a published source bitmap rather than native instrument-export data;
- retain the committed coordinates unchanged;
- display fitted operator curves only over the declared fit population;
- keep the legend outside the data axes;
- mark the exact reversal core only as an audited source-coordinate region; and
- state that the marker is diagnostic and does not represent a correction or assigned physical mechanism.

The frozen clean-built spectrum SVG is:

```text
manuscript/observation_model_uncertainty/figure1_spectrum_models.svg
sha256 3a7d840244d81ac01eb2a1a7be94cdac1334ede56bc62f24f01d5ee5e5992ea2
```

## Authorized claims

- the exact questioned Figure 6a pair has sub-meV influence, including the declared coordinate corners;
- no correction of the nominal reconstructed trace is warranted by this audit;
- flexible fitted edges exhibit material low-energy fit-window leverage;
- the operator-spread-versus-Hansen-Seiler conclusion survives all tested contiguous window omissions;
- the results are deterministic and conditioned on the two reconstructed spectra and declared operator family.

## Prohibited claims

- the plateau is proven physical or proven artifactual;
- the source coordinates may be smoothed, replaced, or deleted in the nominal analysis;
- the sliding-window deletion ranges are confidence intervals, experimental covariance, or probability distributions;
- every fitted operator is stable below `1 meV` under arbitrary multi-point deletion;
- a boundary-limited fit is identified because it remains pinned at a search bound;
- the result generalizes to native spectra, other specimens, temperatures, laboratories, or operator families without additional evidence.

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

The repeated-grid implementation is algebraically vectorized for tractability and must reproduce the controlling scalar 4,001-point grid to within `1e-12 eV` at each nominal spectrum before sensitivity results are accepted.
