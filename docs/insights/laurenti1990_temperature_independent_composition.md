# Laurenti 1990 temperature-independent composition

## Question

Laurenti et al. report a temperature-independent HgCdTe composition of

```text
x = 0.505.
```

Is that value experimentally resolved to three decimal places, or is it the rounded root of the paper's global empirical equation?

## Exact root of the printed equation

The temperature-dependent part of Laurenti equation 7 is

```text
Delta Eg(x,T)
  = 1e-4 A(x) T^2 / B(x,T),
```

with

```text
A(x) = 6.3(1-x) - 3.25x - 5.92x(1-x)
```

and

```text
B(x,T) = 11(1-x) + 78.7x + T.
```

For `0 <= x <= 1` and `T >= 0`, the denominator is positive. Therefore the fitted model is temperature independent exactly when `A(x)=0`.

The two algebraic roots of the printed polynomial are

```text
x = 0.5047258866289238
x = 2.108449789046752.
```

Only the first is physical. It rounds to `0.505`.

Thus the quoted value is mathematically reproducible from the printed coefficients.

## Printed-coefficient precision

The paper does not report covariance or uncertainty for the fitted thermal coefficients. As a formatting sensitivity, allow each coefficient to vary by half a unit in its last printed decimal place:

```text
6.3   -> [6.25, 6.35]
-3.25 -> [-3.255, -3.245]
-5.92 -> [-5.925, -5.915].
```

Across the eight coefficient corners, the physical root spans

```text
0.501711 <= x <= 0.507723.
```

The interval width is `0.006012`. This is not a statistical confidence interval, but it shows that the third decimal depends on coefficient digits not supplied by the article.

## Experimental resolution

The paper reports better-than-3-meV accuracy for the excitonic-model-corrected absorption edges. The associated high-Cd specimen work reports composition accuracy near `+/-0.005`.

At the fitted root and 300 K,

```text
d(Delta Eg)/dx = -0.247549 eV per composition fraction.
```

Therefore:

| Diagnostic | Equivalent scale |
|---|---:|
| shift produced by `Delta x = +/-0.005` at 300 K | `+/-1.238 meV` |
| 3 meV single-edge scale | `Delta x = 0.0121` |
| two independent 3 meV edge values | `Delta x = 0.0171` |

A composition displacement of `0.005` around the root produces a thermal-shift change smaller than the stated single-edge accuracy.

The numerical resolution estimates are diagnostics, not formal confidence limits, because pointwise covariance and fitted-parameter uncertainty are unavailable.

## Experimental bracketing

Figure 1 displays a small positive temperature shift for the `x=0.500` specimen and a small negative shift for the `x=0.550` specimen. Equation 7 gives at 300 K:

| Composition | Thermal shift |
|---:|---:|
| `x=0.500` | `+1.174 meV` |
| `x=0.505` | `-0.068 meV` |
| `x=0.550` | `-10.795 meV` |

The experiment supports a sign reversal near `x=0.5`. It is not a dense local composition scan around `x=0.505`.

## Decision

```text
x=0.505 is the rounded root of Laurenti's printed global empirical fit.
The temperature-sign reversal is experimentally bracketed near x=0.5,
but the critical composition is not experimentally resolved to 0.001.
```

A defensible statement is therefore approximately

```text
x_critical about 0.505 within the Laurenti empirical model,
with experimental precision no better established than order 0.005-0.01.
```

The lower bound reflects reported composition precision; the larger scale reflects the stated energy resolution when translated through the 300 K thermal slope. No formal uncertainty interval can be assigned without the original fit covariance and specimen-level composition measurements.

## Claim boundary

- This does not dispute the existence of a near-temperature-invariant composition.
- It does not refit Figure 1 or Figure 2.
- It does not provide a microscopic explanation for the zero crossing.
- The observable remains an excitonic-model-corrected absorption edge, not a raw quasiparticle gap.
- The exact zero is a property of the empirical numerator; it is not a composition known experimentally to four significant figures.

## Reproduction

```bash
python tools/analyze_laurenti1990_temperature_independent_composition.py \
  --output-csv data/experimental/laurenti1990_temperature_independent_composition.csv \
  --summary-json /tmp/laurenti1990_temperature_independent_composition.json
```
