# R07 completed-reference review: the material-input boundary persists

Date: 2026-10-11. Contribution: R07 only. This is a read-only review of
outputs completed by the previously established DFT supervisors, not a new
calculation. The [threshold-aware decision](threshold_causal_2026-10-11/cycles_and_boundary.md)
remains in force. No physical inversion composition is inferred.

## Newly available evidence

**CALCULATED:** both existing supervisor state records now report terminal
completion. Their latest HgTe reference records pass their native SCF acceptance
gate: return code zero, native `JOB DONE`, native EXX self-consistency reached,
accurate empty states and a 1e-10-Ry SCF threshold. These are numerical
acceptance conditions, not proof of material accuracy. No full impurity SCF
was launched by these completed sequences.

The two references use HSE+SOC, SG15 NC potentials, a=6.46 Angstrom,
90-Ry wavefunction cutoff and k4/q4 grids. Their native Fock cutoffs are
360 and 120 Ry. Native symmetry assignments and orbital-character records
identify Gamma6 bands 33–34 and Gamma8 bands 35–38 in each reference.

| Existing control | Source-qualified result | Interpretation |
|---|---|---|
| 360-Ry Fock reference | signed Gamma gap -0.28976341236020176 eV | Accepted numerical binary reference |
| 120-Ry Fock reference | signed Gamma gap -0.28977011377785367 eV | Accepted numerical binary reference |
| Difference, 120 minus 360 | -6.7014176519109014e-6 eV | Numerical cutoff difference in this binary Gamma gap |
| Reported six-state Gamma reaction-kernel norm | 4.205828324256838e-6 eV | Pointwise comparison in the same physical host projector |
| Maximum sorted-band difference, 64 k points and 44 bands each | 5.8279960256868435e-5 eV | Eigenvalue comparison; no finite-q operator-norm conclusion |

The pointwise kernel is evaluated at z=(8.809990166855265+0.025i) eV in
the native QE energy reference. Its omitted-window inverse certificate is
4.458892854275447e-15 eV **assuming exact native eigenpairs**. This controls
one spectral-window error at that point; SCF, grid, model and material errors
are separate. The source record explicitly leaves the physical Fock
approximation, impurity vertex and dilute-limit accuracy unvalidated.

## Independent checks and provenance

The [frozen review record](../../../data/calculated/r07_completed_reference_review_20261011.json)
pins 23 external source hashes, including the terminal supervisor records,
SCF inputs/results/output, native schemas, Gamma spinors, sector records,
control driver and potential manifest/files. DFT source commit:
`422d71de02df56edae96e47e1a71931e073b48ad`. MCT analytical parent:
`954574f058e50abfd0c4d76d9020f23c460c4cca`.

Checks independently read native termination messages, parsed the two
64-by-44 eigenvalue arrays, recomputed the Gamma sector means and sorted-grid
differences, and recomputed the norm of the reported complex six-state kernel
matrix. They verify numerical consistency and source provenance; they do
not independently re-extract that kernel from the spinors. No native adapter
or supervisor was rerun, changed, stopped or restarted. DFT files were read
only. The preceding 1802-test analytical validation remains associated with
the analytical parent commit; this review changes no code or tests.

## Why this cannot certify a physical inversion

**OPEN:** the accepted binary references do not supply the interior alloy
mass contraction, its composition modulus, a common support-free domain, or
uniform branch-denominator errors. A complex-energy comparison of two HgTe
references is not an error estimate for the true alloy at real energies.
In particular, neither the 6.70-micro-eV gap difference nor the pointwise
kernel norm can be inserted as epsilon in the [T16 root certificate](threshold_causal_2026-10-11/derivation.md).

**PROVEN UNDER ASSUMPTIONS, retained:** matching endpoints, infrared channels
and finite regular moments can still leave different exact inversion roots.
The requisite new physical information remains an independently qualified
interior projected mass contraction or sign bracket, or a controlled
microscopic bound that fixes it. Its support/existence and composition
transversality conditions cannot be replaced by numerical binary convergence.

The [ranked input matrix](threshold_causal_2026-10-11/cycles_and_boundary.md)
therefore keeps the same ordering. Existing native binary references improve
the available supporting infrastructure, while the highest-information
mass/domain/modulus inputs remain missing. No precision escalation or new
expensive computation follows from this review.

## Concise decision ledger

| Finding | Status | Decision |
|---|---|---|
| Existing native reference acceptance | CALCULATED | Record the newly completed controls; preserve earlier failures as historical evidence |
| Numerical Fock-cutoff comparison | CALCULATED | Accept its pointwise binary scope; retain finite-q/material limitations |
| Interior mass/domain/root budget | OPEN | No qualified input found; physical x_c remains unresolved |
| Current R07 disposition | Missing-input boundary | Stop physical prediction; acquire no new numerical work under the current restriction |

No material validation, new theorem or novelty claim is made in this review.
All earlier full/residual-T, strain, threshold, continuum, directional/SOC,
projection-window and exchange-quadrature findings remain binding. The
persistent research objective is unachieved; completed numerical controls
do not make it complete.
