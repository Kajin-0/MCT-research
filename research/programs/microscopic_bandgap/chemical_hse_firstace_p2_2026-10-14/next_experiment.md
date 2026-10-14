# Next finite functional-dependence acquisition — not launched

**Recommendation:** measure one HSE orbital/density relaxation at fixed first
ACE in each matched 8-atom member, then one rebuilt direct operator on the new
state, with the same original physical Γ frame. Compare within-member projected
spectra and operator corrections before/after relaxation. This is the minimum
new physics that tests whether the measured +44.184 meV frozen-source chemical
activation survives self-consistency. It remains Γ/q1 and cannot determine the
k3/converged material gap.

## Measured cost and unresolved bound

Host/Cd preliminary SCF: 55.01/52.01 s; EXX initialization: 8.53/1.96 s;
instrumented first ACE: 147.78/142.76 s; total QE: 213.92/199.14 s. Direct probe
capture is included in ACE timing. Actual kernel peaks are 4.232/4.226 GB,
aggregate source exxbuff 1.217 GB. These replace the earlier heuristic subtotal
and pair timing. Runtime overhead and sustained host interference remain variable.

For a fresh run with two ACE builds, substituting the measured same-state cost
would consume roughly 361.70/341.90 s before the new hybrid inner SCF, assuming
the first timed build cost repeats. The remaining 600-second allowance would be
238.30/258.10 s under that assumption. This is an admission-sizing scenario,
not an upper bound: changed occupations, Davidson work and system load may
increase both build and inner-SCF cost. Full HSE convergence has no measured
outer count or transversality/residual bound and is not admitted now. Later
allocation/restart lifetimes have not been tested by this one-build pilot.

A future finite experiment must prospectively stop after at most one hybrid
inner solve and the second operator reconstruction, with the original 600 s,
12 GiB/swap-zero/tasks-12 and disk/output guards. Require unchanged physical
inputs, fresh state and leases, actual source convergence/charge, native HSE
wave/density consistency, direct/ACE equivalence on the refreshed source,
physical Γ embedding and explicit false outer-convergence status unless native
outer criteria independently pass. Incomplete iteration or timeout is a partial
result, not convergence. Stop on first failure; no retry or prolonged continuation.

No old refused/failed state or first-ACE save is assumed restartable. The present
ELF deliberately exits at first ACE and cannot perform this experiment. A new
private stop/capture counter must be qualified without changing exchange, Fermi,
cutoffs, geometry, bands, k/q, solver accuracy or old evidence. Do not launch
until that narrow source/state/lifetime and resource admission is established.
The user authorized only first ACE here; further native work needs new scope.

Minimum information gained: relaxed Γ projected spectra, true hybrid residuals,
charge/density response, second Fock and dexx, and actual per-iteration cost.
It tests a concrete missing material response, rather than refining generic
ownership machinery. Longer-range k/q and full convergence remain subsequent
separate uncertainties. No physical x_c follows from this finite ordered cell.
