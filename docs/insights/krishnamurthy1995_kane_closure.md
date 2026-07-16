# Krishnamurthy 1995 Table II finite-temperature Kane closure

## Question

Does the calculated Hg0.78Cd0.22Te Table II dataset require a large temperature-dependent Kane velocity, or can its effective-mass change be described primarily by the reported hyperbolic energy scale with an approximately constant velocity?

This is an internal reproducibility test against historical calculated HPTB plus valence-force-field data. It is not experimental validation.

## Primary-paper convention

The owner-supplied primary paper describes the lowest conduction-band energy relative to its minimum by

```text
epsilon(k,T) = sqrt(gamma(T) k^2 + c(T)^2) - c(T).
```

Table II prints, in order:

- temperature;
- calculated gap `Eg`;
- hyperbolic parameter `gamma`;
- hyperbolic energy parameter `c`;
- `m*(T)/m*(0)`.

The note below the table gives

```text
m*(0)/m0 = 0.008
```

and a 13.6 meV zero-point gap correction.

The reciprocal-space normalization of printed `k` is retained rather than inferred. Consequently, the absolute dimensional normalization of printed `gamma` is not used to claim an absolute multiband Kane matrix element. The equation itself requires `gamma k^2` to have dimensions of energy squared, while `c` is an energy.

## Exact table closure

At small `k`,

```text
epsilon(k,T) = gamma(T) k^2 / [2 c(T)] + O(k^4).
```

For a fixed reciprocal-space convention,

```text
m*(T)/m*(T0)
  = [c(T)/gamma(T)] / [c(T0)/gamma(T0)].
```

This identity reproduces all 21 printed mass ratios from 1 to 600 K.

| Reproduction statistic | Result |
|---|---:|
| maximum fractional error | 0.1093% |
| RMS fractional error | 0.0449% |
| maximum disagreement between the two relative-velocity reconstructions | 0.0546% |

The residual scale is consistent with rounding of the printed `gamma`, `c`, and mass-ratio columns.

## Equivalent hyperbolic velocity

The local physical form can be written as

```text
epsilon(q,T) = sqrt[(hbar v_h(T) q)^2 + c(T)^2] - c(T),
```

so the curvature mass satisfies

```text
c(T) = m*(T) v_h(T)^2.
```

Using the reported `m*(0)/m0=0.008`,

```text
v_h(T) = sqrt[c(T)/m*(T)].
```

The absolute values are equivalent hyperbolic velocities, not a unique extraction of the complete 8-band Kane parameter `P`.

| Temperature | Equivalent velocity |
|---:|---:|
| 1 K | 1.136984 x 10^6 m/s |
| 300 K | 1.105239 x 10^6 m/s |
| 600 K | 1.292677 x 10^6 m/s |

### Constant-velocity null

Over the paper-relevant 1–300 K interval:

| Statistic relative to 1 K | Result |
|---|---:|
| mean signed drift | -0.916% |
| RMS drift | 1.317% |
| maximum absolute drift | 2.792% at 300 K |
| RMS residual about the best constant | 0.955% |
| maximum residual about the best constant | 1.894% |

The velocity decreases gently to a minimum near 300 K. It then recovers and rises at higher temperature. The 5% threshold is crossed only at 550–600 K, where the paper itself states that higher-order perturbation or self-consistently renormalized finite-temperature bands become necessary. The high-temperature rise is therefore not a robust rejection of the constant-velocity null.

## Reduced `Eg/(2m*)` diagnostic

The requested reduced diagnostic is

```text
v_eff(T) = sqrt[Eg(T)/(2 m*(T))].
```

It assumes the symmetric two-band identity

```text
c(T) = Eg(T)/2.
```

Under that convention, the maximum 1–300 K drift is 8.528%, which exceeds the 5% threshold. However, Table II does not obey the required identity:

| Temperature | `c / (Eg/2)` |
|---:|---:|
| 1 K | 1.0352 |
| 300 K | 0.8305 |

