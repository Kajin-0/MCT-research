# Decision record: R01 temperature-benchmark eligibility

**Date:** 2026-07-23  
**Program:** R01 — empirical bandgap reconstruction  
**Parent benchmark:** #8  
**Issue:** #320

## Decision

```text
class_specific_single_source_benchmarks_only
```

The repository now contains four E1-eligible specimen-level temperature-series ledgers, but they occupy four different exact operational measurement classes. No class contains the two independent sources required for source-held-out analytical-model ranking.

## Immutable evidence

```text
canonical result
  data/validation/r01_temperature_benchmark_eligibility.json

canonical JSON SHA256
  f6760549685f53980ff8dfb9a36fba8b0019dfa02419edd0f75b39579d56d201

candidate workflow run
  30012926375

candidate artifact
  8565889560

candidate artifact digest
  sha256:1c849b96b2d1155c6af53049ad18908b1a8a27f2d143ab81e9b5ef760c6be4eb
```

The candidate was generated twice and compared byte-for-byte before publication.

## Source graph

| Source | Rows | Temperature-series specimens | Exact measurement class | Absolute-gap eligible series |
|---|---:|---:|---|---:|
| Seiler 1990 | 34 | 3 | `two_photon_magnetoabsorption_modified_Pidgeon_Brown_gap` | 1 |
| Chu 1991 | 7 | 1 | `absorption_turning_point_edge` | 0 |
| Scott 1969 | 70 | 9 | `fixed_absorption_optical_edge_alpha_500_cm_inverse` | 0 |
| Schmit and Stelzer 1969 | 56 | 8 | `detector_half_peak_spectral_response_cutoff` | 0 |

Total:

```text
sources                         4
observations                  167
temperature-series specimens   21
exact measurement classes       4
maximum sources in one class    1
```

## E1 — source-ledger eligibility

All four sources pass the source-ledger gate:

- numerical records are committed and auditable;
- repeated temperatures retain specimen identity;
- exact operational measurement class is explicit;
- composition provenance is explicit;
- uncertainty semantics are explicit, including unknown covariance;
- source lineage and circularity are explicit.

This does not make the four observables interchangeable.

## Exact-class separation

The following identities are prohibited:

```text
TPMA gap
!= absorption turning-point edge
!= alpha=500 cm^-1 fixed-absorption edge
!= detector half-peak cutoff.
```

No independently validated repository observation operator maps these classes onto one common numerical target. Therefore, the source graph has four disconnected class components, each containing one source.

## Gate results

```text
E1 all in-scope source ledgers eligible        true
E2 any exact-class source holdout authorized   false
E3 any exact-class absolute ranking authorized false
E4 universal model advancement authorized      false
```

### Why E2 fails

Every exact class has one source. A leave-one-source-out fold would have no training source within the held-out observation class.

### Why E3 fails

Seiler sample 3 is the only independently composed absolute temperature series among the four counted ledgers. Its TPMA class has no second independent source. Scott and Schmit provide multiple measured-composition specimen series, but their fixed-alpha and detector-cutoff observables are explicitly nonintrinsic without an observation operator. Chu supports an intercept-profiled thermal-increment screen, not method-free absolute-gap ranking.

### Why E4 fails

The parent benchmark advancement rule requires improvement to survive source and measurement-class holdouts. Neither holdout exists within an exact class. Cross-class agreement cannot substitute for that test.

## Relationship to existing analyses

The certificate does not invalidate prior source-bounded results:

- Seiler supports TPMA thermal-shape and low-temperature composition checks;
- Chu supports an independent absorption-turning-point thermal-increment transfer screen;
- Scott supports a fixed-alpha temperature-slope test at figure precision;
- Schmit supports detector-cutoff forward comparisons and specimen-preserving operational-cutoff analyses.

Those are four class-specific results, not four folds of one universal benchmark.

The exact historical-constraint comparison in PR #134 and the Chu transfer screen in PR #137 remain valid within their declared observation boundaries. This certificate prevents those heterogeneous results from being collapsed into a universal winner table.

## Parent benchmark consequence

Issue #8 remains open.

Its first data-availability criterion is now partly satisfied because multiple specimen-level temperature ledgers pass a provenance schema. The controlling model-ranking criteria remain unmet:

- Hansen, Laurenti, and oscillator/moment candidates have not been evaluated under source-held-out folds within one exact class;
- no exact class supports a source holdout;
- nominal and composition-aware rankings cannot be interpreted as universal across the disconnected classes;
- no model improvement can pass the source-and-class advancement rule.

## Stop decision

Do not fit another universal or oscillator-based equation to the pooled 167 observations.

Do not reopen this gate by:

- pooling operational classes;
- fitting source offsets or free composition shifts;
- treating deterministic bounds as Gaussian standard deviations;
- using Scott or Schmit as independent Hansen holdouts;
- using the Chu series as independent validation of the Chu equation;
- counting Seiler samples 1 and 2 as independently composed absolute series;
- introducing a post-result observation correction.

A future E2 test requires a public, auditable second specimen-level temperature source in one existing exact class, or an independently validated observation operator established before numerical pooling. Author or institutional correspondence is prohibited.

## Authorization state

```text
class-specific single-source evaluation       authorized
source-bounded eligibility reporting          authorized
source-held-out exact-class ranking            not authorized
pooled cross-class ranking                     not authorized
new analytical coefficients                   not authorized
universal HgCdTe equation                      not authorized
manuscript                                     not authorized
```
