# Active research progress

**Last updated:** 2026-07-19  
**Controlling branch:** `agent/integrate-orlita2014-constraint`

Detailed results live in `research/decision_records/` and `validation/*_reference_result.json`.

## Controlling scientific state

- Static CdTe extraction uses the isospectral selected-band polar Hamiltonian. The complete linear space has four directions; the complete quadratic space has ten established Weiler directions.
- The conventional tied quadratic model fails matrix and spectral closure. Five established departure directions are sufficient at the declared gate; `N2` is negligible. The former `49%`, large-`N2`, all-six-required, 120-band interpretation is superseded.
- The CdTe A0 point remains invalid for long-range polar response. Further threshold tightening and A1 execution are unauthorized.
- Finite-temperature matrix, Fan-vertex, and special-displacement reconstruction methods pass synthetic oracles, but no audited backend yet closes all SOC, Debye-Waller, polar, gauge, and export requirements.

## Matrix covariance and regenerated statistics

- Hermitian `8x8` Hamiltonians use 64 orthonormal real coordinates; general complex dynamical operators retain 128.
- Dataset schema `2.0` stores covariance dimension `0`, `64`, or `128`; schema `1.0` remains readable through explicit migration.
- Old-versus-new regeneration confirms fitted parameters and Frobenius SSE are unchanged to numerical precision.
- For six matrices and eight parameters, residual degrees of freedom change from `760` to `376`; variance-scaled standard errors increase by `1.4217160742`.
- No committed physical static record contains calibrated Hamiltonian covariance statistics requiring numerical replacement.

## HgCdTe gap program

The leading provisional temperature law remains:

```text
Eg(x,T) = Eg_Hansen(x,0) + 5.918273117836612e-4
          * (1-2*x) * T^3 / (T^2 + 18.059294367159467^2)
```

It is a constrained Seiler-family parameterization, not a new functional family or production equation.

- No replacement for Hansen's zero-temperature composition polynomial is authorized.
- No production absorption-edge correction is authorized.
- The complete paired eight-specimen `2 x 2 x 2` design remains the audit-grade acquisition target.

## Primary evidence state

The centralized recovery ledger now contains:

```text
all sources                         9
primary sources                     8
authorized primary fit sources      0
conditional primary sources         2
blocked primary sources             6
screen-only sources                 1
```

Conditional primary sources are Seiler 1990 and Orlita 2014.

Orlita 2014 adds a carrier-coupled near-critical constraint at approximately `1.8 K`: a graded plateau near `x approximately 0.17`, a low-field model improved by `Eg=4 meV`, `EF approximately 15-17 meV`, and `n approximately (2-3)e14 cm^-3`.

At nominal `x=0.17`, Laurenti is the closest local comparator, but the model-equivalent composition offsets span from `+0.000573` to `-0.006608`. The source is therefore composition-sensitive, carrier-coupled and not an exact homogeneous calibration point.

Orlita and Teppe share the Mikhailov/Dvoretskii MBE and magneto-optical lineage. They are not independent cross-laboratory validation sets.

The static-law reopening gate remains closed because Orlita lacks point uncertainty and homogeneous independent composition uncertainty, and no two independent primary sources satisfy all evidence requirements.

## Absorption edge uncertainty contract

- Every absorption-derived edge record must explicitly preserve source calibration, modality, temperature, thickness, composition provenance, carrier state, tail treatment, fit window, search bounds, model exponents, thresholds, and the raw spectrum.
- The validated exporter returns all declared model and threshold candidates, exclusions, separate model/threshold envelopes, a combined envelope, and the SHA-256 of the full input assumptions.
- It never selects a recommended or corrected material gap.
- Deterministic example: seven candidates span `19.95223 meV`; model-family span is `9.14375 meV`, threshold span is `9.95726 meV`, and the half-range is `9.97612 meV`.
- Research uncertainty export is authorized. Production correction and single-edge selection remain forbidden.

## Authorized next work

1. Continue primary point-data recovery and archive calibrated source figures before digitization.
2. Obtain homogeneous composition and carrier-aware uncertainty for near-critical primary specimens.
3. Apply the uncertainty contract only to native digital or calibrated spectra with complete metadata.
4. Preserve the provisional thermal law without adding parameters.
5. Keep the ZG route at method-readiness status until real-export, finite-size, and polar gates pass.

## Explicitly unauthorized

- treating Orlita as an exact homogeneous point or independent cross-laboratory validation;
- treating old redundant Hamiltonian degrees of freedom or variance-scaled standard errors as current;
- additional empirical gap coefficients from current or uncalibrated data;
- universal source, composition, carrier, defect, threshold, or model-family corrections from current metadata;
- single-edge selection from the uncertainty ensemble;
- A1 execution, further response-threshold tightening, 120-band static reruns, or unsupported novelty claims.
