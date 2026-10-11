# Verified boundary

**CALCULATED — software tests only.** GNU Fortran 14.4.0 was installed into
private `.local/qe75_lowram_20261011/toolchain`, using project-local micromamba
and cache. Original installed QE/compiler environment was not modified. No
global install, permission escalation, hardware purchase or paid action.

1. Pristine actual QE 7.5 `exx.f90` compiled against installed matching-major
   QE modules: 2.625 s, maximum compiler RSS 170,664 KiB. No QE execution.
2. Patched `exx_qstream`, `exx`, `electrons` compiled with streaming enabled
   and disabled: **6 source-object validations PASS**. Private PW main and two
   tiny test optimization modes give **9 successful compiler invocations** in
   the final reproducible validation record. Compiler peaks remain small.
3. **24 tiny Fortran cases PASS**: 12 each at `-O0` and `-O2`. Normal test
   covers nontrivial spatial/spin rotation, both spinor time-reversal branches,
   nonunit lower band bounds, out-of-order/repeated q reads, two immutable
   generations, signed-zero/NaN payload preservation, toy direct-DFT spinor
   exchange action, and ACE-input Gram entries. Storage, contractions and Gram
   entries are bitwise identical in each comparison; maximum kernel difference
   is zero. No contiguous-call array-temporary warning. Offsets above 2 GiB
   are checked arithmetically without creating a large file.
4. Expected error exits reject missing/duplicate producer vectors, premature
   reads, post-seal writes, q/shape errors, pre-existing file, 64-bit overflow
   and deliberately truncated file. Errors cannot become a silently incomplete
   exchange action. These tests write only kilobyte-scale fixtures.
5. **8 independent source checks PASS**. Both active reader bodies become
   byte-identical to pristine arithmetic after removing only I/O/slot alias
   additions; every continued source read is counted. ACE routines and the
   excluded two-q localized routine are byte-identical; singleton orthopool
   definition is confirmed. Focused audit tests additionally reject deliberate
   source-index/weight defects and check provenance/resource arithmetic.
6. A private mixed-object `pw.qstream.UNVALIDATED` **links** with resolved
   shared dependencies and is hashed. Initial link omitted static `libmbd`;
   the installed QE CMake dependency graph supplied it. No new library build
   or PW invocation was needed. Link success is not runtime qualification.
7. Stock `pw.x` and `libqe_pw.a` hashes match intake; all **17** source/supervisor
   pins match, and the entire pre-existing dirty DFT status is identical. No
   native MPI family is present; no supervisor state is changed.

## Negative finding retained

An initial line-based subscript rewrite missed the **continued** source-spinor
density reads in `vexx_k`. Compilation and a standalone store toy cannot expose
that integration bug. Full source inspection rejected that draft. The final
patcher parses balanced subscripts across continuation lines and changes only
the buffer's third index; the independent operation-sequence audit catches a
deliberate recurrence. Earlier draft outputs are not used as final evidence.

The tiny kernel is a deterministic mathematical surrogate, **not actual QE FFT,
distributed MPI, a native ACE factorization, or material validation**. Producer
equivalence rests on the audited unchanged source operations; it has not been
tested at the physical 64³/352-band runtime. No SCF convergence, physical impurity
shift, bandgap or x_c is claimed. Full HSE peak and I/O runtime remain unknown.

Evidence: `validation.json` records commands/stdout/stderr/time and link hash;
`preservation_and_resources.json` records resources and all retained pins.
Reproduction scripts have no PW/MPI run path. Tests and source proof qualify a
candidate storage mechanism; the production gate remains closed.
