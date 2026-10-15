# Source and state dependencies; finite trial, not SCF

The trial is defined by separated spectral projectors of the measured twirled
matrix, not by arbitrary occupations of the152basis. Its142upper and4middle
eigenvalues are separated from .25/.75 by>.24999999. Spectral projectors of
an invariant Hermitian matrix are invariant, including the antiunitary action.
P142+.5P4 has trace144, entropy4log2 and fermionic positivity. Independently
measured global-G density symmetry and Gram errors qualify the floating trial.
The original source changes, explicitly. No finite logit of its saturated
weights, FDselfconsistency, preserved oldsource or new solvedband claim is made.

Dependency order in the new private driver (before electrons/SCF/punch):

1. init_run initializes cell, NC/SOC projectors, FFTs, core/ionic terms. Import
   the frozen natural trial source and original independent physical probes.
2. Native weights.f90 fixed_occ branch copies f_inp*wk; for nspin4 it has NO
   factor1/2. Gammawk=1 and176capacity weights are142ones,fourhalves,30zeros.
   Only this diagnostic call uses tfixed_occ. Native sum_band reconstructs
   charge using wg/omega, native wave_g2r, rho_r2g/sym_rho/rho_g2r. Restore the
   original fixed_occ state. No invented et/ef/eband enters a result; these
   have no eigenstate meaning for source natural orbitals and are not exported.
3. Native exxinit(.false.) consumes EXACTLY that evc/wg and activates HSE through
   start_exx. Require direct mode/use_ace=false. Recompute native v_of_rho
   AFTER activation, then set_vrs and newd. Thus screened localXC, Hartree,
   core/ionic and NC spin-orbit terms and directFock all use the SAME D.
4. g2_kin sets the current native kinetic operator. Compute native
   vloc_psi_nc_acc, calbec/add_vuspsi (including deeq_nc SOC) and vexx on164
   trials. Independently call stock h_psi in DIRECT mode on original6probes.
   This tests completeness of T+local+nonlocal+F, not just exchange matching.
5. Export full action vectors, source/wg/trial bytes, densityG/r, physicalG/B,
   all FFTslab descriptors, HSE/kernel bounds and native Hartree/XCcontractions.
   Allrank barrier and post-returnJOBDONE/terminal/owner/readback required.

The native EXX and ACE arithmetic subroutine bodies and exxinit are byte-identical
to the accepted private source; neither oldACE nor electrons is called. New
code is a fixed-state observable driver, not an alternative SCF equation.
Independent physical-G FFT charge reconstruction must match native rho_r to
1e-10absolute, charge to1e-8e. A local symmetry operation cannot hide a failed
source because nonlocal Dsymmetry is qualified BEFORE native invocation.

## Bounds from measured native quantities

In the finite PW/grid model, ||T|| is its captured largestg2kin. The local
spinor multiplication norm is bounded by max_r(|v0|+sqrt(vx²+vy²+vz²)).
For NC/SOC, V_NL=diag(B,B) C diag(B*,B*); ||V_NL||<=||B||_F²||C||_F.
The native sum of squared vkb over ranks gives the first factor; valid
deeq_nc blocks (all4spin components, actual per-speciesnh) give the second.
Padding coefficients are excluded. The bound is conservative, not fitted.

With nonnegative captured Fourier convolution factors, native direct exchange
obeys ||F||<=alpha max(c_G) max_r sum_j w_j||phi_j(r)||²/omega, as previously
proved. The sum of these four bounds is M>=||H||. Unknown signs/negative kernel
factors refuse this norm certificate. FFT/PW restriction is contractive.

Let S=range(Q), R=(I-QQ*)HQ, D=QdQ*. For Hermitian H,

    ||[H,D]||_F²=||[Q*HQ,d]||_F²+2||Rd||_F².

For ANY exact FDdensity F=f_sigma(H-mu), [H,F]=0, hence

    ||D-F||_F >= ||[H,D]||_F/(2M),
    ||D-F||_op >= ||[H,D]||_F/(2M sqrt(nPWspin)).

These are WHOLE-SPACE lower bounds at every chemical potential, needing no
gap or complement spectral assumption. The independent matrix prototype checks
the exact commutator identity and bound. A nonzero lower bound can falsify a
stationarity claim even when no useful whole-space upper bound is available.

Compute a projected FDmatrix from the actual152Hermitian Ritz matrix, charge144
and sigma.001. Its eigenvalues are Galerkin diagnostics, NOT native solved bands.
Full Ritz/offspace residuals are exported. The earlier gap-free upper bound
uses this coupling and a complement occupied-tail certificate; without the
latter, record only the universal finite-dimensional bound and explicitly mark
it uninformative. Do not claim nativeFD/outer convergence from a small projected
trace, source symmetry or this single action acquisition.

## Admission and cost

Prior measured752direct trials cost~658s with kernelpeak4.78GB. New164+6direct
trials forecast~149s;3times that plus60s startup/I/O is506.25s, below600s hard
limit. New persistent vector columns1002 versus prior1104; same176source store,
FFTdomain, NC/SOC and oneMPIgroup. Priorpeak+2GiB forecasts<7GB. These are
conservative FORECASTS, not adversarial runtime/RSS theorems. Hard cgroup12GiB,
swap0/tasks12/600s and sampled host/disk/output guards remain the authority.

Exact packet byte arithmetic bounds each rank file below1GiB using actual
npwx plus worst allowed216000density/FFT extents. Fixed prepared private files
are block-accounted and subtracted from the14GiB native budget, with8MiBmetadata
headroom. Frozen source/build/backend/input/PP/trial/expectedrho pins are
checked by the live issuer; no arbitrary command or boolean lease bypass.
Socket bind, fresh-root, knownfamily/lock and storage/quota/reservation guards
must pass before service. No hostwide exclusion or network namespace claim.

The first compile failure (missing module imports) and second link failure
(newd must be imported fromdfunct) are preserved. b3 fixes only these interfaces
and links; no native job was attempted during either build. No retry of a
failed native admission or unit is authorized by a compiler correction.
