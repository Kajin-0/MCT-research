# R07 successor-agent scientific handoff — 2026-10-15

> **Read this before launching another calculation.** This document captures intent and navigation across context-window resets. For authoritative live truth consult `state.md`, individual `decision.md` and native readback/verification records, and current Git/tmux state. Never overwrite newer developments with this dated snapshot.

## New VCA physical-reference projection — 2026-10-17

Read [VCA projection decision](vca_x0125_hse_2026-10-17/decision.md) and [numerical record](vca_x0125_hse_2026-10-17/postprocess/reference_projection_results.json). G-labelled reference transport selects Γ6-like33–34 and Γ8-like35–38, reference weights >.9998 and max Td character errors <1.2e-13. Strict subspace amplitudes and full-density 1e-8 symmetry **FAIL**. Candidate ΔΓ=-98.78796872 meV, candidate half=-49.39398436 meV, conditional shift from HgTe half +95.39926805 meV. Do **not** call a strict mass or physical random-alloy xc. No native launch or spend.

## NEWER VCA Gamma audit — 2026-10-17

Read [postprocessing decision](vca_x0125_hse_2026-10-17/decision.md): saved-wave Γ full-density Theta 3.95518494693e-7, Td max 4.95143773706e-7 **both FAIL strict 1e-8**. Provisional 33–34 minus 35–38 energy -98.78796872 meV, half -49.39398436 meV; physical Γ6/Γ8 projection/characters not certified. This is not accepted m_VCA or physical xc; no second QE execution.

## CURRENT R07 terminal VCA checkpoint — 2026-10-17

The previous `LIVE`/`RUNNING` sections below are historical launch snapshots, **superseded** by the [terminal decision](vca_x0125_hse_2026-10-17/decision.md) and [native checkpoint](vca_x0125_hse_2026-10-17/completed_native_checkpoint.json). One zero-cost stock primitive Hg0.875Cd0.125Te HSE+SOC k4/q4 run has **converged numerically**: six exchange builds, dexx 3.5e-10 Ry, `EXX self-consistency reached`, `JOB DONE`, total -484.01592595 Ry, XML SCF true. Worker exit 0, zero restarts, 6,217,211,904 B observed kernel peak. Saved wavefunctions/ACE/density/XML remain in private DFT `.local`. **No Γ6/Γ8 projection or strict full-density Theta/Td 1e-8 certificate, accepted half-gap mass, physical random-alloy x_c, zero-smearing/material error claim.** Next: read-only physical postprocessing; no second HSE job or spending. Host primitive strict symmetry failure unchanged.

## LIVE VCA x=.125 HSE — explicit sole-case authorization

Read `vca_x0125_hse_2026-10-17/decision.md` and running checkpoint FIRST.
Actual stock two-rank SCF now RUNNING;worker r07-vca0125-hse-20261017.service,
observer r07-vca0125-hse-20261017-observe.service. Root
`/home/User/opencode_workspace/DFT/.local/r07_vca_x0125_hse_20261017`.
User approved this single zero-cost24h case;historical unapproved text below
remains prior status,not cancellation. No restart/retry/new case. Do not kill
an active authorized computation. Review same-unit final output when terminal,
then read-only physical projections/FD/full-density1e-8 gates. No result yet.

## CURRENT R07 BUDGET AND SCIENTIFIC STATUS — 2026-10-17

**$0 additional spending.** The prior 128 GiB cloud proposal is historical and is superseded for acquisition. Do not rent or buy compute, hardware or services, and do not launch a native HSE job automatically. See [current zero-cost policy](zero_cost_policy_2026-10-17/decision.md) and [validated VCA compatibility](vca_fr_compatibility_2026-10-17/decision.md). Latest verified research HEAD before this policy update was 66124cb. VCA SG15 FR+SOC pseudo/reader passed five dry and four PBE endpoint checks; x=.125 VCA HSE **has not run**. The primitive HgTe HSE reference retains conventional SCF PASS but strict 1e-8 full-density symmetry FAIL. Scientific goal remains nonempirical composition-dependent inversion and eventually disorder-qualified x_c.

## Non-negotiable ultimate objective

Develop a predictive, **first-principles, nonempirical and analytically interpretable microscopic theory** of Hg_(1-x)Cd_xTe that explains *how Cd substitution alters the Gamma6/Gamma8 inversion*, determines the physically appropriate **signed zero-temperature inversion mass / gap**, and ultimately predicts the **critical composition x_c** with defensible numerical, configurational and material uncertainty. Chemical average, coherent scattering, local correlations and electronic self-consistency must be treated consistently. **Do not fit empirical alloy-bandgap coefficients to obtain x_c**. Hansen/other models may be benchmarks, not the derivation.

We seek a distinct, falsifiable physical advance beyond extant HgCdTe SQS, DFT/HSE, DOS, CPA/SCBA and Kane-mass literature, not a simulation count or generic computational framework.

## Governing scientific principles

1. **Physics first, then methods.** Before expensive work identify: the unknown microscopic operator or physical quantity; how it enters the signed inversion criterion; what independent prediction becomes possible; what result would falsify the assumption. Run a native job only if it can change that decision.
2. **Do not double count alloy physics.** An effective averaged resolvent may be written schematically `Gbar(z,x)=[z-Hbar(x)-Sigma(z,x)]^-1`, but the definition of `Hbar`, disorder self-energy, projector and reference must be fixed jointly. Chemical substitution changes the mean and fluctuating potential. Do not arbitrarily add independently measured finite-density HSE activation to PBE centroid or causal inverse-resolvent responses.
3. **Define the transition physically.** An ordered-cell Gamma-character level difference, Gaussian centroid, finite-eta inverse resolvent, Kane-mass model parameter, Green function mass-zero and bulk topological/transport transition are not interchangeable without an explicit theorem, model and validation. A mass-zero equation is *not itself a novel result*: disorder-renormalized Kane mass in HgCdTe was already studied.
4. **Avoid false uncertainty.** Conditional projector/tail/IEEE bounds are not HSE functional, composition, finite-size, disordered-alloy, electron-phonon or material error bars. Retained data may fail to identify missing causal moments or impurity correlations. Preserve exact mathematical NO-GO claims under their assumptions.
5. **New contribution criterion.** Compare each proposed claim against Wei & Zunger (1991), Phys. Rev. B 43, 1662, doi:10.1103/PhysRevB.43.1662; Krishtopenko, Antezza & Teppe (2022), Phys. Rev. B 106, 115203, doi:10.1103/PhysRevB.106.115203; Alowa et al. (2025), J. Phys. D 58, 135120, doi:10.1088/1361-6463/adb2a0; Lin ACE (2016), SQS (Zunger/Wei/Ferreira/Bernard 1990), and newer competing work. Relevant local files: `chemical_pbe16_p2_2026-10-15/literature_boundary.md`, `analytical_first_2026-10-11/literature.md`, `continuum_spectral_2026-10-11/literature.md`, `threshold_causal_2026-10-11/literature.md`, and `../correlated_random_mass_kane/prior_art_matrix.md`. Novelty currently **UNVERIFIED**.

