# QE 7.6 / EPW 6.1 non-mutating replay boundary

**Program:** R02  
**Issue:** #355  
**Predecessor:** #350 / commit `743f34f8f3e0e9edbdf66185ffaa62df67ac4a6d`  
**Decision:** `REPLAY_BOUNDARY_SUPPORTED` at design level only

## Problem

The issue-350 patched serial replay returned zero and completed 216 electron self-energy calls, but the strict harness stopped because the replay changed `diam.epb1` and the predeclared literal completion markers were absent.

The design question is not whether that historical stop should be relaxed. It remains binding. The question is whether the pinned source supports a future replay protocol in which:

- consumed restart state is immutable;
- mutable outputs are created from absence;
- `.epb` serialization is suppressed;
- completion is established by release-grounded independent evidence.

## Pinned source

```text
repository                         QEF/q-e
QE / EPW                           7.6 / 6.1
commit                             9f93ddec427d2b9a45bb72d828c6d324f62fcabd
EPW/src/input.f90                  caf48c74542f522aeff9ed8431e27512999c3ced
EPW/src/readin.f90                 1f4a3bca3aa511d9782e3d50ce4c66d47f9f5589
EPW/src/ep_coarse_unfolding.f90    b9dcb97df833c42d1e3d793c5d66046a42c7ff77
EPW/src/epw.f90                    fca6e313d45ef636a81ca45b3585d2abe3124da5
EPW/src/stop.f90                   33e504b8c473ac5ca9ad26a59e56b8e5eda0c29a
EPW/src/printing.f90               5437074def616e315e85f3cdfd988fbabcbb1aeb
EPW/src/io/io_var.f90              39e6f840dea02719607f370ab743233575b01346
test-suite/epw_base/epw2.in        a30b69515a204f74d1565f43806efa72f064e67a
```

## `.epb` ownership

The pinned input declarations distinguish two unrelated restart layers:

```text
epbread   read coarse Bloch-representation epmatq from .epb pool files
epbwrite  write coarse Bloch-representation epmatq to .epb pool files
epwread   read Wannier-representation restart state
epwwrite  write Wannier-representation restart state
```

The defaults are:

```text
epbread   false
epbwrite  false
epwread   false
epwwrite  true
```

The coarse-unfolding control flow is decisive.

### Restart without `.epb` input

For:

```text
epwread = true
epbread = false
```

EPW skips the coarse `epmatq` reconstruction branch and later reports:

```text
Do not need to read .epb files; read .fmt files
```

### Independent `.epb` serialization

A separate block is entered when:

```text
epbread OR epbwrite
```

If `epbwrite=true`, EPW opens `prefix.epb<pool>` and writes:

```text
nqc
xqc
et_loc
dynq
epmatq
zstar
epsi
```

The tested issue-350 replay used `epwread=true`, `epbread=false`, and `epbwrite=true`. It did not consume `diam.epb1`, but it still entered the independent write block and replaced that file.

Therefore:

```text
diam.epb1 role                 optional coarse-Bloch serialization output
consumed by tested replay      no
required by self-energy        no
rewritten because              epbwrite=true
```

## Replay input delta

The proposed design input is:

```text
first_principles/b0/r02_epw_nonmutating_replay.in
SHA-256 e56d76aad9dd4fd6f8a5e2969bcc66ebff0fa468836cb2a313adffb11b5d8dda
```

Relative to the issue-350 replay input:

```text
epbwrite  true  -> false
epbread   false -> false, now explicit
```

All other values remain unchanged, including:

```text
epwwrite    false
epwread     true
wannierize  false
elecselfen  true
nest_fn     false
300 K
1.0 eV degaussw
3x3x3 coarse meshes
6x6x6 fine meshes
four-band manifold
```

The source places `epbwrite` only around the `.epb` serialization operation. It does not control interpolation or `selfen_elec_`. The change is therefore classified as output control, not a physical or self-energy parameter change.

