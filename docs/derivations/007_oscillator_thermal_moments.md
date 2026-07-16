# Derivation 007: thermal moments are identifiable before oscillator energies

## Scope

Consider a thermal gap correction represented by fixed Bose occupation scales:

$$
\Delta E(T)
=
\sum_{j=1}^{J}
A_j
\left[
\coth\left(\frac{\Theta_j}{2T}\right)-1
\right]
=
2\sum_{j=1}^{J}
\frac{A_j}{\exp(\Theta_j/T)-1}.
$$

The amplitudes may depend on composition, but composition is suppressed temporarily for clarity.

This derivation asks what combinations of $A_j$ and $\Theta_j$ are actually constrained by finite-temperature data. It does not assert that fitted oscillator scales are literal phonon modes.

## 1. High-temperature expansion

Let

$$
z_j=\frac{\Theta_j}{2T}.
$$

For $|z_j|<\pi$,

$$
\coth z_j
=
\frac{1}{z_j}
+
\frac{z_j}{3}
-
\frac{z_j^3}{45}
+
\frac{2z_j^5}{945}
+\cdots.
$$

Therefore

$$
\coth\left(\frac{\Theta_j}{2T}\right)-1
=
\frac{2T}{\Theta_j}
-1
+
\frac{\Theta_j}{6T}
-
\frac{\Theta_j^3}{360T^3}
+
\frac{\Theta_j^5}{15120T^5}
+\cdots.
$$

Define signed thermal moments

$$
\mu_p
=
\sum_{j=1}^{J}A_j\Theta_j^p.
$$

The index $p$ may be negative. Substitution gives

$$
\boxed{
\Delta E(T)
=
2T\mu_{-1}
-
\mu_0
+
\frac{\mu_1}{6T}
-
\frac{\mu_3}{360T^3}
+
\frac{\mu_5}{15120T^5}
+
\cdots
}.
$$

The leading high-temperature slope is therefore

$$
\boxed{
\frac{d\Delta E}{dT}
\longrightarrow
2\mu_{-1}
=
2\sum_j\frac{A_j}{\Theta_j}
}.
$$

High-temperature data constrain this inverse-scale moment directly. They do not separately determine every $A_j$ and $\Theta_j$.

## 2. Composition-dependent amplitudes

Let each amplitude be a polynomial or another linear basis expansion:

$$
A_j(x)=\sum_{m=0}^{M}a_{jm}\phi_m(x).
$$

Then every thermal moment has the same composition basis:

$$
\mu_p(x)
=
\sum_m
\left(
\sum_j a_{jm}\Theta_j^p
\right)
\phi_m(x).
$$

The moment coefficients are

$$
\boxed{
\mu_{p,m}
=
\sum_j a_{jm}\Theta_j^p
}.
$$

Consequently, two different scale-amplitude decompositions can generate nearly identical observable moment polynomials.

## 3. Why two-scale fits become ill-conditioned

For two scales, the high-temperature columns are approximately

$$
b_j(T)
\approx
\frac{2T}{\Theta_j}-1+\frac{\Theta_j}{6T}.
$$

If the sampled temperatures do not resolve the $1/T$ and higher terms, both oscillator columns lie approximately in the span of

$$
\{T,1\}.
$$

The fit can then exchange amplitude between the two columns while preserving

$$
\mu_{-1}
=
\frac{A_1}{\Theta_1}
+
\frac{A_2}{\Theta_2}
$$

and, less tightly, $\mu_0=A_1+A_2$.

This produces:

- large condition numbers;
- strongly correlated amplitudes;
- fold-dependent selected scales;
- stable predictions despite unstable physical interpretation.

The problem is structural, not necessarily a numerical-solver defect.

## 4. Low-temperature information

At low temperature,

$$
\frac{2}{\exp(\Theta_j/T)-1}
=
2e^{-\Theta_j/T}
\left[
1+e^{-\Theta_j/T}+e^{-2\Theta_j/T}+\cdots
\right].
$$

Thus

$$
\Delta E(T)
\sim
2\sum_j A_j e^{-\Theta_j/T}.
$$

Individual scales become distinguishable only when the data include sufficiently precise temperatures for which their exponential activations differ appreciably.

A high scale satisfying

$$
\Theta_j\gg T_{\max}^{\mathrm{low}}
$$

is nearly invisible in the low-temperature data. Conversely, if low-temperature points are absent, the constant and inverse-temperature moments can trade strongly against the static gap term and each other.

## 5. Identifiability hierarchy

The natural hierarchy is therefore:

1. **prediction envelope** over the measured temperature range;
2. **leading moment** $\mu_{-1}(x)$ or high-temperature slope;
3. **next moments** $\mu_0(x)$ and $\mu_1(x)$ when curvature and the zero-temperature anchor support them;
4. **individual scales and amplitudes** only after the moment representation is insufficient and low-temperature data resolve the exponentials.

A model should not jump directly from stable predictions to claims of identified phonon energies.

## 6. Moment-based analytical alternative

Over a declared high-temperature interval, one may fit

$$
\Delta E(T)
\approx
2T\mu_{-1}
-
\mu_0
+
\frac{\mu_1}{6T}
$$

instead of fitting individual oscillators.

This is a controlled asymptotic representation only when

$$
\max_j\frac{\Theta_j}{2T}
$$

is sufficiently small over the fitted interval. It must not be extrapolated to $T=0$, where the truncated moment expansion is singular while the exact Bose model vanishes.

A practical global model may combine:

- the exact one-scale Bose basis as a parsimonious low-temperature form;
- a small number of constrained moment corrections;
- or a positive/negative spectral density represented by regularized moments rather than freely moving discrete scales.

## 7. Falsification rule

Individual oscillator scales are physically identified only if:

1. their uncertainty regions exclude broad alternative scale pairs;
2. they remain stable across composition, temperature, and source holdouts;
3. the corresponding moments alone cannot explain the predictions;
4. low-temperature data resolve distinct exponential activation;
5. the inferred scales are compatible with an independently calculated or measured coupling spectrum.

Otherwise the defensible output is a moment or prediction envelope.
