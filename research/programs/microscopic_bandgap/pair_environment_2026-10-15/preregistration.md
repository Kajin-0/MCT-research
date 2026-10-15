# Cd-pair environment contrast, prospective protocol — 2026-10-15

Parent892079f. ONE fresh sequential stock-QE PBE+SOC16atom pair at x=.25:
unshared Cd cations(0,7) versus shared(0,1), cation ordering preserved. Both
Cd2Hg6Te8,288e/352spinor bands, a6.46Angstrom cell Q=ones-I, fixed positions,
SG15 FR NC,50/200Ry,Gamma, FD.001Ry, conv_thr1e-9Ry, mixing.3, full-accuracy
Davidson, atomic+random start. Only substitution positions and private paths
differ. max_seconds540 is an administrative stop before the600s hard deadline.
No old state reuse, no native retry, no lowering physics or solver tolerance.

Before launch: independently enumerate periodic nearest Te shells and affine
symmetries. Expected histograms unshared8N1; shared2N0+4N1+2N2. Expected linear
subgroups24 and4, with two internal translation cosets each. The nearest Cd
separations are a and a/sqrt2: configurations are inequivalent, not a global
rotation or origin relabeling. The sharing motif repeats a Cd-neighbour chain;
it is NOT an isolated impurity pair. Native XML rotations/translations must
map actual chemical positions and match exactly the independently predicted
linear subgroup. No Td or Gamma8quartet requirement on the shared geometry.

PRIMARY frame is explicitly NEW: matched accepted PBE16host native50Ry Gamma6
bands275,276 and Gamma8bands287..290, fixed BEFORE either acquisition. Same
physical cell, axes/origin and NC metric; overlap by physical G labels, not
array index. Old original40Ry projector is a separately labeled continuity
check, never silently substituted. Preserve old frame/protocol failures.

Native admission: conv achieved, residual<=1e-9Ry; independent FD charge288
within1e-8e and occupation reconstruction1e-9; full352Gram<=1e-8; physical
HDF5 B=2pi*A^-T and XML reciprocal cross-check1e-10; Gamma capture352bands,
native symmetry subgroup/chemical-map equivalence. Kramers test energy clusters
at1e-5eV: every cluster carrying>=.01 of either fixed-frame normalized spectral
weight must be even-dimensional and have minimum Theta overlap>1-1e-8. Record
ALL clusters, including any low-weight incomplete high-energy source cluster;
this is not full-HSE-source closure. For unshared additionally require native
dominant Gamma6/8 Td labels; no such false label on split shared branches.
No sign or magnitude requirement: negative or unresolved contrast is a result.

Observables after BOTH gates pass: Gamma6/8 normalized spectral weights;
Gaussian W1,1.5,2,2.5,3eV (W2 primary), at own EF; scalar inverse-resolvent and
full6x6 Schur effective response at eta.025,.05,.1eV (eta.05 primary). All
energy windows expressly relative to own EF, NOT aligned impurity kernels.
Report reference sensitivity at a COMMON absolute QE energy only if separate
source/gauge checks justify it; otherwise refuse operator interpretation.
Conditional positive omitted-probability, host-nearby-frame and IEEE bounds;
Gaussian mass>=.05 and inverse margins strictly positive. Bounds do NOT include
SCF eigenpair, functional, finite-cell, structural or material errors. No gap,
physicalxc, N3 determination or fit of local chemistry from a scalar proxy.
Investigate whether N2 matrix extraction is identifiable, rather than imposing
4times a spectral difference as an unproved local operator.

Same tested local owner/rank leases/pidfd and sampled output policy; EXACT600s
per member,12GiB memory, swap0, Tasks12, hostRAM>=4GiB, disk>=10GiB, aggregate
14GiB owned output, two64MiB escrows, one local2rank MPI family. Fresh sockets
<=107bytes, actual non-MPI bind/connect/allowlist check in BOTH roots before
service. Pin all owner/validator/input/PP/ELF/reference sources. Preserve
stock/dirtyDFT/old ledger/old failures, HSE16 and all other sessions. No claim
of continuous aggregate quotas, foreignMPI absence or private networking.

After the pair, commit/push valid evidence and CONTINUE with a distinct HSE
FD/state-bridge algebra/source diagnostic on the retained joint152space. No
HSE SCF can launch from a pure space-closure certificate or the old176ACE state.
