# Comparable probes, exact mesh reduction and qualified uncertainty

**CALCULATED:** actual retained complex-overlap curves and one native matched
Gamma-containing refinement. **PROVEN UNDER ASSUMPTIONS:** bounds on specified
positive spectral functionals and reference derivatives. No novelty claim.

For each physical host sector, use normalized trace weights w_n and
phi_W(t)=exp[-t²/(2W²)], t=E_n-reference. Gaussian mass M=sum w phi, moment
N=sum w t phi, c=N/M and within-member Omega=c6-c8. A common energy-zero shift
of E_n AND reference leaves Omega unchanged. Changing only the reference
moves the spectral window and is a different probe. Energy origins from
independently self-consistent species are not assumed electrostatically aligned.

Positive omitted probability r gives tail mass in[0,r], moment bounded by
rW/sqrt(e) regardless of unbounded missing energies. Same-rank nearby host
projector distance epsilon gives normalized trace-norm change<=2epsilon.
With conditional arithmetic functional budget rho, joint denominator

    m=M-2epsilon-rho>0,
    |c_completed-c_retained| <= (r+2epsilon+rho)(W/sqrt(e)+|c_retained|)/m.

Every branch/member budget uses the SAME joint denominator. The earlier
prepublication denominator correction remains in its historical package; this
analysis starts from its corrected version. No mass threshold is changed;
all probes meet.05. Closure weights come from actual complex spinors, not a
normalization of incomplete retained probability to1. Individual native
eigenpair/operator residual norms, cutoff, k-grid-to-continuum, functional,
finite-cell, ionic/zero-point errors remain outside these conditional bounds.

An independent reference sensitivity identity follows directly from exponential
tilting. For absolute weighted mean m_alpha(reference), differentiating the
positive quotient gives

    d m_alpha / d reference = Var_alpha(E)/W²,
    d Omega / d reference = (Var6(E)-Var8(E))/W².

Relative centroid derivative additionally has -1; it cancels in Omega. AtW2
in the original Cd packet, retained Gaussian variances .07075226/.00897301eV²
give derivative .01544481329. Direct central differences agree within1e-11.
This explains why reference dependence is strongest in the chemically mixed
Gamma6 spectrum. It is a finite retained-spectrum identity, not a scattering
susceptibility or a material bowing parameter. Unknown spectral tails can also
change the derivative; no derivative material error bound is asserted.

## Mesh and native accounting

Conventional cubic reciprocal mesh{0,1/2}³ has eight points. The24 Td signed
permutations preserving tetrahedral bonds group them into four stars of
sizes1,3,3,1 by number of half components. Both atomic species arrangements
are explicitly invariant under these operations. Native nosym=false performs
correct density symmetrization/rotation; four unsymmetrized representative
densities would be inadequate. Both native outputs independently give four
representatives, positive weights(1,3,3,1)/8, uniqueGamma and sumweights1.

This is a legitimate quadrature on the declared nonmagnetic Td branch. The
old run used nosym=true; the difference therefore includes the computational
symmetrization route as well as mesh refinement. It is called **numeric method/
grid sensitivity**, not an isolated proven k-discretization error bound. No
independent same-grid symmetry toggle or spontaneously broken-symmetry test
was run. Two grids cannot certify BZ convergence.

Native all-k normalization: QE7.5 qexsd_init.f90 exports occupations=wg/wk;
qexsd_copy.f90 reimports wg=XMLoccupation*wk. The independent FD charge check
uses sum_k wk sum_b f_bk, not176Gamma occupations alone. Input widths are Ry;
XML energies Hartree are multiplied by2 for Ry or27.211386245988 for eV.
Native Gamma HDF xk is checked through its own reciprocal matrix; its0 vector
and exact7809 PW Miller space match the original full40Ry frame. This avoids
mixing Gamma normalization with whole-BZ integration or cell-volume factors.

Both new self-consistent Gamma HDF files exist; no separate NSCF and no inherited
aborted/restart state. Strict owner records loaded same invocation/exit0, actual
kernel rank exits and empty owned group; old host terminal uncertainty is not
retrospectively repaired. Kernel caps and sampled output risks remain explicit.

Primary P6/P8 never change across grids; a new-host-frame check is separately
labelled and changes new DeltaOmega by only .06218meV. Old-to-new principal
projector distances .005656/.004392 are geometric frame changes, not operator
or material errors; their character multiplicities remain uniquely6/8. Native
Fermi-minus-dominant-Gamma8 offsets are <3e-12eV at stored numerical precision,
so both predefined reference recipes coincide here. This is numerical alignment,
not a claim of physical pico-eV accuracy or species band-offset alignment.

Primary source methods: [QE automatic meshes and nosym](https://www.quantum-espresso.org/Doc/INPUT_PW.html),
version7.5 local PW/src/pw_restart_new.f90 and Modules/qexsd_init.f90 /
qexsd_copy.f90. Official documentation checked2026-10-14. Spectral positivity,
functional-calculus bounds, symmetry reduction and exponential tilting are
established; possible material significance requires controlled physical inputs.
