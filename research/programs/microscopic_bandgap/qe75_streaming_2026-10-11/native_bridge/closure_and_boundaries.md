# State closure, lifetimes and precise remaining boundaries

## Native dependency audit

Pinned QEF QE 7.5: `770a0b2d12928a67048e2f3da8d10d057e52179e`.
The source transformer also checks the exact SHA-256 of the existing first
streaming candidate; it refuses a different private baseline. The original
private source is read, never modified by this phase.

| State | Owner/consumer | Capture/import candidate |
|---|---|---|
| Old real-space source spinors | `exxinit`, direct exchange readers | Sealed per-rank q store; checkpoint hardlink; read-only import; no source producer on restore |
| Old source weights | `x_occupation`, `x_nbnd_occ`, band partition | Exact weights in packet; occupied bound and partition recomputed from these old weights, not current `wg` |
| Old compressed exchange | `xi`, `vexxace_k` | Exact rank xi packet, columnwise without a full-xi temporary; native collected ACE is also captured/read |
| Current inner orbitals/weights | `wfcinit`, `c_bands`, `sum_band` | Collected current waves plus packet current `wg/et`; native wave import cannot fall back to atomic initialization |
| Current mixed density | `potinit`, `v_of_rho`, `set_vrs` | Completed native charge density; normal QE density/potential reconstruction, not inferred from old source spinors |
| Inner solver counter/history | `restart_in_electrons`, `restart_in_cbands`, `mix_rho` | Native `restart_scf`, optional `restart_k`, closed per-rank mix files; capture adds the missing natural-limit record |
| Outer HSE progress | `electrons` | Counter, stop mode, nine scalar values including `ethr`; old energy scalars restored before inner SCF |
| Mapping/encoding | Native FFT and G/q maps | Exact valid `igk_k` entries, q/symmetry mappings, FFT partition/maps, k/G coordinates; padding in `igk_k` is deliberately excluded |

The scoped domain remains CPU, norm-conserving, nonlocalized ACE, spinor k-point
SCF, one image/pool/band group/exchange group; no forces/stress or additional
Hubbard/RISM/SIC/field/ionic state. The target's 352 bands are retained. These
scope restrictions do not constitute proof of support for every other QE flag;
an admitted native profile must independently audit its exact deck and backend.

Sources: [exx](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/exx.f90),
[electrons](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/electrons.f90),
[init_run](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/init_run.f90),
[wfcinit/aceinit0](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/wfcinit.f90),
[native wave/ACE I/O](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/pw_restart_new.f90).

## Why additional scalar/history fields are necessary

**PROVEN UNDER SOURCE ASSUMPTIONS:** `electrons_scf` does not reset `ethr` on the
first inner iteration. The next outer iteration inherits the preceding solver
tolerance. A checkpoint that restores `tr2` but resets `ethr` to its input default
changes the subsequent diagonalization tolerance. Packet version 2 therefore
stores/restores `ethr` explicitly. Earlier local experimental codec version 1 is
refused; it was never a qualified restart or committed material result.

**CALCULATED / SOURCE-CHECKED:** actual unmodified `save_in_electrons` and
`restart_in_electrons`, linked against explicit tiny I/O/module stubs, show that
the zero-counter restart branch ignores saved `ethr/et`. Seeding them from the
packet beforehand preserves them; `dr2` starts at zero for iteration zero. This
test is a native routine control-flow check, not native MPI/HDF5 validation.

**PROVEN UNDER SOURCE ASSUMPTIONS:** the natural inner iteration-limit exit has
no `save_in_electrons` call in stock source. The candidate adds it at that exit.
Earlier explicit stops jump to label 10 and retain the original `iter` versus
`iter-1` distinction. The mixing buffer is closed KEEP before capture.

`mixrho_iter` is assigned the supplied iteration on each `mix_rho` call, and the
ordinary mixing records are reread from the closed buffer. Extra mixing channels
are excluded. At outer mode 2, stale inner history is refused rather than reused.
At inner iteration zero no past mixing history is required.

Sources: [SCF save](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/save_in_electrons.f90),
[SCF import](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/restart_in_electrons.f90),
[partial k save/import](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/save_in_cbands.f90),
[mix_rho](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/mix_rho.f90),
[buffer close KEEP](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/buffers.f90).

## Conditional operator continuation theorem

