# Active research progress

**Last updated:** 2026-07-19  
**Controlling branch:** `agent/hermitian-covariance-64d`

Detailed results live in `research/decision_records/` and `validation/*_reference_result.json`.

## Controlling scientific state

- Static CdTe extraction uses the isospectral selected-band polar Hamiltonian. The complete linear space has four directions; the complete quadratic space has ten established Weiler directions.
- The conventional tied quadratic model fails matrix and spectral closure. Five established departure directions are sufficient at the declared gate; `N2` is negligible. The former `49%`, large-`N2`, all-six-required, 120-band interpretation is superseded.
- The CdTe A0 point remains invalid for long-range polar response. Further threshold tightening and A1 execution are unauthorized.
- Finite-temperature matrix, Fan-vertex, and special-displacement reconstruction methods pass synthetic oracles, but no audited backend yet closes all SOC, Debye-Waller, polar, gauge, and export requirements.

## Matrix covariance correction

- Hermitian `8x8` Hamiltonians now use 64 orthonormal real coordinates.
- General complex dynamical operators retain 128 real coordinates.
- The 64D coordinate norm equals the matrix Frobenius norm, so unweighted fit coefficients and matrix residuals are unchanged.
- Dataset schema `2.0` stores covariance dimension `0`, `64`, or `128` per record.
- Schema `1.0` remains readable: Hamiltonian covariance is projected into 64D; complex self-energy covariance remains 128D.
- Former Hamiltonian chi-square, reduced chi-square, standard errors, and degrees of freedom computed in redundant 128D coordinates are superseded.

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

1. Regenerate Hamiltonian statistical diagnostics that relied on redundant 128D covariance.
2. Build a reusable absorption edge-uncertainty export contract.
3. Continue primary point-data recovery and archive calibrated source figures before digitization.
4. Preserve the provisional thermal law without adding parameters.
5. Keep the ZG route at method-readiness status until real-export, finite-size, and polar gates pass.

## Explicitly unauthorized

- treating old redundant Hamiltonian statistical diagnostics as current;
- additional empirical gap coefficients from current or uncalibrated data;
- universal source, composition, carrier, defect, threshold, or model-family corrections from current metadata;
- A1 execution, further response-threshold tightening, 120-band static reruns, or unsupported novelty claims.
