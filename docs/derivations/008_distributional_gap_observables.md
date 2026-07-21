# Derivation 008: distributional signed-gap propagation and transition width

## Scope

This derivation extends the ideal random-alloy width result to a general smooth signed-gap law

$$
E_g(x,T).
$$

It separates three quantities that are often conflated:

1. the gap evaluated at the mean composition;
2. the mean of the local gap distribution;
3. the width of the local gap distribution.

The derivation also gives the first-order width of a composition-tuned critical temperature. It does not identify an optical Urbach energy, photoluminescence linewidth, quasiparticle lifetime broadening, or a topological invariant.

## 1. Composition distribution

Let the local or specimen-level Cd fraction be

$$
X=\bar x+\delta x,
$$

with

$$
\mathbb E[\delta x]=0,
\qquad
\mathbb E[\delta x^2]=\sigma_x^2.
$$

The interpretation of $\sigma_x$ must be declared. It may represent metrology uncertainty, lateral variation, depth variation, or a coarse-grained local alloy distribution. These are not interchangeable physical quantities.

## 2. Second-order mean-gap shift

Expand the signed gap about $\bar x$:

$$
E_g(X,T)
=
E_g(\bar x,T)
+
E_{g,x}\delta x
+
\frac12 E_{g,xx}\delta x^2
+
\mathcal O(\delta x^3).
$$

Taking the expectation gives

$$
\boxed{
\mathbb E[E_g(X,T)]
\approx
E_g(\bar x,T)
+
\frac12 E_{g,xx}(\bar x,T)\sigma_x^2
}.
$$

Therefore

$$
\mathbb E[E_g(X,T)]
\neq
E_g(\mathbb E[X],T)
$$

when the composition dependence is curved.

Define the curvature bias

$$
\boxed{
\Delta E_{\mathrm{curv}}
=
\frac12 E_{g,xx}\sigma_x^2
}.
$$

For a strictly linear gap law, $E_{g,xx}=0$ and the bias vanishes exactly.

## 3. First-order local-gap width

At leading order,

$$
E_g(X,T)-\mathbb E[E_g]
\approx
E_{g,x}\delta x.
$$

Hence

$$
\boxed{
\sigma_{E,x}
\approx
|E_{g,x}(\bar x,T)|\sigma_x
}.
$$

This equation is a propagation law. It does not assert that $\sigma_{E,x}$ is equal to an experimental tail parameter.

## 4. Local opposite-sign probability

If the propagated local gap is approximated as Gaussian,

$$
G\sim\mathcal N(\mu_G,\sigma_G^2),
$$

with

$$
\mu_G
=
E_g(\bar x,T)+\Delta E_{\mathrm{curv}},
\qquad
\sigma_G=\sigma_{E,x},
$$

then the fraction of local regions with sign opposite to the mean is

$$
\boxed{
p_{\mathrm{opp}}
=
\frac12
\operatorname{erfc}
\left(
\frac{|\mu_G|}{\sqrt2\sigma_G}
\right)
}.
$$

At $|\mu_G|/\sigma_G=1$, $p_{\mathrm{opp}}=0.1587$. At 2 and 3 standard deviations the corresponding fractions are 0.0228 and 0.00135.

This is a local sign statistic under the assumed distribution. It is not a $\mathbb Z_2$ invariant and does not determine bulk transport.

## 5. Critical-temperature uncertainty

Define a local critical temperature through

$$
E_g(X,T_c(X))=0.
$$

Near a reference point $(\bar x,\bar T_c)$ satisfying

$$
E_g(\bar x,\bar T_c)=0,
$$

the implicit-function theorem gives

$$
E_{g,x}\,d x
+
E_{g,T}\,dT_c
=0.
$$

Therefore

$$
\frac{dT_c}{dx}
=-
\frac{E_{g,x}}{E_{g,T}},
$$

and composition variation produces

$$
\boxed{
\sigma_{T_c}
\approx
\left|
\frac{E_{g,x}}{E_{g,T}}
\right|
\sigma_x
}.
$$

This expression exposes two amplification mechanisms:

1. large $|E_{g,x}|$, characteristic of HgCdTe;
2. small $|E_{g,T}|$, which makes temperature tuning weak relative to composition variation.