Upstream `test-suite/epw_base/epw2.in` independently supports the restart semantics: it uses `epwread=true`, `epwwrite=false`, and `wannierize=false` while leaving `epbwrite` at its false default.

## State projection

A future replay should not clone the complete preparation tree verbatim. Preparation outputs must not become immutable replay inputs by accident.

### Preparation manifest

First manifest the complete successful preparation tree and reject:

- symlinks;
- special files;
- missing source-audited restart paths.

### Remove before seed construction

Remove all paths classified as:

```text
replay-declared outputs
transient runtime files
forbidden .epb files
```

### Immutable seed

Hash every remaining regular file. This includes unknown files conservatively, not only a minimal whitelist.

Required consumed paths include:

```text
epwdata.fmt
crystal.fmt
vmedata.fmt
dmedata.fmt
wigner.fmt
diam.epmatwp
diam.ukk
```

### Replay outputs

The initial declared output patterns are:

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

They must be absent from the seed and created by replay. Replacement of a preexisting declared output is not allowed because no declared output remains in the seed.

### Forbidden paths

```text
*.epb*
*raw*vertex*
```

An `.epb` file after a non-mutating replay is a terminal failure. Raw-vertex output remains forbidden because issue #355 is not an exporter test.

### Transient paths

```text
out.*_*
```

These are startup/runtime artifacts, not scientific completion evidence.

## Completion evidence

The previous literals `JOB DONE.` and `Electron Self-Energy` are rejected prospectively because they are not stable completion strings in the pinned EPW path.

A future replay must satisfy all independent conditions below.

### Process condition

```text
exit code = 0
```

### Fatal-condition exclusion

None of:

```text
SIGSEGV
Segmentation fault
Program received signal
Error in routine
%%%%%%
```

### Graceful program completion

The EPW main program calls `stop_epw()` after selected calculations. `stop_epw()` calls `print_clock_epw()`. The source-grounded timer section includes:

```text
Total program execution
```

This marker is necessary but not sufficient.

### Electron-self-energy execution

The timer summary must contain:

```text
selfen_elec_ : ... (N calls)
```

with `N > 0`.

### Physical result file

At least one file matching:

```text
linewidth.elself.*
```

must be:

- newly created from absence;
- nonempty;
- parseable with at least one finite numeric data row.

The I/O module classifies `linewidth_elself` as the physical-output unit for the imaginary electron self-energy.

No single condition can establish completion alone. In particular:

- exit zero without self-energy evidence fails;
- the total timer without `selfen_elec_` fails;
- a timer without a physical result file fails;
- a result file without graceful completion fails.

## Synthetic design oracle

The repository oracle performs no process launch. It supports:

- complete-tree hashing;
- pairwise path-class checks;
- preparation-to-seed projection;
- required consumed-path enforcement;
- immutable mutation/deletion detection;
- forbidden `.epb` detection;
- unknown-output rejection;
- Fortran numeric-row parsing;
- source-grounded completion evaluation;
- inert dry-run manifests.

Adversarial tests cover:

- missing consumed files;
- symlinks;
- path-class collisions;
- immutable mutation or deletion;
- `.epb` recreation;
- unknown output creation;
- exit-zero false positives;
- total-marker-only false positives;
- zero-call self-energy timers;
- missing or malformed linewidth output;
- fatal markers;
- replay-input hash drift;
- accidental execution authorization.

## Decision

```text
source ownership                    resolved
non-mutating boundary               supported at design level
completion evidence                 source-grounded
runtime validation                  not performed
classification                      REPLAY_BOUNDARY_SUPPORTED
```

The issue-350 stop remains unchanged. The allocation patch is not merged by this design, and no replay is authorized.

## Authorization boundary

Authorized:

- source/design records;
- inert replay input;
- pure Python policy and parser tests.

Not authorized:

- configure or build;
- patch application;
- preparation or replay;
- exporter execution;
- MPI, SOC, CdTe, HgTe, HgCdTe, A1, A2 or A3;
- automatic executable successor.
