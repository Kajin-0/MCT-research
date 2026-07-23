# R06 stochastic transport and finite-size noise

## Current phase

Phase 1C — HgCdTe statistics, parameter provenance, and deterministic kernel architecture.

## Core program documents

- `phase_1_model_definition.md`
- `parameter_provenance.md`
- `phase1c_plan.md`
- `phase1c_acceptance_matrix.md`
- `deterministic_boundary_and_circuit_hierarchy.md`
- `phase2_repository_layout.md`

## Governing derivations

- `docs/derivations/stochastic_transport_noise/conventions.md`
- `docs/derivations/stochastic_transport_noise/stochastic_closure.md`
- `docs/derivations/stochastic_transport_noise/contact_detailed_balance.md`
- `docs/derivations/stochastic_transport_noise/contact_onsager_fdt_and_limits.md`
- `docs/derivations/stochastic_transport_noise/contact_prior_art_comparison.md`
- `docs/derivations/stochastic_transport_noise/dimensionless_reduction.md`
- `docs/derivations/stochastic_transport_noise/carrier_statistics_and_einstein_gate.md`
- `docs/derivations/stochastic_transport_noise/conservative_finite_volume_residual.md`

## Executable Phase 1C prototypes

- `src/mct_research/transport_noise/statistics_prototype.py`
- `src/mct_research/transport_noise/finite_volume_prototype.py`
- `tests/test_r06_phase1c_statistics_prototype.py`
- `tests/test_r06_phase1c_finite_volume_prototype.py`

## Scientific status

The broad theory and stochastic-contact novelty hypotheses are rejected. R06 proceeds as a controlled reduction and error-bound study. The executable kernels support source and numerical-architecture verification only. Production HgCdTe simulation, stochastic PSD calculation, predictive detector claims, and manuscript preparation remain gated.