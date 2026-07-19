# Active research progress

**Last updated:** 2026-07-19  
**Controlling branch:** `agent/regenerate-hamiltonian-statistics-64d`

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
- For six matrices and eight parameters, residual degrees of freedom change from `760` to `376`.
- Unweighted reduced chi-square and variance scale increase by `2.0212765957`; variance-scaled standard errors increase by `1.4217160742`.
- Correct pseudoinverse treatment of a rank-64 covariance embedded in 128D reproduces the native 64D parameters, chi-square, and parameter covariance.
- No committed physical static record contains calibrated Hamiltonian covariance statistics requiring numerical replacement. The affected surface was the runtime projection statistics API and synthetic validation.

## HgCdTe gap program

The leading provisional temperature law remains:

```text
Eg(x,T) = Eg_Hansen(x,0) + 5.918273117836612e-4
          * (1-2*x) * T^3 / (T^2 + 18.059294367159467^2)
```

It is a constrained Seiler-family parameterization, not a new functional family or production equation.

- No replacement for Hansen's zero-temperature composition polynomial is authorized.
- No production absorption-edge correction is authorized.
- Measurement model, fit window, threshold, carrier state, tail treatment, and an edge-model uncertainty envelope must accompany absorption-derived gaps.
- Historical primary fit-authority count remains zero; Seiler is conditional and the Chu-Sher table is screen-only.
- The complete paired eight-specimen `2 x 2 x 2` design remains the audit-grade acquisition target.

## Authorized next work

1. Build a reusable absorption edge-uncertainty export contract.
2. Continue primary point-data recovery and archive calibrated source figures before digitization.
3. Preserve the provisional thermal law without adding parameters.
4. Keep the ZG route at method-readiness status until real-export, finite-size, and polar gates pass.

## Explicitly unauthorized

- treating old redundant Hamiltonian degrees of freedom or variance-scaled standard errors as current;
- additional empirical gap coefficients from current or uncalibrated data;
- universal source, composition, carrier, defect, threshold, or model-family corrections from current metadata;
- A1 execution, further response-threshold tightening, 120-band static reruns, or unsupported novelty claims.
