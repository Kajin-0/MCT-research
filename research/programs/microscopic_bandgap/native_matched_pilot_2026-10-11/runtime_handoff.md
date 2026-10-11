# Terminal approved native-pilot handoff

**HOST_RESOURCE_STOP; Cd NOT ADMITTED. No live native handle. No retry.**
**Latest goal status: BLOCKED**, returned by the goal service after the same
missing-input boundary persisted through three resumed goal turns. See
[goal_boundary_audit.json](goal_boundary_audit.json). No completion or new
scientific result is asserted. Do not repeat audits or launch/restart a native
job without qualifying new evidence/fresh scope. Prior progress record follows.

The original research goal was active/unachieved; the user reactivated it after
`52e7915`. This resumed turn made progress through an approved acquisition
attempt, measured terminal failure and a cheap independent reference-irrep
check. Do not mark the objective complete. No goal status was changed by the
agent; old blocked turns do not count in the fresh resumed audit.

## Authoritative terminal record

- Unified exec session **10143 COMPLETED**. Do not poll or restart it.
- Native host:
  `/home/User/opencode_workspace/DFT/calculations/r07/approved_pair_pilot_20261011T195000_scope52e7915/host`.
- Started 19:48:51.848 UTC; stopped 20:01:04.237 UTC; 732.39 seconds.
- Result copied byte-identically to [host_result.json](host_result.json).
- Family RSS 26.72213 GiB crossed the retained 26.63966-GiB cap. The independent
  [audit](terminal_audit.json) isolates the RSS trigger; other hard triggers
  did not fire. All owned MPI descendants terminated; fresh MPI/R07 snapshot empty.
- Adaptive inner SCF converged, but EXX/final 1e-10-Ry gate FAILED. Matched-host
  projector/irrep/1-meV gates NOT EVALUABLE. [Host gate](host_gate.json) is false.
- Cd output absent. The sole host attempt consumed this approval; no Cd,
  second host, restart, variant, extra postprocessor or queue is authorized.
- Two old supervisor states and 15 original source pins remain unchanged.
  Native dirty files/scratch are preserved; no other repo is committed here.

## Preservation and boundary

The dated first resource NO-GO and later passing preflight are both valid.
Actual headroom changed; no guard/input was relaxed. Recovered RAM after stopping
is not new authorization. The interrupted RSS peak is not a successful full-SCF
maximum or planning upper bound; full runtime/peak/model errors remain unknown.

The [source-only irrep check](reference_irrep_bound.md) uses earlier accepted
primitive HgTe spinors, not the failed matched host. It supplies no chemical
packet or material error. No t_H, physical gap or x_c is known. Full/residual T,
strain, threshold, retarded/real-part distinction, directional SOC, periodic
aliasing, coverage and all earlier physical failures remain valid.

Next meaningful progress requires an independently acquired chemistry-bearing
packet or fresh authorization for a justified acquisition resource plan. No
repeats, new agents/sessions, outreach, paid allocation or supervisor operations.
If the same blocker recurs in three consecutive fresh resumed goal turns without
meaningful progress, apply the blocked rule then; this progress turn alone does
not satisfy it. [Decision](decision.md) is terminal for this finite approval.
Validate and commit/push MCT artifacts only; never merge main.
