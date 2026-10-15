# One-relaxation observable and causal interpretation

For each member, rho0/Phi0 is the preliminary semilocal state. The first ACE
approximates its HSE Fock operator and is exact on that 176-vector source span.
The next native inner SCF relaxes Phi and density at fixed first ACE, producing
rho1/Phi1. The second rebuild constructs direct Fock and ACE from Phi1, with
actual occupations and identical physical inputs. No subsequent inner solve is
performed. Final eigenvalues solve the first frozen ACE with the relaxed local
potential, not the rebuilt second operator. Inner convergence is not outer HSE
self-consistency, and neither is a material validation.

Let Ua contain the same original physical host reference spinors, with ranks
2 and4 for Gamma6/Gamma8. Source support maps exactly from7809 to10827 physical
G vectors. Define L0 as local action before first activation, L1 after first
activation, L2 after the one hybrid relaxation, and F1/F2 the direct reference
Fock actions at the two source states. All are captured on the identical Ua.
Kinetic and NC nonlocal PP operators do not change within a member.

    A1_m = trace_Gamma6minus8(F1 + L1-L0),
    R_m  = trace_Gamma6minus8(F2-F1 + L2-L1),
    A2_m = A1_m + R_m.

Chemical differences subtract host from Cd for each of these quantities. A2 is
HSE operator at rho1 relative to the preliminary PBE operator at rho0; it is not
HSE-minus-PBE at rho1. In particular the local R includes Hartree and electronic
polarization changes as well as local XC. Scalar energy-zero shifts cancel in
normalized Gamma6-minus8 traces. Unitary rotations within each fixed subspace
also leave the traces invariant. This does not eliminate physical projector
choice, coupling to other same-irrep states, or finite-cell effects.

Every reference Fock action is direct. ACE-on-source residuals validate each
new compression on its own 176 states. Native fock1 between rebuilds is instead
old ACE acting on the new orbitals: it is reconstructed from distributed old xi
and new Phi as minus weighted squared overlaps. This checks the actual old-state
lifetime/energy dependency without falsely equating ACE and old direct Fock
off-span. Recomputed signed dexx is retained even when native QE applies abs.
No extra costly old-direct-on-new-state experiment is performed.

Within each rebuild density/G/probe bytes must remain unchanged. Between the
two cycles density and source orbitals are expected to change; independent
phase captures, charge, Gram, actual rank/G/FFT and final HDF5 readback qualify
the comparison. First-source Phi is preserved in packets; it is not falsely
claimed externally verified by the final second-source HDF5.

Remaining uncertainties include further hybrid orbital/density relaxation,
Gamma/q1 versus sampled BZ, ordered8atom x=.25 versus dilute/random alloy,
SG15 PBE-generated PPs with HSE, cutoff/basis and projector selection, numerical
FD smearing and static-lattice/zero-point conventions. Small contraction or
SCF residuals do not bound these physical errors. Do not add these operator
traces to the earlier PBE k3 Gaussian response or claim physical x_c. No
restart correctness, full convergence or whole-SCF RAM saving follows.
