# Verification of the finite native cutoff result

**Measured native:** one host then one Cd run, stock QE 7.5, both accepted
science/terminal guards, 11 SCF iterations each. Actual sources are immutable
under [the frozen profile](frozen_protocol.json). Native HSE count is zero.

**Independent read-only checks:** seven focused tests pass in 5.858 s:
actual reciprocal-vector isometry/permutations/refusals/direct complex overlap;
all24 Td label intertwining and native host irreps; all-k FD charge/convergence
and exact input differences; scalar centroid reconstruction at all widths and
both references; joint-bound extremizers/reference invariance; source HSE
allocation arithmetic; actual owner/source pins/caps and old host uncertainty.
Command and test scope are retained in [test_results.json](test_results.json).

To repeat only these cheap checks (never the native pair):

```bash
cd /home/User/opencode_workspace/DFT
source scripts/env.sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
python -m unittest discover \
  -s /home/User/repos/MCT-research/research/programs/microscopic_bandgap/chemical_cutoff_2026-10-14 \
  -p test_science.py -v
```

The tests require retained private native waves. Committed complex-overlap NPZ
and energy/weight CSV files independently reproduce the reported scalar curve
without the large HDF5 waves. An ordinary rerun of analysis/archival scripts
refuses to overwrite existing results. Plot generation reads only retained data.

[The manifest](evidence_manifest.json) pins exact original and compressed
archival bytes, actual ELF/PP/input/native metadata and all wave files. Stdout
and telemetry are gzip-compressed without editing original whitespace/content.
[Final retained accounting](final_retained_account.json) independently verifies
499,945,472 bytes across both members. [Cleanup](terminal_cleanup.json) verifies
both original cgroups absent and known flock available; the old ledger remains
finished/empty and byte-pinned. [Before](protected_before.json) and
[after](protected_after.json) exactly match protected dirty DFT/stock evidence.
Final independent archive readback checks all 30 source hashes and all 22
archived native payloads byte-for-byte after decompression. Protected snapshots
also match byte-for-byte. All new JSON parses and Python files compile without
executing a job. The compact archive occupies 270,579 logical bytes, including
its copied native profile. The result plot was visually inspected.

The seven tests validate mathematical/native-data consistency, not real-alloy
accuracy, eigenpair operator bounds, complete disk quotas, host-wide exclusion,
HSE convergence or physical x_c. Conditional error assumptions are explicit in
[the proof](cross_cutoff_proof.md); unresolved errors remain in [the decision](decision.md).
