# Distributional band-edge flagship manuscript

## Working title

> **From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability**

## Status

The analytical core, deterministic figures and tables, obtained-source audit, Dingrong Table 1 reproduction, and targeted novelty audit are complete through merged PR #190.

Issue #191 controls journal selection and submission packaging.

This manuscript is distinct from Paper I:

> *Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.*

Paper I establishes the historical non-identifiability problem. The flagship develops the constructive forward model, model-specific identifiability bounds, source-conditioned tests, and measurement-design consequences.

## Selected submission venue

Primary:

> **Semiconductor Science and Technology — Paper**

Fallback:

> **Journal of Applied Physics**

Stretch venue, not ready under the current evidence state:

> **Measurement Science and Technology**

Controlling decision:

```text
research/decision_records/2026-07-21-flagship-journal-and-evidence-threshold.md
data/validation/flagship_journal_submission_gate.json
manuscript/distributional_band_edge/journal_submission/semiconductor_science_and_technology.md
```

Semiconductor Science and Technology is selected because its official scope explicitly includes theoretical semiconductor studies, new analytical techniques, and simulation.

## Initial-submission evidence threshold

The current scientific package is sufficient for initial submission to Semiconductor Science and Technology after final packaging.

A newly digitized spectrum is **not required before initial submission**.

The Dingrong source-table reproduction is presented as qualified real-specimen evidence, not complete spectrum validation. Digitization is reserved for an explicit editor/reviewer request or a newly available calibratable dataset that materially changes submission risk.

Measurement Science and Technology would require a calibrated spectrum, quantified uncertainty, method-performance demonstration, and a baseline comparison before submission.

## Publication framing

The manuscript is an **HgCdTe-specific semiconductor optical-metrology and inverse-problem methods paper**.

It is not presented as:

- new general structural-identifiability theory;
- a universal HgCdTe bandgap equation;
- a complete microscopic absorption theory;
- a completely externally validated detector model.

Structural identifiability, parameter symmetries, identifiable parameter combinations, and the Beer-Lambert optical-depth product are prior art. The contribution is their source-grounded HgCdTe application: explicit parameter combinations, model-specific rank bounds, exact counterexamples, quantitative operator effects, and required external measurements.

Controlling novelty audit:

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

The dense-spectrum Jacobian therefore has rank at most three. The amplitude-thickness combination is inherited from optical-depth physics; the explicit HgCdTe gap-carrier combination and combined rank bound are application-specific.

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
| Journal gate | venue and evidence threshold | `data/validation/flagship_journal_submission_gate.json` |

## Dingrong external source-table result

For the real `x=0.19`, `n=7e17 cm^-3` specimen, the printed finite-temperature density equation with

```text
P = 8.0e-8 eV cm
```

misses the four reported Fermi elevations by `11.297 meV` RMS. The rounded rows imply a diagnostic mean near

```text
P = 8.5107e-8 eV cm
```

which reduces the RMS mismatch to `0.785 meV`. This is a source-consistency inference, not a revised universal momentum matrix. The source's filled-edge and operational optical-gap values agree within `0-4 meV`.

## Chang route disposition

Chang 2006/2007 provide the nonparabolic-Urbach model and calculated effective-thickness cutoff dependence. Their published thickness curve is not an independent measured same-specimen series and is not used as external validation.

## Bibliography state

Core novelty, inverse-problem, optical-inversion, and HgCdTe source metadata are verified in:

```text
manuscript/distributional_band_edge/references_verified.json
```

Remaining bibliography work is mechanical generation of journal-style references and final verification of secondary historical gap-law citations.

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

## Remaining submission gates

1. generate the journal-style bibliography from the verified manifest;
2. convert vector figures to accepted journal format without numerical change;
3. create the archive release and DOI;
4. complete author, affiliation, CRediT, funding, conflict, and reviewer metadata;
5. finalize the SST cover letter and manuscript formatting;
6. perform final independent wording and PDF review.

No additional digitization, figure infrastructure, route scoring, or broad mechanism branch is authorized before initial SST submission.
