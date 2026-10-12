# HgCdTe / QE 7.5 low-RAM execution plan and reset handoff

**Plan created:** 2026-10-11 23:56 UTC (2026-10-11 19:56 America/New_York)
**Last verified update:** 2026-10-12 03:08 UTC
**Status:** M5-READINESS FINITE PHASE COMPLETE; NATIVE EXECUTION AND PHYSICAL HgCdTe INVERSION REMAIN BLOCKED
**Owner:** Original `research` Codex tmux session; existing MCT research branch `research/hgcdte-impurity-tmatrix-20261010`.
**Starting verified revision:** `b1a4772`. **Latest native bridge revision:** `6b21779`. **Latest M4 checkpoint:** `1d74a0d`. **Latest readiness checkpoint:** `m5_readiness` artifacts in this commit, starting `1d74a0d`. **This plan does not authorize new numerical runs.**

## Objective and nonnegotiable boundaries

Obtain qualified first-principles HgTe host and Cd-substituted HgTe Γ6/Γ8 spectra and projector overlaps, then investigate a physically defensible alloy inversion threshold with finite-size/disorder and quantified error controls. Near-term engineering goal: demonstrate identical HSE+SOC exact exchange with a low-memory private QE 7.5 implementation **on the existing ~32-GiB VPS**, with no RAM purchase.

- Preserve HSE/SOC, 352 bands, prepared k/q meshes, cutoffs, accuracy, and stock QE for the **original 16-atom experiment**. A separately labelled tiny engineering fixture is not a downgrade of that experiment.
- Keep stock QE, all dirty DFT files, pre-existing supervisors, `calcura`/`commander` tmux sessions, and historical blocked goal untouched. No speculative results, no main merge, no DFT commit, no force push.
- No full 16-atom native run without a fresh, explicit authorization and measured RAM/disk/restart qualification. Only an independently admitted small validation fixture may use existing conditional scope.
- At most one owned MPI family; validate input/pseudopotential/binary provenance and safe resource margins. Fail closed on incompatible restart state.

## Evidence-backed milestone ledger

| ID | Deliverable and binary acceptance gate | State at 2026-10-12 03:08 UTC | Evidence |
|---|---|---|---|
| M0 | Converged binary HgTe Γ reference and cutoff comparison | **PASS: numerical reference only**; no alloy response | `state.md`; binary difference ~6.7014 µeV |
| M1 | Diagnose native 16-atom resource failure | **PASS: diagnostic**, host SCF **FAIL** | `native_matched_pilot_2026-10-11/decision.md`; 26.722-GiB summed RSS, stopped in ACE; Cd never admitted |
| M2 | Implement lossless one-q-plane streamed EXX candidate; source/build/unit checks | **PASS: software-only**; nominal `exxbuff` 22→2.75 GiB | `qe75_streaming_2026-10-11/{decision.md,verification.md}`; `ea8823e` |
| M3a | No-copy versioned checkpoint storage + read-only restoration + 64-bit guards | **PASS: component tests only**; 15 focused + 24 regression | `checkpoint_phase/{decision.md,checkpoint_contract.md}`; `b1a4772` |
| M3b | Complete native checkpoint state bridge: old ACE `xi` and occupations + HSE outer iteration + matching inner SCF/orbitals, both stop paths and post-`punch` publication; proven import | **CANDIDATE BUILT; UNIT TESTS PASS; NATIVE RESTART NOT QUALIFIED** | `native_bridge/{decision.md,closure_and_boundaries.md,validation.json}`; `6b21779`: 21 bridge tests, 24 storage regressions, 14 native-unit compiles and private link; real native MPI/HDF5 readback unverified |
| M4 | Foreground family ownership/live lease, exact reservations and fixture admission | **PASS SMALL-SCALE COMPONENTS / NATIVE INTEGRATION BLOCKED**: M4 monitor tested; dual PROFILE/JOB binding and compiled native client/world-rank wrapper added. Production guardian native packet/hook dispatch, common state/layout/output and complete inventory remain unqualified | `runtime_admission/decision.md`, `m5_readiness/{decision.md,validation.json}` |
| M5 | Native small control-versus-streamed action/energy/Gram/ACE equivalence and restart | **READINESS COMPONENTS ADVANCED / NATIVE NOT RUN**: 12 native-unit compiles + both private links; deterministic first-ACE instruments; exact serial qeh5 wave/density/ACE readback of 1,208,137 values. Actual MPI collectives/SCF restore/common 48-band seed/FFT layout/full envelope/inventory not qualified | `m5_readiness/{decision.md,contract_and_failures.md,validation.json,readback_results.json,link_results.json}` |
| M6 | Admission of full-size host on actual RAM/disk/time using measured peak and sufficient scratch | **NO-GO**: ~31 GiB disk available versus nominal ~22 GiB stream + 10 GiB reserve + output | `checkpoint_phase/phase_outcomes.json` |
| M7 | Accepted matched 16-atom HgTe host then Cd-substituted spectra, physically labelled Γ6/Γ8 overlaps | **NOT ACHIEVED** | Host termination; Cd stage absent |
| M8 | Convergence/locality/finite-size/disorder and physical `x_c` error bounds | **NOT ACHIEVED** | `state.md`; physical input remains missing |

