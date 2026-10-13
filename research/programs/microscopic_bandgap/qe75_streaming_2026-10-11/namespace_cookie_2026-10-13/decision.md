# Namespace-cookie decision — 2026-10-13 12:44 UTC

**Getter/observation workaround PASS; effective private-network isolation FAIL;
native MPI/QE/HSE admission NO-GO.** Starts clean `9fdfdaa`, original research
branch/session, no goal/session/agent/permissions changes. One actual non-MPI
unit was launched; planned follow-up units were not run after its refusal.

## New measured evidence

- Three sockets created **after service startup** each report cookie1; three
  independent fresh host sockets before/after also report1. No inherited fd was
  used for the self measurement. The startup scanner observes no sockets among
  fd0..63; that bounded scan is not a general theorem about pre-existing fds
  above a subsequently lowered RLIMIT_NOFILE. Fresh creation is the decisive
  protection against inherited-socket misidentification.
- The service enumerates five interfaces,16 non-lo entries and8 non-loopback
  addresses. Independent host interface enumeration also yields five. Actual
  loopback entries3 are UP, but the domain includes other devices. Self namespace
  inode stat still returns EACCES13; self executable stat succeeds.
- Manager PrivateNetwork/PrivateUsers are **yes**. The exact owned unit journal
  says namespace support or privileges are missing and it proceeded without.
  Configured Boolean properties therefore did not realize the required domain.
  This independently measured counterexample makes the fresh-cookie/interface
  gate essential. No field was reinterpreted as actual isolation.
- Kernel peer UID/PID/start ticks, live unit MainPID/InvocationID, executable
  image/path fingerprint, actual cgroup/inode,64MiB/swap0/tasks4/oom.group1 were
  bound. pids.current1; cgroup/manager memory peak2,097,152 bytes; no memory/pids
  limit event. These owned controls work independently of network isolation.
- A pathname Unix connection and live owner authentication were observed, but
  both endpoints remain in the host namespace. The accepted endpoint's cookie1
  is explicitly an endpoint measurement, not peer self identity. Owner refused
  before granting the non-MPI receipt or transferring its fd; child reported
  owner EOF and terminal manager status94. Full cross-namespace handshake and
  SCM_RIGHTS remain **NOT QUALIFIED**. Raw `exit_status` is null because refusal
  interrupted normal completion serialization; terminal status94 is retained.
- Actual4096-byte ext4 reservation is block/byte checked. Independent host
  pressure remained above floors. Unit unloaded, witnessed PID1839689 absent,
  original ledger byte-exact and flock free after closure. No foreign inventory,
  network data, IP connect, supervisor action, MPI_Init, QE or HSE.

## Source/independent verification

[Linux6.17 socket getter](https://raw.githubusercontent.com/torvalds/linux/v6.17/net/core/sock.c)
returns the socket's net cookie; [namespace initialization](https://raw.githubusercontent.com/torvalds/linux/v6.17/net/core/net_namespace.c)
assigns cookies from a64-bit counter. Equality identifies the same namespace
under these semantics and no counter wrap; it does not establish isolation from
arbitrary inherited/received sockets. Host vendor kernel semantics are supported
here by the getter/interface/journal observations, not assumed from upstream
version alone. No topological or material inference follows.

[systemd257 executor source](https://raw.githubusercontent.com/systemd/systemd/v257/src/core/exec-invoke.c)
contains the relevant “proceeding without” branches when namespace capability
or setup fails. The owned journal is direct runtime evidence of that behavior;
it does not distinguish every possible permission/kernel-policy cause. No
capability, sysctl, manager default, global namespace or permission was changed.

Seven initial pure certificate/host-socket methods and five final integer
resource methods PASS. Measured refusal replay is recorded separately. The
address-space bound applies to exact resident mappings; a claimed automatic
extension to proc-reported RSS was rejected by independent kernel-source review.
Reported-RSS error, complete MPI producer generations/paths and sustained
monitoring remain unknown. See `runtime_resource_assessment.md`.

## Qualified next action and stop boundary

**Rank1 indispensable execution input:** an actually realized, permission-
compatible segregated local network domain, certified by fresh service/rank
cookies and real loopback-only state. A requested systemd property is insufficient.
The current manager/settings demonstrably do not supply it. This is not a proof
that every possible nonprivileged namespace construction is impossible; no
settings/capability retries or global changes are justified by this result.

Until that input exists, retain refusal. Next independent gates are the real
cross-namespace pathname owner/lease lifecycle, production typed live issuer,
complete local-runtime producer/generation/path envelope and actual MPI rank
registration/cleanup. Original strict host-wide exclusion remains UNPASSED;
owned namespace/cgroup evidence could not prove foreign MPI absence even if
private networking worked. No native attempt is consumed or scheduled.

Stop this bounded investigation after preserving evidence, updating plan and
commit/push. Do not repeat the failed unit, planned negatives or global process
inventory. No physical x_c and no change to target HSE/SOC/352-band inputs.
