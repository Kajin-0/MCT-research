# QE 7.6 / EPW 6.1 serial `epwread` `epmatwp` diagnosis

**Program:** R02  
**Issue:** #335  
**Terminal evidence:** issue #332 / commit `e48abeb2d691f4cef6e4048e0987e205773c728d`  
**Classification:** `SOURCE_DIAGNOSIS_SUPPORTED`  
**Execution:** prohibited

## Result

The pinned serial restart path lacks the `epmatwp` allocation required after `epwread=.true.` bypasses the normal `build_wannier` allocation block.

The source structure and observed backtrace jointly support this diagnosis with high confidence:

```text
normal preparation     allocates epmatwp -> fills -> writes
restart MPI            allocates epmatwp -> reads -> divides
restart serial         no allocation     -> reads -> divides -> SIGSEGV
```

The proposed correction moves the existing MPI allocation immediately above the MPI/non-MPI preprocessor split. It does not change the allocation expression, restart-file format, record layout, MPI offsets, or any scientific contraction.

The correction has not been compiled or executed.

## Pinned source

```text
repository                         QEF/q-e
QE release                         7.6
EPW version                        6.1
commit                             9f93ddec427d2b9a45bb72d828c6d324f62fcabd
EPW/src/global_var.f90             45ece671c03903d2186b118827cc5f7a31145da5
EPW/src/io/io.f90                  73fb24ecbf4b690c460006ec354d0b9a7772a044
EPW/src/wannier.f90                a2b706939505a84b2d082e5a83a3dbb1ae8eef57
EPW/src/wigner.f90                 85e7498a89e43632a5392f11828da9b247212223
```

A later checked source commit, `61569eb480231b649c47f631df9c5c83537df461`, has the same `io.f90` Git blob. The serial branch remains unchanged there. This is not merely a QE 7.6 vendor divergence.

## Observed failure

The same-state fixture completed:

```text
one build
six preparation commands
168-file complete-state manifest
three byte-identical replay clones
```

The first replay was exporter-disabled and failed before electron self-energy evaluation:

```text
workflow run       30020494017
artifact           8569280948
exit code          139 / SIGSEGV
routine            wigner_divide_ndegen_epmat
source             EPW/src/wigner.f90:1009
caller             build_wannier
caller source      EPW/src/wannier.f90:452
```

No exporter code was active. Therefore the exporter patch cannot explain the crash.

## Array ownership

`global_var.f90` declares:

```fortran
COMPLEX(KIND = DP), ALLOCATABLE :: &
  epmatwp(:, :, :, :, :),   &
  epmatwp_dist(:, :, :, :)
```

`epmatwp` is the five-dimensional Wannier electron-phonon matrix. Its effective dimensions are:

```text
band
band
real-space electronic vector
phonon mode
local electron-phonon Wigner-Seitz vector
```

`epmatwp_dist` is a separate distributed four-dimensional representation and is not used in the observed failing path.

## Normal preparation path

For `etf_mem == 0`, the non-restart branch of `build_wannier` performs:

```fortran
ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc), STAT = ierr)
epmatwp = czero
```

The array is then filled by the Bloch-to-Wannier transformation and written to `prefix.epmatwp`.

This allocation is inside the block skipped by:

```fortran
IF (epwread) THEN
  ...
ELSE
  ! normal allocation and transformation
ENDIF
```

Consequently a restart cannot rely on the normal-path allocation.

## Restart path

The restart branch:

1. reconstructs Wigner-Seitz sets;
2. calls `ws_indexes_distribution(nrr_g)`;
3. calls `epw_read`;
4. calls `wigner_divide_ndegen_epmat(epmatwp, ...)`.

### MPI reader

The MPI branch of `epw_read` explicitly performs:

```fortran
ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc), STAT = ierr)
epmatwp = czero
MPI_FILE_READ_AT_ALL(...)
```

The missing normal-path allocation is therefore replaced for MPI restart.

### Serial reader

The serial branch performs:

```fortran
DO irg = 1, nrr_g
  CALL davcio(epmatwp(:, :, :, :, irg), ..., -1)
ENDDO
```

No `ALLOCATE(epmatwp(...))` is visible in this branch or in the common restart path before the read.

The same unallocated array is then passed to:

```fortran
wigner_divide_ndegen_epmat
```

