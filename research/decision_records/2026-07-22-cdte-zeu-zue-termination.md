# Decision record: CdTe zeu/zue route comparison and path termination

**Date:** 2026-07-22  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #271  
**Parent:** #4  
**Status:** completed bounded diagnostic; current polar-response path terminated for A1

## Decision

The current Quantum ESPRESSO/PBE/current-pseudopotential polar-response path is terminated for CdTe A1 work.

The bounded same-state diagnostic completed exactly one SCF state and two independent Gamma-point Born-charge routes. Both response routes converged and agreed tensor-by-tensor, but both violated raw charge neutrality by order unity.

No retry, convergence sweep, altered cutoff, k grid, threshold, structural state, functional, pseudopotential, A1, EPW, HgTe, or alloy calculation is authorized by this result.

## Immutable evidence

```text
workflow run      29944282253
artifact id       8542244366
artifact digest   sha256:8379318f214a564fa1f7fd6ff6bd206b34d392cc4deca09e01f25234822fc6b9
head commit       952db5786413522df6500ffc82d419fa76b97dea
```

The artifact contains the complete SCF save state, both response-route scratch copies, raw QE outputs, exact eigenvalues at all sampled k points, executable and pseudopotential hashes, timing records, and the evidence manifest.

## Measured tensors

The `zeu` route produced cubic diagonal tensors:

```text
Cd  +2.90543 I
Te  -4.15794 I
sum -1.25251 I e
```

The `zue` route produced:

```text
Cd  +2.90575 I
Te  -4.16077 I
sum -1.25502 I e
```

The maximum atom/component route difference was

```text
max |Z*_zeu - Z*_zue| = 0.00283 e
```

which passes the declared `0.05 e` route-agreement threshold.

The maximum raw charge-neutrality residuals were

```text
zeu  1.25251 e
zue  1.25502 e
```

which fail the declared `0.05 e` threshold by factors of approximately `25.05` and `25.10`, respectively.

## Electronic separation and convergence

The minimum occupied--unoccupied separation over all eight sampled k points was

```text
0.49733490292583227 eV
```

at Gamma. This passes the declared `0.05 eV` minimum.

The SCF completed with `JOB DONE` and convergence. Each response route completed with `JOB DONE`, no fatal marker, and two recorded response-convergence completions. The base, `zeu`, and `zue` save states were hash-verified as identical before response execution.

## Interpretation

The close `zeu`/`zue` agreement strongly disfavors a route-specific implementation defect. The positive sampled gap disfavors an explicit sampled metallic-state explanation under the declared grid. The shared order-unity neutrality violation instead demonstrates that the present response state is internally inconsistent for polar effective-charge use despite route agreement and nominal convergence.

Charge-ASR projection would conceal, not validate, this failure.

## Consequence

The following path is closed:

```text
QE 7.4.1
PBE
current verified fully relativistic PseudoDojo Cd/Te ONCVPSP pair
fixed experimental-reference volume
4 x 4 x 4 unshifted k grid
ecutwfc = 114 Ry
ecutrho = 570 Ry
SOC/noncollinear fixed occupations
polar dielectric/Born response as basis for A1
```

This decision does not establish that all QE, PBE, or ONCVPSP polar-response approaches are invalid. It terminates only the tested combined path and forbids automatic escalation from this result.

## Claim boundary

The result does not establish converged CdTe dielectric constants, Born charges, equilibrium pressure, phonons, AHC corrections, Kane parameters, HgTe behavior, or alloy behavior. It establishes only that the tested current polar-response path fails the predeclared raw neutrality gate and is unsuitable for A1.
