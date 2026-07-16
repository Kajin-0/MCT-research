# Krishnamurthy 1995 gap-indexed hyperbolic closure

## Scientific question

Krishnamurthy et al. state that the reported effective mass and hyperbolic parameter `c` are directly proportional to the gap, and conclude that `gamma` and `c` can be interpolated for any positive HgCdTe gap.

Does Table II support literal direct proportionality, or only a weaker statement that the reduced hyperbolic parameters are smooth functions of the gap?

This is an internal test against historical calculated HPTB plus valence-force-field data. It is not experimental validation and the diagnostic relations below are not proposed as new HgCdTe material equations.

## Paper convention

The lowest conduction band is represented by

```text
epsilon(k,T) = sqrt[gamma(T) k^2 + c(T)^2] - c(T).
```

The small-`k` curvature therefore gives

```text
m*(T)/m*(T0)
  = [c(T)/gamma(T)] / [c(T0)/gamma(T0)].
```

PR #50 verified this identity for all 21 Table II rows. The present test asks a different question: whether `c`, `gamma`, and the resulting mass ratio require temperature as an independent variable once the calculated gap is known.

## Literal proportionality test

If `c` and `m*` are directly proportional to the gap in the strict mathematical sense, normalization at 1 K requires

```text
c(T)/c(1 K)  = Eg(T)/Eg(1 K)
```

and

```text
m*(T)/m*(1 K) = Eg(T)/Eg(1 K).
```

The printed table does not satisfy those identities through 300 K.

| Diagnostic | Result |
|---|---:|
| change in `c/Eg`, 1 to 300 K | -19.774% |
| maximum error predicting normalized `c` from normalized `Eg` | 24.647% |
| RMS normalized-`c` error | 11.618% |
| maximum error predicting the mass ratio from normalized `Eg` | 17.784% |
| RMS mass-ratio error | 8.494% |

The paper's phrase “directly proportional” therefore cannot be read as an exact proportionality in the printed numerical table. It is defensible only as a qualitative statement that `c` and `m*` increase with the positive gap over most of the tabulated range.

## Predeclared held-out test

To test the weaker interpolation claim without fitting the complete table, use:

- training: every Table II point from 1 to 100 K;
- held out: 150, 200, 250, and 300 K;
- excluded from the scientific decision: 350 to 600 K.

The lowest-complexity gap-indexed diagnostics are

```text
c(Eg) = a_c + b_c Eg
```

and

```text
gamma(Eg) = a_gamma + b_gamma Eg.
```

The training-only coefficients are

```text
c(Eg) = 0.0280752640 eV + 0.275577448 Eg
```

and

```text
gamma(Eg) = 51.7214785 - 35.3706510 Eg,
```

where `Eg` and `c` are in eV and `gamma` remains in the paper's reported convention.

These are diagnostics of the table, not transferable material parameters.

## Held-out results, 150 to 300 K

### Hyperbolic energy `c`

| Statistic | Result |
|---|---:|
| maximum absolute error | 2.467 meV |
| RMS error | 1.327 meV |
| maximum fractional error | 2.717% |
| RMS fractional error | 1.508% |

### Printed `gamma`

| Statistic | Result |
|---|---:|
| maximum absolute error | 1.1294 reported units |
| RMS error | 0.6360 reported units |
| maximum fractional error | 2.503% |
| RMS fractional error | 1.409% |

### Reconstructed effective-mass ratio

Using

```text
m_pred(T)/m_pred(1 K)
  = [c_pred(T)/gamma_pred(T)]
    /[c_pred(1 K)/gamma_pred(1 K)],
```

gives:

| Statistic | Result |
|---|---:|
| mean absolute fractional error | 0.449% |
| RMS fractional error | 0.666% |
| maximum absolute fractional error | 1.283% at 300 K |

Thus a low-temperature, gap-indexed description predicts the held-out Table II mass ratios substantially better than literal `m* proportional to Eg`.

## Low-temperature turnover

The 10 and 20 K rows provide a limited same-gap diagnostic:

| Difference, 20 K minus 10 K | Value |
|---|---:|
| `Eg` | -0.11 meV |
| `c` | +0.40 meV |
| `gamma` | -0.0384 reported units |

These differences prevent claiming exact single-valued closure at arbitrary precision. However, they are comparable to the printed rounding and far below the historical calculation's approximately 10-15 meV overall comparison/model floor.

The approximately 1 meV gap turnover therefore does not resolve an additional independent temperature variable in `c` or `gamma`.

## High-temperature stop

The 1-100 K relations should not be extrapolated beyond the held-out 300 K limit.

At 350-600 K, the maximum fractional errors reach:

| Quantity | Maximum error |
|---|---:|
| `c` | 45.744% |
| `gamma` | 35.605% |
| reconstructed mass ratio | 16.638% |

This breakdown is consistent with the original paper's warning that higher-order perturbation or finite-temperature-renormalized bands are needed at elevated temperature.

## Scientific decision

```text
Literal direct proportionality is rejected.
Gap-indexed interpolation is supported below 300 K at the few-percent level.
```

The result sharpens the interpretation of the historical prior art:

1. The printed table does not support `c proportional to Eg` or `m* proportional to Eg` as exact equations.
2. Below 300 K, the changes in `c`, `gamma`, and their mass-ratio combination are largely indexed by the calculated gap.
3. Table II does not resolve a separate temperature variable beyond `Eg` for these reduced parameters.
4. The result is consistent with PR #50: large scalar Kane-velocity renormalization is not supported below 300 K.
5. This does not close the complete 8-band Hamiltonian or constrain separate `P8/P7`, `F`, `Delta`, or Luttinger parameters.

## Uncertainty and claim boundary

Limitations:

- the source consists of calculated historical values, not measurements;
- only four temperatures are held out;
- all values are rounded and lack datum-level uncertainty;
- the diagnostic uses one composition, nominally `x=0.22`;
- `gamma` is retained in the printed convention without inferring its absolute unit normalization;
- a successful gap-indexed interpolation does not prove microscopic equivalence between temperature and composition changes.

The conclusion would be falsified by:

- unrounded Table II values producing more than 5% held-out mass error below 300 K;
- matched-gap calculations at different temperatures that disagree beyond numerical and model uncertainty;
- experimental mass or Kane-velocity data retaining more than 5% residual after conditioning on the measured gap.

## Reproduction

```bash
python tools/analyze_krishnamurthy1995_gap_indexed_closure.py \
  --output-csv data/theory/krishnamurthy1995_hg078cd022_gap_indexed_closure.csv \
  --summary-json /tmp/krishnamurthy1995_gap_indexed_closure.json
```
