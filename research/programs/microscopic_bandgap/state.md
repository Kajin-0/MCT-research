# Program state: microscopic zero-temperature bandgap

**Portfolio contribution:** R07

## NEWER VCA Gamma audit — 2026-10-17

Read [postprocessing decision](vca_x0125_hse_2026-10-17/decision.md): saved-wave Γ full-density Theta 3.95518494693e-7, Td max 4.95143773706e-7 **both FAIL strict 1e-8**. Provisional 33–34 minus 35–38 energy -98.78796872 meV, half -49.39398436 meV; physical Γ6/Γ8 projection/characters not certified. This is not accepted m_VCA or physical xc; no second QE execution.

## CURRENT R07 terminal VCA checkpoint — 2026-10-17

The previous `LIVE`/`RUNNING` sections below are historical launch snapshots, **superseded** by the [terminal decision](vca_x0125_hse_2026-10-17/decision.md) and [native checkpoint](vca_x0125_hse_2026-10-17/completed_native_checkpoint.json). One zero-cost stock primitive Hg0.875Cd0.125Te HSE+SOC k4/q4 run has **converged numerically**: six exchange builds, dexx 3.5e-10 Ry, `EXX self-consistency reached`, `JOB DONE`, total -484.01592595 Ry, XML SCF true. Worker exit 0, zero restarts, 6,217,211,904 B observed kernel peak. Saved wavefunctions/ACE/density/XML remain in private DFT `.local`. **No Γ6/Γ8 projection or strict full-density Theta/Td 1e-8 certificate, accepted half-gap mass, physical random-alloy x_c, zero-smearing/material error claim.** Next: read-only physical postprocessing; no second HSE job or spending. Host primitive strict symmetry failure unchanged.

**State:** historical persistent goal BLOCKED, unchanged. Latest separately authorized zero-cost FR-VCA compatibility task: specific SG15 Hg/Cd pseudo/stock SOC reader GO;5dry checks+4endpoint PBE SCFs PASS, no mixed SCF/HSE. HSE launch not approved; no physical inversion result. Earlier128GiB cloud plan remains unpurchased; user current budget$0. Conventional8 k2/q2/152 execution remains NO-GO under12GiB (complete peak unqualified);k4/q2 requires56sources. Primitive k4 host remains conventional SCF PASS/conditional Γ ordering−.289586505eV, strict1e-8 density symmetry FAIL. Historical failures and closed PBE static diagnostic unchanged; physical x_c OPEN.

**Updated:** 2026-10-17 06:58 UTC

## LIVE authorized zero-cost VCA x=.125 HSE calculation

[Running decision](vca_x0125_hse_2026-10-17/decision.md). ONE stock primitive
2atom HSE+SOC k4/q4/e50/200/f200/44/FD.001 VCA .875Hg+.125Cd SCF launched;
unit r07-vca0125-hse-20261017.service, two pw ranks2012299/2012300, observer
2012292. Root DFT/.local/r07_vca_x0125_hse_20261017. 24h/12GiB/swap0/tasks12,
original observer+floors/output/science stops active. Ancillary dry PASS.
RUNNING ONLY; no convergence/mass/xc or symmetryPASS. 822pins/76originals/
dirtyDFT unchanged. No retry/second run. User current explicit authorization
supersedes earlier unapproved wording for THIS sole case;all old failures remain.

## Current operating policy: $0 additional spending

The current user constraint is **zero additional expenditure**, superseding the historical conditional cloud acquisition recommendation. [Current decision](zero_cost_policy_2026-10-17/decision.md). No paid compute, purchases, upgrades, or paid services; no automatic HSE job. The VCA endpoint pseudopotential/SOC-reader compatibility is GO, but mixed HSE execution is separate and remains unapproved. Preserve historical cloud feasibility reports and frozen failures unchanged.

## Specific fully relativistic Hg/Cd VCA compatibility: GO, no HSE admission

Read [decision](vca_fr_compatibility_2026-10-17/decision.md),
[native/resource verification](vca_fr_compatibility_2026-10-17/verification.json)
and [UPF audit](vca_fr_compatibility_2026-10-17/upf_audit.json).
Stock virtual_v2 supplied outputs keep24radial beta/l/j and exact weighted
nonlocalDblocks; noSOCdrop. Cd grid truncation12.45vs13.67bohr and inherited
HgCHIlabels are explicit; l/j/radial support validated, not globaloperator
identity. Five nstep0 SOC reader checks and four fresh Gamma-onlyPBE+SOC
endpointSCFs passed frozen0.1meV/density/charge gates. Max44leveldiffHg
4.03e-5meV,Cd2.08e-4meV; Cdmu-aligned2.75e-4meV. No gap/mass inferred.
Nine bounded two-rank systemd cases total29.73s,kernelpeak123.66MB,zero
swapallowance/tasks12;unitsunloaded. No mixedSCF,HSE,sourcebuild or spending.
All822pins/76originals/dirtyDFTunchanged;oldGateArefusal/staticPBEclosure
and1e-8HSEsymmetryFAIL unchanged. PrimitiveVCAx=.125HSE could test coherent
mean response only,not substitution/disorder/physicalxc;separateapproval and
state/resourcequalification required. Finite assignment COMPLETE/STOP.

## Compute acquisition plan only — no allocation/job approval

Read [one resource/cost decision](compute_acquisition_plan_2026-10-17/decision.md).
Conditional planning recommendation: on-demand n2-highmem-16/128GiB with500GiB
total balanced disk, prioritizing a fresh same-cell16atom host/Cd1 pair at
50/200/Fock200Ry,FD.001,K2/Q2,352spinors. As=2Ap gives exact primitiveK4
electronic folding and geometric exchange-transfer folding, not automatic
finite-grid HSE/state equivalence. Original90/360/Fock120/cold model remains
distinct and refused. Source8 atactualold64³ needs22GiB; newFFT/fullRAM/time
unknown.128GiB is plausible procurement,not capacity certificate. Official
price$1.048112/h;48totalVMh plus250–500GiBdisk≈$51.95–53.60,not runtime promise.
Require explicit spend/model/resource/checkpoint approval;no purchase,account
access,build or nativejob.822pins/76originals/dirtyDFT unchanged. Previous
12GiBNO-GO and strictsymmetryFAIL unchanged;physicalx_cOPEN. Finite phase STOP.

<!-- HSE8_152_Q8_ADMISSION_20261017_BEGIN -->
## Read-only eight-atom152/q8 admission: NO-GO under12GiB

Read [decision](hse8_152_q8_admission_2026-10-17/decision.md),
[exact source/grid/allocation audit](hse8_152_q8_admission_2026-10-17/audit.json)
and [independent verification](hse8_152_q8_admission_2026-10-17/verification.json).
No native job, build, source edit, service, PBE reopening or new infrastructure.

QE permits separate electronic and exchange grids, but allocates the distinct
k+q source union. Centered conventional k2/q2 has4irreps/8sources; k4/q2
has10irreps/56sources. At152bands/retained60³ these need8.405GB/58.835GB
nominal buffers. A single irreducible point forcesq1, including shiftedk2;
k3/q2 falls backq1. Source replay independently reproduces the accepted
primitive native k4 irreps/weights/64sources, without launching QE.

The primitive4³ folded16-point electronic rule is neither centered nor shifted
conventional2³ alone; q8 does not reproduce the full folded exchange rule.
The exact unrelaxed Cd-at-origin8atom motif retains24Td rotations, confirmed
by species-preserving geometry and old native XML; fcc translations fall4to1.
Do not assume lower point symmetry, nor equate geometry with a qualified density.

152bands is legal for144spinor electrons; dominant old Gamma labels fit,
but old nonstationary physical-probe weight above152 reaches1.60e-4.
Both cells have152atomic starting columns: changing176to152 changes the
stock atomic+random branch and ACE span, not merely memory. No coverage or
symmetry certificate for the new model follows from old unconverged data.

Source buffer plus two simultaneous EXX spinor batches totals10.506GB.
Extended named nominal payload is11.231GB,leaving1.654GBunassigned under12GiB;
actual rank padding/backend/cache high water lacks a complete upper bound.
This is pre-execution NO-GO,not proof of OOM or an authorized resource probe.
ONE best unadmitted model: fresh matched8atom centeredk2/q2/152,same50/200/
Fock200Ry,FD.001,HSE.25/.106,SG15FRNC,a6.46A and stock solver. It is not
primitivek4-equivalent. Need trustworthy exact-profile resident envelope
before any separate execution authorization; no new cap or HPC allocation invented.
Original1e-8 density gates and conditional2meV operator-error budget unchanged.
822pins/76oldfiles/dirtyDFT/oldhost decisions verified unchanged. STOP this study.
<!-- HSE8_152_Q8_ADMISSION_20261017_END -->

<!-- PRIMITIVE_K4_HSE_20261017_BEGIN -->
## COMPLETED k4/q4 control: conventional SCF PASS, strict symmetry FAIL

Read [final decision](primitive_k4_hse_2026-10-17/decision.md),
[full state/QR results](primitive_k4_hse_2026-10-17/final_qualification/state_result.json),
[independent verification](primitive_k4_hse_2026-10-17/final_qualification/verification.json)
and [derivation/limitations](primitive_k4_hse_2026-10-17/final_qualification/scientific_result.md).
The 01:37 RUNNING checkpoint/prefixes remain historical, byte-unchanged.

Native finished2026-10-17 03:24:51UTC, sixsourcebuilds, EXX reached/XMLtrue,
lastdexx2.3e-10Ry,lastinner3.2745e-10Ry,total−484.161000956768Ry,
Fock/2−8.96862706Ry. Same frozen50/200/Fock200Ry,FD.001,HSE.25/.106,
SG15FRNC,a6.46A,primitive36e/44spinor; onlyk/q4 relative tok2.
Actual8nativefibers,64qcoordinates,Gammaweight1/64. Weighted/rhocharge errors
~1.39e-11e,FDformula2.78e-14,entropy independently matches native.

