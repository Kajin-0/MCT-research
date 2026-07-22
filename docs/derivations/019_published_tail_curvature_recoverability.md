# Derivation 019: finite-window non-falsifiability and published-figure curvature recovery

## 1. Scope

This derivation belongs to R03, Issue #235. It uses the Gaussian-distributed power-edge operator from Issue #225:

$$
\alpha_p(E)=A\sigma_G^pF_p(z),
\qquad
z=\frac{E-\mu_G}{\sigma_G},
$$

with

$$
F_p(z)=\int_0^\infty t^p\phi(z-t)\,dt,
\qquad p\ge0.
$$

The question is narrower than mechanism identification:

> Can the finite, rasterized absorption plots in Finkman 1979 and 1984 resolve the negative logarithmic curvature predicted by this controlled operator?

The result is a recoverability limit, not a specimen fit.

## 2. Fixed finite dynamic range

Let the displayed absorption interval span

$$
R=\log_{10}\left(\frac{\alpha_{\max}}{\alpha_{\min}}\right)
$$

decades. For a declared upper standardized energy $z_2\le0$, define $z_1<z_2$ implicitly by

$$
\log_{10}F_p(z_2)-\log_{10}F_p(z_1)=R.
$$

The amplitude $A\sigma_G^p$ cancels. The finite-window lineshape is therefore determined by

$$
(p,R,z_2).
$$

The parameter $z_2$ is the location of the displayed upper absorption bound relative to the latent mean gap. A tail-only plot does not determine it unless the mean gap or intrinsic amplitude is independently anchored.

## 3. Deep-tail straightness theorem

From Derivation 016,

$$
\log F_p(z)
=
-\frac{z^2}{2}-(p+1)\log(-z)+C+O(z^{-2})
$$

as $z\to-\infty$. Let $z_2=-a$ with $a\to\infty$ and let

$$
\Delta=R\ln 10.
$$

The local logarithmic slope is

$$
\frac{d\log F_p}{dz}
=a+O(a^{-1}),
$$

so the standardized width required to span the fixed log range is

$$
 h=z_2-z_1
 =\frac{\Delta}{a}+O(a^{-3}).
$$

The logarithmic curvature tends to $-1$. The departure of a twice-differentiable function from its best affine approximation over an interval of width $h$ is $O(h^2)$. Therefore

$$
\boxed{
\epsilon_{\rm affine}
=O\left(\frac{\Delta^2}{a^2}\right)
=O(|z_2|^{-2})
}
$$

for every fixed finite $R$.

Consequently,

$$
\boxed{
\forall R<\infty,\ \forall\varepsilon>0,
\ \exists z_2<0
\text{ such that the Gaussian-power tail differs from a straight log plot by less than }\varepsilon.
}
$$

This is the controlling non-falsifiability statement:

> Straightness over a finite tail interval cannot reject Gaussian convolution when the standardized window location is unconstrained.

The theorem does not say the model is physically correct. It states that one visual property of a tail-only plot is insufficient to reject it.

## 4. Numerical straightness benchmark

For $p=1/2$ and the Finkman 1984 displayed range

$$
R=\log_{10}(1000/5)=2.30103,
$$

the controlled calculation gives:

| $z_2$ | $z_1$ | maximum vertical residual (decades) | maximum horizontal residual fraction |
|---:|---:|---:|---:|
| 0 | -2.64194 | 0.20297 | 0.10811 |
| -2 | -3.63024 | 0.08610 | 0.04174 |
| -4 | -5.09335 | 0.04073 | 0.01874 |
| -6 | -6.80010 | 0.02232 | 0.01002 |
| -8 | -8.62431 | 0.01375 | 0.00610 |

The residual decreases monotonically over this declared grid. Multiplying the horizontal residual fraction by $z_2^2$ approaches a constant, consistent with the $O(|z_2|^{-2})$ asymptotic.

## 5. Pixel-space observation operator

A published semilog trace is represented in pixel coordinates. Let

- $X$ be the empirical horizontal trace span in pixels;
- $Y$ be the vertical span of the selected absorption interval in pixels;
- $u$ be a declared marker-center uncertainty in pixels.

The model curve is mapped to

$$
(x_i,y_i)
=
\left[
X\frac{z_i-z_1}{z_2-z_1},
Y\frac{\log_{10}F_p(z_i)-\log_{10}F_p(z_1)}{R}
\right].
$$

A total-least-squares line is fitted to the pixel coordinates. The reported curvature signal is

$$
D_{\max}=\max_i d_{\perp,i},
$$

where $d_{\perp,i}$ is the orthogonal pixel departure from the best straight line.

The diagnostic ratio is

$$
\mathcal R=\frac{D_{\max}}{u}.
$$

The terms “one sigma” and “three sigma” below are scenario labels for $u$ and $3u$. The source papers do not provide a pixel-level covariance matrix.

