# Bagot/Bogucki analytic CdTe expansion bridge

## Status

A three-term analytic CdTe thermal-expansion fit published by Bogucki et al. was evaluated as an independent bridge diagnostic for the unresolved `90-293 K` interval.

The fit is based on literature CdTe data attributed to Bagot et al. It provides a continuous `alpha_L(T)` curve but remains secondary evidence until the primary Bagot article, measurement details, and uncertainty are acquired and hashed.

## Source and formula

Bogucki et al., *Physical Review B* **105**, 075412 (2022), DOI `10.1103/PhysRevB.105.075412`, Appendix A, fit the CdTe data with

```text
alpha(T) = sum_i g_i (s_i/T)^2 exp(s_i/T) / [exp(s_i/T)-1]^2
```

where the reported CdTe coefficients are

| i | `s_i`, K | `g_i` |
|---:|---:|---:|
| 1 | 222.02098 | 883.96417 |
| 2 | -40.90023 | -384.86715 |
| 3 | -13241.61 | 1403.50696 |

The resulting `alpha` is interpreted in `10^-8 K^-1`, consistent with the reported CdTe curve and direct Smith-White values.

The underlying primary source is Bagot, Granger, and Rolland, *physica status solidi (b)* **177**, 295-308 (1993), DOI `10.1002/pssb.2221770205`, which reports HgCdTe/HgZnTe expansion and constituent-binary behavior from approximately 4 to 280 K.

## Direct-data consistency

Against direct Smith-White CdTe rows from 2 to 283 K, excluding values explicitly reprinted from other literature, the analytic fit gives approximately

```text
RMS alpha difference      = 0.183 x 10^-6 K^-1
maximum absolute difference = 0.347 x 10^-6 K^-1.
```

This is materially closer to the single-crystal Smith-White data than the unadjusted hot-pressed Browder curve, whose overlap RMS is approximately `0.558 x 10^-6 K^-1` on its documented comparison set.

At the high-temperature endpoints:

```text
Bagot/Bogucki alpha(283 K)  ~= 4.558 x 10^-6 K^-1
Smith-White alpha(283 K)    = 4.700 x 10^-6 K^-1
Bagot/Bogucki alpha(293 K)  ~= 4.587 x 10^-6 K^-1
Williams alpha(293 K)       ~= 4.956 x 10^-6 K^-1.
```

The residual source difference remains visible and must enter any execution uncertainty model.

## Zero-temperature lattice diagnostic

Integrating the analytic fit from `0` to `293.15 K` and applying the audited Williams anchor

```text
a(293.15 K) = 6.480841894 A
```

gives

```text
a0 Bagot/Bogucki fit ~= 6.476427 A.
```

The independently adjusted Browder bridge gives approximately

```text
a0 adjusted Browder ~= 6.476035 A.
```

The bridge-model spread is therefore approximately

```text
0.000392 A.
```

Using the midpoint and combining half this spread conservatively with the Williams anchor bound gives a planning envelope of approximately

```text
a0 ~= 6.47623 +/- 0.00078 A.
```

This corresponds to approximately

```text
0.0120% lattice uncertainty
0.0359% first-order volume uncertainty.
```

The volume uncertainty is about 7.2% of the planned `+/-0.5%` A0 volume bracket. The physical geometry is therefore sufficiently narrow for a sensitivity smoke in numerical terms.

## Decision

The remaining blocker is now **provenance rather than numerical sensitivity**.

The analytic fit is not promoted to the execution chain because:

1. it is a secondary fit rather than the acquired primary Bagot record;
2. the primary measurement morphology, calibration, and uncertainty are not yet audited;
3. the fit endpoint differs from Williams by approximately `0.37 x 10^-6 K^-1`;
4. the exact source bytes used for the coefficients are not hashed in the repository.

The result supports a bounded planning geometry but not a source-traceable execution lattice.

## Next gate

Acquire one of:

1. Bagot et al. 1993, to audit the primary full-range CdTe data underlying the analytic fit; or
2. Greenough and Palmer 1973, DOI `10.1088/0022-3727/6/5/315`, for a direct single-crystal `42-300 K` bridge.

Greenough remains the preferred morphology-consistent execution source. Bagot is the stronger immediate cross-check because the secondary coefficients already reproduce the accepted direct data well.

No DFT, DFPT, phonon, AHC, HgTe, or alloy calculation is authorized by this diagnostic.