## Latest zero-cost FR-VCA compatibility — 2026-10-17

Read `vca_fr_compatibility_2026-10-17/{decision.md,preregistration.json,
upf_audit.json,verification.json}`. Specific supplied Hg/Cd virtual_v2 SG15
NC/fullSO pseudo+reader GO within endpoint tests.24beta/l/j retained,
exactweightedDblocks; Cd gridtruncation and inheritedHgCHInames explicit.
Mixed radialGram healthy,not a native mixedstate certificate.5stockdry
readerchecks and4GammaPBEendpointSCFs actually passed;max44leveldiffHg
4.03e-5meV/Cd2.08e-4meV,densityGmax<8e-8e.29.73ssum/123.66MBkernelpeak,
12GiB/swap0/tasks12 hardcontrols,all9unitsunloaded;noHSE/mixedSCF/build/spend.
RawHDF5/UPFs remainprivate;Gitcontainsnativeinput/output/XML/hashes.
No implied all-k operator/material accuracy,ghost-free guarantee or physicalxc.
ExistingprimitiveHSEsymmetry1e-8FAIL unchanged;PBEstaticdiagnostic staysclosed.
Currentuserbudget$0;oldcloudplan isNOT authorization. A futureprimitiveVCA
x=.125HSE state would test coherentfractionalexternaloperator only,not local
Cdimpurity/Teenvironment/disorder. It needs separately approved matchedstate,
symmetry,coverage/resource admission. All822pins/76oldfiles/dirtyDFT preserved.
STOP this finite qualification;no automatic next calculation.

## Latest compute plan only — 2026-10-17

Read `compute_acquisition_plan_2026-10-17/decision.md`. Conditional procurement
recommendation is on-demand n2-highmem-16/128GiB,500GiB total pd-balanced,
for a fresh matched16atom x=0/.125 model at50/200/Fock200Ry,FD.001,K2/Q2,352.
Exact As=2Ap geometry folds primitiveK4 electronic rule; exchange Q4→Q2 also
needs eight reciprocal/band sectors and primitive-periodic full density.
No automatic HSE equivalence or matched-host waiver. Originale90/cold/f120
is different; old64³/22GiB buffer is not the newFFT/fullRAMcertificate.
128 is plausible,not admitted. Explicit spend/region/quota/currentprice,
model/layout/resource/stockcheckpoint approval required before paid action.
Official128price$1.048112/h;48totalVMh+250–500GiBdisk≈$51.95–53.60 beforeextras,
not runtimeforecast. No account/credentialaccess,jobs,builds,services,purchases.
All822pins/76historicalfiles/dirtyDFT unchanged. OldNO-GOs/PBEclosure/goal
untouched. STOP this finite plan; no automatically authorized next phase.

## Latest finite read-only admission decision — eight-atom152/q8, 2026-10-17

Read `hse8_152_q8_admission_2026-10-17/{decision.md,audit.json,verification.json}`.
Assignment COMPLETE: stock centered electronic2³/q2³/152 is source-compatible,
execution NO-GO under12GiB because total resident peak is not established.
Source8.405GB plus two simultaneous full spinor EXX batches2.101GB already
makes10.506GB; named nominal phase model11.231GB is NOT a peak bound.
The remaining1.654GB does not cover all unknown padding/library/cache high water
with an independent certificate. No cgroup-OOM probe is authorized or planned.

Read exact source semantics before suggesting grids: nqs=8transfers is NOT
nkqs=8stored sources on arbitrary k. Conventional centeredk4/q2 gives56sources
and58.835GB at152bands; exactfolded16electronic sampling withq2 needs16sources
and16.810GB but still changes exchange quadrature. Shiftedk2 has one irrep,
so stock forcesq1; centeredk3/q2 falls backq1. Native effective mesh must be
verified in any separately authorized run. Exact rational source replay matches
actual accepted primitivek4 metadata,not newly executed native data.

Cd atorigin in the frozen ideal8atom motif retains24Td rotations and loses
three fcc translations; do not invent lower point symmetry or force an SCF
quartet without actual density qualification.152 is legal for144electrons,
not proof of8empty states/coverage. Old Gamma labels lie below152, but old
nonstationary probe weight above152 reaches1.60e-4. Both native atomic starting
sets are152: atomic+random takes a different branch than176 and ACE span changes.
Keep old176/HSE8 failures and latest primitive strict1e-8 FAIL unchanged.

Best unadmitted candidate is a fresh matched centeredk2/q2/152 host then Cd,
with same explicit physical/solver settings; it is a new coarse ordered model,
not the primitivek4 host plus Cd. Exact-profile complete resident evidence is
missing. No queued run, new resource cap, HPC access, source/owner development,
PBE reopening or physicalxc. This phase ran ZERO native jobs/builds/services;
822pins/76originals/dirtyDFT verified unchanged. Historicalgoal untouched. STOP.

## Latest: COMPLETED primitive k4/q4 host control — 2026-10-17

Read `primitive_k4_hse_2026-10-17/decision.md` and
`final_qualification/{state_result.json,scientific_result.md,resources.json,
cleanup.json,verification.json}` FIRST. Solecase ended03:24:51UTC with
actual EXX self-consistency,6builds,dexx2.3e-10Ry,XMLtrue,lastinner3.2745e-10Ry,
total−484.161000956768Ry,Fock/2−8.96862706Ry. Stock/source/physics unchanged,
8nativeirreps/64q/Gammaweight1/64. FiniteFD.001Ry,staticlattice,e50/200/f200.

ConventionalSCF PASS/usefulconditionalhost reference; strict1e-8densityFAIL.
Untruncated44source/88QRcolumns give GammaThetaop3.615172826e-7,F8.710744260e-7,
Tdmax5.196448527e-7,not compressedwitness4.05e-11. Independent blockF,
physical Rayleigh/residual and phase invariance verified. Do NOT infer1e-8PASS
from quartet degeneracy/charge/characters or a conservative upper bound.
Only3nativeTRIMs1,3,7 allow direct-kTheta;fivegenericpartners absent;
actual native little groups checked,no generated64state/symmetricstar claim.

