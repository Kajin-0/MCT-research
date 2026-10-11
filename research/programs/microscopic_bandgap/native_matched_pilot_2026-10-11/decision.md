# Terminal approved-pilot decision

**HOST_RESOURCE_STOP; Cd NOT ADMITTED; STOP.** One approved native six-rank
HSE+SOC matched 16-atom n2/k2/q2 f120 host ran. The unchanged guard stopped its
owned MPI family during exact-exchange initialization. No substituted SCF,
restart, variant, additional native postprocessor or queue followed. No physical
signed alloy gap, impurity response or x_c is obtained.

## Measured sequence and gates

The first [preflight](preflight.json), 19:22:26 UTC, correctly rejected
26.39040 GiB available against the declared 27.524-GiB guard. After the user
reactivated the original goal and external RAM pressure subsided, the
[resumed preflight](resumed_preflight.json), 19:45:02 UTC, measured 29.27615 GiB
and passed **the identical policy** with no competing MPI/R07 driver. This was
a changed external condition, not a smaller physical input or relaxed gate.
The already authorized host started at 19:48:51.848 UTC and stopped at
20:01:04.237 UTC. [Result](host_result.json), [telemetry](host_telemetry.jsonl)
and [independent audit](terminal_audit.json) preserve native evidence.

| Quantity / gate | Observed result | Implication |
|---|---|---|
| Wall time | 732.39 s; last sample 731.37 s | Below 3600+1800 s; not a time-limit failure |
| Identity-tracked family RSS peak | 26.72213 GiB | Exceeds retained 26.63966-GiB family cap |
| Minimum sampled available RAM | 2.76587 GiB | Below 4-GiB soft reserve, above 2-GiB hard floor |
| Minimum sampled free disk | 30.48957 GiB | Above both disk guards |
| Family / foreign MPI | Seven processes: launcher plus six ranks; no foreign MPI in 354 samples | No ownership conflict |
| Initial adaptive inner SCF | Six iterations; last estimated accuracy 6.87e-6 Ry | Not the final 1e-10-Ry HSE solution |
| Exact exchange | ACE initialization began; EXX self-consistency marker absent | Exchange gate FAILED |
| JOB DONE / return | Absent / 1 after owned resource stop | Native SCF gate FAILED |
| Host projector, irrep and 1-meV comparison | NOT EVALUABLE on an accepted host | No scientific host admission |
| Cd stage | NOT RUN; no Cd output directory | Conditional authorization never became admissible |
| Terminal process check | All owned descendants terminated; fresh MPI/R07 snapshot empty | No live handle to resume |

Output size measured before writing the final result is 11,870,316 bytes.
Raw native scratch/wavefunctions remain in the unique native output and are
not committed here. Full stdout, executed deck, PP, source and supervisor hashes
are retained. All 17 original source/supervisor pins verify after the stop.
Existing dirty DFT files are preserved; new native driver/output belong only
to this approval.

## Uncertainty and retained source check

**CALCULATED:** the final telemetry sample crosses only the RSS guard. The
monitor's final snapshot gives a slightly larger peak than the last telemetry
row. Observed RSS is about 1.256 times the 21.27-GiB dry estimate. Summed RSS
can double-count shared pages, so this ratio is not a rigorous private-memory
underestimate. Independently measured MemAvailable confirms narrowed headroom.
This is an **interrupted-run** sampled peak, not a full-SCF peak or upper bound.
Successful runtime, full scratch growth, exchange convergence, residual errors
and RAM needed for completion remain unknown. No inevitable-OOM theorem follows.

The [Td reference check](reference_irrep_bound.md) uses only earlier accepted
primitive HgTe spinors, without QE postprocessing. Independent group and
angular-momentum checks support their Gamma6/8 labels, with an accidental-quartet
counterexample. Its arithmetic envelopes are conditional model estimates, not
interval-certified HSE eigenpair/material errors. It cannot admit the failed
host or supply a chemical response.

## Qualified next action and scientific boundary

The ranked missing physical input remains an independently self-consistent,
matched chemistry-bearing Gamma spectral packet in a fixed physical frame,
with unresolved weight and observable error bounds. Binary spectra, sorted
bands, irrep labels and the failed host do not determine its Q/V orientation
or response. Prior orientation, periodic-image and continuum counterexamples
remain decisive; no empirical gap coefficient closes this missing information.

This acquisition route additionally needs an independently justified resource
environment/containment plan with adequate full-exchange RAM headroom. The
26.72-GiB interrupted peak is an observation, not a planning upper bound.
Any future attempt needs **fresh scope authorization** and resource review.
Recovered RAM does not authorize a retry of the sole approved host. No reduced
cutoff/grid/band count, relaxed threshold or alternative job is selected.
A converged future pilot would still be a finite periodic approximate-model
mechanism test, not a dilute t_H, full alloy law or physical x_c.

The original research goal is active and unachieved; this resumed turn produced
new measured evidence and a bounded reference check, so it is not marked
complete or blocked. This finite approved acquisition is terminal. No repeated
cheap check can manufacture the missing physical packet.

## Later persistent-goal blocked audit

The preceding active-goal statement records the progress turn at `4e8c73f`.
Two subsequent read-only continuations found the identical terminal host record,
no Cd packet and no live native handle. The same indispensable input boundary
therefore recurred across three resumed turns. The goal service now returns
**blocked**; the full objective remains unachieved. [Audit](goal_boundary_audit.json)
records the count. No new scientific finding, physical coefficient, native
retry or supervisor action follows; stop repeated checks until new independent
input or fresh resource-reviewed scope changes the boundary.
