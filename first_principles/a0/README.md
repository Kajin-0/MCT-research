# CdTe A0: pseudopotential and execution-readiness gate

This directory implements only the authorized A0 preparation and static/phonon
sanity stage from the CdTe thermal-moment decision memo. No electronic-structure
calculation or scientific result is recorded here.

## Authorization boundary

A0 permits only:

- static fully relativistic SOC calculations;
- coarse phonon-stability checks;
- dielectric-tensor and Born-effective-charge sanity checks;
- convergence and resource measurements needed to decide whether A1 is viable.

A0 does not authorize the timed A1 electron-phonon smoke test, production AHC,
dense EPW, HgTe, VCA, SQS, CPA, SCBA or alloy calculations.

## Selected pseudopotentials

The pinned upstream source is

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
spin-orbit data and nonlinear core correction. Cd has 20 valence electrons with
`4s 4p 4d 5s` represented; Te has 16 with `4d 5s 5p` represented.

PR #42 downloaded the exact immutable upstream bytes in an isolated workflow,
verified Git blob identities and published psp8 MD5 values, and recorded SHA-256
values in:

- `cdte_pseudopotential_hash_manifest.json`;
- `cdte_pseudopotential_selection.json`;
- `first_principles/pseudopotential_matrix.csv`.

The pseudopotential payloads themselves are not committed. Every runtime copy
must still be rehashed and match the recorded SHA-256 values.

## Cutoff-unit correction

PseudoDojo publishes cutoff hints in Hartree. Quantum ESPRESSO accepts
`ecutwfc` in Rydberg, so the hints must be multiplied by two.

| Element | low (Ha) | normal (Ha) | high (Ha) | low (Ry) | normal (Ry) | high (Ry) |
|---|---:|---:|---:|---:|---:|---:|
| Cd | 47 | 51 | 57 | 94 | 102 | 114 |
| Te | 34 | 40 | 46 | 68 | 80 | 92 |

Cd controls the compound starting ladder:

```text
94 Ry -> 102 Ry -> 114 Ry
```

These values are starting points, not convergence evidence.

## Lattice and fixed-volume protocol

`cdte_lattice_volume_protocol.md` defines the physical reference-volume gate.
The `6.482 Angstrom` entry remains a planning value only. An execution lattice
requires a hashed primary absolute measurement with temperature and uncertainty;
a transformation to the 0 K reference additionally requires a verified primary
thermal-expansion source and derivation manifest.

The sensitivity points are defined in volume:

```text
Delta V / V = -0.005, 0, +0.005
```

and are converted exactly through

```text
a / a_ref = (V / V_ref)^(1/3).
```

Issue #46 tracks acquisition of the absolute anchor and primary CdTe
thermal-expansion data.

## Declared convergence protocol

`cdte_a0_convergence_protocol.md` declares, but does not execute or certify, the
smallest sequential convergence plan:

- `ecutrho/ecutwfc = 4, 5, 6` at `ecutwfc = 114 Ry`;
- `ecutwfc = 94, 102, 114 Ry` after selecting the charge-density ratio;
- Gamma-centered cubic k grids `4, 6, 8, 10, 12`;
- noncollinear SOC band counts `40, 48, 56, 64` for the verified 36-electron
  primitive cell;
- tightening SCF and phonon thresholds;
- one selected-versus-next-denser cross-factor recheck.

A setting is selected only after two successive refinements satisfy every
applicable observable criterion. Failure at the largest declared point stops the
branch and requires a new decision memo.

Validate the plan structure without running a code:

```bash
python tools/check_cdte_a0_convergence_protocol.py \
  --require-valid \
  --report-json runs/cdte_a0/convergence-protocol-report.json
```

A passing protocol report means only that the proposed ladder is internally
consistent. It does not mean that any numerical setting is converged.

## Exact code-source pins

`cdte_a0_run_spec.json` pins the source trees selected for release-specific
syntax and reproducibility work:

```text
Quantum ESPRESSO qe-7.4.1
commit 500de340b820e1cb8c05f2d8bb8fced102f377c1

ABINIT 10.6.5
commit d50172aacfc501b46cd33ae58fda139e674d40e3
```

