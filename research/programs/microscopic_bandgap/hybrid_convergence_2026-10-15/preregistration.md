# Bounded fresh HSE outer evolution — frozen before launch

2026-10-15. New long-horizon user authorization, parent04d767c. One fresh
Hg4Te4 control and then CdHg3Te4 only if control owner/science/resource gates
pass. No retry of an admitted failed job. No historical state is restarted.

Physical inputs are unchanged: eight atoms, orderedx=.25, a6.46Å, fixed ions,
SG15 fully relativistic norm-conserving pseudopotentials,176 spinor bands/144e,
HSE fraction.25/screen.106Bohr^-1,50/200/Fock200Ry, Gamma/q1, FD sigma.001Ry,
Davidson/full accuracy, mixing.3, conv_thr1e-9Ry, adaptive_thr=false,100 inner
steps, native occupation/EXX/ACE/local-XC arithmetic. Fresh atomic/random start.
The original6 physical Gamma references embed by actual G labels, unchanged.

Run at most EIGHT source/ACE builds (preliminary plus at most seven hybrid inner
solves). Stop with convergence=false when this budget is exhausted. A true
native dexx<1e-9Ry with inner error<=1e-9Ry is required for numerical HSE outer
convergence. A nonconverged eight-build trajectory is a useful finite acquisition,
not convergence or a bound on its uncomputed remainder. No extra outer solve
after the budget and no automatic extension. Native max_seconds1700; hard owned
deadline1800seconds. Total mission allocation initially <=60wallmin/member;
this fresh control consumes <=30wallmin/member. Any future restart qualification
consumes the remainder and must be justified independently before launch.

## Explicit bounded-deadline justification

Accepted04d767c measured two builds plus one hybrid solve at410.33/409.31s,
kernel peak4.549/4.542GB, host RAM floor25.24GB and disk floor62.09GB. Previous
first builds were216/201s. Six additional updates are estimated at~200s each;
1800s is a finite monitored allowance, not a proven completion bound. User
explicitly permits a separately justified larger bounded cap. Keep12GiB kernel
memory, swap0/tasks12, two local ranks/one family, host available>=4GiB and disk
free>=10GiB, aggregate new pair output<=14GiB sampled,1GiB/file. Enforce Nice10,
CPUQuota200%, CPUWeight10, IOWeight10 and read actual cpu.max/cpu.weight before
MPI. This limits owned CPU competition; it does not prove no external impact.
Host floors and memory/OOM/tasks/output checks remain active. At first instability
or limit failure stop owned group and do not launch the next member. No quota
or continuous between-sample output guarantee is claimed.

## Scientific acceptance and observations

Reuse unchanged source gates at EACH build: correct176/144/Gamma/Td/HSE/frame;
finite complete rank-bound packets; SCF error<=1e-9Ry; weighted charge error
<=1e-8e, FD consistency<=1e-9; direct/direct contraction and direct/ACE action,
Gram/Hermiticity/sign/normalization relative tolerances1e-8. Final source wave
must match native HDF5 bytes; XML et/wg export2e-14Ry. Prior source packets are
retained, not falsely called separate HDF5 saves. Within each rebuild rhoR/rhoG/
G/probe bytes remain equal; across updates density changes are measured physics.
All native signed dexx/fock0/1/2 relations checked with the original1e-8 relative
allowance; retain any negative signed value before native abs. Native convergence
flag and dexx must agree. Final eigenvalues solve the previous ACE; for true
outer convergence this remains a finite numerical residual, not exact equality.

Report fixed-frame direct-exchange and local total matrices at each source,
Cd-minus-host Gamma6/Gamma8 normalized traces, density and orbital changes,
native total/Fock/dexx/charge series, actual resources and convergence truth.
Do not add operator shifts to PBE Gaussian centroids. These ordered-cell Gamma/q1
results are not BZ convergence, a random-alloy gap, quasiparticle gap or physicalx_c.

Capture exact ethr/tr2 and localv/vnew in ADDITION to prior complete packets for
future clean-boundary restart analysis. Their presence alone does not certify
restart: actual dependent state, native import and an independent fresh-control
comparison remain required. Inner-interruption old/new-ACE counterexamples and
all previous failures remain unchanged. Never use old diagnostic saves as valid
restart by assertion. Stock QE, dirty DFT, original16atom352band, other sessions,
supervisors, Calcura, main and historical blocked goal are preserved.

Before service: exact hashes, fresh root/jobs/nonces, <=107byte socket addresses
for BOTH members including NUL allowance<=108 and actual disposable bind/cleanup,
old ledger/known flock, protected DFT, source/backend/PP and current host resource
checks. Local-owned pilot does not pass historical host-wide/network exclusion.
Archive raw numeric evidence, source and falsification; commit/push research only.
