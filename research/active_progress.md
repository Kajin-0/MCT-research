# Active research progress

**Last updated:** 2026-07-18  
**Controlling branch:** `agent/hermitian-covariance-schema`

Detailed derivations and exact artifacts are preserved in dated decision records and `validation/*_reference_result.json`. This file states the controlling program position.

## Static CdTe Hamiltonian

- The complete zincblende linear invariant space has four directions. The reduced two-`P` model leaves approximately `0.82018%` residual; all four directions close near `2e-7`.
- Corrected selected-band values are `P8 = 6.7722219515 eV A` and `P7 = 6.2018257202 eV A`.
- The former all-state reconstruction converges to bare `P H P`, not an isospectral eight-band effective Hamiltonian. `selected_band_polar` is now the scientific default and reproduces selected finite-`k` eigenvalues near `3e-14 eV`.
- The complete quadratic invariant space has ten established Weiler directions. The conventional tied model leaves `28.7044%` training and `33.2112%` unused-`[110]` matrix residual; an independent spectral fit also rejects it.
- Five established departure directions reduce worst residual to approximately `0.13246%`; `N2` is negligible. The old `49%`, large-`N2`, all-six-required, and 120-band conclusions are superseded.

## Finite-temperature and A0 boundary

- Synthetic matrix, dynamical-pole, two-`P`, Fan-vertex, and special-displacement reconstruction oracles pass.
- Long-range Fan restoration must occur at the vertex level so the short-/long-range interference term is retained.
- The first CdTe A0 point is an execution pass and physical-response fail. One stricter response point improved acoustic/ASR behavior but worsened Born-charge neutrality by approximately `2.43x`.
- The short-range TO response is plausible; the long-range polar model is internally inconsistent. Further threshold tightening and A1 execution are unauthorized.
- No audited backend yet supplies SOC, matrix Fan and Debye-Waller terms, polar interpolation, controlled gauge transport, and auditable eight-band export simultaneously.

## Provisional HgCdTe temperature law

```text
Eg_eV(x,T) = -0.302 + 1.93*x - 0.81*x^2 + 0.832*x^3
             + alpha*(1-2*x)*T^3/(T^2 + tau^2)
alpha = 5.918273117836612e-4 eV/K
tau   = 18.059294367159467 K
```

- Held-out temperature-shape RMSE is `0.81258 meV`, versus `1.82388 meV` for Hansen and `1.06113 meV` for published Seiler.
- Independent sample-3 absolute-series RMSE is `1.03976 meV`, versus `1.84640 meV` for Hansen.
- This is a constrained Seiler-family parameterization, not a new functional family or production equation.

## Static composition and observation boundary

- Secondary Chu room-temperature points and independent Seiler low-temperature specimens cannot be reconciled by a universal static correction or composition remapping.
- No replacement for Hansen's zero-temperature polynomial is authorized.
- Chu absorption-fit gaps lie mainly above the provisional latent-gap prediction: mean `+9.0392 meV`, RMSE `11.9911 meV`.
- Hg-vacancy bias is rejected by sign; reported extraction scatter is too small; Burstein-Moss filling is plausible but unidentifiable without carrier data.
- The current absorption-only evidence has rank `2/5`. Within the declared two-level family, the complete eight-specimen `2 x 2 x 2` paired design is the unique audit-grade design among all 219 tested subsets.

## Primary-source recovery

- Historical ledger: `0` fully authorized primary fit sources, `1` conditional source, `6` blocked primary sources, and `1` screen-only secondary table.
- Highest-priority historical target remains Chu-Mi-Tang 1992, DOI `10.1063/1.350867`.
- Abstracts and published formulas are model comparators, not point-level evidence.

## Modern primary absorption evidence

