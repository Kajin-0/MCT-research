# Approved native matched pilot — safe preflight NO-GO

**Decision: PREFLIGHT_RESOURCE_NO_GO. No SCF launched.** The user explicitly
approved one staged native HSE+SOC 16-atom n2/k2/q2 f120 host, followed only
after host acceptance by one Cd-substituted member. This finite approval changes
neither the old paused/blocked goal nor the physical acceptance gates. The
permission included stopping if actual resource headroom was unsafe.

At **2026-10-11 19:22:26 UTC**, the read-only [preflight record](preflight.json)
measured:

| Quantity | Measured / recorded value | Interpretation |
|---|---|---|
| Physical RAM | 31.34078 GiB | Host total; no new allocation |
| Effective available RAM | 26.39040 GiB | /proc MemAvailable, restricted by any finite ancestor cgroup cap |
| Used swap | 2.21329 GiB | Excluded from launch headroom |
| Disk free | 30.16499 GiB | Passes the 8-GiB free floor; full-SCF scratch demand remains unmeasured |
| Existing QE/MPI family or R07 driver | None in process snapshot | Availability snapshot, not a reserved ownership lock |
| Existing supervisor records | Both FINISHED; one recorded owner PID absent, other not provided | Read-only intake; state hashes unchanged |
| Prior native dry estimate, six ranks | Host 21.27 / Cd 21.32 GiB | Rough QE dynamical-RAM estimates; full-SCF peak unknown |

## Why the launch gate failed

Before recording the terminal preflight, declare an engineering guard:

```text
required available RAM = 1.20 * prior dry estimate + 2 GiB system reserve.
```

The 20% margin covers uncertainty in the rough allocation estimate and runtime
workspaces/MPI overhead; the 2-GiB reserve protects other resident services.
These are conservative launch-policy choices, **not** measured peak overhead,
a rigorous memory upper bound, a user-specified numerical threshold or a theorem
that the run would certainly fail. After reserving 2 GiB, the host has only
3.12 GiB (about 14.7% of the estimate) for unknown overhead. Full-SCF monitoring
has no previous peak to calibrate against; available swap is not a substitute.

The policy requires **27.524 GiB** available for the host. The measured shortfall
is **1.13360 GiB**. The prospective Cd member would require 27.584 GiB, but it
is not admitted because no host was run or accepted. No lower cutoff, reduced
k/q mesh, smaller band count, relaxed convergence, new variant, queue or implicit
continuation was substituted. This is a conservative safe-preflight decision,
not a physical HSE result or proof of unavoidable OOM.

## Stage disposition and remaining uncertainties

1. Prepared-deck/PP intake passes: 15 source hashes, unchanged matched physics
   (90/360/120 Ry, 352 bands, HSE+SOC, full empty-state accuracy, conv_thr=1e-10),
   previous QE 7.5/six-rank dry provenance and SG15 PP hashes verify.
2. Existing process/supervisor intake passes as a snapshot; no exclusive lock
   is acquired because the RAM gate fails before launch.
3. Host SCF/exchange convergence: **NOT RUN**. Projector/irrep transport and
   the 1-meV host comparison: **NOT EVALUABLE**. No native bands.x or other
   postprocessor is run.
4. Cd-substitution SCF: **NOT ADMITTED**. Full-SCF peak RAM, wall time, output
   growth, Gamma moments and material uncertainty remain **unknown**, not zero.

The approved maximum was six ranks, one sequential family, <=3600 seconds plus
<=1800 seconds grace per member. Actual QE invocations, native output directories
and job-owned allocation are **zero**. No live numerical outcome or memory peak
is inferred from the prior ~169-MiB dry RSS. Existing dirty DFT status and both
supervisor state hashes are preserved. No supervisor or historical goal operation
occurs. No material signed gap or physical x_c is claimed.

## Qualified next action

The same physical inputs need greater **measured available RAM** sufficient for
the declared guard, or an independently justified tighter full-SCF peak bound
and resource-containment plan. Any future attempt needs a fresh preflight and
explicit scope/ownership review; this result creates no retry, waiting loop,
cleanup, allocation request, variant or queue. It does not demand more precise
binary spectra or loosen the [scientific acquisition gates](../physical_input_qualification_2026-10-11/minimum_acquisition.md).

The [collector](collect_preflight.py) is read-only and cannot launch QE. It
refuses to overwrite its result. [Focused tests](test_preflight.py) check saved
provenance, independent GiB/byte guard arithmetic, threshold boundaries,
cgroup/swap treatment and the staged NO-GO. All measurement files are in this
MCT package; no DFT file is edited. Prior analytical/physical rejections remain.