**PROVEN UNDER ASSUMPTIONS:** assume the immutable rank streams, weights and xi
were captured from one quiescent old EXX generation; native current waves and
density read back correctly; all profile/encoding/actual mapping checks pass;
the same supported physical input and arithmetic/backend are used; and exclusive
ownership and successful I/O hold.

The import setup creates the same host basis, screened kernel and partition.
It substitutes the saved old weights before finding the occupied bound, imports
old xi, opens the old stream read-only, and jumps past the entire source producer
and seal. It performs the ordinary temporary deallocation and representation
reset. It never calls `aceinit` on current orbitals during import. Thus the direct
exchange and ACE readers receive the same old-operator operands as at capture.
Those reader/factorization bodies are unchanged. The previously proved one-plane
storage theorem therefore applies to their old-operator actions as well.

This establishes operand closure under the assumptions. It does **not** prove
that actual native density/wave readback meets them, bitwise continuation of all
SCF variables, restart convergence, full runtime peak, or material accuracy.
The old/current-basis ACE counterexample remains valid and is not weakened.
Saving the complete structured source store is not declared intrinsically
incapable of reconstructing an old basis; the candidate preserves old xi directly.

## Publication and import lifetime proof

Both stop hooks close their typed rank packets and set `bridge_pending`; they
do not commit a checkpoint. `punch('all')` finishes native schema, density,
current collected waves and old collected ACE before the all-rank transaction.
Each MPI rank enters the barrier; one image ionode coordinates publication;
status is broadcast and a second barrier follows. Real MPI fault behavior is
**untested**; file-level two-rank stand-ins do not test collective failure.

**PROVEN UNDER STORAGE ASSUMPTIONS:** quiescent cooperating writers, exclusive
owned root, local ext4, successful file/directory fsync and atomic same-filesystem
rename give a global storage commit point at `CURRENT_NATIVE.json` replacement.
Every referenced rank/native member is already synced, hashed and linked to its
same inode. File/manifest checksums establish integrity, not semantic HDF5 validity
or protection from a malicious same-UID owner. SHA-256 is not a signature.

Import verification/retirement is called before `iosys/setup/init_run` reads or
rewrites native restart state. The pointer is durably retired before any mutation;
snapshot payload links are removed while live files remain. A receipt is issued
only after that step completes. A failed retirement has no import receipt and no
available checkpoint. There is **no rollback promise after consumption**.

Old qstore readers finish before producer replacement. The old handle is closed,
rank extent requests are closed, all fresh rank inodes are reserved, and the
producer opens those reserved inodes. Writes cannot reuse a checkpoint generation
with an available pointer. At stopped teardown the live stream is kept; committed
links independently preserve its bytes. The imported typed sidecar is deleted
only after restore, avoiding collision at the next capture.

The native root/monitor lifetime lease is an **unimplemented integration gate**.
The coordinator checks an owned live monitor receipt and ancestry, but this phase
does not implement, issue or validate a complete launcher/lease across real MPI.
No runtime admission profile exists. These limitations prevent a native fixture.

Durability source: [Linux fsync](https://raw.githubusercontent.com/mkerrisk/man-pages/master/man2/fsync.2).
No power-cut experiment or filesystem recovery test is claimed.

## Storage budget and exact remaining acquisition

For B bands, K local k points, Nt total k points and X=npwx*npol, the rank packet
has `240 + 8L + 8B Nt + 16B K + 16X B K` bytes, with L exact layout integers.
The xi serialization is **additional bounded state output**; native collected ACE
is retained too. We do not claim zero total state overhead. Serialization walks
contiguous columns; no whole q-store or whole-xi temporary is requested.
Checkpoint publication/import add hardlinks/metadata, not another 22-GiB store.

The native output envelope must include these packets, native waves/ACE, density,
mix history and metadata. Its bound is a prerequisite for a real fixture; tests
use a conspicuously synthetic 1-MiB envelope and tiny 192-byte rank streams.

**OPEN / NO-GO:** the independently guarded, full native MPI/HDF5 capture/import
roundtrip has not occurred. Needed evidence is one owned matched fixture showing
the old direct-EXX action/energy, xi/ACE action, old occupations, current waves,
density, inner/k/mix counters and both stop modes survive native continuation.
The existing action/energy tolerances and limits in `checkpoint_phase/native_fixture_protocol.md`
remain unchanged. Do not certify restart by filename presence, checksums, compiler
success, a synthetic roundtrip or exit status.