Original e90/f120frame transported bytrueGlabels plus24spinorcharacters
supports approximateGamma6(33–34)/Gamma8(35–38): conditionalordering
−.289586504823eV,nominalhalf−.144793252411eV,quartetspread7.75neV.
Sector amplitude errors>1e-8;fullH/eigenpair/errorbound absent. Not a strict
nonmagnetic mass certificate,positive bulk gap,zero-smearing proof or physicalxc.
Olde90coldΔ differs+.183609meV,not a material/numerical error budget.
Denserquadrature visibly stabilizes this trajectory vs oldk2/HSE8;
initialization/nonlinearbasins and jointk/qchange prevent uniquecausal proof.

Wall6622.739s,kernel6.226GB,swap0,tasks7;host/disk/output floorsheld.
Workerinvocation8dee58502fd048e4bf30a09bd9053a1f exit0,no restart/stoprequest.
Originalworker/observerPIDs/cgroupsgone,bothunitsunloaded,noactivejob.
Private root `/home/User/opencode_workspace/DFT/.local/p4_1017_013015` retained.
Current terminalcopies/hashes supersede RUNNINGstatus; priorcheckpointbytes
andverification remain unchanged. RawHDF5staysprivate,not inGit.
822pins/76originals/dirtyDFT/oldfailures/stock/PBEclosure verifiedunchanged.

STOP: no new native jobs/restarts/Cd/sourceorownerdevelopment authorized.
Future scientific input is stationary sampling-compatible Cd+matchedhost;
do not splice old8Gamma/q1chemistry into thisprimitivehost. Stock8k4/q4
nominalEXXbuffer77.86GB atretained60³/176extents exceeds12GiB.
Primitive4³ folds mathematicallyto16conventionalfibers(19.46GBnominal);
this is NOT an admitted/supported irregularq16native deck. No free launch.
Random-alloyxc still needs independent composition/configuration/observable
information. Historicalpersistentgoal BLOCKED unchanged; no novelty claim.

## Latest native primitive k2/q2 result — 2026-10-17

Read `primitive_k2_hse_2026-10-17/{decision.md,state_result.json,
resources.json,verification.json,cleanup.json}`. From53ca7b3 ONE fresh stock
primitive2atom k2/q2 FD-HSE control actually ran856.34s/16source builds,
50/200/200Ry,44/36,SG15FRNC,a6.46A,HSE.25/.106. After sustained315meV
Gamma8-character splitting, investigator requested normal native EXIT. This
was an EARLY scientific stop,not a frozen plateau trigger,600s rule,6h budget
or resource failure. It does not prove absence of a symmetric fixed point.

Total−484.060104456Ry,Fock/2−8.96881784Ry,dexx6.23e-6>1e-9,XMLfalse;
NO converged/nonmagnetic host,Cd,mass or xc. Actual density Theta opGamma.903712,
L.016914,X.013660;Td max.997426;Gamma8-character315.272meV. Charge/FD pass
and24nativecrystaloperations do not certify nonlocalD. All3actualTRIM checked
with physicalG->−G−2k.8fullBZfibers are symmetry-transported,not nativeexports;
source/exactfull-H residual is missing. No averaging/repair/old retropass.

New old-state translation bound: conventional8Gamma folds primitiveGamma+3X,
newk2adds4L. TwirlingoldD into exactprimitiveperiodicity changes it<=9.23e-6
and leavesTheta lower expression.9999785. Not a nonlinear HSE/FD update.
Coarse sampling is insufficient for this trajectory;ACE/occupation/quadrature
causality still not isolated. OnlyGamma has fractional FD occupations.

Kernelpeak1.043GB,swap0,tasks7,all floors held;ownunit unloaded,originalPIDs
andcgroupgone.822protectedpins/76oldfiles/dirtyDFT/stock/other sessions unchanged.
Prelaunchmissinguserbus andofflineXML48lattice-vs24crystalparser error retained,
fixed before native launch/within readback respectively;ONE native job,no retry.
NEXT physics input,NOT admitted/queued: primitivek4/q4 atsamee50FD law andcuts
would isolatequadrature better. Nominal5.767GBsource and~4.69h16buildFock
forecast need independentfullresource/convergenceadmission. No more owner/PBE
infrastructure;oldaccepted e90coldk4 reference does not isolatek sampling alone.
Current finite assignment COMPLETE;historicalBLOCKEDgoal untouched.

## Confirmed milestones (not claims of a physical random-alloy gap)

- **Analytical identifiability**: binary endpoints plus finite endpoint information do *not* uniquely determine interior alloy electronic structure. Symmetry-reduced causal Gamma responses require independent functions; a single ordered configuration cannot determine all environment-dependent operators. Read `analytical_first_2026-10-11`, `threshold_causal_2026-10-11`, `ordered_environment_2026-10-15`.
- **Matched PBE+SOC Cd response**: 8-atom ordered x=.25, 50/200 Ry, k3, fixed-frame Gaussian W2 **+392.177486 meV** (different cell/Brillouin sampling from 16-atom studies); 16-atom x=.125 matched pair, 50/200 Ry, Gamma, tracked ordered-cell multiplet **+169.033285 meV**, Gaussian W2 **+201.458261 meV**, causal inverse resolvent at eta=.05eV **+135.136468 meV**. These are distinct defined observables, not three gap estimates. See `chemical_k3_2026-10-14/decision.md`, `chemical_pbe16_p2_2026-10-15/decision.md`.
- **Same-composition local environment**: 16-atom x=.25 Cd(0,7) unshared vs Cd(0,1) sharing Te neighbors, matched fixed cell/PP/SCF. Sharing-minus-unshared FD free energy **-88.571432 meV/cell** in fixed PBE model; Gaussian W2 **-2.076649 meV**, sign unresolved within conditional bounds; scalar inverse response **-81.474454 meV**, conditionally negative. Gaussian central-state **-45.073266 meV** nearly canceled by weight redistribution **+42.996617 meV**. Complete 6x6 inverse-response contrast norm **82.917971 meV**, conditional fixed-frame lower bound **57.679585 meV**. Finite-eta causal responses cannot uniquely recover a static Te N2 operator. N3 Te environments still absent; random-alloy gap/x_c unknown. See `pair_environment_2026-10-15`, `environment_redistribution_2026-10-15`, `matrix_environment_2026-10-15`.
- **Matched native HSE activation**: Cd-minus-host fixed-frame HSE correction first-ACE **+44.184097 meV**, after one hybrid inner relaxation/second ACE **+39.811504 meV**; not converged HSE gap. Old 176-state ACE off-span TR action defect ~**2.8179%** and an 8-build nonmagnetic host trajectory with spurious-looking Gamma8-character spread ~**0.655 eV** prompted stop; no converged Cd counterpart. Direct Fock was TR covariant on tested inputs; new TR-space and joint Td/Theta symmetry constructions passed fixed-state tests but not a variational native-FD state. See `chemical_hse_firstace_p2_2026-10-14`, `chemical_hse_relax_2026-10-15`, `hybrid_convergence_2026-10-15`, `symmetry_constructor_2026-10-15`, `joint_symmetry_2026-10-15`.
- **Complete same-density HSE operator, then single-state 304**: `single_state304_2026-10-15/decision.md` (pushed commit **283aad5**) is the latest accepted native milestone as of this snapshot. One native 2-rank HgTe host query measured **304 basis columns + 12 controls from exactly one frozen trial state**, source/kernel/local snapshots byte-stable, Td/Theta defects around 1.7e-11, Hermiticity ~1.32e-15, wall **329.21 s**, kernel peak **5.56 GB**. It avoids a refused cross-run splice. **FD IS NOT STATIONARY**: 304 Galerkin trial density mismatch **0.00942430** (operator norm); Fermi quartet full-H residual **0.023784678 Ry** (~0.3236 eV), full commutator **0.50357023 Ry Frobenius**. Auxiliary Ritz/kinetic values are NOT new physical bands. No self-consistent HSE host, matched HSE Cd gap, physical crossing or x_c has been obtained.
- **Preserved refused work**: exact HSE cross-run append refused at `append_hamiltonian_2026-10-15` (near-roundoff changes in rho/potential/control do not permit byte-exact state splice). PBE static 6-probe operator attempt at `static_environment_2026-10-15` failed owner FD-inventory verification, despite diagnostic native output; shared configuration withheld. No historic failure was silently retried, accepted or deleted.

