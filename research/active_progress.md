# Active research progress

**Last updated:** 2026-07-19  
**Controlling ref:** `main` plus draft manuscript PR #131

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

The leading provisional temperature law remains:

```text
Eg(x,T) = Eg_Hansen(x,0) + 5.918273117836612e-4
          * (1-2*x) * T^3 / (T^2 + 18.059294367159467^2)
```

It is a constrained Seiler-family parameterization, not a new functional family or production equation.

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
- Research uncertainty export is authorized. Production correction and single-edge selection remain forbidden.

## Real-spectrum manuscript result

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
- Chang 2006 remains a useful low-temperature target, but its plotted experimental markers overlap fitted curves. Forced digitization is unauthorized without raw points or a cleaner source asset.

## Manuscript freeze

Breadth-first exploration is complete. The active manuscript objective is:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

The scientific, bibliography, target-journal, deterministic-asset, editable-LaTeX, technical-review, and PDF-render gates are satisfied in draft PR #131.

The reviewed manuscript head is `a249c30d21c8f0a46c36ca91d6c85f8cce1ad2bf`:

```text
focused manuscript workflow   29704457275   success
Python 3.11/3.13 workflow     29704457252   success
IRPT LaTeX workflow            29704457256   success
PDF artifact                   8447468840    18 pages, visually inspected
```

No further scientific implementation, source screening, figure generation, or manuscript restructuring is authorized for this submission unless it corrects an identified defect or changes a controlling conclusion.

## Authorized next work

1. Supply and verify author names, affiliations, corresponding-author details, and postal address.
2. Add the public archive DOI or final repository URL.
3. Confirm funding, competing-interest, acknowledgment, and CRediT statements.
4. Select conflict-free suggested reviewers.
5. Perform the author-controlled final approval, then mark PR #131 ready and merge or submit the package.
6. Add low-temperature, native-export, or independent cross-laboratory evidence only if it becomes available cleanly and changes a controlling conclusion; do not resume broad source accumulation.
7. In parallel only, define one separately authorized converged reproduction of the static CdTe selected-band result; do not broaden the first-principles program.

## Explicitly unauthorized

- treating Orlita as an exact homogeneous point or independent cross-laboratory validation;
- treating old redundant Hamiltonian degrees of freedom or variance-scaled standard errors as current;
- additional empirical gap coefficients from current or uncalibrated data;
- universal source, composition, carrier, defect, threshold, or model-family corrections from current metadata;
- strict Seiler-versus-Hansen ranking from the two Moazzami specimens;
- single-edge selection from the uncertainty ensemble;
- forced digitization of overlapping Chang 2006 points;
- broad source accumulation without a manuscript-critical data target;
- additional micro-PRs that only restate an unchanged authorization boundary;
- A1 execution, further response-threshold tightening, 120-band static reruns, alloy production work, or unsupported novelty claims.
