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
