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
- a qualified real-specimen Dingrong Table 1 reproduction.

The manuscript is now a credible **HgCdTe semiconductor optical-metrology and inverse-problem methods** paper in preparation. It is not yet ready for submission because bibliography verification, venue-specific validation policy, and administrative packaging remain incomplete.

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

The row-implied momentum matrix is a source-consistency diagnostic, not a revised universal constant.

This evidence tests a real source-defined carrier branch and edge operator, but it is not complete native-spectrum validation.

## Rejected validation route

The previously selected Chang published-paper multi-thickness route is rejected.

The Chang 2007 effective-thickness cutoff curve is calculated. It is not an independent same-specimen series of measured spectra or detector responses. The papers do not supply the covariance, effective-thickness calibration, and complete shared specimen parameters required for the declared validation.

Chang remains important prior art and a source-bounded analytical basis. Its calculated curve is not described as external validation.

## Remaining scientific decision

The next decision is venue dependent:

> Is the qualified Dingrong source-table reproduction sufficient for an analytical/metrology methods paper, or does the selected journal require one digitized calibrated spectrum?

A digitized spectrum is authorized only if it changes this submission decision.

### A qualifying spectrum should preserve

- source figure or table identity;
- digitization calibration and uncertainty;
- composition and temperature;
- carrier type and density;
- physical thickness and effective thickness separately;
- reflectance/transmission convention;
- spectral resolution;
- edge or cutoff operator;
- parameter ownership and nuisance assumptions.

A spectrum need not identify every unified-model parameter. It must test a declared prediction while leaving unresolved quantities as nuisance or bounded parameters.

### Rejection gates for digitized validation

Do not promote a digitized case when:

- axes or curve identity cannot be calibrated;
- specimen state changes across curves without provenance;
- effective thickness is silently replaced by physical thickness;
- carrier state is inferred from the same edge being tested;
- source-specific parameters are transferred between specimens;
- the only agreement comes from unconstrained amplitude or offset fitting;
- digitization uncertainty is comparable to or larger than the claimed effect.

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

Before submission, verify full metadata and manuscript placement for:

### General inverse-problem sources

```text
10.1016/0025-5564(70)90132-X
10.1016/j.automatica.2009.07.009
10.1016/j.mbs.2014.08.008
```

### Optical-depth and thin-film inversion sources

```text
10.1351/goldbook.B00626
10.1364/AO.36.008238
10.1364/AO.40.002675
10.1364/AO.40.002682
10.1364/OL.418277
```

### HgCdTe mechanism sources

```text
10.1016/0022-0248(92)90851-9
10.1063/1.2245220
10.1007/s11664-007-0162-0
10.1016/0038-1098(85)90315-1
10.1016/j.physb.2009.08.210
10.1038/ncomms12576
10.1016/0020-0891(91)90110-2
```

Verify title, author order, journal, year, volume, issue, page/article number, and DOI. Distinguish source results from repository inferences in every citation sentence.

## Figure and table gate

The deterministic builder is complete:

```text
python -m tools.build_distributional_band_edge_manuscript_assets \
  --repository-root . \
  --output-dir distributional-generated
```

Remaining work is journal-format conversion only:

- convert accepted SVGs to the required PDF/EPS format;
- preserve vector text and line weights;
- verify final column-width readability;
- do not change numerical content during styling;
- regenerate tables from immutable records.

## Administrative packaging

Required:

- author name and affiliation;
- correspondence address;
- CRediT statement;
- funding statement;
- conflict-of-interest statement;
- data and code availability statement;
- restricted-source handling statement;
- archive release and DOI;
- cover letter;
- suggested reviewers and exclusions;
- journal-specific formatting and word count.

## Submission decision rule

Submission is authorized when:

1. Issue #189 novelty wording and CI are complete;
2. bibliography metadata and citation boundaries are verified;
3. a target venue is selected;
4. the venue-specific decision on source-table versus digitized-spectrum evidence is recorded;
5. figures and tables are converted without numerical change;
6. archive and administrative metadata are complete;
7. final independent wording review finds no unsupported novelty or specimen claim.

## Work freeze

Until a submission gate directly requires it, do not add:

- new route-ranking infrastructure;
- new manuscript architecture;
- additional figure styling systems;
- broad new physical mechanism branches;
- expensive first-principles calculations;
- collaborator-dependent validation requirements.

External collaborators are not required for continued progress.
