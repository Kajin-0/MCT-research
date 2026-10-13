# One fresh first-ACE pair — local pilot, not admitted

**2026-10-13 17:18 update:** real stock HSE and a compatible48-band save are now
available. The proposed matched initialization uses separate wave/density/schema
copies from that actual save; no old ACE restart import. See the
[current decision](../native_first_ace_2026-10-13/decision.md). No numerical pair
has run. Also, diagnostic error85 is printed but QE's errore invokes MPI_ABORT(1):
the intentional-stop process status is1, not85. Keep this distinction in validation.

2026-10-13. Latest user authorization permits one sequential two-atom control
then streamed numerical fixture **if resource and actual-state admission pass**.
This narrow LOCAL-OWNED protocol supersedes the private-network/global-inventory
requirements **for this pilot only**. Neither old requirement has passed. An
owned cgroup does not prove absence of foreign MPI, and `plm=isolated` is a
launcher component, not a private network namespace.

## Numerical question and fixed physical scope

Does disk streaming of the complete q/band store preserve the **first native
exchange operator on identical actual states**, its weighted native contraction,
Gram matrix, and ACE operator? This is a fresh diagnostic of storage, not a
converged HSE SCF or restart experiment. QE's normal preliminary semilocal SCF
and first HSE exchange construction remain unchanged. Deliberate termination
after the first complete ACE is a test boundary, not a different functional.

Keep the whitelisted primitive two-atom HgTe, SG15 fully relativistic NC PPs,
HSE 0.25/0.106, SOC, 90/360/120-Ry cutoffs, k2/q2, **48 spinor bands**, full
accuracy Davidson and original tolerances. The unrelated **352-band/16-atom
target is unchanged and excluded**. `control.in`, `stream.in` and
`preflight_results.json` pin the decks, PPs, source, compiler, dynamic libraries,
candidate executables and proposed commands. Only the owned outdir differs.
The installed distribution stock executable is preserved; the control is the
instrumented **stock arithmetic**, compiled with matching flags/backends.

## Required execution and resource conditions

- The actual existing user manager must report the exact invocation, MainPID
  and cgroup path/inode. Verify kernel `memory.max=12 GiB`, `memory.swap.max=0`,
  `pids.max=32`, control-group killing, no restart/delegation, and <=600-s
  monotonic lifetime for **each** member. One foreground MPI family and one
  global lease, with tested escrow/crash cleanup; do not touch foreign units.
- Use the pinned local MPI launcher, two ranks, one thread, one pool/band/task
  group, `--host localhost:2`, isolated PLM, `self,sm` BTL and `ob1` PML.
  Verify **both actual MPI world-rank peers**, size=2, SO_PEERCRED UID/PID,
  start ticks/pidfd, ELF hash, argv, ancestry and membership in that exact owned
  cgroup. A hostname printout or an environment rank is insufficient. All ranks
  must be local; no remote/dynamic ranks. No network-isolation claim is made.
- Before launch require >=16 GiB host MemAvailable and enough ext4/quota
  headroom for **all** live output/reserved extents plus 10 GiB. During execution
  abort on MemAvailable<4 GiB, disk<10 GiB, summed process-family RSS>12 GiB,
  monotonic elapsed>=600 s, bad inventory of the **owned** family, pressure/OOM/
  swap/task/IO events, peer loss, output cap or native error. A memory cgroup
  bounds charged memory, **not** summed RSS with shared mapping overcount.
  Sampled host/RSS guards are not continuous guarantees against exogenous work.
- Admit a complete allocation/producer certificate through the first-ACE cutoff,
  including FFT planning copies, solver/BLAS/MPI/HDF5/allocator workspaces,
  owner/launcher, stdout and all file generations. Per-file rlimits do not bound
  accumulated closed files. Account actual reserved blocks, metadata/quota,
  inode aliases and output escrow separately. Retain native checked signed-64
  stream extents and real per-rank fallocate/readback; no duplicate whole store.

