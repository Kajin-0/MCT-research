# Stationary matched HSE chemistry: NO-GO before execution

2026-10-16 UTC; baseline `bd71deacf79e670419a80e8f4c9262dcaeed3274`.
One bounded, read-only scientific admission assessment. **No new material
calculation, executable, service, runner or source modification.**

**Decision: NO-GO under the present execution contract.** The audited existing
HSE8 launch path is a fixed two-build diagnostic, not a supported fresh full-SCF
profile. Changing its binary/input/root breaks its frozen pins; unchanged, its
native `electrons.f90` deliberately sets `conv_elec=.FALSE.` and returns after
the second ACE. Its successful finite-acquisition verdict remains valid.
Neither that verdict nor a cgroup cap certifies stationary HSE states.

## What exists, and what is scientifically equivalent

`audit.json` records exact ELF, module, 58 backend-library, PP, input, reference
and source hashes. The stock executable is QE7.5 at
`DFT/.local/qe-env/bin/pw.x`, SHA256
`1d66c7856f5d6b3cd9c66b8578e01512b16bbe907b4360e54234890712ccd6a1`.
It was inspected, **not executed**. The installed environment also records
OpenMPI5.0.10. Private executables audited alongside stock are:

| Existing executable | Qualified scope | Full stationary pair now? |
|---|---|---|
| `h8r_20261015/build1/pw.hse8.relax` | Accepted matched two-build acquisition | **NO**, deliberate diagnostic return |
| `h8c_20261015/build1/pw.hse8.outer` | Eight-build host acquisition | **NO**, unconverged, nonmagnetic-state rejection; Cd withheld |
| `h8u_20261015/build1/pw.hse8.sameD` | Single frozen-D304-column operator acquisition | **NO**, FD nonstationary; not an occupied-state SCF |
| Stock `pw.x`, `ace=.false.` | Established native direct-exchange algorithm | Source-supported; exact full-SCF resource/launch/state qualification **absent** |

**CALCULATED / independently rechecked metadata:** the old matched pair has the
same 6.46-Angstrom cell, origin, positions, complex SOC convention and original
six-probe physical frame. Only one of four Hg sites becomes Cd. Both have
144 electrons,176 spinor bands,50/200/200Ry, Gamma/q1, HSE(.25,.106Bohr^-1)
and FD(.001Ry). XML energies are Hartree: their conversion independently
recovers these Ry settings. All three SG15 PPs are fully relativistic NC,
no PAW/US/NLCC; Hg/Cd valence20 and Te16 give144e in each member. Actual XML
lists24 symmetry operations for each; this alone does not qualify nonlocal
density/operator symmetry or equal chemical symmetry representations.

Initial potential was `atomic`, waves `atomic+random`; there is **no independently
stationary input potential** for a fresh run. The retained reference is the
original7809-G six-spinor frame, to be physically G-embedded into the10827-G
50Ry basis, not substituted for an HSE eigenbasis. The accepted primitive
e90/f120 k4/q4 cold-smearing numerical SCFs remain useful references, but their
cell, cutoffs, quadrature and filling differ. They are not this FD pair.

## Quantitative admission, without an invented upper bound

| Actual past acquisition | Owner wall | Kernel charged peak / sampled family RSS | Outer result |
|---|---:|---:|---|
| HSE8 host, two builds | 410.333s | 4.549GB /4.290GB | dexx2.51875e-3Ry |
| HSE8 Cd, two builds | 409.315s | 4.542GB /4.284GB | dexx2.54897e-3Ry |
| Rejected host, eight builds | 1628.053s | 6.645GB /4.329GB | dexx1.80404e-6Ry; Theta lower witness.999765; quartet spread.655255eV |

GB here means10^9B; cgroup charge includes cache, and sampled RSS may double
count shared pages. All dexx values exceed1e-9Ry. The eight-build job had its
own historical1800s authorization: its elapsed time exceeds the **current600s
cap by1028.053s**. This is not a lower bound on a different direct algorithm.
Two-build inner-SCF errors below1e-9Ry did not establish outer convergence.

Native two-rank packets give EXX60^3, local `nnr=108000`, spinor extent216000,
176 buffered bands and q1. Stock EXX source allocation is **1,216,512,000B
aggregate**. Evc, default-Davidson work/dense matrices and conditional beta
storage bring selected direct-path payloads to **1,594,965,696B**. This is
**not a complete peak or residency bound**: FFT/redistribution, library, local
potential, eigensolver, cache and other simultaneous lifetimes are not closed.
Direct exchange avoids ACE xi, not the full occupied exchange source. Its
complete SCF time, total peak and retained-output upper envelope are unknown.
No extrapolation from the5.56GB frozen-D query or22GiB HSE16 target is used.

At audit time host available RAM was29,915,148,288B and free disk49,536,569,344B;
the host4GiB/disk10GiB floors passed. This does **not** admit the native job.
The prior two-build pair retained about1.466GB, not a full-SCF14GiB guarantee.
Stock direct exchange is selected in `h_psi` by `use_ace=false`; it preserves
the intended HSE operator, but its full nonlinear state still needs testing.
The ordinary DFT `runner.py` has subprocess timeout support, not the required
kernel memory/swap/task, host-floor and aggregate-output contract. No audited
existing full-SCF profile supplies all those gates, fresh authenticated state,
stationary readback and a qualified bounded restart. **No launch is attempted.**

## Scientific boundary and immediate next action

**OPEN / indispensable:** a reproducible stationary nonmagnetic matched HSE
state packet, from an already-qualified native production execution. Require
same-model rebuilt H[D], FD charge/entropy, occupied/eigenpair residuals,
actual crystal/Theta symmetry and tracked Gamma characters, with convergence
and resource logs. Conventional SCF/eigenpair evidence is useful; a universal
mathematical convergence proof is not being demanded. Such evidence is simply
missing for this pair. Direct exchange is the existing-package alternative
to the rejected ACE trajectory, not an assertion of affordability or cure.
Keep the previous1e-8 symmetry and1e-9Ry convergence qualifications unchanged.
Source capacities identify the minimum workload (176 spinors,144e,10827G,
60^3 exchange FFT), not minimum hardware sufficient for convergence. No
defensible numerical minimum RAM/runtime for a complete direct solve follows
from these data. The measured ACE dexx sequence is nonmonotone, so it supplies
no certified contraction or finite-step extrapolation to stationarity.

Next science action is to **obtain that independently qualified matched material
input**, first host, then Cd only after host acceptance. No additional D0
columns, PBE diagnostic, owner/streamer development or scalar extrapolation
can supply it. If a600s job cannot converge, a trustworthy existing native
checkpoint/restart capability would be required before capped continuations;
none is qualified here. More RAM alone does not solve the state/launch boundary.

Even accepted x=0/.25 stationary spectra would establish only a conditional
ordered-cell trend/bracket, with finite-smearing/functional/cell/k errors still
to assess. A physical random-alloy x_c additionally needs interior composition
and disorder input and a justified inversion observable. No projected activation,
inverse-eta ordering, frozen-D eigenvalue or empirical fit is promoted to mass
or x_c. No novelty claim. PBE stays permanently closed; all historical failures,
stock/dirty DFT and original HSE16 remain unchanged. **STOP at this boundary.**
