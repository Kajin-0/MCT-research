# Analytical identifiability and minimum-information gap prediction

Date: 2026-10-11. Portfolio contribution R07. Related infrastructure: issue #4.
Scope: static, zero-temperature microscopic Γ6/Γ8 theory. No empirical alloy
gap inputs, new DFT runs, numerical queues, or manuscript authorization.

**Decision: continue analytical development; do not promote an endpoint-only
or two-constant law to a physical prediction.** A specified finite local
Hamiltonian and probability law define a predictive problem. Binary operators,
symmetry, and finitely many endpoint derivatives do not identify that Hamiltonian
or its interior averaged spectrum in the unrestricted model class.

This is an information limitation, not a proof that an atomic first-principles
Hamiltonian cannot predict an alloy. Specifying the complete microscopic
configuration-to-operator map and its probability law determines the resolvent
uniquely whenever the required limits exist. Assuming unknown mixed interactions
are composition independent does not supply their values.

The useful reduction is exact: with ensemble Td symmetry and one retained copy
of each double-group representation, the Γ response consists of **two scalar
causal functions**, not an arbitrary six-by-six matrix. These functions can be
represented by two positive Feshbach spectral measures. Symmetry does not fix
their energy or composition dependence. This is established representation and
augmented-space mathematics; no priority is claimed.

The package adds four substantive constraints to the existing program:

1. Fixed, composition-independent local interactions can conceal a mixed
   configuration from arbitrarily many endpoint derivatives. An exact random
   atomic Hamiltonian demonstrates this for the entire averaged resolvent.
2. The previously established coherent-invisible directional Te tensor changes
   the **Γ8 self-energy**, rather than merely an unrelated covariance. Under an
   additional isotropic atomic propagator assumption its chemical/SOC response
   contracts to two quadratic invariants. This is a conditional reduction, not
   a statement that real finite-q HgCdTe has only two scattering amplitudes.
3. Even positive spectral measures with the same total weight, static value,
   and first energy derivative can predict different mass-zero compositions.
   Two susceptibilities require additional closure assumptions.
4. A certified distance to the eliminated spectrum supplies an explicit
   nonperturbative error bound for energy linearization. Combined with a common
   energy and mass-slope bound, it specifies the precision needed for x_c.

An additional observable restriction is important: for a bounded finite-range
Bernoulli Hamiltonian with fixed interactions and full configuration support,
the almost-sure **spectral-support set** is independent of x for 0<x<1. Its
weights, Γ peaks, and localization properties can change. Therefore a smoothly
composition-dependent reported band edge cannot automatically be identified
with that support edge. This support phenomenon is established random-operator
physics, not a new HgCdTe discovery.

## Package

| Artifact | Purpose |
|---|---|
| [foundation.md](foundation.md) | Exact sector reduction, augmented-space Feshbach representation, observable definitions, root and error equations |
| [identifiability.md](identifiability.md) | Proofs, physical Hamiltonian counterexamples, covariance quotient, spectral-moment ambiguity, sufficient-input statements |
| [closures.md](closures.md) | Three competing closures, convergence gates, limits, bounds and falsification |
| [inputs_and_decision.md](inputs_and_decision.md) | Ranked input matrix, precision budget, conditional expensive-input justifications and decision |
| [discovery_registry.md](discovery_registry.md) | Scientific status of every principal claim and preserved negative results |
| [literature.md](literature.md) | Bounded primary-literature audit and novelty boundary |
| [verification.md](verification.md) | Independent mathematical checks and reproducibility |

## Scientific continuity

This package supplements the earlier [program state](../state.md). It does not
replace the archived derivations or promote their numerical controls to material
validation. In particular, it retains:

| Existing result | Consequence retained here |
|---|---|
| [Host-invariant reaction kernel](../../../../docs/derivations/host_invariant_reaction_kernel.md) | Fixed physical projectors; distinguish K_P from full finite-box T; thermodynamic/continuation limits remain necessary |
| [Full/residual T and thresholds](../../../../docs/derivations/impurity_reference_and_threshold.md) | Subtract the coherent contrast once; embedded g' is not -g²; finite T does not imply finite T' |
| [Volume path](../../../../docs/derivations/endpoint_volume_path.md) | Fixed-ion impurity response and homogeneous strain are separate inputs |
| [Continuum prescription](../../../../docs/derivations/continuum_prescription_and_crossing.md) | Retarded Hermitian part and principal-value reactance differ; real and complex crossings differ |
| [Threshold self-consistency](../../../../docs/derivations/self_consistent_threshold_and_centroid.md) | Isolated-host x^(3/2) and CPA x² are approximation-specific; the cluster indicator is order one at the CPA edge |
| [Oriented Te response](../../../../docs/derivations/oriented_tetrahedral_response.md) | Coherent derivatives determine order averages, not full directional covariance |
| [SOC tensor classification](../../../../docs/derivations/te_p_soc_tensor_tomography.md) | Fourteen endpoint-invisible p-onsite coefficients under its stated assumptions; no assigned material coefficients |
| [Numerical result ledger](../result_2026-10-11.md) | Exchange quadrature, physical-frame, orbital-projection and incomplete-window artifacts remain disqualifying where their gates failed |
| [Bare-vertex rejection](../result_2026-10-10_self_consistency.md) | Exact T and direct alloy spectra did not repair the archived binary-derived substitution model |

Existing detached calculations retain their established supervision and stopping
rules. This analytical tranche neither launches work nor modifies their state.
Temperature stays deferred. No new physical gap or x_c is reported.
