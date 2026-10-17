# One compute acquisition plan: prioritize the 16-atom x=1/8 pair

2026-10-17 05:54 UTC; baseline `07e8c7918fb72663ac5fb5f0a0f888abec8f55ab`.
**PLAN GO, conditional recommendation; PURCHASE/JOB APPROVAL NO.** Recommend
one on-demand **n2-highmem-16, 128 GiB, us-central1**, with **500 GiB total
pd-balanced storage including boot**, for a fresh matched 16-atom host then
Cd1Hg7Te8 pair. This is a plausible procurement size, **not a capacity or
convergence certificate**. No cloud/account/credential access, native job,
build, service, source edit or purchase occurred. PBE remains closed.

## Why this cell, and what folding actually proves

**PROVEN geometric/discrete-rule identities.** Let the primitive vectors be
the rows of `Ap=(a/2)[[0,1,1],[1,0,1],[1,1,0]]`, a=6.46 Å. The historical
16-atom cell is **As=2Ap**, volume eight primitive cells (two conventional
cells), with reciprocal basis **Bs=Bp/2**. Its centered electronic K2 grid
and eight reciprocal folding sectors n∈{0,1}³ give primitive coordinates
`k=(K+n)/2`: exactly all 64 centered primitive K4 points, each weight1/64
after normalization per primitive cell. Supercell Γ contains primitive
Γ+3X+4L; sorted supercell indices alone cannot identify Γ6/Γ8.

Exchange transfers satisfy the same set identity `qp=(Qs+n)/2`: primitive
Q4 folds to eight supercell Q2 transfers **plus eight reciprocal/band sectors**.
Thus Q2 is the geometrically appropriate folded exchange mesh here, unlike
conventional8 K2/Q2, whose electronic rule contains only half the folded
primitive K4 rule. This is not eight primitive exchange sources replacing64
without the folded bands.

**Conditional operator equivalence only:** the pure host must retain primitive
translation symmetry in its full occupied density matrix; all relevant folded
bands/occupations, weights, spinor phases/normalization, kernel G+q channels,
potential zero and singularity conventions must agree. Plane-wave and FFT
truncation, ACE span/off-span error, finite empty-state prefixes, symmetry
reconstruction and nonlinear SCF basin must also be controlled. Eight complete
44-band blocks give352 states, but not necessarily a complete common-energy
prefix. Native normalized G-labelled spinors need no extra coefficient
1/√8. Geometry alone proves neither stock finite-grid HSE equality nor state
stationarity. **Matched same-cell host is mandatory.** Cd breaks primitive
translations, so no primitive-host/Cd-state splice is permitted.

The original host and Cd-at-origin inputs both retain24 species-preserving Td
operations; both native dry outputs have3 electronic irreps, weights(1,4,3)/8.
For centered K2/Q2, Γ plus all eight Q translations already requires exactly
**nkqs=8 stored source fibers**, independent of further symmetry reduction.
Actual effective lists/flags must still be checked in any future native run.
Reduced symmetry can increase electronic work; it does not enlarge this full
eight-point source set. A two-Cd arrangement needs its own chemical subgroup.

## Single resource matrix — per member, sequential host then Cd

All rows assume stock CPU QE7.5/ACE, SG15 fully relativistic NC, SOC,
HSE(.25,.106 Bohr⁻¹), fixed unrelaxed a=6.46 Å and matched geometry/axes.
GB below means10⁹ bytes; GiB means2³⁰ bytes. Stock nominal source payload is
`B=16 × NFFT × 2 spin components × nbnd × nkqs`; MPI padding, replication,
other arrays and file cache are additional. Counts are source predictions,
not new native output. **Full stationary runtime is UNKNOWN for every pair.**

