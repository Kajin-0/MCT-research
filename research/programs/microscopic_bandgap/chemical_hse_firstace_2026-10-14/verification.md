# Verification and its limits

- Three private object compiles and link passed. Commands, provenance, and
  source arithmetic comparisons are in build_results. Native QE invocations: zero.
- Initial source-anchor checks rejected substring assumptions; those records
  remain preserved. External matcalc is in utils.f90 and the unchanged archive.
- Retained physical-reference byte roundtrip and Gram error 1.86 × 10⁻¹⁵ passed.
  No HSE wave, density, action, energy, or spectrum was acquired.
- One non-MPI exact-address experiment measured 114-byte refusal and 105-byte
  bind success; failed-attempt reuse is refused. No service or native retry.
- Retained manager exit 1, missing launch/receipts, free known lock, and absent
  original cgroup identify the failed attempt. Owner-only peak 12,955,648 bytes
  is not an HSE peak.
- Frozen source/ELF/library/PP/input hashes and protected stock/dirty-DFT
  snapshots match. Existing files, supervisors, and unrelated units are unchanged.

Three focused tests passed in 0.032 seconds. The following command runs the
read-only checks; it does not launch a service, MPI, or QE:

```bash
cd /home/User/opencode_workspace/DFT
source scripts/env.sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
python -m unittest discover \
  -s /home/User/repos/MCT-research/research/programs/microscopic_bandgap/chemical_hse_firstace_2026-10-14 \
  -p test_focused.py -v
```

Do not rerun address_admission.py, preflight.py, launch, or build against this
attempt's state. The short-address patch is prospective and unapplied. Native
collectives, capture, readback, and numerical correctness remain unqualified.
The manifest distinguishes archived prepared inputs from retained private objects
and the unexecuted ELF. `reference.bin` is retained PBE data, not an HSE checkpoint.
No material validation, HSE convergence, physical `x_c`, or full-SCF resource
guarantee follows from these software checks.

Publication check: default `git diff --cached --check` reports five whitespace
lines inside preserved unified patches (upstream trailing spaces and blank
context prefixes). They are retained for exact patch context. The check passes
with invocation-only `-c core.whitespace=-blank-at-eol`; no repository setting or
source whitespace was changed. Frozen-pin and archived-evidence hashes, protected
DFT status, and JSON/Python syntax also passed final read-only checks.
