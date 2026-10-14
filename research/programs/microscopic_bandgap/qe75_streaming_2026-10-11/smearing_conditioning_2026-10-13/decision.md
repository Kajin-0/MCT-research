# Decision: STOP at a native control-side Fermi/neutrality obstruction

**2026-10-13; starts clean pushed1b4c59b.** The cold-smearing explanation of the
historical step4 occupation discrepancy is independently verified. ONE newly
frozen, fresh native control was then attempted; it completed five outer updates,
passed the new scientific gates through4, and was safely refused at5. **No new
streamed member or restart was launched.** Do not claim a fresh paired PASS.

## Actual decision-changing result

Native step5 weighted occupations sum to **36.00559692012919 electrons**, rather
than36. The residual **0.005596920129192995** exceeds the frozen1e-8-electron
budget. The directly captured native ef **0.6714859435488899 Ry** and all-k
weighted occupations reproduce bitwise with the unedited QE Fermi source replay.
Independent analytic evaluation agrees within2.22045e-16 occupations.

At this native ef, the pinned sumkg1/sumkg2 give N'=1.99493e-12 electrons/Ry,
N''=60967.36169 electrons/Ry². The squared-charge error has gradient2.23310e-14
and positive curvature682.45891: a numerically nearly stationary positive-residual minimum, not a
neutral root. QE7.5's Gaussian guess/Newton squared-error minimization can accept
cold-smearing residual<0.01 electrons. The actual0.00559692 falls in that branch.
A bounded, read-only scalar check finds a neutral root near0.669963364989266 Ry;
this is not a replacement native solver or an SCF calculation.

The older control independently shows the same step5 obstruction
(36.00559692416757 electrons), then returns near36 at later steps. Its historical
12-step unconverged trajectory and the old streamed occupation FAIL are preserved.
This new diagnosis neither invalidates their existence nor certifies them under
the new prospective contract. There is no evidence here of wrong streamed Fock
arithmetic: the new stream was never admitted.

| New control measurement | Value |
|---|---:|
| Completed outer updates / accepted updates |5 /4|
| Wall time |202.2887813s|
| Last total / Fock energy |−484.0541752300362 /−8.968516026300037 Ry|
| Last dexx |1.1558833505525001e-3 Ry; unconverged|
| Sampled family RSS / last observed cgroup peak incl.cache |907923456 /1102028800 bytes|
| Minimum sampled host available / disk |30136680448 /25987809280 bytes|
| Maximum sampled aggregate pair output |532279296 bytes|
| Largest output-account sample gap |2.296852s; not continuous protection|
| Cleanup |own unit collected/group empty/exclusive lock released|

## What advanced

**PROVEN:** exact real cold-function Lipschitz bound and stable QR weighted-density
identity; local neutrality inverse requires an explicit nonzero response/branch
condition. **CALCULATED:** all retained steps1–4/ranks/k values reconstruct exactly;
historical step4 bound1.470077639e-8 explains observed1.469269173e-8. First energy/
mu differences occur at step1, not step4. The original1e-8 FAIL remains unchanged.

The prospective protocol derives separate eigen/ef caps9.46969697e-11 Ry from
half the existing1e-8 Ry energy budget and the analytic occupation maximum.
It retains independent energy/density/charge/potential gates. Only the native ef
observer object changed; every exchange/solver/lease archive object is byte-equal
to the successful earlier full-SCF builds. Actual kernel/ELF/JOB/PROFILE/rank
receipts, initial parity and FFT passed; 12GiB/swap0/tasks12/600s limits and sampled
4GiB/10GiB floors held. Aggregate14GiB accounting includes retained native output
of BOTH members; parent owner bookkeeping is separately small and reported,
not represented as a quota. No host-wide exclusion/private-network claim.

## Execution-efficiency limitation

The retrospective audit was initially restricted to the requested paired steps1–4.
The available older control step5 already contained the same charge bias, found
only after the fresh control refusal. Checking ALL retained control states against
the proposed neutrality gate first could have prevented this202s native attempt.
The new run supplies directly captured ef and real refusal/cleanup evidence, but
it was avoidable under this charge policy; it is not independent material
validation. Any future prospective gate must first be screened against every
available retained trajectory, including the unpaired control continuation.

## One precise next requirement, outside this unchanged-solver sprint

**NO-GO for further strict-neutral full-SCF comparison with this unchanged Fermi
solver.** Before another numerical pair, qualify a Fermi-root acceptance rule
that tests charge residual itself and refuses a nonneutral stationary point;
with a documented sign-bracket root branch at the SAME sigma/functional/meshes.
That changes solver behavior/accuracy and requires a separately authorized,
prospectively frozen experiment. Merely allowing0.0056 electrons would need an
independent Hamiltonian/density/energy sensitivity bound; none is supplied.
Do not raise the current neutrality gate, restart the aborted control or run the
new stream against it. Native old-ACE/current-state atomic import remains
unqualified; current scope5 expressly refuses it. Stop this finite sprint here.

No convergence, full-sized memory gain, Cd material result, physical x_c,
new agent/session, goal change, main merge, stock or protected DFT modification.
