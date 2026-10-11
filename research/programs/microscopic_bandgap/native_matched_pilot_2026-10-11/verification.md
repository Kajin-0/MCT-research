# Pilot verification

## Terminal attempt and source-only check

The host result and 354 telemetry rows are copied byte-identically. Tests
independently isolate the RSS violation from time/disk/available-RAM hard-floor
and foreign-MPI triggers, verify strict failure/Cd rejection, and check all 17
original source/supervisor pins. Stdout/input and monitor hashes verify. A fresh
read-only terminal snapshot contains no MPI or R07 numerical driver.

Independent angular-momentum matrix exponentials, group/lift closure, character
orthogonality, dense twirl projectors and accidental-quartet counterexamples
check the source-only symmetry argument. Its scalar arithmetic envelopes are
conditional model estimates, not HSE eigenpair/material-error certificates.
The failed matched host is never admitted by the primitive reference check.

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/User/opencode_workspace/DFT/.venv/bin/python -m pytest -q \
  research/programs/microscopic_bandgap/native_matched_pilot_2026-10-11/test_preflight.py \
  research/programs/microscopic_bandgap/native_matched_pilot_2026-10-11/test_native_member_protocol.py \
  research/programs/microscopic_bandgap/native_matched_pilot_2026-10-11/test_terminal_result.py \
  research/programs/microscopic_bandgap/native_matched_pilot_2026-10-11/test_reference_irreps.py \
  research/programs/microscopic_bandgap/physical_input_qualification_2026-10-11/test_qualification.py
git diff --check
```

**31 focused tests passed** (6+4+3+6+12). Local package/state/ledger/registry
links resolve, and `git diff --check` passes after terminal artifact review. Validation starts no native process,
changes no supervisor/other program/main/goal, and supplies no material x_c.
No DFT scratch or UPF is committed. No automatic follow-up job is created.

## Historical first preflight verification


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
