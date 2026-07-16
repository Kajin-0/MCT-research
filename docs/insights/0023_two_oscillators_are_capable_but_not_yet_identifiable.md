# Insight 0023: two oscillators are capable but not yet identifiable

## Question

Before fitting incomplete experimental data, ask a narrower representational question:

> Can one or two fixed Bose occupation scales compress the established Laurenti analytical equation across composition and temperature?

This is a surrogate-function study. The target values are generated from Laurenti's published equation and are **not experimental observations**.

## Study design

The target grid is

$$
x=0,0.05,\ldots,1,
$$

and

$$
T=0,2,5,10,20,40,77,100,150,200,300,400,500\ \mathrm K.
$$

The candidate model is

$$
E_g(x,T)=
P_2(x)
+
\sum_{j=1}^{J}
A_{j,2}(x)
\frac{2}{\exp(\Theta_j/T)-1},
$$

where both the static term and each oscillator amplitude are quadratic in composition.

A fixed candidate grid is used:

$$
\Theta\in
\{5,10,15,20,30,40,60,80,120,160,240,320,480\}\ \mathrm K.
$$

For every outer fold, the scale or scale pair is selected using only the training data by minimizing training RMSE, then maximum error, then condition number.

The two outer schemes are:

1. leave one composition out;
2. hold out low, intermediate, or high temperature ranges.

## Results

### Leave-one-composition-out

| Model | MAE | RMSE | maximum error | maximum training condition number |
|---|---:|---:|---:|---:|
| one oscillator | 1.073 meV | 1.546 meV | 6.945 meV | 286 |
| two oscillators | 0.591 meV | 0.857 meV | 3.106 meV | 2,802 |

The one-oscillator model selects $\Theta=40$ K in 20 of 21 folds and $60$ K for the held-out HgTe endpoint.

The two-oscillator model selects:

- $(20,240)$ K in 18 folds;
- $(20,160)$ K in two folds;
- $(30,240)$ K at the HgTe endpoint.

Thus the composition interpolation is reasonably stable, but the second model is already substantially more ill-conditioned.

### Held-out temperature ranges

| Model | MAE | RMSE | maximum error | maximum training condition number |
|---|---:|---:|---:|---:|
| one oscillator | 2.792 meV | 4.660 meV | 26.940 meV | 290 |
| two oscillators | 0.979 meV | 1.329 meV | 5.950 meV | 13,883 |

For the one-oscillator model:

- holding out $T\le40$ K selects $80$ K and gives 4.241 meV RMSE;
- holding out $40<T\le200$ K selects $40$ K and gives 2.213 meV RMSE;
- holding out $T>200$ K selects $30$ K and gives 7.184 meV RMSE, with 26.940 meV maximum error.

For the two-oscillator model:

- low-temperature holdout selects $(15,320)$ K;
- intermediate holdout selects $(15,160)$ K;
- high-temperature holdout selects $(20,160)$ K.

Its high-temperature holdout RMSE is 1.458 meV and maximum error is 5.950 meV.

## Interpretation

Laurenti's thermal term is

$$
10^{-4}A(x)\frac{T^2}{T+B(x)},
$$

with a composition-dependent characteristic scale

$$
B(x)=11(1-x)+78.7x.
$$

One fixed Bose scale cannot reproduce that changing curvature uniformly over the full composition and temperature domain. It can interpolate the function at approximately the 1--2 meV RMS level, but its high-temperature extrapolation fails at the tens-of-meV maximum-error level.

Two fixed scales are flexible enough to compress the Laurenti function to approximately 1 meV held-out RMS error. However:

1. the design condition number increases by roughly one to two orders of magnitude;
2. selected scales change materially across temperature folds;
3. the surrogate target itself contains only one composition-dependent Varshni denominator, not evidence for two microscopic phonon channels;
4. no experimental covariance, composition uncertainty, or measurement-class discrepancy is present in this screen.

Therefore the correct conclusion is

$$
\boxed{
\text{two fixed scales are representationally capable, but not physically identified}
}
$$

## Consequence for the experimental benchmark

The one-oscillator model remains the parsimonious first alternative, but it must be tested on held-out temperature ranges, not only held-out compositions.

The two-oscillator model advances only if real specimen data show all of the following:

- temperature-holdout improvement beyond the experimental and composition uncertainty floor;
- stable scale regions or spectral moments across folds;
- acceptable covariance and condition number;
- reduced residual structure rather than redistributed error;
- improvement not driven solely by Cd-rich data or one measurement class.

If the two scales remain fold-dependent and highly correlated, report a low-rank thermal basis or prediction envelope rather than assigning two physical oscillator energies.

## Reproducibility

- study script: `tools/run_laurenti_surrogate_compression.py`;
- aggregate results: `data/validation/laurenti_surrogate_oscillator_compression.csv`;
- benchmark engine: `src/mct_research/analytical_benchmark.py`.
