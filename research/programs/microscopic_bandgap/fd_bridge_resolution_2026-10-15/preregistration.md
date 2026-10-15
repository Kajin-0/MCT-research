# Retained-state FD bridge resolution — 2026-10-15

Read-only follow-through after the ordered-chemistry acquisition; no HSE job
released. Original joint152basis, oldC1orbitals/weights and direct actions remain
unchanged. An exploratory read-only check found six near-orthogonal directions
outside the176saved eigenstates, with kinetic expectations near40Ry. This is
not a prospectively predicted numerical result. Freeze the following independent
audits before drawing its physical or algorithmic conclusion:

1. Reassemble physicalG and both ranks, verify exact stored jointG, native B
   units and cutoff via retained reference. Compute residual SVD directly,
   not sqrt(1-principal-cosine^2). Record all singular values/ranks at1e-3,
   1e-6,1e-8,1e-10. Do not truncate small residuals and claim exact containment.
2. Form the SIX leading residual Ritz vectors and separately orthonormalize
   their projected complement. Independently evaluate kinetic expectation by
   direct physical-G sums and matrix contraction; record high-G (>40Ry) weight,
   occupied-source weight and projector reference weights. Kinetic energy is
   NOT a total Hamiltonian or eigenvalue lower bound: local/nonlocal terms
   may cancel it. No six-band occupation reassignment.
3. Transport the oldFD density into joint152, then explicitly average its
   reduced matrix over all24Td operations, Theta and primitive translations.
   Report trace, entropy, positivity, covariance and changes relative to OLD
   density, including omitted norm/charge. This is a NEW constrained ensemble,
   not an accepted nativeFD solution. No saturated occupation logarithm.
4. Prove which full-Hamiltonian actions remain undetermined from the retained
   eigenstates/direct-Fock/six-vector local packets. Construct an invariant
   Hermitian counterexample on the unconstrained auxiliary space, preserving
   specified old-data constraints to their measured rather than invented
   exact containment. Independently test the finite-matrix variational gradient
   of the explicitly constrained energy+FDentropy, and the distinction between
   solved states, natural source states and compression auxiliary states.

The objective is a decision-changing smaller and correctly typed next physical
input, or a precise no-go. Space closure, kinetic estimates, twirled charge and
offline stationarity identities cannot qualify native HSE self-consistency.
