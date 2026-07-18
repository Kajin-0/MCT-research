# CdTe A0: bounded execution and convergence gate

This directory implements the authorized CdTe A0 static/phonon sanity stage from
the thermal-moment decision memo.

The physical-volume, pseudopotential-byte, runtime-build, and release-specific
input gates are closed for the **first declared A0 convergence point only**. No
scientific calculation or material result has yet been recorded.

## Authorization boundary

A0 permits only:

- static fully relativistic SOC calculations;
- coarse phonon-stability checks;
- dielectric-tensor and Born-effective-charge sanity checks;
- convergence and resource measurements needed to decide whether A1 is viable.

A0 does not authorize the timed A1 electron-phonon smoke test, production AHC,
dense EPW, HgTe, VCA, SQS, CPA, SCBA, or alloy calculations.

The current authorized next action is:

> Execute the smallest declared A0 point and record raw observables. Do not infer
> convergence from one point.

## Selected pseudopotentials

The pinned upstream source is:

```text
PseudoDojo/ONCVPSP-PBE-FR-PDv0.4
commit 7aa01a3fcf5ad226caf25bd387a9be9612be9f27
```

Selected Quantum ESPRESSO files:

```text
Cd/Cd-sp_r.upf
Te/Te-d_r.upf
```

Matched ABINIT files:

```text
Cd/Cd-sp_r.psp8
Te/Te-d_r.psp8
```

The headers identify norm-conserving PBE potentials with full relativity,
spin-orbit data, and nonlinear core correction. Cd has 20 valence electrons with
`4s 4p 4d 5s` represented; Te has 16 with `4d 5s 5p` represented.

The exact immutable upstream bytes were independently acquired and verified in
PR #42. PR #96 reconstructed all four runtime copies from the pinned commit and
required their SHA-256 values to match the selection manifest.

The pseudopotential payloads are not committed. Every future runtime copy must be
rehash-verified before use.

## Cutoff-unit correction

PseudoDojo publishes cutoff hints in Hartree. Quantum ESPRESSO accepts
`ecutwfc` in Rydberg, so the hints are multiplied by two.

| Element | low (Ha) | normal (Ha) | high (Ha) | low (Ry) | normal (Ry) | high (Ry) |
|---|---:|---:|---:|---:|---:|---:|
| Cd | 47 | 51 | 57 | 94 | 102 | 114 |
| Te | 34 | 40 | 46 | 68 | 80 | 92 |

Cd controls the compound starting ladder:

```text
94 Ry -> 102 Ry -> 114 Ry
```

These values are starting points, not convergence evidence.

## Bounded lattice and fixed-volume protocol

The selected fixed-volume reference is:

```text
a_ref(0 K) = 6.476035479332049 Angstrom
conservative absolute bound = +/-0.001814959409196 Angstrom
```

The bound corresponds to a maximum volume uncertainty of approximately
`0.08410%`, or `16.82%` of the declared one-sided `0.5%` A0 volume perturbation.
It is adequate for this sensitivity test but is not a metrology-grade universal
CdTe lattice constant.

The source chain combines:

- the Williams 1969 primary absolute X-ray anchor;
- Smith-White 1975 primary low-temperature single-crystal expansion;
- the verified Browder-Ballard 1972 publisher table as the full-range bridge
  shape;
- an explicit morphology-transfer bound large enough to contain the existing
  alternative bridge estimates.

The sensitivity points are defined in volume:

```text
Delta V / V = -0.005, 0, +0.005
```

and converted exactly through:

```text
a / a_ref = (V / V_ref)^(1/3)
```

All electron-phonon temperatures must use one fixed `V_ref`. Any future
quasiharmonic term must be calculated separately and added once.

## Declared convergence protocol

`cdte_a0_convergence_protocol.md` declares the smallest sequential plan:

