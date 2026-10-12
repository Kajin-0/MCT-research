# M4 decision: process-owner gate advances; native fixture remains BLOCKED

This finite phase starts from MCT `f0d948e` on
`research/hgcdte-impurity-tmatrix-20261010`, retaining the native bridge candidate
`6b21779`. It does not resume the historical goal. **No PW, HSE or MPI computation
was launched.** The private control executable was linked and inspected only.

**TESTED SMALL-SCALE — PASS:** a dedicated foreground owner and child cleanup
monitor now hold a kernel exclusive lease, authenticate both fake ranks through
live Unix peer credentials and process identities, reserve real ext4 extents,
monitor the complete owner/monitor/worker RSS, RAM/disk/time and output budget,
and terminate only witnessed descendants through pidfds. Tests cover TERM,
SIGKILL, timeout, detached descendants, a second owner, stale tickets, simulated
PID reuse, foreign sentinels, collisions, false authorization and restart refusal.
Native bridge CLI authority now requires live RPC; a Boolean or `MONITOR.json`
cannot authorize its native path.

**NEGATIVE RESULT — retained:** simultaneous death of both cleanup authorities
cannot promise automatic orphan cleanup. The kernel lock releases, but the
durable non-FINISHED ledger refuses the next family. The test cleans only its
previously acquired fake-process identities and explicitly reconciles its own
ledger afterward. Production automatic reconciliation is not implemented.

**MEASURED / limited to fake workers:** see exact telemetry in
[runtime_results.json](runtime_results.json). The validation snapshot uses
roughly 0.10 GiB maximum summed family RSS, at least 29.6 GiB MemAvailable and
30.2 GiB free disk. RSS includes shared-page overcount; PSS and a simultaneous
RSS-minus-PSS indicator are reported. Each fake rank reserves 192 logical bytes
(4096 physically allocated); a 32768-byte output escrow is also allocated.
Admission charges both that escrow and future output bytes. These are small
reservation measurements, not the native fixture's FFT extents or peak RAM.

**PASS / preregistration only:** exact paired two-atom HgTe decks are frozen at
48 spinor bands, HSE+SOC, SG15 NC full-relativistic Hg/Te, 90/360/120 Ry, k2/q2,
1e-10 SCF accuracy and accurate-empty Davidson. Only output paths differ.
The pinned PP headers give 36 valence electrons. Matched control/candidate source,
compiler flags, binary and dynamic FFT/MPI/backend fingerprints are recorded in
[preflight_results.json](preflight_results.json) and
[control_build.json](control_build.json). Identical backends are established;
identical initial native waves and actual FFT decomposition are not.

**M4 native admission / M5 — BLOCKED, NOT RUN:**

1. No compiled all-rank native MPI lease registration and hook-to-rank mapping
   exists. The bridge PROFILE and launch JOB fingerprints still require an
   explicit typed binding. The tested fake-rank receipt cannot supply it.
2. Native direct EXX action, energy, Gram/ACE probe instruments and current
   density/wave/old-ACE readback comparison are not complete. Exit status alone
   would not resolve the retained equivalence/restart gates.
3. Native two-rank stream/state extents, output envelope and common initial
   G/k/wave state are uncertified. No guessed native allocation is reserved.
4. Some pre-existing `/proc/maps` entries are unreadable with current permissions.
   Readable inventory finds no MPI family, but strict global inventory refuses;
   this phase changes no permissions and claims no global exclusivity proof.

The original nominal 22-GiB store still fails the 10-GiB reserve on this disk.
The 16-atom/352-band experiment remains excluded and unchanged.

**Validation:** 65 focused methods: 17 real-process lifecycle, 7 preflight
falsification, 21 retained serial native-codec, 15 checkpoint/storage and 5
source regressions. See [validation.json](validation.json); synthetic resource
predicate injections are separately marked, not physical measurements. DFT
HEAD/dirty status, 17 protected input/PP/supervisor pins, stock QE and both prior
candidates, plus `calcura`, `commander` and `research` sessions remain unchanged.
Final owned-worker inventory and kernel lease holders are empty.

**Decision — STOP at this boundary.** The new foreground ownership/resource
component passes a previously absent small-scale gate. Full native M4/M5 does
not pass. The next bounded source gate is a compiled two-rank native lease and
profile-binding adapter with a deterministic first-ACE/readback probe and exact
layout/output declaration; it must resolve inventory uncertainty before native
admission. No fixture, full-size rerun, numerical queue, physical gap or `x_c`
claim is made here.
