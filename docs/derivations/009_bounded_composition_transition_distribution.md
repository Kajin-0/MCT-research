# Derivation 009: bounded composition quadrature and critical-temperature distributions

## Scope

Derivation 008 propagated a small composition standard deviation through a smooth signed-gap law using local derivatives. This note replaces that local approximation with deterministic quadrature over a Gaussian composition model conditioned on the physical interval

$$
0\le x\le1.
$$

The result provides:

1. exact numerical moments of the signed-gap distribution;
2. an explicit comparison with the second-order approximation;
3. the probability that exactly one critical-temperature crossing occurs inside a declared observation window;
4. conditional critical-temperature moments;
5. probabilities of no crossing or multiple crossings.

The assumed composition distribution is a declared metrology or specimen-state model. It is not inferred from nominal composition, Urbach energy, PL linewidth, or a topological measurement.

## 1. Physically bounded Gaussian composition model

Start from an unbounded Gaussian variable

$$
X_0\sim\mathcal N(\mu_x,\sigma_x^2).
$$

Condition it on the physical alloy interval:

$$
p_X(x)
=
\frac{
\phi\!\left((x-\mu_x)/\sigma_x\right)
}{
\sigma_x
\left[
\Phi\!\left((1-\mu_x)/\sigma_x\right)
-
\Phi\!\left(-\mu_x/\sigma_x\right)
\right]
},
\qquad 0\le x\le1.
$$

Here $\phi$ and $\Phi$ are the standard-normal density and cumulative distribution.

The conditioning matters when $\mu_x$ lies within a few $\sigma_x$ of either endpoint. The declared $\mu_x$ and $\sigma_x$ then differ from the effective moments of the bounded distribution.

For example,

$$
\mu_x=0.005,
\qquad
\sigma_x=0.010
$$

gives

$$
P(0\le X_0\le1)=0.69146246,
$$

$$
\mathbb E[X\mid0\le X\le1]=0.01009160,
$$

and

$$
\sigma_{X\mid[0,1]}=0.00697263.
$$

Therefore clipping values to the physical interval would be incorrect: clipping creates endpoint point masses, whereas conditioning changes the continuous density and its normalization.

## 2. Deterministic quadrature

Use the standardized coordinate

$$
z=\frac{x-\mu_x}{\sigma_x}.
$$

For any scalar response $f(x)$,

$$
\mathbb E[f(X)]
=
\frac{
\int_a^b f(\mu_x+\sigma_x z)\phi(z)\,dz
}{
\Phi(b)-\Phi(a)
},
$$

with

$$
a=-\frac{\mu_x}{\sigma_x},
\qquad
b=\frac{1-\mu_x}{\sigma_x}.
$$

The implementation uses Gauss-Legendre quadrature in $z$ over

$$
[\max(a,-z_{\max}),\min(b,z_{\max})]
$$

with default $z_{\max}=8$. The omitted normalized Gaussian tail is retained as a diagnostic. For the near-critical screens in this note it is below numerical relevance.

## 3. Exact signed-gap moments

For a latent law

$$
G=E_g(X,T),
$$

the quadrature computes

$$
\mu_G=\mathbb E[G],
$$

$$
\sigma_G^2=\mathbb E[(G-\mu_G)^2],
$$

and

$$
\gamma_G
=
\frac{
\mathbb E[(G-\mu_G)^3]
}{
\sigma_G^3
}.
$$

These are compared directly with the local approximations

$$
\mu_G^{(2)}
=
E_g(\mu_x,T)
+
\frac12E_{g,xx}(\mu_x,T)\sigma_x^2,
$$

and

$$
\sigma_G^{(1)}
=
|E_{g,x}(\mu_x,T)|\sigma_x.
$$

The reported approximation errors are

$$
\delta\mu_G
=
\mu_G-\mu_G^{(2)},
$$

and

$$
\delta\sigma_G
=
\sigma_G-\sigma_G^{(1)}.
$$

## 4. Gap-sign probabilities

For zero tolerance, the implementation finds composition roots of

$$
E_g(x,T)=0
$$

on $0\le x\le1$, divides the interval at those roots, classifies each open interval by the sign at its midpoint, and integrates the bounded Gaussian probability analytically over the interval.

This avoids estimating a sharp sign probability from sparsely spaced quadrature nodes.

The outputs are

