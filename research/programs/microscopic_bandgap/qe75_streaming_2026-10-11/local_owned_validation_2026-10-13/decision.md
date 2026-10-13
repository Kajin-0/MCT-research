# Finite validation-strategy decision — 2026-10-13 11:53 UTC

**NO-GO for the presently verified native MPI launch path. Source/compile and
serial receipt components PASS. No MPI_Init, MPI job, QE or HSE was run.**
This new phase starts clean `ba48c97` in the original research branch/session;
it does not resume the historical goal or change the original admission gate.

## Decisive new evidence

The first actual fixed non-MPI user service exited91 before identity output.
One diagnostic-only correction, preserving all restrictions, localized the
failure: `stat("/proc/self/ns/net")` returns **EACCES (errno13)** with UID1001
under PrivateUsers/PrivateNetwork. It supplies no verified namespace identity,
loopback inventory or live all-rank isolation certificate. This is a failed
observation mechanism, **not** proof that network namespaces cannot exist or
that every permission-compatible alternative is impossible. No permission
change, host-network fallback or additional namespace retry was made.

Both actual units were audited/reset only after capturing their exact terminal
manager records, then independently found unloaded with recorded exec PIDs
absent. Manager-reported peaks: 2,359,296 and 2,097,152 bytes. These short failed
probes did not supply live kernel/RSS samples; configured properties and manager
peak reports must not be called a complete new MPI resource certificate.
The earlier dependency-type error happened before any unit was launched.

Independent software work then completed:

- A standalone MPI_Init/barrier/integer-allreduce/allgather/application-status
  harness **compiles** with the retained local compiler/Open MPI. The compiled
  executable remains `COMPILE_ONLY`, unexecuted. Actual rank identities feed the
  candidate hook after Init; real operational MPI failure is not “normalized”
  using another possibly broken collective.
- New client magic **R07C** and scope **3 LOCAL_MPI_COLLECTIVE_ONLY** cannot be
  interchanged with retained R07L ABI_NO_MPI or QE NATIVE receipts. All **ten
  serial component methods PASS**, using compiled C and local Unix IPC only.
  Tests include scopes1/2 and magic refusal, challenge/status corruption,
  INT_MIN/signed-overflow normalization, digests and fixed probe payload.
  A serial test server is not a production all-rank registry or live MPI grant.
- Independent source review found that v1 reached Init before obtaining a live
  family receipt. Corrected v2 requires PREINIT action3 with the explicit
  (-1,0) non-world-rank sentinel before MPI_Init. Failed receipt returns92;
  actual REGISTER/CHECK still uses MPI-supplied rank/size afterwards. Final
  ten-method suite includes that typed phase and old-scope/malformed-sentinel
  refusal. V1 binaries/source snapshots and nine-method evidence are retained;
  neither version was executed. Production owner issuance remains absent.
- `local_protocol.md` specifies separate local correctness, resource,
  identity, no-remote, output, failure and cleanup acceptance claims. No new
  executable MPI authorization path is installed; the old controller/guard and
  all QE/native gates remain unchanged.

## Scientific acceptance decision

Foreign MPI absence is not logically required for a **conditional completed
local arithmetic correctness** test, with an isolated communicator and private
unchanged state. Foreign activity can affect completion/pressure; it defeats
timing and unconditional continuous resource-floor claims. The protocol keeps
these validity limits explicit and requires abort on any observed instability.
It is a changed, narrow claim, not a proof of original host-wide exclusion.

Neither local MPI data via `self,sm`, configured cgroup caps, nor an unreadable
namespace observation proves no remote traffic. Installed PRRTE advertises TCP
runtime bootstrap; the proposed isolated loopback path must first be verified.
Original strict host-wide exclusion is still **UNPASSED/HARD_BLOCKED**, and all
QE common-wave/state/readback/FFT/full-envelope gates are separate unpassed
conditions. No numerical agreement, restart, physical spectrum or x_c follows.

## One ranked next prerequisite

**Rank1: a permission-compatible, live owned-namespace/rank identity
certificate under this UID, with no global permission changes.** This is the
first discriminating prerequisite; a larger MPI/QE job cannot supply it safely.
One source-conditioned candidate is a fresh socket's `SO_NETNS_COOKIE`, with
no inherited socket, independently matched between controller/guard/ranks and
combined with interface and kernel peer/cgroup observations. The upstream
[Linux6.17 getter](https://raw.githubusercontent.com/torvalds/linux/v6.17/net/core/sock.c)
returns the socket's namespace cookie, not the current process namespace of an
arbitrarily inherited fd. Host is `6.17.0-41-generic`; upstream inspection is
not validation of that vendor build, namespace isolation or rank tracking.
No cookie alternative was run or substituted for the failed inode gate.

After that certificate, the cross-namespace pathname lifeline/lease and complete
local runtime output envelope still need qualification before the one MPI
attempt. No speculative execution now. The old abstract lifeline cannot simply
cross PrivateNetwork; masking this would hide an additional failure.

Stop this finite assignment after preservation, validation and commit/push.
Do not repeat unchanged inventories/tests or launch the candidate on this
decision. The original one-MPI-run conditional permission remains unused.
