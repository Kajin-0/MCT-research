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

Each datum also receives a measurement class:

- `optical_absorption_edge`;
- `two_photon_magnetoabsorption`;
- `Landau_level_Kane_gap`;
- `transport_inferred_gap`;
- `photoluminescence_or_other`;
- `model_derived`.

Measurement classes are not pooled without either demonstrating compatibility or including a class-dependent offset/uncertainty term. A detector cutoff, an extrapolated absorption edge, and a signed $\Gamma_6-\Gamma_8$ magneto-optical gap are not assumed identical.

## 4. Composition, source, and measurement uncertainty

### 4.1 Composition is an uncertain explanatory variable

Near detector-relevant and inversion compositions,

$$
\left|\frac{\partial E_g}{\partial x}\right|
\sim1\text{–}2\ \mathrm{eV},
$$

so a third-decimal composition error can create meV-scale or larger gap errors. Reported $x$ must not be treated as exact merely because a paper gives three digits.

For a datum with reported composition uncertainty,

$$
x_i^{\mathrm{true}}
\sim
\mathcal N(x_i^{\mathrm{reported}},\sigma_{x,i}^2).
$$

The observation model is

$$
E_{g,i}^{\mathrm{obs}}
\sim
\mathcal N\!\left(
E_g(x_i^{\mathrm{true}},T_i)+b_{s(i)}+b_{m(i)},
\sigma_{E,i}^2+\sigma_{\mathrm{digit},i}^2
\right),
$$

where $b_{s(i)}$ is a source/laboratory offset and $b_{m(i)}$ is an optional measurement-class offset.

### 4.2 Missing composition uncertainty

If a source does not report $\sigma_x$, use one of three declared treatments:

1. infer a source-level latent offset $\delta x_s$ with a sensitivity prior;
2. repeat the benchmark over a stated grid of plausible $\sigma_x$ or $\delta x_s$;
3. exclude the source from claims below its implied composition-error floor.

Never assign zero composition uncertainty by default.

### 4.3 Critical-point likelihood

A reported critical point $(x_r,T_c)$ constrains

$$
E_g(x^{\mathrm{true}},T_c)=0,
$$

not necessarily $E_g(x_r,T_c)=0$ exactly. The critical-temperature likelihood must integrate over composition uncertainty:

$$
p(T_c\mid x_r,M)
=
\int p\!\left(E_g(x,T_c)=0\mid M\right)
 p(x\mid x_r,\sigma_x)\,dx.
$$

A single nominal critical point cannot distinguish equation error from composition calibration error.

### 4.4 Source and specimen grouping

Repeated temperatures on one specimen share the same latent composition and source calibration. They are not independent composition measurements. All folds and bootstrap procedures must preserve specimen groups.

## 5. Validation splits

### Leave-one-composition-out

For each distinct composition/specimen group $x_j$:

1. fit on all other groups;
2. predict all temperatures at $x_j$;
3. retain the complete residual vector;
4. marginalize or profile over the held-out specimen's declared composition uncertainty without refitting a free offset to its observed gaps.

Composition groups must account for reported $\sigma_x$ and repeated measurements on the same specimen.

### Held-out temperature ranges

At minimum:

- low-temperature holdout;
- intermediate-temperature holdout;
- high-temperature holdout.

Exact boundaries are selected from the recovered data distribution before model fitting. Repeated temperatures from the same sample remain grouped to prevent leakage.

### Source-level holdout

When multiple papers contribute data, hold out complete source datasets. This tests transfer across measurement methods and laboratories rather than interpolation within one publication.

### Measurement-class holdout

Where enough data exist, fit optical-edge sources and predict magneto-optical signed-gap sources, then reverse the direction. Failure in this test identifies observable-definition mismatch rather than automatically proving incorrect temperature physics.

## 6. Metrics

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
- measurement-class residuals;
- inferred source composition offsets and their uncertainty;
- parameter covariance and correlation;
- effective degrees of freedom;
- singular values or identifiability diagnostics.

Two residual scores are required where composition is uncertain:

1. `nominal-x residual` using reported composition directly;
2. `composition-marginalized residual` after propagating only the declared composition uncertainty model.

A large improvement from score 1 to score 2 indicates composition calibration sensitivity, not necessarily a superior bandgap equation.

### Critical composition

For each $T$ solve

$$
E_g(x_c,T)=0.
$$

Report

$$
\Delta x_c(T)=x_c^{\mathrm{model}}(T)-x_c^{\mathrm{reference}}(T)
$$

with uncertainty from both the reference composition and the model.

### Critical temperature

For each applicable $x$ solve

$$
E_g(x,T_c)=0
$$

and report $\Delta T_c$ together with the composition-induced uncertainty in $T_c$.

### Equivalent wavelength error

Report only where $E_g$ is safely nonzero and after energy metrics:

$$
\Delta\lambda_i=
\frac{hc}{E_{g,i}^{\mathrm{model}}}
-
\frac{hc}{E_{g,i}^{\mathrm{reference}}}.
$$

Do not average wavelength errors across the zero-gap region.

## 7. Model-selection rules

A more complicated model advances only if:

1. it improves at least two independent held-out schemes;
2. improvement exceeds uncertainty from data reconstruction and composition calibration;
3. parameters remain identifiable across folds;
4. residual structure is reduced rather than merely redistributed;
5. endpoint and limiting behavior remain defensible;
6. the improvement is not driven by one source, one composition, or one measurement class;
7. it does not require implausibly large source-specific composition offsets.

A two-oscillator model with unconstrained or fold-unstable oscillator temperatures is rejected even if its in-sample error is lower.

## 8. Reporting table

| Model | Parameters | Nominal-$x$ MAE | Composition-marginalized MAE | LOCO MAE | Temperature-holdout MAE | Max error | $x_c$ error | $T_c$ error | Identifiable? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| M0 Hansen published | 0 fitted | pending | pending | pending | pending | pending | pending | pending | n/a |
| M0 Hansen refit | pending | pending | pending | pending | pending | pending | pending | pending | pending |
| M1 constrained empirical | pending | pending | pending | pending | pending | pending | pending | pending | pending |
| M2 one oscillator | pending | pending | pending | pending | pending | pending | pending | pending | pending |
| M3 two oscillator/moments | pending | pending | pending | pending | pending | pending | pending | pending | pending |
| M4 + quasiharmonic | pending | pending | pending | pending | pending | pending | pending | pending | pending |
| M5 + disorder width | pending | pending | pending | pending | pending | pending | pending | pending | pending |

## 9. Stop condition

If the one-oscillator or spectral-moment model does not improve held-out energy error beyond reconstructed experimental and composition uncertainty, the project should not claim a superior universal analytical equation. The useful result may instead be:

- a quantified validity range for Hansen;
- a corrected uncertainty model;
- a low-temperature-only extension;
- proof that composition or measurement-definition heterogeneity dominates functional-form error;
- or a recommendation for the minimum composition metrology required to discriminate models.