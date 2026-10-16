# Exact commands, source scope and reproduction boundary

All commands ran from `/home/User/repos/MCT-research`, with bytecode disabled
and OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=1. Existing read-only interpreter:
`/home/User/opencode_workspace/DFT/.venv/bin/python`.

Executed in order:

1. `python research/programs/microscopic_bandgap/pbe_static_lifecycle_2026-10-16/test_offline.py`
2. `python research/programs/microscopic_bandgap/pbe_static_lifecycle_2026-10-16/prepare.py`
3. **ONCE ONLY:** `python research/programs/microscopic_bandgap/pbe_static_lifecycle_2026-10-16/owner.py positive`
4. `python research/programs/microscopic_bandgap/pbe_static_lifecycle_2026-10-16/verify.py`

The full actual systemd-run argv, including local mpirun, properties and
explicit environment transport, is in `evidence/COMMAND.json`. Compiler argv
and return0 are in `build.json`; OMPI_CC=/usr/bin/cc was invocation-local.
`prepare.py` never launches MPI. Actual launch error, captured by the Codex
foreground exec at14:31 UTC (returncode1):

```
account.py:74: target=os.readlink(fd);s=fd.stat()
FileNotFoundError: [Errno 2] No such file or directory: '/proc/1978386/fd/9'
protocol.py:155: Refusal('incomplete/unknown live final pair')
owner.py:205: charges=sample_owned(protocol,accounts,active,ids,root)
checkpoint_capsule.Refusal: incomplete/unknown live final pair
```

This is a transcribed traceback excerpt, not a separate native log. The
original RESULT/STARTED/CLEANUP/COMMAND and empty pw.out are copied byte-for-byte
and hash-verified. No live rank packet exists; no fake output was substituted.

## Source locations

- `owner.py:run`: real external holder, frozen lifecycle-only loader, actual
  manager/cgroup/pidfd binding, escrow/flock, sampled account, abort/cleanup.
- `protocol.py:accept`: actual native wire/kernel peers, scope1601, both-rank
  waits, closed-file readback, pre-ACK FD inventory; `inventory_failure` and
  `terminal` retain strict original rules. No native permission bypass.
- `native_lease.c`: exact compiled receipt ABI except deliberate domain
  separation; `mpi_fixture.c`: actual MPI_Init_thread/world/barrier/allreduce/
  allgather/close/final caller. No PW/QE/PP or Hamiltonian calls.
- `reader.py`: independently typed NON_SCIENCE decoder/readback.
- `account.py`: original sampled accounting core, narrower lifecycle outputs.
- Imported kernel/manager/storage dependencies and actual binary/library
  closure used here are hash-pinned in `frozen_execution.json`.

## Independently rerunnable offline checks

The source scripts deliberately refuse overwriting evidence. Existing live
identity/root/unit MUST NOT be run again. To repeat only offline tests, redirect
their **final test report path** into fresh ignored scratch; do not replace
owner/protocol/kernel functions. For example, from the repo with the interpreter
above (NO service/MPI/QE):

```python
from pathlib import Path
import sys, uuid
p=Path('research/programs/microscopic_bandgap/pbe_static_lifecycle_2026-10-16').resolve()
sys.path.insert(0,str(p))
import test_offline as t
original=t.durable
report=Path('.tmp/r07spc16')/('offline-repeat-'+uuid.uuid4().hex+'.json')
def write(path,data):
    return original(report if Path(path)==p/'offline_results.json' else path,data)
t.durable=write  # test-report destination ONLY; no runtime guard replacement
t.main()
```

These tests cover domain separation, old science refusal, isolated imports,
duplicate/foreign packet rejection and immutable evidence. Live denial,
later-exit/no-retropass, crash/cancel/no-final and3s pending in this new script
are explicitly **modeled**, not new native observations. Actual syscall-based
non-MPI retirement cases remain in the unchanged original component package.

The source review and offline tests passed; the actual owner lifecycle did
not. No new numerical/source-complete Gate B certificate, paired24action
release or first saved-density resource experiment follows. STOP.
