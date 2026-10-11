# Storage commit proof and native-state boundary

## What is implemented and proved

**PROVEN UNDER ASSUMPTIONS:** on local ext4 with successful file/directory `fsync`,
quiescent sealed owned files, and cooperative exclusive checkpoint ownership,
the backend publishes a complete byte-integrity checkpoint or refuses it.
Its commit point is one atomic replacement of `CURRENT.json` after all member
data and the generation manifest are synced. SHA-256 is an integrity check,
not a signature or protection against a malicious owner.

Per-rank roles are `stream`, `exx_state`, `native_state`. Each stream/state member
is linked to the generation directory using the **same device/inode**; its payload
is not copied. Native state files are opaque here: presence/checksum never proves
their semantic completeness. The manifest is deliberately marked
`native_QE_restart_qualified=false`; `require_native=True` always refuses until a
separately audited bridge exists. Tests use conspicuously synthetic state
placeholders and cannot turn them into native QE packets.

Protocol:

1. Freeze/seal all rank sources. Reject missing ranks/roles, symlinks, foreign
   files or changed payloads. Record exact version, rank/FFT/band/q/native encoding
   layout and source/input/PP/state provenance.
2. Sync data, hard-link members, hash/check identities, sync the generation
   manifest and directories. Stage and sync a small global pointer.
3. Atomically publish the pointer and sync its directory. Before publication no
   checkpoint is available; after publication every referenced member is complete
   and hashed. A failed post-rename acknowledgement may still leave a valid
   checkpoint; verification determines that, never an exit code alone.
4. A Fortran `CLOSE(...,STATUS='delete')` may remove the live name while the
   committed hard link retains the data. Adoption recreates active links only
   after checks; unrelated active files block it. The storage adapter imports a
   validated active link as **sealed/read-only**, and rejects producer writes.
5. After **all** old-potential readers finish, close live handles, durably retire
   the committed pointer, then release exact owned names before replacing a full
   generation. A crash after retirement means no available checkpoint; it never
   means permission to restore overwritten old bytes. Cleanup only touches
   generation names whose identity/integrity and ownership were recorded.

**Limitation, not concealed reliability:** this is not rolling last-checkpoint
retention through arbitrary new-generation replacement. For unconstrained raw
byte streams of size B, simultaneous lossless retention of arbitrary old and new
streams has a worst-case 2B information requirement. That statement concerns
raw storage, not an impossibility theorem for QE's structured/recomputable orbital
data. A different representation or recomputation could change the requirement;
none is silently substituted here. This backend exposes consumption explicitly.

Failure injection covers after first link, data sync, manifest sync, before global
commit, after commit and after final sync; additional tests cover retirement,
corruption, incompatible layout/provenance/version, incomplete ranks, writer
contention, symlinks, unrelated cleanup/adoption targets and forbidden native
qualification. These are process-level fault tests, **not physical power-cut or
multi-rank crash validation**.

## Exact native obstruction

QE's interrupted hybrid iteration has two states: the **old exchange operator**
and the **current inner-SCF orbitals/density**. Saving/restoring only the q stream
does not close that state. In the nonlocalized ACE path, `xi` preserves the old
compressed operator, and `x_occupation` preserves its source weights. Minimum
operator capture includes `xi` (or an independently proved faithful old-basis
reconstruction), old exchange occupations/band coverage and exact compatible
mesh/partition/normalization conventions. It also needs the matching HSE outer
scalars and current inner-SCF restart/native state, not merely current `wg/et`.

**PROVEN synthetic counterexample:** for `V=-diag(1,2)`, rank-one ACE built on
`phi_old=(1,0)` gives `A_old=-diag(1,0)`. Rebuilding on
`phi_current=(1,1)/sqrt(2)` gives
`A_current=-[[1,2],[2,4]]/3`. Both are exact on their respective trial vector;
they are different operators. Even exact reconstruction of V does not justify
replacing the old ACE basis with current orbitals. This is not a proof that old
orbitals are unknowable from the complete structured q stream; it rejects the
specific current-basis shortcut.

Source audit found **two** interruption paths in `electrons.f90`: stopped inner
SCF and the between-EXX-iterations `check_stop_now()/nexxiter` branch. The first
package guarded only the first. `run_pwscf` subsequently calls `punch('all')` when
EXX is active; `punch` writes XML/density/native waves and ACE files in separate
operations. A manifest committed inside `electrons` before those writes cannot
certify the resulting complete native checkpoint. An atomic stream manifest
alone also cannot certify those later, possibly partial state files.

The required bridge must stage old operator/state at both stop points, bind the
completed native save after `punch`, synchronize all rank outcomes, and publish
only then. Import must validate the full packet before QE reads/restores it and
before destructive `exxinit`, restore old occupations and ACE rather than derive
them from current orbitals, and honor exact layout/source/PP/operator fingerprints.
No such native capture/import bridge is implemented by these storage APIs.
Native-state qualification therefore fails. This is a concrete implementation
and validation boundary, **not** a claim that implementation is impossible.

Primary sources: [QE 7.5 electrons](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/electrons.f90),
[exchange/ACE](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/exx.f90),
[run_pwscf](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/run_pwscf.f90),
[punch](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/punch.f90),
[native wave/ACE output](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/pw_restart_new.f90).
Durability contract follows [Linux fsync documentation](https://raw.githubusercontent.com/mkerrisk/man-pages/master/man2/fsync.2).