<!-- STOCK_HSE_STATIONARY_20261016_BEGIN -->
## TERMINAL stock HSE8 result — 2026-10-16 23:22 UTC

Read `stock_hse_stationary_2026-10-16/{decision.md,host_state_result.json,
resources.json,native_readback.json,verification.json,cleanup.json}`. The new
user allowed approximately3hour local runtime; do not call600s a universal
user limit. ONE fresh stockQE7.5 ACE host actually ran10488.530204s,79source
builds,20:21:51–23:16:39UTC. Native max_seconds10440 stopped it cleanly after
the current rebuild and saved all. Final total-1936.3410548077159Ry,
Fock/2-35.83701457Ry,dexx1.12e-6>1e-9Ry,XMLSCFfalse. OSexit0/JOBDONE
does NOT mean HSE convergence. No restart, alternative candidate or Cd run.

Actual model unchanged:8atom176spinor/144e,HSE.25/.106,50/200/Fock200Ry,
Gamma/q1,FD.001Ry,6.46A,SG15FRNC,atomic start; both live ranks matched stock
hash1d66c785... . No private source/owner/launcher changes. Full saved density
is NOT nonmagnetic: untruncated QR Theta op.999996959745/F2.00301968,
independent source/scalar witnesses agree; max24Td frame witness.99957689.
Gamma8-character spread661.215meV,Gamma6-character5.386meV; no averaging or
signed gap. Correct FD/charge(+8.17e-11e from both wave and rhoG) is insufficient.
No full-H eigenpair residual bound, stationarity, physicalx_c or Cd response.

Resource-feasible measurement: managerMemoryPeak4,224,897,024B,
sampledRSS4,290,023,424B(shared overcount),tasks7,swap0,no observedOOM/limit
events,hostavailable>=25.269GB,disk>=49.399GB,newfiles131.778MB. Unit had
12GiB/swap0/tasks12/3h limits andCPU200%/nice10. At exit the one-off sampler
failed KeyErrorControlGroup (empty property omitted); preserve this negative,
NOT full samplerPASS. Independent final manager retains same invocation,
NRestarts0/exit0/peak. All three originalPID identities gone,cgroup absent;
own transient unit now unloaded. NO ACTIVE SCIENCE JOB OR TOOL SAMPLER.

Raw root `/home/User/opencode_workspace/DFT/.local/r07stock_20261016_202059`
preserved. cfbad7d18-build ACTIVE snapshot remains immutable historical prefix;
terminal files supersede active state, not its data.822pins/76oldfiles,
dirtyDFT/stock/HSE16/other sessions/PBEclosure/blockedgoal unchanged. No retry
of this candidate. This is not proof of physical HgTe magnetism or that more
RAM would cure it. Stock direct exchange is a distinct established algorithmic
control but whole-SCF cost is unknown (79ACE builds9125s here); no new launch
or infrastructure campaign admitted. Need a genuinely stationary symmetry-
qualified HSE host before Cd; ACE versus finiteGamma instability remains OPEN.
Current finite assignment STOPPED after actual numerical negative result.
<!-- STOCK_HSE_STATIONARY_20261016_END -->

<!-- HSE_PAIR_ADMISSION_20261016_BEGIN -->
## Latest: stationary matched HSE8 pre-execution NO-GO — 2026-10-16 19:53 UTC

Read `hse_pair_admission_2026-10-16/{decision.md,audit.json,verification.json}`.
From bd71dea, ONE bounded source/native-archive assessment is COMPLETE. Zero
native executions/services/builds/new runners; no pending job or retry. Stock
QE7.5 exists (hash1d66c785...), direct exchange ace=false is source-supported.
The exact intended matched8atom model is confirmed from native XML/PP/input:
Hg4Te4 vsCdHg3Te4,176spinors/144e,6.46A,SG15 FR NC,50/200/200Ry,Gamma/q1,
FD.001Ry,HSE(.25,.106),same original physically embedded six-probe frame.
It does NOT provide a stationary material state or input potential.

First concrete blocker: audited fixed HSE8 owner pins an already-used two-build
diagnostic ELF/root; native code deliberately returns conv_elec=false. The
ordinary DFT runner lacks the required kernel/resource/output contract. Stock
direct fullSCF has no independently qualified exact fresh-profile launch,
resource/time/readback/restart path under current12GiB/swap0/tasks12/600s,
host4GiB/disk10GiB/output14GiB limits. No new owner or solver may be built as
part of this completed scope. PBE static diagnostic remains permanently CLOSED.

Old finite two-build host/Cd wall410.333/409.315s, kernel4.549/4.542GB;
both dexx~.0025Ry. Rejected eight-build host1628.053s, dexx1.804e-6Ry,
Theta witness.999765 and quartet.655255eV remains rejected. No extrapolation
or restored nonmagnetism; Cd from that trajectory was withheld. Stock direct
EXX buffer1.216512GB and selected payload1.594966GB are NOT complete peak.
Current host RAM/disk floors pass; full direct-SCF peak/time/output unknown.
This is neither proof of hardware impossibility nor of direct exchange cure.

