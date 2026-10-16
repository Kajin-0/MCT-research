# Choose ONE density-only QE-native probe; execution remains NO-GO

**2026-10-16; baseline9a7dafaca4e605b98adf200a6e463a936f748304.**
Bounded non-executing source/science assessment COMPLETE. No compile, native
MPI/QE/H action, SCF, transient service, protected-file edit or launcher retry.
The Gate A startup FD refusal and every older failure remain immutable.

**Scientific design: GO, CONDITIONAL on the stated implementation tests.
Execution admission: NO-GO.** Select a NEW standalone QE-linked postprocessing
driver using `read_file_new` with a false-initialized needwf variable, explicit `set_vrs`, and probe-only
k/beta allocation, with exactly ONE world rank if the installed MPI runtime
can qualify singleton execution. Do not use or patch the frozen two-rank ELF.
There is no current build, job/profile release, service, nonce or launch command.

## Decision-changing source result

The pinned QE7.5 already provides the essential density-only initialization.
`read_file_new` calls `post_xml_init` before its conditional wavefunction block.
With input needwf=false it neither calls `allocate_wfc_k`, `wfcinit`, nor imports
saved wavefunctions. `post_xml_init` reads XML/PP/rho and rebuilds ionic, Hartree,
PBE-GGA and NC-SOC coefficients. It **does not set vrs**. Separate `n_plane_waves`,
`klist:init_igk`, vkb/g2kin allocation and12-column becp suffice for h_psi.
QE's own `PP/src/pp_example.f90` demonstrates the surrounding H-application
pattern, including explicit set_vrs; its saved-wave solve is NOT copied.
Its aux(npwx,nbnd) template is not a spinor qualification: new arrays need
npwx*npol leading extent, as in the original physical12-probe driver.

This removes a false information requirement: **352 is retained XML spectral
metadata, not a required number of solved/loaded vectors for H[rho_saved]Phi.**
Tiny et/wg metadata still get parsed; nbnd is not set to12 and no electron or
occupation model is changed. The old init_run path DOES unconditionally
allocate evc352/open buffers/call wfcinit, including atomic/random fallback.
Neither that path nor read_file_new(true)/read_file/read_file_ph is preferred.

For THESE exact Hg/Cd/Te UPFs, NC/full-relativistic/has_so are true, US/PAW and
core_correction false, and no PP_NLCC/PP_AUGMENTATION dataset exists. Thus no
unmeasured occupied matrix, augmentation occupations or NLCC density is
required. Full-relativistic bare projector/SOC coefficients remain essential;
NC does not mean local or spin-independent. This statement does NOT extend to
HSE, meta-GGA, Hubbard, magnetic, US/PAW, NLCC or external-field cases.

## Actual retained-input checks and cost reduction

Both accepted saves contain173631 complex density coefficients on the same
80^3 logical mesh, with charge errors +1.0033e-10 and-4.1723e-11 electrons.
Independent direct Fourier sums agree with FFT values at three nodes within
5.60e-16; deliberate physical-G reordering restores all density bytes. Original
50Ry frame/explicit Theta images and24/4 chemical groups are preserved.
These are input/transport checks, NOT native potential/operator equivalence.

Each minimal XML+rho+3PP set is5.98MB; common12-probe payload8,810,960B.
Each member's243,509,564B wfc file can be excluded from production staging.
The avoided evc352 allocation is243,246,080B at logical one-rank N=21595.
Known selected one-rank payloads total439,686,504B (~419.3MiB), dominated by
vkb246,010,240B. This subtotal is **NOT peak RAM**. Radial/FFT/MPI/HDF5/allocator,
initialization transients and outside-reader peaks remain incompletely bounded.
No <=12GiB/600s completion or memory-saving claim has been established.

## Why this choice, rather than alternatives

| Path | Scientific/implementation assessment | Decision |
|---|---|---|
| QE density-only, one world rank | Keeps trusted PBE gradients, FFT and FR projector conventions; needs a small new driver/reader, singleton and confinement qualification. Core adapter estimate200–340 Fortran/Python lines; qualification/confinement additional150–300 lines, planning ranges only. | **ONE preferred path, conditional design GO** |
| Independent rho+UPF evaluator | Mathematically possible here, but must duplicate radial interpolation/quadrature, PBE derivatives/divergence, SOC angular algebra, phases and potential zero. At least6 separately validated component kernels; rough800–2000 new implementation/test lines plus trusted native baselines. | Reject as cheapest path; no evaluator built. |
| Two-rank density-only fallback | Same physical operator after correct transport; no inherent scientific need for2ranks. Revives the unresolved real lifecycle gate and distributed layout. | Consider ONLY if one-rank scientific equivalence fails, not to evade singleton/confinement refusal; no current release. |

The separate MPI singleton issue is unresolved: QE supports initialization
without assuming size2, but the installed OpenMPI5 runtime requires PMIx
support and may need helpers. No “one process/no launcher” assertion is proved.
A read-only Landlock VERSION query returned ABI7; no ruleset, enforcement or
mount namespace was tested. Source/data feasibility is not security admission.

Read [the exact preferred path and observable](preferred_path.md),
[prospective gates and confinement boundary](acceptance_and_policy.md),
[source/PP/input pins and assertions](audit_result.json), and
[independent actual-data checks](independent_results.json).
Read-only reproduction from MCT, with PYTHONDONTWRITEBYTECODE=1 and BLAS/OMP
threads1: use the existing DFT venv Python on `audit.py --check` and
`independent_checks.py --check` in this directory. Neither imports an owner,
builds native code nor invokes systemd/MPI; audit's only kernel experiment is
the non-enforcing Landlock VERSION query. Private saved files must be present;
their hash manifests do not make them public data.

**STOP:** first indispensable new information is whether a fresh pinned
one-world-rank driver can execute under independently demonstrated confinement
and singleton/runtime bounds, followed by valid operator cross-validation.
That needs separate implementation/testing authorization; no build/run is
authorized here. No generic MPI/owner redesign or automatic fallback is queued.
New static A/B could resolve a projected static arrangement contrast, not QHQ,
N2, ensemble linewidth, physical mass/gap or x_c. No novelty/registry promotion.
