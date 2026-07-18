# Active research progress

**Last updated:** 2026-07-18  
**Controlling branch:** `agent/refresh-ledger-and-primary-evidence`  
**Purpose:** durable record of current conclusions, superseded claims, unresolved questions, and authorized next work.

This file is updated whenever an audit or calculation materially changes the research direction. Detailed derivations belong in dated decision records; this file states the controlling project position.

## Current controlling conclusions

### Static CdTe linear Hamiltonian

- The complete time-reversal-symmetric zincblende linear invariant space in the fixed Novik `Gamma6 + Gamma8 + Gamma7` basis has dimension four.
- The former one-`P`/two-`P` comparison spans only the `Gamma6-Gamma8` and `Gamma6-Gamma7` sectors; the remaining allowed directions are `Gamma8-Gamma8` and `Gamma8-Gamma7` bulk-inversion-asymmetry sectors.
- The reduced two-`P` model leaves approximately `0.82018%` training and unused-`[110]` residual.
- The complete four-direction space closes the archived matrices near `2e-7`.
- The corrected selected-band reconstruction gives `P8 = 6.7722219515 eV A`, `P7 = 6.2018257202 eV A`, and `eta_P = 8.79288%`.
- These structures and comparable CdTe coefficients are prior art through DFT2kp. The repository result is an independent reproduction, not a new Hamiltonian claim.

### Static CdTe effective-Hamiltonian correction

- The former all-state overlap reconstruction approaches the bare projection `P_Gamma H(k) P_Gamma`, not an isospectral eight-band effective Hamiltonian.
- The scientific reconstruction is now `selected_band_polar`: polar/parallel transport of bands 31-38 into the fixed Novik Gamma basis.
- It reproduces the selected finite-`k` spectrum to approximately `3e-14 eV`; the superseded all-state construction misses it at quadratic order by up to approximately `0.648 meV` in the validated physical rerun.
- Coupled two-level tests prove that the selected-band construction recovers the exact low-energy second-order shift while the complete all-state construction returns the bare `P H P` block.
- The all-state path is retained only as a diagnostic.

### Static CdTe quadratic Hamiltonian and gauge boundary

- The complete `Td + time reversal` quadratic invariant space has dimension ten and corresponds to established Weiler/extended-Kane classes.
- A full ten-coefficient first-principles CdTe Hamiltonian was already published by DFT2kp; a broad novelty claim is not supportable.
- In the fixed-Gamma polar gauge, the complete ten-dimensional space closes near `1e-5` matrix residual.
- The conventional tied four-dimensional matrix model leaves `28.7044%` training and `33.2112%` unused-`[110]` residual.
- A separate basis-invariant fit to selected-band energy shifts also rejects the conventional model: `3.25891%` training and `4.40343%` `[110]` residual versus declared `1%/2%` gates.
- Five established departure directions (`G`, `G_prime`, `delta_gamma1`, `delta_gamma2`, `delta_gamma3`) reduce the worst training/holdout matrix residual to approximately `0.13246%`; `N2` is negligible at the one-percent gate.
- Individual Weiler coordinates and Frobenius matrix residuals are polar-gauge quantities. Eigenvalues and the spectral-closure rejection are basis invariant.
- The earlier approximately `49%` residual, large `N2`, all-six-required conclusion, and proposed 120-band run are superseded.

### Finite-temperature matrix methodology

- The deterministic matrix oracle validates the complete downstream path: `Td`-symmetric Gamma self-energy, positive-metric quasiparticle linearization, rational dynamical poles, extended-Kane parameter recovery, one-/two-`P` discrimination, and held-out thermal reduction.
- Matrix quasiparticle linearization and two-`P` recovery close essentially at machine precision.
- A synthetic one-scale thermal reduction is correctly rejected on held-out temperatures; this is a method-readiness result, not a material prediction.
- Long-range polar Fan restoration must occur at the **electron-phonon vertex** level. Adding source and target long-range self-energies separately omits the short-/long-range interference term.
- The synthetic vertex oracle closes the correct subtract/interpolate/restore path near machine precision. Naive vertex restoration is wrong by at least approximately `46%`, and omitting the Fan cross term creates at least approximately `34%` self-energy error.

### CdTe A0 physical-response result

