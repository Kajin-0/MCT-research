# HgCdTe observation-model uncertainty manuscript assets

This directory freezes the reproducible data assets for the manuscript:

> **Observation-model uncertainty and identifiability in HgCdTe bandgap extraction**

## Rebuild

From the repository root:

```bash
python -m tools.build_observation_model_manuscript_assets \
  --repository-root . \
  --output-dir manuscript/observation_model_uncertainty
```

The builder uses only committed derived spectra, the validated absorption-edge contract, NumPy, and the Python standard library. It does not copy or embed copyrighted source figures.

## Frozen outputs

- `figure1_spectrum_models.svg` — digitized Moazzami 2005 Figure 6a solid IRSE trace with all fitted observation models.
- `figure2_edge_candidates.svg` — extracted edge versus observation definition for both specimens.
- `figure3_material_residual_envelopes.svg` — four-model residual intervals from fitted-model and stable fixed-threshold envelopes.
- `table1_specimen_provenance.csv` — specimen, source, calibration, composition, carrier, and input-hash record.
- `table2_candidate_definitions.csv` — observation-candidate definitions and source-domain limits.
- `table3_edge_ensemble.csv` — all 28 edges, boundary flags, coordinate sensitivity, and nominal comparator labels.
- `table4_material_model_comparison.csv` — Hansen, published Seiler, Laurenti, and provisional Hansen-Pade predictions and fitted-model residual intervals.
- `table5_claim_boundaries.csv` — authorized, descriptive-only, and unauthorized manuscript claims.
- `manuscript_asset_summary.json` — compact machine-readable decision summary.

## Claim boundary

Published Seiler is nominally closest for every fitted-model edge, but its advantage over Hansen is only `0.177-0.255 meV`. Because specimen-level composition uncertainty is unreported and both spectra come from one study, strict material-law ranking is not authorized.

The complete observation ensemble must be reported. No fixed threshold is identified with the latent material gap, and no corrected or production edge is selected.
