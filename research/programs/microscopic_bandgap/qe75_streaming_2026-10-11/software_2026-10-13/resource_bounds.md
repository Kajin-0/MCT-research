# Exact conditional extents and conservative source bounds

**Scope:** pinned 2-atom primitive HgTe cell (cubic a=6.46 Angstrom), CPU NC SOC,
48 bands, 90/360/120-Ry cutoffs, unshifted k2/q2, one pool and one band/task group,
two ranks, FFTW/default dimension-padding path and symmorphic FFT factors 1 or 2.
Nothing changes the original 16-atom/352-band inputs. True native maps,
decomposition and FFT factors remain UNKNOWN until independently certified.

## Geometry and parallel-workspace proof

For physical primitive vectors a_i and G=sum h_i b_i, with a_i.b_j=2pi delta_ij,
Cauchy gives |h_i|<=r|a_i|/(2pi) whenever |G|<=r. Native `grid_set` takes the
maximum integer indices and returns 2*max+1. Pristine `good_fft_order` rounds to
an allowed 2/3/5 order; default `good_fft_dimension` adds no padding. Outward
cell/Bohr/pi intervals containing the pinned constants and floating roundoff
give integer bounds 13 (wave), 15 (Fock), 26 (density). Native non-Gamma EXX uses
max(120,(sqrt(90)+max|k|)^2): the unshifted primitive k2 representatives have
max|k|<=2pi/a, so 120 still dominates. Thus global orders are <=32^3 Fock and
<=54^3 dense, under the stated FFT-factor condition.

The native `fft_type_set` local workspace is a maximum of stick, real-space and
all-to-all extents, including
`ncpx*nr3px*nproc3` and `nr1px*nr2px*nr3px*nproc2`. Every factor has its natural
global bound, so local `nnr <= P*nr1x*nr2x*nr3x`, P=2. It need not be global
volume/P. An uneven-stick counterexample disproves that shortcut. This package
uses the safe P*V bound, not an assumed balanced layout.

The k2 mesh is the finite group (Z/2)^3 modulo reciprocal translations. q2
addition and integer lattice symmetry preserve it; native `exx_qgrid_init`
identifies points modulo NINT translations. Noncollinear scope has one LSDA
channel. Therefore local/global k and distinct stored auxiliary q counts are
<=8; the runtime q mesh must still be checked unchanged. This does not assert
which native IBZ representative/order or rank owns a point.

`bounds.py` combines these limits with the pinned qdiag/state layout expressions.
It bounds G sets by enclosing integer boxes, layouts by their actual constituent
arrays, and uses the existing checked signed-64 component formulas. The
common-state packet's exact extent is

```
208 + 8L + 24*npw + 16*npwx*npol*B + 16*B*Nt
    + 16*nrho*nspin + 16*ngrho*nspin
```

The initial layout bound includes dense/smooth nl maps and density Miller
labels. The conservative packet limit is below the 128-MiB parser cap under
these scope conditions. Files are block-rounded individually. Aliases of one
owned inode are counted once; overlapping old/new generations count separately.
The lifecycle calculator requires the live inode set at each phase rather than
silently assuming a single generation or charging hardlinks as copies.

## What is established and what is not

**PASS SOFTWARE / SOURCE-CONDITIONED:** exact codec sizes agree with emitted
48-band serial files; overflow/unknown-inode refusals and 512 pristine QE
size/padding cases pass. Conservative component numbers and compiler/source
provenance are in the JSON evidence. They are allocation/payload bounds, not
measured native memory, allocated HDF5 blocks, MPI layouts or SCF equivalence.

**Negative:** equal dataset payload does not determine an HDF5 file's block
allocation. Two serial HDF5 files with identical 48-value data and different
metadata are independently checked to occupy different block counts. This is
not a claim that pinned QE arbitrarily emits metadata: a complete certificate
must supply bounds for its actual producer/library/version and replacement
temporaries. Array payload alone cannot supply them.

**Complete envelope remains BLOCKED:** native HDF5/metadata, XML/log/mix and
full native-file inventory/generation lifetimes, allocator/FFT/MPI/backend peak
workspaces and actual descriptors are still missing. These cannot be replaced
by an arbitrary 1-GiB allowance. The native admission function explicitly
refuses UNKNOWN descriptors or absent independent extras. Retain sampled
12/4/10-GiB/600-s guards; component arithmetic does not make them continuous
hard bounds. No large file/store, FFT transform, MPI communicator or QE run is
launched. Next independent software item: source-level collective/readback
failure semantics, preserving this missing-envelope boundary.
