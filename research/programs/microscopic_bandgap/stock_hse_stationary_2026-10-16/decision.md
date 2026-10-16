# Stock HSE8: long native execution measured; stationary host NO-GO

2026-10-16 UTC. New authorization from a3f49cb allowed an approximately3hour
local candidate; the earlier600s scope was **not** a universal user restriction.
This was ONE fresh stock-QE7.5 host calculation, no private diagnostic binary,
source change, restart, alternative configuration, or new owner/launcher.
Cd was prepared but **never launched**. PBE remains permanently closed.

## Actual numerical result — CALCULATED, not a converged material state

Stock HSE(.25,.106Bohr^-1)+SOC, SG15FR-NC,8atoms/144e/176spinors,
6.46A,50/200/Fock200Ry,Gamma/q1,FD.001Ry,ACE,from_scratch. The actual
command/input/ELF/PP hashes are in `launch_host.json` / `preregistration.json`;
both live rank ELFs independently matched the stock hash. The original physical
six-spinor frame was embedded by actual G labels, not array indices.

| Observed quantity | Value |
|---|---:|
| OS elapsed | **10,488.530204s =2h54m48.53s** |
| Native EXX/ACE source builds | **79** |
| Final corrected total, XML precision | **-1936.3410548077159Ry** |
| Final half-Fock, native printed precision | **-35.83701457Ry** |
| Final exchange residual | **1.12e-6Ry >1e-9Ry** |
| Last inner-SCF error, XML | 8.0996771e-10Ry |
| Charge residual | +8.16556e-11e |
| Independent saved rhoG(0) times cell volume residual | +8.17124e-11e |
| Max FD-occupation reconstruction error | 6.41065e-24 |
| FD entropy contribution -TS | -3.54095e-12Ry |

The exchange residual initially decreased, then plateaued near8.4e-7 and
slowly rose to1.12e-6Ry. **No extrapolation or tolerance change.** Native
`max_seconds=10440` was detected at elapsed10486.87s, followed by writing
XML/density/waves/ACE/restart records. `EXX self-consistency reached` is absent
and XML convergence=false. OS exit0 / `JOB DONE` do **not** make this converged.
No continuation is attempted or restart equivalence claimed.
Native stderr reports IEEE underflow/denormal flags; these are retained, not
silently removed. The reported energies and the independently read arrays are
finite. `native_readback.json` independently confirms the executed parameters;
the saved scalar-density normalization is rhoG(0)*det(cell), in Bohr units.

## Independent saved-state symmetry falsification

For the saved NC density D=W diag(f) W^dagger, all176 native complex spinors
and physical G labels were used. Theta(up(G),down(G))=(down*(-G),-up*(-G)).
The source Gram defect is6.96e-15. A normalized-source compression gives
||D-Theta D Theta^-1||op >= **.999996959728**. An independent QR reduction
of [W sqrt(f),Theta(W) sqrt(f)], retaining every column without truncation,
gives operator norm **.999996959745**, Frobenius norm **2.00301967584**.
An independent scalar contraction on a physical-frame vector gives
-.999790729804, agreeing with its six-matrix reconstruction to1.11e-16.
These are numerical results on this saved density, not material phase claims.

All24 actual host Td operations were tested on the physical-frame density;
the largest compressed defect is **.999576889655**. Full24-space upper tests
were withheld after the independently decisive Theta failure. The reference
Theta-span defect1.2864e-7 is explicitly nonzero: the contraction uses actual
Theta-transformed spinors, **not** a falsely closed six-dimensional frame.
The whole-density QR result is independent of that reference altogether.

The four dominant Gamma8-character states have weights>.99974 and span
**661.214908meV**; the two Gamma6-character states span **5.385866meV**.
Native geometry still lists24 symmetries and a nonmagnetic SOC flag. Those
flags/local-zero-spin do not certify the nonlocal state. Neither averaging
these split states nor subtracting sorted levels yields the requested signed
Gamma6/Gamma8 mass. Do not infer physical HgTe magnetism, topology or x_c.
No same-rebuilt-H full eigenpair residual packet or numerical mass bound exists.

## Measured execution and its limitation

The standard transient unit enforced12GiB/swap0/tasks12,CPU200%/nice10,
hard10800s; no stock/source changes or paid resources. Retained manager
MemoryPeak=**4,224,897,024B**; sampled family RSS peak=**4,290,023,424B**
(shared-page overcount). Sampled task peak7, swap0, all observed limit/OOM
counters0; host available>=25,269,334,016B and disk>=49,398,976,512B.
Fresh retained native/staged files total131,777,577B. Sampling is not a
continuous aggregate quota or host-wide MPI-exclusion proof.

The one-off sampler failed at terminal `KeyError: ControlGroup`: full manager
show omitted the empty property after the cgroup disappeared. The error and
all samples remain in `monitor_terminal_failure.json` / `host_monitor.jsonl`.
**No full sampler PASS.** Independent explicit manager readback retained the
same invocation, exit0/NRestarts0 and final peak; all three recorded PID/start
identities were gone and the original cgroup absent. The own exited transient
unit was then stopped/unloaded; no other unit or raw file was changed/deleted.
This terminal observation defect did not cause the native soft stop or explain
the preceding hours of convergence/symmetry failure. No monitor repair/retry.

## Decision and science boundary

**Resource feasibility was measured; the intended stationary nonmagnetic host
was NOT obtained. Cd release NO-GO.** This separate stock run establishes that
the problem cannot simply be assigned to the earlier private diagnostic stop
or lack of wall time. It does not select ACE off-span bias versus a Gamma-only
mean-field instability or another state/model issue. Both remain hypotheses.

The indispensable next physical input is a symmetry-qualified stationary HSE
host, then matched Cd. Stock direct exchange is an established algorithmic
control, but its whole-SCF cost remains unmeasured: this run spent9125.28s in
79 ACE builds versus1209.11s in the inner solves; replacing all1984 h_psi calls
by direct exchange cannot be assumed affordable. No new calculation or software
campaign is admitted by this decision. BZ/finite-cell/functional/smearing and
alloy-ensemble uncertainties remain separate. No mass, chemical HSE shift,
random-alloy bracket, empirical fit or physical x_c is invented. No novelty claim.

Verification preserves822protected pins,76historical originals,dirtyDFT/stock,
old refusals,originalHSE16 and other sessions. Large native wave/ACE files are
retained privately with hashes; GitHub contains their manifest, not those files.
The18-build stdout checkpoint is an unchanged prefix. Raw native whitespace
is preserved; whitespace checking excludes raw stdout, not code/docs. **STOP.**
