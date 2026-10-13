# Matched 48-band initial-state protocol — software gate, not a generated seed

**New source-level result:** pristine QE `randy` defaults to seed 0 in a fresh
process. The static NC HSE+SOC SCF scope does not take `setup`'s MD/temperature
clock-seeding branch. The compiled pristine RNG gives identical 128-value byte
streams in two fresh serial processes. One extra call produces a different
stream: fixed seed alone cannot certify a matched start. Geometry, local G
order, random-call history, atomic initialization/rotation, compiler/backend and
all initialization fields must match as well. This does not assume independent
atomic+random starts are observed identical in MPI.

Two possible future routes are now precisely distinguished:

1. **Unchanged from-scratch decks:** keep the existing 48-band physical/numerical
   whitelist. Under identical startup path, actual layouts, call histories and
   arithmetic, initial waves are deterministic. Capture and compare *all* states
   after `potinit`/`wfcinit`, before SCF. A source proof is conditional; actual
   packets must pass. Fail the paired experiment if they differ; do not silently
   rotate phases, equate subspaces, retry random seeds or fit a mismatch away.
2. **Immutable native 48-band seed:** only after independently admitted native
   generation, a correctly fingerprinted matching save can feed both members.
   This changes the startup protocol/whitelist and is not issued here. Input
   wave/density/et/layout hashes, strict no-random-fallback readback, and bounded
   copies into separate writable roots are required. Hardlinking immutable input
   into native overwrite paths is unsafe. The old 44-band/k4/Fock180Ry state
   cannot supply this route; no extra bands are fabricated.

The new **read-only observation hook** is inserted after `wfcinit` in both private
`init_run` objects. It serializes 48-band coefficients, physical Miller labels,
k coordinates, actual dense/smooth FFT maps, density-G labels, et/wg, real and
reciprocal density and potential. It reads existing buffers; final local-k evc
is restored by the last read, matching the scoped native initialization end.
It does not set RNG state, replace coefficients, density or occupations, run a
solver, or alter the original 352-band files. Padding is serialized as zero
using only a one-padding-column scratch vector; irrelevant uninitialized padded
values must not cause false mismatch. Every recoverable local write error is
reduced with real QE `mp_max` before the next k/barrier. Actual MPI progress and
readback remain unexecuted; dead-rank recovery still belongs to the guardian.

The observation packet is native-endian/versioned and binds a **shared common
input ID**, separately from live run PROFILE/JOB authorization. Run PROFILEs
include different executable/owned-path identities and must differ between
control and streamed modes. Requiring their equality would falsely reject the
pair. `common_input_id` derives the shared ID from the exact whitelisted physical/
numerical decks, PP/source pins, rank/group scope and common backend identity.
Each future run PROFILE must bind this field, and its guardian must set
`QE75_COMMON_INPUT_SHA256` accordingly. That native environment/publication gate
is unissued; supplied backend strings alone are not live certification.
The checker
requires the exact two-rank/k set, equal corresponding packet bytes, finite
fields, distinct physical reciprocal ownership and the summed NC full-band Gram
error <=1e-12. It refuses phase-only equivalence, changed maps or density,
44 bands, missing peers, truncated/corrupt packets and oversized inputs before
reading their payload. The 128-MiB parser cap is an explicit fixture guard, not
proof that every native layout fits it; actual extent admission remains needed.
Raw observations contain no global all-rank certificate until every file passes.
Their certificate is **not native launch authority** or a scientific result.

**PASS SOFTWARE:** both real-QE objects compile; independent synthetic 48-band
packets compare bitwise and the checker rejects the stated counterexamples.
**OPEN / BLOCKED NATIVE:** no native 48-band common wave/density packet exists,
no MPI common-start proof has been observed, and original admission still needs
actual layout/backend/startup certification before a launch. Software progress
does not waive this gate. Next independent item: exact conditional extents and
conservative FFT/lifetime bounds.
