# Decision record: DOI intake and first external-validation route

**Date:** 2026-07-21  
**Issue:** #184  
**Status:** candidate controlling decision pending PR validation

## Decision

Adopt a machine-readable DOI intake manifest and deterministic validation-route gate for the flagship distributional band-edge manuscript.

Select the following as the **first external-validation route**:

> **Chang multi-thickness / cutoff validation**

Required source pair:

```text
10.1007/s11664-007-0162-0
10.1063/1.2245220
```

The selected route is `ready_after_retrieval`, not ready for immediate specimen-level fitting.

## Why Chang is selected first

The existing repository already contains:

- a source-bounded Chang nonparabolic-Urbach absorption shape;
- a tested single-pass response operator;
- an exact exponential-tail thickness law;
- a proof that tail-only cutoff observations have rank at most two;
- a tested mixed-branch identifiability analysis;
- deterministic manuscript figures and tables.

Therefore a successful source retrieval can test a merged operator directly rather than requiring a new model family.

The current gate score is:

```text
24
```

This is the highest expected decision value among the declared routes.

## Missing Chang evidence

The route remains blocked until the source pair supplies or permits recovery of:

```text
native or calibrated spectra
same-specimen W and b
absorption amplitude
effective-thickness provenance
carrier state
exact detector 50-percent response construction
```

The separate `x=0.23`, `b=103+/-2 meV` value may not be transferred to the `x=0.21` Figure 2 specimen unless the source explicitly establishes common ownership.

## Ranked route result

Under the declared scoring rule:

```text
1  Chang thickness/cutoff                 24
2  Dingrong carrier spectrum              20
3  Chu intrinsic absorption               19
4  Herrmann multimodal tail               18
5  Teppe transition series                18
6  Moazzami source-native recovery         16
7  Ivanov-Omskii PL joint closure          15
8  Finkman independent tail                14
9  Krishtopenko prior-art audit             2
```

Tie-breaking uses lower source priority, then lower implementation cost, then lexical route ID.

## Dingrong decision

The highest-value single paper for extending the unified physics remains:

```text
10.1016/0038-1098(85)90315-1
```

Dingrong is ranked second because it requires more missing source equations, more optical-geometry information, a physical free-carrier background, and more nuisance assumptions before it can test the merged model.

Its current score is:

```text
20
```

The paper should be requested immediately after or alongside the Chang pair, but the Chang route remains the first implementation target.

## Score interpretation

The score is defined as:

```text
3*falsification_power
+ 3*flagship_relevance
+ 2*same_specimen_state
+ 2*calibrated_spectrum
+ composition_provenance
+ carrier_provenance
+ thickness_provenance
+ equation_completeness
+ reproducibility_rights
- 2*nuisance_penalty
- implementation_cost
```

The score ranks expected decision value under the current acquisition state. It is not:

- a probability that a source is correct;
- a posterior probability for a model;
- a substitute for source audit;
- or a permanent ranking.

Every criterion must be updated when a retrieved paper, supplement, or dataset changes the evidence state.

## Intake decision

All acquired source artifacts follow:

```text
literature/acquisition/source_intake_protocol.md
```

The public repository defaults to storing:

- citation and DOI metadata;
- acquisition provenance;
- cryptographic hashes;
- permitted source notes;
- equation audits;
- auditable digitizations;
- derived data.

A publisher PDF is not committed merely because it was supplied by the user.

## Operator-change boundary

Obtaining a source does not authorize changing an operator.

A new operator or parameter transcription requires a separate issue and PR containing:

- source audit;
- equation derivation;
- specimen ownership and valid-domain record;
- tests;
- immutable result;
- claim-boundary update;
- complete CI.

## Authorized user request

Request the Chang pair first:

```text
10.1007/s11664-007-0162-0
10.1063/1.2245220
```

Also request the Dingrong source because of its high mechanistic value:

```text
10.1016/0038-1098(85)90315-1
```

Useful additions include supplements, source data, author manuscripts, parameter tables, and high-resolution figures.

## Claim boundary

No route currently establishes external material validation.

The gate does not:

- convert source availability into scientific validity;
- authorize silent parameter transfer;
- treat nominal composition as exact;
- treat physical thickness as effective thickness;
- identify a generic carrier marker with a source free-carrier law;
- or imply that a lower-ranked route is scientifically false.

## Next decision after merge

When any requested source is obtained:

1. hash and classify the artifact;
2. update its manifest record;
3. perform the source audit;
4. re-score all routes;
5. open a route-specific implementation issue only if the source passes the rejection gates.
