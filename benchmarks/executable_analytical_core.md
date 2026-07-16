# Executable analytical benchmark core

## Status

The repository now contains a synthetic-validated fitting and cross-validation layer in

```text
src/mct_research/analytical_benchmark.py
```

It does **not** yet contain a defensible ranking of Hansen, Laurenti, one-oscillator, or two-oscillator models on a complete experimental dataset.

## Supported linear model family

For fixed oscillator temperatures $\Theta_j$, the executable model is

$$
E_g(x,T)=
P_s(x)
+
\sum_{j=1}^{J}
P_j(x)
\left[
\coth\left(\frac{\Theta_j}{2T}\right)-1
\right]
+
T P_{\mathrm{qh}}(x),
$$

with

$$
\coth\left(\frac{\Theta}{2T}\right)-1
=
\frac{2}{\exp(\Theta/T)-1}.
$$

The zero-temperature value of every occupation basis is defined by its limiting value, zero. Consequently, the static polynomial includes the zero-point-renormalized intercept.

The optional $T P_{\mathrm{qh}}(x)$ block is a benchmark nuisance basis. It must not be described as a microscopic quasiharmonic derivation unless independent thermal-expansion and deformation-potential information is supplied.

## Model mapping

| Benchmark model | Executable specification |
|---|---|
| refitted Hansen form | static degree 3; no oscillator; linear-$T$ degree 1; equality constraint $q_1=-2q_0$ |
| constrained empirical model | selected static degree and linear-$T$ degree |
| one oscillator | one fixed $\Theta$ and polynomial amplitude |
| two oscillators | two distinct fixed $\Theta_j$ and polynomial amplitudes |
| oscillator plus QH nuisance | oscillator block plus linear-$T$ block |

Published Hansen and Laurenti coefficients remain evaluated through `gap_models.py`; they are not refitted automatically.

## Why oscillator scales are fixed

Conditional on $\Theta_j$, the coefficient problem is linear and its rank, singular values, covariance, and held-out predictions are auditable.

If $\Theta_j$ are optimized using all observations before cross-validation, information from the held-out data leaks into the model. Therefore:

1. use physically predeclared scales; or
2. select scales using only the training portion of every outer fold; or
3. use nested cross-validation.

A lower in-sample residual from freely adjusted oscillator temperatures is not an admissible model-selection result.

## Equality-constrained weighted fit

The implementation solves

$$
\min_{\boldsymbol\beta}
\left\|
W^{1/2}(\mathbf y-X\boldsymbol\beta)
\right\|_2^2
$$

subject to

$$
A\boldsymbol\beta=\mathbf b.
$$

It parameterizes the feasible set as

$$
\boldsymbol\beta
=\boldsymbol\beta_0+Z\boldsymbol\theta,
$$

where the columns of $Z$ span the null space of $A$. The reduced problem is solved only when the whitened design $W^{1/2}XZ$ has full column rank.

The fit fails closed on a rank-deficient free-parameter design rather than returning a pseudoinverse curve with unresolved parameters.

## Covariance outputs

Two covariance matrices are reported:

1. `covariance_known_sigma`: conditional on the supplied observation standard deviations being the complete noise model;
2. `covariance_scaled`: multiplied by the reduced chi-square as a model-discrepancy diagnostic.

For exact constraints,

$$
A\operatorname{Cov}(\boldsymbol\beta)=0
$$

up to numerical precision. Zero variance in a constrained direction is a statement about the imposed model, not empirical certainty.

Neither covariance currently includes latent composition, source offset, measurement-class offset, digitization covariance, or model-selection uncertainty. Those must be added at the outer benchmark level.

## Leakage-safe holdouts

The core supports:

- leave-one-group-out prediction;
- arbitrary named, nonoverlapping holdout masks;
- low-, intermediate-, and high-temperature masks;
- source-level or measurement-class masks after the data schema is complete.

Repeated temperatures from one specimen must use one common group label. The fitting layer does not split a specimen automatically.

## Metrics

Residuals are defined as

$$
r_i=E_{g,i}^{\mathrm{observed}}-E_{g,i}^{\mathrm{predicted}}.
$$

The core reports in meV:

- signed mean residual;
- MAE;
- RMSE;
- maximum absolute error;
- inverse-variance-weighted versions of the first three metrics.

Wavelength metrics are deliberately absent from this layer because they become singular and asymmetric near $E_g=0$.

## Current validation

Synthetic tests cover:

- exact one-oscillator coefficient recovery;
- exact two-signed-oscillator recovery with a finite-temperature turnover;
- zero-temperature oscillator limits;
- endpoint and named coefficient constraints;
- covariance removal in constrained directions;
- the Hansen temperature-coefficient relation;
- leave-one-specimen-out prediction;
- temperature-range holdouts;
- rank-deficiency rejection;
- meV metric conventions.

Synthetic recovery verifies implementation algebra. It does not validate any HgCdTe oscillator temperature, composition degree, or physical interpretation.

## Activation gate for real fitting

Do not publish a model ranking until the benchmark contains enough provenance-controlled specimen series to support:

1. at least two independent held-out schemes;
2. specimen grouping;
3. composition uncertainty or a declared sensitivity analysis;
4. observable-class separation;
5. a training-only procedure for any oscillator-scale selection;
6. a comparison against published Hansen and Laurenti coefficients;
7. residual analysis in energy before wavelength conversion.

Until then, the executable core is infrastructure supporting the breadth-first evidence program, not a new HgCdTe bandgap result.