Physical e90/f120 G-labelled frame and24actualTdcharacters support approximate
Gamma6bands33–34/Gamma8bands35–38; e50 lost reference tails retained.
Conditional signedordering−.289586504823eV, nominal Kanehalf−.144793252411eV;
quartetspread7.75e-9eV. NOT a rigorous gap/mass/material error interval.
All44states/88QRcolumns give Gamma fullThetaop3.61517e-7,F8.71074e-7;
Tdmax5.19645e-7. These FAIL unchanged1e-8 despite compressedTheta4.05e-11.
Independent direct Rayleigh/blockF/phase checks agree. Sector amplitude
leakages also>1e-8; no exact-irrep/full-H/eigenpair certificate.
OnlynativeTRIM1,3,7 have direct -k tests;fivegenericpartners absent;
actual little groups checked,no fabricated64export or full-BZThetaPASS.

OS6622.739s,kernelpeak6,225,952,768B,swap0,tasks7;all observed resource floors
held. Original invocation8dee58502fd048e4bf30a09bd9053a1f exited0,no restart,
no EXITrequest/resourcefailure. Both units unloaded;originalPIDs/cgroups gone.
No active science job or authorizedCd. Source/ELF/PP/822pins/76oldfiles,
DFTdirty/oldfailures/PBEclosure/main/other sessions unchanged.

This supports denser-quadrature suppression of the tested instability,
not unique causality/global stability. Olde90coldordering differs+.183609meV;
not a convergence/material error bar. Next missing physical input is sampling-
compatible stationary Cd-bearing HSE+matchedhost,not primitivehost spliced
into oldGamma-only chemistry. Eightatomk4/q4 stock buffer alone77.86GB>
12GiB; folding-equivalent16-source hypothetical19.46GB also exceeds it.
No new deck/streamer/infrastructure or job admitted. STOP solecontrol after
read-only qualification; historicalpersistentgoal remains unchanged.
<!-- PRIMITIVE_K4_HSE_20261017_END -->

<!-- PRIMITIVE_K2_HSE_20261017_BEGIN -->
## Primitive k2/q2 scientific control — rejected trajectory, not a gap

Read [decision](primitive_k2_hse_2026-10-17/decision.md),
[state arrays/trajectory](primitive_k2_hse_2026-10-17/state_result.json),
[verification](primitive_k2_hse_2026-10-17/verification.json).
ONE actual fresh stockQE7.5,2atom36e/44spinors,SG15FRNC,a6.46A,
HSE.25/.106,50/200/Fock200Ry,FD.001,primitive k2/q2/Gamma+L+X.
Actual24Td ops,weights1/8,4/8,3/8,8q sources,FFT40³. No solver/source change.
Outer error approached5.3e-9 then grew with split levels. Native normal EXIT
requested after sustained~315meV spread;16builds,14m16sOS,total−484.060104456Ry,
Fock/2−8.96881784Ry,dexx6.23e-6>1e-9,XMLfalse. Investigator EARLY stop,
not frozen plateau trigger,600s limit,6h exhaustion or no-symmetric-solution proof.

Saved density Theta op Gamma.90371172,L.01691385,X.01365988;Td max.997426.
Gamma8-character315.272meV,not an exact multiplet;occupied35/36 mainly Theta
map to empty38/37. Independent native35 scalar witness.816707. FD/charge pass
(~1.57e-11e) does not repair full density. All actual3TRIM G->−G−2k mappings
checked;8BZ fibers symmetry-reconstructed,NOT independent native full exports.
No full-H residual or stationary/mass/xc certificate. Strict1e-8 gates unchanged.

Read-only old8 translation audit:twirl distance<=9.23135e-6 leaves old Theta
lower expression.99997850. ConventionalGamma folds primitiveGamma+3X;newmesh
adds4L. This controls a cell-periodicity confounder,not unique k/ACE causality.
OnlyGamma has fractional occupations;coarse mesh does not resolve HH continuum.

Kernel peak1.043GB,RSS1.114GB(shared overcount),swap0,tasks7,host>=27.756GB,
disk>=49.354GB,own output37.303MB. Unit/cgroup/originalPIDs gone;observer
completed. Prelaunch bus query and offline48-vs24XML parser failures retained,
not native retries.822pins/76oldfiles/dirtyDFT/stock/priorFAILS unchanged.
NEXT separately scoped physical discriminant: samee50FDprimitive k4/q4,
not direct-HSE by fiat or new owner software;nominal5.767GBsource/4.69h16-build
Fock forecast are NOT complete admission/convergence bounds. No job queued.
Current assignment STOPPED; old persistent goal and all historical stops unchanged.
<!-- PRIMITIVE_K2_HSE_20261017_END -->

<!-- STOCK_HSE_STATIONARY_20261016_BEGIN -->
## Stock HSE8 long-run result — host scientific NO-GO; no Cd

Read [decision](stock_hse_stationary_2026-10-16/decision.md),
[native state](stock_hse_stationary_2026-10-16/host_state_result.json),
[resources](stock_hse_stationary_2026-10-16/resources.json) and
[verification](stock_hse_stationary_2026-10-16/verification.json).
New user authorization explicitly allowed approximately3hours; old600s was
a prior scope, not a universal user preference. One fresh stockQE7.5 ACE
host, two local ranks, no source/binary/runner changes, exact declared HSE
.25/.106,50/200/200Ry,176/144,FD.001,Gamma/q1,6.46A,SG15FRNC. Real run
20:21:51–23:16:39UTC,10488.530204s,79source builds. Native max_seconds10440
recognized10486.87s and saved all; OSexit0/JOBDONE but XMLSCFfalse and no EXX
self-consistency. Final E=-1936.3410548077159Ry,Fock/2=-35.83701457Ry,
dexx1.12e-6>1e-9Ry. No automatic continuation or restart qualification.

Charge+8.17e-11e independently from orbitals and saved rhoG; FD error6.41e-24.
These do not certify the nonlocal state: independent untruncated QR gives
Theta-density op.999996959745,F2.00301968; source compression/scalar checks
agree.24Td physical-frame lower witness max.99957689. Gamma8-character
spread661.214908meV,Gamma6-character5.385866meV; do not average/label gap.
No full-H residual certificate, stationary nonmagnetic state or physical mass.

Manager peak4,224,897,024B,sampledRSS4,290,023,424B(shared overcount),swap0,
sampled tasks7; host available>=25.269GB,disk>=49.399GB. New retained files
131.778MB. Standard kernel12GiB/tasks12/3h caps; no hardware purchase. Last
sampler failed KeyErrorControlGroup after group release, raw failure retained;
independent explicit manager readback and all recorded PID identities gone,
old cgroup absent, own unit unloaded. No full sampler PASS or retry claimed.

Raw root `DFT/.local/r07stock_20261016_202059` preserved; Git stores metadata,
small native stdout/XML and hashes, not large wave/ACE files.18build prefix
checkpoint cfbad7d immutable; this terminal result supersedes ACTIVE only.
822pins/76originals/dirtyDFT/stock/oldPBE failures and other sessions unchanged.
NEXT physical input remains a stationary symmetry-qualified HSE host before
Cd; stock direct exchange is an established control with unmeasured full-SCF
cost, not an automatically admitted retry. ACE versus Gamma-only instability
not selected. This finite assignment STOPPED; no pending job, no physicalxc.
<!-- STOCK_HSE_STATIONARY_20261016_END -->

<!-- HSE_PAIR_ADMISSION_20261016_BEGIN -->
## Stationary matched HSE8 admission — terminal NO-GO before execution

Read [decision](hse_pair_admission_2026-10-16/decision.md),
[read-only source/input audit](hse_pair_admission_2026-10-16/audit.json) and
[independent verification](hse_pair_admission_2026-10-16/verification.json).
From clean bd71dea: stock QE7.5, three private ELFs, modules/58 backends,
original SG15 PPs, archived inputs/XML/packet extents and fixed physical frame
were inspected without executing any solver or service. Exact old pair model
50/200/200Ry, Gamma/q1,176/144,FD.001Ry,HSE(.25,.106),6.46A is confirmed;
no independent stationary input potential exists for this pair.

Existing fixed owner pins the two-build private executable and used roots;
native code returns with conv_elec=false after second ACE. Ordinary DFT runner
does not supply required kernel/resource/output contract. Stock ace=false is
an established direct-exchange alternative, NOT full-SCF admitted. Known old
two-build members cost410.333/409.315s, kernel4.549/4.542GB; eight-build host
1628.053s exceeds current600s, remains unconverged/symmetry rejected. These
observations neither bound a direct full solve nor prove it impossible.
Native EXX subtotal1,216,512,000B; selected direct payload1,594,965,696B is
NOT complete peak. Host available29.915GB/disk49.537GB passed floors only.

No fresh job/source/runner, no Cd release, no historical retry or retropass.
822pins/76history and dirtyDFT/stock/PBE-final refusal remain unchanged.
Minimum missing input: independently qualified stationary matched HSE state
packet, rebuilt full H[D]/FD charge+entropy/eigenpair/symmetry and convergence
logs, from an already-supported bounded native execution; qualified restart
would be required for continuations if600s insufficient. Conventional numerical
evidence is useful; no universal SCF proof is demanded. No hardware purchase,
new infrastructure phase, projected activation->mass or physical xc claim.
Current finite assignment STOPPED at this input/operational boundary.
<!-- HSE_PAIR_ADMISSION_20261016_END -->

<!-- PBE_FINAL_ADMISSION_BEGIN -->
## FINAL PBE diagnostic TERMINATED; stationary HSE chemistry priority — 2026-10-16 19:27 UTC

