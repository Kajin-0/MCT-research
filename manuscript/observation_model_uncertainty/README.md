# HgCdTe fitted-intercept extraction case study

This directory contains reproducible assets for the strengthened manuscript revision:

> **Extraction-model and fit-domain dependence of fitted HgCdTe optical intercepts: a two-spectrum case study**

The controlling scientific scope is `strengthened_revision_scope.md`. The earlier `manuscript_draft.md` is an archived working draft and must not override the strengthened title, estimand separation, residual-screen treatment, or claim boundaries.

## Controlling LaTeX source

The complete current manuscript source is under `strengthened/`:

- `strengthened/manuscript.tex` - root LaTeX source;
- `strengthened/frontmatter.tex` and `strengthened/sections/*.tex` - complete current manuscript;
- `strengthened/references.tex` and `strengthened/references.bib` - self-contained and machine-readable bibliographies;
- `strengthened/SOURCE_SHA256SUMS` - committed source integrity manifest.

The workflow `.github/workflows/hgcdte-fitted-intercepts-package.yml` regenerates the deterministic figures, compiles the current LaTeX manuscript, creates `PACKAGE_SHA256SUMS`, and uploads a complete checksummed ZIP artifact. The older `irpt/` source is retained for provenance only and is not the controlling strengthened manuscript.

The revision incorporates:

- `strengthened_revision_scope.md`;
- `strict_revision_summary.md`;
- `local_feature_robustness_addendum.md`;
- `data/validation/moazzami2005_model_robustness_reference.json`;
- `data/validation/moazzami2005_model_robustness_summary.csv`;
- the frozen robustness figures described below; and
- the claim boundaries in this README.

## Scientific scope

The study analyzes two 300 K absorption-coefficient curves from Moazzami et al. Figure 6. The curves are model-derived spectroscopic-ellipsometry outputs reconstructed from embedded bitmaps, not native direct-absorption measurements. The paper therefore quantifies downstream extraction dependence; it does not estimate the total experimental uncertainty of either specimen.

The primary estimand class contains fitted optical-intercept models only. Fixed-alpha crossings are separately defined operational coordinates and do not enter the fitted-model span or an empirical-equation ranking.

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
- Coherent calibration-corner maxima: **0.89 meV** and **0.68 meV**.
- Alternative reconstruction maxima with fixed membership: **0.69 meV** and **0.81 meV**.
- Largest admissible reconstruction-plus-membership shifts: **1.25 meV** and **1.96 meV**.
- Fit-domain/weighting maxima: **5.71 meV** and **5.44 meV**.
- Non-boundary spans across the endpoint/weighting grid: **2.59-11.00 meV** and **1.84-11.09 meV**.
- Two-point reconstruction irregularity near 0.198 eV: approximately **0.12 meV** nominal influence; physical origin unidentified.

The descriptive line-envelope screen is evaluated over a 4 by 3 threshold grid. Its retained span is threshold-dependent, so it is secondary and is not interpreted as a physical interval or abstract-level headline.

The robust conclusion is not that one universal 5-7 meV uncertainty applies to HgCdTe. For these two reconstructed, model-derived curves, the fitted optical intercept is materially conditioned by the functional form, fit-domain endpoints, and weighting convention.

## Frozen figures

- `figure1_spectrum_models.svg` - reconstructed source coordinates and fitted extraction models; no local-feature highlight.
- `figure6_relative_fitted_intercepts.svg` - fitted intercept positions with boundary-limited candidates labeled.
- `figure7_robustness_scales.svg` - coherent calibration, reconstruction, membership, and endpoint/weighting sensitivity shown separately.
- `figure8_model_residual_compatibility.svg` - residual RMS normalized by reconstructed source-line half-width.

Energy-resolved residual arrays and the screen-threshold grid are exported in the detailed robustness JSON. The strengthened review PDF also contains specimen-specific residual-versus-energy panels and endpoint heatmaps.

Earlier equation-ranking, threshold-envelope, identifiability, and acquisition-design figures are retained only for provenance or supplementary development. They are not controlling main-evidence figures for the strengthened revision.

## Claim boundaries

Authorized:

- deterministic downstream sensitivity for the two reconstructed curves;
- explicit separation of fitted intercepts and operational fixed-alpha coordinates;
- boundary-excluded and completeness spans reported separately;
- residual compatibility and screen-threshold sensitivity reported descriptively;
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
