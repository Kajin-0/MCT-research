# Teppe 2016 primary magneto-optical gap-series decision

**Date:** 2026-07-18  
**Primary source:** Teppe et al., Nature Communications 7, 12576 (2016), DOI `10.1038/ncomms12576`

## Evidence admitted

Five exact primary-source statements or figure labels are admitted:

- Sample A: 5 +/- 2 meV at 2 K;
- Sample A: 28 meV at 57 K;
- Sample A: 36 meV at 77 K;
- Sample A: 56 meV at 120 K;
- Sample B: zero gap at 77 K.

These are magneto-optical zero-field-intercept or gap-closure measurements, not absorption-edge estimates.

## Source inconsistency

Sample A is labeled `x=0.175` in the main text and figures but `x=0.170` in Methods. The difference is large enough to reverse the aggregate model ranking.

Using the figure/text composition, Laurenti has the lowest combined five-point RMSE (`4.2005 meV`). Using the Methods composition, the provisional Hansen-Pade model has the lowest RMSE (`5.0665 meV`), narrowly ahead of Hansen (`5.3533 meV`).

When Sample A composition is profiled separately for each equation, the provisional Hansen-Pade model prefers `x=0.170466` and reaches `1.8558 meV` RMSE, while Laurenti prefers `x=0.175068` and reaches `4.6947 meV`.

## Decision

1. Admit the Teppe series as primary benchmark evidence.
2. Withdraw the statement that the provisional Hansen-Pade model is the globally leading HgCdTe gap law.
3. Retain it only as the leading constrained model within the Seiler specimen regime on which it was validated.
4. Do not promote Laurenti from the Teppe comparison because its ranking depends on selecting one side of the source's unresolved composition conflict.
5. Do not refit any coefficient to these five points.
6. Reopen strict model selection only after Sample A composition is resolved from author records, growth records, or independent metrology.

## Interpretation

This result strengthens the repository's existing conclusion that composition provenance is a first-order part of the observation operator. A `0.005` composition ambiguity is comparable to several meV of gap error and can dominate differences among analytical temperature laws.

## Reproducibility

- validated analysis head: `0a7ec2fb7909f1ef2eafc634c93e46c5666ed1c3`
- workflow run: `29662261465`
- artifact: `8434677608`
- digest: `sha256:ba1b170e868385bdedb513d777d51977e140fd33a140be071f78b02b43c54264`
- compact result: `validation/teppe2016_primary_gap_series_reference_result.json`

## Claim boundary

The gap labels are primary evidence. The composition is not internally consistent within the same publication. The audit therefore supports a provenance and identifiability conclusion, not a universal equation ranking.
