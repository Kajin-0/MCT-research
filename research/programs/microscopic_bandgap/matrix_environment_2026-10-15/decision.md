# Matrix environment physics — decision, 2026-10-15

**ADVANCE the conditional finite-resolution matrix contrast. NO-GO for a
static local N2 operator, material dynamic susceptibility, or physical x_c
from these spectra alone.** Read-only follow-through after the new same-D HSE
acquisition committed in f249885; no further native job was issued.

## CALCULATED from accepted native PBE chemistry

Same 16-atom cell, x=.25, sharing Cd(0,1) minus unshared Cd(0,7), fixed native
50Ry host Gamma6/8 complex frame. All nine frozen probes t=-.1,0,+.1 eV and
eta=.025,.05,.1 eV are evaluated relative to each specimen's own EF. Full
complex contrasts are archived in matrix_differences.npz; source/input hashes
and exact rows are in result.json. No empirical fit or new spectrum alignment.

At the primary t=0, eta=.05 eV:

| Quantity | Actual value | Conditional fixed-frame omitted-measure uncertainty |
|---|---:|---:|
| Green contrast norm | .875714265 /eV | <=.046593132 /eV |
| Inverse-kernel contrast norm | 82.917971 meV | <=25.238386 meV |
| Norm lower bound | **57.679585 meV** | same finite-data assumptions |
| Gamma6-8 normalized trace contrast | -81.658351 meV | [-132.135124,-31.181578] meV |
| Trace half-mass coordinate | -40.829176 meV | not the physical crossing mass |
| Trace common coordinate | -40.887956 meV | own-EF referenced |
| Off-block norm / Gamma8 anisotropy | 9.240132 / 2.070061 meV | raw, not individually sign/norm certified |

All nine matrix-norm lower bounds are positive; the smallest is 26.880005 meV.
Trace contrasts span -92.631569 to -73.113064 meV across those probes. Matrix
inverse identity and internal block-unitary covariance errors are below 1e-15.
Positive spectral causality passes for each specimen. This is a continuum-
compatible finite-resolution observable, not a sharp eigenvalue/gap, impurity
T, linewidth or random-alloy self-energy. Full-matrix bounds condition on the
EXACT chosen physical frame; arbitrary nearby-frame transport is excluded.
Native eigenpair/SCF, cell/BZ, functional and material errors are not included.

The earlier scalar inverse contrast -81.474454 meV and Gaussian W2 contrast
-2.076649 meV retain their own definitions and verdicts. The Gaussian sign
remains unresolved. The new matrix result does not revise either observable
or convert ordered same-composition chemistry into an alloy gap.

## New falsification and minimum information

The retained analytic trace derivative is -.090244349 dimensionless. Independent
central differences agree below 3.6e-10. A new noncommuting resolvent bound
reduces its matrix uncertainty from 15.239626 to .589217, but its trace sign is
still unresolved. Positive normalized completions explicitly realize both
signs if no omitted-support ordering is supplied. Zero-energy examples are
NOT admissible under exact lowest-352 ordering, which has not been certified.

Only a coarse independent omitted-support certificate L>.206595624 eV above
each own EF is sufficient to settle this derivative's sign within the fixed
data model. Merely reporting the highest printed band at about 7.96 eV is not
such a certificate. This is a concrete information budget, not a parameter
chosen to fit a desired material result. No physical A or T' is extracted.

Even an ordered omitted tail does not identify the static moment: independent
20/40 eV matrix completions preserve all retained data but change the static
trace by 20.93/22.59 meV. Their Green differences are only about 2.7e-5/eV.
This disproves static-operator identification from finite-eta partial spectral
data without extra moment/Hamiltonian input. It does not disprove uniqueness of
a fully specified atomic Coulomb problem. Proofs and limitations are in
theory.md; verification.json records independent noncommuting tests.

## Geometry and ranked next physical input

All 56 three-Cd subsets of the same 16-cell were enumerated. Thirty-two contain
one N3 Te environment, with histogram (1,3,3,1,0); 24 have (0,4,4,0,0). Candidate
Cd(0,1,2), x=.375, has actual nearest-neighbor counts (3,2,2,2,1,1,1,0) and
chemical point-group order 6. Independent periodic Cartesian nearest-four
geometry agrees. One such new SCF would add composition/environment evidence,
but cannot isolate N3 against the current x=.25 cells. See next_input.md.

1. **HSE H[D0] on 152 new action-completion directions.** This addresses the
   measured FD-state obstruction in the new 304-space; known H[D0]Q need not be
   repeated. Native same-D state/query admission must be extended before use.
2. **If a static PBE contrast is needed: full native H on six physical probes
   at EACH retained configuration's own SCF density.** Twelve actions resolve
   the projected static moment, without another SCF or many more bands. They
   still do not determine a complete local N2 tensor or background locality.
3. **For this derivative: a coarse omitted-support/eigenpair certificate.**
   It is logically cheaper information than a full new spectrum; attainable
   fidelity/cost remains open, and it does not by itself validate the material.
4. **N3-bearing x=.375 PBE acquisition**, or two new same-x cells for a true
   configurational contrast. Cost forecast is based on actual 16-atom native
   work, not a new resource admission. No such job is queued.

**STOP at those specific acquisition/certification boundaries.** This phase
continued after the native HSE milestone through matrix physics, derivative
falsification and geometry/identifiability. It did not repeat PBE grids, broken
HSE iterations or generic ownership tests. No convergence or physical x_c.
