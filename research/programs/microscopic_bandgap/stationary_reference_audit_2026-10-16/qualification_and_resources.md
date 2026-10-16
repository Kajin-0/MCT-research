# YES/NO qualifications and source-grounded feasibility

**YES** is restricted to the stated claim. **NO** means the required claim is
not qualified, not that the original run failed its own contract. No old result
is edited. Source data and exact paths/hashes are in `native_audit.json`;
`metadata_audit.json` distinguishes original SCF and expanded exports.

| Required object/claim | e90 f360 | e90 f120 | Reason / remaining input |
|---|---|---|---|
| Original native SCF and exchange convergence | YES | YES | `result.json`, native stdout and original SCF XML agree; original SCF schema hashes equal the pre-existing `grid_expansion.json` parent pins |
| Electron count and saved charge | YES, numerical | YES, numerical | Occupation quadrature36e; independent rhoG(G=0)×volume=36.00000000000001e |
| Full original eight-k wavefunctions, occupations and ACE saved | YES, accessible | YES, accessible | Newly pin8 wfc+8 ACE and density/schema files per original; 64-point exports also retained. Most original full-BZ file pins are NEW today, not historical immutable operator fingerprints |
| Native physical Γ6/Γ8 frame and NC normalization | YES, conditional numerical frame | YES, conditional numerical frame | All24Td sector span defects ~1e-14, Gram~4e-15; original/export Γ coefficient norm differences~2.3e-15 are small but NOT byte identity |
| Exact same-D operator/restart replay from `open_grid` | NO | NO | Export rotates/transforms wavefunctions. Charge datasets equal but HDF5 container hashes differ. Native complete source/kernel/local-potential state fingerprint and replay are not certified |
| Nonlocal occupied density Td defect<=1e-8 | NO | NO | Calculated Γ lower witnesses8.54e-7 /1.04e-6, despite near-degenerate Γ8 energies; no averaging repair |
| Nonlocal whole-density Θ defect<=1e-8 | NO certificate | NO certificate | Compressed Γ witnesses~3.8e-9 are not whole-space bounds; conservative full-BZ upper is loose. Zero local spin is insufficient |
| Saved ACE symmetry on six Γ probes<=1e-8 | NO | NO | Td2.42e-8 /9.15e-8; Θ2.37e-8 /1.05e-8. Calculated probe defects, not a whole direct-Fock norm |
| Strict FD occupation/state interpretation | NO | NO | Original smearing=`mv`, not `fd`; changing μ/f requires a new nonlinear H[D] test |
| Same-D full-H eigenpair / occupied stationarity bound | NO | NO | No retained full kinetic+local+SOC+DIRECT-Fock residual packet on these native stationary candidates |
| Zero-smearing, stable variational physical host | NO | NO | Scalar convergence is not Hessian/FD/σ->0 or material accuracy; no new physical ordering claim |
| Direct transfer to H304 e50 Γ/q1 state | NO | NO | Different PW/EXX cutoffs, BZ quadrature, filling law and cell; measured e90 high-G tails are nonzero |
| Self-consistent Cd substitution / random-alloy mass | NO | NO | D_c and aligned screened response missing; ordered PBE and fixed-D HSE do not supply them |

The YES frame entries are useful: do **not** demand more D0 columns before
using these actual numerical host states as the reference source. The NO
entries prevent promoting them to an exact1e-8 FD/direct-operator certificate.
The small native primitive symmetry defects are not equivalent to the earlier
176-source host's order-unity TR defect or .655-eV quartet split.

Matching lattice vectors, origin/species positions and Hg/Te PP hashes are
independently checked in the original SCF metadata. Effective output cutoffs
are90/360/360 and90/360/120Ry. The f120 SCF XML's *input* ecutfock field is0,
whereas the executed hashed deck specifies120Ry, its effective output gives60Ha
and its native FFT is32³. Do not infer the actual cutoff from that input field
alone or silently treat the f120 and default-f360 operators as identical.
The serialization origin of that0 field was not separately proved here.

The reported charge check verifies occupations and the rhoG zero mode, not
complete off-diagonal orbital-density/native-local-potential consistency.
Γ Kramers pair energy/occupation differences are separately retained in the
metadata; no pairwise degeneracy is imposed at generic non-TRIM k points.

## Actual costs and mandatory source allocation

Pinned QE7.5 `exxinit` allocates, for the nonlocalized spinor branch,

    exxbuff(dfftt%nnr*npol, max_buff_bands_per_egrp, nkqs).

