# Distributional band-edge flagship manuscript

## Working title

> **From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability**

## Status

Analytical manuscript core in active development.

This manuscript is distinct from the completed Paper I:

> *Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.*

Paper I establishes the historical non-identifiability problem. The present manuscript develops a constructive forward theory and exact structural-identifiability results.

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

## Merged analytical foundation

| Component | Controlling result | Repository record |
|---|---|---|
| Composition-to-gap propagation | local and exact bounded-Gaussian transition distributions | `data/validation/near_critical_transition_model_dependence.json` |
| Gaussian gap convolution | Herrmann approximately-`s/2` scale reproduced; fit-window non-uniqueness | `data/validation/herrmann_gaussian_tail_reproduction.json` |
| Detector cutoff | tail-only cutoff Jacobian rank at most two | `data/validation/chang_2006_cutoff_identifiability.json` |
| Carrier filling | nonparabolic high-density correction and density-series conditioning | `data/validation/dingrong_1985_carrier_filling_sensitivity.json` |
| Unified spectrum | base rank at most three; marked rank four with one combined null | `data/validation/unified_spectrum_structural_rank.json` |

## Manuscript assets

- `manuscript_draft.md` — scientific narrative and equations;
- `claim_matrix.md` — claim, evidence, status, and prohibited overstatement;
- `figure_plan.md` — executable figure definitions and intended message;
- `submission_gap.md` — remaining work before journal submission.

## Claim-state rules

Every result is labeled as one of:

- exact analytical theorem;
- numerical verification of an exact theorem;
- source reproduction;
- bounded synthetic sensitivity;
- external material validation;
- open hypothesis.

Synthetic parameters are never presented as inferred specimen properties. Source-specific parameters are not transferred across specimens without provenance.

## Current submission boundary

The analytical core is strong enough to draft now. Journal submission remains blocked by at least one external validation case using a calibrated real spectrum or same-specimen multi-state dataset with sufficient composition, carrier, thickness, and observation provenance.
