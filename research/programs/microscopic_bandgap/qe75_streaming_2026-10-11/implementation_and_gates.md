# Concrete implementation and resource gates

## Candidate implemented

Build with `-D__EXX_QSTREAM`; without it the stock storage path remains selected.
The private source edits `exx.f90`, `electrons.f90`, the PW CMake list and Makefile,
and adds the independent Fortran store module. A private copy of installed
`libqe_pw.a` replaces just the exchange/SCF objects and adds the store, then links
against existing QE 7.5 dependencies and a privately compiled PW main. This is
an economical **mixed-object candidate**, not a clean all-source release build.
The stock executable, archives, environment and scientific decks are untouched.

Per rank, store native complex vectors in one owned file under its unique outdir:
`prefix.exx_qstream.<me_pool>`. File position, in bytes, is

`1 + 16 R [(q-1) B + (b-lo)]`.

Checked 64-bit products reject overflow before creation. Each producer vector
must match shape and may be written once. Seal requires full coverage and exact
file extent; a reader cannot run on an unsealed generation. Load reads one
contiguous plane. No compression, lossy conversion, altered weights, occupied-band
trimming, reduced ACE projector count, transformed k/q mesh or solver change.
No whole-store memory temporary is required. The tested contiguous calls emit
no Fortran array-temporary warning. A fresh producer closes/deletes its previous
owned store; a stale file is rejected, so unique outdirs remain mandatory.

The proof does not authorize arbitrary raw access to `exxbuff(:,:,ikq)` from other
executables. The q-plane layout stays rank-3 allocatable, avoiding the additional
descriptor/ownership hazards of an allocatable-to-mmap-pointer substitution.

## Checkpoint obstruction, deliberately not hidden

Stock `electrons.f90` reloads an **old-density** full exchange buffer after an
`exxinit`, and exports it at interruption. A single cached q plane cannot replace
that old state. Reconstructing from current wavefunctions is not demonstrated
equivalent. Copying a second full buffer can require another nominal 22 GiB.
This first patch rejects hybrid restart import and fails before EXX checkpoint
metadata/export when a run is interrupted after exchange activation. It changes
workflow capability, not the converged Hamiltonian. It therefore does **not**
qualify the previous 3600+1800-s staged pilot, whose interruption semantics must
be handled explicitly before reuse. No restart file is falsely certified.

A concrete next implementation, if chosen, is a versioned per-rank stream
checkpoint that transfers ownership of the existing complete store without
copying it. Before destructive `exxinit` on import, retain/read that old store;
validate source fingerprint, FFT/band/q layout, rank decomposition and completeness;
then atomically commit a manifest only after all ranks report successful closure.
Do not trust filename/shape alone. Test crash-before/after-manifest, incompatible
old formats, changed MPI layout and interrupted generation. This is a **design**,
not implemented or restart-validated. An explicit no-resume validation scope is
another workflow option; neither is automatically authorized by this package.

## Actual resources versus mathematical allocation

After build-only work: available RAM **29.6853 GiB**, free disk **30.2920 GiB**.
The original native family reached 26.7221 GiB RSS and was stopped before full
ACE/SCF completion. No new runtime peak is measured.

Stream disk capacity is nominal **22 GiB aggregate**, with unknown local FFT
padding. Nominal residual disk is only about **8.292 GiB**, before new native
wavefunctions, checkpoints, runtime files and reserve. File capacity is not
extra purchased hardware, but it is a real resource obligation. A future
preflight must sum each rank's actual `16 R B Q` requirement, require adequate
free blocks/quota plus bounded output/reserve, and refuse tmpfs or an unintended
memory-backed scratch path. The modified code checks I/O errors but does not
yet preallocate blocks or enforce this aggregate disk admission gate.

**No full-memory certificate:** `temppsic_nc` and `result_nc` remain full target
spinor arrays; in a nominal full-352-band layout they together represent another
two q-plane-sized arrays (about 5.5 GiB). `xi(npwx*npol,352,nks)` remains, along
with reciprocal wavefunctions and solver/MPI allocations. Compiler/runtime I/O
buffers and filesystem clean/dirty cache matter. Fortran `FLUSH` does not promise
`fsync`, physical writeback or a bound on kernel dirty pages. The OS may reclaim
clean cache; no assumption that all cache is harmless or instantly reclaimable
is used here. Disk bandwidth and native HSE wall time are unmeasured. Loading
planes for three irreducible target k points can nominally read roughly 66 GiB
per complete ACE action, excluding energy/other actions and cache effects.

Before any native work: reconcile checkpoint behavior, fully build/audit the
chosen binary, test stock-versus-streamed native exchange/ACE on a small legal
fixture with identical FFT/MPI decomposition, and establish conservative actual
padding/scratch/peak guards. Such a fixture must have separately established
scope; none is queued or launched. Acceptance requires matching action, exchange
energy and ACE Gram/projector residuals at unchanged accuracy, safe observed
memory/disk and correct failure/cleanup behavior. Reject discrepancy, unsupported
mode, bad checkpoint, failed resource gate or absence of native comparison.