Next actual science deliverable requires an independently qualified stationary
matched HSE material packet from established native production: rebuilt same-D
H,FD charge/entropy,eigenpair+occupied residuals,actual symmetry and Gamma frame,
convergence/resource evidence. Existing primitivee90 cold numerical SCFs remain
accepted in their own domain; they are not e50FD substitutions. Conventional
numerical SCF convergence is useful without a universal proof, but absent here.
Only after stationary host may same-domain Cd be released; ordered0/.25 is not
random-alloyxc.822protected pins/76historical files/DFTdirty/oldPBE refusals and
blocked goal are unchanged. STOP; no queued work/infrastructure continuation.
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

<!-- PBE_DENSITY_ONLY_FEASIBILITY_20261016_BEGIN -->
## Latest density-only PBE path assessment — 2026-10-16 17:35 UTC

From9a7dafa: read `pbe_density_only_feasibility_2026-10-16/{decision.md,
preferred_path.md,acceptance_and_policy.md,audit_result.json,verification.json}`.
Non-executing phase COMPLETE: conditional scientific design GO, execution NO-GO.
ONE preferred NEW QE-linked postprocessor: needwf variable false on entry to
read_file_new; post_xml_init rebuilds saved scalar-density PBE/ionic/NC-SOC,
then explicit set_vrs and k/beta/probe-only setup for h_psi. No full init_run,
wfcinit/openfil/electrons/read_collected_wfc needed. Keep352 XML band metadata;
no352-band solve/load/evc is physically required for this static NC-PBE query.
Actual UPFs have no NLCC/US/PAW; full relativistic projectors remain essential.
Retain original50/200Ry cell/PP/rho/spin frame,6+6Theta per member=24pair actions.

Input charge errors<=1.004e-10e; actual-density direct Fourier/FFT check<=5.60e-16.
New rank1 G/FFT/packet reader needed, no naive reuse of two-rank headers/ELF.
Selected439.69MB allocations NOT a total bound. No actual H actions, static
chemical number,2meV certificate, build, service, native MPI or DFT write.
read_file_new overwrites needwf; missing set_vrs and stop_run file side effects
must be addressed explicitly. QE pp_example is a pattern, not a SOC-safe driver.

Singleton MPI/no helper and kernel write/network containment are NOT proved.
Read-only Landlock VERSION returned ABI7; no ruleset/mount enforcement applied.
Separate prospective policy must prove staged RO inputs, finite scoped outputs,
closed inherited write paths, all helper/shm/stdio/outside-reader bounds and
terminal ownership under12GiB/swap0/tasks12/600s and original floors/budget.
No profile/nonce/ELF release or generic owner continuation authorized. Gate A
refusal remains immutable and cannot be bypassed by the one-rank proposal.
Independent evaluator is higher-cost; two-rank fallback only after actual
one-rank scientific-equivalence failure AND new review, never automatic.
Static A/B still do not determine QHQ/N2/ensemble mass/gap/x_c. Registry/goal
unchanged. STOP at separate implementation/admission authorization boundary;
all prior handoff text is preserved exactly below.
<!-- PBE_DENSITY_ONLY_FEASIBILITY_20261016_END -->

<!-- PBE_STATIC_LIFECYCLE_20261016_BEGIN -->
## Latest Gate A lifecycle-only actual attempt — 2026-10-16 14:35 UTC

From9f59814: read `pbe_static_lifecycle_2026-10-16/{decision.md,
preregistration.md,commands_and_boundary.md,verification.json}` FIRST.
Finite user-authorized phase COMPLETE: **NO-GO / STOP**, not Gate B release.
New isolated R07L/scope1601 NON_SCIENCE MPI C harness built and frozen. Real
production-derived owner.run created one systemd local two-rank launcher unit
with actual12GiB/swap0/tasks12/600s. At startup `/proc/1978386/fd/9` vanished
inside strict Account.sample; incomplete/unknown live-final-pair refusal after
0.202116s. ZERO authenticated begins/finals, packets or collective results.
Do not claim actual two-world-rank qualification from command intent.
Conditional missing-final negative NOT RUN; no retry or replacement identity.

Actual terminal manager peak2,789,376B; sampled holderRSS24,408,064B. These
are startup observations only. Known actor pidfds dead, managerfailed/exit1,
foreground wait1 and original empty/absent cgroup checked; immutable RESULT
REFUSED, no OUTSIDE_FINAL/science release. Cleanup's rank-exit field is vacuous
with no ranks; no false rank proof. pw.out empty; exact initial ENOENT in tool
traceback is archived as an explicitly transcribed excerpt. No assumption
whether fdclose or taskexit caused disappearance; never silently skip it.

Old PBE implementation/source/refusals,126profile/14raw pins, stockQE/dirtyDFT/
historical ledger verified unchanged. No QE/HSE/SCF/saved-density action, hostwide
inventory, private-netns proof, original HSE16 or goal/session change. Gate A
full lifecycle and Gate B/backend/2meV qualification remain BLOCKED. No physical
mass/gap/x_c or registry promotion. A future live attempt requires new explicit
scope plus a tested bootstrap FD-lifetime/accounting solution; do not rerun this
unit/root/lease or launch a science member. All older handoff text preserved.
<!-- PBE_STATIC_LIFECYCLE_20261016_END -->

<!-- PBE_STATIC_COMPLETION_20261016_BEGIN -->
## Latest PBE native completion — 2026-10-16

From37f48db: read `pbe_static_completion_2026-10-16/{decision.md,acceptance.md,
build_result.json,component_results.json,resource_audit.json,verification.json}`.
New actual QE-linked PBE-only R07S/scope16 final hook exists in private MCT
scratch: begin before init, checked packet flush/close + barrier, live final,
world error normalization/barrier, return before electrons/punch. Stock
physics objects unchanged. Native ELF NEVER executed; no new MPI/SCF/action,
service/member, DFT/source write, old refusal reclassification or HSE work.

Production dispatcher/account/reader source uses actual kernel peers and a
fresh scope, no wrapper/inherited-socket self identity. Actual NON-MPI C clients
exercise it, including fatal liveEACCES, wrong/early/lost finals, incomplete
packet, failed reader/import, descriptor reuse, output burst and lost log.
Terminal manager/cgroup and positive tiny reader were MOCKED; native reader
rejects the fixture. Do NOT call these components full production qualified.

Native owner.run/actual systemd/MPI collectives, safe setup/cancel/crash, complete
12GiB/backend/outside-holder resource and2meV numerical error qualification
remain BLOCKED. Source loader/CLI prohibit native release. Scope-local pending
latch preserves unknown cleanup; protected old ledger is never rewritten.
Resource metadata are source-selected terms, not1GiB/4s forecast converted
to a bound. No pair/job/queue/restart is created. Stop at this explicit native
qualification/resource boundary; a future one-member live resource query
requires separately reviewed protocol/authorization and no automatic Cd/shared
release. Exact6+6Theta/member,24total and original24/4 subgroups/physical
contract remain. No gap, N2, linewidth/EBS, random alloy or x_c claim; registry
status and all old handoff below unchanged.
<!-- PBE_STATIC_COMPLETION_20261016_END -->

