# Active research progress

**Last updated:** 2026-07-19  
**Controlling branch:** `agent/export-absorption-edge-uncertainty`

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
- Historical primary fit-authority count remains zero; Seiler is conditional and the Chu-Sher table is screen-only.
- The complete paired eight-specimen `2 x 2 x 2` design remains the audit-grade acquisition target.

## Absorption edge uncertainty contract

- Every absorption-derived edge record must explicitly preserve source calibration, modality, temperature, thickness, composition provenance, carrier state, tail treatment, fit window, search bounds, model exponents, thresholds, and the raw spectrum.
- The validated exporter returns all declared model and threshold candidates, exclusions, separate model/threshold envelopes, a combined envelope, and the SHA-256 of the full input assumptions.
- It never selects a recommended or corrected material gap.
- Deterministic example: seven candidates span `19.95223 meV`; model-family span is `9.14375 meV`, threshold span is `9.95726 meV`, and the half-range is `9.97612 meV`.
- Research uncertainty export is authorized. Production correction and single-edge selection remain forbidden.

## Authorized next work

1. Continue primary point-data recovery and archive calibrated source figures before digitization.
2. Apply the uncertainty contract only to native digital or calibrated spectra with complete metadata.
3. Preserve the provisional thermal law without adding parameters.
4. Keep the ZG route at method-readiness status until real-export, finite-size, and polar gates pass.

## Explicitly unauthorized

- treating old redundant Hamiltonian degrees of freedom or variance-scaled standard errors as current;
- additional empirical gap coefficients from current or uncalibrated data;
- universal source, composition, carrier, defect, threshold, or model-family corrections from current metadata;
- single-edge selection from the uncertainty ensemble;
- A1 execution, further response-threshold tightening, 120-band static reruns, or unsupported novelty claims.
