# Native first-ACE pair passed; HSE relaxation remains open

**PASS for the separately frozen p2 acquisition.** One real two-rank host pilot
and one sequential Cd pilot completed the planned first ACE. Every owner,
resource, source, scientific and readback gate passed. No retries occurred.
This does not change the original c50f466 owner FAIL, whose old root/unit/files
were never reused. Stock QE, dirty DFT, other sessions and the historical goal
remain untouched.

**CALCULATED:** the chemical difference in the fixed original Γ6–Γ8 normalized
trace of the first HSE activation operator is **+44.184097 meV**. Direct exchange
contributes +55.956327 meV; the local-potential contribution is −11.772230 meV.
[Methods and limits](methods_and_limits.md) define the observable and distinguish
it from converged HSE eigenvalues and the prior PBE Gaussian response.

| Native measurement | Hg4Te4 | CdHg3Te4 |
|---|---:|---:|
| Guarded wall time (s) | 215.601161 | 200.985943 |
| QE wall time (s) | 213.92 | 199.14 |
| Kernel MemoryPeak (bytes) | 4,232,114,176 | 4,225,994,752 |
| Sampled family RSS, shared overcount (bytes) | 4,284,395,520 | 4,279,013,376 |
| Half-Fock energy (Ry) | −35.730844162428 | −35.782160667461 |
| First-activation total (Ry) | −1936.291896046756 | −1936.435500483927 |
| Preliminary source SCF steps | 11 | 11 |
| Preliminary source SCF error (Ry) | 6.79314e-10 | 2.61609e-10 |
| Direct/ACE action relative residual | 5.07178e-16 | 5.31170e-16 |
| Direct/ACE Gram relative residual | 5.28057e-16 | 5.71458e-16 |

Both have 10,827 wave plane waves, 86,791 EXX G vectors, native 60³ FFT and a
measured aggregate exxbuff extent of 1,216,512,000 bytes. All source waves read
back byte-for-byte; rhoR/rhoG remain byte-identical across activation. Native
24-operation symmetry, actual Γ/q1 settings, 176 bands/144 electrons, FD charge,
physical reference embedding, pinned ELF/PP/source and both live rank leases
passed. Complete native packets and HDF5 waves are retained privately with
hashes; small native logs, XML, manager/lease records and telemetry are archived.
Three independent read-only scientific checks passed. An unavailable mpmath
import in the first offline check was replaced by stdlib Decimal; that check
failure is retained and did not affect native science or the frozen protocol.

The strict 12 GiB memory/swap-zero/tasks-12/600 s caps held. Lowest observed host
MemAvailable was 25,619,382,272 bytes; free disk stayed above 63,640,834,048 bytes.
Maximum sampled pair output charge was 861,986,816 bytes; final charge including
fixed prepared source/PROFILE is 861,831,394 bytes, below 14 GiB. Sampling leaves
the already documented between-sample writer/burst risk; no continuous aggregate
quota theorem or host-wide foreign-MPI absence claim is made. Both own cgroups
are gone; known lock is free and the old ledger is byte-identical.

The new host/Cd socket addresses were independently bound and removed before
services: 103/101 pathname bytes, 104/102 including NUL. Only the reviewed patch
changed the versioned owner; the same compiled QE ELF and native arithmetic
were reused, with fresh jobs/nonces/roots. This pilot measures approximately
4.23 GB of actual first-ACE kernel memory, not whole-SCF RAM improvement.

## Scientific decision

**Advance functional-dependence research, with a finite HSE relaxation experiment
as the next acquisition.** The measured operator effect is tens of meV and is
chemically sensitive; another small PBE grid adds less relevant information.
However first-ACE timing does not bound the number or cost of HSE outer/inner
iterations. Full HSE convergence within 600 s is not demonstrated.

[The next experiment](next_experiment.md) proposes a separately admitted one-
outer-relaxation matched comparison, not an open-ended SCF. It is unlaunched and
requires explicit scope plus minimal source/state qualification. The current
first-ACE acquisition is complete. Stop after validated research commit/push.
No converged HSE gap, physical x_c, restart success or full-SCF memory saving.
