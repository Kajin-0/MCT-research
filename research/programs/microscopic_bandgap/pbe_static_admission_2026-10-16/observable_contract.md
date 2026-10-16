# Static environment observable and its admission boundary

**PROVEN UNDER ASSUMPTIONS; no new operator actions acquired.** Two ordered
16atom periodic configurations have the same cell, origin,6Hg/2Cd/8Te, pinned
SG15 FR NC potentials,50/200Ry, Gamma,352spinor capacity,288e, FD.001Ry. The
only chemical change is Cd positions(0,7) to(0,1). Reuse the ACCEPTED original
PBE SCF save files, never the refused diagnostic's output as a control. New
roots contain independently hashed copies; no SCF or occupation update.

For PBE the saved scalar density and its gradients determine Hartree/XC;
ionic local and NC SOC terms are fixed by species/positions/PPs. Unlike HSE,
there is no Fock dependence on a separately unqualified nonlocal density matrix.
The accepted XML explicitly disables magnetization and its saved HDF5 contains
only scalar rhoG. That qualifies the declared nonmagnetic PBE local model,
NOT time reversal of a reconstructed nonlocal occupied density or FD stationarity.
This is why the frozen saved-density PBE question is eligible while the HSE
state bridge remains blocked. It does not certify that saved PBE wavefunctions
are exact eigenstates of the final saved-charge Hamiltonian.
The existing static packet does not capture native evc/occupation bytes.
Unchanged saved HDF5 hashes are NOT native wavefunction readback. Enforce no
wfcinit atomic/random fallback; for stronger wave/eigenpair claims add explicit
readback/queries. PBE H[rho_saved] itself needs the qualified charge/local and
ionic state, not invented full nonlocal-D fidelity.

Let F be the EXACT original accepted host50Ry six spinors, ordered2+4,
with physical integer G labels and native reciprocal B, Gamma k=0, same spin
axes and cell. The audit reconstructs F byte-for-byte from that accepted host
HDF5, with Gram defect2.67e-15. No e90/40Ry substitution, naive index overlap,
Theta purification, tail renormalization or changed irrep frame is permitted.

Write S=F†F, Pi=F S^-1 F†, Q=I-Pi; use exact Gram metrics instead of pretending
rounded F is an exact isometry. Each sector projector is
Pi_a=F_a(F_a†F_a)^-1F_a†, and W=Pi_6/2-Pi_8/4. Tr W=0, ||W||_1<=2.
The tiny cross-sector Gram defect is retained in arithmetic/embedding error;
it is not corrected by changing the original frame.

For each member m the primary outputs are

    Y_m=H_m[rho_saved,m] F,  A_m=F†Y_m,  B_m=QY_m,
    Omega_m=Tr(W H_m),  delta_Omega=Omega_sharing-Omega_unshared.

A is the full STATIC first spectral moment in this specified frame, without
a finite-band tail assumption. B is the full out-of-six-state action in the
DECLARED finite50Ry Hilbert space. Report singular values/norms of B_m and
B_s-B_u, and scalar/traceless/block components of A. It is not a quasiparticle
gap, eliminated-space self-energy, Te-only vertex or infinite-cutoff result.
Kinetic actions must cancel in the difference (identical G/cell); local and
nonlocal SOC species/charge contributions are reported separately.

Under H_m->H_m+c_m I, A_m->A_m+c_m S but Omega and B are unchanged.
Thus delta_Omega, delta_B and the METRIC-traceless matrix contrast need no
assumed common Fermi level. Full scalar/common contrast DOES need alignment.
Use no own-EF subtraction in the primary static actions.

## Gauge / numerical energy alignment

There is a defensible SOURCE-CONDITIONED canonical periodic QE convention:
`v_h` in pinned v_of_rho.f90 sets Hartree G=0 to0; `setlocal` sums the SAME
per-species vloc times structure factors; at G=0 the structure factors are
species counts. Equal cell/composition/PPs therefore give equal ionic G=0.
`set_vrs` adds this local potential to the same PBE functional derivative,
without an arbitrary specimen EF shift. This requires ordinary3DPBC, no ESM/
2D cutoff/MT correction/external field/gate/plugin or independently added
constant. Future preflight must validate these flags and capture v_of_0 /
local-potential convention in both members. XC mean changes are kept, not
removed to force alignment. See the pinned source lines in source_budget.json.

This is a NUMERICAL MODEL gauge, not a vacuum/interface or absolute material
band-offset alignment. If its independent checks fail or remain incomplete,
publish only gauge-invariant outputs; the scalar/common interpretation is
NO-GO. Existing own-EF values differ by about7.96meV and are not automatically
the common energy zero. A common-z resolvent comparison additionally fixes an
aligned reference E_star before either member; old own-EF data are not relabeled.

## Honest action count and symmetry

