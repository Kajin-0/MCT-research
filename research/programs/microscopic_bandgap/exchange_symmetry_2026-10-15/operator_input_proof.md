# Closed operator domain for the two-source test

This is fixed-orbital norm-conserving DIRECT Fock, not H_psi/full SCF. Native
PW initialization supplies the lattice/reciprocal/FFT and species context only.
Canonical occupied source density is imported before the first exxinit, replacing
all initialization orbital coefficients, et and wg, including padding. No native
Fermi solve, density mixing, local-potential reconstruction or ACE build occurs.
The old full-state byte refusal remains valid in its different Hamiltonian domain.

The unchanged vexx/vexx_k source obtains source real-space orbitals from exxbuff,
occupations x_occupation, q/k maps, FFT/G/kinetic momentum data, HSE kernel scalars
and MPI decomposition. exxinit transforms imported evc and regenerates that store
with the same nks1/negrp1/npool1/two-rank layout. Native source source-copy proof:
transform_evc_to_exx(type2), negrp1, evc_exx=evc; x_occupation=wg/wk. The second
source overwrites the existing same-sized exxbuff rather than allocating another
full q generation. Coefficients on physical -G are exchanged across ranks BEFORE
preparation of Theta sources/trials; no inherited rank-local conjugation shortcut.

For the immutable Γ/q1 host deck, the unique full-BZ momentum is0. In exx_grid_init,
identity symmetry is visited first; duplicates are excluded. Required native
nkqs=1, index_xk=index_sym=index_xkq=1 and xkq_collect=0 are checked explicitly.
The HSE kernel/divergence depends on this frozen geometry/grid/cutoff and fixed
functional parameters, not the SCF local density. Native actualFFT60³, α.25,
screen.106, Fock200 and physical per-rank G ordering must match retained source.
Same compiled direct routine/backends and six-column call size are mandatory.

Readback writes actual canonical Φ/et/wg/trials/G/B/k and kernel/FFT extents after
each direct call. Python compares all input bytes, then first V[D]P action bytes
against the accepted original control. Any missing/nonreproduced operator state
therefore refuses; no approximate full-state proof or tolerance relaxation is used.
The new covariance test uses the complete physical G basis to transform OUTPUT
spinors too; it never substitutes J acting only in an approximately closed6frame.

No unqualified USPP/PAW, extra q, shifted k, GPU, localization, additional pool/
group or different band/spin rank layout is allowed. NC makes unallocated dummy
becpsi irrelevant to vexx, as in the retained source-matched direct6probe call.
Source arithmetic routines are byte-compared before compilation. The private
driver returns before electrons/non_scf/punch. Any initialization XML/density is
not a solved state and cannot be interpreted as SCF/restart evidence.

Native resource caps do not prove completion. All allocated source/trial arrays
are bounded by176spinors/12trials/actualnpwx; only one1.216GB aggregate q store is
regenerated. The extra canonical input files are~0.13GB, not a copied22GB store.
Use existing hard12GiB/swap0/tasks12/600s and sampled output/host-floor controls;
fail before MPI if compilation/provenance/input/owner/storage gates cannot close.
