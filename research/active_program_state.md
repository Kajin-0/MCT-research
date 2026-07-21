# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #167  
**Active milestone:** #191  
**Execution mode:** independent, public-data-first, reproducible computation

This is the sole controlling research ledger. `research/active_progress.md` is retired.

## Completed Paper I

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction**

Paper I is scientifically frozen. Remaining work is administrative submission packaging.

## Active flagship manuscript

> **From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability**

Controlling forward chain:

```text
latent signed gap
-> composition/gap distribution
-> carrier and defect state
-> intrinsic, tail, and free-carrier response
-> effective thickness and instrument response
-> declared observation operator
-> reported observable
```

Completed milestones:

```text
PR #181  analytical manuscript core
PR #183  deterministic seven-figure and three-table pipeline
PR #185  DOI intake and validation-route gate
PR #188  Dingrong Table 1 reproduction and source-state correction
PR #190  prior-art audit and novelty boundary
```

## Selected journal and evidence threshold

Issue #191 selects the primary submission venue:

> **Semiconductor Science and Technology — Paper**

Fallback:

> **Journal of Applied Physics**

Stretch venue not ready under the current evidence state:

> **Measurement Science and Technology**

Controlling files:

```text
data/validation/flagship_journal_submission_gate.json
research/decision_records/2026-07-21-flagship-journal-and-evidence-threshold.md
manuscript/distributional_band_edge/journal_submission/semiconductor_science_and_technology.md
manuscript/distributional_band_edge/references_verified.json
```

Semiconductor Science and Technology is selected because its official scope directly includes theoretical semiconductor studies, new analytical techniques, and simulation.

The present analytical, numerical, source-conditioned, and Dingrong source-table evidence is sufficient for initial submission after packaging.

A newly digitized spectrum is **not required before initial submission**.

Digitization is reserved for:

1. an explicit editor or reviewer request;
2. a newly available source-native or calibratable spectrum with sufficient provenance;
3. a pre-submission editorial statement that the current source-table evidence is insufficient.

Measurement Science and Technology would require a calibrated spectrum, quantified uncertainty, performance demonstration, and baseline comparison before submission.

## Publication framing

The manuscript is:

> **an HgCdTe-specific semiconductor optical-metrology and inverse-problem methods paper**

It is not:

- new general structural-identifiability theory;
- a universal HgCdTe bandgap equation;
- a complete microscopic absorption theory;
- a completely externally validated detector model.

Established prior art includes structural identifiability, parameter symmetries, identifiable combinations, the Beer-Lambert optical-depth product, thickness-dependent detector cutoff, and Gaussian-gap-induced apparent tails.

Candidate application-specific contributions are:

- explicit HgCdTe combinations `Eg0+Delta`, `sigma_G`, and `A*d`;
- the rank-three bound for the declared distributed spectrum;
- the tail-only Chang rank-two bound;
- the marked-model combined null vector;
- the exact five-parameter spectral counterexample;
- quantified fit-window and mixed-branch effects;
- the Dingrong printed-parameter consistency result;
- the external-measurement prescription implied by the symmetries.

## Central model-specific result

For the declared Gaussian-gap, power-law local edge, uniform carrier translation, and single-pass response, five nominal parameters

```text
Eg0
Delta_carrier
ln sigma_G
ln A
ln d
```

enter only through

```text
Eg0 + Delta_carrier
sigma_G
A*d
```

Therefore

```text
dR/dEg0 = dR/dDelta_carrier
dR/dlnA = dR/dlnd
rank(J) <= 3
```

Two parameter sets preserving the three combinations generate 281-point spectra with maximum difference `2.22e-16`.

A controlled nontranslational carrier marker raises rank to four but leaves one combined null direction. The marker is not the Dingrong free-carrier absorption law.

## Supporting quantitative results

```text
central near-critical latent-law span                25.0803 K
maximum conditional-width linearization error         9.657 K
Herrmann source-window W_fit/s                         0.50504
fit-window increase in apparent W                       60.1%
5-to-20 um synthetic cutoff energy shift             -16.636 meV
5-to-20 um synthetic cutoff wavelength shift          +2.494 um
tail-only cutoff rank                                  <= 2
mixed-branch condition number                         199.81
illustrative high-density parabolic overestimate      147.323 meV
five-density illustrative condition number          11034.75
Dingrong printed-P Fermi-shift RMS discrepancy         11.297 meV
Dingrong row-implied-P Fermi-shift RMS discrepancy      0.785 meV
```

Synthetic values are not specimen fits.

## Dingrong source-table evidence

The real source specimen has:

```text
x                         0.19
carrier type              n-type
Hall density              7.0e17 cm^-3
transmission thickness    0.16 mm
refractive index used     3.5
spectral interval         7-17 um
temperatures              77, 100, 200, 300 K
edge operator             extrapolation to 2000 cm^-1
```

The printed finite-temperature density equation with printed

```text
P = 8.0e-8 eV cm
```

undershoots the four reported Fermi elevations by RMS `11.297 meV`.

The rounded rows imply a diagnostic mean

```text
P = 8.5107e-8 eV cm
```

which reduces the RMS discrepancy to `0.785 meV`. It is not a revised universal material constant.

The source filled edge and operational optical gap differ by `0-4 meV`, RMS `2.915 meV`.

This is qualified real-specimen source-table evidence, not complete native-spectrum validation.

## Chang disposition

Chang 2007 Figure 1 is a calculated detector-cutoff curve, not an independent measured same-specimen thickness series. It is not external validation.

Chang remains prior art and a source-bounded model basis. The tail-only rank result is analytical.

## Bibliography state

Core metadata are verified in:

```text
manuscript/distributional_band_edge/references_verified.json
```

The manifest covers the central structural-identifiability, parameter-symmetry, optical-inversion, effective-thickness, and HgCdTe mechanism sources.

Remaining bibliography work is:

1. generate SST-style references;
2. verify secondary historical gap-law citations;
3. freeze citation numbering after the final reference set.

## Submission package state

Prepared:

- journal selection and evidence threshold;
- journal-positioning paragraph;
- SST cover-letter draft;
- data and code availability statements;
- restricted-source statement;
- single-author CRediT template;
- funding and conflict templates;
- submission checklist.

Remaining critical path:

1. merge Issue #191 after CI;
2. generate the SST-style bibliography;
3. convert approved SVGs to accepted journal vector format;
4. create archive release and DOI;
5. complete author, affiliation, reviewer, and declaration metadata;
6. finalize SST manuscript formatting and cover letter;
7. perform final independent wording and PDF review;
8. tag the submission release after all workflows pass.

## Explicitly unauthorized before initial SST submission

- speculative spectrum digitization;
- reopening journal ranking without new editorial evidence;
- new route-scoring infrastructure;
- new manuscript architecture;
- additional figure-design systems;
- broad new physical mechanism branches;
- presenting general identifiability or Beer-Lambert structure as new;
- presenting Chang's calculated curve as external validation;
- treating Dingrong's row-implied `P` as universal;
- claiming complete free-carrier-spectrum validation;
- requiring collaborators;
- escalating to expensive first-principles work without a submission-changing need.
