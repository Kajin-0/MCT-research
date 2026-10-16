# Native completion implemented; full production qualification BLOCKED

**2026-10-16; baseline37f48db. No native QE/PW/MPI/SCF/member/restart or user
service was executed. All builds and tiny non-MPI children stayed in new MCT
scratch; protected DFT/stock/old profiles and refusals are unchanged.**

| Gate | Actual outcome |
|---|---|
| Native source placement / compile / link | **PASS, source-conditioned.** New actual QE-linked ELF has a PBE-only begin hook BEFORE init_run, checked packet flush/size/close and all-rank barrier BEFORE final receipt, then normalized world error reduction/barrier. run_pwscf still returns before electrons/punch. Exact H/kinetic/local/NC-SOC calls unchanged. Stock archive member comparison is in verification; only the private run_pwscf object differs. ELF was NEVER executed. |
| Typed native transport and production dispatcher | **PASS, bounded non-MPI components.** Real compiled C clients call the same receipt ABI linked into QE, through owner.service/make_protocol, actual socket-bound kernel peers and pinned ELF/argv. New R07S/scope16 binds JOB/PROFILE/fresh invocation/nonce. No Python-wrapper or inherited-socket identity. Both live finals are held pending packet/readback/resource gates. |
| Strict retirement / accounting / import | **PASS, components.** Live FD EACCES is fatal and absorbing after later real exit. Only a known exited rank with BOTH prior live finals enters bounded pending. Premature/foreign/lost rank, truncated packet, failed readback, descriptor reuse, nonzero/mismatched manager, cgroup mismatch, lost log and allocated output burst refuse. Clean owner/reader import and missing/corrupt dependency tests run in isolated interpreters. |
| Full production owner + real MPI collectives | **NOT QUALIFIED.** owner.run implements the external-holder path and wires the tested handlers/account/reader, but its actual systemd/MPI lifecycle, startup/cancellation/crash cleanup and two-world-rank normalization were not executed. Terminal manager/empty-cgroup and positive physics reader in component tests were explicitly mocked. These are NOT a production/native PASS. |
| Complete resource / numerical certificate | **NO-GO.** Required backend/initialization/owner peak allocations and time/output envelopes are incomplete. No <=2meV numerical action certificate is created. Past1GiB/4s is not a bound. The source loader refuses before service creation; no frozen execution manifest/release or resource certificate exists. |

## Concrete implementation and acceptance

`native_probe.inc` retains six original host50Ry physical columns and six exact
Theta images per member: **12 each /24 total**, not24 simultaneous columns per
rank. `native_phase.inc` obtains rank/size from QE mp_world, not environment.
`native_lease.c` uses a fresh socket for every call, socket-bound owner pidfd,
live owner start/lock checks, echoed random challenge and nonnegative errors.
The linked binary fingerprint is in [build_result.json](build_result.json).

The new outside-family `owner.py` keeps actual peer pidfds through per-rank
exit; `protocol.py` authenticates before replying, closes acceptance on any
failure, and checks manager/cgroup/foreground wait/outputs separately. A fresh
private pending-unit latch is written before creation and removed only after
terminal proof plus durable outside signoff. Unknown cleanup blocks the next
scoped member; it does not prove global absence of MPI or control other
controllers. The protected historical family ledger is read, never rewritten.
The native execution CLI is disabled and loader independently refuses this
phase's NOT_GRANTED release.

`reader.py` has an explicit hash-pinned dependency, reads both actual packet
rank/PID/FFT/G/frame/charge fields and compares saved-source hashes. It checks
metric Hermiticity, component summation, original Theta controls and QHP with
the actual Gram inverse; no changed projector or own-EF subtraction. Readback
is repeated after exit. The six-state/full-H stationary or material error is
NOT inferred from a small consistency residual. No old refused packet was
used as a new control, even in the positive component fixture.

See [acceptance and limitations](acceptance.md), [component evidence](component_results.json),
[resource audit](resource_audit.json), [new source/ELF/PP pin plan](prospective_pins.json)
and [verification](verification.json). Development import/fixture defects were
detected before any native job; original negative checks and fixes are retained
in [development_failures.json](development_failures.json).

## Stop boundary and minimum next experiment — NOT authorized here

**STOP: do not run either member.** Independent actual systemd/MPI lifecycle
qualification and a complete runtime/resource contract cannot follow from
these compile/non-MPI results. Unknown owner/readback overhead must join the
native budget; a12GiB kernel cap limits the unit, not all outside-holder memory.
Safe setup/cancel/crash behavior must be tested before relying on owner.run.

The smallest NEXT live resource experiment, only after those acceptance gates
and separate authorization, is ONE fresh first-member saved-density12-query
diagnostic, not SCF or the pair: capture initialization/FFT/beta/reader/close
peaks, actual all-rank hook/readback and terminal cleanup. Retain12GiB/swap0/
tasks12/600s, host4GiB and disk10GiB floors and14GiB sampled aggregate outputs;
no retry or automatic shared release. It is a resource/owner qualification,
not an automatically certified static chemical sign. If source-complete
admission remains mandatory and unavailable, that experiment is itself NO-GO;
obtain a separately justified bounded resource protocol first, never a boolean
override. No such protocol, release, job or queue is issued here.

The potential scientific gain remains static PHP/QHP arrangement contrast at
fixed x=.25. The original<=2meV budget, physical frame and24/4 chemical subgroups
are unchanged; no shared quartet is imposed. Static projection is not an
ensemble linewidth/EBS test, including the user's cited Wang–Luo–Zunger2019
LDA+U result. No novelty, dynamic inverse relabeling, N2/random-alloy mass,
converged HSE, empirical gap fit or physical x_c is claimed. Registry unchanged.
