# Submission gap and publication gate

## Current state

The flagship manuscript has:

- a revised analytical draft;
- stable exact-statement numbering;
- a C01-C23 evidence matrix;
- a red/yellow/green novelty audit;
- six controlling numerical/source records;
- seven deterministic SVG figures;
- three deterministic manuscript tables;
- complete Python 3.11/3.13 CI coverage;
- an audited source-intake record;
- a qualified real-specimen Dingrong Table 1 reproduction;
- a selected journal and locked initial-submission evidence threshold;
- a verified core bibliography manifest.

## Selected venue

Primary:

> **Semiconductor Science and Technology — Paper**

Fallback:

> **Journal of Applied Physics**

Stretch venue, not ready under the current evidence state:

> **Measurement Science and Technology**

Controlling files:

```text
data/validation/flagship_journal_submission_gate.json
research/decision_records/2026-07-21-flagship-journal-and-evidence-threshold.md
manuscript/distributional_band_edge/journal_submission/semiconductor_science_and_technology.md
```

Semiconductor Science and Technology is selected because its official scope directly includes theoretical semiconductor studies, new analytical techniques, and simulation.

## Locked evidence threshold

The current scientific package is sufficient for initial submission to Semiconductor Science and Technology after final packaging.

A newly digitized spectrum is **not required before initial submission**.

Digitization is authorized only when:

1. an editor or reviewer explicitly requests a full-spectrum demonstration;
2. a source-native or calibratable spectrum becomes available with sufficient specimen and axis provenance;
3. a pre-submission editorial inquiry states that the Dingrong source-table evidence is insufficient.

Do not digitize a spectrum merely to make the paper appear more empirical.

Measurement Science and Technology would require a calibrated spectrum, explicit uncertainty, method-performance demonstration, and baseline comparison before submission. The current package does not satisfy that venue's evidence threshold.

## Scientific evidence already present

### Analytical and numerical foundation

The repository contains:

- exact bounded composition-to-gap propagation;
- transition-root censoring analysis;
- Herrmann source-scale reproduction;
- quantified fit-window non-uniqueness;
- Chang source-bounded cutoff and rank analysis;
- nonparabolic carrier sensitivity and conditioning;
- unified model-specific rank bounds and exact counterexample.

### Qualified external source-table evidence

Dingrong et al. provide a real `x=0.19`, `n=7e17 cm^-3` specimen at 77, 100, 200, and 300 K. The repository reproduces the finite-temperature density-equation structure and audits Table 1.

Controlling record:

```text
data/validation/dingrong1985_table1_reproduction.json
```

Result:

```text
printed P = 8.0e-8 eV cm
Fermi-shift RMS mismatch = 11.297 meV
row-implied mean P = 8.5107e-8 eV cm
row-implied-mean RMS mismatch = 0.785 meV
source filled-edge versus operational optical-gap difference = 0-4 meV
```

The row-implied momentum matrix is a source-consistency diagnostic, not a revised universal constant. This is qualified real-specimen source-table evidence, not complete native-spectrum validation.

## Rejected Chang validation route

The Chang 2007 effective-thickness cutoff curve is calculated. It is not an independent same-specimen series of measured spectra or detector responses. The papers do not supply the covariance, effective-thickness calibration, and complete shared specimen parameters required for the previously declared validation.

Chang remains important prior art and a source-bounded analytical basis. Its calculated curve is not described as external validation.

## Novelty boundary

Controlling files:

```text
literature/prior_art/2026-07-21-flagship-rank-theorem-audit.md
data/validation/flagship_novelty_claim_matrix.json
research/decision_records/2026-07-21-flagship-publication-framing.md
```

Do not claim novelty for:

- structural identifiability as a concept;
- parameter-symmetry methods;
- identifiable parameter combinations;
- the Beer-Lambert optical-depth product;
- thickness-dependent cutoff physics;
- Gaussian gap distributions producing near-exponential tails.

Candidate application-specific contributions are:

- explicit HgCdTe identifiable combinations;
- the declared spectrum rank-three bound;
- the tail-only Chang rank-two bound;
- the marked-model combined null vector;
- the machine-precision counterexample;
- quantified fit-window and mixed-branch results;
- the Dingrong printed-parameter inconsistency;
- the resulting measurement-design prescription.

Theorem labels indicate exactness under assumptions, not unprecedented general mathematics.

## Bibliography gate

Core metadata are verified in:

```text
manuscript/distributional_band_edge/references_verified.json
```

The manifest contains verified DOI, author order, title, journal/source, year, volume, issue, and pages or article number for:

- foundational structural-identifiability sources;
- parameter-symmetry and identifiable-combination methods;
- Beer-Lambert and thin-film optical inversion sources;
- Herrmann, Chang, Dingrong, Teppe, Ivanov-Omskii, and Chu HgCdTe sources.

### Retained source-provenance DOI set

The original seven source-acquisition identifiers remain explicit because they define the historical evidence and validation provenance even when a source is already obtained or a route is rejected:

```text
10.1016/0038-1098(85)90315-1
10.1007/s11664-007-0162-0
10.1063/1.2245220
10.1016/0022-0248(92)90851-9
10.1016/j.physb.2009.08.210
10.1038/ncomms12576
10.1016/0020-0891(91)90110-2
```

Their presence is a provenance contract, not an assertion that every route remains active.

Remaining bibliography work:

1. generate SST-style references from the manifest;
2. verify secondary historical gap-law citations;
3. freeze numbering only after the final reference set is complete.

## Figure and table gate

The deterministic builder is complete:

```text
python -m tools.build_distributional_band_edge_manuscript_assets \
  --repository-root . \
  --output-dir distributional-generated
```

Remaining work is journal-format conversion only:

- convert accepted SVGs to the required vector format;
- preserve vector text and line weights;
- verify final column-width readability;
- do not change numerical content during styling;
- regenerate tables from immutable records.

## Journal-facing package

Prepared in:

```text
manuscript/distributional_band_edge/journal_submission/semiconductor_science_and_technology.md
```

It contains:

- article type and scope fit;
- journal-positioning paragraph;
- cover-letter draft;
- data and code availability statements;
- restricted-source statement;
- single-author CRediT template;
- funding and conflict templates;
- submission checklist.

## Administrative packaging

Still required:

- author name and affiliation;
- correspondence address;
- final CRediT statement;
- confirmed funding statement;
- conflict-of-interest statement;
- archive release and DOI;
- suggested reviewers and exclusions;
- final SST formatting and word count;
- submission PDF inspection.

## Submission decision rule

Initial SST submission is authorized when:

1. Issue #191 is merged;
2. journal-style bibliography and secondary-citation verification are complete;
3. vector figures and tables are converted without numerical change;
4. archive and administrative metadata are complete;
5. final independent wording review finds no unsupported novelty or specimen claim;
6. all workflows pass on the submission tag.

A full digitized spectrum is not on this critical path.

## Work freeze

Until an SST editor or reviewer changes the evidence requirement, do not add:

- new route-ranking infrastructure;
- new manuscript architecture;
- additional figure-design systems;
- broad new physical mechanism branches;
- speculative spectrum digitization;
- expensive first-principles calculations;
- collaborator-dependent validation requirements.

External collaborators are not required for continued progress.