Interference can invalidate completion, timing and pressure comparisons. It
does not automatically invalidate arithmetic of a completed, authenticated
local communicator. This limited statement cannot certify performance,
foreign-family exclusion, whole-host safety or physical HgCdTe properties.

## Live numerical admission phases — distinct scope 4

The new private client requires live owner scope **4**, different from old
restart scope 2 and standalone collective scope 3. An environment Boolean or
saved test JSON cannot grant it. Every request binds JOB/PROFILE plus fresh
nonce and kernel-authenticated owner/lease. Fortran normalizes every nonzero
error to a positive failure before reducing on the actual world communicator.

1. REGISTER/CHECK: verify all real rank peers before large PW initialization.
2. Phase 4: after every rank/k initial wave/density/potential/et/wg/map packet
   is closed, validate complete NC coverage, finite active fields, Gram and
   shared common-input identity. For control, establish the immutable actual
   baseline; for streamed, require bitwise corresponding initial packets.
   Never import the incompatible 44-band/k4/Fock180Ry seed, rotate phases,
   repair failed states or generate retries.
3. Phase 5: after the actual dense/smooth/Fock descriptor is captured, compare
   rank-specific layout/maps with the pinned scope and (for streamed) control.
   Compute checked actual stream/state extents, then recheck the full resource
   certificate and host floors **before** q-buffer allocation.
4. Phase 7, streamed only: both ranks have published exact stream requests.
   The owner must verify fresh paths, fingerprint and extent against actual
   descriptors; reserve both new regular inodes, sync, verify owner, logical
   length and allocated blocks with quota/free-space guards, then issue live
   receipts. The retained `qs_begin_reserved` stays unchanged. No old native
   density/operator retirement or restart publication is authorized.
5. Phase 6: require complete first-ACE before/after packets for every rank/k,
   unchanged active inputs/maps/occupations and safe resources. Numerical
   evidence is already closed and native energy globally reduced. A live
   receipt reaches a **deliberate error-85 cutoff**; it does not mean SCF success.
   The owner records the expected diagnostic termination and verifies cleanup.
   Only then may it admit the one streamed member. A mismatch/refusal terminates
   the pair immediately, without retries or changed settings.

The scope-4 production issuer is **not integrated/qualified**. Existing issuers
refuse the new phases/scope. Compiled fences are a client-side remedy, not a
launch permit. Both native candidates remain `UNADMITTED`.

## Quantitative comparison and validity

`compare_pair.py` independently decodes bounded unaliased regular files and
requires complete two-rank/k/stage coverage, exact source `phi`, occupations,
deterministic probes, layout and physical reciprocal ownership. Only unused
input-wave padding is excluded; operator/projector/probe padding must be zero.
No active row, spin, phase or band rotation is removed. Global Gram/factor and
energy copies must agree across ranks; sum energy once per k, not twice.
Independently reconstruct full-band NC Gram, `sum Phi† V Phi`, normalized probe
and `-Xi (sum Xi† probe)` on all physical rows. Equal but incorrectly recorded
ACE actions must fail these internal checks even if both members agree.

Compare **control-direct to streamed-direct**, and **control-ACE to streamed-ACE**.
For action/Gram/projector/factor defects require max absolute defect
`<= max(1e-13, 1e-12 * max(|control|,|stream|))`. Require <=1e-12 Ry per-k and
summed native exchange-contraction discrepancy. Record these contractions in
their native `matcalc_k`/`aceinit` convention: they are not automatically the
final SCF exchange-energy term (the electrons wrapper uses a factor 1/2).
Native fingerprints and actual state parity are necessary in addition to norms.
ACE need not equal direct exchange on an off-subspace probe. The independent
synthetic counterexample intentionally has different direct and ACE actions.

No convergence, actual restart/readback, full-size peak RAM, material bandgap,
alloy response or physical `x_c` follows from passing this first-ACE comparison.

**Current decision: BLOCKED before any launch.** RAM/disk floors pass; complete
pre-first-ACE resource/output certification and live scope-4 issuer integration
do not. Actual native common-wave and FFT observations remain unavailable.
No MPI/QE/HSE process is started by the prepare/build/test programs in this package.