Read `pbe_final_admission_2026-10-16/{decision.md,science_transition.md,
result_fs.json,predicates_fs.jsonl,verification.json}`. This finite assignment
is COMPLETE; no further PBE infrastructure phase, singleton retry, or12/24
static acquisition is scheduled. This supersedes prior proposals to continue
that diagnostic; their original evidence and status remain untouched below.

NEW named/durable owner had14offline passes. ONE fresh FS service reached
all pre-nonce identity/kernel/manager gates then actual LandlockABI7 negative
checks/FD-capability tests completed with exit0. Overall sequence REFUSED at
BOUNDED_SAMPLE: holder ru_maxrss563,339,264B exceeded512MiB536,870,912B;
this peak check was missing from preflight, not a proven instantaneousRSS
measurement. No guard change/retry/retropass; prior anonymous cause unproved.
SingletonWITHHELD, zero QE/material/H/SCF jobs. Worker kernel peak1,835,008B,
swap0/native.122243s; holder elapsed.210653s. Actual owned pidfd exit/cgroup
absence and both fresh unit names not-found checked. Result/journal prefix
and post-Unref complete hashes separately preserved; no hidden hash repair.

PBE diagnostic TERMINATE; scientific executionNO-GO. New driver remains hard-
gated/unexecuted,2meV absent.822protected pins/76historical files/dirtyDFT/
stock unchanged. No physical x_c, N2, linewidth or new material result.

NEXT scientific deliverable is stationary matched HSE+SOC chemical STATES and
signed periodic Γ mass with residual/symmetry/error certificates, then a second
composition and conditional alloy adapter. Original primitive numerical HSE
SCFs/frames remain useful; old8atom/176ACE/D0 defects cannot be bypassed.
Existing stock ace=false direct-exchange path is a scientific control candidate,
NOT resource/convergence admitted. No source/owner development campaign or job
authorized here. If a qualified bounded calculation is unavailable, missing
independent stationary material input is the boundary. No endpoint/gap fitting.
Historical persistent goal/registry/main/other sessions remain unchanged. STOP.
<!-- PBE_FINAL_ADMISSION_END -->

<!-- DENSITY_DRIVER_BUILD_BEGIN -->
## Density-only driver implemented; runtime qualification refused — 2026-10-16 18:25 UTC

Read `pbe_density_driver_2026-10-16/{decision.md,packet_and_execution_boundary.md,
build_result.json,runtime_fs_probe.json,verification.json}`. From75b0e33,
new private standalone QE7.5 read_file_new(needwf=false)/set_vrs/k/beta/becp12/
h_psi main compiled+linked first attempt against unchanged stock archive.
No evc352/wfc loading/SCF call on new path; metadata352/288 preserved. New
one-rank R07D1 G-labelled input/packet+metric/Theta reader;9offline tests.
C hard gate EPERM before mp_startup; QE-linked ELF NEVER EXECUTED.

ONE fresh NON_SCIENCE FS service reached READY then pre-nonce owner admission
AssertionError; no traceback/named predicate retained, so exact failed check
cannot be recovered. Empty go proves no Landlock/seccomp/negative tests/MPI
ran. Absorbing REFUSAL preserved, no retry; singleton WITHHELD. Owned pidfd
exit and empty/absent original cgroup checked. Manager startup peak1,835,008B,
owner elapsed.146s only, NOT QE resources. Manager Resultsuccess/wait0 after
owner TERM is not native success (ExecMainCode2/status15). No old GateA PASS.

BUILD GO only; confinement/singleton/native-equivalence/full-resource/2meV
remain UNQUALIFIED; material EXECUTION NO-GO. Next separate NON_SCIENCE scope
must first retain named pre-nonce identity/kernel/manager/member facts, then
qualify actual write confinement and singleton without helper/network. No
scientific job/release in this phase, no static numeric response or xc.
Original protected pins/dirtyDFT/stock/failed evidence verified unchanged.
Registry and blocked goal unchanged; STOP at separate authorization boundary.
All previous handoff/state history remains below.
<!-- DENSITY_DRIVER_BUILD_END -->

## Density-only static PBE path — conditional design GO, execution NO-GO

[Decision](pbe_density_only_feasibility_2026-10-16/decision.md),
[exact native path/observable](pbe_density_only_feasibility_2026-10-16/preferred_path.md),
[prospective acceptance/policy](pbe_density_only_feasibility_2026-10-16/acceptance_and_policy.md),
[source/input audit](pbe_density_only_feasibility_2026-10-16/audit_result.json),
[independent read-only checks](pbe_density_only_feasibility_2026-10-16/independent_results.json).
From9a7dafa, no build/native action/MPI/service/SCF/protected edit. Select ONE
NEW standalone postprocessor: read_file_new with needwf initiallyfalse,
explicit set_vrs, separate k-index/vkb/g2kin/becp12 allocation and unchanged
h_psi components. post_xml_init already rebuilds density/PBE/ionic/FR-NC;
no evc352/wfcinit/openfil/read_collected_wfc needed. Keep nbnd352 XML metadata,
nelec288 and original6+6Theta probes; do not lower bands or redefine frame.
Actual SG15 headers have no NLCC/US/PAW; this does not generalize to HSE.

Both accepted scalar densities/physicalG checked: charge error<=1.004e-10e,
independent direct-Fourier/FFT<=5.60e-16. Original24/4 groups and Theta leak
unchanged. Remove243.5MB/member saved-wave input and243.25MB evc allocation;
selected439.69MB buffers are NOT full peak/time/output bounds. No numerical
2meV certificate or new static A/B obtained. PBE saved-density H is not SCF.

One world rank is source-supported, but installed MPI singleton/no-helper
behavior UNPROVED. Landlock VERSION ABI7 observed without applying rules;
actual write/network confinement and complete owner/backend envelope UNPROVED.
Execution NO-GO; no frozen ELF mutation, profile/nonce or launch authority.
stop_run creates/deletes files; new read-only shutdown must avoid it. Existing
two-rank reader/ELF cannot be implicitly used as a one-rank control. No generic
owner redesign/fallback, Gate A retropass, physical mass/gap/N2/x_c or registry
promotion. Stop at separate reviewed implementation/admission boundary.

## Gate A actual lifecycle attempt — NO-GO, STOP

[Decision](pbe_static_lifecycle_2026-10-16/decision.md),
[preregistration](pbe_static_lifecycle_2026-10-16/preregistration.md),
[actual immutable refusal/cleanup](pbe_static_lifecycle_2026-10-16/evidence/RESULT.json),
[verification](pbe_static_lifecycle_2026-10-16/verification.json).
From9f59814, NEW isolated R07L/scope1601 NON_SCIENCE C MPI harness and
production-derived owner.run compiled/imported/frozen. Actual two-rank command
entered a real bounded systemd user unit. `/proc/1978386/fd/9` disappeared during
launcher FD accounting; strict incomplete-final-pair refusal after0.202116s.
No authenticated begin/final, packet or MPI collective completion was obtained.
No task-close/exit cause is inferred from ENOENT. One attempt, zero retries;
conditional missing-final test withheld. No QE/PW/SCF or protected DFT writes.

Actual kernel12GiB/swap0/tasks12/600s observed; manager final peak2,789,376B,
holder RSS24,408,064B sampled. Cleanup checked known actor pidfds, wait1,
same failed manager/invocation and empty/absent cgroup. No success was issued.
The empty-rank cleanup Boolean is vacuous, NOT rank-exit evidence; failure log
is empty and no MPI diagnostic is invented. Original RESULT stays REFUSED.
Old126profile/14raw pins, stock/dirtyDFT/ledger unchanged. No host-wide exclusion
or private-network proof, Gate B/2meV release or scientific resource bound.
STOP at bootstrap FD-lifetime/accounting boundary; no automatic next service,
resource probe or paired24actions. Registry/scientific status unchanged.

## PBE native-completion implementation — source/component PASS, native BLOCKED

[Decision](pbe_static_completion_2026-10-16/decision.md),
[source/test acceptance](pbe_static_completion_2026-10-16/acceptance.md),
[build](pbe_static_completion_2026-10-16/build_result.json),
[real non-MPI components](pbe_static_completion_2026-10-16/component_results.json),
[verification](pbe_static_completion_2026-10-16/verification.json).
From37f48db, NEW private MCT-only compile: actual QE world begin before init,
checked packet close/barrier then typed live native final, normalized collective
and barrier before exit. Stock archive physics objects/source remain unchanged.
The production external-holder dispatcher/reader/strict account now connect
to that ABI. Original6+6Theta per member, PBE/FD/cell/PP/frame unchanged.

Compiled C NON-MPI peers pass actual live identity/receipt/packet gating;
live EACCES remains absorbing through later exit. Premature/foreign/lost rank,
failed readback, corrupt import, descriptor reuse, lost log, output burst and
modeled manager/cgroup failures refuse. Native reader rejects the synthetic
fixture; positive reader/terminal snapshots were explicitly mocked. No new
native action, MPI/SCF/member, service, protected DFT write or HSE work.

Full owner.run/systemd/MPI lifecycle and complete initialization/backend plus
outside-reader RAM/time/output envelopes are NOT qualified. No source-complete
resource or2meV numerical certificate/frozen execution release exists; loader
and CLI refuse. Stop here. A minimal future one-member live resource query
would require separately reviewed owner/lifecycle/resource authorization,
not automatic shared release or old rejected-output reuse. Old refusals,
native data, protected dirty DFT/stock and registry status remain unchanged.

## PBE-first static environment admission — STOP before native

