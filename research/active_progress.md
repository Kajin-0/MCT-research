# Active research progress

**Last updated:** 2026-07-19  
**Controlling ref:** `main`

Detailed results live in `research/decision_records/` and `validation/*_reference_result.json`. This file records the program-level decisions that control new work.

## Controlling scientific state

- Static CdTe extraction uses the isospectral selected-band polar Hamiltonian. The complete linear space has four directions; the complete quadratic space has ten established Weiler directions.
- The conventional tied quadratic model fails matrix and spectral closure. Five established departure directions are sufficient at the declared gate; `N2` is negligible. The former `49%`, large-`N2`, all-six-required, and 120-band interpretation is superseded.
- An independent post-processing implementation on the immutable physical artifact reproduces the selected-band isospectral construction, the 4D linear and 10D quadratic invariant spaces, and the conventional quadratic failure on an untouched `[110]` holdout.
- This independent reproduction uses direct SVD polar transport and a separately implemented raw-symmetry projector. It is not a new electronic-structure calculation and does not establish PBE, pseudopotential, geometry, cutoff, or band-count convergence.
- The static post-processing reproducibility question is closed. Additional static replication on the same physical artifact is unauthorized; a genuinely independent electronic-structure setup would require separate scientific justification and authorization.
- The CdTe A0 point remains invalid for long-range polar response. Further threshold tightening and A1 execution are unauthorized.
- Finite-temperature matrix, Fan-vertex, and special-displacement reconstruction methods pass synthetic oracles, but no audited backend closes all SOC, Debye-Waller, polar, gauge, and export requirements.

## Independent static CdTe reproduction

The independent SVD-polar path reproduces:

```text
minimum selected overlap singular value       0.9998015324
maximum selected eigenvalue error              2.576e-14 eV
complete linear invariant dimension            4
complete quadratic invariant dimension         10
complete linear training residual              1.523e-7
complete linear [110] holdout residual          1.447e-7
complete quadratic training residual           1.255e-5
complete quadratic [110] holdout residual       7.956e-6
conventional quadratic training residual       0.287044
conventional quadratic [110] holdout residual   0.332112
P8                                              6.772222 eV A
P7                                              6.201826 eV A
```

The `[110]` direction is excluded from training. Coarse/fine/Richardson variation is `1.42e-4` for `P8` and `1.17e-4` for `P7`. Scalar differences from the controlling implementation are no larger than `1.88e-11` for residual diagnostics and `2.83e-13 eV A` for the two linear couplings.

Authorized conclusion: the controlling static post-processing result is independently reproducible on the same immutable physical input. Unauthorized conclusion: that the underlying physical calculation or fitted material parameters are independently validated.

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
- The Chu 1991 eight-specimen 300 K composition series separates absolute turning-point agreement from composition shape. Raw non-circular MAE favors Schmit-Stelzer (`8.579 meV`), while leave-one-specimen-out transfer of one source-class offset favors Seiler (`4.186 meV`) and Hansen (`4.277 meV`).
- Seiler and Hansen differ by only `0.091 meV` in offset-transfer MAE and are not distinguishable. The provisional Padé value is `7.479 meV`.
- Across a shared `delta_x = +/-0.005` composition-bias sweep, the minimum Padé offset-transfer MAE (`7.424 meV`) exceeds the maximum Hansen MAE (`4.320 meV`) by `3.104 meV`.
- These Chu results do not select Hansen, Seiler, or another universal law because the source reports absorption turning points, printed figure labels, incomplete specimen-state metadata, and a circular Chu-equation lineage.
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

## Completed manuscript milestone

PR #131 merged the submission-oriented manuscript:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

Two Moazzami 2005 solid-IRSE traces pass the complete contract:

```text
x=0.226, T=300 K, d=15.40 um, 125 derived points
x=0.310, T=300 K, d=4.95 um, 115 derived points
```

- Fractional/Chu fitted-model spans are `6.414 meV` and `6.830 meV`.
- Coordinate perturbation moves every fitted-model edge by less than `0.891 meV`.
- Fixed thresholds through `4000 cm^-1` remain below the declared `5 meV` coordinate-sensitivity gate.
- The `5000 cm^-1` crossing for `x=0.310` shifts by `5.694 meV` and is excluded from precision claims.
- Operational threshold choice changes the nominal closest material comparator. No threshold is identified with the latent gap.
- Published Seiler 1990 is nominally closest for every fractional/Chu fitted edge, but its advantage over Hansen is only `0.177-0.255 meV`.
- Because specimen-level composition uncertainty is unreported and both spectra come from one study, the Seiler-Hansen ordering is descriptive only. Strict material-law ranking is not authorized.

Issue #129 is complete. Journal submission and author declarations are external administrative actions rather than active research-development work.

## Active research track

Issue #132 is the controlling post-manuscript evidence program:

> **Integrate historical HgCdTe magneto-optical and edge-observation evidence.**

New work must change a controlling decision by separating observation classes, specimen lineage, composition uncertainty, carrier state, or defect state. Additional unpaired literature accumulation is not sufficient.

## Authorized next work

1. Prioritize paired or same-specimen cross-modality evidence that can estimate an observation-class offset without pooling unlike measurements.
2. Use the Chu 1991 composition result as a prototype for leakage-safe nuisance-offset transfer, not as a universal correction.
3. Recover and audit Herrmann 1992, DOI `10.1016/0022-0248(92)90851-9`, only if the complete operator can be reconstructed without hybrid assumptions.
4. Convert the paired `2 x 2 x 2` acquisition design into a collaboration-ready experimental protocol with metrology, processing, calibration, and covariance requirements.
5. Reopen material-law development only after independent observation-class-controlled evidence exceeds propagated composition and measurement uncertainty.

## Explicitly unauthorized

- treating Orlita as an exact homogeneous point or independent cross-laboratory validation;
- treating old redundant Hamiltonian degrees of freedom or variance-scaled standard errors as current;
- additional empirical gap coefficients from current or uncalibrated data;
- universal source, composition, carrier, defect, threshold, or model-family corrections from current metadata;
- treating a fitted Chu source offset as transferable outside that source and observation class;
- additional static post-processing replication on the same physical artifact;
- claiming static electronic-structure convergence from the independent post-processing result;
- single-edge selection from the uncertainty ensemble;
- broad source accumulation without a decision-changing target;
- additional micro-PRs that only restate an unchanged authorization boundary;
- A1 execution, further response-threshold tightening, 120-band static reruns, alloy production work, or unsupported novelty claims.
