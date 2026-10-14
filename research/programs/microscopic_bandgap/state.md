# Program state: microscopic zero-temperature bandgap

**Portfolio contribution:** R07

**State:** historical physical goal BLOCKED; exploratory PBE+SOC host/Cd response has measured probe, k and cutoff sensitivity; full cutoff/BZ/material accuracy OPEN; small HSE assessed only, no admitted full 600-s HSE pair; HSE-grade/dilute input and physical x_c OPEN; original failures/full-target gates preserved

**Updated:** 2026-10-14

## One measured cutoff pair and separate HSE assessment — 2026-10-14 20:34 UTC

[Finite decision](chemical_cutoff_2026-10-14/decision.md): starting31e872e,
ONE sequential stock PBE+SOC8atomHg4Te4/CdHg3Te4 pair increases40/160→50/200Ry,
unchanged176bands144e/6.46A/SG15FR/FD.001Ry/k2/nativeTd/solver. Both SCFs
converge11iterations226.27/212.73s, independent all-k charge<1.3e-11e;
both live rank/resource/terminal gates PASS. Original host uncertainty retained.

Exact NC physical-vector isometry embeds ORIGINAL7809PW host frame into10827PW
with3018new-only zeros, no truncation/renormalization/index overlap; all24Tdmaps
pass. W2 response+.393337031960eV vs+.395351851152eV: measured−2.014819meV.
Conditional cutoff-difference interval[−9.57679,+5.54715]meV includeszero.
W1–3 shifts−1.83450…−2.05337meV; all new conditional response intervals positive.
Secondary new50host-frame change+.087142meV is kept separate. Seven focused
actual-data/math/source checks pass; full cutoff/BZ/material errors remainOPEN.

PeakRSS1.038GB/kernel.954GB under12GiB/swap0/tasks12/600s, hostRAM>28.72GB/
disk>65.45GB; final aggregate499945472B under sampled14GiB. Both groups absent,
knownflockfree/oldledger unchanged; protected stock/dirtyDFT exact. No retry,
NSCF/HSE/16atom/jobqueue, other session/supervisor/Calcura or historicalgoal action.
All prior occupation/neutrality/owner/RAM failures and full-target gates remain.

[HSE source assessment](chemical_cutoff_2026-10-14/hse_feasibility.md) has no launch:
complex Gamma/q1 buffer1.133GiB subtotal, k2/q2 buffer9.064GiB before fulloverhead;
actual old2atom ACErebuild25.19s/unconverged14updates. 8atom Gamma14-rebuild
heuristic~25min is not a convergence guarantee; full600s HSE unqualified.
Rank missing HSE input as actual8atom ACE timing/wholepeak/descriptor under a
separate scope. Best next current-cost chemistry test is PBE50/200unshifted3x3x3,
four exactTd/TRstars and estimated220–260s/member, NOT launched/admitted here.
STOP this finite cutoff phase. No material signed gap, HSE convergence or x_c.

## Probe sensitivity and one matched k refinement — 2026-10-14 18:24 UTC

[New finite decision](chemical_uncertainty_2026-10-14/decision.md): retained native
complex spectra give all30 preregistered W=1–3eV/reference-offset probes. Response
range .382321–.411168eV (28.85meV probe sensitivity), conditional interval union
[.379519,.417418]eV positive. This is a spectral-probe choice, not material error.

ONE fresh sequential matched stock PBE+SOC pair keeps8atomx.25/a6.46A/SG15FR/
176bands144e/40/160Ry/FD.001Ry and refines to Gamma-containing unshifted2x2x2.
Both native SCFs converge11iterations,162.92/158.32s; weighted charge errors
<2.7e-11e. Exact Td atomic/mesh proof permits4 native stars with weights1:3:3:1,
native Gamma saved withoutNSCF. New nosym=false route is explicitly distinguished
from oldnosym=true; measured difference is method/grid sensitivity, not a pure
certified BZ error. Primary ORIGINAL physical host frames remain fixed.

W2 DeltaOmega+.3953518512eV versusold+.4010050707eV: measured−5.65322meV,
conditional grid-difference interval[−13.22899,+1.92255]meV includeszero. Both
tested grids keep positive chemical response; no BZ convergence/material gap/x_c.
Fermi/Gamma8-reference recipes agree at schema precision; separately usingnew
host frame changes refined response only+.06218meV. Complex frame normalization,
translation and Td labels independently checked. Six focused tests pass.

Both NEW terminal owners/resource gates pass with real typed leases/managerexit0/
kernel exits/empty groups. RSS<.78GB, kernel<.70GB under12GiB/swap0/tasks12/600s;
hostRAM>27GiB/disk>61GiB; final retained aggregate360718336B under sampled14GiB.
Original host terminal uncertainty and all olderFAILs unchanged. Stock/dirtyDFT/
oldledger/supervisors/Calcura/sessions/goal protected; no NSCF/retry/other campaign.
Stop this finite pair. Highest-information next input is matched cutoff
qualification on the same frame/grid; HSE/cell/functional/ionic errors remainOPEN.

## First chemistry-bearing native pair — 2026-10-14 17:42 UTC

[Decision and actual evidence](chemical_pbe_pilot_2026-10-14/decision.md): new
explicit user scope authorizes a separate affordable exploratory PBE+SOC cell,
not a downgrade of original16atom352band HSE. ONE fresh sequential stock-QE
two-rank pair,8atom cubicHg4Te4/CdHg3Te4 atx.25,a6.46A,40/160Ry,176bands,
144electrons,FDsigma.001Ry,supercellGamma. Native SCF11/12 converge in42.16/
43.35s,charge residuals3.05e-11/8.95e-12electron. Both7809PW spaces agree;
full complex NC overlaps and fcc-translation/Td characters identify host
Gamma6/8, then measure substituted spectral weight. No CdTe/dry-init shortcut.

Specified W2eV Gaussian projected ordering changes+.4010050707eV, conditional
completion/nearby-projector/arithmetic interval[.3971702205,.4048399209]eV.
Dominant host-character levels shift+.3812465558eV;Gamma6/8 dominant weight
.97634757/.99199916. These are periodic exploratory chemical responses, not
material gap/linewidth/T-matrix/x_c. Unknown cutoff/grid/functional/finite-cell/
eigenpair errors are outside the interval. First genuinely chemical input now
exists; earlier absence statements below refer to earlier datasets/scopes.

Both local resource guards pass:12GiB/swap0/tasks12/600s,host4GiB/disk10GiB
floors,sampled aggregate14GiB output;peaksRSS<.6GB/kernel<.52GB,owned groups
empty/lockfree. Original host terminal-manager recording is UNCERTIFIED after
post-computation NumPy serialization error,accepted=false retained. New Cd
scope accepts independently scientific host+guard/kernel-exit/cleanup evidence;
Cd manager/exit0 fully recorded and passes. No old owner FAIL override.
Two setup refusals and a prepublication joint-bound cross-term correction are
retained. Six focused independent mathematical/native-data checks pass.

STOP this finite pair at material uncertainty boundary; rank next input as
controlled matched chemical functional/cell/grid qualification. Original48band
root still rejects352band/288e, original HSE memory/numerical/owner failures
remain, no new HSE convergence/restart/streaming RAM gain. Stock/dirtyDFT/old
ledger/supervisors/Calcura/sessions/historicalgoal preserved. See scoped
[handoff](chemical_pbe_pilot_2026-10-14/handoff_ledger.md); no manuscript/novelty claim.

## Physics-first native existing-data checkpoint — 2026-10-14

