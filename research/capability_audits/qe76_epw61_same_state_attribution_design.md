# QE 7.6 / EPW 6.1 same-state exporter attribution design

**Program:** R02  
**Issue:** #318  
**Predecessor:** #313 / PR #316  
**State:** design only; no EPW execution authorized

## Why a new design is required

Issue #313 completed one direct exporter-disabled and one direct exporter-enabled upstream diamond sequence. The raw complex-vertex evidence was internally consistent with EPW's scalar contraction, but the enabled and disabled standard outputs differed by:

```text
maximum self-energy difference  1.9286256500095078e-7 eV
predeclared limit                1e-12 eV
```

Both sequences independently regenerated SCF, phonon, Wannier, and interpolation state. The observed difference cannot distinguish exporter I/O from ordinary independent-run numerical variation.

The historical result remains `STOP_NONPERTURBATION_GATE`. This design does not reinterpret or relax it.

## Pinned upstream evidence

```text
repository  QEF/q-e
release     qe-7.6
commit      9f93ddec427d2b9a45bb72d828c6d324f62fcabd
```

Git blob identities at the pinned commit:

```text
EPW/src/epw.f90                     fca6e313d45ef636a81ca45b3585d2abe3124da5
EPW/src/ep_coarse_unfolding.f90     b9dcb97df833c42d1e3d793c5d66046a42c7ff77
EPW/src/wannier.f90                 a2b706939505a84b2d082e5a83a3dbb1ae8eef57
EPW/src/use_wannier.f90             104bfee94e9b32e5cb1f86c47382f34090393f3b
EPW/src/io/io.f90                   73fb24ecbf4b690c460006ec354d0b9a7772a044
test-suite/epw_base/epw1.in         624b4f8a47b003443a131f15afb7815b33a3398e
test-suite/epw_base/epw2.in         a30b69515a204f74d1565f43806efa72f064e67a
```

## Read/restart control flow

The pinned source establishes the following:

1. In `epw.f90`, `epwread=.true.` and `epbread=.false.` skip `setups`, `openfilepw`, and `init`; the restart therefore does not require the PW save tree.
2. `epw.f90` still calls `ep_coarse_unfolding`, `build_wannier`, and `use_wannier`.
3. Inside `ep_coarse_unfolding`, the `epwread` branch skips projector generation, coarse q-grid regeneration, external-eigenvalue loading, k-map generation, and coarse electron-phonon reconstruction.
4. That same branch reads `crystal.fmt` directly with `STATUS='old'` to restore crystal, mass, band-skip, Wannier-center, and related state.
5. When `wannierize=.false.`, `epw.f90` loads the existing band-manifold/rotation data through `loadbm` and the `.ukk` file.
6. In `build_wannier`, the `epwread` branch reconstructs the Wigner–Seitz cells from the saved Wannier centers, then calls `epw_read`.
7. The active replay path does **not** call `epw_read_ws_data`; the call in `wannier.f90` is commented. Consequently `wigner.fmt` is a preparation output retained by the complete-tree policy, not an active replay input in this source revision.
8. `epw_read` opens `epwdata.fmt`, `vmedata.fmt`, and `dmedata.fmt` with `STATUS='old'`. Under MPI, it opens `prefix.epmatwp` with `MPI_MODE_RDONLY`.
9. Upstream `epw2.in` demonstrates the restart controls:

```text
epwwrite   = .false.
epwread    = .true.
wannierize = .false.
```

### Source-audited consumed paths

```text
epwdata.fmt
crystal.fmt
vmedata.fmt
dmedata.fmt
diam.epmatwp
diam.ukk
```

### Source-audited preparation outputs retained in the clone

```text
epwdata.fmt
crystal.fmt
vmedata.fmt
dmedata.fmt
wigner.fmt
diam.epmatwp
diam.ukk
```

The design does not assume either list is exhaustive. Every regular file in the completed preparation tree is included in the immutable manifest and copied into every replay clone.

## Replay-input derivation

The committed replay input is:

```text
first_principles/b0/r02_epw_same_state_replay.in
SHA-256 6e36c722d58c90cb6d58ffdee06568d1803fdea41c1d1196f57c583e8add7b73
```

Relative to upstream `epw1.in`, exactly three restart-control values change:

```text
epwwrite    .true.  -> .false.
epwread     .false. -> .true.
wannierize  .true.  -> .false.
```

These values are taken directly from upstream `epw2.in`.

All physical and self-energy settings remain those of `epw1.in`, including:

