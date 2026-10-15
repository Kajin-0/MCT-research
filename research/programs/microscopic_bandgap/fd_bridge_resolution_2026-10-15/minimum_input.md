# Next physical input after resolving the auxiliary/state confusion

**Acquire one complete SAME-D native Hamiltonian action certificate, before
another hybrid SCF trajectory.** This is not another request for endpoint gaps,
more bands in an unchanged defective ACE, a scalar energy, or a symmetry average
renamed native FD. No new native job is admitted in this package.

The read-only result separates four tasks that cannot be collapsed:

1. Frozen trial density: specify jointly invariant natural orbitals AND weights,
   consistent with144e, spinor/nonlocal density and FDentropy conventions. The
   computed twirl is a trial. Its tiny rounded negative/above-one occupations
   are reported; clipping is used only to evaluate an indicative floating
   entropy, not to certify a strict positive FD density or finite logit.
2. Native local state: reconstruct charge from that exact trial by the native
   Gamma/FFT/NC normalization, verify reciprocalG0/integral144 and all spin
   components, then rebuild HSE Hartree/XC+ionic+SOC state. Importing natural
   source orbitals while keeping oldPBE/oldHSE local potentials is incompatible.
3. Complete action: export kinetic, local, nonlocal-SOC and DIRECT Fock actions,
   on the invariant support/physicalframe AND independent solved-state trials.
   A152compression can cover the physical frame; it must not replace the176
   solved bands or assign artificial occupations to six normalized high-G
   differences. Old operator qualifications apply to a different D. An ACE
   action cannot certify its own off-span error; require matched direct trials.
4. State residual: diagonalize/track the actual H[D] in the declared solved
   domain, solve FD charge from its eigenvalues, compare density/entropy and
   full eigenpair/off-space residual. A finite-Galerkin FD check alone needs
   the complement/tail certificate in theory.md before a full-space claim.
   Direct evaluation of D-f(H[D]) avoids logarithms of rounded saturated
   occupations. It still requires the complete Hamiltonian and tail input.

Acceptance remains numerical and physical-domain specific: charge1e-8e,
original reference preservation1e-10 when claiming the original frame,
operator/source/TR/crystal gates1e-8, actual Kramers/quartet checks on the
nonmagnetic host, consistent energy/entropy and a measured stationarity budget.
A new constrained-frame protocol must be labelled NEW rather than passing
old preservation failures. Sigma remains .001Ry. The bound multiplier250/Ry
does not imply that an SCF1e-9Ry energy residual is a4e-12density bound.

Information gain: this action/readback distinguishes a valid density-state
bridge from a symmetry-only repair and supplies an actual residual for the
gap-free FD bound. Export size on152vectors is52.66MB globally before metadata;
retaining176solved-state trials and independent controls costs more. The prior
~.875s/directtrial is a FORECAST ONLY. Source integration, density rebuild,
kernel/output guards, independent controls and a finite resource envelope are
not yet verified, so no runtime/12GiB admission or release is claimed.

Native source review: `PW/src/h_psi.f90` applies kinetic and calls local and
nonlocal/exchange paths; retained `hybrid_convergence/pilot_native.inc` calls
only `vloc_psi_nc_acc` for local0/1. The old C1 before-packets provide direct
Fock on176columns and eigenvalues from their prior solved state, not the new
trial's complete H[D]. Recombining these mismatched pieces cannot certify the
new FD bridge. This is the precise current hard scientific/software boundary.

Separate random-alloy boundary: the new measured N2-sharing PBE contrast does
not determine an HSE functional correction, N3operator, short-range order,
random-alloy causal self-energy or physical crossing definition. None can be
replaced by empirical bowing or an endpoint-only interpolation.