[Measured decision](finite_q_host_probe_2026-10-14/decision.md): one bounded
read-only contraction of accepted native HgTe HSE+SOC f120/k4q4 spinors, all64k,
44 bands, in the earlier physical Γ6/Γ8 reference frame. Specified cell-periodic
wavepacket probe W=.5eV/eta=.025eV: ordering−84.771483meV, conditional completion
interval[−86.199614,−83.343353]meV. Native Γ gap−289.770114meV is a different
observable. Non-Γ Γ8-probe near-window weight.0534063; no impurity vertex/A or
bulk-continuum theorem inferred. Global uncomputed band weight19.03/23.91%
never renormalized; known high-energy separation>=4.94948eV limits the combined
centroid tail to1.428131meV under explicit eigenpair/metric/input assumptions.
Operator, native residual, grid-to-continuum and material errors remain unknown.
Old chemical mass floorp=.05 not passed or changed by this diagnostic.

Actual6.9483s, RSS511127552B under512MiB/60s analysis limits. Integral,
actual-spinor origin/unitary/relabel, closure and positive-tail checks pass.
Initial helper dependency and XML/HDF unit intake refusal retained; explicit
tpiba conversion fixed without changing scientific tolerances. No QE/MPI,
supercell, native retry or infrastructure campaign. Stock/dirty DFT/old failures/
supervisors/Calcura/other sessions and historical goal unchanged.

Six prepared chemical schemas have zero eigenvalue sets; incomplete privatePBE
host has no Cd result. CdTe binary and its rejected scattering-frame trial are
not substituted spectra. Qualified root is explicitly48band/3k/36e and cannot
admit352band/288e target. STOP native acquisition at exact profile/input gate;
highest-information missing packet remains self-consistent matched host/Cd Γ
eigenvalues and physical complex overlaps with coverage/alignment/residuals.
Existing Kajin SSH identity now publishes research branch; prior authentication
failures remain dated history. No new converged HSE/material x_c/RAMgain claim.

## Prospective terminal ownership — 2026-10-14 15:20 UTC

[New finite decision](qe75_streaming_2026-10-11/terminal_owner_2026-10-14/decision.md):
rooted native control12 checkpoint preserved in local commit89922a7; ordinary Git
push fails authentication/access. Narrow non-MPI test distinguishes live rank FD
EACCES (refuse) from pinned kernel task exit, with authenticated final receipts,
retained clean manager invocation and empty cgroup. Two tiny actual user-service
controls pass valid retirement/refuse nonzero exit; source/account wiring keeps
all numerical/resource gates. Prospective native integration remains unissued.
The historical native EACCES cause stays OPEN; original RESULT stays FAILED,
stream never ran, no new native attempt/restart. Publication/final prospective
freeze is the next gate. No Calcura, other session, supervisor, goal, stock or
dirty DFT operation; no material x_c/convergence/memory-gain inference.

## Safeguarded Fermi-root checkpoint — 2026-10-14 14:56 UTC

**CALCULATED / SOLVER PASS, OWNER FAIL:** [decision](qe75_streaming_2026-10-11/fermi_root_2026-10-14/decision.md).
All 18 complete historical control snapshots were audited first. The separately
authorized private solver certifies increasing, unique cold-smearing roots under
stated numerical evaluation bounds and refuses competing roots. Independent
high-precision and actual native scalar-object checks pass; exchange/ACE objects
and physical inputs are unchanged. Old occupation and neutrality FAILs remain.

ONE fresh two-rank control completed 12 accepted outer updates. Maximum charge
error 9.590905847289832e-11 electrons; step-five bias removed in this new solver
scope. Last total/Fock energies −484.05800703870875/−8.967178784294628 Ry and
dexx 2.2422123699072927e-5 Ry: HSE NOT CONVERGED. Exact final wave/rhoG readback,
both final rank receipts and native return zero/JOB DONE are recorded separately
from owner acceptance. After the receipts the owner refused EACCES on registered
rank-zero `/proc/1905562/fd`; original failed RESULT preserved. Stream never
launched, no retry/restart. Terminal race is only a hypothesis.

Elapsed 520.352 s, sampled RSS 966787072 bytes, last observed cgroup peak
1805807616 bytes including cache; RAM/disk floors and kernel caps held. Own unit
collected, group empty, lock free; stock/dirty DFT/history/ledger/supervisors and
other sessions preserved. User cache cleanup resolves old disk pressure only.
Next exact gate is identity-safe terminal ownership, first with non-MPI evidence.
No whole-SCF memory gain, Cd, 16-atom acquisition, physical x_c or goal change.

## Cold-smearing/strict-neutrality checkpoint — 2026-10-13 23:58 UTC

**CALCULATED / STOP:** [finite decision](qe75_streaming_2026-10-11/smearing_conditioning_2026-10-13/decision.md).
All retained old4steps/allk occupations reproduce bitwise with the exact source
Fermi replay; MVT upper1.470077639e−8 explains old1.469269173e−8 mismatch. Historical
old1e−8 FAIL unchanged. Separate prospective eigen/ef energy/density gates frozen.
Only ef observer changes native objects. ONE fresh control5outer/202.288781s,
4accepted, refuses5: charge36.00559692012919, native ef.6714859435488899Ry,
N'~2e−12/N''60967; nonneutral squared-error minimum accepted by QE0.01e cold
fallback. Samebias in old control5. Stream never launched, no retry or final
restart capture. LastE−484.0541752300362/Fock−8.968516026300037Ry, unconverged.
RAM/disk/kernel/lease gates held; ownfamilyempty/stock/dirtyDFT/oldledger/sessions
preserved. Next minimum proof is strict charge-root acceptance at SAME smearing;
solver behavior change requires new scope. No physicalxc/Cd/16atom/RAMgain claim.

## Full-SCF numerical/scientific checkpoint — 2026-10-13 22:51 UTC

**CALCULATED / PARTIAL:** [full-SCF decision](qe75_streaming_2026-10-11/full_scf_2026-10-13/decision.md)
records real control12HSEouter updates/486.471663s/native480softstop, finalE
−484.05799662412244Ry/Fock−8.967244339726552Ry/dexx3.62615e−6>1e−10. Exact
native wave/rhoG HDF5readback/both finalreceipts/cleanowned exit, not convergence.
Stream4generations/173.113413s passes commonsteps1–3; fourthstepoccupation
1.469269e−8>prereg1e−8 fails. Other state/energy differences tiny, but fullpaired
acceptance remains FAILED. No toleratedrerun or restart; highprecisionFermi and
independent smearing-sensitivity budget missing. Previous fixed-Fock bitwise
success/fullstatebyte refusal preserved. Native qstore generation life advanced;
operatorimport remainsOPEN. Counts12vs4 unmatched, no whole-SCF RAMgain claim.
Stock/original352band/dirtyDFT/ledger/sessions preserved, ownunitscollected/lease
free; historicalgoal unchanged, no physicalxc/Cd/material convergence claim.

## Actual fixed-orbital streamed EXX/ACE — 2026-10-13 21:01 UTC

**CALCULATED:** [native fixed-operator decision](qe75_streaming_2026-10-11/fixed_operator_2026-10-13/decision.md)
qualifies ONE real two-rank48-band HgTe HSE+SOC90/360/120Ry/k2/q2 streamed first
ACE. Replayed actual control source/trial/probe inputs and full kernel/FFT
readbacks; all active corresponding direct/Gram/ACE/projector/energy outputs
bitwise identical at all3k. Native weighted contraction−17.885954461447270Ry,
difference0, independently WG-trace/Gram/action checked. No final SCF Fock term,
HSE convergence, Cd or physical xc inference. Original rhoR/vrs full-state
refusal unchanged; new fixed Fock driver does not run SCF. Original raw control
auxiliary tables were not captured; reconstruction remains source-conditioned,
independently tested by real action equality.

