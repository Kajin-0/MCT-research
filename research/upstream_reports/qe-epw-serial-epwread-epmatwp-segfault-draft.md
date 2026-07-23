# Draft upstream report: serial `epwread` segfault in `wigner_divide_ndegen_epmat`

## Summary

A serial QE 7.6 / EPW 6.1 restart using `epwread=.true.`, `epbread=.false.`, `wannierize=.false.`, and `etf_mem=0` segfaults in `wigner_divide_ndegen_epmat` before electron self-energy evaluation.

Source inspection indicates that the serial `epw_read` branch reads `epmatwp` without allocating it after the normal `build_wannier` allocation block has been bypassed. The MPI branch explicitly performs the missing allocation.

The proposed source change has not been compiled or executed.

## Version

```text
repository  QEF/q-e
commit      9f93ddec427d2b9a45bb72d828c6d324f62fcabd
QE          7.6
EPW         6.1
compiler    GNU Fortran on Ubuntu 24.04
build       serial QE executables with OpenMP enabled
```

The same `EPW/src/io/io.f90` Git blob is present at later checked commit `61569eb480231b649c47f631df9c5c83537df461`.

## Reproduction outline

Using the upstream `test-suite/epw_base` diamond fixture:

1. Build serial `pw`, `ph`, and `epw` executables.
2. Run the standard preparation sequence through `epw1.in`.
3. Preserve the complete prepared directory.
4. Replay only `epw.x` from the preserved state with an input derived from `epw1.in` by changing:

```text
epwwrite    .true.  -> .false.
epwread     .false. -> .true.
wannierize  .true.  -> .false.
```

All physical, mesh, temperature, broadening, band, and self-energy settings remain unchanged.

## Observed result

The preparation succeeds. The first exporter-disabled replay exits with code 139:

```text
Program received signal SIGSEGV: Segmentation fault - invalid memory reference.

#...
__wigner_MOD_wigner_divide_ndegen_epmat
  at EPW/src/wigner.f90:1009
__wannier_MOD_build_wannier
  at EPW/src/wannier.f90:452
```

The failure occurs before electron self-energy evaluation.

## Relevant source path

`epmatwp` is a five-dimensional allocatable array declared in `global_var.f90`.

In the normal non-restart `build_wannier` path for `etf_mem == 0`:

```fortran
ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc), STAT = ierr)
epmatwp = czero
```

That block is bypassed for `epwread` restart.

In `epw_read`, the MPI branch restores the allocation:

```fortran
#if defined(__MPI)
ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc), STAT = ierr)
epmatwp = czero
...
```

The serial branch has no visible allocation before:

```fortran
DO irg = 1, nrr_g
  CALL davcio(epmatwp(:, :, :, :, irg), lrepmatw, iunepmatwp, irg, -1)
ENDDO
```

`build_wannier` then calls:

```fortran
CALL wigner_divide_ndegen_epmat(epmatwp, ...)
```

which is where the observed run segfaults.

For one serial process, `ws_indexes_distribution` gives `nirg_loc == nrr_g`, so the existing allocation expression is sufficient for the serial direct-read loop.

## Proposed minimal source change

Move the existing allocation and zero initialization immediately before the MPI preprocessor branch:

```diff
       filint = TRIM(tmp_dir) // TRIM(prefix) // '.epmatwp'
       IF (TRIM(lsda) == 'down') filint = ...
       !
+      ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc), STAT = ierr)
+      IF (ierr /= 0) CALL errore('epw_read', 'Error allocating epmatwp', 1)
+      epmatwp = czero
+      !
 #if defined(__MPI)
-      ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc), STAT = ierr)
-      IF (ierr /= 0) CALL errore('epw_read', 'Error allocating epmatwp', 1)
-      epmatwp = czero
```

This preserves the existing MPI allocation expression and does not alter file offsets, record lengths, restart formats, or scientific calculations.

## Additional note

The MPI allocation has a fifth extent of `nirg_loc`, while `wigner_divide_ndegen_epmat` declares its explicit fifth dummy extent as `nrr_g`. The routine appears to index only local `ir_g_loc`, but the actual/dummy extent relationship may deserve a separate review. It did not cause the observed serial failure because `nirg_loc == nrr_g` in serial.

## Validation status

```text
source diagnosis supported   yes
minimal patch compiled       no
minimal patch executed       no
MPI behavior tested          no
```

This report is a source-level diagnosis and patch proposal, not a claim of a validated fix.
