# HgCdTe / QE 7.5 low-RAM execution plan and reset handoff

**Plan created:** 2026-10-11 23:56 UTC (2026-10-11 19:56 America/New_York)
**Last verified update:** 2026-10-11 23:56 UTC
**Status:** ACTIVE ENGINEERING; PHYSICAL HgCdTe INVERSION REMAINS BLOCKED
**Owner:** Original `research` Codex tmux session; existing MCT research branch `research/hgcdte-impurity-tmatrix-20261010`.
**Starting verified revision:** `b1a4772`. **This plan does not authorize new numerical runs.**

## Objective and nonnegotiable boundaries

Obtain qualified first-principles HgTe host and Cd-substituted HgTe Γ6/Γ8 spectra and projector overlaps, then investigate a physically defensible alloy inversion threshold with finite-size/disorder and quantified error controls. Near-term engineering goal: demonstrate identical HSE+SOC exact exchange with a low-memory private QE 7.5 implementation **on the existing ~32-GiB VPS**, with no RAM purchase.

- Preserve HSE/SOC, 352 bands, prepared k/q meshes, cutoffs, accuracy, and stock QE for the **original 16-atom experiment**. A separately labelled tiny engineering fixture is not a downgrade of that experiment.
- Keep stock QE, all dirty DFT files, pre-existing supervisors, `calcura`/`commander` tmux sessions, and historical blocked goal untouched. No speculative results, no main merge, no DFT commit, no force push.
- No full 16-atom native run without a fresh, explicit authorization and measured RAM/disk/restart qualification. Only an independently admitted small validation fixture may use existing conditional scope.
- At most one owned MPI family; validate input/pseudopotential/binary provenance and safe resource margins. Fail closed on incompatible restart state.

## Evidence-backed milestone ledger

| ID | Deliverable and binary acceptance gate | State at 2026-10-11 23:56 UTC | Evidence |
|---|---|---|---|
| M0 | Converged binary HgTe Γ reference and cutoff comparison | **PASS: numerical reference only**; no alloy response | `state.md`; binary difference ~6.7014 µeV |
| M1 | Diagnose native 16-atom resource failure | **PASS: diagnostic**, host SCF **FAIL** | `native_matched_pilot_2026-10-11/decision.md`; 26.722-GiB summed RSS, stopped in ACE; Cd never admitted |
| M2 | Implement lossless one-q-plane streamed EXX candidate; source/build/unit checks | **PASS: software-only**; nominal `exxbuff` 22→2.75 GiB | `qe75_streaming_2026-10-11/{decision.md,verification.md}`; `ea8823e` |
| M3a | No-copy versioned checkpoint storage + read-only restoration + 64-bit guards | **PASS: component tests only**; 15 focused + 24 regression | `checkpoint_phase/{decision.md,checkpoint_contract.md}`; `b1a4772` |
| M3b | Complete native checkpoint state bridge: old ACE `xi` and occupations + HSE outer iteration + matching inner SCF/orbitals, both stop paths and post-`punch` publication; proven import | **IN PROGRESS / NOT VERIFIED** | Work started under `native_bridge/`; no committed or accepted result as of this timestamp |
| M4 | Runtime-integrated per-rank disk reservation, disk quota, filesystem, RAM and time monitoring | **PARTIAL**: APIs tested; native hooks/monitor not verified | `checkpoint_phase/resource_contract.md` |
| M5 | Native small stock-versus-streamed MPI/FFT/EXX/ACE equivalence: actions, energy, Gram/projectors; controlled restart | **NOT RUN / GATED** by M3b/M4 | `checkpoint_phase/native_fixture_protocol.md` |
| M6 | Admission of full-size host on actual RAM/disk/time using measured peak and sufficient scratch | **NO-GO**: ~31 GiB disk available versus nominal ~22 GiB stream + 10 GiB reserve + output | `checkpoint_phase/phase_outcomes.json` |
| M7 | Accepted matched 16-atom HgTe host then Cd-substituted spectra, physically labelled Γ6/Γ8 overlaps | **NOT ACHIEVED** | Host termination; Cd stage absent |
| M8 | Convergence/locality/finite-size/disorder and physical `x_c` error bounds | **NOT ACHIEVED** | `state.md`; physical input remains missing |

**Scientific truth boundary:** Calculated binary HgTe Γ splitting is not a measured or first-principles alloy `E_g(x)`. The 87.5% number is an **allocation estimate**, not native peak-RAM proof. A linked private QE executable is not a validated SCF. Do not infer a physical `x_c` until M7 and M8 pass.

## Critical path and decision points

1. **Finish M3b once**. Audit and implement exact native state capture/import with end-to-end failure injection. A byte-valid EXX file alone cannot restore the old ACE operator; never reconstruct it from current orbitals without proof. On implementation failure, write an exact blocking defect and STOP.
2. **Decouple the two engineering hypotheses where safe:** numerical equivalence of streamed exchange versus reliability of long-running checkpoint/restart. An explicitly authorized **fresh no-restart tiny fixture** may provide earlier information, but do not reinterpret the existing conditional authorization to skip its checkpoint prerequisite. Require approval of a revised test protocol before changing sequence.
3. **Pass M4 and M5** using the already scoped candidate controls when admissible: <=12 GiB monitored MPI-family RSS, >=10 GiB disk reserve, <=600 s per fixture, one MPI family, identical input/binary-backend provenance, quantitative native action/energy/Gram checks. Report numerical residuals, not just process exit status.
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

## Context-reset handoff (snapshot at creation)

- **Read first:** this file, `research/programs/microscopic_bandgap/state.md`, `qe75_streaming_2026-10-11/checkpoint_phase/{decision.md,checkpoint_contract.md,resource_contract.md,native_fixture_protocol.md}`, then DFT `AGENTS.md`.
- **Repo:** `/home/User/repos/MCT-research`; branch `research/hgcdte-impurity-tmatrix-20261010`, last verified committed `b1a4772`.
- **Active owner:** existing tmux `research`, Codex GPT-6.1-Sol xhigh. At snapshot it was working on `native_bridge/exx_checkpoint_state.f90` and QE restart paths; **untracked `native_bridge/` belongs to that active agent—do not stage/overwrite without coordination**.
- **DFT working tree:** `/home/User/opencode_workspace/DFT` contains retained modified/untracked research outputs. Private source/compiler/binary under `.local/qe75_lowram_20261011/`; original stock binary unchanged.
- **Current blocker:** no native capture/import of old ACE projectors/occupations bound to complete inner/outer QE restart, including after `punch`. No native comparison has been run.
- **Resource snapshot:** approximately 29 GiB MemAvailable; ~31 GiB free disk, 4 GiB swap. Original full stream fails retained 10 GiB disk reserve. Recheck; numbers become stale.
- **Approval:** user authorized checkpoint-bridge engineering with conditional small fixture; **no full 16-atom HSE rerun or historical blocked-goal resume**.
- **Next action:** let active agent finish an independently verifiable M3b artifact; update this ledger with test result and change-log entry, or record exact technical NO-GO.

## Change log

- **2026-10-11 23:56 UTC | starting `b1a4772` | governance | PLAN CREATED |** Original native HSE host failed; software EXX stream, checkpoint storage and guard components tested; native state bridge still in progress; no accepted alloy spectra. Next: M3b qualification, then M4/M5.
