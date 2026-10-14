# One chemistry-bearing PBE+SOC pilot (frozen before native execution)

2026-10-14; parent research commit e6d48d9. NEW user-authorized exploratory
accuracy/cell domain. No change to original HSE16/352band/288electron target,
stock executable, old owner/occupation failures, or blocked historical goal.

One sequential pair: cubic conventional zincblende Hg4Te4, then CdHg3Te4
(replace the cation at the origin, x=0.25), fixed a=6.46 Angstrom. SG15 FR v12
PBE NC potentials, Cartesian spin axes/origin/cell identical. Gamma-only
supercell sampling folds primitive Gamma and three X sectors. No relaxation,
isolated-impurity limit, alloy averaging or thermodynamic extrapolation.

PBE+SOC, 40/160 Ry, 176 spinor bands/144 electrons, Fermi-Dirac smearing
0.001 Ry (a numerical occupation regulator, not a zero-temperature result),
SCF conv_thr=1e-9 Ry, full-accuracy Davidson, beta=.3, max100 iterations,
fresh atomic/random starting states. Host and impurity are independently
self-consistent; their total energies have different species and are not an
impurity formation energy. Lower cutoffs/k sampling are NOT certified material
accuracy; no fitted alloy gap, physical x_c, or detector cutoff.

Scientific gates: native JOB DONE, converged SCF in schema/stdout, finite native
eigenvalues/complex NC spinors, charge residual <=1e-8 electron with independently
reconstructed FD occupations. Same physical PW spaces, spin axes and cells.
Physical host Gamma6/Gamma8 assignment must pass primitive-translation and Td
complex-character tests (nearby multiplicities uniquely 1) and orthonormality
<=1e-8; otherwise report unassigned complex overlaps only. Select near-edge
host sectors by their symmetry and independently retained accepted HSE reference,
explicitly quantifying any reference-cutoff loss, never calling HSE/PBE identical.
Report complete computed-window trace weights and missing weight, phase-invariant
host-sector energy centroids/weights and dominant resolved energies, not a sharp
impurity Gamma8 irrep or a material gap. Keep all unmeasured cutoff, k, finite-cell,
functional, relaxation and many-body uncertainties OPEN.

Execution: existing local-owned acceptance, not host-wide exclusion or private
network proof. ONE MPI family, two local ranks (isolated plm, self/sm transport),
fixed stock ELF and PP/input/source hashes. Fresh Unix peer credentials AND
SO_PEERPIDFD bind both rank wrappers before exec of pinned stock QE; both actual
rank PIDs retain identity across exec. Kernel cgroup MemoryMax12GiB, swap0,
TasksMax12, wall600s; sampled family RSS12GiB (shared overcount), host available
4GiB and free disk10GiB floors. Local ext4/quota admission includes aggregate
14GiB output envelope plus real 64MiB escrow per member. Strict known-path,
recursive inode/blocks, deleted-open FD accounting and metadata allowance;
per-file1GiB cap is not aggregate. Bursts/external writers between samples remain
accepted sampled-domain risks. No hidden continuous disk theorem.

NEW stock-PBE terminal contract: live registered rank FD denial refuses. Proven
pidfd exit permits deferred accounting only; successful terminal acceptance needs
both registered rank kernel exits, launcher0, retained same manager invocation
success/exit0, empty/removed original cgroup, complete final tree and native state.
No fake native phase10 records (unmodified stock does not emit bridge receipts).
On any failure terminate ONLY this unique owned unit; preserve evidence and do
not retry. Cd member launches only after host scientific AND owner gates pass.
