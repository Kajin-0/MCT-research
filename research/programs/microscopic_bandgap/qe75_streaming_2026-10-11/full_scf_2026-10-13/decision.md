# Full HSE SCF evolution: real partial trajectories, occupation gate FAILED

2026-10-13 22:47 UTC; starts clean pushed7116be0, same research session.

**CALCULATED — REAL QE7.5/TWO-RANK/HSE+SOC:** genuine electrons()/inner-SCF/
outer-EXX evolution ran for matched tiny HgTe physical inputs. The corrected
control completed12 outer updates and stopped cleanly at native max_seconds480;
486.471663s including native punch/readback/cleanup. The streamed member completed
four operator generations, then the live owner refused its fourth-step occupation
comparison and stopped the owned family;173.113413s. **Neither is converged.
The full paired acceptance FAILED; steps1–3 pass, step4 fails.** No rerun or
post-observation enlargement of the preregistered1e-8occupation limit.

| Actual record | Total energy (Ry) | Fock energy (Ry) | dexx (Ry) |
|---|---:|---:|---:|
| Control last completed outer12 | −484.05799662412244 | −8.967244339726552 | 3.626147897506371e−6 |
| Control corresponding outer4 | −484.0564679351221 | −8.965583328962456 | 7.024281529055543e−5 |
| Stream outer4, refused | −484.0564679351359 | −8.965583328972652 | 7.024282504985990e−5 |

Fullprecision native scalars, waves/densities/maps and raw logs are retained.
Fock energy here is native0.5*fock2, unlike the earlier first-ACE contraction
sum. Step1 dexx0 is an initialization value, not HSE convergence. Control final
XML=false; no EXX self-consistency message, last error>1e-10Ry. Stream aborted
before final punch: its saved schema is not a final streamed SCF result.
[Actual numerical summary](numerical_result.json), [preregistration](preregistration.md).

## Decisive fourth-step falsification

At k1 the actual occupation difference is **1.4692691729933927e−8**, exceeding
**1e−8**. This is the exact first scientific refusal, retained with all raw
fourth-step records and error stack. Other observed fourth-step differences:

- Total energy:1.38e−11Ry; Fock energy:1.02e−11Ry.
- Eigenvalues:1.919420178353448e−11Ry(limit2e−7Ry).
- Occupation-weighted orbital density:7.776699230049112e−9relative Frobenius
  (limit1e−7); k2/k3 around1e−11.
- rhoR:4.732880753977042e−13native units; rhoG:4.063752195989359e−15
  (both limits1e−9); vrs:4.67803573656056e−12Ry(limit1e−8Ry).

**FALSIFIED:** this pair does not satisfy the preregistered standalone occupation
criterion. This does **not** falsify the earlier bitwise fixed-input Fock/ACE
result, which is unchanged, or prove altered HSE physics. It does not constitute
a qualified full-SCF equivalence result simply because energy differences are tiny.

**HYPOTHESIS / OPEN cause:** tiny spectral/common Fermi-energy differences may be
amplified by numerical smearing. Highprecision Fermi energies were not captured,
so this cause is not established. A next criterion must be independently derived
from the actual smearing/eigenvalue/Fermi uncertainty and density-operator
sensitivity, before another run; it must not be chosen just above1.469e−8.
The present gate remains failed. Individual orbital byte equality was never
presumed; weighted-density comparison is invariant to appropriate phase/band
rotations. The old rhoR6.66e−16/vrs1.03e−13byte refusal is preserved unchanged.

## Genuine trajectory and resource evidence

Control outer11→12 charge relativeL2 change:5.74606e−6; maximum rhoR change
1.32422e−5native units. Occupation-weighted orbital-density changes at k1/k2/k3:
1.31775e−3/3.91094e−5/2.00823e−5. These are *changes between SCF states*, not
||Hpsi−epsilon psi|| residuals or material linewidths. Native inner estimated
SCF accuracy, ethr, tr2 and dexx are separately preserved. Nonmonotonic energy/
dexx steps occur; no monotonic-convergence assumption or fitted gap law is used.