Stream96.193434s/RSS629506048B/cgrouppeak982867968B incl.cache, sampled floors
30.399GBRAM/28.908GBdisk, no cap events. No matched whole-SCF memory-gain claim.
Original owner RESULT remains FAILED for post-completion cgroup-file deletion
race after both6receipts; raw stack/samples retained. Numerical qualification
is separate; completion-only future fix tested offline, not a native rerun.
Two setup-only attempts retained (inactiveWK serializer refusal then completed
kernel capture/ENODEV). Stock/dirty DFT/old ledger/sessions unchanged, groups
collected/lease free. Stop finite authorized operator scope; physical acquisition
and full SCF/restart boundaries preserved. Historical goal never changed.

## Actual first-ACE control and refused pair — 2026-10-13 19:33 UTC

[Measured native decision](qe75_streaming_2026-10-11/native_pair_execution_2026-10-13/decision.md):
one complete two-rank control first ACE, native12 packets/two phase6 receipts,
112.925992s, RSS884166656bytes; independent Gram/ACE-action checks pass.
Original post-exit monitor race and lost raw telemetry retained, no full HSE
convergence. Real streamed startup fails byte parity before EXX: orbitals/rhoG/
occupations/maps identical, rhoR6.66e−16/vrs1.03e−13Ry differences. Paired operator
comparison and streaming memory gain remain unqualified. Sampled local contract
explicitly differs from unpassed global inventory; old negative results preserved.
No further native run; precise next requirement is proven canonical operator-
state replay/readback. All own groups empty; stock/old ledger/dirty DFT/sessions
preserved. No16atom, Cd, material x_c or historical-goal change.

## Actual stock native HSE evidence — 2026-10-13 17:18 UTC

**CALCULATED, not fully converged:** [independently retained stock experiment](qe75_streaming_2026-10-11/native_first_ace_2026-10-13/decision.md)
verifies two MPI ranks, primitive HgTe/48 spinor bands, HSE+SOC90/360/120Ry/k2/q2,
14 real outer EXX iterations, last total energy−484.05790653Ry, dexx3.87e−6Ry,
Fock ACE−8.96709093Ry; XML convergence=false and MAX_SECONDS420. Own journal
peak706,560,000bytes/swap0. Save93,390,854logicalbytes, independent NC wave Gram
errors≤3.2e−15. This is genuine native progress and a compatible initialization
seed, not a final material gap, isotope/temperature result, Cd response or x_c.

The same finite task prepares separate seed copies and a source-candidate local
first-ACE owner. One **NON-MPI** production launch-refusal probe verifies actual
cgroup12GiB/swap0/tasks12/AS896MiB and cleanup. Native rank callbacks/lease lifetime
and numerical EXX/ACE equivalence remain unqualified. Actual native release is
refused before mutation because14GiB output allowance/per-file limits do not
certify retained backend/tempfile generations. No new QE/HSE/MPI or16-atom job
was launched by this Codex phase. Source intentional-error85 versus MPI_ABORT(1)
terminal semantics are corrected. Larger PBE host remains incomplete; smaller
160-band PBE is confirmed rejected for too few noncollinear bands; no Cd packet.
All older dated software/no-native statements below are retained historical
conditions. The historical blocked goal, original HSE352-band settings, stock,
protected DFT files/supervisors and other sessions remain unchanged.

## Separate finite QE low-RAM engineering task

The separately authorized [native bridge phase](qe75_streaming_2026-10-11/native_bridge/README.md)
implements a compiled candidate with exact old xi/occupations, current wg/et,
HSE outer scalars including **ethr**, both EXX stop hooks, post-punch publication,
native-file hardlink/atomic transactions, explicit old-operator import and a
checked reserved-inode producer handoff. It adds the missing natural inner-limit
SCF record and refuses atomic/random wavefunction fallback. **21 serial methods,
24 storage regressions, 14 native-unit compiles and six unchanged reader/ACE
body checks pass; a private binary links but is never executed.** Full native
MPI/HDF5 readback and the owned monitor/whole-job lease/admission profile remain
unqualified. Decision **STOP_NATIVE_READBACK_AND_RUNTIME_OWNERSHIP_BOUNDARY**;
native fixture NOT ADMITTED / NOT RUN. No actual restart or physical gap/x_c is
claimed. Final free disk ~30.259 GiB still fails nominal 22-GiB stream + 10-GiB
reserve before state overhead. Stock/previous private PW, dirty DFT status,
17 protected pins and historical BLOCKED goal remain unchanged.
[Handoff](qe75_streaming_2026-10-11/native_bridge/handoff_ledger.md).

The subsequent [bounded checkpoint/resource phase](qe75_streaming_2026-10-11/checkpoint_phase/README.md)
implements and tests a versioned no-copy storage-ownership transaction, read-only
Fortran storage adapter, strict 64-bit block/quota/reservation and resource guard
APIs. Fifteen small test methods plus 24 storage regressions pass; no native
QE/MPI runs. Read-only Q_GETINFO resolves quota status without elevated permissions.
A missed between-EXX-iterations export path is documented and closed by a compiled
private-source refusal patch. **At b1a4772 native state capture/import was unimplemented
and unqualified:** old ACE/occupations must be bound to the current native SCF save
at both stop points and after punch. **Decision STOP_NO_NATIVE_STATE_BRIDGE**;
the conditionally authorized small native comparison is NOT ADMITTED / NOT RUN.
No checkpoint library test is promoted to native restart success. Stock QE,
previous private PW binary, dirty DFT files, 17 pins and historical BLOCKED goal
remain unchanged. The original nominal 22-GiB store also fails the new 10-GiB disk
reserve; it is not allocated. [Handoff](qe75_streaming_2026-10-11/checkpoint_phase/handoff_ledger.md).

The [q-plane streaming package](qe75_streaming_2026-10-11/README.md) traces the
actual QE 7.5 producer/readers, ACE and EXX checkpoints. **PROVEN UNDER ASSUMPTIONS:**
lossless one-q-plane storage preserves the scoped CPU/NC/SOC exchange action and
unchanged 352-band ACE operations; nominal resident `exxbuff` capacity falls
22 to 2.75 GiB (87.5%). **CALCULATED:** 24 tiny Fortran storage/kernel/failure
cases, source-operation audits and actual exchange/SCF object compilation pass;
a private mixed-object PW candidate links but is **unexecuted / UNVALIDATED**.
Stock QE, dirty DFT files and all 17 source/supervisor pins remain unchanged.

**Decision:** retain the software candidate; native paired SCF **NOT QUALIFIED**.
The first candidate deliberately rejects EXX restart import/export, whose old
buffer semantics and disk duplication cannot be hidden. Full MPI/FFT equivalence,
peak memory, actual padding, disk admission and I/O wall time remain unverified.
No SCF/HSE/MPI run, queue, supervisor operation, physics reduction or hardware
purchase occurs. This independent engineering task does not resume or modify
the historical BLOCKED goal, admit Cd, or provide a physical gap/t_H/x_c. Stop
at the explicit software/runtime boundary; see the [decision](qe75_streaming_2026-10-11/decision.md).

## Current goal boundary audit

The goal service now returns **blocked**, after the same indispensable physical
input boundary recurred in three consecutive resumed goal turns, including the
approved host-attempt turn. The host/proof turn made progress; two later
read-only continuations supplied no new scientific information. The native
terminal result remains byte-identical, Cd data absent, and no live native
handle exists. No new native scope or independently qualified material packet
has arrived. This status update is administrative, not a new discovery or
completion claim. [Audit](native_matched_pilot_2026-10-11/goal_boundary_audit.json)
records the count and evidence. Stop repeated checks. Resume requires qualifying
independent data or fresh justified acquisition scope/resources; no automatic
retry, variant, new session, outreach or supervisor operation is created.
The dated progress record below is unchanged.

## Resumed goal and terminal approved host attempt