<!-- PBE_STATIC_ADMISSION_20261016_BEGIN -->
## Latest PBE static environment admission — 2026-10-16

Fromfdc1b02: read `pbe_static_admission_2026-10-16/{decision.md,
observable_contract.md,owner_import_acceptance.md,verification.json}` FIRST.
Read-only phase COMPLETE; scientific static-observable GO, native pair NO-GO.
No new native action/SCF/MPI/build/service or protected DFT write. All126 old
profile pins/14 refused raw pins checked; no old result is retrospectively PASS.

Exact original50Ry host frame has6Theta residual singular directions>1e-8,
so primary12actions across BOTH arrangements require12extraTheta controls:
24total. Do not replace the frame or force Td/quartet on the4-operation shared
cell. Scalar saved PBE densities pass their actual24/4 groups. Static A/B and
trace contrast are new potential observables, not the old own-EF inverses or
physical mass/gap. Common scalar requires an independently checked energy
gauge; trace/complement are scalar-shift invariant. N2/QHQ/random-alloy x_c
remain unidentifiable. Prospective2meV numerical budget is not achieved.

Importer preflight now passes with explicit pinned dependency and negative
tests. Kernel-only small NON-MPI children prove liveEACCES refuses, real dead
rank can only enterPENDING, fake/wrong/incomplete identities refuse. Terminal
manager/cgroup cases were INJECTED, not a new service/native owner acceptance.
The pinned PBE ELF has NO live native final hook and owner has NO retirement
caller. Complete12GiB/600s/14GiB resource envelope remains unqualified. Stop
here; only new scoped private integration/qualification could permit a future
separately authorized fresh pair. No unchanged HSE or generic infrastructure
continuation is requested. Historical goal/registry status and all old handoff
content below are unchanged.
<!-- PBE_STATIC_ADMISSION_20261016_END -->

<!-- STATE_UPDATE_20261016_BEGIN -->
## Latest nonmagnetic state-update qualification — 2026-10-16

Frombe13479: read `state_update_2026-10-16/{decision.md,next_input.md,theory.md,
handoff_ledger.md}` and verification before another native proposal. Known
FD304 is now an actual176-capacity source INITIAL GUESS with full nonlocal
Theta upper6.98e-12/all96host-space operations<7.77e-12,144e, independent4spin
FFT density and bitwise actual2rank-G transport. It is NOT a native FD solution,
SCF checkpoint or a reinterpretation of any old failed state. No twirling/level
averaging. Actual species subgroup:96host,24Cd; this Cd keeps Td but loses fcc
translations. Never impose host symmetry on arbitrary Cd configurations.

New conditional necessary uniform-H correction709.1054meV for D1 stationarity
is NOT a projected chemical error. Local nonlinear feedback/stability remain
unknown; a defined<=2meV chemical budget is not achieved. Existing qualified
reader enforces old fixed occupations and returns before occupied solve, so D1 is REFUSED at
that source interface. A relaxed equality check would not implement SCF.
The original profile pins D0 bytes; the weight predicate alone does not specify
its orbitals. This is an executable-contract boundary, not an impossibility proof.

ONE next-input protocol: direct-Fock full-space occupied solve initialized by
the new trial, controlled omitted occupation/FD/nonlocal symmetry, THEN same-D
native density/local-XC/Fock rebuild and full-H stationary/readback checks.
Offline codec/complete small nonlinear logic tested; native implementation,
complete resource and owner admission NOT established. No service/MPI/QE/build,
DFT write or Cd attempted. Do not rerun old176ACE or304 actions to substitute
for the missing solve. Physical gap/x_c and screened chemistry remain OPEN.
Historical goal and registry status unchanged; all earlier handoff preserved.
<!-- STATE_UPDATE_20261016_END -->

## Latest frozen-response Theta decomposition COMPLETE — 2026-10-16

From4cfc16b: read `theta_response_2026-10-16/{decision.md,theory.md,
source_norm_certificate.md,handoff_ledger.md}`, result/verification and table.
Distinct actual-data result: the95.54meV chemical leakage survives Theta-even
projection. Updated even Q norm95.4618–95.5739meV, odd.2198–.3320meV;
all even singular values>91.5138meV. Updated odd trace magnitude<1.12e-8meV
under the stated source assumptions, leaving the finite+39.8115meV trace even
to that precision. These are NOT stationary/material error bars.

Original six-frame closure1.286399e-7 fails1e-8. Exact six-column reconstruction
is therefore NO-GO, not a new PASS. A gauge-covariant Hermitian representative
retains unknown QQ completion in rigorous conditional interval formulas.
Finite-grid norm32Ry/member,64Ry/chemical is source conditioned: original native
kernel multipliers were not captured. Do not present centres as unique physical
operators, pretend exact W closure or discard the QQ uncertainty.

Full actual density defects now available: host second.001428208op/.004040264F,
initial Cd5.99595e-7op. Old compressed witnesses were lower and are preserved.
All sources remain strict1e-8 TR-unqualified. Zero local spin/Theta-even frozen
action is not self-consistency or cubic Td. Nonlinear-XC averaging has a possible
consistent already-even local-density exception, but no FD state is certified.
Unknown even feedback needs a bounded Hessian and inverse FD response/Jacobian.
Minimum next physical input is unchanged: qualified matched same-state full-H
six-probe screened response/state residual, not another unchanged HSE or extra
ThetaR-only job. No native/source/build/DFT write, optical search, goal/session,
registry-status or historical refusal change. STOP; all old handoff remains.

## Latest science-first screening feasibility COMPLETE — 2026-10-16

From5dc77a9: read `screening_feasibility_2026-10-16/{decision.md,theory.md,
minimum_input.md,handoff_ledger.md}` and real/independent checks. NO new native
job is admitted.32 original matched HSE packets give new full-action results:
updated chemical activation trace+39.811504meV, positive compressed-sector
Rayleigh differences39.591459–40.032986meV, but Q-action norm95.541080meV and
smallest singular91.550099meV. A closed six-state activation operator is
falsified; this is not a measured self-energy/gap error or a material mass.

Actual matched host density Theta lower witnesses3.27666e-7/0.001395756895
and second Cd4.01839e-7 disqualify strict1e-8 nonmagnetic continuation even
before another unchanged176-source build. Independent native scalar checks
confirm them. Preserve the accepted finite+44.184097→+39.811504meV observation;
no historical acquisition or failed trajectory is reclassified.

