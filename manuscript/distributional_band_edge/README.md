# Distributional band-edge flagship manuscript

## Working title

> **From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability**

## Status

The analytical core, deterministic figures and tables, DOI intake, Dingrong Table 1 reproduction, and targeted novelty audit are complete on the repository branches and merged work through PR #188. Issue #189 controls the final prior-art and publication-framing gate.

This manuscript is distinct from Paper I:

> *Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.*

Paper I establishes the historical non-identifiability problem. The flagship manuscript develops a constructive forward model, model-specific identifiability bounds, source-conditioned tests, and measurement-design consequences.

## Publication framing

The manuscript is an **HgCdTe-specific semiconductor optical-metrology and inverse-problem methods paper**.

It is not presented as:

- new general structural-identifiability theory;
- a universal HgCdTe bandgap equation;
- a complete microscopic absorption theory;
- a completely externally validated detector model.

Structural identifiability, parameter symmetries, identifiable parameter combinations, and the Beer-Lambert optical-depth product are prior art. The candidate contribution is their source-grounded HgCdTe application: explicit parameter combinations, model-specific rank bounds, exact counterexamples, quantitative operator effects, and required external measurements.

Controlling audit:

```text
literature/prior_art/2026-07-21-flagship-rank-theorem-audit.md
data/validation/flagship_novelty_claim_matrix.json
research/decision_records/2026-07-21-flagship-publication-framing.md
```

## Forward hierarchy

```text
latent signed gap
-> local/specimen distribution
-> carrier and defect state
-> intrinsic, tail, and free-carrier absorption
-> effective optical thickness and instrument response
-> declared edge or cutoff operator
-> reported observable
```

## Central model-specific result

Under the declared Gaussian-gap, power-law local edge, uniform carrier translation, and single-pass response, five nominal parameters enter only through:

```text
Eg0 + Delta_carrier
sigma_G
A*d
```

Therefore the dense-spectrum Jacobian has rank at most three. The amplitude-thickness combination is inherited from optical-depth physics; the explicit HgCdTe gap-carrier combination and combined rank bound are the application-specific result.

A controlled nontranslational carrier feature raises rank to four but leaves one combined invariance until an independent scale is supplied.

## Evidence foundation

| Component | Result | Record |
|---|---|---|
| Composition distribution | exact bounded transition distributions and root censoring | `data/validation/near_critical_transition_model_dependence.json` |
| Gaussian gap convolution | Herrmann scale reproduced; 60.1% fit-window change | `data/validation/herrmann_gaussian_tail_reproduction.json` |
| Detector cutoff | model-specific tail-only rank at most two | `data/validation/chang_2006_cutoff_identifiability.json` |
| Carrier sensitivity | nonparabolic high-density sensitivity and conditioning | `data/validation/dingrong_1985_carrier_filling_sensitivity.json` |
| Dingrong source test | finite-temperature Table 1 reproduction and printed-parameter audit | `data/validation/dingrong1985_table1_reproduction.json` |
| Unified spectrum | rank at most three; marked rank four with one null | `data/validation/unified_spectrum_structural_rank.json` |
| Novelty boundary | red/yellow/green claim audit | `data/validation/flagship_novelty_claim_matrix.json` |

## Dingrong external source-table result

For the real `x=0.19`, `n=7e17 cm^-3` specimen, the printed finite-temperature density equation with printed

```text
P = 8.0e-8 eV cm
```

misses the four reported Fermi elevations by `11.297 meV` RMS. The rounded rows imply a diagnostic mean near

```text
P = 8.5107e-8 eV cm
```

which reduces the Fermi-shift RMS mismatch to `0.785 meV`. This is a source-consistency inference, not a revised universal momentum matrix. The source's filled-edge and operational optical-gap values agree within `0-4 meV`.

The result is qualified source-table evidence, not complete native-spectrum validation.

## Chang route disposition

Chang 2006/2007 provide the nonparabolic-Urbach model and calculated effective-thickness cutoff dependence. Their published thickness curve is not an independent measured same-specimen series and is not used as external validation.

The exact logarithmic tail shift is treated as an inherited forward-model consequence. The project-specific result is the tail-only rank-two bound and mixed-branch conditioning analysis.

## Manuscript assets

- `manuscript_draft.md` — revised source-aware manuscript;
- `theorem_index.md` — stable exact statements and proof summaries;
- `claim_matrix.md` — evidence and audited novelty wording;
- `figure_plan.md` and `figure_manifest.json` — deterministic seven-figure contract;
- `submission_gap.md` — remaining scientific and administrative gates.

## Deterministic asset generation

```text
python -m tools.build_distributional_band_edge_manuscript_assets \
  --repository-root . \
  --output-dir distributional-generated
```

Outputs:

```text
7 deterministic SVG figures
3 Markdown tables
1 machine-readable asset summary
```

The builder regenerates numerical content from immutable records and fails closed on disagreement.

## Headline results

```text
latent-law transition span                 25.0803 K
Herrmann source-window W_fit/s              0.50504
fit-window increase in apparent W            60.1%
5-to-20 um synthetic cutoff shift          -16.636 meV
tail-only cutoff rank                       <= 2
mixed-branch condition number               199.81
synthetic parabolic BM overestimate         147.323 meV
five-density condition number             11034.75
Dingrong printed-P Fermi-shift RMS error     11.297 meV
unmarked unified spectral rank               3 of 5
exact-counterexample maximum difference      2.22e-16
marked unified spectral rank                 4 of 5
```

Synthetic values are not specimen fits.

## Claim-state rules

Every result is classified as:

- exact statement under declared assumptions;
- numerical verification;
- source-conditioned reproduction;
- bounded synthetic sensitivity;
- external material validation;
- open validation target.

A theorem label denotes exactness under assumptions, not unprecedented mathematics.

## Current submission boundary

The manuscript now has:

- a complete analytical narrative;
- deterministic figures and tables;
- a qualified real-specimen source-table test;
- an audited novelty boundary;
- version-controlled code and immutable numerical records.

Remaining gates are:

1. complete bibliography and citation verification;
2. decide whether the selected journal requires a digitized calibrated real spectrum beyond the Dingrong source table;
3. convert vector figures to journal format;
4. complete archive DOI, authorship, affiliation, CRediT, funding, conflict, and data/code statements;
5. final independent wording review.

No additional figure styling, route scoring, metadata framework, or broad mechanism branch is authorized unless it directly closes one of these gates.