The observed backtrace terminates at its first array division.

## Distribution dimensions

For `use_ws == .false.` or `etf_mem == 0`, `ws_indexes_distribution` partitions the combined range:

```text
1 .. nrr_g * nmodes
```

and derives:

```text
irg_start = floor((irn_start - 1) / nmodes) + 1
irg_stop  = floor((irn_stop  - 1) / nmodes) + 1
nirg_loc  = irg_stop - irg_start + 1
```

### Serial one-process case

```text
irn_start = 1
irn_stop  = nrr_g * nmodes
irg_start = 1
irg_stop  = nrr_g
nirg_loc  = nrr_g
```

Therefore the existing allocation expression is correct for serial execution:

```fortran
ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc))
```

because `nirg_loc == nrr_g`.

### MPI case

```text
nirg_loc <= nrr_g
```

The existing MPI allocation already uses `nirg_loc`. Moving the same allocation above the preprocessor split preserves that behavior.

## Root-cause ranking

### 1. Missing serial restart allocation — supported

Evidence:

- normal preparation allocates before use;
- restart bypasses that allocation;
- MPI restart explicitly replaces it;
- serial restart does not;
- the first serial replay fails when the array is divided;
- the exporter was disabled and self-energy evaluation had not begun.

Confidence: **high**.

### 2. Restart-file corruption or record-length mismatch — unlikely primary cause

The preparation and replay used the same executable and compiler, and the complete restart tree was copied byte-for-byte. Direct-access Fortran I/O can be compiler-dependent, but a missing allocation independently explains the failure.

Confidence: **low**.

### 3. `STATUS='unknown'` — not supported as the observed cause

The required file existed in the immutable manifest. A stronger `STATUS='old'` would be preferable for fail-closed restart semantics, but the backtrace is an array operation rather than a file-open error.

Confidence: **very low**.

### 4. MPI actual/dummy fifth-dimension mismatch — latent separate risk

The MPI allocation uses `nirg_loc`, while `wigner_divide_ndegen_epmat` declares an explicit fifth dummy extent of `nrr_g`. The routine indexes only local `ir_g_loc`, but the declared global extent is larger than the actual local allocation when distributed.

This did not cause the observed serial failure because `nirg_loc == nrr_g` for one process. It should not be silently repaired in the same patch without a separate source proof.

## Historical context

Relevant upstream history shows that sequential `epmatwp` handling has required dedicated fixes before:

```text
cbd08e75df513def922f37272d5f3c1ef1b78928
  Restart with arbitrary number of cores after epmatwp has been written

9707a90417d4b2915c2345c23d2f7aeb8f752c9c
  Debug closing epmatwp file in sequential

a3e738ab6e6f436d08ee54d68406eac196b784c2
  Debug sequential version and epmatwp file-unit handling
```

These commits do not prove the present allocation diagnosis, but they establish that serial and MPI restart lifecycles have historically diverged.

## Minimal patch design

The inert proposal moves:

```fortran
ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc), STAT = ierr)
IF (ierr /= 0) CALL errore(...)
epmatwp = czero
```

from inside `#if defined(__MPI)` to immediately before it.

This creates one common allocation for both readers.

### Preserved behavior

- MPI shape remains `nirg_loc`.
- MPI offsets and counts are unchanged.
- Serial direct-read records are unchanged.
- File names and record lengths are unchanged.
- Restart formats are unchanged.
- Wigner degeneracies are unchanged.
- Electron-phonon matrix values are unchanged.
- Self-energy and all scientific contractions are unchanged.

### Static proof obligations

1. Exactly one restart allocation exists for `etf_mem == 0`.
2. Serial `nirg_loc == nrr_g`.
3. Every serial `irg=1..nrr_g` read fits the fifth extent.
4. Every local Wigner index fits the fifth extent.
5. MPI retains the same allocation expression.
6. No MPI offset, broadcast, or file-I/O line changes.
7. No physical or scientific expression changes.

The repository synthetic model checks obligations 1–5. Obligations 6–7 are checked from the inert patch text.

## Decision

```text
classification                SOURCE_DIAGNOSIS_SUPPORTED
observed failure explained    yes
patch compiled                no
patch executed                no
MPI correctness validated     no
scientific capability restored no
```

A runtime test of this patch would require a separate bounded issue. It is not authorized here.
