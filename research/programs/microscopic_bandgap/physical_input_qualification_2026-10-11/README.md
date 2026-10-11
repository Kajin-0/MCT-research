# R07 — existing physical-input qualification

2026-10-11; task base `b19fc65`; existing branch
`research/hgcdte-impurity-tmatrix-20261010`. Three decision-driven phases under
the continuous research mandate; the historical blocked goal is unchanged.

**Decision: REFERENCE CONDITIONING PASS / MATERIAL INPUT NO-GO —
STOP_ACQUISITION_BOUNDARY.** Existing numerical HgTe reference frames permit a
conditional uniform window certificate. They do not identify substitution
response. An exact periodization counterexample also excludes promoting one
periodic-cell response to a dilute impurity amplitude without additional input.
One unexecuted matched acquisition design is retained; no calculation is queued.

- [Decision, input ranking and uncertainty boundary](decision.md)
- [P1: native reference and interior-data intake](phase1_reference_inventory.md)
- [P1 audit and source hashes](existing_audit.json), [read-only audit](audit_existing.py)
- [P2: uniform positive-measure bounds and transfer falsifier](phase2_uniform_reference_bounds.md)
- [P2 outward arithmetic](reference_bound.json), [evaluator](evaluate_reference_bound.py)
- [P3: periodic aliasing, causal discriminator and symmetry check](phase3_periodic_aliasing.md)
- [One unexecuted acquisition design](minimum_acquisition.md)
- [Design arithmetic and witnesses](acquisition_budget.json), [checker](check_acquisition_budget.py)
- [Independent tests](test_qualification.py), [verification](verification.md)
- [Persistent compaction handoff](handoff_ledger.md)

The [prior centroid NO-GO](../centroid_feasibility_2026-10-11/decision.md),
[continuum decision](../continuum_spectral_2026-10-11/cycles_and_decision.md),
[threshold boundary](../threshold_causal_2026-10-11/cycles_and_boundary.md)
and [archival NO-GO](../evidence_acquisition_2026-10-11/stage0_report.md) stand.
No physical x_c, material sign bracket, intrinsic linewidth, sharp gap or
priority claim is made. Only this package, R07 state and its registry row change.

## Reproduce cheap checks

From the MCT repository root, using its existing environment:

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q \
  research/programs/microscopic_bandgap/physical_input_qualification_2026-10-11/test_qualification.py
```

The tests re-evaluate the saved bound/design arithmetic, exact small matrices,
and source hashes. They never run a native driver, SCF or job supervisor.
The native audit was executed once using the existing DFT environment for h5py;
its saved result suffices here. Do not rerun it to refine an already negligible
reference digit, or operate the separate DFT repository.
