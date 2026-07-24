# R06 Phase 1C project-defined simplified Kane targets

These targets validate a dimensionless nonparabolic statistics prototype. They do not validate HgCdTe material parameters.

## K0 - input domain

Reject nonfinite reduced chemical potential, nonpositive temperature, nonpositive density scale, negative nonparabolicity, negative reduced energy, and inadequate quadrature controls.

## K1 - explicit model identity

The closure identity must remain

```text
project_defined_isotropic_simplified_kane
```

and must not contain the names Madarasz or Lowney.

## K2 - density-of-states positivity

For `beta>=0` and `epsilon>=0`,

\[
\sqrt{1+\beta\epsilon}(1+2\beta\epsilon)>0.
\]

## K3 - parabolic reduction

At `alpha=0`, density, compressibility, and generalized Einstein factor must agree with the merged parabolic Fermi closure.

## K4 - thermodynamic derivative

The directly integrated chemical compressibility must agree with a centered derivative of density with respect to reduced chemical potential.

## K5 - generalized Einstein identity

\[
\Theta=\frac{n}{k_BT\,\partial n/\partial\mu}
=\frac{I_n}{I_\chi}
\]

must close to numerical precision.

## K6 - nonparabolic density-of-states enhancement

At fixed explicit parabolic density scale, positive `alpha` must increase both density and compressibility relative to `alpha=0`.

## K7 - monotonicity

Density must increase monotonically with reduced chemical potential.

## K8 - Boltzmann limit

At sufficiently negative reduced chemical potential,

\[
\Theta\rightarrow1
\]

for fixed nonparabolicity.

## K9 - scale separation

Density and compressibility must scale linearly with the explicit parabolic density scale. `Theta` must remain independent of that scale.

## K10 - quadrature refinement

The dimensionless integrals must be stable under declared quadrature refinement.

## K11 - frozen numerical points

The implementation must reproduce the three high-precision dimensionless regression points in `project_kane_reference_points.json`.

These are internal numerical references, not primary material-validation points.

## K12 - protocol compliance

The closure must satisfy the carrier-statistics protocol merged in PR #381.

## K13 - parameter transparency

The reduced nonparabolicity must be reported as

\[
\beta=\alpha k_BT.
\]

No hidden composition, gap, effective-mass, or temperature relation is permitted.

## K14 - material boundary

Passing K0-K13 does not authorize:

- an HgCdTe value of `alpha`;
- an HgCdTe density scale;
- full three-band Kane equivalence;
- intrinsic neutrality;
- source-exact Madarasz/Lowney reproduction;
- material-accurate density, susceptibility, screening, transport, or noise.