[Decision](pbe_static_admission_2026-10-16/decision.md),
[physical contract](pbe_static_admission_2026-10-16/observable_contract.md),
[owner/import acceptance](pbe_static_admission_2026-10-16/owner_import_acceptance.md),
[input audit](pbe_static_admission_2026-10-16/input_audit.json),
[verification](pbe_static_admission_2026-10-16/verification.json).
Fromfdc1b02, no new native/operator/SCF/build/service or protected DFT write.
All126 frozen profile pins and14 refused raw pins match. Accepted original
16atom x=.25 SCF states and exact host50Ry frame survive; scalar densities pass
actual24/4 chemical groups, not a shared host quartet. The full nonlocal FD
density and saved full-H eigenpair residuals are not newly certified.

Original-frame Theta leakage1.65485e-6 has6singular directions above1e-8:
12primary physical actions need12additional Theta controls across the pair.
Static A=F†HF, B=QHF and scalar-shift-invariant trace contrast are distinct
from old own-EF finite-eta data; <=2meV numerical sign budget is prospective.
N2, QHQ, ensemble disorder, physical gap/x_c and material error remain unknown.

Isolated importer and real non-MPI kernel pidfd/live-EACCES component tests
pass; injected terminal manager/CG cases are not production authority. Pinned
PBE native final hook and owner retirement caller are absent. Complete source
RAM/runtime/output envelope is also unqualified; old~1GiB/4s is not a bound.
STOP at that exact integration/admission boundary; no future pair launched.
Old live-rank FD refusal/import defect and HSE state gate remain immutable;
registry status unchanged. Any future acquisition needs a new private scoped
source/profile/ELF and separately authorized BOTH-member execution.

## Nonmagnetic electronic-state update qualification — STOP before native

[Decision](state_update_2026-10-16/decision.md),
[state-update theory](state_update_2026-10-16/theory.md),
[ONE next input](state_update_2026-10-16/next_input.md),
[retained-data trial](state_update_2026-10-16/result.json),
[independent checks](state_update_2026-10-16/independent_results.json).
Frombe13479: the known FD304 density is now a reproducible full-G trial source,
with144e,Theta density upper6.98e-12/all96host operations<7.77e-12 and independent
four-component FFT/actual rank-G packet roundtrip. No twirl or level averaging.
Species geometry independently gives96host versus24Cd space operations;
this Cd site keeps Td but loses host fcc translations. These OFFLINE inputs do
not qualify a new native state. Full-H commutator still obstructs stationarity;
new conditional uniform-H correction lower709.1054meV is not chemical error.

Existing qualified source enforces the old weight template and exits before any occupied
solve. New D1 cannot pass that reader; removing its guard alone is insufficient.
One next protocol requires full-space direct occupied solve/tail/FD/symmetry,
then same-D Fock/local-XC rebuild and full-H residual. New native implementation,
total occupied-solver12GiB/600s resource and owner admission are absent. No native
run/build/Cd/DFT write. Prospective2meV chemical numerical budget is defined,
not achieved; unknown feedback stability remains. Old finite chemistry and all
refusals unchanged; registry remains blocked/unverified. Stop this bounded phase.

## Frozen-response time-reversal decomposition COMPLETE — 2026-10-16

[Decision](theta_response_2026-10-16/decision.md),
[theory](theta_response_2026-10-16/theory.md),
[conditional source norm certificate](theta_response_2026-10-16/source_norm_certificate.md),
[native-data results](theta_response_2026-10-16/result.json),
[all member responses](theta_response_2026-10-16/response_table.csv),
[handoff](theta_response_2026-10-16/handoff_ledger.md).
From4cfc16b, no new native/source/build/DFT write. Original reference Theta
closure1.2864e-7 fails1e-8, so exact six-column reconstruction is REFUSED.
Hermitian cross-block information plus a reviewed frozen-QE norm bound still
gives conditional intervals: updated chemical even Q norm95.4618–95.5739meV,
odd.2198–.3320meV, even minimum singular>91.5138meV. Updated odd trace is
bounded within about1.12e-8meV of zero in this defined frame, not asserted
identically zero. These bounds concern closure/completion, not material error;
original multiplier packet is absent and source assumptions are explicit.

Full finite-rank source density defects: host relaxed.001428208op/.004040264F;
preliminary Cd5.99595e-7op, despite its tiny old compressed lower witness.
All4sources fail strict1e-8 TR state qualification. Independent actual column/
trace, gauge and scalar-density checks pass. The large remote action survives
even projection but even-state/SCF feedback remains unbounded: no repaired
H[D_even], FD solution, cubic quartet, gap or physicalx_c. Nonlinear projected
Hessian/inverse FD-Jacobian and qualified matched full-H/state input remain
missing. No extra ThetaR job is justified just to narrow these small intervals.
STOP this distinct phase; previous finite PASS/FAIL/source/owner gates remain.
Registry status unchanged; no new optical search or native admission.

## Science-first screening feasibility COMPLETE — 2026-10-16

[Decision](screening_feasibility_2026-10-16/decision.md),
[theory](screening_feasibility_2026-10-16/theory.md),
[minimum input](screening_feasibility_2026-10-16/minimum_input.md),
[actual retained-data contractions](screening_feasibility_2026-10-16/retained_result.json),
[independent checks](screening_feasibility_2026-10-16/independent_results.json),
[handoff](screening_feasibility_2026-10-16/handoff_ledger.md).
From5dc77a9, zero native/source/build/DFT writes. Reused32 originally pinned
real matched HSE packets. Updated chemical activation trace+39.811504meV
retains positive compressed-sector Rayleigh differences39.591459–40.032986meV,
but its out-of-six-state action norm95.541080meV (smallest singular91.550099meV)
falsifies a closed six-state activation operator. It is not a gap/self-energy
error. Actual host source-density Theta lower witnesses3.27666e-7/0.001395756895
and Cd second4.01839e-7 rule out strict1e-8 nonmagnetic continuation. Independent
direct scalar and QR checks agree; old finite-acquisition PASS is unchanged.

Neither one more unchanged A outer build nor B original16atom is admitted.
The B stream stores22GiB despite2.75GiB resident plane, already8GiB over14GiB
output cap. Disk availability does not waive the contract; full352SCF/restart
and total resource bounds remain unqualified. A scalar geometric-tail sign
certificate would require an independently uniform q<.90103694 for chemistry
or q<.51249540 separately, not an observed ratio. Sharp projected remainder
sign radius19.905752meV is conditional, not an attained error bound. Minimum
next physical input is qualified matched same-D full-H six-probe screened
remainder/state evidence. Existing e90 cold frames transfer references, not
e50 FD self-consistency. STOP at this boundary; no native run, optical repeat,
empirical input, convergence or physical x_c. All historical gates unchanged.

## Original stationary-reference reuse audit COMPLETE — 2026-10-16

[Decision](stationary_reference_audit_2026-10-16/decision.md),
[qualification/resources](stationary_reference_audit_2026-10-16/qualification_and_resources.md),
[theory/contract](stationary_reference_audit_2026-10-16/theory_and_contract.md),
[minimum input](stationary_reference_audit_2026-10-16/minimum_input.md),
[native audit](stationary_reference_audit_2026-10-16/native_audit.json),
[handoff](stationary_reference_audit_2026-10-16/handoff_ledger.md).
From clean9a83424, distinct read-only audit of ORIGINAL primitive e90 k4/q4
f360/f120 SCF saves, beyond P1's Gamma cross-cutoff inventory. Original SCF
XML matches prior expansion-parent hashes; full wave/occupation/ACE files
survive and supply useful numerical host/reference frames, avoiding more D0
blocks. Exported open_grid metadata is not the SCF convergence authority.

Native charge36e and physical Gamma irrep spans pass numerical checks, but
cold-smearing Gamma8 occupation spreads8.55e-7/1.06e-6 yield cubic density
witnesses8.54e-7/1.04e-6. Saved-ACE six-probe cubic defects2.42e-8/9.15e-8
and unknown DIRECT/full-H residuals do not certify strict1e-8 FD stationarity.
The accepted native SCF flags are unchanged. FD reinterpretation of stored
spectra shifts mu−1.895584meV only algebraically; no H[D_new] is acquired.
e90-to-e50 physical-frame tails are measured, not renormalized away. Original/
export coefficients differ near roundoff, so no byte-replay PASS or old-failure
reclassification. New source hashes do not invent historical kernel fingerprints.

Source-based nominal EXX buffers: primitive f1202.75GiB, f36013.21GiB,
original16atom f12022GiB. Stock matched chemistry under12GiB is NO-GO;
H304's5.56GB is not a substitute bound. Both original open_grid exports
used54³ FFT; regenerating f120 export would also require a nominal13.21GiB
buffer, so use existing exports read-only. Primitive f120 is a candidate for
future same-state residual qualification only after a complete two-rank
source/state/resource gate; no new native run is admitted. Independently
self-consistent Cd-screened density/operator in that host frame remains
indispensable, followed by dilute/alloy/material/observable control. STOP at
that actual information/resource boundary. No native/optical/synthetic rerun,
empirical coefficient, material mass or physical x_c in this phase.

## Public one-specimen optical intake COMPLETE — 2026-10-15

[Decision](public_optical_intake_2026-10-15/decision.md),
[ranked availability](public_optical_intake_2026-10-15/availability_matrix.md),
[source chronology](public_optical_intake_2026-10-15/sources.json),
[unsent request](public_optical_intake_2026-10-15/draft_request.md),
[test/intake gate](public_optical_intake_2026-10-15/three_field_test.md).
From clean 4affbd8, fresh publisher-linked six-page Teppe/Orlita supplements and
eight targeted public queries did not locate a complete independently calibrated
raw three-field HH-to-electron package with polarization and independent assay.
Teppe S5 is plotted 77 K data; on-request availability is not public raw access.
HAL/API file inventories were inaccessible and remain UNKNOWN, not empty.
Local extracted fits/annotations/calculated screens are not raw spectra.