```text
elecselfen  = .true.
nest_fn     = .false.
fsthick     = 15 eV
temps       = 300 K
degaussw    = 1.0 eV
4-band manifold
3x3x3 coarse k/q meshes
6x6x6 fine k/q meshes
```

No temperature, broadening, grid, band-window, projection, or self-energy parameter changes.

## Prepared-state policy

After one future preparation run completes successfully:

1. Stop all processes and flush the filesystem.
2. Walk the complete preparation directory.
3. Reject symlinks and special files.
4. Record every regular file with relative path, file type, mode, size, and SHA-256.
5. Require the source-audited preparation outputs.
6. Include unknown regular files rather than silently discarding them.
7. Create three byte-identical copies: `disabled_a`, `disabled_b`, and `enabled`.
8. Recompute and compare all three pre-replay manifests.

This complete-tree policy is intentionally stricter than a restart-file whitelist. It prevents an unrecognized saved-state dependency from differing between controls and treatment.

## Mutation policy

For each replay:

- every preexisting file must remain present;
- every preexisting file must retain mode, size, and SHA-256;
- no preexisting file may be mutated;
- new files are allowed only under predeclared output patterns;
- stdout, stderr, and the enabled raw-vertex file are opened outside the replay tree before process launch.

Any mutation, deletion, or unauthorized new file terminates attribution.

The initial allowed new-name patterns are limited to known EPW result and mapping products:

```text
EPW.bib
linewidth.elself.*
selecq.fmt
*.kgmap
*_0.kmap
*.freq
*.qdos_*
*.self
*.res*
```

A future execution issue must verify this list against the prepared-state manifest before running. It may narrow the list but may not expand it after observing replay output.

## Three-replay identifiability design

One prepared state and one replay input support:

```text
disabled_a  exporter variables unset
disabled_b  exporter variables unset
enabled     R02_EXPORT_RAW_VERTEX=1
            R02_EXPORT_IK_GLOBAL=1
```

All three use one executable hash, one replay-input hash, one environment definition, one thread configuration, one byte-identical prepared-state manifest, and separate immutable stdout/stderr paths.

No PW, PH, `pp.py`, Wannierization, or upstream-state regeneration is allowed during replay.

## Prospective attribution rule

For each parsed scalar component:

```text
A = disabled_a
B = disabled_b
E = enabled
```

First require baseline reproducibility:

```text
|A - B| <= 1e-12
```

The units are eV for energy and self-energy and dimensionless for Z/lambda-like quantities.

Only after the baseline passes, define the deterministic disabled interval:

```text
[min(A,B), max(A,B)]
```

Expand the interval on each side by the same fixed `1e-12` numerical floor. The enabled component passes only when:

```text
E >= min(A,B) - 1e-12
E <= max(A,B) + 1e-12
```

Every component must pass.

This rule preserves the original issue-313 standard, measures replay reproducibility before evaluating exporter treatment, and makes no statistical population claim from three deterministic replays.

If disabled A/B fails, attribution stops before interpreting the enabled replay. If enabled falls outside the envelope, exporter noninterference is not established. Threshold or floor fitting after execution is prohibited.

## Synthetic design oracle

The repository design tool performs no process launch. It provides:

- complete-tree SHA-256 manifests;
- required-path checks;
- clone-identity checks;
- pre/post mutation and deletion detection;
- allowed-new-output validation;
- deterministic attribution-envelope evaluation;
- inert dry-run replay manifests.

Adversarial tests cover missing restart files, symlinks, clone drift, state mutation or deletion, unauthorized outputs, unstable disabled baselines, enabled-envelope violations, nonfinite or shape-mismatched data, negative or incomplete thresholds, replay-input hash drift, and accidental execution authorization.

## Stop conditions

Stop at design or future execution if:

- the required preparation outputs are absent;
- three pre-replay manifests differ;
- any preexisting file mutates or disappears;
- a replay creates an undeclared file;
- disabled A/B exceeds the original numerical ceiling;
- enabled leaves the fixed disabled envelope;
- any physical parameter changes;
- any source, executable, patch, state, or replay-input hash drifts.

## Authorization boundary

Issue #318 authorizes source inspection, replay-input derivation, hashing/manifests, synthetic tests, and inert JSON only.

It does not authorize configure/build, state preparation, EPW replay, threshold fitting, SOC, CdTe, HgTe, HgCdTe, A1, A2, or A3.

A future execution requires a separate bounded issue after this design gate passes and merges.