The user reactivated the original analytical-bandgap goal after `52e7915`.
External resource conditions changed: the [resumed preflight](native_matched_pilot_2026-10-11/resumed_preflight.json)
measured 29.27615 GiB available and passed the unchanged 27.524-GiB guard, with
no MPI/R07 driver. Existing approval permitted one six-rank matched-host SCF:
unchanged 90/360/120-Ry HSE+SOC, 352 bands, conv_thr=1e-10, 3600+1800-second cap,
unique directory and foreground owned-process monitoring. No old supervisor
or detached queue was created/changed.

The [terminal handoff](native_matched_pilot_2026-10-11/runtime_handoff.md) records
session 10143 COMPLETED at 20:01:04 UTC, after 732.39 seconds. Family RSS reached
26.72213 GiB above its retained 26.63966-GiB cap; minimum available RAM was
2.76587 GiB and minimum free disk was 30.48957 GiB. All owned descendants
terminated; no foreign MPI appeared. Adaptive inner SCF converged but EXX/final
1e-10-Ry SCF did not. Matched-host projector/irrep/1-meV gates NOT EVALUABLE;
**Cd NOT ADMITTED / NOT RUN**. [Result and decision](native_matched_pilot_2026-10-11/decision.md)
retain measured rejection. No retry, restart, variant, lowered input or queue.
The interrupted peak is not a full-SCF bound; successful runtime/peak errors
remain unknown. All 17 original source/supervisor pins verify.

An independent [reference-irrep bound/check](native_matched_pilot_2026-10-11/reference_irrep_bound.md)
uses earlier accepted primitive spinors only. Conditional nearby-projector
math and small-matrix counterexamples support their Gamma6/8 labels; calculated
arithmetic envelopes do not certify HSE eigenpair/material accuracy or admit
this failed host. The chemistry-bearing packet remains missing. No physical
gap, t_H or x_c is inferred. The original goal is active/unachieved; this
resumed turn made progress, not three repeated blocked turns. Records below
are historical and preserve their original outcomes.

## Approved staged native pilot — measured preflight NO-GO

The user explicitly approved one n2/k2/q2 16-atom f120 HSE+SOC matched host,
then one Cd member only if the host's native SCF/exchange/projector/irrep gates
pass, with at most six ranks and 3600+1800 seconds per member. The
[finite pilot intake](native_matched_pilot_2026-10-11/README.md) records a safe
NO-GO at 2026-10-11 19:22:26 UTC: measured available RAM 26.39040 GiB versus
27.524 GiB required by a declared 20% dry-estimate margin +2-GiB system-reserve
policy. The guard is conservative engineering judgment, not a measured peak
or proof of unavoidable OOM. Disk has 30.16499 GiB free; no active MPI family
or R07 numerical driver is found. Existing supervisors are FINISHED and untouched.

Prepared matching physical inputs, dry QE 7.5/six-rank and PP provenance verify.
Host SCF/exchange convergence and projector/irrep gates are **NOT RUN / NOT
EVALUABLE**; Cd is **NOT ADMITTED**. No new native directory, SCF, postprocessor,
restart, queue, variant, supervisor operation, lowered physical input or DFT
file modification occurs. Full-SCF peak RAM/disk, chemistry-bearing spectra
and physical x_c remain unknown. Adequate measured headroom or an independently
justified tighter peak/resource-containment plan is needed before any fresh
scoped attempt. This finite approval does not resume/change the historical goal.
The previous acquisition and analytical decisions below remain dated records.

## Continuous minimum-cost physical-input qualification

The [new qualification package](physical_input_qualification_2026-10-11/README.md)
and [persistent handoff](physical_input_qualification_2026-10-11/handoff_ledger.md)
complete three phases from `b19fc65`; P1/P2 checkpoints `904748f`/`29d3460`
were pushed before the next phase. **CALCULATED:** a read-only native audit
reproduces the accepted numerical HgTe Gamma reference comparison. Conditional
positive-measure bounds give mass floor >0.29017 and cutoff-induced windowed
ordering error <0.059 meV across the declared reference envelope. Exact native
eigenpair/metric residual and physical/model errors remain uncertified.

**FALSIFIED:** perfect binary projected spectra/sorted bands determine the
substitution response, including with the correct Gamma irrep multiplicities.
An exact periodization ambiguity also prevents one finite-cell packet from
identifying isolated impurity T without independent locality/image control.
Total leakage in a noncommuting primitive host frame is not substitution evidence.
These strengthen, and do not replace, the prior host, full/residual T, threshold,
continuum, SOC covariance, exchange-quadrature and physical-input negatives.

**Decision: STOP_ACQUISITION_BOUNDARY.** The smallest currently prepared
numerical chemistry test needs matched pure/substituted native spectra and
physical-host overlaps with tail/residual errors. One design (currently two
SCFs, no launch) is retained with a provisional 2-meV finite-cell observable
budget; it does not certify material accuracy or physical x_c. Further material
ordering needs independent interior contractions/state-law/errors, and dilute
prediction needs image/localization controls. No extra binary refinement or
synthetic repetition supplies them. No DFT/MPI/HSE, deck, queue, paid action,
outreach, session fork or supervisor operation occurred. Historical blocked goal
and other programs are unchanged. The earlier finite tasks below remain dated
records with their original rejections intact.

## Separate bounded centroid model-feasibility study

The [registered feasibility package](centroid_feasibility_2026-10-11/README.md)
was frozen in `5347d3c` before scanning 135 exact synthetic continuum rows:
three window half-widths, three finite analytical eta values, five interior
compositions and three endpoint/coherent-equivalent spectral redistributions.
**CALCULATED:** all numerical and >=0.05 window-mass gates pass; the minimum
lower mass is 0.0694186. Balanced signs are stable across all nine windows/eta
at each composition. The alternatives destroy the registered robust sign at
every composition, with individual enclosed signs at least 5.408 meV from zero.

**Decision: finite model NO-GO — STOP.** The study qualifies an exact causal
synthetic benchmark, not a physical HgCdTe TB/CPA model. Its negative result
quantifies the prior windowed odd-moment obstruction without changing any
rejection gate. The ranked missing physical input remains independently bounded
interior Gamma spectral-window contractions in a predetermined physical frame
and state; no material x_c or operational sign bracket is asserted. No new scan,
native calculation, acquisition, numerical queue or supervisor action follows.
The historical blocked goal is unchanged; no goal API or new session was used.

## Separate finite continuum-observable sprint

The [continuum package](continuum_spectral_2026-10-11/README.md) completes three
analytic/falsification cycles from clean `3316bfd`. **PROVEN UNDER ASSUMPTIONS:**
positive projected spectral measures give bounded test-function and windowed
centroid error estimates at fixed analytical eta without support-free domain D.
Isolated spectral-peak shifts additionally require separation and curvature;
operational crossing accuracy requires a lower composition modulus. Eta is not
an intrinsic linewidth. These are alternative observables, not sharp Gamma gap,
shared-pole or topology certificates.

**FALSIFIED:** causality or endpoint/coherent moments alone fix continuum-window
ordering, dominant peak selection, a sharp spectral limit, composition
transversality or bulk topology. The package preserves explicit counterexamples
and all previous reaction-kernel, full/residual T, strain, threshold, directional
SOC and continuum negative results.

**Decision: THEOREM PASS / MATERIAL NO-GO — STOP.** The single highest-information
missing input is independently certified interior Gamma6/Gamma8 windowed moments
in a predetermined physical frame and state family, with normalization, coverage
and residual errors. No current material object supplies them. Sharp physical
inversion remains OPEN; no physical x_c or new operational interval is asserted.
This separate finite task leaves the historical blocked goal unchanged and
creates no calculation, acquisition, outreach or supervision queue.

## Independent evidence-acquisition decision

