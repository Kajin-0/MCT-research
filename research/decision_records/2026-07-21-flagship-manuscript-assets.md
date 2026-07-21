# Decision record: deterministic flagship manuscript assets

**Date:** 2026-07-21  
**Issue:** #182  
**Status:** candidate controlling decision pending PR validation

## Decision

Implement the flagship manuscript figures and tables as deterministic, repository-native assets using pure Python, NumPy, SVG, Markdown, and immutable validation records.

Do not add a general plotting dependency solely for manuscript packaging. The existing Paper I asset pipeline demonstrates that deterministic custom SVG is sufficient and easier to regression-test byte for byte.

## Entry point

```text
python -m tools.build_distributional_band_edge_manuscript_assets \
  --repository-root . \
  --output-dir distributional-generated
```

The builder produces:

```text
figure1_forward_hierarchy.svg
figure2_transition_distribution.svg
figure3_herrmann_tail_nonuniqueness.svg
figure4_chang_cutoff_rank.svg
figure5_carrier_filling.svg
figure6_unified_structural_rank.svg
figure7_measurement_design.svg

table1_theorem_summary.md
table2_quantitative_results.md
table3_claim_provenance.md

distributional_band_edge_asset_summary.json
```

## Input authority

The five immutable records remain the numerical source of truth:

```text
data/validation/near_critical_transition_model_dependence.json
data/validation/herrmann_gaussian_tail_reproduction.json
data/validation/chang_2006_cutoff_identifiability.json
data/validation/dingrong_1985_carrier_filling_sensitivity.json
data/validation/unified_spectrum_structural_rank.json
```

The builder must not copy regenerated spectral arrays from prose. It regenerates:

1. the Herrmann square-root Gaussian-gap spectrum and fit-window tail regressions through public package functions;
2. the carrier-density filling series through `carrier_filled_optical_edge_ev`;
3. the unified exact-counterexample spectra through `unified_response_spectrum`.

If regenerated values disagree with immutable records beyond declared numerical tolerances, generation fails before any asset summary is accepted.

## Evidence-state rendering

Every figure contains accessible title and metadata fields. The metadata include:

- claim IDs;
- input source paths;
- generating Git commit when available.

Synthetic and source-conditioned panels are labeled explicitly. No generated asset is permitted to imply external material validation.

Line style, fill state, annotation, and text—not color alone—distinguish model families, branches, and claim states.

## Figure decisions

1. **Forward hierarchy:** conceptual forward chain and evidence states.
2. **Transition distribution:** central latent-law temperatures, conditional widths, crossing probabilities, and local-approximation error.
3. **Herrmann tail:** regenerated spectrum, fit-window-dependent `W_fit/s`, high-`R^2` non-uniqueness, and the declared 4 meV inversion interval.
4. **Chang cutoff:** energy/wavelength versus effective thickness and tail-only versus mixed-branch singular values.
5. **Carrier filling:** parabolic/nonparabolic density dependence, overestimate, high-density decomposition, and density-series conditioning.
6. **Unified rank:** exact spectral overlap, unmarked/marked singular values, and the remaining marked-model null vector.
7. **Measurement design:** external constraints and visible validation-status matrix.

## Table decisions

- Table 1 summarizes the theorem hierarchy.
- Table 2 reads headline quantitative values directly from immutable records.
- Table 3 extracts all 23 claim IDs and their evidence status from the claim matrix.

The generated tables are review assets. Final journal typography may be produced later from the same structured content.

## Validation contract

Merge requires:

- seven parseable SVG files with unique filenames and accessible titles;
- three Markdown tables;
- deterministic byte-for-byte regeneration;
- complete metadata and claim IDs;
- explicit units and synthetic-status labels;
- exact expected filenames;
- numerical regeneration checks against immutable records;
- focused workflow artifact upload;
- full pytest success on Python 3.11 and 3.13.

## Claim boundary

Generated figures and tables are presentation layers for already authorized analytical, numerical, source-reproduction, and bounded synthetic claims.

They do not:

- validate a real HgCdTe specimen;
- convert illustrative parameters into measured material properties;
- identify Urbach energy with composition variance;
- convert local sign probability into a topological phase fraction;
- turn the generic carrier marker into the Dingrong free-carrier law;
- or authorize a universal detector-cutoff correction.

## Next decision after merge

1. visually inspect the generated SVG artifact at publication scale;
2. correct only documented readability or encoding defects while preserving numerical content;
3. execute the DOI acquisition queue;
4. select and complete one external validation route;
5. convert approved SVG assets to final journal PDF format without changing the data contract.
