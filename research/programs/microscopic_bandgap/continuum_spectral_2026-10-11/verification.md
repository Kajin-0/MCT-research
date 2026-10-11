# Independent verification and scope

2026-10-11. This finite package starts from clean commit
`3316bfdc55c089b11010d157adf3d9622f5215c7` on the existing research branch.
No goal API or session/permission change was used. Its three mathematical cycles
are recorded in [the decision ledger](cycles_and_decision.md).

The written proofs use spectral positivity, exact resolvent subtraction,
trace duality, ratio identities, strong concavity and the intermediate-value
theorem. Independent finite-bath and continuous-measure checks use dense
Hermitian inverses/eigendecompositions, closed-form uniform-bath Cauchy
transforms, fixed quadrature and exact small topology/endpoint arithmetic.
They are synthetic consistency checks, not proofs of material coefficients,
accepted projectors or the existence of experimental raw data.

Reproduce from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q \
  research/programs/microscopic_bandgap/continuum_spectral_2026-10-11/test_independent.py
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q \
  tests/test_r07_analytical_first.py \
  tests/test_r07_threshold_causal_closure.py \
  tests/test_gamma8_threshold.py \
  tests/test_scalar_cpa_threshold.py
.venv/bin/python research/programs/microscopic_bandgap/evidence_acquisition_2026-10-11/check_stage0.py
.venv/bin/python research/programs/microscopic_bandgap/evidence_acquisition_2026-10-11/check_evidence.py
git diff --check
```

The tests check normalization, causality, continuum support, value/derivative
operator bounds, window/tail/resolution budgets, centroid and peak uncertainty,
causal negative examples, copy/gauge/reference/unit effects, composition-root
conditioning and loss of topology information. No native calculation, fitting
operation, empirical data or material parameter sweep is used. Fixed 2x2–4x4
matrices and 160-point quadratures create no research work queue.

[Provenance](provenance.json) pins the earlier packages/derivations/tests that
this sprint preserves. The new R07 state/registry entry is additive; unrelated
programs, frozen evidence records, DFT repositories and all detached supervisors
are untouched. Declared scope controls are not independent process telemetry.
Fresh primary-method literature access is distinguished in [literature.md](literature.md)
from unavailable material information. No paper download was necessary.

Passing these checks leaves the decision **THEOREM PASS / MATERIAL NO-GO**.
No sharp signed Gamma gap, physical x_c, operational material crossing interval,
bulk topological phase, native input acquisition or manuscript priority is
certified. The old blocked goal remains unchanged. Stop after the validated
commit/push; do not open a fourth analytic cycle.

## Completed validation

- All 18 new independent checks passed, including byte-identical verification
  of 37 pinned prior artifacts. Matrices were at most 4x4; continuum integrations
  used the fixed 160-point rule.
- The four focused existing theorem/threshold files passed: **34 tests** in
  0.67 seconds. No prior tests or production modules were edited.
- Stage-0 provenance passed: 21 input hashes, nine source-access rows and six
  unaccepted sample rows; its decision remains NO-GO.
- The original evidence checker passed: 584 frozen records, 24 primary
  publications and 49 local links. No raw data or fresh PDF hash was added.
- `git diff --check` passed. Changes are limited to this new package, R07 state
  and the R07 registry row. Previous packages/derivations/data remain unchanged.

These counts establish synthetic and provenance validation only. No physical
uncertainty, peak margin, root modulus, interval or material certificate is
inferred from them.