The original reference's Theta-outside-frame Frobenius norm is1.6548532e-6;
ALL SIX residual singular values exceed1e-8. Therefore6physical+6exactTheta
controls/member are mandatory: **24 full-H applications across the pair**,
not12. Do not replace the probes by a nearby Kramers-closed space. Require
H_m Theta F versus Theta(H_m F) relative<=1e-8, component sum/Hermiticity,
NC normalization, charge<=1e-8e, complete physical G/B/FFT/padding and source
readback. Explicit Theta controls avoid the unmeasured QQ-completion shortcut.

Actual chemical point groups are24 unshared and4 sharing, with corresponding
native fractional translations verified against SPECIES, not host Td imposed
on sharing. The saved Fourier densities match their actual native operations
exactly at displayed arithmetic in this read-only audit. Future native local
potentials must retain those symmetries. No shared quartet is required. To
claim a numerical full-H crystal covariance on an imperfectly closed probe
space, extra H(gF) actions OR an independent whole-operator/source error bound
are required; geometry/24 metadata alone is not such a measurement. Count
those controls separately; the current12query driver has no hidden ones.
For example all nonidentity native point operations, using raw6column images,
cost at most138extra actions in unshared and18 in sharing:180total including
the24primary/Theta actions, BEFORE optional eigen/resolvent controls. Reducing
this count needs a measured invariant-span/error certificate, not assumption.

## Eigenpair and static-versus-dynamic claims

Existing accepted SCF thresholds/FD charge/Kramers records remain accepted
under their original gates. A total-energy SCF error is not an eigenpair
residual. The primary24 actions give full physical-probe actions and B, NOT
full-H residuals for all352 saved eigenstates. For6 tracked native eigenstates
per member, add12 actions (36total), report ||H psi_j-e_j psi_j|| in Ry without
averaging a split quartet; that does not certify all352 or the omitted spectrum.
Exact saved rhoG/copy hashes qualify H[rho_saved] even if spectral stationarity
remains conditional. Do not call such output a newly certified stationary gap.

Schur reduction for a true self-adjoint aligned H gives
K_m(z)=A_m+B_m†(z-C_m)^-1B_m in an orthonormal representation,
C_m=QH_mQ. Therefore new A distinguishes a true static projection from an
energy-dependent eliminated response. But A/B do not determine C, and old
partial spectral K also has eigenpair/tail errors and distinct own-EF arguments.
Do not label old K-A as a measured pure self-energy merely by subtraction.

Cheapest additional rigorous single-z comparison:6retained-resolvent trial
vectors Ytilde_m(z) per member, with6new H actions/member (36total if added to
the24 static/Theta actions;48total if the12 eigenstate controls are ALSO kept).
The FULL residual S_m=(z-H_m)Ytilde_m-F yields

    ||F†(z-H_m)^-1F-F†Ytilde_m|| <= ||F|| ||S_m|| / Im(z).

This needs no common spectral gap. Inverse conditioning still needs its own
nonzero singular margin. Source m/query/header/becp and resource admission must
be extended for extra columns. The current12query binary cannot silently
implement those options. The proposed primary acquisition is ONLY24; stronger
static/dynamic attribution remains conditional without these extra inputs.

## Prospective numerical decision and identifiability

Target<=2meV numerical error on delta_Omega, chosen independently of the
unknown static contrast. A sufficient allocation is<=.5meV projected-H error
per member (e.g..25meV action/arithmetic plus.25meV saved-potential/transport),
since |delta_error|<=2(epsilon_s+epsilon_u). Original-frame transport must be
byte exact; physical frame/functional/cell/alloy uncertainty is separate. Small
shared-path component disagreement is evidence, not by itself a rigorous bound
on systematic source/arithmetic error. If that bound cannot be supplied, report
only numerical consistency, not a certified2meV sign. Sign requires an interval
excluding0; no sign is predicted here. Likewise a nonzero B_m or delta_B lower
bound requires an independently budgeted full action error.

Falsifiable conclusions: a nonzero delta_Omega rejects arrangement-independent
STATIC projection at fixed x/cell; nonzero B rejects closure of that operator
in the six-state frame; nonzero delta_B demonstrates arrangement-sensitive
remote coupling. Agreement of two static traces alone proves neither closure
nor a random-alloy law. Any static/finite-eta discrepancy only becomes a pure
Schur-response contrast with the additional state/resolvent certificates above.

Even exact A and B do not identify a unique localN2 tensor: periodic pair
distance/global screening/other cluster contributions can produce the same
columns. QZQ changes leave every measured H F unchanged but change eliminated
resolvents when B!=0. N3 environments remain absent, and two ordered cells do
not determine an ensemble mean/covariance or random-alloy x_c. Do not add these
screened configuration operators to an independent disorder self-energy without
jointly defining the mean and fluctuation subtraction. No bowing or x_c fit.
