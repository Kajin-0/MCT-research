# RUNNING: one stock HSE+SOC VCA xCd=.125 calculation

Launched2026-10-17; baseline6101a6e. User explicitly approved this sole zero-cost
local scientific case. **RUNNING, not a converged/material result.** One ancillary
nstep0 HSE reader check passed (exit0,36e,24beta,SOC), then ONE fresh SCF started.
No restart/retry/second composition or paid action authorized.

Root: `/home/User/opencode_workspace/DFT/.local/r07_vca_x0125_hse_20261017`. Worker `r07-vca0125-hse-20261017.service`; observer `r07-vca0125-hse-20261017-observe.service`.
Initial mainPID2012295, actual stock pw.x ranks2012299/2012300; observer2012292.
Invocation6937cb9475e54888b5cba081bf954210. Native output `pw.out`; observer
`resource_samples.jsonl`, `science_progress.json`, `observer.err`; final native
save will be `out/r07pk4.save`. Standard systemd user ownership persists after
Codex returns. Never restart an existing unit or call initial output final.

Exact successful primitive host input copied, changing only new private
paths/cation PP filename. Hg species label remains a placeholder; UPF element
Xx,20valence,24FRbeta is .875Hg+.125Cd, verified D blocks/hash. Same2atom
fcc6.46Å,36e/44spinors,HSE(.25,.106),50/200/Fock200Ry,FD.001Ry,k4/q4,
stockACE,adaptive_thr=false,conv_thr1e-9,Davidsonfullacc,mixing.3,atomic+random.
[Preregistration](preregistration.json) freezes input/source/PP/ELF/observer
hashes BEFORE launch. Original host input/saves and failures are untouched.

Actual worker guards12GiB,swap0,tasks12,CPU200%,24h;native max_seconds82800.
Existing observer copied BYTE-IDENTICALLY, worker BindsTo observer; samples
hostRAM>=4GiB,disk>=10GiB,owned output<=14GiB every30s. Output is sampled,
not an adversarial continuous quota. Retain the original >=12build/last3
split>.2eV+FD asymmetry+no residual improvement EXIT guideline, top-band stop,
and 16MiB printed-log safety limit. Printed indices are provisional labels;
final Gamma6/8 requires G-labelled physical projections and full-density
Theta/Td at UNCHANGED1e-8. Conventional SCF and strict symmetry are distinct.
Temporary short path `.local/v125t_1017` is a fresh symlink into THIS root/tmp,
so MPI runtime files remain in tracked owned physical scratch. No new launcher,
owner,exchange implementation,source build or framework.

See [dry result](dry_result.json),[launch argv](launch.json),[running checkpoint](running_checkpoint.json)
and [live observer properties](observer_effective_properties.txt). The template
observer_props field in launch.json retains original paths; actual observer_argv
and live readback are authoritative, as [explicitly noted](launch_record_note.json).
822protected pins,76historical files,DFTdirty bytes and stock/backends verified
unchanged after launch. No hostwide foreign-MPI absence claim or old Gate A PASS.

This is a specified primitive coherent external-potential VCA approximation,
NOT an impurity/supercell/random-alloy result. HSE stationary occupations,
SCF/eigenpair evidence,full-BZ/sector symmetry and composition response await
completion/readback. Old host conditional ordering-.289586504823eV and strict
symmetryFAIL remain unchanged. No physicalxc,zero-smearing or material-error claim.

Next continuation: inspect SAME unit/output/observer, preserve terminal evidence,
then perform read-only final projections/charge/symmetry qualification. No second
native job or automatic continuation. If observer/resource/science refusal occurs,
preserve it and stop this trajectory. Historical blocked goal unchanged.


## Terminal verification update — 2026-10-17

**COMPLETED numerical HSE+SOC**, superseding the RUNNING status above (original launch evidence preserved). Native `pw.out` reports final `!! total energy = -484.01592595 Ry`, 6 source builds, last `est. exchange err (dexx) = 3.5E-10 Ry`, `EXX self-consistency reached`, and `JOB DONE.` Native saved XML reports SCF true (1.681808213917471E-10 Ry). The final observer records worker exit status 0, NRestarts 0, memory peak 6,217,211,904 B (below 12 GiB), and no scientific stop request. Original stderr retains IEEE underflow/denormal notices. Eight HDF5 wavefunction sets, eight ACE sets, density and XML are retained privately. Details/hashes: [completed native checkpoint](completed_native_checkpoint.json).

**NOT ACCEPTED YET:** G-labelled physical Γ6 doublet/Γ8 quartet symmetry projections; full-density time reversal and Td at the unchanged 1e-8 gate; independently certified HSE eigenpair residual/uncertainty; signed half-gap `m=(EΓ6-EΓ8)/2`; physical random-alloy transition `x_c`. Index-based candidate degeneracy and near-half FD occupations are not symmetry certification. Keep HgTe host strict symmetry FAIL. This run alone cannot identify alloy-disorder response.

