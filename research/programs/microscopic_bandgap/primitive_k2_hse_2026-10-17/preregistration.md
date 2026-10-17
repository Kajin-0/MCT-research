# One primitive k2/q2 stock-HSE control — frozen before launch

2026-10-17 UTC; baseline53ca7b3. ONE fresh atomic-start HgTe computation;
no retry, Cd, restart, direct-exchange alternative or source modification.
Stock QE7.5 ACE, HSE(.25,.106 Bohr^-1), SG15 FR NC, SOC/noncollinear,
primitive fcc vectors a/2(011),(101),(110), Hg0/Te(.25,.25,.25) fractional,
a6.46Å,36e/44spinor bands,50/200/Fock200Ry,FD sigma.001Ry.
`host_pw.in` and `preregistration.json` freeze the exact deck and binaries.

**Question:** does a primitive, k-sampled FD calculation retain a practically
nonmagnetic cubic state, unlike the rejected8atom Gamma-only candidate?
This changes cell representation AND Brillouin integration/source mixing.
It is not an isolated proof that k sampling causes/cures the old pathology.
The original e90/cold/k4 reference remains a different numerical model.

Unshifted primitive2x2x2 is the cheapest non-Gamma closed integration mesh:
8 full points, expected Gamma1/L4/X3 star multiplicities, each point a TRIM.
Use native Td reduction as in the previous host; do not disable symmetry or
enforce degenerate occupations. Check actual native k/q coordinates, weights,
spinor normalization and reciprocal frames, not just requested mesh labels.
Native saves contain irreducible states. Tests must distinguish those actual
states from full-BZ states reconstructed with verified crystal spin rotations.
At every TRIM Theta maps G to -G-2k; a Gamma-only G->-G test is insufficient.
Report whole retained density-operator tests, not only scalar/local spin.

**Prospective interpretation gates:** outer `EXX self-consistency reached`,
XML SCF true and final |dexx|<=1e-9Ry; native inner error<=1e-9Ry; finite arrays,
36e charge error<=1e-8e and FD occupation error<=1e-8. Report Gram, Kramers
occupation/energy differences, exact finite-rank Theta norms at all stored k,
and Td covariance in physical G+k frames. Strict symmetry qualification still
requires defects<=1e-8; a smaller but failing result remains failing. Identify
Gamma6/8 through native double-group/physical overlaps with quantified reference
truncation; do not infer from sorted indices. No forced averaging/repair.
Full-H eigenpair residual is not inferred from energy/dexx; absence must be
reported. A scalar-converged but symmetry-broken state is not an accepted
nonmagnetic host. No gap/mass/x_c follows from an unqualified state.

**Resources:** ordinary transient systemd,2 local MPI ranks,one family;
MemoryMax12GiB,swap0,TasksMax12,CPU200%,nice10. Hard6hours; native max_seconds
21000 allows checkpoint margin.100 exchange builds/100inner steps, no automatic
continuation. Host available>=4GiB, disk>=10GiB, own sampled files<=14GiB,
per-file2GiB. Observe simple OS counters and terminate only this unit on hazard.
Sampled disk accounting is not a quota or continuous adversarial guarantee.
No claim of host-wide MPI absence from a cgroup; visible native family checked.
MPI local transports only, TMPDIR/shared-memory backing private. No new socket
owner/lease/launcher implementation. Existing ordinary stock launch is reused.

**Feasibility basis, not a total-memory proof:** pristine `exx.f90` allocates
complex `exxbuff(nrxxs*npol,nbnd,nkqs)` and ACE xi separately. Q2 has8 full
source points rather than old primitive q4's64. At the old f36054^3 EXX grid,
44bands/8sources/npol2 nominal aggregate is1.652GiB, versus13.215GiB at64sources.
New f200 is below f360; actual padding/descriptors and every allocation remain
runtime measured, protected by kernel cap. Old primitive f120 q4 SIX-rank SCF
used4.056GB RSS/2581.5s; old8atomGamma ran10488.5s/4.225GB kernel peak.
These are forecasts only. Actual first EXX FFT/grid/source/cost and peaks will
be recorded. Six hours is a finite authorized diagnostic budget, not a promise
of convergence. If native refuses/fails/time-stops, preserve it and STOP.

Archive input/source/PP/ELF, stdout/XML/wave hashes, trajectory and terminal
manager/cgroup identity. Protect all old failed states and822pins/76originals.
PBE pipeline remains permanently closed; no new infrastructure phase.

## Additional read-only discrimination, registered 2026-10-17 00:31 UTC

The conventional8atom Gamma cell already folds primitive Gamma and3X points
when primitive translations hold; it is not literally a primitive single-k
model. New primitive k2 adds4L points and enforces the smaller periodicity.
Without another native run, test the OLD saved occupied density under the
three fcc half translations: plane-wave signs (-1)^(Gy+Gz),(-1)^(Gx+Gz),
(-1)^(Gx+Gy) in its conventional G basis. Use full finite-rank QR norms and
an independent scalar-density Fourier check. This does not repair/reclassify
the old state. It can identify or bound a separate translation-breaking
confounder; it cannot uniquely establish the cause of the TR instability.
