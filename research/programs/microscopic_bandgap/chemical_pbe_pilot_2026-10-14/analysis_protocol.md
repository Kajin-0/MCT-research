# Matched native complex-projection protocol (before Cd projection analysis)

2026-10-14. Only the two completed native PBE8 SCFs; no additional MPI job.
Complex NC overlaps in exactly identical cubic cell, origin, spin axes, PW
cutoff/Miller spaces. Keep phases through the calculation; report trace weights
which are invariant to sector/eigenstate unitary changes. Independently test
actual complex unitary rotations and reciprocal relabeling.

Primitive Gamma at conventional-cell Gamma has only all-even or all-odd cubic
Miller indices (fcc reciprocal lattice). Check translation probability of each
selected host state. Identify near-edge candidates using accepted HSE Gamma
spinors restricted explicitly to common40Ry PW space; calculate the missing
HSE norm and never use restricted vectors as exact full-space overlaps. Final
host Gamma6/8 designation comes from24 spatial Td operations with consistent
spin lifts, character multiplicities, span leakage and the existing conditional
nearby-invariant-projector theorem. The substituted states need not carry a
primitive Gamma label; they are projected onto the matched HOST physical sectors.

Main bounded observable: Gaussian test-function centroid with W=2eV relative
to each native Fermi reference. For normalized sector P_alpha/rank d,
w_n=Tr(P_alpha |n><n|)/d, t_n=E_n-E_F,
M=sum w_n exp[-t_n^2/(2W^2)], N=sum w_n t_n exp[-t_n^2/(2W^2)], c=N/M.
Omega=c6-c8 within each member is invariant under a common energy-zero shift;
DeltaOmega=Omega_Cd-Omega_host. Numerical FD E_F is a declared selection
reference, not an electrostatic band-offset alignment between species.
Require M>=.05 (existing chemical mass floor; no relaxation). Also report all
176 retained weights, raw near-edge dominant projected eigenenergies/Kramers
group splittings, and full retained-band centroids distinguished from Omega.

Conditional omitted-spectrum bound: if native states are the orthonormal
eigenstates of a common Hermitian operator with complete positive spectral
measure, r=1-sum_retained w>=0. Since0<=phi<=1 and|t phi|<=W/sqrt(e),
|c_complete-c_retained| <=r(W/sqrt(e)+|c_retained|)/M. This needs no bound on
uncomputed high energies. It is NOT a measured eigenpair/operator/material error.
For a same-rank nearby physical host projector at operator distance epsilon,
normalized trace-norm change <=2epsilon. Replace r by2epsilon in the ratio bound,
and denominator by M-2epsilon (must remain positive). Sum separate tail and
projector bounds conservatively for both branches/members. Dot-product/closure
errors and native convergence/eigenvalue conditioning are recorded separately;
no SCF total-energy threshold is asserted to bound all individual eigenvalues.

No rigorous material uncertainty from one cutoff/cell/grid/functional. Report
that limitation explicitly; no physical x_c, dilute T-matrix, sharp alloy Gamma
gap or topological boundary. No post hoc threshold selection to pass a failure.
