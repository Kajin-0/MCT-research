# Density-only driver: build GO; runtime qualification REFUSED

2026-10-16, baseline `75b0e3392e071452e7f7ce018f35046842f821f2`.
Finite authorized phase complete. **No QE-linked executable was run, no
material density/potential/action was evaluated, and no scientific release is
issued.** Historical Gate A and refused PBE diagnostics remain unchanged.

## Implemented and measured

**CALCULATED / software evidence:** the new standalone
[`density_driver.f90`](density_driver.f90) compiled and linked on its FIRST
frozen-source attempt, using the existing QE7.5 modules and unchanged stock
`libqe_pw.a` (SHA256 `65349164…16f0a2`). No QE physics object was patched or
archive replaced. Exact commands, diagnostics (none), source/ELF hashes and
private location are in [build_result.json](build_result.json). A separate
non-LTO C gate always returns EPERM before `mp_startup`; the new ELF is
explicitly **UNEXECUTED**, not a runnable science profile.

The implemented path is needwf=false `read_file_new` → `post_xml_init`,
explicit `set_vrs`, one-rank `n_plane_waves/init_igk`, `g2_kin/init_us_2`,
becp12, native `h_psi` and separate kinetic/local/NC-SOC actions. Saved XML
nbnd352/nelec288 remain metadata. No SCF, occupations, saved wave loading,
`allocate_wfc_k`, `wfcinit`, `openfil`, `electrons` or `non_scf` is invoked by
the new path. The linked archive DOES contain these symbols through untaken
branches; absence from the ELF is neither asserted nor required. Runtime
initialization and numerical equivalence remain untested.

The new R07D1 packet/reader has singleton metadata, physical G labels, FFT,
rho/potential and 12 complex probe/component actions. Nine offline tests pass:
import isolation, finite extents/nonfinite/duplicate rejection, old two-rank
schema refusal, explicit Theta controls and Theta²=-1, component/Hermiticity/
normalization, and scalar-shift invariance using exact Gram metrics. These
synthetic tests validate code/arithmetic, NOT HgCdTe or the native operator.

## Actual NON_SCIENCE attempt — refusal is final

Both separate tiny C programs built: filesystem/seccomp probe and direct
MPI_Init_thread singleton probe. Neither links QE. ONE fresh filesystem-only
service was attempted at **18:20:12 UTC**, unit
`r07-owned-02c469543180441d9568d046045620f8.service`.
It printed `NON_SCIENCE READY pid=1983796`. The owner then raised an admission
`AssertionError` BEFORE writing the fresh nonce; the `go` file is still empty.
It stopped only this owned service. No Landlock rules, negative write tests,
process/socket tests or MPI initialization ran. The conditional singleton
attempt was **WITHHELD**, not retried or replaced.

[Immutable result](runtime_fs_probe.json), [prospective identity/command](preregistered_fs_probe.json)
and private original RESULT/FROZEN bytes agree. Kernel pidfd exit and original
cgroup empty/absent were checked. Manager recorded peak **1,835,008 B**, swap
peak0, about **77 ms native lifetime**; whole owner attempt **0.146157 s**.
These are startup-only observations, not QE memory/time bounds. Manager
configuration reports12GiB/swap0/tasks12/600s, but the live kernel/manager/
member admission certificate did not finish. The original frozen floors were
29,904,355,328 B available RAM and49,539,375,104 B free disk.

**Important negative evidence:** cleanup has manager Result=success and
foreground wait0, yet ExecMainCode=2/ExecMainStatus=15 (owner-requested TERM).
It is NOT native success. The absorbing owner REFUSAL takes precedence.
The error handler did not retain a traceback/named predicate or intermediate
facts, so the exact failed assertion cannot be recovered from these records.
It is bounded to the pre-nonce identity/kernel-limit/manager/member checks;
no FD-race, Landlock denial, PMIx need or resource exhaustion is inferred.
That diagnostic loss is itself an implementation defect. The failed frozen
owner/source/result are preserved, and no second live attempt is justified in
this phase. This is a new NON_SCIENCE scope, never a retry/pass of old Gate A.

## Decision and exact next boundary

**BUILD GO; CONFINEMENT/SINGLETON UNQUALIFIED; SCIENTIFIC EXECUTION NO-GO.**
Before another separately authorized NON_SCIENCE attempt, the owner must record
named admission predicates and their actual facts durably BEFORE releasing a
nonce, including start/pidfd/exe/cgroup and kernel/manager values. Independently
exercise those predicates offline. Do not reinterpret or rerun this unit.
Only then can actual positive/negative Landlock and one-process/no-helper
singleton behavior be tested. If OpenMPI needs a helper, socket or unadmitted
write path under this strict contract, stop; do not auto-launch mpirun or
weaken confinement. ABI7 availability and compiled tests are not enforcement.

The separate material release additionally needs the exact initialization,
component/native-control, physical-frame/Theta, readback, owner and full
resource tests listed in [packet_and_execution_boundary.md](packet_and_execution_boundary.md).
The prospective2meV numerical contrast certificate is NOT achieved. Primary
future science remains24 actions total, not12. No new static environment value,
N2, linewidth, physical mass/gap/x_c, HSE result, or novelty claim is made.
