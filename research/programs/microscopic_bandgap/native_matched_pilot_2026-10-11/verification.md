# Preflight verification

Scope: the user's finite native-pilot approval, starting at MCT `626fbc3` on
`research/hgcdte-impurity-tmatrix-20261010`. The DFT branch is separately recorded
in [preflight.json](preflight.json); it is neither committed nor pushed here.
Only read-only native provenance/deck/PP intake, proc/cgroup/disk measurement,
git-status snapshots and existing supervisor-state inspection occurred.

The engineering policy was stated before the terminal measured record. Tests
independently calculate `estimate*1.20+2 GiB`, check floor/ceil byte boundaries
and distinguish decimal GB, GiB, available physical memory, cgroup remaining
allowance and swap. They do not assert that a 20% margin is a certified peak
bound. The saved host/impurity required headrooms both exceed the snapshot.

Fifteen native input/provenance/PP hashes and two supervisor hashes verify;
dirty-status before/after strings agree. Hashes do not claim every unrelated
dirty or ignored file was independently byte-audited; preservation follows
from the collector's no-native-write/no-launch actions and the scoped records.

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q \
  research/programs/microscopic_bandgap/native_matched_pilot_2026-10-11/test_preflight.py \
  research/programs/microscopic_bandgap/physical_input_qualification_2026-10-11/test_qualification.py
git diff --check
```

No live SCF, resource allocation, postprocessor, supervisor change, restart,
native input rewrite, physical sign, material x_c or main merge is validated.
The terminal result is **safe preflight NO-GO**, not successful HSE convergence.
Do not repeat the collector or automatically wait for more memory.

## Completed checks

**18 focused tests passed:** six new preflight checks and twelve retained
physical-input qualification checks. All 15 native source pins, two supervisor
state hashes, the collector hash and the earlier reference records verify.
Independent arithmetic confirms the host shortfall and byte-unit boundaries.
Local package/design/handoff links resolve; `git diff --check` passes. No DFT
file, native output directory, live supervisor or prior analytical derivation is
changed. R07 state and registry record only this finite approval/NO-GO amendment.