- The initial CdTe A0 calculation is an execution pass and a physical-response sanity fail.
- The original point had `31.20 kbar` pressure, raw acoustic modes near `-183.63 cm^-1`, Born-charge sum `-0.51611 e`, and a `26.9853%` optical shift under simple ASR.
- One authorized same-geometry stricter diagnostic (`ecutrho = 570 Ry`, `tr2_ph = 1e-14`) was completed.
- The acoustic and ASR pathologies collapsed materially, but the Born-charge neutrality error worsened by approximately `2.43x`; numerical tightening therefore did not validate the response.
- No further numerical tightening is authorized.
- A zero-compute consistency audit found a plausible short-range TO frequency but an internally inconsistent long-range polar model: gap ratio approximately `0.325`, dielectric ratio approximately `8.84`, predicted-LO error approximately `7.07%`, and polar-strength ratio approximately `0.303` relative to the experimental anchor.
- The current point may inform short-range planning but cannot supply a validated macroscopic polar contribution.
- A1 remains unauthorized.

### Finite-temperature backend boundary

- No currently audited backend satisfies all project requirements simultaneously: spin-orbit coupling, matrix-resolved Fan and Debye-Waller terms, polar interpolation, controlled gauge transport, and an auditable eight-band export.
- QE has relevant matrix/Debye-Waller machinery but lacks a validated SOC route for this project.
- EPW supports SOC and polar interpolation but the standard self-energy route does not provide the required Debye-Waller matrix contribution.
- ABINIT's modern EPH path does not satisfy the SOC requirement.
- Special-displacement/ZG methods can include total thermal effects but require a validated supercell-to-primitive eight-band matrix reconstruction.
- A synthetic ZG reconstruction oracle now proves that overlap selection, polar gauge recovery, displacement pairing, configuration averaging, Gamma projection, and time-reversal restoration can recover a known primitive eight-band thermal matrix despite remote leakage and degenerate rotations.
- The ZG route is method-feasible, not yet a physical HgCdTe result. Real-export feasibility, finite-size convergence, and polar restoration remain open.

### Provisional HgCdTe temperature law

The leading provisional analytical model is

```text
Eg_eV(x,T) = -0.302 + 1.93*x - 0.81*x^2 + 0.832*x^3
             + alpha*(1-2*x)*T^3/(T^2 + tau^2)
```

with

```text
alpha = 5.918273117836612e-4 eV/K
tau   = 18.059294367159467 K
```

- Held-out temperature-shape RMSE is `0.81258 meV`, compared with `1.82388 meV` for Hansen, `1.06113 meV` for published Seiler, and `0.78622 meV` for a freely trained Seiler family.
- On the independently composed sample-3 absolute temperature series, RMSE is `1.03976 meV`, compared with `1.84640 meV` for Hansen and `1.40383 meV` for published Seiler.
- The model is a constrained zero-anchored member of Seiler's rational family, not a new functional family.
- It is implemented as `provisional_hansen_pade_gap_ev`; it is not a production equation.

### Static-composition and cross-source boundary

- The secondary Chu-attributed room-temperature table and the independently composed Seiler low-temperature samples are mutually inconsistent under every audited universal static correction.
- On the Chu screen, RMSE is `16.2664 meV` for Hansen, `3.2568 meV` for Chu 1983, `11.6940 meV` for Laurenti, and `11.9911 meV` for the provisional model.
- On independent Seiler samples 3-5, RMSE is `3.8867 meV` for Hansen, `15.9735 meV` for Chu 1983, `11.7503 meV` for Laurenti, and `4.1762 meV` for the provisional model.
- Minimal Chu-fitted static corrections reduce Chu held-out error to approximately `2.8-3.1 meV` but degrade Seiler transfer to approximately `6.7-7.3 meV`.
- An affine composition remapping fits the Chu table with `0.001596` RMS composition residual and `2.149 meV` gap RMSE, but transfers to Seiler at `8.848 meV` RMSE.
- No replacement for Hansen's zero-temperature polynomial is authorized.

### Gap observation-operator boundary

- The Chu absorption-fit gaps lie predominantly above the provisional latent-gap prediction: mean signed residual `+9.0392 meV`, RMSE `11.9911 meV`, and seven positive residuals out of eight.
- A constant source offset is insufficient; centered RMSE remains `7.8791 meV`.
- The Hg-vacancy edge mechanism is rejected for this discrepancy by sign because it lowers the apparent absorption edge.
- Reported extraction-method scatter near `2 meV` is too small.
- Burstein-Moss filling has the correct sign but is unidentifiable without carrier density and carrier type.
- Composition and the secondary table's absorption-threshold variable are severely confounded (`VIF = 33.14`).
- No production observation operator is identified. Measurement-class metadata must remain explicit.

