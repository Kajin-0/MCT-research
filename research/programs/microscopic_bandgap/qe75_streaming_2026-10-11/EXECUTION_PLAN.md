# HgCdTe / QE 7.5 low-RAM execution plan and reset handoff

**Plan created:** 2026-10-11 23:56 UTC (2026-10-11 19:56 America/New_York)
**Last verified update:** 2026-10-12 01:42 UTC
**Status:** M4 FINITE PHASE COMPLETE; NATIVE ADMISSION AND PHYSICAL HgCdTe INVERSION REMAIN BLOCKED
**Owner:** Original `research` Codex tmux session; existing MCT research branch `research/hgcdte-impurity-tmatrix-20261010`.
**Starting verified revision:** `b1a4772`. **Latest native bridge revision:** `6b21779`. **Latest M4 checkpoint:** runtime-admission artifacts in this commit, starting `f0d948e`. **This plan does not authorize new numerical runs.**

## Objective and nonnegotiable boundaries

Obtain qualified first-principles HgTe host and Cd-substituted HgTe Γ6/Γ8 spectra and projector overlaps, then investigate a physically defensible alloy inversion threshold with finite-size/disorder and quantified error controls. Near-term engineering goal: demonstrate identical HSE+SOC exact exchange with a low-memory private QE 7.5 implementation **on the existing ~32-GiB VPS**, with no RAM purchase.

- Preserve HSE/SOC, 352 bands, prepared k/q meshes, cutoffs, accuracy, and stock QE for the **original 16-atom experiment**. A separately labelled tiny engineering fixture is not a downgrade of that experiment.
- Keep stock QE, all dirty DFT files, pre-existing supervisors, `calcura`/`commander` tmux sessions, and historical blocked goal untouched. No speculative results, no main merge, no DFT commit, no force push.
- No full 16-atom native run without a fresh, explicit authorization and measured RAM/disk/restart qualification. Only an independently admitted small validation fixture may use existing conditional scope.
- At most one owned MPI family; validate input/pseudopotential/binary provenance and safe resource margins. Fail closed on incompatible restart state.

## Evidence-backed milestone ledger

| ID | Deliverable and binary acceptance gate | State at 2026-10-12 01:42 UTC | Evidence |
|---|---|---|---|
| M0 | Converged binary HgTe Γ reference and cutoff comparison | **PASS: numerical reference only**; no alloy response | `state.md`; binary difference ~6.7014 µeV |
| M1 | Diagnose native 16-atom resource failure | **PASS: diagnostic**, host SCF **FAIL** | `native_matched_pilot_2026-10-11/decision.md`; 26.722-GiB summed RSS, stopped in ACE; Cd never admitted |
| M2 | Implement lossless one-q-plane streamed EXX candidate; source/build/unit checks | **PASS: software-only**; nominal `exxbuff` 22→2.75 GiB | `qe75_streaming_2026-10-11/{decision.md,verification.md}`; `ea8823e` |
| M3a | No-copy versioned checkpoint storage + read-only restoration + 64-bit guards | **PASS: component tests only**; 15 focused + 24 regression | `checkpoint_phase/{decision.md,checkpoint_contract.md}`; `b1a4772` |
| M3b | Complete native checkpoint state bridge: old ACE `xi` and occupations + HSE outer iteration + matching inner SCF/orbitals, both stop paths and post-`punch` publication; proven import | **CANDIDATE BUILT; UNIT TESTS PASS; NATIVE RESTART NOT QUALIFIED** | `native_bridge/{decision.md,closure_and_boundaries.md,validation.json}`; `6b21779`: 21 bridge tests, 24 storage regressions, 14 native-unit compiles and private link; real native MPI/HDF5 readback unverified |
| M4 | Foreground family ownership/live lease, exact reservations, quota/filesystem, RAM/disk/time and fixture admission | **PASS SMALL-SCALE COMPONENTS / NATIVE ADMISSION BLOCKED**: 17 real fake-process lifecycle + 7 preflight checks; live kernel lease and all-fake-rank receipts; native rank adapter, typed profile binding, layout/output/common-wave certificate and complete global inventory missing | `runtime_admission/{decision.md,ownership_and_limits.md,validation.json,runtime_results.json,preflight_results.json}` |
| M5 | Native small stock-versus-streamed MPI/FFT/EXX/ACE equivalence: actions, energy, Gram/projectors; controlled restart | **NOT RUN / GATED**: live MPI/HDF5 wave, density and ACE readback, stop/failure collectives and monitor/lease unverified | `native_bridge/decision.md`, `checkpoint_phase/native_fixture_protocol.md` |
| M6 | Admission of full-size host on actual RAM/disk/time using measured peak and sufficient scratch | **NO-GO**: ~31 GiB disk available versus nominal ~22 GiB stream + 10 GiB reserve + output | `checkpoint_phase/phase_outcomes.json` |
| M7 | Accepted matched 16-atom HgTe host then Cd-substituted spectra, physically labelled Γ6/Γ8 overlaps | **NOT ACHIEVED** | Host termination; Cd stage absent |
| M8 | Convergence/locality/finite-size/disorder and physical `x_c` error bounds | **NOT ACHIEVED** | `state.md`; physical input remains missing |

**Scientific truth boundary:** Calculated binary HgTe Γ splitting is not a measured or first-principles alloy `E_g(x)`. The 87.5% number is an **allocation estimate**, not native peak-RAM proof. A linked private QE executable is not a validated SCF. Do not infer a physical `x_c` until M7 and M8 pass.

## Critical path and decision points