The [2026-10-11 evidence memo](evidence_acquisition_2026-10-11/decision_memo.md)
and [primary-source matrix](evidence_acquisition_2026-10-11/source_evidence_matrix.md)
complete the separately authorized R07 investigation. Published alloy states,
unfolded weights, CPA/SCBA propagators and independent inversion observations
exist. The audited evidence does not qualify the common support-free kernel
domain, interior mass signs on that domain, all-pairs lower composition modulus
and uniform physical residual budget required for the inversion certificate.
No physical zero-temperature x_c or new material coefficient is asserted.

One [staged archival ordering pilot](evidence_acquisition_2026-10-11/next_pilot.md)
is proposed, with raw-data/metrology intake gates and explicit resource caps.
It is not run or queued. This evidence-acquisition task stops at the substantiated
missing-input conclusion. The old blocked analytical goal's status, controls and
usage budget are unchanged; no goal API was called. No existing process or
supervisor was interrupted or altered. Historical analytical/numerical decisions
and their goal wording below are preserved as dated records.

## Objective and scope

**Separately scoped Stage-0 intake, 2026-10-11:**
[archival feasibility](evidence_acquisition_2026-10-11/stage0_report.md) is
complete at NO-GO. No accessible calibrated polarization-resolved raw/independent
assay package qualifies the requested x approximately 0.150/0.185 pair.
Supporting-data availability on author request is not verified access to that
package. One precise archive request is retained unsent. Stage 1 is not admitted;
no new calculation, contact, queue or goal-status change follows. Domain D
remains unproved and physically doubtful for generically coupled inverted
continua; only a conditional operational finite-temperature sign bracket could
avoid it. No such new bracket or physical x_c is asserted.

Derive an interpretable, no-alloy-gap-fit equation for the signed
Gamma6-minus-Gamma8 gap and its inversion. The user explicitly authorized this
research continuation on 2026-10-10. Related endpoint infrastructure is tracked
in issue #4; this work does not alter R02's thermal or first-principles gates.
Temperature and empirical coefficient tuning are outside this tranche.

## Analytical-first directive and current decision

The user's 2026-10-11 directive supersedes the computational priority list below.
No additional DFT/MPI/HSE calculations or queues are launched. Existing detached
supervisors retain their established stopping rules and are not modified.
The previous numerical evidence is preserved as a dated snapshot, not upgraded
or reinterpreted by this analytical tranche.

The [analytical package](analytical_first_2026-10-11/README.md) establishes:

- **PROVEN UNDER ASSUMPTIONS:** finitely many endpoint derivatives, and even
  full endpoint impurity operators through any fixed cluster order, fail to
  identify unrestricted fixed local mixed interactions. An exact atomic
  Bernoulli model has unchanged binary/single-impurity data and changed Γ spectra.
- **PROVEN UNDER ASSUMPTIONS:** ensemble Td reduces the retained Γ6/Γ8 problem
  to two scalar causal functions, representable by positive augmented-space
  Feshbach measures. This is a functional reduction, not a two-constant theory.
- **PROVEN UNDER ASSUMPTIONS:** coherent-invisible directional Te/SOC response
  can enter the Γ8 mass self-energy. Gap-relevant covariance contracts to two
  functions at second order; full covariance reconstruction need not be required.
- **PROVEN:** equal static/dynamic moments and total spectral weight do not fix
  the full self-energy or an inversion root. An exact universal two-susceptibility
  prediction from these inputs is **FALSIFIED**; its conditional rational
  identities are preserved.
- **PROVEN UNDER ASSUMPTIONS:** spectral separation gives the nonperturbative
  linearization bound A h²/(d-|h|). A real mass root has conditional error
  [ε_m+(L_m/u)ε_s]/m. Thresholds can invalidate the needed separation/regularity.
- **PROVEN UNDER ASSUMPTIONS:** full-support, finite-range fixed-interaction
  Bernoulli spectral support is x-independent inside (0,1); this established
  phenomenon further separates support edges from measured Γ peaks.

**Previous decision (preserved):** continue threshold-aware analytical development and a quantified
common/mass uncertainty budget. The [ranked input plan](analytical_first_2026-10-11/inputs_and_decision.md)
specifies physical forward contractions as missing information; it creates no
calculation queue. Spectral-moment, weak-covariance and CPA closures each retain
explicit gates and falsification conditions. No physical E_g(x), x_c, material
validation, priority claim or manuscript promotion is established.

## Resumed threshold-aware analytical cycles and current decision

The [threshold package](threshold_causal_2026-10-11/README.md) completes three
distinct theory-first derivation/falsification cycles, without new native work.

- **PROVEN UNDER ASSUMPTIONS:** a specified positive fractional density admits
  an exact infrared split, uniform regular C¹/value bounds for subleading p>1,
  and a positive-envelope causal closure. A raw divergent threshold derivative
  is retained through an infrared function, not inserted as a finite constant.
- **PROVEN UNDER ASSUMPTIONS:** on a common support-free real energy segment,
  positive Γ measures give |Δmass|<=|Δcommon inverse|, including finite threshold
  endpoint limits. With branch residuals ε6,ε8, existence margins and a lower
  composition mass secant slope m>0, |δx_c|<=max(ε6,ε8)/m. No separate finite
  raw T' or mass-energy Lipschitz input is needed for this gap-side certificate.
- **FALSIFIED:** causality alone extends the contraction into a continuum;
  a bounded positive-density bath gives ratio 9. Positivity also cannot ensure
  composition transversality; a cubic mass tangency violates linear root bounds.
- **PROVEN / FALSIFICATION:** identical IR channels and regular C,A,S,d at the
  same threshold can still have different exact sharp-crossing roots. These
  inputs close a bounded approximation, not an exact universal gap law.

**Current decision:** stop physical prediction at the demonstrated missing-input
boundary. An independently qualified interior mass contraction on the common
trajectory, or a controlled microscopic bound fixing it, is indispensable;
support/observable and composition-modulus gates remain required. The package
ranks these inputs by information gained. No acquisition queue or expensive
calculation proposal is created. The persistent broad objective remains active
and unresolved; its completion is not inferred from synthetic checks.

All earlier negative results, numerical gate failures and detached numerical
ownership remain unchanged. A causal local energy-linear approximation does
not replace the exact global spectral normalization or centroid sum rules.

## Completed existing reference controls: current availability

The [completed-reference review](result_2026-10-11_completed_reference_review.md)
records newly available terminal outputs from the established supervisors.
**CALCULATED:** both HgTe k4/q4 controls pass their native SCF acceptance gate;
their 360/120-Ry Fock-cutoff signed Gamma gaps differ by 6.7014 micro-eV.
The pointwise six-state Gamma reaction-kernel comparison is 4.2058 micro-eV,
while the maximum sorted-band difference is 58.2800 micro-eV. Source hashes,
native termination, eigenvalue arrays and reported matrix norm are checked.

These are accepted numerical reference controls, not a physical impurity
potential, finite-q operator certificate or alloy mass uncertainty budget.
The source records explicitly retain those limitations and launch no full
impurity SCF. No DFT files or supervisors were modified. The current physical
prediction decision above is unchanged: the interior mass/domain/modulus
input is missing. No further numerical work is proposed or queued.

## Preserved numerical and analytical evidence from preceding tranches

The following numerical status statements describe their preceding tranches.
In particular, the formerly running HgTe reference and pending Fock comparison
have the completed status recorded above; their earlier failures remain
preserved and do not become accepted retrospectively.

