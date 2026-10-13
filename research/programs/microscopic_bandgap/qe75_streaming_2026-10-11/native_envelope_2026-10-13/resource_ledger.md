# Two-atom native producer/allocation ledger — 2026-10-13

**SOURCE-CONDITIONED selected bounds; COMPLETE NATIVE ENVELOPE NOT CERTIFIED.**
The scope is the retained CPU norm-conserving HgTe fixture: two atoms, 48 spinor
bands, 90/360/120-Ry wave/density/Fock cutoffs, k2/q2, one pool/band/EXX/task
group and two world ranks. The original 352-band experiment is unchanged.
`source_pins.json` pins the inspected sources; `envelope.py` contains checked
signed-64-bit expressions. No native run or actual FFT descriptor exists.

## Exact producer expressions and lifetime corrections

Let Gk be the global **active compact** k+G count, Gd the global density count,
g the local smooth count, N the padded local wave count, B=48, p=2, s=4,
K<=8 and m the mixing history length. These are variable descriptors, not
measurements. Prior conservative bounds give Gk,N<=19,683 and Gd,g<=148,877.

| Producer / source | Selected bytes or count | Lifetime / qualification |
|---|---|---|
| `pw_restart_new.write_collected_wfc` + `gk_l2gmap_kdip`; `io_base.write_wfc` | per wfc **or** ACE dataset payload `(16 p B + 12) Gk` | Both have `MillerIndices` as well as `evc`. File attributes and format allocation are additional. Helper compacts original density-G labels to `1..ngk_g`; the original maximum label can exceed Gk. |
| Collected writer parent arrays | `20 N + 4 K` | `igk_l2g`, compact map, `mill_k`, `ngk_g`; persist across each file's writer. |
| Map-helper arrays | conservatively `8 Gd + 4 Gk` | Two density-label-indexed arrays plus compact list; helper finishes before HDF5 gathers. Do not size them using Gk alone. |
| Wave root gather | `max(12 Gk, 16 p Gk)` | Miller buffer is freed before complex-column buffer. Neither is the entire wave matrix. Native `mergekg`/`mergewf`/MPI internals are separate. |
| `io_base.write_rhog` | dataset payload `(16 s + 12) Gd` | One Miller dataset and four complex spin datasets. Miller buffer freed before `rho_g` and `rhoaux`. Selected root gather peak `max(12 Gd,16 Gd+16 glocal)`. |
| `qeh5_module` | default contiguous, unfiltered datasets; complex pointer supplied to real-DP H5Dwrite | No QE-side entire complex-to-real matrix copy in that call. This does **not** prove zero HDF5/backend conversion or cache memory. File creation uses default properties and truncation. |
| `scf.open_mix_file` / `mix_rho` | record `16 g s`; max record index `2m+2`; `m<=25` | Scoped ordinary HSE/NC response excludes meta/XDM/U/PAW/dipole/SIC/GC-SCF/plugins. Native defaults are m=8 and **io_level=0 for SCF**, derived from `read_namelists` / `input`; this fixture omits disk_io. Actual fields are still captured/checked. |
| `buffers.open_buffer` / `close_buffer(keep)` | `(2m+2)16gs` logical mixing store | io_level>0: direct-access disk during SCF. io_level=0: RAM records, **then disk dump on keep BEFORE RAM records are freed**, with one extra record vector. Index metadata is separate; initial 1024 entries are pointers, **not 1024 full data records**. Both stop paths can keep history. |
| `create_mix_type`, `mix_rho`, `io_buffer` | `(2m+3)16gs` selected data plus small mixing matrix/work arrays | df/dv coexist with input/output mixing objects and io_buffer; the disk history does not replace these arrays. Extra local-TF arrays need their own entry if that mode is admitted. |
| EXX q store | retained conditional two-rank full store <=1.5 GiB, one resident plane <=192 MiB | Logical stream, block rounding and actual reserved inode extents differ. The old checkpoint's generation/alias ownership contract remains mandatory. |
| Current `evc`, `evc_exx`, old `evc0`, ACE `xi` | generally `16 p N B` times source live multiplicity/k count | Parent persistent arrays, current transforms and old/new operator lifetimes must all be included. Never infer multiplicity from one printed memory estimate. |
| `exxinit` scratch | NC global gather arrays `psic_all_nc`, `temppsic_all_nc`; local `psic_nc`, `temppsic_nc`, `psic_exx` | Both global and local grids appear. A local FFT workspace need not be global volume/2. New observer is after transform/FFT initialization and before these gathers/exxbuff; it is not a pre-run peak certificate. |
| First-ACE diagnostics, old-operator packets, common-wave capture, FFT packets | retained checked packet formulae plus new labelled FFT arrays | Include I/O buffers, integer conversion temporaries and all retained per-k/per-rank files. File observation cannot stand in for native SCF readback. |
| Restart density/potential, XML/schema, copied pseudopotentials, mixing/wfc/exx direct buffers, other native scratch | additional producers | Enumerate actual live inode generations and native I/O mode. Each unenumerated producer stays UNKNOWN. |
| stdout/stderr, guardian log, backend errors/debug logs | additional producers | Native/Fortran output widths and iteration counts do not bound external MPI/plugin diagnostics. Current sampled output guard is **not** a hard write quota or bounded log sink. No guessed byte allowance is inserted. |
| FFTW/ELPA/BLAS/MPI/HDF5/allocator | additional RSS | FFTW3 uses `FFTW_MEASURE` and explicit `ALLOCATE(...,mold=...)` planning copies; cached plans persist. ELPA/BLAS workspaces, MPI transport/plugins/collective staging, caches, stacks, fragmentation and shared mappings are not the arrays above. |

