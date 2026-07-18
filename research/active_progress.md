# Active research progress

**Last updated:** 2026-07-18  
**Controlling branch:** `agent/gate-real-a1-input` / PR #103  
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

### Finite-temperature matrix pipeline

- PR #102 implements a deterministic synthetic oracle for the complete downstream finite-temperature Kane pipeline before any A1 electron-phonon calculation.
- The oracle validates the most general `Td`-symmetric Gamma self-energy, positive-metric quasiparticle linearization, exact rational dynamical poles, extended-Kane parameter recovery, one-/two-`P` discrimination, and held-out thermal reduction.
- Matrix quasiparticle linearization recovers the known target with maximum relative error `1.3751e-16`.
- Rational dynamical self-energy linearization agrees with exact quasiparticle roots within `5.6064e-9 eV`.
- All nine extended-Kane parameters are recovered with maximum absolute error `1.1462e-11`; the maximum two-`P` matrix residual is `4.2649e-16`.
- The nested one-`P` model is correctly rejected with minimum matrix residual `2.2660e-4`.
- A synthetic signed two-scale gap trajectory has a resolved maximum at `100 K`.
- A one-scale reduction misses held-out temperatures by as much as `2.2908 meV`.
- The correct two-scale model recovers held-out points within `8.24e-14 meV` and improves by `22.91` declared numerical standard uncertainties.
- The matrix pipeline is ready to accept real first-principles inputs. This is a method-readiness result, not a material result.
- The controlling record is `first_principles/matrix_oracle/finite_temperature_kane_oracle_reference_result.json`.

### CdTe A0 physical audit

- PR #98 is an execution pass and a physical-response sanity fail.
- Immutable audit replay confirms:
  - SCF accuracy `4.5e-9 Ry` and direct Gamma gap `0.4973 eV` pass;
  - hydrostatic pressure is `31.20 kbar` and fails the unqualified fixed-volume interpretation gate;
  - raw acoustic modes are `-183.63 cm^-1` and fail translational invariance;
  - Born-charge sum is `-0.51611 e` and fails neutrality;
  - the optical triplet shifts from `223.27` to `283.52 cm^-1` after simple ASR, a `26.9853%` change;
  - dielectric eigenvalues are isotropic and positive at `62.326671426`.
- Response numerical sanity and fixed-volume physical interpretation both fail.
- A1 remains explicitly unauthorized.
- The controlling record is `first_principles/a0/cdte_a0_first_point_audit_reference_result.json`.
- Exactly one next diagnostic is authorized: the same geometry with `ecutrho = 570 Ry` and `tr2_ph = 1e-14`, retaining `ecutwfc = 114 Ry`, `4x4x4`, `nbnd = 40`, and SCF `conv_thr = 1e-8 Ry`.
- No volume, functional, pseudopotential, q-grid, HgTe, alloy, or A1 escalation is authorized until that response diagnostic is audited.

### Minimum real A1 matrix export

- PR #103 defines the smallest real export accepted by the validated matrix pipeline.
- The export uses six temperatures and seven k points: `Gamma`, `+/-[001]`, `+/-[111]`, and unused `+/-[110]` holdout.
- Every record must contain separately provenanced real Fan, Fan damping, real Debye-Waller, Fan derivative, and total self-energy matrices in the exact Novik selected-band polar gauge.
- The gate enforces complete provenance, Fan plus Debye-Waller closure, Hermitian components, causal nonpositive damping, positive quasiparticle metric, Gamma `Td` covariance, time reversal, and mode-resolved Gamma frequency-bin gap identities.
- A structurally valid export remains rejected whenever the A0 audit does not authorize A1.

### Other methodological caveats

- Matrix uncertainty storage still uses a redundant 128-real-component representation for an `8x8` Hermitian matrix. Statistical covariance must move to the 64 independent real Hermitian coordinates before chi-square, parameter-standard-error, or likelihood claims are made.
- The Seiler held-out analysis profiles one additive offset per held-out specimen. It tests conditional temperature-shape transfer, not strict absolute gap prediction.

## Current novelty boundary

Not novel:

- first-principles symmetry-adapted `k.p` extraction;
- unitary alignment of degenerate DFT subspaces;
- complete zincblende linear and quadratic invariant construction;
- four linear and ten quadratic CdTe extended-Kane coefficients;
- scalar HgCdTe electron-phonon gap and mass renormalization;
- nonlinear composition-dependent HgCdTe temperature laws;
- the synthetic finite-temperature matrix oracle;
- the executable A0/A1 gating schemas themselves.

Potentially useful and narrower:

- independent finite-k reproduction of published CdTe linear couplings;
- explicit matrix-level and spectral quantification of errors caused by reduced two-`P` and tied quadratic models;
- comparison of reduced-model failure across independently extracted Hamiltonians;
- observable consequences of omitted symmetry-allowed terms;
- a rigorously defined finite-temperature full-matrix HgCdTe self-energy projected into a fixed, auditable gauge, provided it improves held-out observables beyond established models;
- evidence that real finite-temperature corrections require separate `P8(T)` and `P7(T)` or generate established extended-Weiler channels not captured by scalar edge shifts.

## Authorized next work

1. Merge PR #103 after standard tests and immutable A0 audit replay pass.
2. Execute exactly one same-geometry stricter-response diagnostic at `ecutrho = 570 Ry`, `tr2_ph = 1e-14`.
3. Audit that artifact with the same physical gates and stop unless acoustic, Born-charge, and ASR violations collapse materially.
4. Correct matrix covariance from redundant 128D storage to the 64 independent Hermitian coordinates.
5. Acquire or construct an independent Hg-rich specimen-level benchmark suitable for held-out temperature/composition validation.

## Explicitly unauthorized

- execute A1 from the current failed A0 physical-response state;
- accept any real A1 matrix export while the A0 prerequisite is false;
- treat synthetic thermal amplitudes, moments, or turnover as CdTe/HgCdTe predictions;
- a 120-band static Kane run for the all-state reconstruction;
- additional static band-count work without a new falsifiable question;
- broad claims of a new CdTe extended-Kane Hamiltonian;
- generalization that all six quadratic departure directions are required at engineering-level accuracy;
- use of the PR #98 phonon, dielectric, or Born-charge values as validated physical predictions;
- volume ladder, functional change, pseudopotential change, HgTe, alloy, production AHC, or dense electron-phonon work before the one authorized response diagnostic is audited.