The approximation fails where $E_{g,T}=0$, where higher-order terms dominate, or where a unique local critical temperature does not exist.

## 6. Teppe/Laurenti near-critical screen

Use the reconstructed Laurenti law at

$$
\bar x=0.155,
\qquad
T=77\ \mathrm K.
$$

The executable central-difference calculation gives

$$
E_g=-4.7812\times10^{-5}\ \mathrm{eV},
$$

$$
E_{g,x}=1.7191085\ \mathrm{eV},
$$

$$
E_{g,xx}=0.4711102\ \mathrm{eV},
$$

and

$$
E_{g,T}=3.8517802\times10^{-4}\ \mathrm{eV/K}.
$$

### Case A: $\sigma_x=0.001$

$$
\Delta E_{\mathrm{curv}}
=2.36\times10^{-7}\ \mathrm{eV}
=0.000236\ \mathrm{meV},
$$

$$
\sigma_{E,x}=1.7191\ \mathrm{meV},
$$

$$
\sigma_{T_c}=4.4632\ \mathrm K,
$$

and

$$
p_{\mathrm{opp}}=0.48896.
$$

The curvature correction is negligible at this width, but the propagated local-gap scale is much larger than the approximately zero mean gap.

### Case B: $\sigma_x=0.005$

$$
\Delta E_{\mathrm{curv}}=0.00589\ \mathrm{meV},
$$

$$
\sigma_{E,x}=8.5955\ \mathrm{meV},
$$

$$
\sigma_{T_c}=22.3158\ \mathrm K,
$$

and

$$
p_{\mathrm{opp}}=0.49805.
$$

The result quantifies why composition is a poor fine-tuning coordinate near the transition unless the achieved composition distribution is independently constrained far below the usual historical uncertainty scale.

## 7. Interpretation hierarchy

The same algebra can be applied at different levels, but the meaning changes:

- **metrology level:** $\sigma_x$ is uncertainty in one specimen's mean composition;
- **specimen nonuniformity level:** $\sigma_x$ describes a measured lateral or depth distribution;
- **coarse-grained alloy level:** $\sigma_x$ describes local fluctuations over a declared volume;
- **source population level:** $\sigma_x$ describes variation among nominally similar specimens.

Only the first two can usually be connected directly to macroscopic published measurements without an atomistic model.

## 8. Connection to optical observables

An absorption or luminescence experiment generally reports a nonlinear functional of the local response:

$$
S_{\mathrm{obs}}(E)
=
\int p(g)S(E\mid g,\theta)\,dg.
$$

Applying an edge operator after this averaging gives

$$
E_{\mathrm{edge}}
=
\mathcal O[S_{\mathrm{obs}}],
$$

which is not generally equal to $\mu_G$ or $E_g(\bar x,T)$. This noncommutation is the central mathematical problem of the flagship program:

$$
\mathcal O
\left[
\int p(g)S(E\mid g)\,dg
\right]
\neq
\int p(g)\mathcal O[S(E\mid g)]\,dg.
$$

Herrmann's Gaussian-gap convolution and Chang's nonparabolic-Urbach model provide two source-specific routes for testing this statement.

## 9. Falsification tests

The second-order propagation is rejected or restricted when:

1. the result changes materially under derivative-step refinement;
2. $\sigma_x$ is large enough that third-order terms are non-negligible;
3. the composition distribution is strongly bounded, skewed, multimodal, or correlated in a way not represented by one variance;
4. the latent gap law is non-smooth over the support;
5. a full quadrature or measured composition map predicts materially different moments;
6. the target experiment responds to localization, percolation, or spectral self-energy rather than a local scalar gap.

## 10. Required reporting

Every use of this propagation must report:

- the latent gap law;
- $\bar x$, $T$, and the interpretation of $\sigma_x$;
- numerical derivative steps or analytical derivatives;
- $E_g(\bar x,T)$, $\Delta E_{\mathrm{curv}}$, and $\sigma_{E,x}$;
- $\sigma_{T_c}$ when $E_{g,T}\neq0$;
- whether $p_{\mathrm{opp}}$ is reported;
- a statement that the result is not automatically an optical width or topological invariant.
