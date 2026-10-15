# Which signed inversion is physically being predicted?

All equivalences below are **PROVEN UNDER ASSUMPTIONS**, not established for
the physical random alloy. A model's eigenvalues are not automatically exact
electron addition/removal energies. Fix the lattice path a(x), ionic/strain
state, carrier density, static-lattice versus zero-point convention, and
thermodynamic/boundary limit before giving x_c a meaning.

## Periodic electronic reference

For a nonmagnetic periodic Bloch operator with SOC, a cubic Td double-group
Gamma6 doublet and Gamma8 quartet have energies e6 and e8 when each target
multiplet is isolated from other copies of the same irrep and is tracked
continuously. Define Delta_Gamma=e6-e8 and M_K=Delta_Gamma/2. These are a signed
band-order separation and Kane mass convention, not a negative excitation gap.
For an exact many-body propagator the corresponding statement additionally
requires identifiable quasiparticle poles and a justified band assignment.

Positive Delta_Gamma equals a fundamental gap only if filling, direct extrema
at Gamma and absence of other pockets/gap closings are established. In the
inverted cubic case the heavy-/light-hole Gamma8 sector can remain touching;
negative Gamma6-Gamma8 separation coexists with a zero excitation gap. A
four-band Dirac replacement that deletes heavy holes need not preserve the
self-energy or transition. Strain changes the symmetry and can split Gamma8;
do not average its levels into a quartet in a symmetry-broken configuration.

## Random alloy and physical projectors

An individual alloy realization generally has neither translation nor Td.
Define its static self-consistent operator H_omega in a common Hilbert space,
or specify its interacting retarded propagator separately. The configurational
law, positions and boundary conditions are physical inputs. After the infinite
volume limit, ensemble translation/Td covariance permits a Gamma momentum
fiber and inequivalent single-copy injection frames Phi6,Phi8. Then

    Phi_alpha* Gbar_Gamma(z,x) Phi_alpha = g_alpha(z,x) I_dalpha,
    dalpha = 2,4.

With several irrep copies, the exact commutant is a matrix in copy space.
Choosing/downfolding a particular copy is additional physical information.
An inherited PBE trial frame is a well-defined probe, not automatically a
converged HSE/quasiparticle-band projector. Unitary changes within a fixed
physical sector preserve traces; changing the subspace changes the observable.
A chosen frame may depend on x only with declared transport/derivative control.

| Candidate | Definition | When it agrees with a sharp signed band order |
|---|---|---|
| Periodic/mean-chemical Kane mass | (e6-e8)/2 for specified Bloch operator | Exact for that periodic operator; not generally the random-alloy pole mass |
| Sharp spectral-atom order | e6_atom-e8_atom, with nonzero thermodynamic delta weights and tracked branches | Defines a sharp order without requiring a common global gap; existence/residue/branch conditions must be established |
| Real inverse-root order | roots of Re[1/g_alpha(E+i0,x)]=0 | Agrees with sharp poles under a pole/background certificate; otherwise a resonance-center convention |
| Complex resonance order | Re z6-Re z8 on a specified analytic sheet | Needs analytic continuation and isolated tracked resonances; not necessarily real-axis poles or spectral maxima |
| Spectral peak/window functional | declared peak or smoothed projected weight/centroid | Requires separate damping/background and peak-selection arguments; no generic equivalence |
| Green-function zero | g_alpha=0 or det G_P=0 | Generally an antiresonance/self-energy singularity, not an energy pole or gap closure |
| Bulk topology/mobility transition | change of a well-defined global invariant or localization phase | Requires momentum/real-space, filling and gap/localization hypotheses beyond Gamma data |

For exact retarded denominators D6=F_s-m and D8=F_s+m, a shared pole obeys
F_s=m=0. If its energy is complex these are TWO complex equations. A single
real composition parameter does not generically make both widths coincide.
Coincident real parts of poles or real inverse roots are weaker statements.
Taking Hermitian parts of the retarded result is not principal-value reactance
scattering; retain the existing continuum-prescription distinction.

For D(E)=F(E)+i Gamma(E), Gamma>=0, the projected spectrum is
A=Gamma/[pi(F^2+Gamma^2)]. A stationary peak satisfies

    Gamma'(F^2-Gamma^2)-2 Gamma F F'=0.

At F=0 this requires Gamma'=0 or Gamma=0. Energy-dependent broadening can
therefore separate a peak from a real inverse root. Multiple peaks or branch
switches can remove a unique scalar signed separation. eta in E+i eta is a
mathematical resolution; it adds no proof of intrinsic linewidth or poles.

A two-state Hermitian bath gives g_P(z)=(z-a)/[z(z-a)-t^2]. At E=a it has a
Green zero although det(a-H)=-t^2 is nonzero. Thus an observed inverse singularity
cannot be relabeled a band inversion. A continuum need not admit any meromorphic
second-sheet continuation, so resonance poles cannot be assumed either.

## Topology is a separate target

Zincblende lacks inversion symmetry; an inversion-parity shortcut is not
available merely from atomic s/p labels. A gapped TR-symmetric periodic model
may admit a 3D Z2 invariant of its occupied bundle. A disordered system needs
an appropriate sample/ergodic real-space or mobility-gap formulation. Cubic
inverted HgTe's touching Gamma8 sector requires a separately declared gapped
regularization (for example a specified strain path) before an insulating
invariant is invoked. An interacting zero-frequency topological Hamiltonian
also requires its own nonsingularity/gap conditions and the full physical G.
An index of an arithmetic disorder-average is not automatically a sample index.

The existing Gamma-identical/different-global-topology counterexample in
`continuum_spectral_2026-10-11/observables_and_failures.md` N7 remains decisive.
Even perfect knowledge of both Gamma functions cannot exclude a transition
elsewhere in momentum space. No Gamma scalar alone proves a topological x_c.