STOP at `NO_GO_PUBLIC_RAW_CALIBRATION_ASSAY_NOT_LOCATED`; no claim that records
never existed. One practical next route is the UNSENT draft to Teppe's printed
correspondence address for existing low-T sample-A records, permission and matched
metrology. No contact, new measurement, spectrum analysis, synthetic rerun or
native job. A qualified package could test the conditional optical adapter via
held-out B3; it cannot alone identify microscopic mass/topology or physical x_c.
Original two-specimen Stage0 NO-GO, old draft, AGENTS, native failures and all
conditional physics remain unchanged. No novelty or new material coefficient.

## Competing inversion routes COMPLETE — 2026-10-15 21:34 UTC

[Decision](competing_inversion_routes_2026-10-15/decision.md),
[comparison](competing_inversion_routes_2026-10-15/comparison_and_phase_boundary.md),
[ONE input](competing_inversion_routes_2026-10-15/one_next_input.md),
[handoff](competing_inversion_routes_2026-10-15/handoff_ledger.md).
Three analytical-only cycles fromc80147f complete, milestones4462514/c2ba548
published. Ensemble Td does not forbid a fixed Bernoulli pair Gamma6-HH Born
channel; actual local/finite-q covariance and angular/dispersion gates matter.
Exact criticalsqrt model loses atom for anyc>0 but is arbitrarily pole-like at
finiteeta, with O(c^2) singularscale; not a material exponent/linewidth.

Alternative no-atom signed optical Kane witnessQ/(2D), explicit error and
held-out thirdfield test accepted under model hypotheses. Actual circular
current confirms positive opticalbias from zero-mean symmetricmass mixture.
Canonical[H,.] cancels globalCI disorder; a bounded Liouvillian/source-contracted
closure is possible without atoms, but oneparticleG alone cannot predict optics.
Global phaseequivalence needs separate hypotheses; no physicalxc/M activation.

ONE recommended next input is a calibrated three-field single-specimen HH
transitionresponse, to test the observable adapter rather than fit microscopic
coefficients. Earlier IR input is conditionally deprioritized, not disproven.
Accepted PBE/H304 lack both physicalIR and finiteB/source/vertex data; Stage0
raw/metrology NO-GO remains. No new archive outreach, data fit or nativejob.
R02/R05 status, stationarity, N3 and every priornegative/failure retained.
Focused model/proof/source/oldpin/stock/DFTdiff checksPASS. Stop at material
input boundary; specific synthesis noveltyUNVERIFIED against primary papers.

## Competing inversion routes: cycle2 — 2026-10-15 21:19 UTC

[RouteB](competing_inversion_routes_2026-10-15/route_B_optical_mass.md),
[closure](competing_inversion_routes_2026-10-15/transition_disorder_closure.md),
[literature](competing_inversion_routes_2026-10-15/literature.md).
Conditional two-field Kane signed-mass statistic and third-field falsification
with explicit error budget accepted; no atom needed in canonical global-scalar
disorder model. Actual small Landau/circular-current checksPASS. Symmetric
zero-mean mass mixtures produce positive optical bias even with actual current
weights: no general equality to mean/mass-zero/topology. An identical-oneparticleG
counterexample has different optics; a bounded Liouvillian closure depends on
commutator-active disorder and source/occupation errors. This is a conditional
forward theory, not a material activation or empirical fit. Continue ONEinput
ranking/retained-data audit; old H304 and all native refusals unchanged. Nojobs.

## Competing inversion routes: cycle1 — 2026-10-15 21:09 UTC

New analytical-only assignment fromc80147f;
[scope](competing_inversion_routes_2026-10-15/scope.md),
[routeA](competing_inversion_routes_2026-10-15/route_A_symmetry_and_IR.md),
[ledger](competing_inversion_routes_2026-10-15/cycles_and_decisions.md).
Exact fixed-local Bernoulli pair counterexample: zero coherent Gamma6/8mixing
but nonzero HH Born covariance atq0. Ensemble Td is not individual-site Td;
all24group/TR, R02projectors and covariance checksPASS. Uniform curvature and
nonzero angular weight are necessary for the quoted exponent formula; flat,
nonanalytic and dark-channel cases separated. No material coupling/exponent.
Continue competing no-atom Kane/optical criterion and selection of ONE input;
do not automatically request more HSE or the earlier IR certificate. No native
job, old-goal change or reinterpretation of any historical failure.

## Analytical physical-inversion assignment COMPLETE — 2026-10-15 20:51 UTC

[Decision](physical_inversion_2026-10-15/decision.md),
[claim registry](physical_inversion_2026-10-15/discovery_registry.md),
[minimum input](physical_inversion_2026-10-15/one_next_input.md),
[handoff](physical_inversion_2026-10-15/handoff_ledger.md).
Three no-native analytical phases from89ef0f1 completed. Exact chemical/disorder
projection accounting, common/mass covariance and sharp-atom/inverse-root
certificate accepted under assumptions. Z>=3/4 gives localrooterror<=2(1-Z)eta/Z
without D; physical atom eligibility/uniform errors/transversality are required.
A positive p<=1 eliminated threshold weight excludes a target atom; even
zero real inverse and zero damping do not suffice. These are established
Friedrichs/Stieltjes territory; specific synthesis/constants novelty UNVERIFIED.

Actual16cell geometry confirms N2 sampled, N3 invisible. Current PBE ordered
and nonstationaryH304 do not identify physical alloy mass/x_c; no opposite
completeH304 completion/sign was fabricated. Prior endpoint/moment/directional,
full-support Bernoulli, host-invariant/full-residualT, retarded/PV and all native
refusals retained. ONE future input is a controlled physical Gamma8/heavy-hole
infrared certificate on the crossing domain; endpoint impurity needs bounded
background adapter and a stationary host. It can falsify sharp eligibility,
not close x_c alone. No honest new nativecost/admission or materialerror exists.
Focused symbolic/dense/continuum/geometry checksPASS; protected hashes/DFTdiff
verified. Claim-level primary comparison done; Alowa fulltext incomplete.
STOP at physical information boundary, no native jobs or historical goal change.

## Analytical physical-inversion assignment: phases1–2 — 2026-10-15 20:40 UTC

From89ef0f1. [Scope](physical_inversion_2026-10-15/scope.md),
[accounting](physical_inversion_2026-10-15/chemical_disorder.md),
[observable definitions](physical_inversion_2026-10-15/observables.md),
[prior-art matrix](physical_inversion_2026-10-15/prior_art_matrix.md).
Exact static counterexamples establish projected chemical-subtracted kernels
need not be causal and separate scalar/mass variances omit a mass-relevant
cross-covariance. Dense/exact polynomial checksPASS; no nativeDFT/HSE job.
Earlier full/residualT, host-invariant, threshold and identifiability results
retained. Physical sharp/real-root/resonance/Green-zero/topological definitions
are separated; no physicalxc. [Sharp-atom certificate](physical_inversion_2026-10-15/sharp_atom_certificate.md)
proves a gap-free local inverse-root enclosure if independently known Z>=3/4.
[Threshold obstruction](physical_inversion_2026-10-15/threshold_eligibility.md)
shows a positive coupling density with exponent<=1 rules out a target atom at
threshold; it is established Friedrichs mathematics, not a HgCdTe measurement.
Independent continuum/bath/counterexample checksPASS. Continue the actual-data
minimum-input decision. Phase1 actual checkpoint20:31; Alowa limited to preview; novelty
UNVERIFIED. All prior native failures and protected state unchanged.

## Read-only continuum response and true physical moments — 2026-10-15 19:22 UTC

Continued accepted native283aad5; retained successorguardrails19b6679.
[Decision](hse_residual_response_2026-10-15/decision.md),
[reset](hse_residual_response_2026-10-15/handoff_ledger.md),
[minimum inputs](hse_residual_response_2026-10-15/minimum_input.md).
Second-order residualGreen bound needs no common spectralgap and only a query-
actionerror certificate. At eta.5eV original-frame inverseordering−.729914eV
has conditional finite-native interval[−1.232296,−.227533]eV; eta1/2also negative.
Small eta.05/.1/.2 uncertified. The1e-6Rywholequeryerror is an explicit unproved
intervalassumption, not material uncertainty; signcapacity.00149924Ry. Noη->0,
realpole/topology/physicalgap/xc inference. Counterexample searches found NO
opposite sign; limitedcompletions preserve304basis butnot12extra controls.

True nativephysicalHP controls expose5.8135e-7frame leakageoutside304 and
1.3912e-5Ryactiondifference; four-moment shortcutREJECTED. Actual Γ6/8spectral
standarddeviations2.02504/1.68314eV are notlinewidths. Squaredleakage bounds
unmeasuredthirdmoment1.213e-7Ry³; fourthnotclosed. All316query geometry still
misses6next directions at1e-8/1e-10. FD304commutatorop.0521183Ry gives conditional
fullFDdistance>=1.3115e-7; no SCF/Cdrelease despite symmetry/charge.

Independent bath/action/608dense-Schur/gauge/moment checksPASS; allnativepins,
stock/dirtyDFT/oldrefusals/registry/cgroupcleanup exact. No additional native
job, ownerchange, queue, other-session/main/goal edit. STOPnativeat actual
stationarity/nonlinearH[D1] boundary. Nextphysicstheory: qualifiedinversion
criterion and minimal causal chemical/disorder input, not anotherproxyasgap.

## Complete native H304 and an actual state obstruction — 2026-10-15 15:55 UTC

[Decision](single_state304_2026-10-15/decision.md),
[reset](single_state304_2026-10-15/handoff_ledger.md). ONE fresh native HSE8
trialD0 query,304columns+12controls from ONE state, not oldsplice. Source review
rejected unsafe m316vexx at cached176capacity; two legal158calls and explicit
SOCworkspace preserve arithmetic. Actual local/SOC/source/kernel before/after
snapshot bytes equal on bothranks; allTd/Theta1.7e-11, Hermiticity1.3e-15,
charge144e and completehpsi/component2.4e-16 pass. Owner329.21s/kernel5.56GB,
12GiB/swap0/tasks12/600s/floors/14GiBbudget and terminalcleanupPASS.

