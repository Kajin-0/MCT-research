# R07 competing inversion routes — analytical-only, 2026-10-15

Start with [decision](decision.md), [claim registry](discovery_registry.md) and
[cross-route input/phase comparison](comparison_and_phase_boundary.md).

- [RouteA symmetry/IR/finite-resolution analysis](route_A_symmetry_and_IR.md).
- [RouteB signed optical witness and disorder bias](route_B_optical_mass.md).
- [Minimal transition-disorder closure](transition_disorder_closure.md).
- [ONE next input](one_next_input.md), [primary prior art](literature.md).
- [Cycle ledger](cycles_and_decisions.md), [handoff](handoff_ledger.md),
  [validation](verification.md).

Run from the MCT repo with the already available environment; these are
small Python matrix/analytic checks, never QE/MPI/material validation:

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/User/opencode_workspace/DFT/.venv/bin/python research/programs/microscopic_bandgap/competing_inversion_routes_2026-10-15/check_route_A.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/User/opencode_workspace/DFT/.venv/bin/python research/programs/microscopic_bandgap/competing_inversion_routes_2026-10-15/check_route_B.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/User/opencode_workspace/DFT/.venv/bin/python research/programs/microscopic_bandgap/competing_inversion_routes_2026-10-15/check_resolution_and_quotient.py
python3 research/programs/microscopic_bandgap/competing_inversion_routes_2026-10-15/verify_package.py
```

Output numerical units are declared synthetic, except cited retained-data
summaries and exact Bernoulli composition statistics. No physical x_c or
new calibrated experiment is claimed. General Kane/SCBA/optical/threshold
methods are established; specific synthesis novelty is UNVERIFIED.