**Next falsifiable gate:** read-only state analysis must either validate the Γ representations and strict density symmetry to support a conditional VCA half-gap, or report the exact failure metric and refuse a qualified mass. Do not restart, rerun, launch another composition, purchase compute, modify stock/dirty DFT, or silently symmetrize the density.


## Read-only Gamma density audit — 2026-10-17

[Script](postprocess/read_only_gamma.py) and [measured results](postprocess/gamma_density_results.json) use the established host full-finite-rank density QR and G-labelled transformations, applied directly to the saved native x=.125 spinors. **STRICT 1e-8 SYMMETRY FAIL**: Gamma full-density time-reversal operator defect 3.95518494693e-7 (Frobenius 8.86298082304e-7), and maximum 24-operation Td defect 4.95143773706e-7. All 88 QR columns retained; independent extremal direct-action residual 1.5152e-15. No density repair or acceptance-threshold change.

The **provisional printed-index** 33–34 versus 35–38 signed ordering is -0.0987879687199 eV, half -0.04939398435995 eV. THESE ARE NOT certified Gamma6/Gamma8 sectors: physical virtual-cation spinor projector/character association has not been completed. Do not promote to m_VCA, error bound, bulk gap or x_c. Existing HgTe host strict symmetry FAIL independently persists. Next falsifiable question is whether reference-frame physical Gamma6/Gamma8 projections and characters agree with this provisional indexing; strict density gate still fails regardless. No additional native job authorized.


## Native spinor reference-frame projection — 2026-10-17

[Read-only script](postprocess/reference_projection.py) and [numeric evidence](postprocess/reference_projection_results.json) G-map the previously reviewed e90/f120 HgTe reference spinors into the native xCd=.125 e50 basis without renormalizing omitted tails. Same cell/origin/axes, different cation pseudopotential and chemical composition; reference character association is **conditional**, not exact operator identity. All24 native crystal operations were tested. The Γ6-like doublet selects bands 33–34, reference weights .999809663 and min singular .999904827; Γ8-like quartet selects35–38, weights .999854314 and min singular .999927154. Max Td trace character errors 1.12953e-13 / 3.60008e-14 support the intended representation association. Strict amplitudes still fail: Γ6 Td4.91600e-7/Theta3.89800e-7, Γ8 Td2.90744e-7/Theta2.47127e-7, while the already established full-density Theta3.95518e-7/Td4.95144e-7 both exceed frozen1e-8. Trace agreement is not an amplitude certificate.

Conditional Γ6-like minus Γ8-like ordering=-98.7879687199 meV; **candidate half-ordering=-49.39398436 meV**, versus previous HgTe conditional half -144.7932524115 meV, nominal difference +95.39926805 meV. This is neither a strict nonmagnetic HSE mass certificate nor a physical random-alloy interpolation or x_c. Do not assign error bars from projector singular values or smearing. No new QE job, symmetrization, repeat, or additional spending. Next falsification target: independent physical projector/character checks and full-H eigenpair residual or a justified analysis of the 1e-8 symmetry defect; no further native launch authorized.


## Revised literature boundary — 2026-10-17

See [R07 prior-art priority](../prior_art_priority_2026-10-17.md). Nicklas and Wilkins (2011) already predicted HSE/SQS x_c around 0.17, excluding generic HSE crossover prediction as novel. The future research question is a nonempirical coherent-VCA-versus-disordered-alloy distinction, not an interpolation or rebranding of the current strict-symmetry-failing VCA candidate. No additional native calculation approved.


## Primary-method audit follow-up — 2026-10-17

Read [three-paper method/identifiability audit](../three_paper_method_audit_2026-10-17.md). Existing HSE SQS x_c and SCBA disorder mass prior art constrain novelty; published x=.125 SQS mostly coherent near Gamma makes testing/limiting VCA error more defensible than asserting a large shift. Same-Hamiltonian unfolded spectral/projection and disorder covariance data missing. Existing 1e-8 density symmetry FAIL and zero-cost/no-new-run gate unchanged.


## Public SQS input availability gate — 2026-10-17

[Matched comparison decision](../vca_atomistic_data_gate_2026-10-17.md): Wang 2019 public Figure 5 x=.125 EBS is open, but no raw coordinates, numeric unfolding weights or projection-resolved Gamma spectra were located; negative search result is not proof of nonexistence. Wang HgCdTe functional is LDA+U(Ud=10 eV), not our HSE, hence cross-paper subtraction does not isolate a disorder correction. Strict 1e-8 VCA density symmetry FAIL and no-new-job/bash policy persist. Quantitative comparison NO-GO until numerical inputs and same-H alignment exist.