- Chang 2006 and Moazzami 2005 provide primary absorption methodology and figure-level spectra.
- Chang reports a nominal `x=0.21`, approximately `80 K` absorption curve with n-type carrier metadata, but no machine-readable points, point uncertainty, or independent composition method is recovered.
- Moazzami reports twelve MBE samples over `x=0.22-0.60`, FTIR at `40-300 K`, and same-specimen FTIR/ellipsometry agreement. Its final absorption model explicitly inserts Hansen `Eg(x,T)` and therefore cannot independently validate the material gap.
- Yue 2019 is mechanism-review evidence for defect-, Fermi-level-, conductivity-, and temperature-dependent optical shifts.
- Classification: `0` observation-authorized, `2` observation-conditional, `2` blocked, `1` review-only, and `0` static-gap-authorized sources.
- Seven figures are registered for possible digitization; none is authorized until exact primary page images and axis-calibration records are archived.

## Absorption observation-model benchmark

- The exact Moazzami fractional-power family recovers its generating edge within approximately `0.00375 meV`, so the deterministic fit itself does not create multi-meV bias.
- Forcing a linear exponent produces scenario-dependent shifts from approximately `-0.56` to `-8.10 meV`.
- A free power law fitted to a source-inspired Urbach/nonparabolic reference still shifts the inferred edge by approximately `-11.36` to `-15.95 meV`.
- Defining the edge at `alpha=1500 cm^-1` produces positive nominal biases of `9.21-16.77 meV`, overlapping the sign and scale of the existing `+9.04 meV` Chu/provisional mean discrepancy.
- Changing only the threshold from `600` to `2000 cm^-1` spans `18.62-29.33 meV` across the nominal scenarios.
- Across 36 Urbach/amplitude sensitivity cases, the median threshold bias is `4.61 meV` at `1000 cm^-1`, `13.06 meV` at `1500 cm^-1`, and `24.75 meV` at `2000 cm^-1`.
- This establishes synthetic scale compatibility, not a diagnosis or universal correction.

## Hermitian matrix covariance schema

- Hermitian `8 x 8` matrices now use 64 independent real coordinates instead of redundant 128D real/imaginary storage.
- `hvec` uses `sqrt(2)`-scaled upper-triangle coordinates and exactly preserves the Frobenius inner product.
- Matrix dataset schema `2.0` stores `64 x 64` covariance under `hermitian_frobenius_64`.
- Schema `1.0` archives remain readable through an explicit `128D -> Hermitize -> 64D` migration recorded in provenance; new exports reject 128D covariance.
- Unitary gauge rotation induces an orthogonal 64D map, so covariance trace is preserved without duplicated entries.
- GLS observation count and residual degrees of freedom now use 64 coordinates per matrix. Statistical claims from the old redundant covariance representation are superseded.
- Covariance on a general non-Hermitian self-energy remains unsupported and fail-closed; gauge uncertainty is not yet propagated.

## Controlling decision

- **Observation-model research is authorized.**
- **Measurement definition can generate multi-meV inferred-edge bias.**
- **Production observation correction is not authorized.**
- **Static material-gap refitting remains unauthorized.**
- Every absorption-derived gap must preserve model, fit window, threshold, carrier state, tail treatment, and an edge-model uncertainty envelope.
- Hermitian matrix statistical analysis must use the schema-2 independent 64D coordinates.

## Authorized next work

1. Convert the validated observation benchmark into a reusable uncertainty-envelope/export contract without promoting a universal correction.
2. Continue primary point-data recovery, including the composition/growth sources underlying Moazzami 2005.
3. Archive exact source page images and calibration before figure digitization.
4. Preserve the provisional thermal law without adding parameters.
5. Keep the ZG route at method-readiness status until real-export, finite-size, and polar gates pass.
6. Estimate physical 64D covariance only from declared convergence ensembles; do not invent gauge uncertainty.

## Explicitly unauthorized

- additional empirical gap coefficients from current data or uncalibrated figures;
- treating abstracts, formulas, secondary tables, or webpage previews as point-level fit authority;
- universal source, composition, Burstein-Moss, vacancy, threshold, or model-family corrections from current metadata;
- production absorption correction without machine-readable common-specimen evidence;
- covariance-based physical confidence claims from synthetic diagonal matrices or legacy redundant 128D coordinates;
- A1 execution, further response-threshold tightening, 120-band static reruns, or broad novelty claims unsupported by the recorded evidence.
