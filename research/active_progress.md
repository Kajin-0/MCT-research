# Active research progress

**Last updated:** 2026-07-18  
**Controlling branch:** `agent/fix-static-effective-hamiltonian` / PR #101  
**Purpose:** durable record of current conclusions, superseded claims, unresolved questions, and authorized next work.

This file is updated whenever an audit or calculation materially changes the research direction. Detailed derivations belong in dated decision records; this file states the controlling project position.

## Current controlling conclusions

### Static CdTe linear Hamiltonian

- The complete time-reversal-symmetric zincblende linear invariant space in the fixed Novik `Gamma6 + Gamma8 + Gamma7` basis has dimension four.
- The repository's former one-`P`/two-`P` comparison spans only the `Gamma6-Gamma8` and `Gamma6-Gamma7` sectors.
- The remaining two allowed linear directions are the `Gamma8-Gamma8` and `Gamma8-Gamma7` bulk-inversion-asymmetry sectors.
- The reduced two-`P` model leaves `0.8201798%` training residual and `0.8201766%` unused `[110]` residual.
- The complete four-direction linear space closes the archived matrices at approximately `2e-7`.
- The corrected selected-band reconstruction gives `P8 = 6.7722219515 eV A`, `P7 = 6.2018257202 eV A`, and `eta_P = 8.79288%`.
- The dominant couplings agree with the independently published DFT2kp CdTe result at roughly the one-percent level.
- The four-direction structure and CdTe coefficients are prior art through DFT2kp. The repository result is an independent cross-method reproduction, not a new Hamiltonian claim.

### Static CdTe effective-Hamiltonian correction

- The former all-state overlap reconstruction approaches the bare projection `P_Gamma H(k) P_Gamma`, not an isospectral eight-band effective Hamiltonian.
- In the physical rerun, the all-state diagnostic misses the selected spectrum by a maximum of approximately `0.648 meV` and has an aggregate selected-eigenvalue residual of approximately `1.030 meV`.
- The scientific reconstruction is now `selected_band_polar`: polar/parallel transport of bands 31-38 into the fixed Novik Gamma basis.
- Its maximum selected-eigenvalue error is `3.38e-14 eV`, with minimum selected-overlap singular value `0.9998015324`.
- Coupled two-level tests prove that the selected-band construction recovers the exact low-energy second-order shift while the complete all-state construction returns the bare `P H P` block.
- Source eigenvector phases and rotations inside exactly degenerate selected eigenspaces do not change the polar result.
- A lightweight immutable-artifact replay workflow now validates post-processing without rebuilding Quantum ESPRESSO.

### Static CdTe quadratic Hamiltonian

- The complete `Td + time reversal` quadratic invariant space has dimension ten and corresponds to established Weiler/extended-Kane classes.
- A full ten-coefficient first-principles CdTe Hamiltonian was already published by DFT2kp. Broad claims of a new complete quadratic CdTe model are not supportable.
- In the fixed-Gamma polar gauge, the complete ten-dimensional space closes with `1.2548e-5` training residual and `7.9562e-6` `[110]` holdout residual.
- The conventional tied four-dimensional matrix model leaves `28.7044%` training residual and `33.2112%` `[110]` holdout residual.
- A separate basis-invariant fit to selected-band energy shifts also rejects the conventional quadratic model: `3.25891%` training residual and `4.40343%` `[110]` holdout residual, versus declared `1%/2%` gates.
- The exhaustive 64-subset frontier is result-driven rather than hard-coded:
  - three departures reach below `10%`;
  - four departures reach below `5%`;
  - five departures reach below `1%` and `0.5%`;
  - all six are required only below `0.1%` at this smoke point.
- The best five-direction model uses `G`, `G_prime`, `delta_gamma1`, `delta_gamma2`, and `delta_gamma3`; its worst training/holdout residual is `0.13246%`.
- `N2 = 0.0573008 eV A^2` in repository orthonormal normalization and is not required at the one-percent gate.
- The earlier approximately `49%` residual, large `N2`, all-six-below-10% conclusion, and proposed 120-band run are superseded.
- The controlling numerical record is `first_principles/a0/cdte_corrected_static_reference_result.json`.

### Gauge boundary

- Eigenvalues and the conventional spectral-closure result are invariant under unitary changes of basis within the selected manifold.
- Individual Weiler coordinates and Frobenius matrix residuals are representation-dependent under additional smooth `k`-dependent unitary transformations.
- The reported matrix values are therefore explicitly fixed-Gamma polar-gauge quantities, not gauge-free material constants.
- The former open gauge question is resolved sufficiently for model selection: the conventional model fails both the declared matrix-gauge test and an independent basis-invariant spectral test.

### Other methodological caveats

- Matrix uncertainty storage still uses a redundant 128-real-component representation for an `8x8` Hermitian matrix. Statistical covariance must move to the 64 independent real Hermitian coordinates before chi-square, parameter-standard-error, or likelihood claims are made.
- The Seiler held-out analysis profiles one additive offset per held-out specimen. It tests conditional temperature-shape transfer, not strict absolute gap prediction.

### CdTe A0 phonon/electronic first point

- PR #98 is a successful execution and provenance record, not a physical-validation pass.
- The SCF point has approximately `3.12 GPa` hydrostatic pressure at the fixed experimental volume.
- The raw Gamma acoustic triplet is strongly negative, the Born-charge sum violates the acoustic sum rule, and the optical frequency changes by approximately `27%` after simple ASR.
- These response quantities are not authorized as physical CdTe reference values.
- The A0 response workstream remains separate from the static Kane-method correction.

## Current novelty boundary

Not novel:

- first-principles symmetry-adapted `k.p` extraction;
- unitary alignment of degenerate DFT subspaces;
- complete zincblende linear and quadratic invariant construction;
- four linear and ten quadratic CdTe extended-Kane coefficients;
- scalar HgCdTe electron-phonon gap and mass renormalization;
- nonlinear composition-dependent HgCdTe temperature laws.

Potentially useful and narrower:

- independent finite-k reproduction of published CdTe linear couplings;
- explicit matrix-level and spectral quantification of errors caused by reduced two-`P` and tied quadratic models;
- comparison of reduced-model failure across independently extracted Hamiltonians;
- observable consequences of omitted symmetry-allowed terms;
- a rigorously defined finite-temperature full-matrix HgCdTe self-energy projected into a fixed, auditable gauge, provided it improves held-out observables beyond established models.

## Authorized next work

1. Merge PR #101 after the final test, physical, and immutable-replay checks pass.
2. Define the smallest falsifiable finite-temperature matrix-self-energy experiment using the corrected selected-band polar gauge.
3. Separate gauge-invariant finite-temperature observables from gauge-fixed matrix coefficients in the AHC design.
4. Correct matrix covariance from redundant 128D storage to the 64 independent Hermitian coordinates.
5. Acquire or construct an independent Hg-rich specimen-level benchmark suitable for held-out temperature/composition validation.
6. Record PR #98 as execution pass / physical-response sanity fail and authorize only the smallest diagnostic needed to distinguish volume stress from response-convergence failure.

## Explicitly unauthorized

- a 120-band static Kane run for the all-state reconstruction;
- additional static band-count work without a new falsifiable question;
- broad claims of a new CdTe extended-Kane Hamiltonian;
- generalization that all six quadratic departure directions are required at engineering-level accuracy;
- use of the PR #98 phonon, dielectric, or Born-charge values as validated physical predictions;
- HgTe, alloy, production AHC, or dense electron-phonon work before a bounded finite-temperature matrix experiment is specified and gated.
