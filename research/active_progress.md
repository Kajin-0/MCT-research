# Active research progress

**Last updated:** 2026-07-18  
**Controlling branch:** `agent/record-static-kane-audit`  
**Purpose:** durable record of current conclusions, superseded claims, unresolved questions, and authorized next work.

This file is updated whenever an audit or calculation materially changes the research direction. Detailed derivations belong in dated decision records; this file states the controlling project position.

## Current controlling conclusions

### Static CdTe linear Hamiltonian

- The complete time-reversal-symmetric zincblende linear invariant space in the fixed Novik `Gamma6 + Gamma8 + Gamma7` basis has dimension four.
- The repository's former one-`P`/two-`P` comparison spans only the `Gamma6-Gamma8` and `Gamma6-Gamma7` sectors.
- The remaining two allowed linear directions are the `Gamma8-Gamma8` and `Gamma8-Gamma7` bulk-inversion-asymmetry sectors.
- The reduced two-`P` model leaves a relative matrix residual of approximately `0.82018%`.
- The complete four-direction linear space closes the archived finite-k matrices at approximately `2e-7`, including the unused `[110]` direction.
- The extracted dominant couplings remain approximately `P8 = 6.7722 eV A` and `P7 = 6.2018 eV A` and agree with the independently published DFT2kp CdTe result at roughly the one-percent level.
- The four-direction structure and CdTe coefficients are prior art through DFT2kp. The repository result is an independent cross-method reproduction, not a new Hamiltonian claim.

### Static CdTe quadratic Hamiltonian

- The complete `Td + time reversal` quadratic invariant space has dimension ten and corresponds to the established Weiler/extended-Kane classes.
- A full ten-coefficient first-principles CdTe Hamiltonian was already published by DFT2kp. Broad claims of a new complete quadratic CdTe model are not supportable.
- The repository's current all-state overlap reconstruction converges to the bare projection `P_Gamma H(k) P_Gamma`, not to an isospectral eight-band effective Hamiltonian.
- The all-state construction misses the selected DFT eigenvalues by approximately `0.55-1.03 meV` at `|k| = 0.01 A^-1`; the discrepancy scales as `k^2` and therefore contaminates the quadratic coefficients directly.
- The scientifically appropriate finite-k object is the selected-eight-band polar/parallel-transport Hamiltonian, which is exactly isospectral to bands 31-38 at every sampled k point.
- Under this corrected reconstruction, the conventional tied four-dimensional quadratic model leaves approximately `28.7%` training error and `33.2%` `[110]` holdout error.
- Five established departure directions reduce the worst residual to approximately `0.20%`; the `N2` direction is negligible.
- The earlier approximately `49%` residual, large `N2`, and statement that all six departure directions are required are superseded.
- A proposed 120-band convergence run is cancelled because increasing the state count in the current formula would converge the wrong mathematical object more accurately.

### Methodological caveats still open

- The selected-band polar Hamiltonian is isospectral, but matrix coefficients can change under smooth k-dependent unitary transformations inside the selected manifold. The controlling next conceptual audit is to separate gauge-invariant conclusions from parallel-transport-gauge-dependent coefficient values.
- Matrix uncertainty storage currently uses a redundant 128-real-component representation for an 8x8 Hermitian matrix. Statistical covariance should move to the 64 independent real Hermitian degrees of freedom before chi-square, parameter standard-error, or likelihood claims are made.
- The Seiler held-out analysis profiles one additive offset per held-out specimen. It tests conditional temperature-shape transfer, not strict absolute gap prediction.

### CdTe A0 phonon/electronic first point

- PR #98 is a successful execution and provenance record, not a physical-validation pass.
- The SCF point has approximately `3.12 GPa` hydrostatic pressure at the fixed experimental volume.
- The raw Gamma acoustic triplet is strongly negative, the Born-charge sum violates the acoustic sum rule, and the optical frequency changes by approximately `27%` after simple ASR.
- These response quantities are not authorized as physical CdTe reference values.
- The A0 response workstream remains separate from the static Kane-method correction.

## Current novelty boundary

Not novel:

- first-principles symmetry-adapted k.p extraction;
- unitary alignment of degenerate DFT subspaces;
- complete zincblende linear and quadratic invariant construction;
- four linear and ten quadratic CdTe extended-Kane coefficients;
- scalar HgCdTe electron-phonon gap and mass renormalization;
- nonlinear composition-dependent HgCdTe temperature laws.

Potentially useful and narrower:

- independent finite-k reproduction of published CdTe linear couplings;
- explicit matrix-level quantification of errors caused by reduced two-`P` and tied quadratic models;
- comparison of reduced-model failure across independently extracted Hamiltonians;
- observable consequences of omitted symmetry-allowed terms;
- a rigorously defined finite-temperature full-matrix HgCdTe self-energy projected into a fixed, auditable gauge, provided it improves held-out observables beyond established models.

## Authorized next work

1. Replace the all-state bare-projection path with an explicit selected-band polar reconstruction as the scientific default.
2. Add a deterministic isospectrality gate and a coupled two-level test that distinguishes `P H P` from a valid effective Hamiltonian.
3. Recompute and commit the corrected four-dimensional linear result, ten-dimensional quadratic result, Weiler coordinates, model-reduction frontier, and observable consequences.
4. Complete the gauge-dependence audit before treating individual quadratic coordinates as unique material parameters.
5. Add DFT2kp, Jocić-Vukmirović, and VASP2KP to the prior-art matrix and map the published CdTe coefficients into repository conventions.
6. Correct the matrix covariance schema from redundant 128D storage to the 64 independent Hermitian coordinates.
7. Record the PR #98 A0 point as execution pass / physical-response sanity fail before any second response calculation.

## Explicitly unauthorized

- a 120-band static Kane run under the current all-state reconstruction;
- broad claims of a new CdTe extended-Kane Hamiltonian;
- generalization that all six quadratic departure directions are required;
- use of the PR #98 phonon, dielectric, or Born-charge values as validated physical predictions;
- HgTe, alloy, AHC, or dense electron-phonon work before the controlling method corrections are merged.