A source pin is not an installed-binary record. Before execution, archive:

- the complete version output;
- SHA-256 for `pw.x`, `ph.x` and `abinit`;
- compiler, MPI and linked-library versions;
- release-specific syntax-check results for every rendered input.

## Runtime pseudopotential inspection

Acquire runtime copies from the immutable upstream commit, then inspect and hash
every file. Example commands:

```bash
python tools/inspect_pseudopotential.py pseudos/Cd-sp_r.upf \
  --format upf --expect-element Cd --expect-z-valence 20 \
  --expect-functional PBE --require-fully-relativistic \
  --require-spin-orbit --require-nlcc \
  --output-json pseudos/Cd-sp_r.upf.inspect.json

python tools/inspect_pseudopotential.py pseudos/Te-d_r.upf \
  --format upf --expect-element Te --expect-z-valence 16 \
  --expect-functional PBE --require-fully-relativistic \
  --require-spin-orbit --require-nlcc \
  --output-json pseudos/Te-d_r.upf.inspect.json

python tools/inspect_pseudopotential.py pseudos/Cd-sp_r.psp8 \
  --format psp8 --expect-element Cd --expect-z-valence 20 \
  --expect-pspxc 11 --require-fully-relativistic --require-spin-orbit \
  --output-json pseudos/Cd-sp_r.psp8.inspect.json

python tools/inspect_pseudopotential.py pseudos/Te-d_r.psp8 \
  --format psp8 --expect-element Te --expect-z-valence 16 \
  --expect-pspxc 11 --require-fully-relativistic --require-spin-orbit \
  --output-json pseudos/Te-d_r.psp8.inspect.json
```

The runtime SHA-256 values must equal the byte-verification manifest. Upstream
Git SHA-1 and psp8 MD5 values are additional provenance anchors, not substitutes
for runtime SHA-256 verification.

## Input rendering

Use `tools/render_first_principles_input.py` only after runtime files pass
inspection. Supply every pseudopotential through `--input-file` so its SHA-256
enters the render manifest.

```bash
python tools/render_first_principles_input.py \
  first_principles/templates/qe/cdte_scf.in \
  runs/cdte_a0/scf.in \
  --parameters-json runs/cdte_a0/scf.parameters.json \
  --manifest-json runs/cdte_a0/scf.manifest.json \
  --input-file Cd_UPF=pseudos/Cd-sp_r.upf \
  --input-file Te_UPF=pseudos/Te-d_r.upf
```

The renderer fails on missing, unused or unresolved parameters. Rendering does
not execute a code and does not establish release-specific syntax validity.

## Fail-closed readiness check

`cdte_a0_run_spec.json` is the machine-readable execution contract.
`tools/check_cdte_a0_readiness.py` recomputes readiness rather than trusting a
manually edited Boolean.

Generate the current blocker report without authorizing execution:

```bash
python tools/check_cdte_a0_readiness.py \
  --report-json runs/cdte_a0/readiness-report.json
```

Require every prerequisite before an execution wrapper proceeds:

```bash
python tools/check_cdte_a0_readiness.py \
  --require-ready \
  --report-json runs/cdte_a0/readiness-report.json
```

The strict command exits nonzero while any blocker remains. It also rejects any
attempt to enable A1, AHC, dense EPW, HgTe or alloy work in the A0 record.

## Current blockers before A0 execution

The convergence ladders are now declared but have not been run. The repository
intentionally remains not ready because the following execution inputs are
unresolved:

1. installed QE/ABINIT version output and executable hashes;
2. release-specific syntax checks against the pinned releases;
3. the primary-experimental absolute lattice anchor and thermal-expansion
   derivation tracked by Issue #46;
4. runtime pseudopotential rehash and input-render manifests;
5. static ordering, cutoff/k-grid/band convergence, phonon stability, dielectric
   tensor and Born-charge results;
6. measured resources before any larger calculation.

No result should be inferred from the presence of templates, source pins,
pseudopotential hashes, declared ladders or a successful validator unit test.
