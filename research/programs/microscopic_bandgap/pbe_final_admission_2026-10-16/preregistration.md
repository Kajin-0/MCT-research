# FINAL bounded admission sequence — NON_SCIENCE only

Baseline0c8df58,2026-10-16. User authorizes ONE NEW sequence, never a retry of
old unit/source/result. No QE-linked ELF, materials file, density/potential,
SCF, HSE or Hamiltonian action is permitted. The old hard refusal stays frozen.

Before any unit:14offline checks must pass; all original pins/dirty DFT and
historical files must match. Sources/new tiny ELFs/owner/checks and both fresh
roots/unit IDs/argv/nonces are pinned in STARTED.json. Existing cooperative
family lock is held; old ledger is read-only and must report FINISHED/empty.
Any preflight failure prevents launch. STARTED.json prevents a second sequence.

Fixed sequence: (1) one FS-only C service; (2) ONLY IF every FS gate and cleanup
passes, one direct singleton MPI C service. No launcher, helper permission,
network permission or fallback. No second attempt after unexpected refusal.
New owner has no anonymous assertions: each admission predicate records
name/expected/observed/source line with fsync BEFORE token release; exceptions
retain full traceback. Raw manager/kernel identity/limits are retained BEFORE
comparison. Terminal manager success/text alone cannot pass; native exit0,
pidfd exit, original cgroup empty, exact nonce/invocation and postchecks required.

Both services:MemoryMax12GiB,MemorySwapMax0,TasksMax12,RuntimeMax600s,Restartno,
Delegateno,KillModecontrol-group,OOMPolicykill,NNPyes,2cores/CPU200%,Nice10,
LimitNOFILE64,LimitCORE0,LimitFSIZE1MiB. Tiny source alarm15s, gate wait5s and
owner elapsed deadline25s are additionally stricter. Host available4GiB and
free disk10GiB floors; all new roots/build/owner outputs counted within14GiB.
Outside holder AS512MiB/CPU60s/file1MiB and finite logs/sample count. It is a
trusted finite-program sampled disk/floor contract, NOT a hard aggregate quota
or host-wide MPI-exclusion/private-network-namespace proof. Terminal-empty
checks and same owned unit cleanup are mandatory; no foreign process changes.

Dummy staging only; no actual material copies. Actual Landlock ABI7 rules
handle write/create/remove/refer/truncate/IOCTL rights; allow writes only to one
precreated output inode (known bounded stdio is inherited). All other inherited
FDs are kernel-closed and checked; stdio actual inodes/access/append are checked.
Negative tests use disposable RO/foreign/TMPDIR canaries and unlinked O_TMPFILE
attempts at/tmp,/dev/shm; no protected-original writes. The intentional dummy
preopened canary demonstrates Landlock's inherited-FD exemption, then closes
it and verifies EBADF. NNP and seccomp mode2 are measured; sockets/process
fork/exec denied, normal threads bounded. Reads are not globally allowlisted;
this is write confinement for a fixed trusted test, not an arbitrary-code sandbox.

Conditional singleton executes ONLY MPI_Init_thread(MPI_THREAD_SINGLE),
Comm_size==1,rank0,Finalize. No mpirun; fork/process clone/exec/socket needs
fail closed. A helper or unexpected write path rejects this exact domain; no
relaxation/retry. Worldsize alone does not prove helper absence. Native source
and actual cgroup membership/no-fork filter must jointly support that claim.

Any refusal ends this PBE diagnostic path: record exact named failure/native
stderr/trace/cleanup, withhold remaining test, TERMINATE this diagnostic rather
than propose another infrastructure phase. Mandatory science transition focuses
on stationary HSE+SOC signed inversion mass at multiple compositions. Even a
complete NON_SCIENCE PASS would leave scientific execution NO-GO pending a
separate authorization and full component/state/resource/error qualification.
