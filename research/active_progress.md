# Active research progress

**Last updated:** 2026-07-19  
**Controlling ref:** `main`

Detailed results live in `research/decision_records/` and `validation/*_reference_result.json`. This file records the program-level decisions that control new work.

## Controlling scientific state

- Static CdTe extraction uses the isospectral selected-band polar Hamiltonian. The complete linear space has four directions; the complete quadratic space has ten established Weiler directions.
- The conventional tied quadratic model fails matrix and spectral closure. Five established departure directions are sufficient at the declared gate; `N2` is negligible. The former `49%`, large-`N2`, all-six-required, and 120-band interpretation is superseded.
- The CdTe A0 point remains invalid for long-range polar response. Further threshold tightening and A1 execution are unauthorized.
- Finite-temperature matrix, Fan-vertex, and special-displacement reconstruction methods pass synthetic oracles, but no audited backend closes all SOC, Debye-Waller, polar, gauge, and export requirements.

## Matrix covariance and regenerated statistics

- Hermitian `8x8` Hamiltonians use 64 orthonormal real coordinates; general complex dynamical operators retain 128.
- Dataset schema `2.0` stores covariance dimension `0`, `64`, or `128`; schema `1.0` remains readable through explicit migration.
- Old-versus-new regeneration confirms fitted parameters and Frobenius SSE are unchanged to numerical precision.
- For six matrices and eight parameters, residual degrees of freedom change from `760` to `376`; variance-scaled standard errors increase by `1.4217160742`.
- No committed physical static record contains calibrated Hamiltonian covariance statistics requiring numerical replacement.

## HgCdTe gap program

The previously leading provisional temperature law is retained as an archived candidate:

```text
Eg(x,T) = Eg_Hansen(x,0) + 5.918273117836612e-4
          * (1-2*x) * T^3 / (T^2 + 18.059294367159467^2)
```

It is a constrained Seiler-family parameterization, not a new functional family or production equation.

- Chu 1991 provides an independent `x=0.276`, 6-300 K absorption-turning-point series. The observed same-specimen shift is `61 meV`; Hansen predicts `70.466 meV` and the provisional Padé law predicts `79.096 meV`.
- Anchored thermal-increment MAE is `7.215 meV` for Hansen and `11.725 meV` for the provisional Padé law. Across the conservative `x=0.276 +/- 0.005` interval, the minimum Padé MAE (`10.829 meV`) exceeds the maximum Hansen MAE (`8.011 meV`).
- The provisional Padé law therefore does not retain its previously claimed broad cross-source transfer advantage. It must not be described as the leading candidate without this qualification.
- This result does not select Hansen or another universal law because the source is an absorption turning-point observation class with printed figure labels, not an observation-class-controlled latent-gap series.
- No replacement for Hansen's zero-temperature composition polynomial is authorized.
- No production absorption-edge correction is authorized.
- The complete paired eight-specimen `2 x 2 x 2` design remains the audit-grade acquisition target for separating latent gap, observation class, carrier state, and vacancy state.

## Primary evidence state

The centralized recovery ledger contains:

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

At nominal `x=0.17`, Laurenti is the closest local comparator, but model-equivalent composition offsets span from `+0.000573` to `-0.006608`. The record is composition-sensitive, carrier-coupled, and not an exact homogeneous calibration point.

Orlita and Teppe share the Mikhailov/Dvoretskii MBE and magneto-optical lineage. They are not independent cross-laboratory validation sets. The static-law reopening gate remains closed.

## Absorption-edge uncertainty contract

- Every absorption-derived edge record must preserve source calibration, modality, temperature, thickness, composition provenance, carrier state, tail treatment, fit window, search bounds, model definitions, thresholds, and the raw spectrum.
- The exporter returns all valid candidates, exclusions, separate model/threshold envelopes, a combined envelope, and the SHA-256 of the complete input assumptions.
- The candidate ensemble includes fractional-power models and fixed thresholds. The prior-art Chu 1994 Kane-region model may be enabled within `0.170 <= x <= 0.443` and `77 <= T <= 300 K`.
- The exporter never selects a recommended or corrected material gap.
- Deterministic seven-candidate example: combined span `19.95223 meV`, model-family span `9.14375 meV`, threshold span `9.95726 meV`, and half-range `9.97612 meV`.
- Research uncertainty export is authorized. Production correction and single-edge selection remain forbidden.

## Manuscript freeze

Breadth-first exploration is complete. New work is controlled by one immediate manuscript objective:

> **Observation-model uncertainty and identifiability in HgCdTe bandgap extraction.**

The manuscript must combine the validated absorption contract, the demonstrated multi-meV model/threshold sensitivity, cross-source identifiability limits, and the paired acquisition design. It becomes submission-grade only after application to real calibrated spectra.

No additional source-specific screen, synthetic oracle, empirical coefficient, or ledger-only PR is authorized unless it changes at least one controlling decision:

1. authorizes or falsifies the provisional thermal model using independent primary evidence;
2. changes the absorption observation-model conclusion on a real spectrum;
3. independently reproduces or rejects the static CdTe matrix result;
4. opens a physically valid finite-temperature backend route;
5. changes the minimum experimental acquisition design.

## Authorized next work

1. Select `2-4` real primary HgCdTe absorption spectra with recoverable calibration, composition, temperature, thickness, and carrier metadata.
2. Apply the complete uncertainty ensemble, including fractional-power, threshold, and Chu 1994 candidates where source-domain gates permit.
3. Demonstrate whether observation-model uncertainty changes an actual material-model ranking or conclusion.
4. Freeze manuscript figures, tables, claim language, and evidence checklist around that result.
5. In parallel only, define one separately authorized converged reproduction of the static CdTe selected-band result; do not broaden the first-principles program.

## Explicitly unauthorized

- treating Orlita as an exact homogeneous point or independent cross-laboratory validation;
- treating old redundant Hamiltonian degrees of freedom or variance-scaled standard errors as current;
- additional empirical gap coefficients from current or uncalibrated data;
- universal source, composition, carrier, defect, threshold, or model-family corrections from current metadata;
- single-edge selection from the uncertainty ensemble;
- broad source accumulation without a manuscript-critical data target;
- additional micro-PRs that only restate an unchanged authorization boundary;
- A1 execution, further response-threshold tightening, 120-band static reruns, alloy production work, or unsupported novelty claims.
