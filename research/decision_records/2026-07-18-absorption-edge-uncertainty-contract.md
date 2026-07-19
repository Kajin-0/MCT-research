# Absorption-edge uncertainty export contract

**Date:** 2026-07-18  
**Status:** validated reporting and interchange contract  
**Decision:** absorption-derived HgCdTe edges must preserve observation metadata and a same-record model-sensitivity envelope; no universal edge correction is authorized.

## Problem

The validated absorption observation-model benchmark showed that the inferred edge can move by several to tens of meV when the analyst changes:

- the absorption model family;
- the fitted exponent;
- the fit window;
- the fixed absorption threshold;
- the treatment of Urbach or other sub-gap tails;
- carrier-state assumptions.

A scalar `Eg` value and a single quoted measurement uncertainty therefore do not contain enough information to compare absorption-derived edges with magneto-optical, transport, or latent-gap models.

The missing quantity is not another universal correction coefficient. It is a provenance-explicit record of the observation operator and a sensitivity envelope obtained by reanalyzing the same underlying record.

## Contract

The machine-readable contract is named:

```text
hgcdte_absorption_edge_uncertainty
```

with schema version:

```text
1.0
```

Every record requires:

1. record identifier;
2. composition value, method, status, and uncertainty when known;
3. temperature and uncertainty when known;
4. reported edge and reported standard uncertainty when available;
5. explicit observable definition;
6. measurement modality;
7. extraction method;
8. complete edge-model name, expression, and parameters;
9. energy and/or absorption analysis window;
10. fixed threshold when the extraction method uses one;
11. carrier-state status and measured/inferred metadata when available;
12. tail treatment and parameters;
13. at least one same-record sensitivity reanalysis;
14. source DOI and exact source locator;
15. evidence class and claim boundary.

A fixed threshold must lie inside the declared absorption window. A measured or inferred carrier state must include carrier type, density, and method. Stored envelopes are recomputed on load; a tampered or inconsistent envelope is rejected.

## Envelope semantics

For central reported edge `E0` and same-record alternative analyses `Ei`, the contract reports:

```text
Emin = min(E0, Ei)
Emax = max(E0, Ei)
lower deviation = E0 - Emin
upper deviation = Emax - E0
span = Emax - Emin
```

The envelope is also decomposed by varied factor, such as `fixed_threshold` or `model_family`.

This range is a deterministic sensitivity interval. It is not automatically:

- a standard deviation;
- a confidence interval;
- a Bayesian credible interval;
- a correction to the latent material gap;
- a probability distribution.

The source-reported standard uncertainty is retained in a separate field and is not combined in quadrature with the sensitivity envelope unless a future probabilistic model explicitly justifies that operation.

## Synthetic reference export

The reference generator converts the four validated observation-model benchmark scenarios into complete contract records.

Each record uses the `1500 cm^-1` threshold edge as the central reported observation and includes seven same-record alternatives:

- fixed thresholds `600`, `1000`, `1200`, and `2000 cm^-1`;
- free fractional-power fit;
- fixed `p=0.5` fit;
- fixed `p=1.0` fit.

The four synthetic records produce:

```text
records                               4
alternatives per record               7
minimum total envelope span      30.5011 meV
maximum total envelope span      46.1483 meV
maximum lower deviation          32.7203 meV
maximum upper deviation          13.4279 meV
```

These large spans are expected because the reference intentionally combines broad threshold and model-family alternatives. They demonstrate contract behavior and the scale of observation-model sensitivity. They are not production uncertainty assignments for real specimens.

## Evidence-class boundary

The reference records are labeled:

```text
synthetic_method_benchmark
```

They must not be pooled with experimental primary observations as though they were measured gap points.

Experimental records can use the same contract only when the sensitivity alternatives are derived from the same underlying spectrum or dataset. Cross-specimen scatter or unrelated literature formulas must not be mislabeled as same-record model sensitivity.

## Validation

The focused tests verify:

1. deterministic benchmark-to-contract metrics;
2. separation of reported standard uncertainty from sensitivity;
3. mandatory threshold metadata;
4. threshold/window consistency;
5. mandatory same-record alternatives;
6. carrier-state completeness;
7. physically valid absorption-edge energies;
8. JSON round trip and envelope-tamper detection.

The dedicated workflow regenerates the JSON, CSV, and compact summary; compares them with committed references; and runs the focused test suite.

## Files

- `src/mct_research/absorption_observation.py`
- `tools/build_absorption_edge_uncertainty_contract.py`
- `tests/test_absorption_edge_uncertainty_contract.py`
- `validation/absorption_edge_uncertainty_contract_reference.json`
- `validation/absorption_edge_uncertainty_contract_reference.csv`
- `validation/absorption_edge_uncertainty_contract_summary.json`
- `.github/workflows/absorption-edge-uncertainty-contract.yml`

## Scientific decision

- reusable observation metadata contract: **authorized**;
- same-record sensitivity envelopes: **authorized**;
- preserving measurement and extraction provenance: **required**;
- combining sensitivity with standard uncertainty without a probability model: **not authorized**;
- universal absorption-edge correction: **not authorized**;
- static HgCdTe gap refit from current absorption evidence: **not authorized**.

## Next work

1. Apply the contract to an experimental primary spectrum only after calibrated point data and exact source provenance are available.
2. Add explicit thickness and optical-transfer metadata when a source provides enough information to reconstruct absorption from transmission/reflection.
3. Add carrier-filling sensitivity only when carrier type, density, temperature, and band model are all declared.
4. Keep the synthetic reference as a method oracle, not an empirical training set.
