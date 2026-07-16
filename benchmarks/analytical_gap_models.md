# Common analytical HgCdTe bandgap benchmark

**Status:** protocol defined; no model-ranking result yet  
**Dependency:** reconstructed and provenance-controlled experimental data  
**Primary residual unit:** meV

## 1. Objective

Compare analytical models using identical data partitions, uncertainty assumptions, and metrics. No model may use a different subset merely because it fits that subset better.

## 2. Required model family

### M0 — Reproduced Hansen baseline

$$
E_g(x,T)=
-0.302+1.93x-0.81x^2+0.832x^3
+5.35\times10^{-4}T(1-2x).
$$

Two scores are required:

1. published coefficients used without refitting;
2. same functional form refitted to the reconstructed common dataset.

This separates functional-form error from historical coefficient/data differences.

### M1 — Constrained low-order empirical model

A minimal composition polynomial with a low-order temperature coefficient:

$$
E_g(x,T)=P_m(x)+TQ_n(x),
$$

where $m$ and $n$ are chosen by nested validation, not by in-sample residual alone.

Constraints may include:

- endpoint consistency;
- smoothness over $0\le x\le1$;
- physically defensible sign or monotonicity only where supported by data;
- no unnecessary terms with unresolved covariance.

### M2 — One-effective-oscillator model

$$
E_g(x,T)=E_g(x,0)
+A(x)\left[
\coth\left(\frac{\Theta(x)}{2T}\right)-1
\right].
$$

The reference $E_g(x,0)$ includes zero-point renormalization. $A(x)$ and $\Theta(x)$ must use a constrained composition representation.

### M3 — Two-oscillator or spectral-moment model

$$
E_g(x,T)=E_g(x,0)
+\sum_{j=1}^{2} A_j(x)
\left[
\coth\left(\frac{\Theta_j(x)}{2T}\right)-1
\right].
$$

The second oscillator is accepted only if it improves held-out performance and is identifiable. A spectral-moment equivalent may replace explicit oscillators if it has fewer or better-conditioned parameters.

### M4 — Optional quasiharmonic extension

$$
E_g^{\mathrm{total}}(x,T)
=E_g^{\mathrm{fixed\ volume}}(x,T)
+\Delta E_g^{\mathrm{QH}}(x,T).
$$

This term is included only when independent thermal-expansion and deformation-potential information is available or when it is explicitly treated as a separately uncertain component.

### M5 — Optional disorder-width model

The mean gap remains distinct from a width parameter:

$$
E_g\sim\mathcal D\left(\mu_g(x,T),\sigma_g(x,T)\right).
$$

The width must be fitted to an observable sensitive to broadening; it may not be inferred from mean-gap residuals alone.

## 3. Data hierarchy

Each datum receives a level:

- `A`: primary numerical table with stated uncertainty;
- `B`: primary figure digitization with calibrated digitization uncertainty;
- `C`: secondary reproduction traceable to a primary source;
- `D`: engineering formula or uncited compilation.

Primary benchmark scores use levels A and B. C and D are sensitivity/legacy comparisons, not equal-status observations.

## 4. Validation splits

### Leave-one-composition-out

For each distinct composition group $x_j$:

1. fit on all other composition groups;
2. predict all temperatures at $x_j$;
3. retain the complete residual vector.

Composition groups must account for reported $\sigma_x$ and repeated measurements on the same specimen.

### Held-out temperature ranges

At minimum:

- low-temperature holdout;
- intermediate-temperature holdout;
- high-temperature holdout.

Exact boundaries are selected from the recovered data distribution before model fitting. Repeated temperatures from the same sample remain grouped to prevent leakage.

### Source-level holdout

When multiple papers contribute data, hold out complete source datasets. This tests transfer across measurement methods and laboratories rather than interpolation within one publication.

## 5. Metrics

All primary metrics are calculated in energy:

$$
\mathrm{MAE}_{E}=\frac1N\sum_i|r_i|,
\qquad
\mathrm{MaxAE}_{E}=\max_i|r_i|.
$$

Report:

- weighted and unweighted MAE in meV;
- maximum absolute error in meV;
- RMSE in meV;
- signed mean residual;
- residual versus $x$;
- residual versus $T$;
- residual autocorrelation within repeated-temperature series;
- source-specific residuals;
- parameter covariance and correlation;
- effective degrees of freedom;
- singular values or identifiability diagnostics.

### Critical composition

For each $T$ solve

$$
E_g(x_c,T)=0.
$$

Report

$$
\Delta x_c(T)=x_c^{\mathrm{model}}(T)-x_c^{\mathrm{reference}}(T).
$$

### Critical temperature

For each applicable $x$ solve

$$
E_g(x,T_c)=0
$$

and report $\Delta T_c$.

### Equivalent wavelength error

Report only where $E_g$ is safely nonzero and after energy metrics:

$$
\Delta\lambda_i=
\frac{hc}{E_{g,i}^{\mathrm{model}}}
-
\frac{hc}{E_{g,i}^{\mathrm{reference}}}.
$$

Do not average wavelength errors across the zero-gap region.

## 6. Model-selection rules

A more complicated model advances only if:

1. it improves at least two independent held-out schemes;
2. improvement exceeds uncertainty from data reconstruction;
3. parameters remain identifiable across folds;
4. residual structure is reduced rather than merely redistributed;
5. endpoint and limiting behavior remain defensible;
6. the improvement is not driven by one source or one composition.

A two-oscillator model with unconstrained or fold-unstable oscillator temperatures is rejected even if its in-sample error is lower.

## 7. Reporting table

| Model | Parameters | In-sample MAE (meV) | LOCO MAE | Temperature-holdout MAE | Max error | $x_c$ error | $T_c$ error | Identifiable? |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| M0 Hansen published | 0 fitted | pending | pending | pending | pending | pending | pending | n/a |
| M0 Hansen refit | pending | pending | pending | pending | pending | pending | pending | pending |
| M1 constrained empirical | pending | pending | pending | pending | pending | pending | pending | pending |
| M2 one oscillator | pending | pending | pending | pending | pending | pending | pending | pending |
| M3 two oscillator/moments | pending | pending | pending | pending | pending | pending | pending | pending |
| M4 + quasiharmonic | pending | pending | pending | pending | pending | pending | pending | pending |
| M5 + disorder width | pending | pending | pending | pending | pending | pending | pending | pending |

## 8. Stop condition

If the one-oscillator or spectral-moment model does not improve held-out energy error beyond reconstructed experimental uncertainty, the project should not claim a superior universal analytical equation. The useful result may instead be:

- a quantified validity range for Hansen;
- a corrected uncertainty model;
- a low-temperature-only extension;
- or proof that measurement-definition heterogeneity dominates functional-form error.