### Minimum evidence required to continue equation development

- The current absorption-only evidence has rank `2/5` for a local audit model separating latent gap intercept, latent composition slope, absorption offset, carrier filling, and vacancy contribution.
- Paired absorption and magneto-optical gaps alone reach rank `3/5`; adding Hall or a vacancy proxy alone reaches `4/5`.
- Three paired specimens with independent composition, carrier, and vacancy contrasts are the algebraic full-rank minimum, but have only one residual degree of freedom and maximum leverage `1.0`.
- Within the declared two-level `2 x 2 x 2` candidate family, exhaustive evaluation of all 219 subsets proves that the complete eight-specimen factorial is the unique audit-grade design under the declared thresholds.
- Per temperature block the recommended design has 16 paired observations, 11 residual degrees of freedom, condition number `2.61803`, and maximum leverage `0.4375`.
- Repeat at a low-temperature block and at `300 K`, for 32 paired gap observations.
- Independent composition uncertainty should be near `sigma_x = 1e-3` or better to keep composition-induced gap uncertainty near or below `2 meV`.

### Other methodological caveats

- Matrix uncertainty storage still uses a redundant 128-real-component representation for an `8x8` Hermitian matrix. Statistical covariance must move to the 64 independent real Hermitian coordinates before chi-square, parameter-standard-error, or likelihood claims are made.
- The Seiler held-out shape analysis profiles one additive offset per specimen. It tests conditional temperature-shape transfer, not strict absolute prediction except where explicitly stated.

## Current novelty boundary

Not novel:

- standard first-principles symmetry-adapted `k.p` extraction;
- complete zincblende linear and quadratic invariant construction;
- four-linear and ten-quadratic CdTe extended-Kane coefficients;
- generic nonlinear HgCdTe temperature laws;
- Seiler-family rational temperature dependence;
- standard polar subtract/interpolate/restore methodology;
- special-displacement thermal averaging;
- the synthetic validation or acquisition-design tools themselves.

Potentially useful and narrower:

- independently quantified matrix-level and spectral errors of reduced Kane models;
- the stable zero-anchored two-parameter Seiler-family reparameterization with specimen-level transfer evidence;
- a full-matrix finite-temperature HgCdTe self-energy in an auditable fixed gauge, if real data or first-principles output validates held-out observables;
- evidence that thermal corrections require distinct `P8(T)` and `P7(T)` or generate established extended-Weiler channels beyond scalar edge shifts;
- a paired multimodal specimen dataset that separates latent material law from measurement-class, carrier-filling, and defect effects.

## Authorized next work

1. Recover primary point-level HgCdTe `x-Eg-T` evidence with explicit composition method, measurement definition, and uncertainty. Priority sources are Chu-Mi-Tang 1991/1992, Scott 1969, Schmit-Stelzer 1969, and the source studies underlying Hansen 1982.
2. Treat formulas and abstracts as historical comparators only. Do not promote them to point-level validation evidence.
3. Reopen static-law fitting only if a primary point table or a genuinely independent specimen-level dataset passes provenance gates.
4. Preserve the provisional Hansen-Pade thermal law without adding parameters.
5. Correct matrix covariance from redundant 128D storage to the 64 independent Hermitian coordinates.
6. Keep the ZG matrix route at method-readiness status until a real export contract, finite-size test, and polar-restoration plan are validated.

## Explicitly unauthorized

- additional empirical gap coefficients from the current Seiler and secondary Chu data;
- treating the secondary Chu table as primary fit authority;
- a universal source offset, composition remapping, Burstein-Moss correction, or vacancy correction from the current metadata;
- executing A1 from the failed CdTe long-range response state;
- further response-threshold tightening or an uncontrolled convergence ladder;
- using current CdTe dielectric, Born-charge, or long-range phonon values as validated predictions;
- a 120-band static Kane run for the all-state reconstruction;
- broad claims of a new CdTe extended-Kane Hamiltonian or a universal new HgCdTe bandgap equation;
- production ZG/AHC work before the remaining real-export and polar gates are satisfied.
