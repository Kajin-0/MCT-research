# Verification and bounded execution record

2026-10-11. Base `c1a2ccde7f10ad3ff23c2d224ffa415f0545404a`, existing branch
`research/hgcdte-impurity-tmatrix-20261010`. Pre-registration `5347d3c` precedes
all scan evaluation; its files and scientific parameters were not modified.
The runner records its SHA256, the exact registration hash, full registration
commit and five pinned prior sources in [results.json](results.json).

## Executed numerical study

```bash
OPENBLAS_NUM_THREADS=1 /usr/bin/time -f 'elapsed_seconds=%e max_rss_KiB=%M' \
  .venv/bin/python \
  research/programs/microscopic_bandgap/centroid_feasibility_2026-10-11/run_study.py \
  --output research/programs/microscopic_bandgap/centroid_feasibility_2026-10-11
```

The grid ran **once**, 135 rows in 2.31 seconds, maximum RSS 38,684 KiB, with
at most 200 segments x 16 quadrature nodes. Interval bounds use fixed 32-digit
outward operations, 64-term reduced atan with explicit remainder and the
documented correctly rounded Decimal ln contract. Atomic polynomial primitives
and an integration-by-parts uniform-bath formula integrate complete known
measures; no support-free gap D, continuum discretization or eta limit is used.
Retained spectra are not truncated to a numerical band prefix.

Fixed independent composite Gauss-Legendre rules of orders 8 and 16 use positive
kernel evaluations, independently of the primitive recurrences. Maximum observed
discrepancies are 2.356238e-11 (mass) and 1.072465e-11 eV (moment); the maximum
W-normalized moment discrepancy is 9.278094e-12. These differences are checks,
**not** certified errors. The maximum interval centroid radius is 7.573279e-26 eV,
conditional on the stated arithmetic contracts. Rounding errors cannot stand
in for physical model/projector/probe errors. No extra precision is sought.

Runtime environment: existing repository `.venv`, Python 3.13.7, NumPy 2.5.3,
pytest 9.1.1. No dependencies installed. A bare `python` invocation was absent;
system `python3` lacked NumPy. Both failed before any model evaluation, then
the existing environment was used. No alternative Codex process/session was created.

The first staged whitespace check caught CSV's default CRLF export. Its only
post-scan runner edit specifies LF; exported CSV line endings and the current
runner hash were updated without reintegration. An independent test reconstructs
the original integration-code SHA256
`65d2a7388d9d72b5d1ee531452f60f12ba6b7bfe67614ae5e8252d60b4afccf2`
and checks the unchanged canonical numerical-row SHA256
`9a0035ad124e77f13bf166222eb50af15902c48dd96b293a2f1b4d0e8a9a61c0`.
No formula, parameter, rounding contract, gate or numerical value changed.

## Focused independent validation

```bash
OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q \
  research/programs/microscopic_bandgap/centroid_feasibility_2026-10-11/test_feasibility.py \
  research/programs/microscopic_bandgap/continuum_spectral_2026-10-11/test_independent.py
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q \
  tests/test_r07_analytical_first.py tests/test_r07_threshold_causal_closure.py \
  tests/test_gamma8_threshold.py tests/test_scalar_cpa_threshold.py
.venv/bin/python research/programs/microscopic_bandgap/evidence_acquisition_2026-10-11/check_stage0.py
git diff --check
```

New checks cover outward rational arithmetic, independent pi/ln constants,
fixed-projector dense Hermitian resolvents (7x7 finite **adapter proxies**, not
continuum replacements), exact positive normalization/full-centroid/endpoint
controls, direct quadrature of atom and bath, reference/unit covariance,
the complete registered grid and all saved enclosures, parity-based balanced
signs, mass-invariant affine redistribution and rejected ties/overwrites.
The full grid is not integrated a second time by tests; small formula cases
and saved intervals are checked independently. No synthetic test validates
physical Gamma projector transport, alloy disorder or experimental metrology.

Earlier continuum/threshold/CPA checks and frozen Stage-0 provenance retain
their prior negative gates. Changes are restricted to this package, an additive
R07 state entry and the R07 registry row. Other program state, prior files,
production code, empirical data and both repositories' numerical supervisors
are untouched. The historical blocked goal remains unchanged; no goal API,
session fork, outreach, paid action, DFT/HSE/MPI, supercell or queue was used.

Commit/push the validated finite study to the same research branch, never main,
and stop at the [decision](decision.md). A physical inversion is still OPEN.

## Completed checks

- New feasibility tests and previous continuum tests: **37 passed** (0.58 s).
- Four focused prior analytical/threshold/CPA test files: **34 passed** (0.63 s).
- Stage-0 check: 21 pinned inputs, nine access rows and six unaccepted sample
  rows verified; the archival NO-GO is unchanged.
- Registration/source/code pins and all 135 saved numerical rows verified;
  no scientific gate/parameter changed after registration.
- Final whitespace and package-local link checks recorded before commit.

These 71 tests are mathematical/synthetic and provenance checks only. The
registered scientific sign gate fails despite numerical correctness. No material
precision, physical x_c, empirical validation or manuscript novelty is asserted.
