# Active research progress

**Last updated:** 2026-07-18  
**Controlling branch:** `agent/recover-modern-primary-absorption-evidence`

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

## Controlling decision

- **Observation-model research is authorized.**
- **Production observation correction is not authorized.**
- **Static material-gap refitting remains unauthorized.**
- Measurement classes must remain explicit.

## Authorized next work

1. Build a formula-level absorption benchmark covering Urbach/nonparabolic behavior, the Moazzami fractional-power law, measurement-method transfer, and edge sensitivity to tails, filling, thickness, and thresholds.
2. Continue primary point-data recovery, including the composition/growth sources underlying Moazzami 2005.
3. Archive exact source page images and calibration before figure digitization.
4. Preserve the provisional thermal law without adding parameters.
5. Correct matrix covariance from redundant 128D storage to 64 independent Hermitian coordinates.
6. Keep the ZG route at method-readiness status until real-export, finite-size, and polar gates pass.

## Explicitly unauthorized

- additional empirical gap coefficients from current data or uncalibrated figures;
- treating abstracts, formulas, secondary tables, or webpage previews as point-level fit authority;
- universal source, composition, Burstein-Moss, or vacancy corrections from current metadata;
- production absorption correction without machine-readable common-specimen evidence;
- A1 execution, further response-threshold tightening, 120-band static reruns, or broad novelty claims unsupported by the recorded evidence.