Therefore the greater-than-5% reduced drift is convention-sensitive. It cannot override the exact hyperbolic closure printed by the paper. A velocity defined from `Eg/(2m*)` reproduces the mass algebraically when inserted back into the same equation and is not an independent predictive test.

## Model comparison through 300 K

The reported mass ratios were compared with three restricted descriptions.

### 1. Gap-only temperature renormalization with fixed velocity

```text
m*(T)/m*(1 K) = Eg(T)/Eg(1 K).
```

| Error statistic | Result |
|---|---:|
| mean absolute fractional error | 5.852% |
| RMS fractional error | 8.494% |
| maximum absolute fractional error | 17.784% at 300 K |

Gap motion alone does not reproduce the calculated mass curve.

### 2. Temperature-dependent velocity with a forced `c=Eg/2` closure

Using the paper-convention hyperbolic velocity while replacing `c` by `Eg/2` gives a maximum mass-ratio error of 24.647% at 300 K. The failure is caused by the false `c=Eg/2` identification, not by insufficient velocity drift.

The alternative reduced velocity `sqrt[Eg/(2m*)]` reproduces the mass exactly by construction and has no independent predictive content.

### 3. Complete reported hyperbolic parameterization

```text
m*(T)/m*(1 K)
  = [c(T)/gamma(T)] / [c(1 K)/gamma(1 K)].
```

| Error statistic | Result |
|---|---:|
| mean absolute fractional error | 0.0385% |
| RMS fractional error | 0.0484% |
| maximum absolute fractional error | 0.1093% |

This is a successful reproduction of Table II, not independent physical validation of the historical model.

## Low-temperature turnover

The calculated gap falls from 113.60 meV at 1 K to 112.56 meV at 20 K, a depth of 1.04 meV, before increasing.

At the 20 K minimum:

- paper-convention equivalent velocity drift: -0.0197%;
- reduced `Eg/(2m*)` velocity drift: -0.815%.

The turnover does not create a resolved Kane-closure effect. Its 1.04 meV depth is below the paper-level approximately 10–15 meV comparison/model accuracy and Table II supplies no pointwise uncertainty. It remains a candidate signed-channel feature, not established physics.

## Numerical decision

The robust paper-convention velocity drift is 2.792% over 1–300 K, below the declared 5% threshold.

```text
Decision: large P(T) renormalization is not supported by Table II.
```

This supports the repository's leading constant-Kane-velocity null at the few-percent level. It does not show that every non-gap invariant is temperature independent, and it does not close the complete 8-band Hamiltonian.

The historical table does not determine:

- an absolute conventional 8-band `P(T)` without a declared reciprocal-space and Hamiltonian convention;
- separate `P8(T)` and `P7(T)`;
- `F(T)`;
- `gamma1(T)`, `gamma2(T)`, or `gamma3(T)`;
- off-diagonal matrix self-energy or wavefunction rotation.

The candidate microscopic contribution remains a complete matrix self-energy projection and closure test, but Table II does not provide evidence that a large scalar `P(T)` effect should be expected below 300 K.

## Uncertainty and falsification

Limitations:

- all 21 points are historical calculated outputs, not measurements;
- printed values are rounded and have no datum-level uncertainty;
- the paper's overall comparison/model floor is approximately 10–15 meV;
- the absolute printed-`gamma` reciprocal-space normalization is not inferred;
- the equivalent absolute velocity inherits the stated `m*(0)/m0=0.008`;
- the 550–600 K behavior lies in the regime where the authors identify missing higher-order/self-consistent effects.

The conclusion is falsified if:

1. primary-source inspection shows a different hyperbolic equation or column ordering;
2. unrounded data fail the `c/gamma` mass identity beyond numerical accuracy;
3. modern calculation or experiment resolves more than 5% velocity drift over a controlled 1–300 K range;
4. a low-temperature turnover survives a complete uncertainty budget and materially changes a held-out observable.

## Reproduction

```bash
python tools/analyze_krishnamurthy1995_kane_closure.py \
  --output-csv data/theory/krishnamurthy1995_hg078cd022_kane_closure.csv \
  --summary-json /tmp/krishnamurthy1995_kane_closure_summary.json
```