**CALCULATED:** the SG15 CdTe accurate-empty control reduces the projected
time-reversal defect from 6.37827 eV to 2.95137 meV, while the signed Gamma
gap changes by only 0.8884 micro-eV. The unchanged 1-meV gate still fails;
a 1e-10-Ry seeded SCF refinement was interrupted at its wall limit without
an outer checkpoint and is rejected. The longer-budget HgTe k4/q2 host
stops cleanly without exchange convergence and splits its Gamma8-derived
quartet by 311.9218 meV. A source-checked q=G=0 exchange feedback component
is 297.6848 meV at q2; its blind q4 prediction is 6.711425 meV. A fresh
q4 control stops cleanly with native Gamma6/Gamma8 identity and a 1.052622
micro-eV quartet spread, but exchange error 2.315e-5 Ry fails the unchanged
criterion. An identical-physics continuation is running; no signed HgTe
gap is accepted. At X the two same-material
physical frames have minimum overlap singular value 0.109056 and a
same-label matrix difference of 6.30703 eV, invalid as an impurity operator.

**CALCULATED:** the matched fixed-ion 16-atom HgTe/Cd-in-HgTe inputs pass
native QE dry runs with estimated dynamical memory about 14.1 GB. No
self-consistent impurity result or dilute coefficient exists yet.

**CALCULATED:** native radial coefficient reconstruction matches Gamma and
X amplitudes to about 7e-13. The pinned QE 7.5 standalone interface uses
the numeric zona=1 as 1 inverse bohr; the earlier inverse-Angstrom metadata
description was inaccurate. The 26-band window captures only 0.0162204 of
the least-captured fixed physical trial direction at X. All 44 supplied
bands raise this to 0.469856. These are trial-norm fractions, not gap errors.
Identical ordered 208-spinor trial blocks are prepared for the paired cells.
A bounded, checkpoint-checked SCF runner is ready; DFT fast tests: 85 pass.

**CALCULATED:** the prepared Gamma-only n2/q1 supercell preserves the
primitive q2 exchange-feedback spacing. Matched n2/k2/q2 input decks are
prepared to match the finer k4/q4 reference-host spacings; their native
dry checks estimate 78.44/78.49 GiB, exceeding 31.34078 GiB physical RAM.
No full SCF is launched for those decks. Explicit matched Fock-cutoff
120-Ry native dry checks now estimate 21.27/21.32 GiB, within the sampled
total/available-memory budgets. Their seven-process dry peaks are about
169 MiB; these are not full-SCF peaks. The f120 approximation still
requires a matching accepted primitive reference and physical operator
comparison. It cannot modify an existing restart. The full 64-point,
44-band fixed-hydrogenic-trial
resolvent fails the sufficient inverse certificate (product 58.86078).
A different reference-UPF atomic s/p projector has a pointwise Gamma
omitted-window inverse bound 2.355045 meV, but a worst finite-q bound
484.115 meV. Reference-radial reconstruction and transport to the impurity
remain pending. The bound assumes exact eigenpairs; SCF/grid and residual
errors are separate. These are physical-projector controls, not a T-matrix.

**PROVEN:** fixed-physical-trial projected resolvents admit an omitted-band
error certificate from the unresolved spectral norm and distance to the
omitted spectrum. A separate energy-dependent effective inverse difference
must not be confused with the ambient physical impurity T-matrix.

**PROVEN:** actual host eigenstates provide an invariant physical projector
with exact R0. The impurity spectrum projected onto the same host spinors
then yields both full finite-volume T_P and the distinct P-irreducible
reaction kernel K_P. Full finite-box T can vanish on shell because of the
one exact host pole; reaction-kernel volume convergence or ordered volume
and energy limits are required. No physical endpoint value is computed yet.

**CALCULATED:** native same-host extraction in the actual six Gamma6/Gamma8
spinors gives reaction-kernel norm 2.5819e-15 eV. Physical reciprocal-vector
transport handles permutation and integer Bloch relabeling, with mismatched
NC spaces rejected. The 44-band prefix leaves unresolved projector norm
3.6086e-15. This passes a zero-substitution negative control and does not
upgrade material accuracy or calculate a physical impurity coefficient.

**PROVEN under static localized-substitution assumptions:** unresolved
fixed-host-edge projector norm is bounded by
sum_a ||V Phi_a||^2/(Lambda-E_a)^2. Its conditional O(1/Ncell) scaling
explains a possible window advantage over local atomic trials; actual
self-consistent localization and continuum/volume limits remain untested.

**PROVEN continuum qualification:** Herm(T[g^R]) generally differs from
T[Herm(g^R)]. A common complex mass zero characterizes a shared complex
pole; a real-energy ordering crossing can occur with unequal linewidths
without such a shared pole. The real-denominator, spectral-peak and complex
pole observables must be distinguished before using a mass-route x_c.
**CALCULATED:** the archived-model 21-row continuation audit verifies the
ordered reactance/retarded conversion to 5.64e-16 relative error, with a
real mid-gap CdTe equality control. It predicts no new physical coefficient
or inversion composition. See the [continuum gate](../../../docs/derivations/continuum_prescription_and_crossing.md).

**PROVEN under an isolated quadratic Gamma8 threshold and nonzero finite
forward amplitude:** the gap-side contribution to -T8' scales as
tau8^2 k8/sqrt(delta). **CALCULATED:** k8=0.5119895494464 eV^(-3/2) for
the published CdTe binary model, whose projected linear term vanishes.
Physical linear BIA and the inverted-HgTe continuum require separate checks;
this is not the physical total A. A finite A_slope cannot be equated to a
divergent unregularized endpoint derivative under those assumptions.

**PROVEN:** a composition-dependent volume path adds homogeneous-strain
terms to fixed-volume impurity endpoint slopes. These must be accounted
for before interpreting the boundary slope sum as dynamic susceptibility.

**PROVEN:** full host-referenced impurity T cannot also be added as a residual
to a binary chord. The correct residuals are t_H=tau_H-DeltaM and
t_C=tau_C+DeltaM. The handoff mass law is valid with these residuals.

**PROVEN under fixed tetrahedral covariance:** coherent Bernstein derivatives
determine order-averaged orbital vertices. Full local covariance adds a
positive directional term that those derivatives cannot determine. In the
restricted real spin-independent Te p-onsite sector, three coherent scalars
and four directional coefficients reconstruct all 16 environments from
three oriented representative matrices. Directional one-body Frobenius
scattering has the complementary filter (2/9)(16-|F(q)|^2). It is zero at
q=0 and maximal at scalar form-factor zeros; pair/triplet configurational
channels remain white. Exact stabilizer ranks and exhaustive covariance,
tomography and Fourier audits pass to 3.55e-15. No physical coefficient,
linewidth or susceptibility is inferred.

**PROVEN for the local time-reversal-even spinful p sector:** the oriented
closure has 14 endpoint-invisible coefficients, six coherent and eight
directional. For a chemical quadrupole a(T tensor I) plus a directional
SOC quadrupole alpha Q(T), the angular j=3/2 intra-sector amplitude is
a-2alpha while j=3/2-to-j=1/2 amplitude is a+alpha. Vanishing intra-sector
anisotropy does not imply vanishing inter-sector coupling. The spinful
proper/improper rotation and angular audit passes to 1.48e-15. These
are local angular projectors, not the complete Bloch branch T-matrix.

