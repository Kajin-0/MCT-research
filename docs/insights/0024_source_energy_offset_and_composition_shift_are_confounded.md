# Insight 0024: source energy offsets and composition shifts are confounded in Hansen Table I

## Scope

The 16 numerical points printed in Hansen Table I consist of seven Tobin photodiode cutoff measurements and nine Rawe photoconductor cutoff measurements, all reported at 80 K over the narrow interval

$$
0.199\le x\le0.216.
$$

These points were part of the historical Hansen evidence base. They are not an independent validation set for the Hansen equation.

The present question is narrower:

> Can these points distinguish a source-dependent energy or edge-criterion offset from a source-dependent composition calibration shift?

## Two competing adjustment models

For a published gap equation $f(x,T)$, consider

$$
y_i=f(x_i,T_i)+b_{s(i)}+\epsilon_i,
$$

where $b_s$ is a source-dependent energy offset, and

$$
y_i=f(x_i+\delta x_{s(i)},T_i)+\epsilon_i,
$$

where $\delta x_s$ is a source-dependent composition shift.

For small $\delta x_s$,

$$
f(x+\delta x_s,T)
\approx
f(x,T)
+
\frac{\partial f}{\partial x}\delta x_s.
$$

Therefore the two corrections are locally equivalent when $\partial f/\partial x$ is nearly constant over the source's composition window:

$$
\boxed{
b_s
\approx
\left\langle\frac{\partial f}{\partial x}\right\rangle_s
\delta x_s
}.
$$

Only curvature of the gap law across the observed composition interval can separate the two mechanisms from gap data alone.

## Exact diagnostic results

### Residual metrics

| Model | Adjustment | MAE | RMSE | Maximum error |
|---|---|---:|---:|---:|
| Hansen | none | 2.158 meV | 2.742 meV | 4.985 meV |
| Hansen | source energy offsets | 1.791 meV | 2.288 meV | 5.942 meV |
| Hansen | source composition shifts | 1.790 meV | 2.288 meV | 5.942 meV |
| Laurenti | none | 2.962 meV | 3.776 meV | 10.279 meV |
| Laurenti | source energy offsets | 1.743 meV | 2.365 meV | 6.798 meV |
| Laurenti | source composition shifts | 1.743 meV | 2.366 meV | 6.807 meV |

For Hansen, the energy-offset and composition-shift RMSE values differ by only

$$
0.00027\ \mathrm{meV}.
$$

For Laurenti, they differ by only

$$
0.00120\ \mathrm{meV}.
$$

These differences are negligible relative to the unknown datum-level uncertainty and the measurement-definition heterogeneity of the historical compilation.

### Fitted equivalent corrections

| Model | Source | Energy offset | Composition shift |
|---|---|---:|---:|
| Hansen | Tobin | $-0.957$ meV | $-0.000591$ |
| Hansen | Rawe | $-1.830$ meV | $-0.001134$ |
| Laurenti | Tobin | $+3.481$ meV | $+0.002000$ |
| Laurenti | Rawe | $+2.447$ meV | $+0.001407$ |

The energy-offset-to-composition-shift ratios reproduce the local composition derivatives of the respective equations.

## Linear identifiability calculation

Linearize one source at its reported compositions and parameterize:

- $b_s$ in meV;
- $\delta x_s$ in units of $0.001$ composition.

The local design columns are

$$
X_s=
\begin{bmatrix}
10^{-3} & 10^{-3}\partial_xf(x_1,T_1)\\
\vdots & \vdots\\
10^{-3} & 10^{-3}\partial_xf(x_n,T_n)
\end{bmatrix}.
$$

The resulting diagnostics are:

| Model | Source | $\partial_xf$ range | Scaled condition number | Parameter-covariance correlation |
|---|---|---:|---:|---:|
| Hansen | Tobin | 1.6126--1.6209 eV | 1391 | $-0.99999871$ |
| Hansen | Rawe | 1.6109--1.6209 eV | 1359 | $-0.99999865$ |
| Laurenti | Tobin | 1.7355--1.7419 eV | 2011 | $-0.99999934$ |
| Laurenti | Rawe | 1.7355--1.7432 eV | 1944 | $-0.99999929$ |

The derivative varies by less than approximately 0.62% within either source. Consequently, the two adjustment directions are almost collinear.

## Consequences

### 1. The adjusted ranking is not a validation result

After two source-specific adjustments, Hansen and Laurenti have MAEs of approximately 1.790 and 1.743 meV. Their difference is only

$$
0.047\ \mathrm{meV}.
$$

This does not establish Laurenti superiority. The data are in-sample for Hansen, the corrections are fitted to the same points, and datum-level uncertainties are unavailable.

### 2. A free source offset can hide composition error

Allowing both $b_s$ and $\delta x_s$ without informative priors would create an effectively singular fit. A benchmark must not interpret a fitted source energy correction as evidence for a measurement-class offset unless composition calibration is independently constrained.

### 3. The next data should break the ridge

At least one of the following is required:

1. independent composition metrology with a reported uncertainty;
2. a substantially wider composition range measured by the same method and laboratory;
3. repeated temperature measurements on the same specimen, where a constant source or composition offset cannot remove thermal curvature;
4. two measurement methods applied to the same independently characterized specimen;
5. an external calibration standard that constrains the edge-criterion offset.

### 4. Source corrections must be validated out of source

Source-specific offsets can be nuisance parameters in a hierarchical model, but they cannot count as predictive improvement unless evaluated under source-level holdout or constrained by external calibration.

## Reproducibility

- source table: `data/hansen/measurements.csv`;
- executable study: `tools/run_hansen_table1_source_adjustment_diagnostic.py`;
- model metrics: `data/validation/hansen_table1_source_adjustment_models.csv`;
- identifiability diagnostics: `data/validation/hansen_table1_source_adjustment_identifiability.csv`.
