# Verification conditions — 2026-10-13 11:53 UTC

Final v2 harness/client compile PASS; ten serial methods PASS, no MPI_Init or
MPI job. Read-only twelve-pin/claim consistency PASS. `component_results.json`
and `harness_build.json` describe v2; `.v1` records preserve the earlier
nine-method/source condition. V1 lacks the live PREINIT call and is not a
runtime-qualified candidate. V1/v2 binaries and source snapshots remain in the
new private directory, without overwriting retained QE/backend/owner files.

Serial tests load a **non-MPI-linked** C codec shared object, use local Unix
threads and a serial test server, and compile a tiny status function. They do
not prove rank registration, real MPI error/collective behavior, namespace
isolation, MPI descendants or production authorization. The source-order check
is a source check, not execution of the harness. The PREINIT sentinel is not a
world-rank receipt; actual world rank/size must still come from MPI after Init.

Two actual **non-MPI** isolated-user services failed: first errno-less exit91,
then localized self-netns stat EACCES13. An earlier Python dependency type
failure launched no unit. Configured service properties and terminal manager
MemoryPeak are retained; no live kernel/RSS certificate is fabricated from
these short failures. Both exact units are unloaded and recorded exec PIDs
absent. No further namespace test or standalone MPI attempt was made.

Native harness compilation initially refused because mpicc's configured
compiler was not in PATH. The fixed build adds the retained local toolchain
PATH, removes wrapper compiler overrides and hashes the actual compiler,
MPI/PMIx libraries and launch executables. These are **selected pins**, not a
complete dynamic-component/runtime envelope certificate. Link success and
readelf metadata do not imply any MPI execution. `build_harness.py` refuses
overwriting existing v2 binaries; it is not a routine rerun command.

Preservation PASS covers original17 pins, dirty DFT HEAD/status, stock and
prior candidates, sessions, byte-exact legacy ledger restoration, both ledgers
closed/no flock holders, and only our known unit/PID closure. Protected earlier
supervisor state says complete; no global foreign-process inventory is claimed.
Original strict host-wide exclusion and all native QE gates remain unchanged.

For a new relevant code change only: DFT `source scripts/env.sh`, run absolute
`test_components.py` (serial C/Unix IPC), then `verify_artifacts.py` (read-only).
The namespace probe is an actual service experiment; do not rerun unchanged.
No QE, MPI harness, HSE, full16-atom, paid action, DFT commit or main merge.