$$
P(G<0),
\qquad
P(G=0),
\qquad
P(G>0).
$$

For a continuous composition distribution, an isolated exact root has zero probability. A finite near-zero probability requires a declared nonzero energy tolerance and then becomes an observation-scale quantity.

These sign probabilities do not define a bulk $\mathbb Z_2$ invariant.

## 5. Critical-temperature transformation

For every quadrature composition node $x_i$, search the declared interval

$$
T_{\min}\le T\le T_{\max}
$$

for roots of

$$
E_g(x_i,T)=0.
$$

Each composition node is assigned to exactly one category:

1. **single crossing** — one root in the interval;
2. **always normal** — no root and $E_g>0$ throughout the sampled interval;
3. **always inverted** — no root and $E_g<0$ throughout the sampled interval;
4. **multiple crossing** — more than one root;
5. **unresolved** — none of the above.

Only single-crossing nodes contribute to the conditional critical-temperature moments:

$$
\mathbb E[T_c\mid\text{one crossing}],
$$

$$
\sigma_{T_c\mid\text{one crossing}},
$$

and conditional skewness.

The crossing probability

$$
P_{1c}=P(\text{exactly one crossing in the window})
$$

must be reported with those moments.

## 6. Local approximation at the central composition

When the mean composition has exactly one root $T_c(\mu_x)$, the implicit-function approximation is

$$
\sigma_{T_c}^{(1)}
=
\left|
\frac{E_{g,x}}{E_{g,T}}
\right|_{(\mu_x,T_c)}
\sigma_x.
$$

The exact conditional distribution is compared through

$$
\delta\bar T_c
=
\mathbb E[T_c\mid1c]-T_c(\mu_x),
$$

and

$$
\delta\sigma_{T_c}
=
\sigma_{T_c\mid1c}-\sigma_{T_c}^{(1)}.
$$

A large discrepancy may arise from nonlinear transformation, physical composition truncation, or censoring by the declared temperature window. These mechanisms must not be conflated.

## 7. Near-critical three-law screen

Use

$$
\mu_x=0.155,
\qquad
0\le T\le300\ \mathrm K,
$$

and compare three existing repository laws:

1. reconstructed Laurenti;
2. Hansen-Schmit-Casselman;
3. archived provisional Hansen-Padé.

No model prior is assigned and no universal law is selected.

### Central critical temperatures

| Latent law | $T_c(0.155)$ |
|---|---:|
| Laurenti | 77.1241 K |
| Hansen | 52.0438 K |
| provisional Hansen-Padé | 52.5937 K |

The central model span is

$$
\boxed{25.0803\ \mathrm K}.
$$

The Hansen and provisional Padé values differ by only

$$
0.5498\ \mathrm K,
$$

while both differ strongly from Laurenti at this nominal composition.

## 8. High-precision composition scenario: $\sigma_x=0.001$

| Latent law | $P_{1c}$ | conditional mean $T_c$ | exact $\sigma_{T_c}$ | local $\sigma_{T_c}^{(1)}$ | width error |
|---|---:|---:|---:|---:|---:|
| Laurenti | 1.000000 | 77.0972 K | 4.46435 K | 4.46214 K | +0.00221 K |
| Hansen | 1.000000 | 52.0318 K | 4.55975 K | 4.55961 K | +0.00014 K |
| provisional Padé | 1.000000 | 52.5974 K | 3.80408 K | 3.80512 K | -0.00104 K |

The local approximation is effectively exact at this scale:

$$
\max|\delta\sigma_{T_c}|=0.00221\ \mathrm K.
$$

However, the latent-law central-temperature span is approximately 5.5–6.6 times the composition-induced standard deviation.

### Result A

> At $\sigma_x=0.001$, nonlinear propagation is not the limiting uncertainty. The unresolved latent-law choice dominates the predicted critical temperature.

This does not select a law. It identifies which uncertainty source controls the calculation.

## 9. Intermediate scenario: $\sigma_x=0.005$

| Latent law | $P_{1c}$ | always normal | conditional mean $T_c$ | exact $\sigma_{T_c}$ | local width error |
|---|---:|---:|---:|---:|---:|
| Laurenti | 0.996439 | 0.003561 | 76.6301 K | 22.2899 K | -0.0208 K |
| Hansen | 0.986951 | 0.013049 | 52.5419 K | 21.8538 K | -0.9442 K |
| provisional Padé | 0.986951 | 0.013049 | 53.2412 K | 18.3449 K | -0.6807 K |

