# Comparable projected response and k3 symmetry qualification

**PROVEN UNDER ASSUMPTIONS:** for this nonmagnetic cubic cell, the 24 Td
operations preserve both atomic-species arrangements. Adding time reversal
groups {0,+1/3,-1/3}^3 into stars of sizes1,6,12,8. Without time reversal the
eight-point star splits4+4; Td alone is insufficient. Native24 rotation
matrices, translations, input flags and actual weights must independently
agree. Pinned QE7.5 PW/src/setup.f90 uses time_reversal = not noinv and not
magnetic_sym, magnetic_sym = noncolin and domag. No starting magnetization
is supplied. A mathematical orbit count is not a native acceptance substitute.

Unlike the older Gamma-only→k2 comparison, k2 and k3 here share native
nosym=false, cutoffs, spinor/PP/cell/smearing/solver conventions. Their meshes
are not nested; they share Gamma but otherwise sample different points. The
measured difference is quadrature/self-consistent grid sensitivity, not a
rigorous bound to continuous BZ integration. Native SCF convergence does not
prove the unique physical ground state, control functional error or provide
an operator-norm eigenpair bound.

The primary original40Ry physical host projectors remain fixed. Match actual
cell/origin/global spin axes/Bloch k and reciprocal (G+k)B, then inject old
NC coefficients into the same vectors in the50Ry basis with zero new-only
coefficients. J†J=I; missing labels or incompatible cells refuse. Full complex
spinors are contracted without discarding/renormalizing computed-state norm.
Verify all24 spatial/spin group intertwining; geometry/projector error carries
unchanged through the isometry. Native k2→k3 host frame principal angles and
secondary new-host-frame responses are separate measurements.

For each frame of rank d use w_b=Tr(P|psi_b><psi_b|)/d, not retained-probability
normalization. Let phi=exp[-t^2/(2W^2)], t=E-reference, M=sum(w phi),
N=sum(w t phi), c=N/M and Omega=c6-c8. DeltaOmega=OmegaCd-OmegaHost.
A common energy-origin change in E and reference leaves the observable
unchanged; moving reference alone changes the probe. Own-Fermi and own
dominant projected-Gamma8-quartet references are therefore reported separately.
They are not presumed equivalent for k3 or electrostatic species alignment.

Positive uncomputed spectral mass r permits tail mass in[0,r] and moment
|tail|<=rW/sqrt(e), even without bounded missing energies. Same-rank host
projector distance epsilon gives normalized trace-norm change<=2epsilon;
rho is the conditional IEEE arithmetic functional budget. With unchanged
M>=.05 and M-2epsilon-rho>0, the joint centroid bound is

    |c_completed-c| <= (r+2epsilon+rho)(W/sqrt(e)+|c|)/(M-2epsilon-rho).

Summing four branch/member bounds controls a response, and summing independent
k2/k3 response radii controls their difference. No covariance cancellation
is presumed. The original-frame epsilon is unchanged; arithmetic uses actual
component count. This conditional bound excludes native eigenpair/operator,
SCF branch, functional, lattice/finite-cell, ionic/zero-point, BZ-continuum and
material errors. It does not bound an ordinary unfiltered energy moment.

The native all-k charge is sum_k wk sum_b FD((mu-e_bk)/sigma), using actual
XML occupations=wg/wk, not Gamma occupations alone. XML energies are Hartree;
multiply2 for Ry and27.211386245988 for eV. Spinor NC Gram, Bloch-vector units,
band count, cell and Gamma HDF metadata are independently checked. Native
Gamma is saved at the new SCF charge; no incompatible-density NSCF or restart.
Projected centroids are continuum-compatible probes, not sharp original signed
Gamma gaps, absorption edges, topology or physical x_c. No novelty is claimed.
