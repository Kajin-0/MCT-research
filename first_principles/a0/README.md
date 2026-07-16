# CdTe A0: pseudopotential acquisition and input gate

This directory implements only the authorized A0 preparation stage from the CdTe
thermal-moment decision memo. No electronic-structure calculation has been run.

## Selected primary pair

The pinned upstream source is

```text
PseudoDojo/ONCVPSP-PBE-FR-PDv0.4
commit 7aa01a3fcf5ad226caf25bd387a9be9612be9f27
```

Selected files:

```text
Cd/Cd-sp_r.upf
Te/Te-d_r.upf
```

Matched ABINIT files:

```text
Cd/Cd-sp_r.psp8
Te/Te-d_r.psp8
```

The UPF headers identify norm-conserving PBE potentials with full relativity,
spin-orbit projectors and nonlinear core correction. Cd has 20 valence electrons
with `4s 4p 4d 5s` shells represented; Te has 16 with `4d 5s 5p` represented.

## Cutoff-unit correction

PseudoDojo's published cutoff hints are in Hartree. Quantum ESPRESSO accepts
`ecutwfc` in Rydberg, so the hints must be multiplied by two.

| Element | low (Ha) | normal (Ha) | high (Ha) | low (Ry) | normal (Ry) | high (Ry) |
|---|---:|---:|---:|---:|---:|---:|
| Cd | 47 | 51 | 57 | 94 | 102 | 114 |
| Te | 34 | 40 | 46 | 68 | 80 | 92 |

Cd controls the compound starting ladder:

```text
94 Ry -> 102 Ry -> 114 Ry
```

These are convergence starting points, not converged values.

`ecutrho` remains unresolved. Do not assume that any fixed multiple of `ecutwfc`
is sufficient without a total-energy, stress, force, gap and phonon convergence
check.

## Required local acquisition

Download from the immutable upstream commit, not from an unpinned default branch.
After acquisition, inspect every file and save the emitted JSON:

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

Record the locally calculated SHA-256 values in
`cdte_pseudopotential_selection.json` and `pseudopotential_matrix.csv`. The
upstream Git blob SHA-1 and PseudoDojo psp8 MD5 values are provenance anchors;
they do not replace a local SHA-256 of the exact bytes used by a calculation.

## Input rendering

Use `tools/render_first_principles_input.py` only after the local files pass
inspection. Every pseudopotential must be supplied through `--input-file` so its
SHA-256 enters the run manifest.

Example structure:

```bash
python tools/render_first_principles_input.py \
  first_principles/templates/qe/cdte_scf.in \
  runs/cdte_a0/scf.in \
  --parameters-json runs/cdte_a0/scf.parameters.json \
  --manifest-json runs/cdte_a0/scf.manifest.json \
  --input-file Cd_UPF=pseudos/Cd-sp_r.upf \
  --input-file Te_UPF=pseudos/Te-d_r.upf
```

The renderer fails on missing or unused parameters and unresolved placeholders.
A successful render does not imply that `pw.x` or `ph.x` accepts the input.

## Remaining blockers before execution

1. local SHA-256 verification of all selected files;
2. exact installed Quantum ESPRESSO and ABINIT versions;
3. a declared lattice constant and its provenance;
4. `ecutrho`, k-grid, band-count and SCF-threshold ladders;
5. release-specific syntax checks;
6. static ordering, phonon stability, dielectric tensor and Born-charge sanity;
7. measured resources from the one authorized A1 smoke test before any larger run.

A0 does not authorize AHC, dense EPW, HgTe or alloy calculations.