Source audit adds an independent B obstruction: full352-band stream generation
22GiB exceeds14GiB tracked-output cap despite2.75GiB resident plane. Present
disk availability does not override this. Original16atom stock memory,
wholeSCF/restart, primitive cold/e50 FD transfer and all old refusals remain.
No q is measured: conditional geometric sign factors.90103694/.51249540 and
sharp projected sign radius19.905752meV only describe missing certificates.
One future input is a qualified same-state matched full-H six-probe screened
remainder, not another unchanged outer step or H304 trial. State bridge is
not launch-ready. STOP at this honest boundary; no optical/native/build/source
change, sessions, goal or material x_c. All earlier handoff content is retained.

## Latest original-host reuse audit COMPLETE — 2026-10-16

Read `stationary_reference_audit_2026-10-16/{decision.md,qualification_and_resources.md,
theory_and_contract.md,minimum_input.md,handoff_ledger.md}` and native/independent
checks. From9a83424, original e90 k4/q4 f120/f360 HgTe SCF states survive; their
SCF XML matches earlier expansion-parent pins. Numerical host frames and source
states are reusable as references/initial states, so additional H304[D0] columns
are not needed to find a numerical host. This is new full-source/occupation
qualification beyond P1; old SCF acceptance remains intact.

Strict FD/direct-H transfer is NOT qualified: native cold occupations produce
Gamma cubic density witnesses~1e-6; saved ACE six-probe defects~1e-8–1e-7;
full-H residual/stability and source-kernel replay remain unbounded. FD roots
of stored spectra are only reinterpretations, not nonlinear H[D_new] updates.
e50/Γ-only model and e90 k4/q4 state differ in frame, quadrature and occupation
law. No primitive small defect is relabelled as the old severe broken host.
No same-D byte-replay PASS: original/export coefficient roundoff is retained.

Original16atom stock nominal EXX buffer22GiB fails12GiB admission independently
of H304's unrelated5.56GB peak. Primitive f120 subtotal2.75GiB suggests a future
same-state residual candidate, but complete two-rank RAM/time/output/state
qualification is absent. Both archived open_grid logs show54³ FFT even for
f120 (temporary4*ecutwfc); a new export also carries13.21GiB nominal buffer.
Reuse the existing exports, not a new postprocessor. No native run is authorized
here. The indispensable
chemistry is aligned self-consistent Cd-screened H[D_c], not another host
interpolation or fixed-D ionic shift. Further alloy/material/continuum/root
inputs remain. STOP at that precise boundary; no new optical search, synthetic
mass example, DFT command/write, H304 action, goal/session or old-gate change.
All previous handoff content below is preserved. Read the new decision before
proposing any next computation; do not promise a cheap SCF or material x_c.

## Latest finite public optical intake COMPLETE — 2026-10-15

From clean pushed 4affbd8: `public_optical_intake_2026-10-15/decision.md`,
`availability_matrix.md`, `sources.json`, `three_field_test.md`, `draft_request.md`
and verification record the new bounded search. Both publisher-linked supplements
were freshly read; eight targeted queries plus linked institutional routes found
no complete publicly accessible raw/polarization/calibration/independent-assay
three-field HgCdTe package. Teppe S5 is a plotted 77 K series, not raw low-T records;
supporting data remain offered on request. HAL/API access was incomplete, so do
not call those file inventories empty. Local fitted/figure/calculated summaries
remain excluded. This is an availability boundary, not global nonexistence.

STOP with a precise UNSENT sample-A request to Teppe's publication correspondence
address; current mailbox, raw retention/rights and sample-assay mapping unconfirmed.
No outreach, native job, new spectrum/model calculation or historical-goal change.
Preserve the older Stage0 pair NO-GO and unsent Guldner draft. Qualified records
could test the operational Kane adapter using held-out B3; still no microscopic
mean/disorder determination or physical zero-T x_c. Do not repeat broad searches
without a concrete new source lead. All earlier handoff content below is retained.

## Latest competing-route phase COMPLETE — 2026-10-15 21:34 UTC

New assignment fromc80147f completed three analytical-only milestones in
`competing_inversion_routes_2026-10-15/`. Read its `decision.md`,
`comparison_and_phase_boundary.md`, `one_next_input.md`, `verification.json`
and `handoff_ledger.md` first. Milestones4462514/c2ba548 published en route;
completion commit is in the latest Git log. No native job or physical x_c.

RouteA now distinguishes actual local-site Td from ensemble symmetry: a
fixed Bernoulli directional pair interaction has zero coherent cross-irrep
mean but a positive Gamma6-HH constant Born covariance. The p formula needs
nonzero angular norm, positive uniform curvature and a controlled continuum
limit; exact flatness/nonanalytic vertices/warping can defeat a naive exponent.
Born is not exact eliminated response. Exact sqrt-threshold normalization can
lose its atom below an O(c^2) scale while finiteeta looks pole-like.

RouteB gives a meaningful conditional signed optical Kane witnessQ/(2D) from
one HH family at two fields, with an independent third-field/error test and
no atom premise. A symmetric zero-mean mass mixture gives positive optical
bias even with ACTUAL circular-current weights. [H,.] removes global scalar
disorder at canonical filling; an exact-G counterexample proves optical
vertex/source information is still needed. A source-resolved second-order
contraction can suffice with explicit errors; it is a function, not a fitted
constant. No real-mass/topology/mobility equivalence is assumed.

ONE next input is a calibrated three-field one-specimen transitionresponse
to discriminate the observation adapter. It is not an empirical microscopic
coefficient or a substitute for the failed Stage0 endpoint-pair pilot. Raw
records/calibration are not currently accessible. Earlier IR certificate is
conditionally deprioritized for routeB, but remains decisive for routeA.
Stop at this genuine data/physical-source boundary; no new job/outreach/goal
resume. Keep prior H304 nonstationarity, N3 and all old mathematical/native
refusals intact. Broad Kane/SCBA/optical/environment principles are established;
specific synthesis novelty UNVERIFIED. R02/R05 remain unchanged.

## Previous completed analytical phase — 2026-10-15 20:51 UTC

User's NEW no-native assignment starts89ef0f1. Three phases in
`physical_inversion_2026-10-15/` are now COMPLETE. Read `decision.md`,
`discovery_registry.md`, `verification.json` and `handoff_ledger.md` first.
Accounting3d8af76 and sharp-atom certificate92051fd were published en route;
consult latest Git log for completion commit. Physical prediction is NO-GO:
missing qualified state/alloy functions, sharp eligibility and transversality.