| Ordered pair / role | Cell and centered electronic k / Fock q | Electrons, bands, occupation / cutoff model | Source fibers and nominal EXX buffer | Full RAM and scratch planning status |
|---|---|---|---|---|
| (a) x=0/.25, high sampling comparator | Conventional cubic8; K4/Q4 |144e/176 spinors; FD.001Ry;50/200/Fock200Ry|64; retained60³ ⇒ **77.856768GB**|Buffer alone72.51GiB; full peak unknown. 250–500GiB disk is an assumption, not a save/output bound.|
| (a), exchange-reduced alternative | Same8; K4/Q2 |144e/152; same FD/cutoffs, changed ACE/start span|**56**, not8;60³ ⇒ **58.834944GB**|Not primitive-equivalent exchange quadrature; total peak unknown. Same provisional disk envelope.|
| (a), coarse alternative, not recommended acquisition | Same8; K2/Q2 |144e/152; same FD/cutoffs|8;60³ ⇒ **8.404992GB**|Named nominal payload11.231GB; complete peak unqualified under12GiB. Eight above electron count are not certified empty/adequate.|
| (b) original x=0/.125 model, historical evidence | As=2Ap,16; K2/Q2 |288e/352; **cold MV.001Ry;90/360/Fock120Ry**|8; actual old EXX64³ ⇒ **23.622320128GB=22GiB**|Dry21.27/21.32GiB; interrupted family RSS26.72213GiB, **not full peak**. No accepted SCF. Provisional disk250–500GiB.|
| **(b) preferred new x=0/.125 model** | Same16, host and Cd-at-origin; K2/Q2 |288e/352; **FD.001Ry;50/200/Fock200Ry**, stock Davidson/full accuracy, mixing.3, adaptive_thr=false, conv_thr1e-9Ry|8; **new FFT unknown**.64³/80³/96³ scenarios ⇒ **23.622/46.137/79.725GB**|Source plus two simultaneous full-spinor EXX batches ⇒29.528/57.672/99.657GB, **not total peak or an upper range**. Plan500GiB total disk; measured output/retention limit still needed.|
| Optional second composition x=.25 in same16 | Cd2Hg6Te8; same K2/Q2, chosen arrangement declared |288e/352; identical preferred model|8 at full K2; same FFT-conditional formula|Not initially acquired/approved. Requires accepted host, exact subgroup, configuration interpretation and remaining budget.|

**Model boundaries:** original e90/cold/f120 is not successful primitive
e50/FD/f200. The preferred model changes those original numerical choices
prospectively and matches the recent primitive functional/occupation/cutoffs;
it still needs its own host qualification. Existing e90/f120 physical probes
are labels transported by true G vectors, not an equal stationary e50 state.
152 bands lost some old probe weight above152;352 likewise needs measured
coverage, FD charge/tail and folded-sector tests, not a band-count assertion.

The 64³–96³ cases are **descriptor sensitivity scenarios**, not predictions
or certified bounds. A108³ stress case already needs113.515GB source plus
28.379GB in the two batches, exceeding128GiB before other allocations.
QE chooses the EXX descriptor from cell, cutoff, k extents and FFT layout;
the old64³ cannot be copied into the new model by fiat. Persistent waves/xi,
Davidson, beta/SOC, FFT plans, buffers, MPI/BLAS/HDF5, rank padding and cache
must enter admission. Old dry21.3GiB and interrupted26.7GiB cannot supply an
upper bound. No full-SCF wall or disk bound follows from the two-second dry run.

## One machine recommendation and contingent cost

**128GiB is plausible for the prioritized16 pair**, because its known22GiB
old source and the new descriptor scenarios are materially below an8atom
64-source high-sampling case, with substantial possible overhead headroom.
Select128 rather than paying twice as much initially; do not interpret this
as permission to buy or attempt an OOM. Proposed later admission: complete
profile-specific planned resident envelope≤96GiB, scientific hard cap112GiB,
16GiB OS reserve, zero worker swap. These are **new proposed cloud limits**,
not changes to current local guards or measured adequacy. If the descriptor,
rank layout and full envelope cannot satisfy them,128 is NO-GO: request a
separately cost-approved **256GiB** configuration with a new explicit envelope,
or stop. A108³ descriptor is a definite128 rejection. No automatic upgrade;
384GiB has no established need for the prioritized model.