`init_index_over_band(...,nbnd,nbnd)` and the exchange layout allocate the
source buffer for the specified bands; fractional occupied count is not
permission to replace nbnd. ACE additionally allocates
`xi(npwx*npol,nbndproj,nks)`. FFT padding, duplicated global FFT work arrays,
redistribution, bands/eigensolver/PP tables, MPI/BLAS/HDF5 and output cache
must be included in a complete runtime envelope. Occupied-source memory is
not inferred from six Γ columns or a previous operator-query peak.

| Object, original settings | Source-conditioned nominal exxbuff | Actual historical family RSS / wall | Present12-GiB decision |
|---|---:|---:|---|
| Primitive e90/f120, k4/q4,44 bands;32³ EXX FFT,64 q points | 2,952,790,016B =2.75GiB | 4,056,358,912B (~3.78GiB),2581.52s, SIX ranks | Original accepted run existed; a NEW two-rank residual job is plausible, **not yet admitted** from this subtotal/history |
| Primitive e90/f360, k4/q4,44 bands;54³ EXX FFT | 14,189,395,968B (~13.21GiB) | 15,545,294,848B (~14.48GiB),1227.23s for terminal restart, not full chain | NO for this stock layout under12GiB; buffer subtotal alone exceeds cap |
| Original16atom e90/f120 n2/k2/q2,352 bands;64³ EXX FFT,8 q points | 23,622,320,128B =22GiB | Prior unfinished host26.722GiB; dry forecast21.27/21.32GiB | NO stock matched chemistry admission under12GiB |

These are nominal aggregate array capacities, not rigorous general resident
memory lower/upper bounds: padding/replication/physical page use depend on
layout. The scientific algorithm fills the buffered source data. With swap0,
one cannot admit a full stock stage requiring the nominal22GiB buffer using a
12GiB hard cap; no total envelope satisfying that cap is established. Neither
less MPI nor a band-group flag proves removal of the aggregate workload.
The measured interrupted peak reinforces this rejection but is not a bound
on the complete run. Source-based refusal does not promise RAM needed for
completion on another host or authorize purchasing hardware.

**Additional source/native trap:** `open_grid.f90` temporarily sets
`ecutfock=4*ecutwfc`, disables ACE and calls `exxinit` before restoring the
settings for export. BOTH original expansion stdout hashes verify, and BOTH
logs show54³ EXX FFT, including f120. Regenerating the primitive f120 export
therefore carries the f360~13.21GiB nominal buffer, not its SCF's2.75GiB.
The existing expanded files can be reused read-only; do not schedule another
`open_grid` as a cheap/12GiB-safe preparation. No new postprocessor was run.

The already tested small fixed-operator streamer is **not** a validated352-band
whole-SCF/restart alternative. No memory-saving claim from H304's5.56GB is
imported. No new SCF, binary, deck, dry-run, MPI, queue or supervisor is created.

## One concrete prospective host gate, not a cheaper chemistry launch

The nearest genuinely useful *future* numerical acquisition would qualify
the existing **primitive f120 source** with same-state full-H residuals, rather
than compute another D0 block:

1. Pin original eight-k state, source occupations, PP/core, local potential,
   exact q mapping/kernel, origin, FFT and energy convention before/after.
   Keep original cold smearing for a same-model check. A separate FD/zero-σ
   protocol is needed if that is the intended stationary model.
2. Apply kinetic+local+nonlocal SOC+DIRECT Fock to physical Γ6/Γ8 and all
   occupation-bearing source columns needed for the proposed stationarity
   bound (or a proved smaller residual contraction with a complement budget).
   Compare matching ACE action, symmetry, charge and native source fingerprint.
   Six Γ actions alone can qualify their eigenpair residuals, not full-D FD.
3. Before any native execution prove the actual TWO-rank descriptor-based
   allocation/output envelope, scratch admission and bounded time. The2.75GiB
   array plus old3.78GiB RSS are insufficient total upper bounds. Retain12GiB,
   swap0, tasks12, <=600s unless separately authorized, host4GiB/disk10GiB floors,
   <=14GiB sampled aggregate, fresh short sockets and qualified owned leases.
   This assignment authorizes none of those runs.
4. Accept only an observable-derived residual/error contract; report failures
   at old1e-8 gates unchanged. A new FD state or relaxed numerical observable
   domain requires a separately frozen prospective model, not retroactive PASS.

Even a passing primitive residual packet **does not acquire Cd chemistry**.
For the original16atom contrast, the necessary nonlinear substituted SCF and
matched pure-cell/folding qualification remain independently missing, and
stock resource admission is NO-GO. No smaller unknown HSE job is invented as
a substitute. Retained PBE chemistry stays in its distinct approximate model.