**CALCULATED, conditional:** one collected wave+ACE generation's dataset
payload <=487,508,544 bytes; one density payload <=11,314,652 bytes. Miller
datasets add **5,565,660 bytes** to those selected producers. Selected wave
parent/map/gather peak <=1,663,440 bytes; density gather <=4,764,064 bytes.
Plain m=8 mixing history logical store <=171,506,304 bytes/rank and selected
live mixing arrays <=181,035,040 bytes/rank. These loose box bounds are not
whole native RAM/disk estimates; independent source/library terms remain.

**Decision-changing source finding:** the legal unchanged fixture defaults to
RAM buffering, not direct disk. Its mixing store and df/dv arrays must both
enter RSS. `close_buffer(keep)` means io_level=0 **does not imply zero disk
output**; include the transient RAM+disk overlap in the stop/punch envelope.
Wave buffering is also in RAM by default: selected two-rank padded wave
record payload <=483,729,408 bytes. We change accounting, not `disk_io` or
any fixture physics to hide this allocation.

## Disk envelope equation

For each owned live inode i, write a certified logical/data bound bi and a
certified nonpayload allocation bound hi. With filesystem block a, the data
charge is `ceil(bi/a)*a`; add hi, per-directory/filesystem metadata and quota
charges. Peak disk is the maximum **union of distinct live inode identities**
across phases. Hardlink aliases count once; two replacement/generation inodes
count twice when they coexist. Apply the existing resource contract to actual
per-rank reservations, output escrow **and future output**, plus the unchanged
10-GiB reserve. Do not count escrow as already-written native output.

The new `require_complete` refuses UNKNOWN HDF5 allocation, logs, XML/PPs,
miscellaneous files, generations, filesystem/quota and packet/manifest terms.
Even numerical allowances alone cannot issue native admission: their provenance
and phase coverage would still need qualification.

## RSS envelope equation and explicit obstruction

For rank r and phase t, the array bound is the sum over allocations **live in
that phase**, including compiler argument temporaries. Add that rank's backend
workspace, allocator/stack/library mapping allowance. Sum across ranks and all
owned launcher/guardian descendants and foreground owner; retain the existing
shared-RSS overcount policy. Take the phase maximum. Keep MemAvailable and
kernel/page-cache pressure as separate system predicates; RSS alone does not
bound them. The existing guard samples these predicates and never claimed
continuous hard enforcement.

All parent PW allocation phases, compiler temporaries and the pinned backend
working sets are not currently certified. SHA256 identifies a library; it
does not bound its workspace. In particular FFT planner copies and old/new ACE
coexistence invalidate “exxbuff plus a little overhead” reasoning. A complete
12-GiB certificate cannot be issued by adding arbitrary slack to known arrays.

## Independent tiny native-library check and stopping boundary

`hdf5_check.py` compiles an isolated writer against the **pristine qeh5 object**
and installed HDF5, with the retained MPI-initialization trap. Four tiny
files (wave/density, G=17/257) independently verify datasets, attributes,
storage sizes, exact synthetic values and contiguous/unfiltered defaults.
They emulate these producer schemas; they are not `io_base` MPI gathers or
full native files. All files total less than 1 MiB. Observed wave nonpayload
bytes differ (6,188 versus 4,344); density nonpayload is 4,096 in these cases.
These are **measurements**, not extrapolated universal metadata bounds. The
largest serial child RSS was 54,356 KiB including the compiler. No PW/MPI ran.

**BLOCKED whole envelope:** the complete producer/generation audit and pinned
backend workspace proof or independently qualified measurement are still
needed. Further synthetic sizes cannot establish those missing statements.
Native observations cannot be acquired while host-wide admission is
HARD_BLOCKED. This phase closes the concrete payload/lifetime omissions and
installs the descriptor observer; it does not manufacture admission.
