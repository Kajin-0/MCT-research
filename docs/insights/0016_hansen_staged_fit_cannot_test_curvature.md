# Insight 0016 — Hansen's staged regression cannot test temperature curvature

**Status:** exact consequence of the published fitting procedure.  
**Novelty status:** methodological reconstruction, not a new HgCdTe bandgap law.  
**Use:** determine which historical data must be recovered before fitting phonon-based models.

## 1. Published reduction

For each specimen with temperature-dependent data, Hansen et al. first replaced the raw series

$$
\{T_{ij},E_{ij}\}_{i=1}^{n_j}
$$

by a linear regression

$$
E_j(T)\approx a_j+s_jT.
$$

The slopes $s_j$ were then fitted as one linear function of composition, and each specimen was normalized to 80 K before the composition polynomial was fitted.

Thus the final equation was not fitted directly to the complete raw $(x,T,E_g)$ cloud.

## 2. Information discarded by the first stage

Suppose the actual specimen-level law contains quadratic curvature:

$$
E_j(T)=A_j+B_jT+C_jT^2.
$$

Let

$$
\bar T_j=\frac1{n_j}\sum_iT_{ij},
$$

and define central moments

$$
\mu_{2,j}=\frac1{n_j}\sum_i(T_{ij}-\bar T_j)^2,
\qquad
\mu_{3,j}=\frac1{n_j}\sum_i(T_{ij}-\bar T_j)^3.
$$

The ordinary-least-squares linear slope is

$$
\boxed{
\hat s_j
=B_j+C_j\left(
2\bar T_j+\frac{\mu_{3,j}}{\mu_{2,j}}
\right).
}
$$

Therefore curvature is not estimated as curvature. It is aliased into a sample-window-dependent linear slope.

Two specimens having the same physical $B_j$ and $C_j$ but different temperature grids can produce different fitted slopes.

## 3. Bias in the normalized 80 K value

Let $T_0=80\ \mathrm K$. The value predicted at $T_0$ by the specimen-level linear regression differs from the true quadratic value by

$$
\boxed{
\hat E_j(T_0)-E_j(T_0)
=C_j\left[
\mu_{2,j}-(T_0-\bar T_j)^2
+(T_0-\bar T_j)\frac{\mu_{3,j}}{\mu_{2,j}}
\right].
}
$$

For a temperature grid symmetric about its mean, $\mu_3=0$, so

$$
\hat E_j(T_0)-E_j(T_0)
=C_j\left[
\mu_2-(T_0-\bar T)^2
\right].
$$

Even the normalized 80 K point can therefore inherit a curvature-dependent bias whose sign and magnitude depend on the sampled temperature window.

## 4. Consequence for the reported 13 meV standard error

The reported standard error of estimate

$$
13\ \mathrm{meV}
$$

measures agreement of the final empirical expression with the historical reduced and mixed-observable evidence. It is not a direct test of whether

$$
\frac{\partial^2E_g}{\partial T^2}=0.
$$

The staged procedure assumed a linear specimen-level temperature law before the global composition equation was constructed. The fit cannot independently validate the assumption it imposed during data reduction.

## 5. Source-count reconstruction

Hansen states that 22 studies were used. The citation graph contains only 21 numbered data references because Ref. 6 contains two independent private datasets:

- Rawe photoconductors;
- Tobin photodiodes.

The exact count is

$$
4\ \text{published sources in Refs. 1--4}
+2\ \text{private datasets in Ref. 6}
+14\ \text{magneto-optical sources in Refs. 7--20}
+2\ \text{binary endpoints in Refs. 24--25}
=22.
$$

Ref. 5 is a comparison equation rather than fitted data. Refs. 21--23 support composition calibration rather than gap observations.

## 6. Reconstruction priority

To test Hansen against one- or two-oscillator laws, recovering only the 80 K normalized points is insufficient. The required object is the raw specimen-level series:

$$
\{x_j,T_{ij},E_{ij},\text{observable class},\sigma_x,\sigma_E\}.
$$

Priority should therefore be assigned to sources that provide:

1. multiple temperatures on the same specimen;
2. independently measured composition;
3. a stable operational gap definition;
4. enough points below roughly 50 K to resolve curvature or turnover;
5. explicit uncertainty or sufficiently clear figures for calibrated digitization.

## 7. Model-selection implication

A new analytical model must not be credited for recovering curvature from data that were already linearly compressed by Hansen. The valid comparison is:

- fit all candidate models to reconstructed raw series;
- preserve specimen grouping and one latent composition per specimen;
- hold out complete specimens or temperature ranges;
- compare in meV before wavelength conversion.

Until the raw series are recovered, Hansen's 13 meV error is a historical engineering accuracy statement, not an information limit on physically constrained nonlinear models.
