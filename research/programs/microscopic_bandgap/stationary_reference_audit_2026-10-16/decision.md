# Reuse the original numerical HSE host frame; refuse a hidden stationary-state transfer

2026-10-16, clean pushed baseline **9a83424**. **READ-ONLY assessment complete.**
No native DFT/HSE/MPI, new optical search, outreach, build or DFT command/worktree
mutation. Python/HDF5 analysis ran from MCT, borrowing the existing interpreter
with bytecode disabled; no DFT drivers/modules were executed. Old failures and
SCF acceptances remain immutable. No physical x_c or material uncertainty.

**Decision-changing answer:** **YES**, both accepted original e90 k4/q4 HgTe
SCFs and their native wavefunctions survive and supply a useful physical Γ6/Γ8
numerical host frame. They can replace D0 as a reference/initial-state source.
**NO**, neither currently qualifies an exact1e-8 nonmagnetic FD/full-H state,
an e50 Γ-only stationary transfer or the missing screened Cd operator. Further
H304 block acquisitions are not the required reference step.

## New facts beyond the earlier P1 inventory

| Native retained quantity | f360 | f120 |
|---|---:|---:|
| Original SCF XML convergence / EXX stdout | accepted / reached | accepted / reached |
| Final inner energy-error estimate, Ry |1.24016e-11|1.64628e-11|
| Native electron count; independent saved-rho count |36;36.00000000000001|36;36.00000000000001|
| Γ8 energy spread, eV |1.57948e-8|1.95782e-8|
| Γ8 cold occupation spread |8.55461e-7|1.06037e-6|
| Γ nonlocal-density cubic compressed witness |8.53898e-7|1.04147e-6|
| Saved ACE relative cubic defect on six Γ probes |2.41772e-8|9.15257e-8|
| Saved ACE relative Θ defect on six Γ probes |2.37337e-8|1.04547e-8|

**CALCULATED:** exact cold wgauss occupations reproduce the original arrays
within1.64e-13, both weighted counts reproduce36e. An independent FD charge
root on those **stored eigenvalues** shifts μ by−1.895584meV and changes
occupations by at most3.51e-7; it is NOT a new self-consistent state. All24Td
Γ6/Γ8 span defects remain ~1e-14. Full64-point f120 density tests include
Θ and cubic generators; their conservative upper bounds do not certify
whole-density1e-8 symmetry. Do not equate compressed witnesses with upper bounds.

The original `r07.save` XML hashes match the pre-existing expansion-parent
pins. `r07_open.save` is an expanded export with placeholder SCF fields,
not the convergence authority. Γ coefficient differences from original are
~2e-16; charge datasets match exactly though HDF5 container hashes differ.
**Byte-identical state replay is NOT established.** New source pins preserve
the full currently accessible original/exported files; they do not manufacture
historical fingerprints of a complete direct-exchange/local-potential bundle.

The six physical e90 Γ spinors also have measured nonzero high-G weight above
e50: Γ6≈2.038e-6, Γ8≈1.278e-7. Discarding/renormalizing it is a changed frame.
The old f360/f120 Γ agreement is not a finite-q chemical or global-H error bound.
Small primitive occupation/symmetry defects are not the earlier severe broken
176-source host failure, and neither past result is retroactively reclassified.

## Precisely missing input and numerical acceptance

[Theory/input contract](theory_and_contract.md) fixes the required common
Hilbert space, Hamiltonian/density/source, energy gauge and observable. Retained
host eigenpair/full-H residual and stability are still unbounded. Changing cold
smearing to FD or changing cell/quadrature requires nonlinear H[D] consistency,
not six auxiliary occupations. A trace/free-energy/dexx flag cannot certify it.

The minimum **chemistry-bearing** input is an aligned, independently
self-consistent Cd-in-HgTe H_c[D_c] packet with fixed host projectors, full
complex spectra/actions, induced local+SOC+Fock response, coverage and residual
errors, plus a matched pure-cell/folding control. D_c is not reconstructible
from the host alone. Define mean and disorder once from the same configuration
operators; do not add screened chemistry twice. Physical dilute/random-alloy
inversion further requires image/statistical/material and observable-eligibility
inputs. Old full/residualT, retarded/PV, heavy-hole and root no-gos remain.

A projected static gap changes by at most2||PδHP||; a prospective2-meV
matched contrast budget can allocate1meV per cell including all frame/operator
errors. This is an illustrative sufficient NUMERICAL contract, not achieved
accuracy, a replacement for frozen1e-8 gates or physical mass. The bound on
physical x_c remains ε_m/s only when a qualified mass, bracket and independent
slope lower bound s exist; neither material quantity is available.

## Resources and final gate

[YES/NO and resource table](qualification_and_resources.md): source-matched
primitive f120 EXX buffer2.75GiB, f360~13.21GiB, original16atom f120 **22GiB**.
The latter already exceeds the12GiB cap before other allocations; old21.3GiB
dry/26.7GiB interrupted evidence does not qualify a launch. H304's5.56GB is a
different operator/state/workload. **NO-GO for stock original matched chemistry
under12GiB.** No cheaper HSE launch is invented.

A further native/source cross-check found BOTH archived `open_grid` expansions
used54³ EXX FFT: the exporter temporarily raises f120 to4*ecutwfc. Its nominal
13.21GiB buffer also fails12GiB admission. Reuse the already saved exports;
regenerating them is not a cheap preparation. No postprocessor was run here.

The nearest prospective reference improvement is a same-state primitive f120
DIRECT full-H residual packet using the accepted source, not D0. Its buffer
subtotal/history makes it a candidate only; a complete TWO-rank RAM/output/time
envelope, source replay, science/owner gates and new authorization are missing.
No native feasibility PASS is issued by this read-only phase. Even if that
packet passes, nonlinear Cd chemistry is still indispensable and resource-blocked.

**STOP at this precise boundary.** Reusable numerical frame YES; stationary
FD/direct-H transfer and screened chemical mass NO. Existing PBE chemistry and
H304 conditional operator results retain their definitions. Verification uses
real saved data, independent charge/root/tail arithmetic and source capacities,
not another synthetic mass example. No novelty/material/convergence promise.
