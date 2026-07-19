# HgCdTe observation-model uncertainty manuscript

This directory contains the reproducible assets and working draft for:

> **Observation-model uncertainty and identifiability in HgCdTe bandgap extraction**

## Rebuild

From the repository root, generate the spectrum-derived tables and Figures 1-3 with:

```bash
python -m tools.build_observation_model_manuscript_assets \
  --repository-root . \
  --output-dir generated
```

Generate the conceptual Figures 4-5 with:

```bash
python -m tools.build_observation_model_conceptual_figures \
  --output-dir conceptual-generated
```

The builders use only committed derived spectra, validated analysis oracles, NumPy, and the Python standard library. They do not copy or embed copyrighted source figures.

The repository tests rebuild all frozen outputs and require byte-for-byte equality. `SHA256SUMS` independently binds every committed figure, table, and machine-readable summary.

## Manuscript

- `manuscript_draft.md` — working abstract, introduction, methods, results, discussion, limitations, conclusions, captions, and bibliography placeholders.
- `SHA256SUMS` — integrity manifest for all generated manuscript assets.

Bibliographic fields marked for verification must not be completed from memory. They require exact primary-source recovery.

## Frozen figures

- `figure1_spectrum_models.svg` — digitized Moazzami 2005 Figure 6a solid IRSE trace with all fitted observation models.
- `figure2_edge_candidates.svg` — extracted edge versus observation definition for both specimens.
- `figure3_material_residual_envelopes.svg` — four-model residual intervals from fitted-model and stable fixed-threshold envelopes.
- `figure4_identifiability.svg` — latent-gap versus method, carrier, vacancy, and measurement-term identifiability diagram.
- `figure5_paired_acquisition_design.svg` — paired audit-grade `2 x 2 x 2` acquisition design generated from the validated design oracle.

## Frozen tables and summaries

- `table1_specimen_provenance.csv` — specimen, source, calibration, composition, carrier, and input-hash record.
- `table2_candidate_definitions.csv` — observation-candidate definitions and source-domain limits.
- `table3_edge_ensemble.csv` — all 28 edges, boundary flags, coordinate sensitivity, and nominal comparator labels.
- `table4_material_model_comparison.csv` — Hansen, published Seiler, Laurenti, and provisional Hansen-Pade predictions and fitted-model residual intervals.
- `table5_claim_boundaries.csv` — authorized, descriptive-only, and unauthorized manuscript claims.
- `manuscript_asset_summary.json` — machine-readable real-spectrum decision summary.
- `conceptual_figure_summary.json` — machine-readable conceptual-figure source and claim boundary.

## Controlling claim boundary

Fitted observation-model choice contributes `6.414-6.830 meV` of edge spread, while the declared coordinate perturbations move fitted edges by no more than `0.891 meV`. Fixed absorption definitions change the nominal closest material comparator.

Published Seiler is nominally closest for every fitted-model edge, but its advantage over Hansen is only `0.177-0.255 meV`. Because specimen-level composition uncertainty is unreported and both spectra come from one study, strict material-law ranking is not authorized.

The complete observation ensemble must be reported. No fixed threshold is identified with the latent material gap, no corrected or production edge is selected, and no universal replacement for Hansen is claimed.