**Scientific truth boundary:** Calculated binary HgTe Γ splitting is not a measured or first-principles alloy `E_g(x)`. The 87.5% number is an **allocation estimate**, not native peak-RAM proof. A linked private QE executable is not a validated SCF. Do not infer a physical `x_c` until M7 and M8 pass.

## Critical path and decision points

1. **Validate M3b, do not redesign it again without evidence.** Candidate `6b21779` now captures old `xi`, occupations, current tolerance/state scalars, both stop hooks and post-`punch` atomic manifests. Unit compilation and synthetic tests pass. The remaining falsifiable check is real QE MPI/HDF5 state readback and old-versus-current ACE action after native restart. Any failed readback or state mismatch must be recorded as an explicit defect; no restart success is claimed from synthetic tests.
2. **Decouple the two engineering hypotheses where safe:** numerical equivalence of streamed exchange versus reliability of long-running checkpoint/restart. An explicitly authorized **fresh no-restart tiny fixture** may provide earlier information, but do not reinterpret the existing conditional authorization to skip its checkpoint prerequisite. Require approval of a revised test protocol before changing sequence.
3. **Retain the passed component gates and stop at production native admission.** Typed separate PROFILE/JOB digests, a compiled real-world-rank lease wrapper before state reads and deterministic first-ACE direct/Gram/energy/factor/xi/probe instruments now compile and link in both private modes. Serial pristine qeh5 readback matches 1,208,137 existing wave/ACE/density values bitwise; it is not an MPI SCF restart. The inspected 44-band/k4/Fock180Ry save cannot certify the 48-band/k2/Fock120Ry fixture. Native production packet/hook dispatch, actual collective/readback/common-state behavior, exact FFT/output lifetime budget and complete inventory remain missing. Component receipts cannot authorize native scope. Never demand ACE=direct on an arbitrary G probe; compare each corresponding control/stream action separately. No native admission or launch occurs until every retained gate passes. Preserve 12/4/10-GiB/600-s policy and its sampling limitations.

4. **Solve M6 using the current VPS only.** Inspect disk inventory; reclaim only identified dispensable scratch after explicit review. Do not delete scientific data or relax disk policy to force an admission.
5. **Obtain M7 then M8** through fresh separately justified execution scope and error budgets. A 16-atom periodic Cd substitution is a finite-cell calculation, not by itself a dilute-limit or alloy inversion determination.

## Churn detection and stop rules

- Every substantial phase must change a previously failing **acceptance gate** or produce a new physically meaningful observation, not merely add tests, write more handoffs, or re-audit identical data.
- After **one substantial engineering phase without passing a new gate**, stop and explicitly report why the next experiment remains blocked and whether to change strategy. No repeated no-op goal resumes.
- Distinguish **PROVEN**, **TESTED SMALL-SCALE**, **SOURCE-CONDITIONED**, **MEASURED NATIVE**, **BLOCKED**, and **NOT RUN** in every status report.
- Do not equate commit volume, test count, source compilation, or documentation length with scientific progress.
- If a new blocker appears (e.g. native ACE state, disk reserve), add it to the ledger and name the smallest falsifiable check that would retire it.

## Required update protocol — on every milestone, stop or handoff

1. Immediately revise **Last verified update**, current active milestone, and its evidence/state above.
2. Append one timestamped entry to **Change log**: `YYYY-MM-DD HH:MM UTC | commit | milestone | result PASS/FAIL/BLOCKED | measured evidence | next action`.
3. Refresh the **Context-reset handoff** below, including branch/commit, live process/owner status, changed files, exact reproduction command, blocker, and what is **not** authorized.
4. Run appropriate *small* tests and `git diff --check`, then commit and push this plan **together with corresponding validated research artifacts** on the existing research branch. Do not falsely stamp verification before it occurs. Never overwrite an active agent's uncommitted work.
5. On context reset, **read this file first** followed by cited package decisions/AGENTS. Compare against live `git status`, actual provenance and any running jobs; this document is a checkpoint, **not automatically trusted live state**.

