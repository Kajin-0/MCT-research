# Verification and data reproduction

Native: exactly one host then one Cd stock-QE two-rank SCF; no retry/NSCF/HSE.
Both native11-step convergences, weighted all-k charge/occupation/source/mesh/
terminal gates PASS. Strict preflight inputs and source/backend/PP hashes are
in[frozen_protocol.json](frozen_protocol.json); the original40Ry physical frame
and identical-cutoff k2 baseline are pinned too.

Five focused independent checks PASS in2.113s: actual full-complex physical
mapping with permutation/missing-source/wrong-cell negatives; native symmetry,
mesh and all-k FD charge/unchanged inputs; scalar functional and summed bounds
at all widths/references; host projectors and24map intertwining; actual owner/
caps/pins/old host uncertainty. The no-time-reversal counterexample gives five
stars, not the accepted four. Parser correction is separately retained and does
not replace the missing translations of lattice-only rotations with zeros.

Reproduce ONLY read-only science checks, not the native pair:

```bash
cd /home/User/opencode_workspace/DFT
source scripts/env.sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
python -m unittest discover \
  -s /home/User/repos/MCT-research/research/programs/microscopic_bandgap/chemical_k3_2026-10-14 \
  -p test_science.py -v
```

Tests needing spinors use the private native wave files pinned in the manifest.
Committed complex-overlap NPZ/CSV data reproduce scalar responses separately.
Analysis and archival scripts refuse an existing result/archive, so ordinary
reuse does not overwrite measured evidence. Plot reads only retained data.

Compact exact inputs/schema/logs/telemetry/rank/kernel/manager receipts are
archived; stdout and telemetry are gzip-compressed without editing bytes.
Large waves stay private. Final independent block/inode/metadata accounting
is500674560B across both members, under the sampled14GiB policy; not a hard
quota. Cleanup verifies both original cgroups absent and knownlockavailable,
oldledger finished/empty/hashunchanged. Protected before/after snapshots match
stock QE and dirtyDFT HEAD/status/diff/files exactly. No other session or job
control, global permissions, DFT/main commit or historicalgoal operation.
Final independent readback verifies all30 private source hashes and22 archived
payloads byte-for-byte after decompression. Protected snapshots also match
byte-for-byte; new Python sources compile and all JSON parses. The compact
archive occupies280205logicalbytes. The response plot was visually inspected.

These checks establish native-data/mathematical consistency, not material
validation, an eigenpair residual norm, BZ convergence, HSE convergence, foreign
MPI absence or a physical x_c. See[decision](decision.md) for actual numerical
values and[next experiment](next_experiment.md) for the unexecuted recommendation.