| Resource | Control12 steps | Stream4 steps, refused |
|---|---:|---:|
| Summed sampled family RSS bytes | 963,956,736 | 553,095,168 |
| Last observed cgroup memory peak bytes, including cache | 1,800,224,768 | 1,083,039,744 |
| Minimum sampled MemAvailable bytes | 30,112,305,152 | 30,316,838,912 |
| Minimum sampled free disk bytes | 27,367,337,984 | 26,581,319,680 |

Work counts differ: **no whole-SCF memory/performance improvement claim**. Real
admission kernel12GiB/swap0/tasks12/AS896MiB/file1GiB/hard600s; zero observed cap
or pressure events. Control's unloaded terminal manager record displays default
infinite limits: those defaults are **not the running limits**. Actual admission
kernel records and runtime counters prove applied caps; successful wait-client0,
both post-punch receipts/JOBDONE/empty group prove clean control termination.

The new scope5 local contract retains4GiBhost/10GiBdisk floors and sampled14GiB
owned-output budget, inode/block/deleted-open accounting and disclosed between-
sample producer/external-writer risks. No original host-wide MPI exclusion or
private-network claim is promoted. Byte-identical independent seed/PP copies,
same48bands/90-360-120Ry/k2/q2/SG15/HSE(.25/.106)/SOC/solver/tolerances. Both new
source compilations O2/no-fast-math/bounds-checks; exchange arithmetic unchanged.
Only operational native time limit480 reserves grace within hard600.

## Targeted implementation results and failures retained

1. Real full-SCF path replaces the diagnostic stop only in NEW private builds;
   the qualified fixed-operator experiment is never rerun or edited.
2. Each streamed generation uses live all-rank reservation after old readers
   return and old qstore closes/deletes. Four actual generations reserve exactly
   201,326,592bytes/rank, distinct inode IDs, no whole-store copy. Old-store
   presence refuses overwrite. Actual full-SCF generation lifecycle advanced.
3. First control attempt reached real second HSE update, then refused missing
   step1 observation: hook was placed in inactive restart branch. Corrected
   source placement and exact branch check; old91.832sFAILED result kept. Fresh
   corrected control restarted from the original seed, **not** unqualified partial
   state. One targeted correction; no unchanged retry campaign.
4. Stream initially refused disk admission before service/lease mutation because
   generic805MiB/rank maximum overbudgeted scratch. Native control FFT proves
   exact201,326,592B/rank bound; native larger extents still refuse. Subsequent
   reservations use14GiB minus already-accounted retained output, plus actual
   extents conservatively. Same14GiB budget/10GiBfloor, not relaxed policy.
5. Native control final collected wave and reciprocal-density HDF5 readbacks are
   **bitwise exact against actual native buffers**. Both live final receipts,
   quiescent files, numerical layers and clean owned teardown passed. Stream
   stopped on the scientific gate before final punch, so no stream final-state
   readback or restart is claimed. No extra generic test suites; one small
   independent orbital-metric check and real-data pass/failure replay only.

## Restart boundary and decision

**OPEN / NOT ATTEMPTED:** new fresh-scope5 refuses import. Control partial state
has exact current wave/rhoG readback, but the combined oldoperator/occupations/
inner/outer-state atomic import has not been natively qualified. Aborted stream
has no matching post-punch oldACE/state publication; files alone do not authorize
continuation. No automatic resume after time limit/refusal, no available native
restart receipt. Legacy bridge/negative old-current-basis results remain intact.

**STOP at measured scientific boundary.** Keep12-step control trajectory,3passed
paired steps and failed4th occupation bound. Next minimum input is highprecision
native Fermi energy and an independently justified smearing-sensitivity error
budget; native checkpoint capture/import qualification remains indispensable
before any continuation. Do not patch the failure with empirical gap parameters
or a posthoc occupation tolerance. No converged HSE, Cd/material xc,16atom/352band
run, RAM purchase, goal/session/agent/stock/dirty-DFT/supervisor changes. All own
units collected/lease free; only uniquely owned dispensable escrows retired.