**PROVEN:** for an embedded lattice Green function, g'=-P G^2 P*, generally
not -g^2. At complex energy the positive scattering-cloud norm is
-Im(T)/eta, generally different from -Re(T').

**PROVEN:** a three-dimensional quadratic threshold with nonzero constant
scattering amplitude allows finite T but divergent T'. An exactly integrable
independent-impurity example has an x^(3/2) pole correction, so bounded Hermite
remainders and finite endpoint curvatures need a regularity check.

**CALCULATED:** Schindler's published sp3d5 binary model has been rebuilt.
Gamma signed gaps are -0.3015709 and +1.5981345 eV. X and L checks, SOC,
time reversal, finite-q uniform-vertex closure and embedded sum rules pass.
Its VCA inversion is x=0.1816612.

**CALCULATED:** for the explicit quarter-share Te partition and 0.4 eV source
offset, exact single-impurity resummation retains a large static discrepancy.
On a 30^3 grid at eta=50 meV, the corrected common-mode cubic root is
0.3321358; the branch-pole reciprocal reduction root is 0.3496545.
Using full T twice instead gives 0.1646405, a spurious apparent success.
These are finite-broadening diagnostic interpolants, not physical x_c predictions.

**CALCULATED:** at the CdTe Gamma8 threshold the real gap-side derivative
grows from 13.58 to 63.02 as the even grid increases from 6^3 to 30^3,
while T8 remains finite (1.276 to 1.305 eV). Finite-gap detuning regularizes
the trend. This disfavors extracting a constant dynamic A from the unqualified
endpoint derivative of the full lattice T.

**CALCULATED:** explicit n=8 and n=12 random supercells of the same frozen
linear-substitution Hamiltonian give Gamma spectral-peak separation -138 meV
at x approximately 0.18, and a peak crossing near x=0.30. The latter is not
a topological-invariant determination. Iteration, two seeds, box size and
eta=5–50 meV controls support the large discrepancy beyond the endpoint
interpolation. No empirical gap coefficient was used.

**PROVEN:** every configuration of this linear model has the VCA Gamma
spectral centroid exactly; its spectral maximum need not coincide with it.

**PROVEN within scalar CPA:** self-consistency changes the declared
independent-host x^(3/2) threshold correction to x^2. CPA DOS edge, Gamma
spectral peak and real-denominator root have different x^2 coefficients.
The conventional omitted-cluster indicator remains order one in the same
layer. This is not a controlled asymptotic statement about exact HgCdTe.

**HYPOTHESIS:** a physical, self-consistent substitution potential may still
reduce the static discrepancy through environmental response and charge transfer.
The current test supplies no evidence that resummation alone is sufficient.

**NOVELTY CANDIDATE:** none established in this tranche. The value is the
specific falsification and corrected HgCdTe prediction protocol. Generic Dyson,
optical-theorem, threshold and interpolation mathematics is established.

## Artifacts

- [Calculation and interpretation](result_2026-10-10.md)
- [Direct-alloy and self-consistency result](result_2026-10-10_self_consistency.md)
- [Hybrid host capability and core-approximation gate](result_2026-10-10_hybrid_gate.md)
- [Completed host comparison and projected-frame failure](result_2026-10-10_projected_host.md)
- [Empty-state repair and physical-frame negative control](result_2026-10-11.md)
- [Portable hybrid host record](../../../data/calculated/static_hse_binary_gate_20261010.json)
- [Reference and threshold derivation](../../../docs/derivations/impurity_reference_and_threshold.md)
- [Endpoint volume-path correction](../../../docs/derivations/endpoint_volume_path.md)
- [Conditional Gamma8 threshold kernel](../../../docs/derivations/gamma8_threshold_kernel.md)
- [Frozen Gamma8 kernel](../../../data/calculated/gamma8_quadratic_threshold_20261011.json)
- [Fixed-trial resolvent and spectral-window certificate](../../../docs/derivations/fixed_trial_resolvent.md)
- [Host-invariant reaction kernel and finite-volume pole limits](../../../docs/derivations/host_invariant_reaction_kernel.md)
- [Continuum prescription and broadened crossing qualification](../../../docs/derivations/continuum_prescription_and_crossing.md)
- [Archived-model continuum audit](../../../data/calculated/sp3d5_continuum_prescription.json)
- [Coarse HgTe quartet and exchange-component figure](figures/hgte_quartet_feedback.pdf)
- [Finer quartet and impurity memory control](figures/hgte_grid_control.pdf)
- [General oriented tetrahedral response](../../../docs/derivations/oriented_tetrahedral_response.md)
- [Oriented Te p-tensor tomography](../../../docs/derivations/te_p_tensor_tomography.md)
- [Frozen directional identity audit](../../../data/calculated/te_p_tensor_tomography_audit.json)
- [Relativistic onsite tensor closure](../../../docs/derivations/te_p_soc_tensor_tomography.md)
- [Frozen spinful audit](../../../data/calculated/te_p_soc_tensor_audit.json)
- [Self-consistent threshold and centroid derivation](../../../docs/derivations/self_consistent_threshold_and_centroid.md)
- [Frozen endpoint reductions](../../../data/calculated/sp3d5_endpoint_reductions.json)
- [Threshold convergence](../../../data/calculated/sp3d5_cdte_threshold.json)
- [Figure](figures/impurity_reference_and_threshold.pdf)
- [Direct-alloy and threshold figure](figures/self_consistent_threshold_and_alloy.pdf)

## Validation

Latest full repository suite: **1787 passed**, including eleven independent
analytical-first spectral-bound, hidden-interaction, causal finite-bath,
reference/unit-invariance, root-certificate and atomic-CPA checks. The frozen
[synthetic audit and verification](analytical_first_2026-10-11/verification.md)
establish mathematical behavior only. The preceding **1776 passed** included
three independent
binary-curvature, spin-three-halves angular and radial threshold checks.
Independent checks include a full finite-Hamiltonian inverse, numerical T
derivatives, positive off-spectrum norms, the causal optical theorem, direct
threshold quadrature and a bracketed concentration-pole solve.
New checks include random-cell dense inversion versus Lanczos, exact folded
binary spectra, spectral-centroid closure, the full scalar CPA equation,
implicit derivatives, threshold coefficients and the pair indicator limits.

## Historical computational agenda — superseded as current priorities

The following list is preserved to document the earlier numerical route and
its unresolved gates. It is not authorization to launch, restart or take over
any calculation under the current analytical-first directive.

1. Finish the live SG15 HgTe finer-exchange control
   `hgte_hse_sg15_k4_q4_e90_fullacc_c1e-10_t3600_g1800_restart_cee66000` in the companion DFT
   repository before another MPI family. Both coarse CdTe HSE hosts
   converged: signed gaps 1.7048135 eV (PseudoDojo) and 1.5753656 eV (SG15),
   with independently assigned Gamma sectors and verified grid expansion.
   Their 129.4479-meV difference is not attributable to NLCC alone.
   Accurate empty states reduce the 26-spinor matrix defect by over 2000
   times, to 2.95137 meV, still above the unchanged 1-meV gate. DFT commit
   6a1f9f8 contains the completed controls, physical-frame overlaps,
   native trial-unit/capture audit, prepared pair and bounded SCF runner.
   It also records the rejected coarse HgTe quartet and the blind q4
   component prediction; see the [exchange-grid protocol](/home/User/opencode_workspace/DFT/docs/r07_hgte_exchange_grid.md).
   The stricter CdTe refinement was
   killed at its wall limit without a checkpoint and is rejected. It
   needs a new longer-budget calculation. The completed finer-pair native
   default-cutoff memory estimates exceed RAM; f120 pair dry checks now
   fit. Compare matched primitive Fock-cutoff controls
   before any physical extraction. The first q4 terminal control restores
   native Gamma8 identity with a 1.05-micro-eV spread. Exchange convergence
   remains required before accepting that edge. Restoration supports a
   coarse-grid cause; the component's isolated
   gain is not the full SCF Jacobian. Rerun the Gamma assignments,
   projection and native-wavefunction checks after HgTe converges. In
   smeared HgTe, a fixed lowest-36-band slice is not an occupied projector.
   No scattering host is accepted yet. A clean time-limited continuation
   must retain `--accurate-empty` and `--scf-threshold 1e-10`.
   The preceding wrapper exited 143 while its ranks survived. Detached
   supervision preserved the missing native OS status and observed a
   clean stop with six freshly written checkpoints; that run remains
   unaccepted. Its terminal exchange error 2.8e-9 Ry exceeds the unchanged
   1e-10-Ry criterion. The dry probes completed and a fresh unchanged SCF
   now captures its native exit status with full MPI-family supervision.
   DFT commit 82628b7 preserves the terminal and resource records and the
   physical-frame Fock comparison. Its native same-operator CdTe control
   gives a 1.84e-15-eV residual, not an f120 accuracy result.
   A second acknowledged detached owner waits for the exact numerical
   queue, allows at most two unchanged f120 continuation chunks if needed,
   and compares only accepted references through native spinor overlaps
   and window certificates. Both owners enforce one MPI family. These
   bounded numerical sequences start no full impurity SCF; physical
   finite-q operator, isolated-cell and material accuracy remain pending.
2. Obtain or compute a common-gauge, self-consistent Cd-in-HgTe potential and
   the reciprocal Hg-in-CdTe potential with defensible binary electronic structure.
   First test the host-invariant edge-spinor resolvent/reaction-kernel route,
   retaining full nonlocal HSE through the impurity spectrum. Certify its
   window and cell-size/continuation limits before interpreting an endpoint
   shift; the finite-box on-shell full T is not a dilute amplitude.
   Test frozen reference-potential atomic radial projectors and enlarge
   the supplied spectral window; do not identify native host/impurity
   atomic labels as one physical basis.
   The present PBE endpoint artifacts are not adequate meV-level inputs.
3. Use the corrected full/residual conventions and define the HgTe common-mode
   continuation explicitly. Declare the lattice path: fixed-volume impurity
   derivatives omit the endpoint homogeneous-strain terms when a(x) varies.
   Freeze branch values and mass roots before validation.
4. Determine the threshold channel selection, the intended spectral observable,
   and self-consistent linewidth
   before treating T' as a finite constant-A input or invoking endpoint pair
   curvatures. CdTe mid-gap mass evaluation is a cleaner control than its band edge.
5. Test local-background dependence and irreducible environment clusters only
   after the physical one-impurity problem; add no empirical bowing coefficients.
   Preserve common-frame orbital tensors and bond-resolved hopping directions
   in that extraction before taking any coherent tetrahedral average.

The existing binary-derived vertex is terminated as a candidate physical
predictor at this level. It is retained as a reproducible diagnostic and code test.
No manuscript, material validation, or replacement of Hansen is claimed.

## QE7.5 M4 finite engineering checkpoint — 2026-10-12 01:40 UTC

**TESTED SMALL-SCALE:** [runtime admission package](qe75_streaming_2026-10-11/runtime_admission/decision.md)
passes a previously absent real foreground fake-family owner/lease/monitor gate.
65 focused methods verify actual tiny ext4 reservations, identity-safe process
cleanup, live all-fake-rank receipts, refusal after dual authority crash, exact
small paired decks and matched compiler/FFT/MPI backend pins. Native bridge
entry now requires live RPC rather than Boolean/file authorization. Stock QE,
prepared physical inputs, dirty DFT state and pre-existing supervisors/sessions
are unchanged. No native PW/HSE/MPI run occurred.

**BLOCKED:** native compiled rank registration and PROFILE/JOB binding,
EXX/energy/Gram/ACE and density/wave/old-ACE readback instruments, native
layout/output/common-wave certificates and complete global MPI inventory.
Unreadable pre-existing mappings remain UNKNOWN; no permission change.
Sampled resource predicates are not hard cgroup bounds. M5 remains NOT RUN;
the original 16-atom/352-band experiment still fails disk admission. The finite
phase stops here. Historical blocked goal, physical no-go results and missing
material-input boundary remain unchanged; no physical gap or `x_c` is inferred.

## QE7.5 M5-readiness finite checkpoint — 2026-10-12 03:08 UTC

**SOURCE-CONDITIONED / TESTED COMPONENTS:** [M5 readiness](qe75_streaming_2026-10-11/m5_readiness/decision.md)
adds typed separate PROFILE/JOB digests, compiled real-QE-world-rank registration
before state reads, deterministic first-ACE direct/energy/Gram/factor/xi/probe
instruments and signed-64 component extents. Both private candidates link with
matching backends; 78 focused methods pass. Pristine serial QE qeh5 versus h5py
reads 1,208,137 existing wave/ACE/density complex values bitwise. This is I/O and
software evidence, not material convergence, native action equality or restart.
ACE/direct inequality off the interpolation span is preserved as a synthetic
counterexample, not a novel material result.

**BLOCKED / NOT RUN:** production native packet/hook dispatch, real MPI collective
and both-stop SCF restoration behavior, common initial 48-band k2/Fock120Ry state,
actual FFT and complete output/RAM certificate, and full inventory (36 unreadable
mapping entries). The inspected 44-band k4/Fock180Ry save is not relabelled as the
fixture seed. Serial parallel-HDF5 dependency loading is distinguished from MPI
initialization; explicit initialization refusal stubs pass checks. No PW/HSE or
real MPI communicator was run, no DFT data/supervisor/session changed, and no
physical gap or `x_c` is inferred. The finite phase stops here; historical blocked
goal and all prior physical no-go results remain unchanged.

## QE7.5 finite M5 integration checkpoint — 2026-10-13 00:44 UTC

**TESTED SMALL-SCALE:** [production guardian transport](qe75_streaming_2026-10-11/m5_integration/decision.md)
now dispatches the unchanged compiled rank ABI with distinct JOB/PROFILE digests
and live registered-C-child receipts; native bridge requires native scope and
agreement with the registered executable ancestor. Only ABI_NO_MPI scope is
issued. Thirty-seven focused methods pass; peak integration summed RSS
97,746,944 bytes. Dirty DFT, 17 pins, stock/previous candidates and sessions are
unchanged; final workers/lease empty. Historical BLOCKED goal remains unchanged.

**STOP AT FIRST NATIVE GATE:** 32 live mappings remain unreadable, including
PID 1 and three same-UID processes; strict global inventory refuses at PID 1.
Owned-family control does not prove host-wide absence of foreign MPI. One missing
input is a permission-compatible authoritative foreign-family inventory/admission-domain
certificate. No permissions or unrelated processes changed. Native collective,
checkpoint/readback, common 48-band wave, actual FFT/output and action/energy/Gram
qualification remain unpassed. No QE/HSE/MPI run, 44-band seed reuse, original
352-band physics change, physical gap or `x_c` claim. Finite phase ends here;
see [reset handoff](qe75_streaming_2026-10-11/m5_integration/handoff_ledger.md).

## Autonomous independent QE software progression — 2026-10-13 01:36 UTC

User policy `339265a` permits independent safe engineering despite blocked native
inventory. Three checkpoints advance source/serial gates: `3342cc3` matched
48-band initial-state capture/protocol; `402b340` conservative FFT/component/
lifetime bounds; current checkpoint exact serial native-encoded reader and
collective decision checks. [Decision](qe75_streaming_2026-10-11/software_2026-10-13/decision.md).
Seventeen focused methods, 512 pristine FFT size cases, two actual QE capture
object compiles and ten no-MPI decision traces pass. Shared common input ID is
separate from differing mode-specific PROFILE/JOB identity; full packet bytes,
physical maps, NC Gram and density/potential/et/wg are checked. Irrelevant padded
memory is canonicalized in output only.

**SOURCE-CONDITIONED, not native:** selected small-fixture two-rank q payload
<=1.5 GiB and resident plane <=192 MiB; initial packet <=66,350,584 bytes. Full
native HDF5/output/generation/backend/RSS and true descriptors remain unknown.
Actual common waves, MPI progress, both native SCF stop/readback paths and
EXX/ACE values remain unobserved. Native launch HARD_BLOCKED; scientific goal
remains BLOCKED/unachieved. No original physics, stock/previous candidates,
dirty DFT, supervisors, sessions or goal changes; no physical gap/x_c claim.

The capture objects also link into two new private, unexecuted/unadmitted QE
candidates with matching retained FFT/MPI/runtime backend fingerprints. Old
stock and private candidates remain preserved; linking is not native validation.