1. `ecutrho/ecutwfc = 4, 5, 6` at `ecutwfc = 114 Ry`;
2. `ecutwfc = 94, 102, 114 Ry` after selecting the density ratio;
3. Gamma-centered cubic k grids `4, 6, 8, 10, 12`;
4. SOC band counts `40, 48, 56, 64` for the verified 36-electron cell;
5. tightening SCF and phonon thresholds;
6. one selected-versus-next-denser cross-factor recheck.

A setting is selected only after two successive refinements satisfy every
applicable observable criterion. Failure at the largest declared point stops the
branch and requires a new decision memo.

Validate the plan structure without running a code:

```bash
python tools/check_cdte_a0_convergence_protocol.py \
  --require-valid \
  --report-json runs/cdte_a0/convergence-protocol-report.json
```

A passing protocol report establishes only that the ladder is internally
consistent.

## Exact code and runtime evidence

The source trees are pinned to:

```text
Quantum ESPRESSO qe-7.4.1
commit 500de340b820e1cb8c05f2d8bb8fced102f377c1

ABINIT 10.6.5
commit d50172aacfc501b46cd33ae58fda139e674d40e3
```

PR #96 built the pinned sources and validated the deterministic first-point
inputs without a scientific run:

```text
workflow run 29623698323
artifact 8423244947
artifact digest
sha256:7835dddd59f042997daba935f15719030a31840f07516e3bc9b07c0150b14b9e
```

The compact persistent record is:

```text
first_principles/a0/cdte_a0_runtime_readiness_reference.json
```

It preserves source commits, executable hashes for the validated build instance,
runtime pseudopotential hashes, rendered-input hashes, syntax-output hashes, and
the no-calculation/no-result boundary.

A current-head revalidation reproduced all three rendered-input hashes and all
four pseudopotential hashes exactly. `pw.x` and `ph.x` also rebuilt
byte-identically. ABINIT produced a different executable hash because its binary
embeds build metadata; fresh ABINIT builds must be rehashed rather than assumed
byte-identical.

The GitHub runner's NetCDF library lacked parallel NetCDF-IO support. Single-rank
ABINIT dry validation passed, but multi-rank ABINIT production output is not
authorized by this record. Quantum ESPRESSO remains the primary A0 execution
backend.

## Validated first A0 point

```text
a_ref         = 6.476035479332049 Angstrom
ecutwfc       = 114 Ry
ecutrho       = 456 Ry
ABINIT ecut   = 57 Ha
k grid        = 4x4x4, unshifted
nbnd          = 40
SCF threshold = 1e-8 Ry
PH threshold  = 1e-10
```

Release-specific checks passed:

- QE `pw.x` completed `nstep=0` initialization and reported `JOB DONE`;
- every rendered `INPUTPH` key exists in the pinned QE definition source;
- ABINIT accepted the complete input with `input.abi --dry-run`, read both PSP8
  files, completed consistency checks, and explicitly skipped the driver.

These checks establish input and runtime readiness. They do not establish any
physical observable.

## Fail-closed readiness check

Generate the current report:

```bash
python tools/check_cdte_a0_readiness.py \
  --report-json runs/cdte_a0/readiness-report.json
```

Require every prerequisite before execution:

```bash
python tools/check_cdte_a0_readiness.py \
  --require-ready \
  --report-json runs/cdte_a0/readiness-report.json
```

The strict command also rejects any attempt to enable A1, AHC, dense EPW, HgTe,
or alloy work in the A0 record.

## Current state

Closed gates:

- physical fixed-volume provenance and bounded uncertainty;
- exact source-code pins;
- upstream and runtime pseudopotential hashes;
- installed runtime build records;
- deterministic first-point rendering;
- QE and ABINIT release-specific syntax checks;
- finite sequential convergence protocol.

Still unknown until calculations are run:

- total energy, stress, forces, and Gamma ordering at the selected point;
- cutoff, k-grid, band-count, and iterative-threshold convergence;
- phonon stability and acoustic-sum-rule residual;
- dielectric tensor and Born effective charges;
- wall time, memory, and scratch requirements.

No CdTe gap, phonon, dielectric, Born-charge, electron-phonon, HgTe, alloy, or
analytical-equation claim follows from readiness alone.
