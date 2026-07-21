# Distributional band-edge flagship manuscript

## Working title

> **From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability**

## Status

The analytical manuscript core was merged in PR #181. Deterministic figure and table generation is implemented on Issue #182 / PR #183 and is pending final CI and merge.

This manuscript is distinct from the completed Paper I:

> *Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.*

Paper I establishes the historical non-identifiability problem. The present manuscript develops a constructive forward theory, exact structural-identifiability results, and measurement-design consequences.

## Central thesis

A measured HgCdTe edge is not generally a scalar function of composition and temperature alone. It is the output of a forward operator involving:

```text
latent signed gap
-> local/specimen distribution
-> carrier and defect state
-> intrinsic and tail absorption
-> optical thickness and instrument response
-> declared edge or cutoff operator
-> reported observable
```

The manuscript's strongest result is structural:

> Under the declared unified single-state spectrum model, five nominal parameters enter through only three independent combinations. Exact null directions cannot be removed by better signal-to-noise or denser spectral sampling.

A calibrated nontranslational carrier-dependent feature raises the rank from three to four but leaves one combined scaling/translation invariance until an independent optical scale is supplied.

## Merged analytical foundation

| Component | Controlling result | Repository record |
|---|---|---|
| Composition-to-gap propagation | local and exact bounded-Gaussian transition distributions | `data/validation/near_critical_transition_model_dependence.json` |
| Gaussian gap convolution | Herrmann approximately-`s/2` scale reproduced; fit-window non-uniqueness | `data/validation/herrmann_gaussian_tail_reproduction.json` |
| Detector cutoff | tail-only cutoff Jacobian rank at most two | `data/validation/chang_2006_cutoff_identifiability.json` |
| Carrier filling | nonparabolic high-density correction and density-series conditioning | `data/validation/dingrong_1985_carrier_filling_sensitivity.json` |
| Unified spectrum | base rank at most three; marked rank four with one combined null | `data/validation/unified_spectrum_structural_rank.json` |

## Manuscript analytical assets

- `manuscript_draft.md` — complete analytical narrative, equations, results, discussion, limitations, and submission boundary;
- `theorem_index.md` — stable proposition/theorem numbering and proof summaries;
- `claim_matrix.md` — claim, evidence class, record, status, authorized wording, and prohibited overstatement;
- `figure_plan.md` — seven-figure scientific and executable-data specification;
- `figure_manifest.json` — machine-readable figure, panel, record, function, filename, and rendering contract;
- `submission_gap.md` — external-validation requirements, publication packaging, and DOI acquisition queue.

Controlling decision:

```text
research/decision_records/2026-07-21-flagship-manuscript-analytical-core.md
```

## Deterministic generated assets

Public command:

```text
python -m tools.build_distributional_band_edge_manuscript_assets \
  --repository-root . \
  --output-dir distributional-generated
```

Generated review package:

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

The builder uses pure Python, NumPy, deterministic SVG, and Markdown. It adds no plotting dependency.

It regenerates and regression-checks:

- the Herrmann source-aligned spectrum and fit-window tail energies;
- the carrier-density nonparabolicity series;
- the unified exact-counterexample spectra;
- every headline value used by the generated tables.

Every SVG contains an accessible title plus metadata identifying claim IDs, source paths, and the generating commit. Synthetic and source-conditioned assets are explicitly labeled. Repeated generation is byte-for-byte deterministic.

The numerical generation core is preserved separately from a thin public presentation wrapper. Artifact inspection changed only line-weight legends, spacing, and display of the committed `2.22e-16` numerical bound.

Controlling decision:

```text
research/decision_records/2026-07-21-flagship-manuscript-assets.md
```

## Stable theorem hierarchy

1. local composition-to-gap propagation;
2. local critical-temperature amplification;
3. Gaussian-gap spectral scale form;
4. exact exponential-tail thickness law;
5. tail-only cutoff rank bound of two;
6. exact Kane-type nonparabolic filling solution;
7. unified unmarked-spectrum rank bound of three;
8. marked-spectrum combined invariance and rank bound of four.

## Headline quantitative results

```text
latent-law central transition span       25.0803 K
Herrmann source-window W_fit/s            0.50504
fit-window increase in apparent W          60.1%
5-to-20 um cutoff energy shift            -16.636 meV
5-to-20 um cutoff wavelength shift         +2.494 um
high-density parabolic BM overestimate    147.323 meV
five-density carrier condition number      11034.75
unmarked unified spectral rank             3 of 5
exact-counterexample maximum difference    2.22e-16
marked unified spectral rank               4 of 5
```

Every value is traceable to an immutable validation record. Synthetic values are not specimen fits.

## Claim-state rules

Every result is labeled as one of:

- exact analytical theorem;
- numerical verification of an exact theorem;
- source reproduction;
- bounded synthetic sensitivity;
- external material validation;
- open hypothesis or validation target.

Synthetic parameters are never presented as inferred specimen properties. Source-specific parameters are not transferred across specimens without provenance.

## DOI-assisted acquisition

The user can assist by locating sources using exact DOIs. The highest-priority queue is maintained in `submission_gap.md` and currently begins with:

```text
10.1016/0038-1098(85)90315-1
10.1007/s11664-007-0162-0
10.1063/1.2245220
10.1016/0022-0248(92)90851-9
10.1016/j.physb.2009.08.210
10.1038/ncomms12576
10.1016/0020-0891(91)90110-2
```

Retrieved papers must pass a source audit before they alter an operator or manuscript claim.

## Current submission boundary

The analytical core and deterministic review assets support a coherent theorem/methods manuscript. Preferred journal submission remains blocked by at least one external validation case using a calibrated real spectrum or same-specimen multi-state dataset with sufficient composition, carrier, thickness, and observation provenance.

The remaining execution order is:

1. complete CI and merge PR #183;
2. audit papers obtained through the DOI queue;
3. complete one external validation route or explicitly authorize theorem/methods-only submission;
4. convert approved SVG assets to final journal PDF format;
5. finish bibliography, archive metadata, authorship, declarations, and journal packaging.

External collaborators are not required for continued progress.
