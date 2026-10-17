# RUNNING: the sole stock primitive k4/q4 FD-HSE control

2026-10-17 UTC; baseline ab6fbd0. **Execution admitted and actually started;
scientific outcome OPEN.** This is a live evidence checkpoint, not a native
restart certificate, converged HSE result, signed mass or x_c.

The same stock QE7.5/ACE binary and backends as k2 are running on two local
ranks. The input reversal/diff verifies that only k2/q2->k4/q4, fresh paths/
prefix and native runtime changed. All cutoffs,FD.001,HSE.25/.106,geometry,
SG15 FR NC,36e/44spinors,spin axes,atomic start and solver settings are held.
The old accepted e90/cold primitive references remain different models;
their near-degenerate quartet is not the result of this new calculation.

## Measured startup, not a forecast presented as data

Native stdout verifies **8 irreducible k points,64 distinct quarter-grid
exchange-source coordinates, Gamma weight1/64,24crystal operations and40³
EXX FFT**. Exact printed k/weights and all64source rows are retained in
`initial_native_readback.json`. Final XML is not yet available; XML stores
q-grid dimensions rather than explicit source coordinates. Both actual rank
ELFs independently match stock hash1d66c785…; native MPI reports2ranks/1node.

At the immutable **01:37:07UTC** checkpoint, after~158s:

| Observed quantity | Value |
|---|---:|
| Status |RUNNING, first ACE rebuild in progress|
| Completed outer residual records |0|
| Kernel memory peak so far |6,133,006,336B (~5.71GiB)|
| Sampled family RSS peak |6,196,469,760B; shared-page overcount|
| Worker swap peak / tasks |0 /7|
| Sampled host available minimum |23,760,388,096B|
| Sampled disk free minimum |49,351,831,552B|
| Sampled owned files+metadata maximum |2,101,248B|

The initial semilocal SCF converged in10inner iterations. Its printed
−484.82971436Ry is **not a final corrected HSE energy**; no completed HSE
trajectory, full spinor density-Theta/irrep test or material interpretation
is claimed. The initial printed Gamma quartet is degenerate at display
precision with occupations.5; this does not qualify the evolving HSE state.
The first8empty bands are displayed unoccupied; final band adequacy and
physical sectors still need saved-array validation.

## Active ownership, finite bounds and prospective stop

- Worker: `r07-pk4-1017013015.service`, invocation
  `8dee58502fd048e4bf30a09bd9053a1f`, launcher PID1999216,
  actual stock rank PIDs1999219/1999220 (start/cgroup/exe recorded).
- Private root: `/home/User/opencode_workspace/DFT/.local/p4_1017_013015`.
  Current stdout,resource samples,progress,possible stop/terminal records
  stay there; committed checkpoint files are immutable prefixes.
- Standard systemd12GiB/swap0/tasks12,CPU200%,nice10,**24h hard bound**;
  native max_seconds82800(23h) leaves one hour for stock save boundary.
  RuntimeMax starts termination2026-10-18 01:34:29UTC; configured stop grace
  is30s before group SIGKILL. No instantaneous-death or checkpoint guarantee,
  restart or second case.
- Bounded stdlib sampling: `r07-pk4-1017013015-observe.service`,256MiB/
  swap0/tasks3. Worker standard BindsTo/After relationship makes observer
  failure stop that worker. It launches no science and inventories no FDs.
  Original k2 one-off sampling is persisted for this asynchronous case,
  with the frozen printed-spectrum guideline; no new solver/owner framework.
- Host4GiB/disk10GiB floors and14GiB owned-output budget are sampled30s;
  not continuous/quota guarantees. Worker kernel memory/swap/tasks/time
  caps are hard. Observer stderr empty and both units active at checkpoint.
  No global foreign-MPI exclusion/network-namespace claim is made.

`preregistration.md` specifies the>=12COMPLETED-build early-stop guideline:
three sustained>0.2eV candidate splittings,degraded FD occupations and no rapid
residual improvement. It requests stock EXIT once. Printed33–34/35–38 are
provisional index probes, not proved irreps; final physical G-labelled complex
overlaps must confirm/refute any stop interpretation. If symmetry restores
or residual rapidly improves, continue within the finite budget. Neither
sampling nor a stop proves that no symmetric solution exists.

## Source/resource assessment and remaining scientific question

5.767GB is the unpadded nominal q64 source buffer, **not total RAM**. Other
arrays/caches remain additional; actual peak can grow and a private OOM is a
terminal failure, not authorization for a retry/cap increase. Source branch
review plus the actual12GiB hard cap and preflight headroom (available minus
worker+observer caps still>4GiB) justified this guarded acquisition. The old
4.69h/16build forecast is not a convergence or runtime guarantee;24h is finite.
No new source build, direct-exchange alternative, PBE job or paid hardware.

The decision-changing result will be whether this denser **same-FD/e50**
trajectory remains/restores symmetry and reaches actual outer SCF. This
isolates quadrature better than the old cold/e90 references; initialization
and nonlinear basin effects remain. Even success is a primitive host control,
not Cd chemistry or random-alloy x_c. No averaging split levels into a mass.

## Next review and preservation

Query the existing units and read private `science_progress.json`,
`resource_samples.jsonl`, `pw.out`, `observer.err` and any
`scientific_stop_request.json`, `resource_refusal.json`, `terminal_manager.json`.
**Do not relaunch** if units disappear: inspect terminal records/journal first.
After termination, qualify native XML/waves/charge/FD and actual Td/Theta.
k4 contains non-TRIM k points: use the actual -k fiber modulo reciprocal G,
not the unchanged k2 G->−G−2k self-fiber formula. Report reconstructed stars
separately from native saved representatives; do not launch open_grid.
Full-H eigenpair residual absence is explicit; conventional convergence is
not a universal state/material error certificate. Verify own cleanup then stop.

All822protected pins,76historical originals,old k2/HSE8 failed evidence,
stock/dirtyDFT and PBE closure are checked unchanged. No main,other session,
goal,credential or remote configuration changed. `verification.json` validates
the **RUNNING checkpoint**, not a final scientific PASS. The one bounded case
may continue asynchronously after this Codex turn; no additional job is queued.
