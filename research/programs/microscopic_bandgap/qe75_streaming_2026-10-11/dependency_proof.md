# Buffer lifetimes, dependencies and conditional equivalence

**PROVEN UNDER ASSUMPTIONS — source-conditioned storage theorem.** Source is
QEF QE 7.5 commit `770a0b2d12928a67048e2f3da8d10d057e52179e`; line numbers below
refer to pristine source. Installed QE is a conda build of this release, not a
claim of byte-identical upstream build flags.

## Lifetime audit

| Producer / consumer | Original data dependency | Candidate handling |
|---|---|---|
| `exxinit` 338–873 | Every local source band at each symmetry-expanded `ikq`; all bands intentionally prepared at 508–514; allocation 546–552 | Same producer order, FFT, spin rotation, spatial permutation and time reversal. Store one completed spinor vector immediately after CPU writes; seal only after full coverage |
| CPU `vexx_k` 1717–2180 | Each outer `iq` accesses only `ikq=index_xkq(current_ik,iq)`; source density and potential-result products | Load complete local q plane before contraction/OpenMP regions; both density and result products map buffer storage to slot 1 |
| `exxenergy` 2670–2756 | Calls `vexx`; no separate simultaneous-q requirement | Uses patched CPU reader |
| `exxenergy2_k` 3095–3411 | One source q plane per outer `iq`; target orbitals held separately | Same one-plane load and subscript mapping; global occupation/kernel indices unchanged |
| ACE 3825 onward | Builds `xi` from full-band `vexx`; factorizes exchange Gram matrix | `aceinit`, `aceinit_k`, `aceupdate_k`, `vexxace_k` byte-identical; `nbndproj=352` retained |
| `electrons` HSE outer loop | Old buffer/ACE remain available for old-potential energy; `exxinit` replaces generation only after that use | Store persists until next producer/deallocation, never freed at the end of ACE |
| `electrons` restart import/export | Reads/writes **all** of old `exxbuff` as a stock unformatted record | Explicit fatal rejection before import or before writing restart metadata; a cached plane is never emitted as a full checkpoint |
| `deallocate_exx` | Ends module buffer lifetime | Close/delete owned stream and deallocate cache |

All additional known readers were audited: Gamma-only routines; GPU routines;
`exx_stress`; `vexx_loc_k`; `loc_scdm_k`; augmented `us_exx`; `PP/open_grid`.
Localized `vexx_loc_k` needs two q planes at once, so it **cannot** use this proof.
The candidate rejects Gamma-only, GPU, localization, US/PAW, non-SCF, forces,
stress, multiple exchange groups and multiple pools before EXX allocation.
Only a private PW executable is linked; no patched PP tool is built or installed.
This is not a general QE library ABI/layout promise to external consumers.

## Source-conditioned theorem

Let each rank's immutable generation be matrices
`U_q ∈ C^(R×B)`, `R=nrxxs*npol`, `B=max_buff_bands_per_egrp`.
Assume:

1. CPU norm-conserving noncollinear spinor, nonlocalized ACE fresh SCF;
   `npool=negrp=1`, forces/stress disabled, no external direct-buffer consumer.
2. Every `(q,b)` is produced exactly once and the source generation remains
   unchanged until the next `exxinit` or EXX teardown.
3. Native unformatted stream I/O recovers the same 16-byte complex-DP values;
   shape, 64-bit offsets, completeness and I/O status checks pass.
4. Each active reader uses a single source q plane at a time. Original arithmetic,
   global q/occupation/symmetry indices, target/source loop order, FFT calls,
   distributed reductions and ACE factorization are unchanged.

Then replacing simultaneous `{U_1,…,U_Q}` with a lossless store and one resident
`U_q` gives the same reader operation sequence with the same operands. Induction
over its original loop order gives the same contractions and accumulated result
(bitwise under unchanged arithmetic execution). Consequently the exchange action
and energy sent to the unchanged ACE code are equal. This establishes storage
equivalence, **not** whole-program runtime equivalence or SCF convergence.

**Proof of producer coverage under one pool:** QE loops over all irreducible
host k points assigned to that pool and all `iexx_start:iexx_end` source bands;
the q loop accepts precisely the `index_xk(ikq)=current_ik` class. Each expanded
q has one class. With one exchange group, band partition covers all 352 bands.
The store separately checks absence of duplicates and omissions; it cannot
silently accept a failed assumption. Spin components are completed after the
existing OpenMP implicit barrier before writing. Reads occur before parallel
contraction regions and are not performed from concurrent worker threads.

**Proof of omitted broadcast:** QE's `mp_start_orthopools` sets
`nproc_orthopool=npool`. At `npool=1` the intra-orthopool communicator has one
rank; each broadcast transfers no data to a different rank. All intra-exchange
FFT gather/scatter and reductions across the six ranks remain present. The
multiple-group buffer ring is excluded by `negrp=1`.

**Memory identity:** original resident user allocation `16 R B Q` bytes becomes
`16 R B` plus `B Q` logical completeness flags and small I/O bookkeeping. For
`Q=8`, saving is exactly `7/8` of that array's capacity for any unchanged local
FFT padding. Aggregate nominal grid `64^3`, `npol=2`, `B=352` gives
23,622,320,128 → 2,952,790,016 bytes. Separate target/result spinors, `xi`, solver,
MPI/runtime allocations and kernel filesystem cache are outside this identity.

## Primary source provenance

[QEF `exx.f90`](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/exx.f90),
[QEF `electrons.f90`](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/electrons.f90),
[QEF `mp_pools.f90`](https://github.com/QEF/q-e/blob/qe-7.5/Modules/mp_pools.f90),
[QEF `exx_band.f90`](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/exx_band.f90).
The source theorem is an engineering application; no scientific novelty claim.
