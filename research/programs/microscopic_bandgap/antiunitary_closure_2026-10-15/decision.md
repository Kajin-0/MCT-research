# Actual-source closure qualified; original density-preserving repair impossible

2026-10-15. New read-only phase from d6b95cc; no native execution in this package.

CALCULATED from retained full complex native spinors, direct-residual SVD:

| Source | Missing directions >1e-8 | Full density TR operator defect |
|---|---:|---:|
| 1, preliminary PBE |166|5.197963e-7|
| 2|122|.001428199|
| 3|176|.007882564|
| 8|176|.999986742|

At1e-5 source1 has2large missing directions; at1e-6 it has10, at1e-7 it has66,
and at1e-9 all176. Thus the old two-large-leakage observation does not justify
an178-column repair at1e-8. These are stable direct-residual numerical ranks,
not an exact-rank theorem about floating/native data. The earlier cancellation-
sensitive square-root counts and Gamma-frame lower witness are preserved.

The native preliminary PBE core142 support has TR leakage5.1781e-7, its
fractional143–146 support2.4792e-7, and the empty147–176 support.90525. All142
core weights are exactly1; central weights differ around.5 at~1e-11; empty
tail charge is negligible. Hence the large empty-space cutoff issue is distinct
from the smaller but real occupied-support defect. A correct charge or near-
degenerate quartet does not supply an exactly invariant density.

PROVEN: the nearest invariant Hermitian density is Dbar=(D+ThetaDTheta^-1)/2,
at distance ||D-ThetaDTheta^-1||/2. A basis rotation preserving D cannot remove
this obstruction. Changing occupations/orbitals would be a NEW constrained
ensemble protocol, not an old-run repair or a newly converged PBE/HSE state.

CALCULATED constructive cover:352auxiliary columns, source-cover residual
1.1094e-14, TR closure1.0363e-14, Gram1.0355e-14; paired transformations are
bit-exact. No density/occupation was edited. This is a stable sufficient cover,
not an optimal approximate dimension claim. All source Grams of -Fock are
positive (.036–.037Ry minimum, condition~25), but their enlarged Gram is unknown.

Three independent tiny checks PASS: complete ACE symmetry/source exactness;
counterexample to averaging a nonclosed ACE; constrained-ensemble energy
derivative and counterexamples to augmented-Gram and unequal-weight shortcuts.
These are mathematical/model checks, not material validation or novelty claims.

**Advance one independent operator-constructor qualification only.** Source
completion is now constructive; direct actions on the extra columns remain the
missing operator input. A new explicitly labelled TR-constrained fixed-source
ensemble test can measure them and energy/source accounting without SCF, Cd,
occupation fitting or force claims. It must declare that it changes D to Dbar,
retain the old BYTE refusal and use independently frozen numeric controls.
No original host/Cd full-SCF release follows. No physicalx_c is claimed.