1. **Validate M3b, do not redesign it again without evidence.** Candidate `6b21779` now captures old `xi`, occupations, current tolerance/state scalars, both stop hooks and post-`punch` atomic manifests. Unit compilation and synthetic tests pass. The remaining falsifiable check is real QE MPI/HDF5 state readback and old-versus-current ACE action after native restart. Any failed readback or state mismatch must be recorded as an explicit defect; no restart success is claimed from synthetic tests.
2. **Decouple the two engineering hypotheses where safe:** numerical equivalence of streamed exchange versus reliability of long-running checkpoint/restart. An explicitly authorized **fresh no-restart tiny fixture** may provide earlier information, but do not reinterpret the existing conditional authorization to skip its checkpoint prerequisite. Require approval of a revised test protocol before changing sequence.
3. **Retain the passed M4 fake-process gate; close native integration before M5.** The foreground owner/monitor, live flock/peer credentials, identity-safe cancellation, actual tiny ext4 reservations and exact small deck/backend fingerprints now pass. Native bridge entry requires live RPC; Boolean/file receipts cannot grant authority. Implement a compiled native two-rank registration and bridge PROFILE/JOB binding, deterministic first-ACE/readback instruments, certified stream/state/output extents and common waves. Strict global inventory currently refuses unreadable pre-existing mappings. No native admission is issued. Only after every retained gate passes may the single scoped sequential control/stream fixture use <=12 GiB sampled family RSS, >=10 GiB free disk, >=4 GiB MemAvailable and <=600 s running wall. These sampled guards are not cgroup hard ceilings. Stop on any discrepancy; no speculative launch.
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

## Context-reset handoff (updated 2026-10-12 01:42 UTC)

- **Read first:** this file, `runtime_admission/{decision.md,ownership_and_limits.md,handoff_ledger.md,validation.json}`, R07 `state.md`, retained `native_bridge` and `checkpoint_phase` decisions/protocols, then DFT `AGENTS.md`.
- **Repo:** `/home/User/repos/MCT-research`; existing branch `research/hgcdte-impurity-tmatrix-20261010`; M4 starts `f0d948e`, native bridge remains `6b21779`. This commit contains the tested M4 package, native Python entry fence and these ledger updates. No main merge or DFT commit.
- **Owner/status:** original research conversation; finite M4 phase ends here. Tests ended with no live owned fake workers, no lease holders and FINISHED own registry. Recheck live state; do not clear an unknown/stale family. Existing `calcura:$0`, `commander:$1`, `research:$3` preserved. Historical blocked goal unchanged.
- **DFT preservation:** HEAD `422d71d`, all prior dirty paths, 17 protected input/PP/supervisor pins, stock archive/executable and both prior candidates unchanged. New disposable artifacts only under `.local/qe75_lowram_20261011/runtime_admission/`.
- **Passed gate:** 65 focused methods: 17 real fake-process lifecycle, 7 preflight, 21 serial bridge-codec, 15 checkpoint and 5 source regressions. Actual tiny reservations, live all-fake-rank authorization, crash cleanup, double-crash readmission refusal and exact small deck/source/compiler/backend pins. No native PW/MPI/HSE execution.
- **Blockers:** compiled native rank/lease and PROFILE/JOB binding, deterministic EXX/energy/Gram/ACE instruments and density/wave/old-ACE readback, exact native layout/output envelope and common initial waves; unreadable mappings leave global MPI inventory UNKNOWN. M4 native admission BLOCKED; M5 NOT RUN.
- **Resource snapshot:** roughly 29.6 GiB MemAvailable and 30.2 GiB disk; fake-family peak ~0.10 GiB summed RSS with separately reported PSS/shared overcount. These are not native peaks. Full nominal 22-GiB stream + 10-GiB reserve still fails disk admission.
- **Reproduction:** from `runtime_admission/`, `/home/User/repos/MCT-research/.venv/bin/python validate.py`. This executes only bounded fake/serial tests and read-only fixture preflight, not QE/MPI. A retained non-FINISHED ledger must refuse rather than auto-reset.
- **Next gate if assigned:** compiled native rank adapter + first-ACE/readback source instrumentation and certified small budgets/inventory. No full 16-atom HSE run, supervisor change, extra fixture, goal resume or automatic new campaign is authorized by this handoff.

## Change log

- **2026-10-11 23:56 UTC | starting `b1a4772` | governance | PLAN CREATED |** Original native HSE host failed; software EXX stream, checkpoint storage and guard components tested; native state bridge still in progress; no accepted alloy spectra. Next: M3b qualification, then M4/M5.
- **2026-10-12 00:40 UTC | `6b21779` | M3b | CANDIDATE BUILT / NATIVE QUALIFICATION BLOCKED |** Typed old `xi`/occupation/`ethr` packets, both stop hooks, post-`punch` manifests and no-copy handoff implemented; 21 tests, 24 regressions, 14 native-unit compiles and private linking pass; no MPI/HDF5 readback or native fixture. Next: M4 owned monitor/lease and admitted tiny matched fixture before claiming M3b native success.

- **2026-10-12 01:42 UTC | M4 checkpoint (this commit; starts `f0d948e`) | M4 | PASS SMALL-SCALE / NATIVE BLOCKED |** Real foreground owner/child monitor, live kernel lease/two fake-rank receipts, actual ext4 allocations, cancellation/crash/orphan/timeout tests and exact paired small-deck/backend pins; 65 focused methods pass. Strict native inventory and missing rank/diagnostic/layout/state gates refuse launch. Protected DFT/session state unchanged. Next: source/unit native adapter and deterministic readback, only under a separately scoped continuation.
