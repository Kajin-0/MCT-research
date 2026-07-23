# HgCdTe fitted-edge extraction case study

This directory contains reproducible assets for the strict manuscript revision:

> **Extraction-model and fit-domain dependence of reported HgCdTe optical band edges: a two-spectrum case study**

The earlier `manuscript_draft.md` is an archived working draft. It overemphasizes a broad uncertainty interpretation, fixed-alpha/equation-ranking results, and a proposed acquisition design. It is not the controlling scientific framing.

The controlling revision must incorporate:

- `local_feature_robustness_addendum.md`;
- `data/validation/moazzami2005_model_robustness_reference.json`;
- `data/validation/moazzami2005_model_robustness_summary.csv`;
- the strict robustness figures described below; and
- the claim boundaries in this README.

## Scientific scope

The study analyzes two 300 K absorption-coefficient curves from Moazzami et al. Figure 6. The curves are model-derived spectroscopic-ellipsometry outputs reconstructed from embedded bitmaps, not native direct absorption measurements. The paper therefore quantifies downstream extraction dependence; it does not estimate the total experimental uncertainty of either specimen.

The primary estimand class contains fitted gap-intercept models only. Fixed-alpha crossings are retained as separately defined operational coordinates and do not enter the fitted-model span or an empirical-equation ranking.

## Reproducible analysis

From the repository root:

```bash
python -m tools.run_moazzami2005_model_robustness \
  --repository-root . \
  --output-json generated/moazzami-model-robustness.json

python -m tools.build_moazzami_model_robustness_reference \
  --repository-root . \
  --output-json generated/moazzami-model-robustness-reference.json \
  --output-csv generated/moazzami-model-robustness-summary.csv

python -m tools.build_observation_model_manuscript_assets \
  --repository-root . \
  --output-dir generated/manuscript-assets

python -m tools.build_observation_model_robustness_figures \
  --reference-json data/validation/moazzami2005_model_robustness_reference.json \
  --output-dir generated/robustness-figures
```

The builders use committed derived spectra, calibration records, validated deterministic analysis code, NumPy, and the Python standard library. Copyrighted source pages and source figures are not redistributed.

## Controlling quantitative results

- Boundary-excluded nominal fitted-model spans: **5.09 meV** and **6.68 meV**.
- Full completeness spans including boundary-limited fits: **6.41 meV** and **6.83 meV**.
- Secondary line-envelope-compatible nominal spans: **2.61 meV** and **2.09 meV**.
- Coherent calibration-corner maxima: **0.89 meV** and **0.68 meV**.
- Alternative reconstruction maxima with fixed membership: **0.69 meV** and **0.81 meV**.
- Largest admissible reconstruction-plus-membership shifts: **1.25 meV** and **1.96 meV**.
- Fit-domain/weighting maxima: **5.71 meV** and **5.44 meV**.
- Non-boundary spans across the endpoint/weighting grid: **2.59-11.00 meV** and **1.84-11.09 meV**.
- Two-point reconstruction irregularity near 0.198 eV: approximately **0.12 meV** nominal influence; physical origin unidentified.

The robust conclusion is not that one universal 5-7 meV uncertainty applies to HgCdTe. For these two reconstructed, model-derived curves, the fitted intercept is materially conditioned by the functional form, fit-domain endpoints, and weighting convention.

## Frozen figures

- `figure1_spectrum_models.svg` - reconstructed source coordinates and fitted extraction models; no local-feature highlight.
- `figure6_relative_fitted_intercepts.svg` - fitted intercept positions with boundary-limited candidates labeled.
- `figure7_robustness_scales.svg` - coherent calibration, reconstruction, membership, and endpoint/weighting sensitivity shown separately.
- `figure8_model_residual_compatibility.svg` - residual RMS normalized by reconstructed source-line half-width.

Earlier equation-ranking, threshold-envelope, identifiability, and acquisition-design figures are retained only for provenance or supplementary development. They are not controlling main-evidence figures for the strict revision.

## Claim boundaries

Authorized:

- deterministic downstream sensitivity for the two reconstructed curves;
- explicit separation of fitted intercepts and operational fixed-alpha coordinates;
- boundary-excluded and completeness spans reported separately;
- residual compatibility reported descriptively;
- fit-domain and weighting conventions identified as material sensitivity axes;
- the local two-point irregularity does not control the central result.

Not authorized:

- a probability interval or total experimental uncertainty budget;
- a unique physical band gap;
- a physical explanation of the local plateau;
- an empirical-equation winner;
- a universal HgCdTe extraction correction;
- generalization to native data, other specimens, temperatures, laboratories, or model families.

## Submission state

**READY_FOR_SPECIALIST_REVIEW**, not submission-ready. Native source data, inversion covariance, composition uncertainty, independent validation, final bibliography closure, journal-template conversion, author metadata, and a DOI-bearing archive remain unresolved.