The304FDstate is NOT stationary: μshift−1.4723meV, Fermi quartet whole-H
residual.02378468Ry, fullcommutator.50357023RyF, densityD0mismatchop.0094243.
Finite-H freeenergy−163.092meV/cell is not a nonlinearHSE energy decrease.
Missing lower-right operatorblock is removed; occupied fullspace/coupled-tail
and H[D1]/outerconsistency are NOT closed. NoCd/SCF/gap/xc release.
Continue distinct read-only finite-resolution resolvent qualification with
measured R=HV−VA; no anothernativejob, presumedcomplementgap or oldFAILretropass.
ProtectedDFT/stock/oldledger/HSE16/main/sessions/blockedgoal unchanged.

## Independent native static input and finite stop — 2026-10-15 15:28 UTC

After publishing c16f9af, continued the distinct PBE saved-charge6physical+
6Theta-control question. [Decision](static_environment_2026-10-15/decision.md),
[reset](static_environment_2026-10-15/handoff_ledger.md). ExactlyONEunshared
operator-only native job, no SCF,2.36sPW. OwnerFAILED4.0203s on incomplete
taskFDinventory, kernel.956GB. Not proven benign race. Ownedcleanup verified,
no retry, sharedWITHHELD. Original frozen source also had a Reader import
defect missed by ASTpreflight; original log/source retained, prospective
one-line import remedy tested IN MEMORY only. No production retropass.

UNQUALIFIED packet diagnostic: native savedrhoGexact, charge288.0000000001002e,
H/component/Theta~1e-15; static original-frame trace-.685644699eV. Accepted
unshared finiteeta.05trace-.685188200eV andpartialfirstmoment-.624613921eV
differ by.4565meV/61.03meV respectively. No sharedstaticcontrast/gap/eigenpair
accuracy or materialerrorbar inferred from this refused experiment.

Read-only HSEnew-query selfblock spans3.371486..52.575660Ry, Hermiticity1.2e-15;
not wholecomplement gap or304FD. Crossoperatorreciprocity9.86e-15Ry is NOT
identity. Restricted lower-block delta_C would suffice for a SEPARATE bounded
Ritz/HSFD claim, but it is unproved. A future unified304single-state batch
forecast~319s avoids splicing; no new build/job admitted under failedscope.

STOP native trajectories at strict state identity and terminal inventory/import
gates. No genericinfra campaign, repeatedfailedunit or unsafeworkaround. Exact
source/raw/protectedDFT/stock/cgroupcleanup checks pass; both nativefailures
preserved, no activefamily/queue, HSE16/main/other sessions/blockedgoal unchanged.

## Native append acquisition and strict scientific refusal — 2026-10-15 15:08 UTC

From9401972, exactly ONE new residual152query using accepted b3ELF and exact
oldsource/controls. [Decision](append_hamiltonian_2026-10-15/decision.md),
[reset](append_hamiltonian_2026-10-15/handoff_ledger.md). Owner/terminal/resource
PASS168.361s/4.244GBkernel;12GiB/swap0/tasks12/600s and all floors/cleanup pass.
STRICT science FAIL: VXCcontraction1.42e-13Ry,rhoR5.55e-16,vrs8.01e-13Ry and
directFockcontrols2.08e-17 differ in native reconstruction. Exact importedD0
does not imply bitwise native state. No tolerance change, native retry,304splice,
FDresult or manufactured convergence. Raw source/actions/refusal retained.

Old152operator acceptance/nonstationarity remain. New exact append needs full
canonical nativeoperator replay; a bounded-error contract would be SEPARATE,
not a retropass. Cause of near-roundoff differences not established. Protected
DFT/stock/oldledger/HSE16/other sessions/main/goal unchanged. Continue independent
PBE staticH probe source qualification at retainedcharges, not HSE repetition.

## Follow-through: full matrix contrast and minimum tail information — 2026-10-15 14:18 UTC

After the native same-D checkpoint f249885, continued distinct retained-data
physics without another native job. [Decision](matrix_environment_2026-10-15/decision.md),
[proofs](matrix_environment_2026-10-15/theory.md),
[reset ledger](matrix_environment_2026-10-15/handoff_ledger.md).
Same-cell PBE16x=.25 sharing-minus-unshared full6matrix kernel at ownEF/eta.05:
norm82.917971meV, conditional fixed-frame lower57.679585meV; trace-81.658351meV
interval[-132.135124,-31.181578]meV. All nine prescribed matrix norms have
positive lower bounds. No real-axis common gap assumed; no physical gap claim.

Energy derivative -.09024435 remains unresolved even after a preconditioned
resolvent bound reduces matrix error15.24->.5892. Independent omitted-support
certificate L>.206596eV would settle its conditional sign; printed bands are
not a completeness/eigenpair certificate. Ordered20/40eV positive tail examples
alter static trace20.93/22.59meV while preserving all retained data. Thus inverse
kernel cannot uniquely identify static localN2operator. Material errors excluded.

Independent affine-orbit geometry:56three-Cd subsets split32N3-bearing/24N3-free.
Candidate012x=.375 has group6 and histogram(1,3,3,1,0); candidate017N3-freegroup8.
One new cell mixes composition/environment; a same-x contrast needs two new
SCFs. Fixed-local count rank closes only with COMPLETEbackground-independent
operators, absent here. No N3job admitted/queued or random-alloy inference.

STOP at concrete next physical input:152newH[D0] residual-direction actions for
the304joint-symmetry FDbridge; alternative static PBEinput is12completeH probe
actions on the retained two SCFdensities. Coarse tail-order certificate suffices
for the derivative alone. No further native work under the completedONEhost
acquisition. Tests/pins pass, protectedDFT/stock/oldfailures unchanged; no main,
other-session, historicalgoal or originalHSE16 changes. Physicalxc stillOPEN.

## Complete SAME-D HSE operator, actual FD obstruction — 2026-10-15 13:56 UTC

[Native decision](same_density_hamiltonian_2026-10-15/decision.md),
[reset ledger](same_density_hamiltonian_2026-10-15/handoff_ledger.md).
Fromb799d28, exactly ONE new8atom176capacity/144e/HSE+SOC50-200-200Ry/Gamma-q1
host query. Explicit NEW positive trialP142+.5P4, not FD-of-HSE. Native fixed-
occupation density path then exxinit->v_of_rho->set_vrs->newd reconstruct SAME-D
kinetic/local/nonlocalSOC/DIRECT Fock. No oldACE, SCF, Cd, restart orHSE16.

CALCULATED: charge144.00000000000006e, independentrho agreement2e-15, complete
h_psi/component difference2.4e-16; all24Td/Theta~1e-14. Owner185.30s, kernel
4.246GB; all12GiB/swap0/tasks12/600s/floors/live2rank/cleanup gates pass. Original
physical8atom40Ry reference bytes fixed; projectedH ordering−.728387722eV and
Gamma8spread4neV are operator expectations, NOT native/converged gap values.

The missing completeH[D0] acquisition is REMOVED. Native operator symmetry
does not supply FDstationarity: projected density mismatchop.0040404, Fermi
Ritz quartet whole-space residual.02625424Ry. Conditional commutator lower
bound gives full-space FDdensityerrorop>=1.2211e-7. No tiny useful upperbound
or full-state convergence is invented. Old negative gates remain immutable.

New read-only block-Krylov completion: occupied298/full304spaces retain joint
symmetry2.1e-11 and capture existingHD/HQ actions. Next indispensable new native
input is ONLY152H[D0] actions on residual directions, not a repeat of knownHQ.
Unknown lower-right block and density-update/outer convergence still required.
No second native query under this one-acquisition scope. Raw packets/source/
ELF/PP/backend/owner hashes archived; protectedDFT/stock/oldledger exact. No
queued family, sessions/main/blockedgoal unchanged. Continue independent matrix
environment/N3identifiability analysis; no physicalxc or empirical fit.

## Follow-through: redistribution and exact HSE input boundary — 2026-10-15 06:47 UTC

After publishing native chemistrya753cf5, continued two independent read-only
science phases without another QE job. [Spectral decomposition](environment_redistribution_2026-10-15/decision.md):
Gaussian contrast=−45.073266central+42.996617rest=−2.076649meV; inverse contrast
=−66.283104central−15.191350rest=−81.474454meV. Exact identities agree4.55e-16eV.
No averaged shared quartet or fictitious selected-only Hamiltonian. OwnEF
center±.1eV inverse signs remain conditionally negative; Gaussian unresolved
sign and all original numerical evidence unchanged. No new materialerrorbar.

[State-bridge decision](fd_bridge_resolution_2026-10-15/decision.md),
[proof](fd_bridge_resolution_2026-10-15/theory.md),
[reset](fd_bridge_resolution_2026-10-15/handoff_ledger.md). Actual joint152basis
has six near-unit directions beyond saved176states, mostly highG with~40Ry
kinetic, NOT six established low-energy bands. A new twirled144e trial closes
symmetry3.42e-15 but lacks same-DHSEHamiltonian/FD qualification. PROVEN finite-FD
Hilbert-Schmidt residual/coupling/tail bounds require no gap aroundmu; independent
matrix tests pass. No full-space tail/convergence guarantee is invented.

STOP at precise rank1missing input: [complete same-Dnative H[D] action](fd_bridge_resolution_2026-10-15/minimum_input.md)
with source natural weights, actual local charge/XC/SOC, independent direct
exchange controls, FD/eigenstate/offspace residual. Old directFock/6local actions
refer to different/incomplete states. No further HSEtrajectory can safely be
released merely from space closure or a resource forecast. This is a scientific
state/input boundary after multiple results, not an owner or permission block.
No native job queued, historicblockedgoal unchanged; physicalxc remains OPEN.

