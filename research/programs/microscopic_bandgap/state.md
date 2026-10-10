# Program state: microscopic zero-temperature bandgap

**Portfolio contribution:** R07

**State:** reference and direct-alloy audits complete; physical impurity input unresolved

**Updated:** 2026-10-10

## Objective and scope

Derive an interpretable, no-alloy-gap-fit equation for the signed
Gamma6-minus-Gamma8 gap and its inversion. The user explicitly authorized this
research continuation on 2026-10-10. Related endpoint infrastructure is tracked
in issue #4; this work does not alter R02's thermal or first-principles gates.
Temperature and empirical coefficient tuning are outside this tranche.

## Current evidence

**PROVEN:** full host-referenced impurity T cannot also be added as a residual
to a binary chord. The correct residuals are t_H=tau_H-DeltaM and
t_C=tau_C+DeltaM. The handoff mass law is valid with these residuals.

**PROVEN:** for an embedded lattice Green function, g'=-P G^2 P*, generally
not -g^2. At complex energy the positive scattering-cloud norm is
-Im(T)/eta, generally different from -Re(T').

**PROVEN:** a three-dimensional quadratic threshold with nonzero constant
scattering amplitude allows finite T but divergent T'. An exactly integrable
independent-impurity example has an x^(3/2) pole correction, so bounded Hermite
remainders and finite endpoint curvatures need a regularity check.

**CALCULATED:** Schindler's published sp3d5 binary model has been rebuilt.
Gamma signed gaps are -0.3015709 and +1.5981345 eV. X and L checks, SOC,
time reversal, finite-q uniform-vertex closure and embedded sum rules pass.
Its VCA inversion is x=0.1816612.

**CALCULATED:** for the explicit quarter-share Te partition and 0.4 eV source
offset, exact single-impurity resummation retains a large static discrepancy.
On a 30^3 grid at eta=50 meV, the corrected common-mode cubic root is
0.3321358; the branch-pole reciprocal reduction root is 0.3496545.
Using full T twice instead gives 0.1646405, a spurious apparent success.
These are finite-broadening diagnostic interpolants, not physical x_c predictions.

**CALCULATED:** at the CdTe Gamma8 threshold the real gap-side derivative
grows from 13.58 to 63.02 as the even grid increases from 6^3 to 30^3,
while T8 remains finite (1.276 to 1.305 eV). Finite-gap detuning regularizes
the trend. This disfavors extracting a constant dynamic A from the unqualified
endpoint derivative of the full lattice T.

**CALCULATED:** explicit n=8 and n=12 random supercells of the same frozen
linear-substitution Hamiltonian give Gamma spectral-peak separation -138 meV
at x approximately 0.18, and a peak crossing near x=0.30. The latter is not
a topological-invariant determination. Iteration, two seeds, box size and
eta=5–50 meV controls support the large discrepancy beyond the endpoint
interpolation. No empirical gap coefficient was used.

**PROVEN:** every configuration of this linear model has the VCA Gamma
spectral centroid exactly; its spectral maximum need not coincide with it.

**PROVEN within scalar CPA:** self-consistency changes the declared
independent-host x^(3/2) threshold correction to x^2. CPA DOS edge, Gamma
spectral peak and real-denominator root have different x^2 coefficients.
The conventional omitted-cluster indicator remains order one in the same
layer. This is not a controlled asymptotic statement about exact HgCdTe.

**HYPOTHESIS:** a physical, self-consistent substitution potential may still
reduce the static discrepancy through environmental response and charge transfer.
The current test supplies no evidence that resummation alone is sufficient.

**NOVELTY CANDIDATE:** none established in this tranche. The value is the
specific falsification and corrected HgCdTe prediction protocol. Generic Dyson,
optical-theorem, threshold and interpolation mathematics is established.

## Artifacts

- [Calculation and interpretation](result_2026-10-10.md)
- [Direct-alloy and self-consistency result](result_2026-10-10_self_consistency.md)
- [Reference and threshold derivation](../../../docs/derivations/impurity_reference_and_threshold.md)
- [Self-consistent threshold and centroid derivation](../../../docs/derivations/self_consistent_threshold_and_centroid.md)
- [Frozen endpoint reductions](../../../data/calculated/sp3d5_endpoint_reductions.json)
- [Threshold convergence](../../../data/calculated/sp3d5_cdte_threshold.json)
- [Figure](figures/impurity_reference_and_threshold.pdf)
- [Direct-alloy and threshold figure](figures/self_consistent_threshold_and_alloy.pdf)

## Validation

Latest full repository suite: **1773 passed**, including 25 new tests across
the reconstruction and self-consistency tranches.
Independent checks include a full finite-Hamiltonian inverse, numerical T
derivatives, positive off-spectrum norms, the causal optical theorem, direct
threshold quadrature and a bracketed concentration-pole solve.
New checks include random-cell dense inversion versus Lanczos, exact folded
binary spectra, spectral-centroid closure, the full scalar CPA equation,
implicit derivatives, threshold coefficients and the pair indicator limits.

## Next decision-changing work

1. Obtain or compute a common-gauge, self-consistent Cd-in-HgTe potential and
   the reciprocal Hg-in-CdTe potential with defensible binary electronic structure.
   The present PBE endpoint artifacts are not adequate meV-level inputs.
2. Use the corrected full/residual conventions and define the HgTe common-mode
   continuation explicitly. Freeze branch values and mass roots before validation.
3. Determine the threshold channel selection, the intended spectral observable,
   and self-consistent linewidth
   before treating T' as a finite constant-A input or invoking endpoint pair
   curvatures. CdTe mid-gap mass evaluation is a cleaner control than its band edge.
4. Test local-background dependence and irreducible environment clusters only
   after the physical one-impurity problem; add no empirical bowing coefficients.

The existing binary-derived vertex is terminated as a candidate physical
predictor at this level. It is retained as a reproducible diagnostic and code test.
No manuscript, material validation, or replacement of Hansen is claimed.