## Context-reset handoff (updated 2026-10-12 03:08 UTC)

- **Read first:** this file, `m5_readiness/{decision.md,contract_and_failures.md,handoff_ledger.md,validation.json}`, retained M4/M3b/checkpoint decisions and DFT `AGENTS.md`.
- **Repo:** `/home/User/repos/MCT-research`, current research branch `research/hgcdte-impurity-tmatrix-20261010`; phase starts `1d74a0d`. This commit includes readiness software/evidence, typed native API binding and ledger updates. No main merge or DFT commit.
- **State:** finite phase ends at native admission. No PW/HSE/MPI launcher/real communicator was run. Existing `calcura:$0`, `commander:$1`, `research:$3` untouched. Historical blocked goal unchanged. End validation: no ABI workers or lease holders, M4 own ledger FINISHED; recheck live state.
- **Preservation:** DFT HEAD `422d71d`, starting dirty status, 17 protected input/PP/supervisor pins, stock archive/executable and prior M2/M3/M4 candidates unchanged. New disposable work only in `.local/qe75_lowram_20261011/m5_readiness/`.
- **Passed:** 78 focused methods (13 readiness + 65 retained); 12 native-unit compiles; matching private links; dual-digest/compiled two-peer ABI; deterministic ACE codec and counterexample; pristine qeh5 serial bitwise readback of 1,208,137 complex values (19,330,192 payload bytes). Compiler peak ~185 MiB is not an HSE peak.
- **Native blockers:** production native binary-packet/hook dispatch and real MPI collectives; both native SCF stop/restoration paths; common initial 48-band/k2/Fock120Ry waves; actual two-rank FFT/G/q and whole-output/peak-RAM bounds; 36 unreadable mapping entries leave global inventory UNKNOWN_REFUSE. No Boolean or component ABI receipt may grant native authority.
- **Data boundary:** inspected existing save is 44-band/k4/Fock180Ry; readback success does not make it a fixture seed or validate material convergence. Parallel-HDF5 transitively loads libmpi; serial decoder uses explicitly tested MPI-initialization refusal stubs. No claim of an MPI-free dependency graph.
- **Reproduction:** in DFT, `source scripts/env.sh`, then `python /home/User/repos/MCT-research/research/programs/microscopic_bandgap/qe75_streaming_2026-10-11/m5_readiness/validate.py`. Sequential cheap component tests/readback only; never executes native candidates. Do not reset unknown leases or overwrite completed private builds.
- **Next, only if separately assigned:** resolve production ownership/common-state/layout/inventory prerequisites; then reassess the single conditional small fixture. Full 16-atom/352-band run, lowered target physics, supervisor changes, numerical queues and goal resume remain unauthorized.

## Change log

- **2026-10-11 23:56 UTC | starting `b1a4772` | governance | PLAN CREATED |** Original native HSE host failed; software EXX stream, checkpoint storage and guard components tested; native state bridge still in progress; no accepted alloy spectra. Next: M3b qualification, then M4/M5.
- **2026-10-12 00:40 UTC | `6b21779` | M3b | CANDIDATE BUILT / NATIVE QUALIFICATION BLOCKED |** Typed old `xi`/occupation/`ethr` packets, both stop hooks, post-`punch` manifests and no-copy handoff implemented; 21 tests, 24 regressions, 14 native-unit compiles and private linking pass; no MPI/HDF5 readback or native fixture. Next: M4 owned monitor/lease and admitted tiny matched fixture before claiming M3b native success.

- **2026-10-12 01:42 UTC | M4 checkpoint (this commit; starts `f0d948e`) | M4 | PASS SMALL-SCALE / NATIVE BLOCKED |** Real foreground owner/child monitor, live kernel lease/two fake-rank receipts, actual ext4 allocations, cancellation/crash/orphan/timeout tests and exact paired small-deck/backend pins; 65 focused methods pass. Strict native inventory and missing rank/diagnostic/layout/state gates refuse launch. Protected DFT/session state unchanged. Next: source/unit native adapter and deterministic readback, only under a separately scoped continuation.

- **2026-10-12 03:08 UTC | M5-readiness checkpoint (this commit; starts `1d74a0d`) | M5 readiness | COMPONENT PASS / NATIVE BLOCKED |** Typed distinct PROFILE/JOB digests, compiled native world-rank lease and deterministic first-ACE instruments; both private candidates linked; 78 methods pass, exact serial wave/ACE/density decode checks 1,208,137 values. Existing 44-band seed is incompatible, 36 mappings unknown, production dispatch/actual collective/state/layout/full-envelope gates remain unqualified. No native run; protected state unchanged. Stop at admission boundary.