## Same-composition N2-bearing PBE contrast — 2026-10-15 06:42 UTC

[Decision](pair_environment_2026-10-15/decision.md),
[reset ledger](pair_environment_2026-10-15/handoff_ledger.md). ONE fresh stock
PBE16pair: Cd(0,7)unshared8N1 versus Cd(0,1)sharing2N0+4N1+2N2, SAME x=.25,
cell/PP/50-200Ry/Gamma/352bands288e/FD.001. Both converge12/13steps under600s,
owner365.3/374.7s, kernel peaks2.095GB; all livelease/charge/symmetry/cleanup
gates pass. Native groups24/4; relevant shared clusters are Kramers doublets,
not an enforced Gamma8quartet. Fixed native50Ry16host frame declared BEFORE
acquisition. Original40frame/old failures unchanged, not silently requalified.

CALCULATED sharing-minus-unshared GaussianW2−2.076649meV, conditional interval
[−11.327833,+7.174536]meV unresolved. Scalar causaleta.05−81.474454meV,
conditional[−111.443387,−51.505520]meV; full6matrix−81.658351meV. These are
different observable responses, not material gap estimates. Physical sharing
Gamma8derived doublets span4.04794meV; Gamma6/8weight redistributes. Same-cell
finite-FD free energy−88.571432meV, not isolated pair binding or zeroTmaterial
energy. Conditional bounds exclude functional/SCF-eigenpair/BZ/cell errors.

N2geometry has now been sampled; this does NOT extract its local operator from
nonlinear projected spectra. N3remains an exact unseen environment in the fixed
local model, and random-alloy/HSE input remains missing. No physicalxc. Protected
DFT/stock/oldledger hashes exact, raw evidence archived, no native family left.
Continue read-only joint152FD/state and spectral-redistribution diagnostics;
no defective HSEiteration or PBEgrid sweep is authorized by this result alone.

## Real16atom x=.125 chemical response — 2026-10-15 05:52 UTC

[Native physics decision](chemical_pbe16_p2_2026-10-15/decision.md),
[completed reset ledger](chemical_pbe16_p2_2026-10-15/handoff_ledger.md).
ONE native stock-PBE16 host11steps and ONE Cd12steps converge at50/200Ry,
352spinor bands288e, fixedSG15FR/a6.46/Gamma/FD.001. Charge errors<6.4e-11e;
340.123/345.365s, kernel peaks2.114/2.105GB, all owner/resource cleanup gates pass.
Exact physicalG cell embedding preserves ORIGINAL Gamma6/8 frame. Both actual
native multiplets passTd/Theta/degeneracy BEFORE means. Tracked ordered-cell
multiplet response+169.033285meV; GaussianW2+201.458261meV conditional interval
[197.871355,205.045167]meV; causaleta.05+135.136468meV, conditional scalar
[118.253626,152.019310]meV. Distinct observables, NOT three estimates of one gap.
Both absolute orderings negative. No dilute slope, random-alloy gap orxc.
Cell/composition/BZ differ fromx=.25k3; no bowing or convergence inferred.

Native full nonlocal densityTheta defects4.53e-7/1.64e-7 remain above1e-8HSE
source requirement despite tiny ordered-cell quartet spreads. No HSE release.
Old pre-QE socket owner failure and wrong-unit readback assertion remainFAILED;
independent corrected-unit read-only host qualification did NOT rerun the host.
Stock/dirtyDFT/all old evidence exact; no other sessions touched. Historicalgoal
unchanged. This finite chemical acquisition is complete; no further job queued.

Next boundary: [exact unseen-environment kernel](ordered_environment_2026-10-15/theorem.md)
and [ranked independent input](ordered_environment_2026-10-15/minimum_input.md).
Both ordered geometries contain onlyN0/N1; they cannot determineN2/N3local
operators even from full Hamiltonians. First useful missing chemistry is a
same-cell/same-composition Cd-Cd sharing contrast; HSE first requires actual
full Hamiltonian/FD-state qualification. Conditional finite-eta resolvent bounds
relax support-freeD, not missing material input. All previous no-go results stand.

## Joint crystal/Theta space, actual state still missing — 2026-10-15 05:25 UTC

[New decision](joint_symmetry_2026-10-15/decision.md),
[proof and state obstruction](joint_symmetry_2026-10-15/theory.md).
CALCULATED new152space maxall24Td/Theta/primitive-translation leakage1.61e-14.
Original occupied/reference coverage changes4.65e-7/9.30e-7: old1e-10source
preservation gates still FAIL. No native occupations changed, no new HSE run,
no inherited source-exact Fock or FD state claim. PROVEN separated twirled
projectors have an invariant nearby rank-preserving cutoff with distance
<=delta/(1-delta). PROVEN space closure alone does not imply D=f(H[D]); actual
full Hamiltonian and off-space/FD/charge residual remain indispensable.

Next independent acquisition is a separately preregistered PBE16 orderedx=.125
host/Cd pair, not a repeat of the defective HSE host or old90Ry cold-smearing
PBE16 attempt. No new numerical chemical result yet at this checkpoint.

## Retained PBE causal chemistry response — 2026-10-15 04:32 UTC

[Decision](pbe_causal_response_2026-10-15/decision.md): independent read-only
causal contraction of accepted k3/50-200Ry ordered x=.25 host/Cd complex spectra,
original fixed physical Gamma6/8 projectors. At each own Fermi and eta=.05eV,
CALCULATED inverse-resolvent ordering response +.354050668eV with conditional
positive-tail/frame/IEEE interval [.344926560,.363174775]eV. All9 preregistered
t/eta choices have positive conditional sign; no new native run or grid.

It differs from Gaussian W2 +.392177486eV by38.1268meV on the SAME operator:
observable dependence, not HSE/material error. Both absolute inverse orderings
are negative. Eta is analytical resolution, not linewidth. Unknown functional,
SCF eigenpair, BZ, cell/random-alloy and material errors remain outside these
intervals. No sharp gap, topology or physical x_c. These additional contractions
do not identify composition dependence; previous continuum and endpoint/local
identifiability no-go results remain. The native joint-symmetry/state bridge
below remains the precise next boundary; no further SCF/Cd released.

## Native TR constructor and full-symmetry boundary — 2026-10-15 04:24 UTC

[Native decision](symmetry_constructor_2026-10-15/decision.md),
[read-only proof/audit](antiunitary_closure_2026-10-15/decision.md),
[precise next input](symmetry_constructor_2026-10-15/next_input.md).
Direct residual SVD resolves166missing directions at1e-8 in the old176source,
not merely2. Full source density TR defect grows5.198e-7→.001428→.007883→.999987
at sources1/2/3/8. A density-preserving basis repair is mathematically impossible.

ONE fresh native two-rank D/TD fixed-source test,658.09s, NEW900s hard cap,
unchanged176physicalbands/HSE kernel/PP/cell/kq; noSCF/nativeACE/restart/Cd/retry.
Canonical inputs pass byte readback. CALCULATED direct covariance2.32e-16;
new364auxiliary Gram positive(min.012319Ry/cond75.4), OFFLINE compression exact
source/reference~6e-16 andTRcomm9.60e-16. This is the explicitly NEW ensemble
Dbar=(D+TD)/2, not nativeFD of a convergedHSE Hamiltonian. Old BYTE replay remains
REFUSED. Actual kernel4.780GB, sampledRSS4.524GB, host/diskfloors and cleanup pass;
old raw/stock/dirtyDFT/ledger exact, no live ownedfamily, combined output3.938GB.

Direct actions now resolve the old ACE/offspan error at SAME originalD:
2.8179%relative onTPhi, op.131652Ry/maxcolumn.100545Ry, versus3.11e-15 own-source
interpolation; occupiedweightederror6.72e-8Ry. These are actionnorms, not gapshifts
or proof of the old instability's cause. Naturaloccupied rank146ofDbar isTRclosed
and positive/wellconditioned with6.98e-13e dropped, but independent reference
error4.03e-4 andTdselfcomm2.97e-8>1e-8 REFUSE it as a fullsolver replacement.

PROVEN/CALCULATED: TR protects doublets, not aGamma8quartet. Both oldsource and
new364cover have largeTd-generator leakage; native joint crystal/translation/
TR state, occupations/entropy and Hamiltonian residual remain missing. No further
identicalHSE/Cd run is admitted. No prior gates/FAILs weakened, physicalmagnetism,
fullHSE convergence, wholeSCFmemoryadvantage or physicalx_c claimed. Historical
goal and other programs/sessions unchanged. Underlying algebra established;
noveltyUNVERIFIED. This is a substantive native/mathematical milestone and a
precise next scientific boundary, not an originalgoal resume.

## Independent direct-kernel discriminator — 2026-10-15 03:40 UTC

[Decision](exchange_symmetry_2026-10-15/decision.md): from pushed63b8d75, one
fresh two-rank fixed-source/Theta-source Fock probe completed in27.064s, with no
SCF, ACE rebuild or restart. Actual source, trial, G, et and wg bytes match.
Owner, kernel-resource and terminal gates passed. The retained direct-action
BYTE gate refused at1.402e-17Ry maximum difference (~1.1e-16 relative). The
original traceback is preserved; there is no accepted FINAL and no retry.

CALCULATED DIAGNOSTIC: within the new run, direct-kernel time-reversal covariance
has1.645e-16 relative residual, and its second identity has1.660e-16. This
disfavors a gross covariance failure for these tested fresh-kernel inputs. It
does not pass the refused replay or establish the cause of the old SCF instability.
Peak kernel memory was1.847GB; all limits held. Both phases' combined native
outputs are3.038GB<14GiB. Protected DFT, stock, earlier evidence and the old
ledger are unchanged; no owned MPI family remains live.

