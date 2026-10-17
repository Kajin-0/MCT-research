# One stock primitive HgTe k4/q4 control

Frozen 2026-10-17 before native launch; baseline ab6fbd0. ONE fresh atomic-start
stock QE7.5 ACE case; no restart, retry, Cd, PBE diagnostic or source build.
The input diff is restricted to k/q2->4, fresh paths/prefix and runtime budget.
Same a6.46Å primitive cell/origin, SG15 FR NC,36e/44spinors,50/200/Fock200Ry,
HSE(.25,.106Bohr^-1),FD.001Ry,SOC,noncollinear,symmetry on,inner1e-9Ry,
adaptive_thr=false,100outer/100inner steps,Davidson/full_acc,mixing.3.

**Question:** does denser BZ/exchange quadrature suppress the near-Fermi
occupation/symmetry instability of the k2 trajectory? Mesh/q sampling is the
only deliberate physics change. Atomic+random initialization is not a
byte-identical Gamma seed across the two executions; nonlinear basin and
initialization effects remain. The old e90/k4 cold/f120/f360 states are useful
references but do not constitute this e50/FD control or isolate its cure.

Unshifted4³ includes Gamma. Verify actual native k coordinates/weights and64
q-source coordinates; require observed Gamma weight1/64. XML stores q-grid
dimensions, not explicit q coordinates; stdout supplies the latter. Expected
8 irreducible k points and24crystal operations are to be checked, not assumed.
44bands is held: old accepted k4 also used44 and k2's upper8 were empty.
Check the new upper-band occupations and spectral range; no completeness or
off-span ACE bound follows from this history. Failure does not authorize
silently increasing bands/changing solver or smearing.

## Finite execution and resource basis

Standard existing stock mpirun/two local ranks and transient systemd limits;
MemoryMax12GiB,swap0,TasksMax12,CPU200%,nice10,hard24hours. Native max_seconds
82800(23h) reserves an hour for the next stop/save boundary; checkpoint
completion is not guaranteed under arbitrary slowdowns.100outer steps remains
a second finite bound. No continuation of an interrupted state is admitted.

Pristine EXX source allocates a persistent host complex exxbuff over local
FFT sites,2spinor components,44bands and64source points. At the observed k2
40³ grid the aggregate unpadded capacity is5,767,168,000B(5.37GiB). GPU and
localized-exchange alternative buffers are not enabled in this stock CPU deck.
ACE xi,temporary/global FFT arrays,PP/solver/BLAS/HDF5/cache remain additional;
the subtotal and old1.043GBpeak are **not a total upper bound**. A private OOM
is possible and ends the sole attempt. The actual kernel12GiB cap,swap0 and
OOMPolicy=kill bound its host charge; preflight requires MemAvailable minus
the full cap still>=4GiB, and disk minus14GiB still>=10GiB. No cap increase.

The k2 Fock wall792.14s for16builds times(8/3) irreducible k times(64/8)
sources forecasts4.69h for16builds, not a timing/convergence bound.24h allows
substantially more iterations;600s is not a user restriction. Inspect actual
native allocation and time. Stock files,PP copies,stdout/stderr,MPI TMPDIR
and shared-memory backing are private to this new short root. No custom
owner sockets/leases: actual MPI socket paths, if present, are inspected
after startup; no invented socket name is certified as an actual endpoint.

Reuse simple OS/resource sampling in a bounded job-specific observer under
a separate transient service (256MiB,swap0,3tasks,no restart). Its16MiB log-read
ceiling bounds parsing overhead; an unexpected larger log stops the case.
The standard worker BindsTo this observer, so a crashed observer also stops
the worker. Native terminal facts are saved before observer exit/worker unload.
It is not a new
launcher/FD/lease framework and launches no science. It checks exact worker
InvocationID,host available>=4GiB,disk free>=10GiB,owned sampled output<=14GiB;
on a floor/budget failure it stops only the same owned invocation. A changed
invocation is refused without killing a replacement. Kernel limits are hard;
30s output/floor sampling is not an aggregate quota or continuous guarantee.
Observer/source/output are private; immutable checkpoint copies go to Git.
No global foreign-MPI absence or private-network proof is claimed.

## Prospective scientific stop and acceptance

Early-stop guideline is frozen now: after>=12COMPLETED source builds, require
the last3Gamma candidate blocks each spread>0.2eV, last spread not decreasing
by>.0002eV from the first, initial quartet occupation spread<=.1 and last3
occupation spreads>=.8, and all last3dexx>1e-8Ry with last/first>=.5. This
means sustained large splitting, degraded occupations and no rapid residual
recovery. It requests stock prefix.EXIT once, not a retry or convergence claim.
If restoring symmetry or rapidly approaching convergence, continue within
the finite budget. A topmost-band occupation>1e-8 is a separate inadequate-band
stop. Resource/native failure is absorbing; no second case.

During execution, printed Gamma bands33–34/35–38 are **candidate index probes**
only, with .0001eV and .0001occupation display resolution. Require a separated
35–38 window (>0.01eV from bands34/39) before automatic symmetry-stop use.
This does NOT prove their irreps. Final physical G-labelled complex overlaps
and Td operations must confirm or refute the provisional assignment; an
early stop cannot by itself prove the absence of a symmetric fixed point.
No spinor density is inferred from scalar charge, native nonmagnetic labels
or adjacent energies, and no incomplete mutable HDF5 snapshot is accepted.

Accept native outer SCF only with reachedEXX message, XMLtrue,lastdexx<=1e-9Ry
and inner error<=1e-9Ry. Require36e within1e-8e,FD formula within1e-8,
normalized spinors,Theta/Td1e-8 and qualified physical sectors before a
nonmagnetic-host interpretation. Generic k now needs the actual -k fiber
mod reciprocal G: **do not run the k2 all-TRIM analysis unchanged**. Reconstruct
stars with checked native rotation/little groups and report that extension
separately from actually saved representatives; never claim64nativeexports.
No open_grid, full-H action or other native postprocessor is authorized.
Full-H/eigenpair residual unavailability and finite-smearing/cutoff/material
uncertainty remain explicit. No averaging split levels into a gap/mass/x_c.

If still running, archive an immutable stdout/resource/identity checkpoint,
commit/push state/handoff and report RUNNING. Do not restart the same unit.
After its sole termination, read saved arrays and verify own cleanup/protected
pins; then stop this experiment. No additional material job is authorized.
