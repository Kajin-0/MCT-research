# Decision: native fixed-orbital EXX/ACE numerical equivalence qualified

2026-10-13 20:59 UTC; starts clean MCT682b5d5 in the original research session.

**CALCULATED — REAL TWO-RANK QE7.5 HgTe HSE+SOC:** the ONE streamed fixed-orbital
first-ACE member completed. Against the retained genuine stock-arithmetic
control, all active source/trial/probe inputs, output bases, direct actions,
Phi†V Phi Gram matrices, ACE projectors/Cholesky factors and ACE probe actions
are **bitwise identical** across both ranks and all three irreducible k points.
Twelve real stream diagnostic packets and both live completed phase6 receipts
are retained. Independent native contraction/action reconstruction passes.

| k | Control native contraction (Ry) | Stream native contraction (Ry) | Difference (Ry) |
|---|---:|---:|---:|
| 1 | −2.233385945366400 | −2.233385945366400 | 0 |
| 2 | −8.951652593765756 | −8.951652593765756 | 0 |
| 3 | −6.700915922315115 | −6.700915922315115 | 0 |
| Unique-k sum | **−17.885954461447270** | **−17.885954461447270** | **0** |

Every measured corresponding direct/direct and ACE/ACE component difference,
Gram difference and factor/projector difference is zero. Independent WG-weighted
Gram trace agrees with native energy. These are native matcalc/aceinit weighted
contractions, **not the final SCF Fock term**. This is not a direct=ACE assertion
for the off-span probe. [Full independent result](numerical_result.json),
[component comparisons](comparison.json), [protocol and dependency proof](protocol.md).

## Why the new experiment resolves the earlier boundary

**PROVEN UNDER THE PINNED FIXTURE ASSUMPTIONS:** fixed NC CPU spinor Fock needs
source orbitals, occupations, q/k mappings, screened kernel and trial/output
basis, rather than an independently reconstructed SCF local potential. The new
driver replays canonical control source/trial/probe data into native buffers,
reads it back, and invokes unchanged Fock/ACE arithmetic. No electrons()/SCF,
density update, HSE outer iteration or punch occurs. No exchange action/Gram/xi
output is supplied from the control. Canonical readback must match every byte.
The earlier full-state rho(real)/vrs refusal is **unchanged**, not passed here.

All eight source k+q spinors derive from the three captured irreducible k states
through the actual signed index_sym/index_xk/index_xkq, rotation and spin tables.
Native occupation/WG/WK division is bit-checked. Missing original auxiliary
kernel tables required one targeted setup-only reconstruction/capture; its
actual q/FFT/basis layout matches the original control. The streamed member's
entire two-rank 17,018,200-byte kernel packet pair matches that capture bitwise,
including all24 target-k/q Coulomb multiplier arrays,24 active spin rotations,
rir, cell/screen/divergence/regularization fields and native weights. Those
original control auxiliary tables were not recorded: their reconstruction from
the pinned deterministic constructors is **source-conditioned**, not a claim
of an unavailable original raw-table comparison. Actual full action equality
provides an independent numerical test of that reconstruction.

## Measured budgets and limits of the claim

Stream: **96.193434s**, sampled summed family RSS **629,506,048bytes** (includes
shared-map overcount), manager cgroup MemoryPeak **982,867,968bytes** including
charged file cache; zero memory/task pressure events observed. Minimum sampled
MemAvailable **30,398,865,408bytes**, free disk **28,907,634,688bytes**. Maximum
sampled owned output charge **679,354,368bytes**; maximum output sample gap
**0.739017s**. Independent resource samples retained (no lost stream telemetry).
Actual checked ext4 per-rank stream extents **201,326,592bytes**, one resident
q-plane **25,165,824bytes/rank** from native dimensions and unchanged allocation.
The 8→1 buffer reduction is87.5%; measured whole-job RSS is not this percentage.

The prior control sampled family RSS884,166,656bytes included preliminary SCF;
the replay does not. This is **not a matched whole-SCF RAM/performance benchmark**.
Stream cgroup peak exceeds control883,781,632bytes, consistent with extra charged
file cache; do not hide it or advertise whole-cgroup memory savings. No32-GiB
full-target feasibility, native restart or HSE convergence follows.

Real UID/ELF/argv/lineage/JOB/PROFILE/nonce/flock and cgroup receipts preceded all
work. Kernel limits memory12GiB/swap0/tasks12,600s, file1GiB/AS896MiB; sampled
RSS12GiB/MemAvailable4GiB/free disk10GiB/output14GiB. Disk accounting remains the
expressly approved sampled local risk contract: external writers/bursts can
cross floors between samples; metadata allowance is not exact ext4 journal
allocation. Original host-wide MPI exclusion and private-network proof remain
unpassed. No Boolean receipt, permission change or foreign-process modification.

## Retained failures and narrow remedies

- First compile refused a misplaced preprocessor directive/stream-only compile
  template for setup; corrected privately before any native work.
- First setup (2.864s) refused phase8 readback because the serializer wrote
  inactive padded WK(40000) rather than WK(1:3). All six retained packets prove
  the sole difference is319,976extra inactive bytes. Exact active buffer
  readback had passed. Corrected native packet extent; no input tolerance change.
- Corrected setup (3.640s) closed every input/kernel record and both phases8/9,
  then reached intentional no-ACE stop. Its owner subsequently reported ENODEV;
  the exact stack was not captured, so its origin is **not proven**. Original
  RESULT stays FAILED; separate read-only qualification accepts closed numerical
  kernel data, not a passed resource-monitor lifecycle. No setup EXX was run.
- Stream closed all first-ACE packets, passed numerical comparison and both
  phase6 receipts, then owner `counters(cg)` raced actual cgroup removal while
  reading memory.oom.group. Exact stack, terminal native MPI_ABORT1, completed
  receipts and empty collected group are retained. **Original stream RESULT
  stays FAILED. Numerical qualification is separate from that teardown failure.**
- Targeted future teardown predicate permits a vanished group only after both
  live completion receipts and exact matching terminal invocation/status; live,
  incomplete or incompatible state still refuses. Two focused offline checks
  pass on actual retained evidence and negative cases. **No native rerun tests
  this remedy**, and the failed original RESULT is never rewritten.

Two setup-only attempts (one serializer refusal, one completed capture), ONE
stream operator execution, zero new control SCF/action runs. The scope ends
here; no rerun/campaign to obtain a cosmetically passing owner RESULT.

**DECISION:** advance the *fixed-operator numerical equivalence* foundation.
Keep full SCF-state parity, checkpoint/restart, owner teardown reliability and
full16atom physical acquisition gated. Stock QE, original352-band/HSE/SOC
inputs, dirty DFT422d71d, old ledger, supervisors and calcura/commander/research
sessions are unchanged. All own groups collected and shared lease free; only
own dispensable escrows retired. No Cd/material gap/x_c, novelty claim, historical
goal change, hardware purchase, new session/agent, DFT commit or main merge.