## 6. Source-conditioned empirical trace spans

Finkman and Schacham 1984 give the modified-Urbach energy difference implied by their Eq. (10):

$$
\Delta E
=
\frac{T+81.9}{3.267\times10^4(1+x)}
\ln\left(\frac{\alpha_{\max}}{\alpha_{\min}}\right).
$$

Composition-dependent intercept and bowing terms cancel from the difference. This expression is used only to map each source line onto the audit-render horizontal pixel scale. It is not interpreted as a Gaussian-disorder law.

### Finkman and Schacham 1984, Figure 4

Declared audit geometry at 300 dpi:

```text
panel energy range:      0.20-0.30 eV
panel width:             545 px
absorption interval:     5-1000 cm^-1
vertical span:           562 px
center uncertainty:      6 px scenario
composition:             x=0.29
```

| temperature | trace span | horizontal span | departure if $z_2=0$ | critical $z_2$, $1u$ | critical $z_2$, $3u$ |
|---:|---:|---:|---:|---:|---:|
| 85 K | 20.982 meV | 114.354 px | 12.102 px | -1.455 | not reached for $z_2\le0$ |
| 300 K | 48.012 meV | 261.665 px | 25.510 px | -3.183 | -0.717 |

The low-temperature line cannot exceed an 18-pixel threshold anywhere in the controlled subgap domain, even if the upper plotted point coincides with the latent mean gap. The 300 K line exceeds 18 pixels only if

$$
z_2\gtrsim-0.72.
$$

### Finkman and Nemirovsky 1979, Figure 3

Declared audit geometry at 300 dpi:

```text
panel energy range:      0.08-0.18 eV
panel width:             848 px
panel absorption range:  5-2000 cm^-1
selected fit range:      20-1000 cm^-1
panel height:            982 px
selected vertical span:  641.180 px
center uncertainty:      6 px scenario
composition:             x=0.205
```

| temperature | trace span | horizontal span | departure if $z_2=0$ | critical $z_2$, $1u$ | critical $z_2$, $3u$ |
|---:|---:|---:|---:|---:|---:|
| 80 K | 16.088 meV | 136.429 px | 12.289 px | -1.374 | not reached for $z_2\le0$ |
| 300 K | 37.950 meV | 321.818 px | 26.337 px | -3.031 | -0.723 |

The same pattern appears. The broad high-temperature trace is potentially curvature-sensitive only if its upper point lies within approximately $0.72\sigma_G$ below the latent mean gap. The published tail plot does not independently establish that anchor.

## 7. Why Ariel 1995 does not supply the missing test

Ariel et al. differentiate the absorption coefficient itself and use extrema of

$$
\frac{d^2\alpha}{dE^2}
$$

to estimate a graded gap interval. That is an important derivative and smoothing precedent, but it is not the present observable. For a true exponential,

$$
\alpha''=\frac{\alpha}{W^2}>0,
$$

while

$$
\frac{d^2\log\alpha}{dE^2}=0.
$$

Thus $\alpha''$ does not discriminate a true exponential from a curved log tail in the way required here. Ariel et al. also warn that differentiation amplifies noise and that excessive smoothing can move derivative peaks. Those warnings strengthen, rather than remove, the figure-recoverability gate.

## 8. Decision

Manual digitization of the Finkman figures is not authorized as a curvature-validation step at this stage.

The reason is structural:

1. the tail-only figures do not independently identify $z_2$;
2. a sufficiently negative $z_2$ makes the Gaussian-power model arbitrarily straight over the displayed finite range;
3. the low-temperature traces fail the conservative three-uncertainty threshold even at $z_2=0$;
4. the high-temperature traces require $z_2\gtrsim-0.72$, an anchor not established by the figures;
5. source scatter, line thickness, smoothing, and baseline uncertainty are not included in the six-pixel scenario and can only weaken recoverability.

The next admissible evidence is one of:

- numerical absorption data with measurement covariance;
- an independently constrained mean-gap location and intrinsic amplitude;
- above-gap data sufficient to constrain the local intrinsic branch and locate the tail window in standardized coordinates;
- a higher-resolution source figure with recoverable point centers and documented preprocessing.

## 9. Claim boundary

Supported:

- finite-window straightness error tends to zero as the Gaussian-power window is moved deep below the mean gap;
- the decay is consistent with $O(|z_2|^{-2})$;
- the audited Finkman panels cannot provide a model-independent curvature test without an external gap-location anchor;
- the stated pixel thresholds are reproducible under declared source-conditioned scenarios.

Not supported:

- that the measured tails are Gaussian-disorder tails;
- that the empirical Finkman gap equals $\mu_G$;
- that six pixels is a measured statistical standard deviation;
- that visual straightness proves a true Urbach mechanism;
- that digitized publication figures constitute material validation;
- that this result authorizes a manuscript or submission.
