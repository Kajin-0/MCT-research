# Primary HgCdTe gap source recovery gate

**Date:** 2026-07-18  
**Status:** active evidence gate  
**Decision:** do not reopen static band-gap fitting from formulas, abstracts, or secondary tables.

## Question

Can the historical literature currently available to the repository supply a second independent, primary, point-level `x-Eg-T` dataset with sufficient composition and measurement provenance to reopen the HgCdTe static composition law?

## Fit-authority requirements

A source is full point-level fit authority only when all of the following are recovered:

1. primary full text;
2. point-level gap observations;
3. composition measurement method or independently auditable composition provenance;
4. pointwise uncertainty or enough raw information to reconstruct it;
5. the operational gap/edge measurement definition.

A published empirical equation is a model comparator, not a substitute for its source observations. A secondary transcription is a screen, not primary fit authority.

## Recovery results

### Chu, Mi and Tang — Infrared Physics 32 (1991), 195-211

- DOI: `10.1016/0020-0891(91)90110-2`
- Primary abstract/metadata recovered.
- Reported scope: intrinsic optical absorption of thin films made from bulk HgCdTe, `x = 0.165-0.45`, `T = 4.2-300 K`.
- The abstract states that fitted absorption curves produced `Eg`, momentum matrix, heavy-hole mass and spin-orbit splitting, and that Burstein-Moss shift and Urbach tails were discussed.
- Full text, point table, composition method and point uncertainty were not recovered.
- Status: **blocked**.

### Chu, Mi and Tang — Journal of Applied Physics 71 (1992), 3955-3961

- DOI: `10.1063/1.350867`
- Primary abstract/metadata recovered.
- Reported scope: samples thinner than `10 um`, `x = 0.170-0.443`, `T = 4.2-300 K`.
- The abstract defines the reported gap at the transition between the Urbach exponential region and the Kane intrinsic-absorption region.
- The composition range exactly matches the eight-point secondary Chu-Sher Table 4.4 screen, making this the highest-priority primary recovery target.
- Full text, point table, composition method and point uncertainty were not recovered.
- Status: **blocked**.

### Scott — Journal of Applied Physics 40 (1969), 4077-4081

- DOI: `10.1063/1.1657147`
- Primary abstract/metadata and empirical equation recovered.
- Reported scope: optical absorption edge, `x = 0.23-0.61`, `T = 10-300 K`.
- Point-level observations, composition method and point uncertainty were not recovered.
- Status: **blocked**.

### Schmit and Stelzer — Journal of Applied Physics 40 (1969), 4865-4869

- DOI: `10.1063/1.1657304`
- Primary abstract/metadata and empirical equation recovered.
- Reported scope: photoconductive and photovoltaic cutoff measurements, approximately `x = 0.17-0.60`, `T = 20-300 K`.
- Spectral-response points, composition provenance and uncertainty were not recovered.
- Status: **blocked**.

### Hansen, Schmit and Casselman — Journal of Applied Physics 53 (1982), 7099-7101

- DOI: `10.1063/1.330018`
- Primary metadata and the final empirical equation recovered.
- The paper reports combining 22 studies and a standard error near `0.013 eV`.
- The 22-study observation ledger, source-specific measurement definitions, weights and uncertainties were not recovered.
- Status: **blocked**.

### Chu, Xu and Tang — Applied Physics Letters 43 (1983), 1064-1066

- DOI: `10.1063/1.94237`
- Primary formula and declared range recovered: `0 <= x <= 0.37` plus `x = 1`, `T = 4.2-300 K`.
- Point-level optical data and composition provenance were not recovered.
- Status: **blocked**.

### Seiler, Lowney, Littler and Yoon — JVST (1990)

- DOI: `10.1116/1.576952`
- Primary PDF, digitized temperature series, measurement definitions and gap uncertainties are present in the repository.
- Only one temperature-series specimen has independently tied composition; specimen offsets are profiled in the shape test.
- Status: **conditional**, not sufficient by itself for a universal static refit.

### Chu and Sher Table 4.4 (2008)

- DOI: `10.1007/978-0-387-74801-6`
- Eight room-temperature points are available as a secondary transcription attributed to the Chu-Mi-Tang absorption experiments.
- Primary composition metrology and point uncertainties are absent.
- Status: **screen-only**.

## Decision

No primary historical source currently satisfies the complete point-level fit-authority requirements. Therefore:

- a new static composition refit is not authorized;
- the provisional Hansen-Pade temperature kernel remains unchanged;
- the Chu-Sher secondary points remain an external screen only;
- abstracts and historical formulas remain model comparators only;
- no figure digitization will be treated as primary evidence unless the actual primary page image, axis calibration, measurement definition and uncertainty treatment are archived.

## Recovery priority

1. Obtain the complete 1992 Journal of Applied Physics article (`10.1063/1.350867`) because its composition range matches the secondary eight-point table and its gap definition is directly relevant.
2. Obtain the complete 1991 Infrared Physics article (`10.1016/0020-0891(91)90110-2`) to recover sample, carrier and Burstein-Moss metadata.
3. Obtain Scott 1969 and Schmit-Stelzer 1969 point tables or calibrated figures with sample composition methods.
4. Reconstruct Hansen 1982's 22-source ledger before treating Hansen residuals as homogeneous measurement noise.
5. Prefer a new common-specimen paired dataset over further historical coefficient fitting if these sources cannot be recovered.

## Reopen condition

Static-law development may resume only when at least two independent primary point-level sources pass the declared requirements, or when the eight-specimen paired acquisition design is executed with independent composition, magneto-optical gap, absorption spectrum, Hall data and vacancy-sensitive metadata.

## Machine-readable record

- `data/evidence/hgcdte_primary_gap_source_recovery.csv`
- `tools/audit_primary_gap_source_recovery.py`
- `tests/test_primary_gap_source_recovery.py`
