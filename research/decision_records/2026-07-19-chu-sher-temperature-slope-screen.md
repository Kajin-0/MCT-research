# Secondary Chu-Sher HgCdTe temperature-slope screen

**Date:** 2026-07-19  
**Source:** Chu and Sher, *Physics and Properties of Narrow Gap Semiconductors* (2008), DOI `10.1007/978-0-387-74801-6`, Chapter 3, Table 3.7  
**Status:** secondary screen; not primary fit authority

## Recovered secondary table

Table 3.7 reports one temperature coefficient for each of ten HgCdTe compositions:

```text
x             0.200  0.218  0.226  0.276  0.330  0.344  0.362  0.366  0.416  0.443
dEg/dT
(1e-4 eV/K)    3.10   3.14   2.90   2.34   1.70   1.40   1.37   1.20   0.80   0.50
```

The surrounding text states that the coefficients were obtained from measured absorption-derived `Eg(T)` curves and then fitted by

```text
dEg/dT = (6 - 14x + 3x^2) * 1e-4 eV/K.
```

The exact primary source assignment of every table row is not uniquely resolved by the secondary text. The primary composition method, fit interval, point uncertainty, and covariance are also not recovered.

A source inconsistency remains unresolved: the Chu-Mi-Tang 1992 abstract describes samples thinner than `10 um`, while the secondary book labels one `x=0.200` spectrum as `25 um`. The table is therefore retained only as a source-censored external screen.

## Observation-operator problem

Hansen and Chu 1983 are exactly linear in temperature, so their `dEg/dT` is independent of the slope operator.

Laurenti and the provisional Hansen-Pade law are nonlinear. The secondary table reports one coefficient but does not expose the exact primary regression interval. Assigning one derivative to a nonlinear law would therefore introduce an undocumented observation operator.

The audit evaluates three declared operators:

1. local derivative at `300 K`;
2. secant from `80 K` to `300 K`;
3. secant from `4.2 K` to `300 K`.

Residual units below are `1e-4 eV/K`.

## Results

### Local derivative at 300 K

| Model | RMSE | Mean signed residual: table - model |
|---|---:|---:|
| Chu 1983 | `0.10520` | `-0.02450` |
| Hansen | `0.14348` | `-0.10133` |
| Laurenti | `0.17576` | `-0.15422` |
| provisional Hansen-Pade | `0.33043` | `-0.31579` |

### Secant from 80 K to 300 K

| Model | RMSE | Mean signed residual: table - model |
|---|---:|---:|
| Chu 1983 | `0.10520` | `-0.02450` |
| Hansen | `0.14348` | `-0.10133` |
| Laurenti | `0.14589` | `-0.12070` |
| provisional Hansen-Pade | `0.35041` | `-0.33543` |

### Secant from 4.2 K to 300 K

| Model | RMSE | Mean signed residual: table - model |
|---|---:|---:|
| Laurenti | `0.08250` | `-0.01077` |
| Chu 1983 | `0.10520` | `-0.02450` |
| Hansen | `0.14348` | `-0.10133` |
| provisional Hansen-Pade | `0.34404` | `-0.32919` |

## Interpretation

The winner changes with the nonlinear slope operator:

- Chu 1983 is closest for the local-300-K and 80-300-K operators;
- Laurenti is closest for the 4.2-300-K secant.

This prevents the secondary table from selecting a unique nonlinear temperature law without recovery of the original fit interval.

The provisional Hansen-Pade law ranks fourth under all three declared operators. Its fitted high-temperature amplitude

```text
alpha = 5.918273117836612e-4 eV/K
```

is approximately `10.6219%` larger than Hansen's `5.35e-4 eV/K` amplitude. Over this secondary absorption-derived screen, it therefore predicts systematically steeper temperature dependence.

That result is a cross-source tension, not a refutation of the provisional model. The provisional law was selected using specimen-level Seiler magneto-optical temperature-shape transfer, whereas Table 3.7 is a secondary absorption-family transcription with unrecovered composition and slope-estimation metadata.

The Chu 1983 relation is also not independently validated by this screen because the book presents that relation as a fit to the same source-family temperature coefficients.

## Decision

- admit Table 3.7 as screen-only evidence: **yes**;
- treat the secondary table as primary fit authority: **no**;
- refit `alpha`, `tau`, or a static coefficient: **no**;
- claim one global model winner: **no**;
- record cross-source thermal-slope tension for the provisional law: **yes**;
- require the primary `Eg(T)` points and their fit interval before strict comparison: **yes**.

## Files

- `data/experimental/chu_sher_2008_table3_7_temperature_coefficients.csv`
- `tools/audit_chu_sher_temperature_slope_screen.py`
- `tests/test_chu_sher_temperature_slope_screen.py`
- `validation/chu_sher_temperature_slope_screen_reference_result.json`

## Claim boundary

This screen quantifies compatibility with a secondary transcription. It does not recover the primary spectra, establish composition uncertainty, identify the slope-regression interval, supply independent model validation, or authorize a universal HgCdTe temperature law.