Exact mean/disorder split must be Schur-projected consistently; its chemical
difference need not retain causal sign. Aligned scalar/mass cross correlation
matters; two contractions suffice only for fixed-Gc diagonal second-Born traces,
not full SCBA. If a true atom has Z>=3/4, its finite-eta inverse root lies within
2(1-Z)eta/Z without D. A positive eliminated threshold power p<=1 can exclude
the atom even with zero real inverse/zero damping. All constants are conditional;
none is a material measurement or physical mass/x_c. N2 is measured, N3 still
invisible. Preserve prior same-IR/different-root and other no-go theorems.

ONE recommended future input is the controlled physical Gamma8/heavy-hole
infrared weight in the intended crossing domain, with stationary source and
bounded adapter from any impurity/model data. It can choose/falsify the sharp
observable route, not determine x_c alone. No new native job, outreach, actual
cost bound or resumed historical goal. STOP at this physical-information boundary
until new input or a genuinely distinct theorem is available. Historical dated
snapshots below do not supersede this completed phase.

## Latest in-flight/unfinished work at time of writing

**Completion update — 2026-10-15 19:22 UTC, original session resumed:** the
previously untracked `hse_residual_response_2026-10-15/` has now been audited,
independently checked and prepared as a scoped accepted READ-ONLY milestone.
Consult its `decision.md`, `verification.json`, `minimum_input.md` and reset
ledger; the dated unfinished snapshot below is historical. No further native
job was launched. Gap-free residual bounds give conditionally negative broad
finite-resolution inverseordering, not a physical inversionmass/gap/xc.
Actionerror allowance is explicitly unproved as an interval enclosure. Original
P leakage and true nativeHP matter:4moment shortcut refused; first2moments and
boundedthird only. FD304 remains nonstationary (conditionalerrorlower1.31e-7);
noHSESCF/Cdrelease. The19b6679guardrails, oldFAILs and native283aad5 remain intact.

At snapshot 2026-10-15 16:42 UTC the research branch points to **283aad5** on `research/hgcdte-impurity-tmatrix-20261010`, pushed to GitHub. The worktree also contains a **separate UNTRACKED** `research/programs/microscopic_bandgap/hse_residual_response_2026-10-15/` directory from Codex's interrupted read-only resolvent/moment analysis. **Preserve it. Do not stage, edit, erase or claim it accepted until the original work has been audited and independently checked.** The original Gamma reference has an estimated ~5.8e-7 component outside H304, so do not assert spectral moments beyond what actual full-H actions and explicit leakage bounds determine.

The `research` tmux session was **idle due to model five-hour usage limit** when this handoff was created. No current native MPI family was seen. Usage state may change; verify live before sending any prompt. Do not replace Codex's in-flight session with a new, unrelated program.

## Scientific next steps (ranked; only after reviewing current state)

1. **Completed:** the residual/moment audit89ef0f1 and the new analytical physical-inversion package are accepted in their explicit conditional domains. Do not redo them or relabel their observables as physical mass.
2. **Cross-route physics input:** the analytical framework and competing sharp/optical criteria are now defined/tested under assumptions. Follow the latest package's ONE-input decision; do not repeat the derivations or treat an optical/finite-eta zero as a physical/topological x_c. Actual raw response or independently qualified microscopic source/disorder data are still missing.
3. **Self-consistent HSE only if decision-changing**: H304 reveals that projecting into larger finite subspace does not make the trial FD stationary. The missing scientific inputs are occupied-state full-H relaxation/complement-tail control and nonlinear SAME-D1 H[D1] consistency; formulate the smallest justified native experiment *if* it would resolve an explicit inversion-theory unknown. Do not rerun known symmetry-defective ACE or claim fixed-state H304 as a converged HSE gap.
4. **Independent alloy statistics**: N3-bearing and N3-free same-composition controls, cluster response operators, finite-size and disorder-distribution identification require new physical data and valid reference gauges. Additional small-supercell spectra alone may be prior-art repetition and are not automatically high priority.
5. **Validation**: only after the inversion criterion is defined, compare predicted mass/crossing and uncertainty to established first-principles, Kane/SCBA and experimentally justified magneto-optical/optical probes. No manuscript or novelty status is yet authorized.

## Successor's first actions

1. `cd /home/User/repos/MCT-research`; read `AGENTS.md`, this handoff, the first ~100 lines of `research/programs/microscopic_bandgap/state.md`, `research/contribution_registry.md`, and the latest decision/verification files.
2. Run `git status --short --branch`, `git log -5 --oneline`, and check `origin/research/hgcdte-impurity-tmatrix-20261010`; inspect `tmux capture-pane -pt research -S -80` and owned native processes. **Do not assume that a dated snapshot describes the live task.**
3. Read the latest `competing_inversion_routes_2026-10-15/decision.md`, then the accepted physical-inversion/residual packages. The older uncommitted-work warning is historical, superseded by verified completion; all material limitations and original native refusals remain.
4. Respect dedicated repo portfolio programs R01-R06, other tmux sessions, old failed/accepted outputs, private DFT worktree, stock QE and the original16atom352band HSE target.
5. Every next milestone must answer: **which new physical prediction or theoretical criterion became possible, and does it materially advance signed inversion gap/x_c?** Record assumptions, closest prior art, exact derivation/native provenance, quantitative numerical/material uncertainty, falsification, NO-GO and proof of what is still missing. Commit/push validated work only to existing research branch.

## Operating constraints and data integrity

- Only one owned MPI native family at a time, with independent source/PP/ELF hashes, owner/FD inventory and terminal process proofs, and true physical/charge/symmetry gate checks; use fresh short Unix sockets. Last successful H304 used a 12 GiB memory cgroup, zero cgroup swap, tasks<=12, <=600s wall and host RAM/disk floors >=4GiB/10GiB, sampled output<=14GiB. Limits are per-protocol; inspect measured resource forecasts before any new run. No unlimited jobs, retries or automatic policy relaxations.
- A failure is a scientific/numerical outcome; freeze original logs and source before any prospective NEW protocol. Do not retrospectively soften exact byte replay or owner gates.
- Private raw native packets live under authorized VPS DFT workspaces with hashes in the repo, not necessarily on GitHub. No credential changes, forced Git pushes, main merges, deletion/cleanup of old packets, purchases or interference with Calcura.
- The repository is a **research portfolio**; R07 does not override other programs. Historical physical objective remains OPEN until actually demonstrated. Keep `state.md` and `research/contribution_registry.md` truthful.

**Single-sentence compass**: Explain and predict HgCdTe's *physical zero-temperature signed Gamma6/Gamma8 inversion and x_c* from independently justified microscopic chemical and disorder physics—not from fitted gap coefficients, finite-size spectral proxies, or accumulation of simulations.