Official [Google general-purpose pricing](https://cloud.google.com/products/compute/pricing/general-purpose?hl=en),
Iowa/us-central1, on-demand USD, accessed2026-10-17:

| Machine | vCPU / RAM | USD/hour | 8 total VM-hours |24 hours|48 hours|
|---|---|---:|---:|---:|---:|
|**n2-highmem-16**|16 /128GiB|**1.048112**|8.38|25.15|50.31|
|n2-highmem-32|32 /256GiB|2.096224|16.77|50.31|100.62|
|n2-highmem-48|48 /384GiB|3.144336|25.15|75.46|150.93|

These are **spending scenarios, not runtime forecasts**, and apply to total
billable VM time across setup, host, Cd and readback, not hours per rank.
At [pd-balanced pricing](https://cloud.google.com/compute/disks-image-pricing)
≈$0.10/GiB-month (730h convention),250–500GiB costs≈$25–50/month or
$0.03425–0.06849/hour. Selected128GiB VM plus that disk costs approximately
**$8.66–8.93 /$25.98–26.80 /$51.95–53.60** for8/24/48 total VM-hours.
Separate boot capacity, if outside this total, adds cost. Taxes, external IP,
egress, snapshots and retained archives are excluded and need approval.
Allocated disk keeps charging after VM stop until deletion (another day of
250–500GiB costs≈$0.82–1.64, excluding snapshots); verify export
hashes, then explicitly delete unneeded VM/disks/snapshots under approved
retention. No cleanup or allocation is performed now.

[Spot](https://docs.cloud.google.com/compute/docs/instances/create-use-spot)
is discounted but can be preempted at any time; reject it for this first
multi-hour SCF unless genuine restart/recovery is independently qualified.
Use no commitment/premium image. QE supports pools, band/EXX groups, PW/FFT
and linear-algebra distribution; more vCPUs neither divides all memory nor
guarantees proportional speed. The precise stock layout must be frozen and
budgeted; this plan's buffer model is one pool/one EXX group.
[QE parallelization documentation](https://www.quantum-espresso.org/Doc/user_guide/node20.html).

## Exact acquisition boundary and science stop rule

Before **any paid VM**, obtain explicit user maximum all-in spend, region/zone,
quota/availability and current-price confirmation, selected physical model,
stock ELF/PP/input pins, exact layout/FFT memory and disk/retention admission,
bounded wall allocation and checkpoint strategy. No credentials/quota queried.
Propose at most48 total billable VM-hours for this pair including overhead,
at most24h for host, Cd only within the remainder; not a promise of convergence.
QE max_seconds/save margin must precede the approved hard deadline. Use only
stock supported restart after validated saved-state parity; existing custom
stream/restart diagnostics are not a qualified substitute. No assumed free
continuation or autorenewal.

**Stop host before Cd** on resource/output failure, missing native outer EXX
convergence, charge/FD/entropy inconsistency, failed full occupied-density
Theta or actual spatial-group qualification at unchanged1e-8, untracked Γ
sectors or insufficient spectral coverage. Preserve conventional convergence
separately from stringent symmetry: the recent primitive k4 host still FAILS
the latter. Predeclare a native save-and-exit if, after≥12 rebuilds, a sustained
>0.2eV host Γ8-character split/occupation asymmetry grows without decreasing
outer residual. This stops a trajectory, not proof no symmetric solution exists.
No retry/alternative model or averaging to manufacture a quartet.

If host passes, run only its matching Cd partner and independently qualify
its density/group/sectors. Report energy, residuals, true spinor overlaps,
complement leakage, frame/tail errors and aligned operator response; dexx is
not a full-H/eigenpair error certificate. Any≤2meV numerical contrast goal
requires its own observable error budget, not a material error claim. Even
opposite ordered Γ signs at0/.125 would bracket only the accepted ordered
model with additional continuity/sector hypotheses. Finite smearing, strain,
finite cell, HSE functional and random-configuration uncertainty remain;
no random-alloy x_c, fitted bowing or novelty claim follows.

## Evidence and verification

- Read original [minimum acquisition](../physical_input_qualification_2026-10-11/minimum_acquisition.md),
  [terminal native pilot](../native_matched_pilot_2026-10-11/decision.md),
  [primitive final/folding](../primitive_k4_hse_2026-10-17/final_qualification/next_sampling_cost.json)
  and [152/q8 source audit](../hse8_152_q8_admission_2026-10-17/decision.md).
  Frozen failures remain unchanged.
- Read actual original host/impurity `pw.in`, `pw_dry.out` and dry JSON under
  DFT/calculations/r07/cd_in_hg_pair_n2_k2_q2_e90_f120_prepare; all six hashes
  match retained manifests. Actual EXX64³ comes from later native stdout,
  not the dry output's **dense108³** descriptor.
- Tiny offline exact-fraction enumeration independently verified64 electronic
  fold points,8sources,3stars and species-preserving24Td geometry in both
  original members. Direct and reciprocal rotation maps were treated separately
  after an initial diagnostic caught their interchange; no native data changed.
  Integer buffer arithmetic and all cost multiplications were independently
  recomputed. No new testing framework or executable deck was created.
- Source reviewed at immutable qe-7.5 tag:
  [exx_grid_init/exx_qgrid_init](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/exx_base.f90#L160-L487),
  [EXX descriptor](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/exx.f90#L128-L239),
  [buffer](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/exx.f90#L480-L552),
  [simultaneous spinor batches](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/exx.f90#L1798-L1825).
- All822protected pins,76historical files and dirtyDFT status/diff verified
  unchanged. Only this planning memo and scoped R07 navigation are updated.
  Official pricing tables were verified through indexed Google pages; full
  general-purpose page retrieval timed out/exceeded parser size. Rates are
  planning evidence, not an account quote; reconfirm before approval. **STOP.**
