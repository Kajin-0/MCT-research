# Verification and independent-check scope

The package begins at `b19fc65` on the existing research branch. P1 and P2 were
separately tested, committed and pushed (`904748f`, `29d3460`) before P3.
Only this package, R07 state and its registry row are changed. Native sources
are read-only, no drivers run, and supervisor state paths are explicitly skipped.
These scope statements describe actions performed, not process telemetry.

## What the checks establish

- One native existing-data audit, 0.83 seconds /94,452 KiB RSS, reconstructs
  the fixed-frame kernel control and saves actual spectral weights/overlaps;
  29 completed/prepared/static source hashes are verified. The native module
  is imported with bytecode disabled using already installed h5py.
- Outward Decimal arithmetic encloses the reported rounded-input reference
  and design formulas. No native eigenpair/metric, SCF or material residual is
  converted into a certified zero. Existing helper code is reused unchanged.
- Independent moment integrals and differentiated window critical points
  check the transport/tail constants without an inverse-kernel fit.
- Dense inverses versus Schur elimination check opposite causal responses,
  including the correct Gamma6/Gamma8 multiplicities (10x10 synthetic maximum).
- Equal 4-site periodizations and different 12-site kernels supplement an
  independent **infinite-chain exact T** evaluated by a 2x2 inverse. This
  demonstrates information loss, not material validation.
- A 3x3 bath verifies leakage PSD, a missing-prefix inverse error certificate,
  and positive host leakage when the retained frame is not spectral and V=0.
- Saved result flags leave physical x_c and material bounds null, reject a
  gratuitous micro-eV operator-precision requirement, and declare no DFT launch.

## Focused reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q \
  research/programs/microscopic_bandgap/physical_input_qualification_2026-10-11/test_qualification.py \
  research/programs/microscopic_bandgap/continuum_spectral_2026-10-11/test_independent.py \
  research/programs/microscopic_bandgap/centroid_feasibility_2026-10-11/test_feasibility.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q \
  tests/test_r07_analytical_first.py \
  tests/test_r07_threshold_causal_closure.py \
  tests/test_gamma8_threshold.py \
  tests/test_scalar_cpa_threshold.py
git diff --check
```

The first group comprises 12 new and 37 preserved checks; the second comprises
34 existing theorem/threshold checks. Passing them certifies numerical/synthetic
consistency and provenance only. It cannot establish physical projector transfer,
material error, localization, a composition modulus or HgCdTe inversion.

No spectrum grid, material fit, new native job, DFT environment change, archive
contact or additional discovery cycle is part of verification. Arithmetic output
drivers refuse overwriting existing records. The read-only audit need not be
repeated; tests use its pinned record. Terminal decision is
**STOP_ACQUISITION_BOUNDARY**, with one unexecuted design.

## Completed validation

The combined focused suite passed **83 tests**: 12 in this package, 18 prior
continuum, 19 prior centroid and 34 prior theorem/threshold checks. All 29
source pins and saved arithmetic code hashes verify. The reference displacement
gate explicitly checks every source/comparison branch-energy pair, not merely
matched sorted levels. Thirty local Markdown links resolve. `git diff --check`
passes. No prior package, production module, native file or unrelated program
state is edited; only the R07 state/registry add this terminal decision.