The composition-induced width is now

$$
18.34\text{–}22.29\ \mathrm K,
$$

which is comparable to the 25.08 K central model span.

A finite portion of the composition model has no transition inside 0–300 K and remains normal throughout the window.

### Result B

> Near $\sigma_x=0.005$, composition-distribution uncertainty and latent-law uncertainty are comparably important. Conditional transition statistics begin to require explicit no-crossing probability.

## 10. Broad scenario: $\sigma_x=0.010$

| Latent law | $P_{1c}$ | always normal | conditional mean shift | exact conditional $\sigma_{T_c}$ | local width error |
|---|---:|---:|---:|---:|---:|
| Laurenti | 0.913966 | 0.086034 | +5.5170 K | 37.9403 K | -6.6812 K |
| Hansen | 0.858810 | 0.141190 | +11.0501 K | 35.9386 K | -9.6575 K |
| provisional Padé | 0.858810 | 0.141190 | +9.8254 K | 30.6204 K | -7.4308 K |

At this width, 8.6–14.1% of the bounded Gaussian composition model remains normal throughout 0–300 K. The conditional root distribution is therefore censored: high-composition regions without a root are absent from its temperature moments.

The local implicit-function width overestimates the conditional exact width by 6.68–9.66 K, while the conditional mean shifts upward by 5.52–11.05 K.

### Result C

> At $\sigma_x=0.010$, reporting only $T_c(\mu_x)\pm|dT_c/dx|\sigma_x$ is materially misleading. The transition-in-window probability and conditional-distribution shift are required.

## 11. Recoverability interpretation

The calculation separates three regimes.

### Regime I — local and law-limited

For small $\sigma_x$:

- the derivative approximation is accurate;
- every composition realization crosses inside the window;
- latent-law disagreement dominates.

At $\mu_x=0.155$, $\sigma_x=0.001$ lies in this regime.

### Regime II — distribution and law co-limited

At intermediate $\sigma_x$:

- exact and local widths remain similar;
- composition width is comparable to model spread;
- a small no-crossing probability appears.

The $\sigma_x=0.005$ screen lies near this regime.

### Regime III — censored and nonlinear

At broad $\sigma_x$:

- a substantial probability has no transition in the observation window;
- conditional moments shift and narrow relative to the local Gaussian approximation;
- the crossing probability becomes indispensable.

The $\sigma_x=0.010$ screen lies in this regime.

## 12. Significance for the flagship paper

This result strengthens the Paper I conclusion constructively:

1. composition uncertainty cannot always be represented by a single propagated error bar;
2. latent-law uncertainty and composition-distribution uncertainty dominate in different regimes;
3. the experiment's observation window changes the reported transition distribution;
4. a conditional $T_c$ mean and width are incomplete without crossing probability;
5. temperature tuning is not merely convenient—it avoids part of the inversion problem created by imprecise composition tuning.

The result is suitable for the flagship paper as an analytical and computational section, but it is not yet an experimental validation of a specific $\sigma_x$ for the Teppe specimens.

## 13. Validation and falsification

The implementation includes tests for:

- exact linear Gaussian transformations;
- quadratic mean and variance;
- endpoint-conditioned composition moments;
- exact linear critical-temperature transformation;
- no-crossing classification;
- multiple-root retention;
- the Teppe/Laurenti local limit;
- invalid bounds and quadrature settings.

The result must be revised if:

1. quadrature-order refinement changes manuscript values materially;
2. the root-grid resolution misses a decision-changing multiple root;
3. a measured composition distribution is strongly non-Gaussian;
4. spatial correlation, percolation, or domain coupling changes the observable relative to independent local-gap averaging;
5. a magneto-optical forward model shows that fitted Kane mass responds differently from the scalar local signed gap.

## 14. Claim restrictions

Do not claim:

- that the chosen $\sigma_x$ values describe the actual Teppe specimens;
- that no-crossing probability is a measured normal-phase volume fraction;
- that local sign fractions determine a bulk topological invariant;
- that model spread is a Bayesian credible interval;
- that Laurenti, Hansen, or the provisional Padé law is selected by this sensitivity analysis;
- that a scalar gap-root distribution reproduces magneto-optical fitting without an explicit observation operator.