PROVEN: the smallest invariant source superspace is S+ThetaS. Equal local charge
and zero local spin density do not determine the nonlocal exchange operator.
Three tiny independent checks pass. The frozen176-column ACE/source contract
does not certify the required nonmagnetic host. Stop native/Cd work at this
scientific boundary. The next independent input is a symmetry-qualified,
self-consistent host operator/density, with a complete constructor or direct
control before matched chemistry. Do not average the split Gamma8 energies into
a gap or silently change occupations/bands. See the
[ranked minimum input](exchange_symmetry_2026-10-15/minimum_input.md).
All prior finite activation/PBE results retain their original scope. No converged
HSE or physical x_c is claimed; the historical blocked goal is unchanged.

## Eight-source hybrid host and symmetry falsification — 2026-10-15 03:16 UTC

[Decision](hybrid_convergence_2026-10-15/decision.md): one fresh host,1628.053s,
8source builds; final E−1936.340914771158Ry, half-Fock−35.836800151016Ry,
dexx1.804e-6Ry>1e-9. Native owner/packet/science acquisition/readback gates PASS,
outer convergence=false.12GiB/swap0/tasks12 and preregistered1800s low-priority
bound held; kernel6.645GB includes output cache, sampledRSS4.329GB. Cd notrun.

CALCULATED exact native density TR witness grows to0.999765; central quartet
spread0.655255eV, despite charge error<1e-10e and exactly zero LOCAL spin density.
First176-column ACE span is non-TR-closed (leakage².81948), ACE antiunitary action
commutator relative.02818, while source action reconstructs5.44e-16. Independent
native scalar witness agrees2.89e-15. Thus crystal-symmetry metadata/source-space
ACE equality do not qualify the intended nonmagnetic host. No physical magnetic
phase or exact-HSE instability cause inferred. Earlier finite activation numbers
remain valid for their scope; no updated chemical HSE pair/gap/x_c is claimed.

STOP this trajectory/Cd release, not the long-horizon mandate. Next smallest
independent discriminator is fixed-source direct Fock time-reversal covariance
with canonical retained data; no SCF/restart or changed physics. Fresh input,
source/FFT/kernel and owned-resource gates required before any native probe.
Source/matrices/causal-window and density analyses/proofs/raw evidence retained;
protected DFT/stock/history/16atom/main/sessions/goal unchanged. Restart remains
unqualified. See new decision/verification/handoff before further action.

## One hybrid relaxation and second ACE — 2026-10-15 00:30 UTC

[Measured decision](chemical_hse_relax_2026-10-15/decision.md): new scope from
bce98cc, fresh private build/jobs and84/82-byte checked sockets. Same HSE physical
inputs, exactly one hybrid inner solve and second Fock/ACE per member, no retry.
Both native members pass all source/owner/readback/resource gates in410.333/
409.315s with kernel peaks4.549/4.542GB; preliminary11/hybrid9steps, inner residuals
7.77e-11/4.42e-10Ry. Final source HDF5 and within-rebuild density bytes pass;
direct/ACE~6e-16; independent old-xi/new-Phi Fock/dexx bridge <=2.85e-14Ry.

CALCULATED same physical Γ6−Γ8 chemical trace +44.184097→+39.811504meV;
relaxation−4.372594meV = exchange+1.239720 + local−5.612314. It compares updated
HSE[rho1] against preliminary PBE[rho0], not a Gaussian gap or HSE−PBE[rho1].
Final eigenvalues solve first ACE, not rebuilt second operator. Native dexx
.00251875/.00254897Ry; HSE outer convergence false and limiting/material error
unknown. Positive finite trace does not certify full-gap/inversion or physicalx_c.

Raw/source/matrices/provenance retained; all caps/floors and1.466GB final output
pass, own cgroups absent, lock free, stock/dirtyDFT/old FAILs/accepted data and
original16atom352band/Calcura/sessions/supervisors/goal unchanged. No DFT/main
commit, restart or whole-SCF memory saving claim. Current finite scope complete;
no more native work. Further outer relaxation/remainder is the next missing input.

## Real matched HSE first-ACE activation — 2026-10-14 23:57 UTC

[Scoped decision](chemical_hse_firstace_p2_2026-10-14/decision.md): clean c50f466,
separate new authorization and p2 root; only reviewed short-socket change. Actual
103/101-byte binds pass before services. Same native ELF/physics, fresh leases,
ONE host and ONE Cd two-rank Γ/q1 first ACE, all gates PASS, no retries. Old
failed owner/root/evidence remains FAIL and unchanged.

CALCULATED fixed original Γ6−Γ8 trace of HSE activation, Cd minus host:
+44.184097 meV = exchange +55.956327 + local −11.772230 meV. This is a direct
fixed-density operator comparison, not a spectral gap or Gaussian response.
Both preliminary SCFs 11 steps and <1e-9 Ry; source waves/density byte-exact,
direct/ACE <6e-16 and three independent offline scientific checks PASS.
Guard walls 215.601/200.986 s; kernel peaks 4.232/4.226 GB, caps/floors/cleanup
pass. HSE deliberately unconverged; source spectra remain semilocal. Raw native
provenance and complex matrices archived/pinned; dirty DFT/stock/past failures/
16-atom target/sessions/Calcura/goal unchanged.

First-ACE feasibility is now measured. Full HSE within 600 s is not bounded;
next useful finite acquisition is one hybrid relaxation plus rebuilt operator,
with separate source/state/cost admission. Nothing further launched. Physical
x_c, material uncertainty, restart and whole-SCF memory saving remain OPEN.

## HSE acquisition owner failure before MPI — 2026-10-14 23:16 UTC

[Actual scoped decision](chemical_hse_firstace_2026-10-14/decision.md): from
40d2b9e, explicitone8atom176band144e/HSE.25/.106/Gamma-q1/50-200-Fock200Ry/
FD.001/SG15FR/6.46A matched firstACE request. Minimal private3object observer/
false-convergence postpunch stop compiles/links with unchanged original kernel/
ACE arithmetic and stock/backends. Fixed6Gamma direct/local action anddensity/
state capture designed, **native numeric correctness UNEXECUTED**.

Sole host owner fails beforeMPI on114byteAF_UNIXlease.sock pathname. Real
exactaddress nonMPIbind reproducesrefusal;105byte.../s succeeds/cleansowninode.
Retained managerexit1,READY but noLAUNCH/RANKS/GUARD_RESULT/pw.out; original
frontendmissingGUARD_RESULT error retained, underlyingservicestderr notsaved.
No HSEenergy/state/resource/chemistry exists; Cd notrun. Userno-retry/firstowner
FAILrule enforced. Owneronlykernelpeak12955648B notHSE; cgroupgone/lockfree/
oldledgerexact. New shortsocket/freshp2/attempt-reuse-refusal/root-binding patch
is prospective/unapplied, not originalFAIL promotion or futurelaunch approval.

Three focused source/reference/refusalchecks PASS, sourcebuild/preparedinput/
reference/failure records archived. Allfrozen/protectedstock/dirtyDFT/pastFAILs
and acceptedPBE+.392177 unchanged; no newservice/native retry/PBEgrid/16atom/
goal/supervisor/Calcura/session/main/DFTcommit action. STOP thisfinitefailedowner
phase; nextphysics remains corrected/newlyscopedHSEfirstACE after minimumlaunch
integrityfix. Materialfunctional dependence/fullHSEcost and physical x_c OPEN.

## Same-cutoff k3 chemical pair — 2026-10-14 22:20 UTC

[New finite decision](chemical_k3_2026-10-14/decision.md): from3fe5ef2, ONE
sequential stock PBE+SOC8atomHg/Cd pair at176bands144e/50/200Ry/FD.001Ry/
6.46A/nativeTd/unchangedsolver, onlyunshiftedk2→k3/privatepaths change. Native
24crystal symmetries,four stars(1,6,12,8)/27 and uniqueGamma capture confirmed;
withoutTR theoreticalstar splits4+4. BothSCFs converge11steps243.78/225.01s,
independent charge<9.2e-11e. Host terminal/source/physical frame gates pass
before Cd. Initial crystal/lattice XML parser error source-corrected and retained;
no threshold relaxation or native retry.

Original40Ry Gamma6/8 projectors physically embed7809→10827vectors with no
source norm lost/renormalization/index overlap; all24maps pass. W2 response
+.392177486293eV versus+.393337031960eV k2: measured−1.159546meV; conditional
grid difference[−8.78763,+6.46854]meV includeszero. All tested widths/references
retain positive conditional response; primary host/Cd member orderings both
negative, so no positive-gap claim. Newhostframe effect+.099038meV vs+.087142
is separate. Five focused native-data/math checks PASS; material/operator/
eigenpair/finite-cell/BZ errors OPEN. Two same-cutoff meshes do not prove convergence.

Kernel/typedrank/managerexit0/emptygroup gates pass; maxRSS1.037GB/kernel.953GB
under12GiB/swap0/tasks12/600s,host4GiB/disk10GiB floors; aggregate500674560B
under sampled14GiB. Raw/complex/source pins archived; stock/dirtyDFT/oldledger
exact, all historic host uncertainty/HSEFAILs preserved. No NSCF/retry/HSE/
extra job/supervisor/Calcura/other session/historicalgoal changes. STOP finitepair.

Recommend a separately qualified matched8atom HSE Gamma/q1 FIRST-ACE pilot,
same176/50/200/Fock200/FD/PP/cell; source-conditioned2.230GB subtotal is not
fullRSS bound,320–365s/pair is heuristic. Need actual176bandstop/diagnostics/
state/FFT/output/resource/owner admission and separate authorization; no launch
or source build here. FirstACE would not imply fullSCF or materialgap/x_c.

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
