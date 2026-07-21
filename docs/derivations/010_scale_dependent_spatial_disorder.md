# Derivation 010: scale-dependent spatial disorder in HgCdTe band-edge observables

## 1. Scope

This derivation replaces the scalar-disorder-width assumption with a spatial random-field model. The objective is not to claim new Gaussian random-field mathematics. The objective is to identify the exact quantity sampled by a finite HgCdTe measurement and determine what measurement scales are required to recover microscopic disorder parameters.

Let the local CdTe mole fraction be

\[
x(\mathbf r)=\bar x+\delta x(\mathbf r),
\qquad
\mathbb E[\delta x(\mathbf r)]=0,
\]

with stationary covariance

\[
C_x(\mathbf h)
=
\mathbb E\!\left[
\delta x(\mathbf r)\,
\delta x(\mathbf r+\mathbf h)
\right].
\]

A normalized measurement kernel satisfies

\[
\int_{\mathbb R^D}w_a(\mathbf r)\,d^D r=1,
\]

where the parameter \(a\) represents the probe scale. The measured composition coordinate is

\[
X_a
=
\int_{\mathbb R^D}w_a(\mathbf r)x(\mathbf r)\,d^D r.
\]

The distinction between \(x(\mathbf r)\) and \(X_a\) is the central point. A pointwise microscopic variance is not the variance reported by a finite optical spot, pixel, electrical weighting field, diffusion volume, or thickness average.

## 2. General covariance identity

Because the kernel is normalized,

\[
\mathbb E[X_a]=\bar x.
\]

Subtracting the mean and expanding the square gives

\[
\begin{aligned}
\operatorname{Var}(X_a)
&=
\mathbb E\!\left[
\left(
\int w_a(\mathbf r)\delta x(\mathbf r)\,d^D r
\right)
\left(
\int w_a(\mathbf r')\delta x(\mathbf r')\,d^D r'
\right)
\right]\\
&=
\iint
w_a(\mathbf r)w_a(\mathbf r')
\mathbb E[\delta x(\mathbf r)\delta x(\mathbf r')]
\,d^D r\,d^D r'\\
&=
\boxed{
\iint
w_a(\mathbf r)w_a(\mathbf r')
C_x(\mathbf r-\mathbf r')
\,d^D r\,d^D r'
}.
\end{aligned}
\]

Equivalently, with the kernel autocorrelation

\[
A_a(\mathbf h)
=
\int w_a(\mathbf r)w_a(\mathbf r+\mathbf h)\,d^D r,
\]

we obtain

\[
\operatorname{Var}(X_a)
=
\int C_x(\mathbf h)A_a(\mathbf h)\,d^D h.
\]

In the spectral domain, if \(S_x(\mathbf k)\) is the composition power spectral density and \(W_a(\mathbf k)\) is the Fourier transform of the probe,

\[
\boxed{
\operatorname{Var}(X_a)
=
\frac{1}{(2\pi)^D}
\int S_x(\mathbf k)|W_a(\mathbf k)|^2\,d^D k
}.
\]

Thus a finite measurement reports a filtered spectral integral. It does not report \(C_x(0)\) unless the probe approaches a point measurement.

## 3. Exact Gaussian covariance--Gaussian probe theorem

Assume

\[
C_x(\mathbf h)
=
\sigma_x^2
\exp\!\left(-\frac{|\mathbf h|^2}{2\ell^2}\right),
\]

where \(\sigma_x^2=C_x(0)\) is the microscopic variance and \(\ell\) is the correlation length. Let

\[
w_a(\mathbf r)
=
\frac{1}{(2\pi a^2)^{D/2}}
\exp\!\left(-\frac{|\mathbf r|^2}{2a^2}\right).
\]

Draw independent random vectors \(\mathbf R,\mathbf R'\sim N(0,a^2I_D)\). The double integral is the expectation

\[
\operatorname{Var}(X_a)
=
\sigma_x^2
\mathbb E\!\left[
\exp\!\left(-\frac{|\mathbf R-\mathbf R'|^2}{2\ell^2}\right)
\right].
\]

Because

\[
\mathbf H=\mathbf R-\mathbf R'
\sim N(0,2a^2I_D),
\]

its density is

\[
p_H(\mathbf h)
=
\frac{1}{(4\pi a^2)^{D/2}}
\exp\!\left(-\frac{|\mathbf h|^2}{4a^2}\right).
\]

Therefore

\[
\begin{aligned}
\frac{\operatorname{Var}(X_a)}{\sigma_x^2}
&=
\frac{1}{(4\pi a^2)^{D/2}}
\int_{\mathbb R^D}
\exp\!\left[
-|\mathbf h|^2
\left(
\frac{1}{4a^2}+\frac{1}{2\ell^2}
\right)
\right]d^D h\\
&=
\frac{1}{(4\pi a^2)^{D/2}}
\left[
\frac{\pi}
{\frac{1}{4a^2}+\frac{1}{2\ell^2}}
\right]^{D/2}\\
&=
\left(1+\frac{2a^2}{\ell^2}\right)^{-D/2}.
\end{aligned}
\]

Hence

\[
\boxed{
V(a)
\equiv
\operatorname{Var}(X_a)
=
\sigma_x^2
\left(1+\frac{2a^2}{\ell^2}\right)^{-D/2}
}.
\]

The corresponding standard deviation is

\[
\boxed{
\sigma_{x,a}
=
\sigma_x
\left(1+\frac{2a^2}{\ell^2}\right)^{-D/4}
}.
\]

### 3.1 Small-probe asymptote

For \(a/\ell\ll1\),

\[
\frac{V(a)}{\sigma_x^2}
=
1
-D\frac{a^2}{\ell^2}
+\frac{D(D+2)}{2}\frac{a^4}{\ell^4}
+O\!\left(\frac{a^6}{\ell^6}\right).
\]

A sufficiently small probe approaches the microscopic variance.

### 3.2 Large-probe asymptote

For \(a/\ell\gg1\),

\[
\frac{V(a)}{\sigma_x^2}
=
2^{-D/2}
\left(\frac{\ell}{a}\right)^D
\left[
1-\frac{D}{4}\frac{\ell^2}{a^2}
+O\!\left(\frac{\ell^4}{a^4}\right)
\right].
\]

The measured variance decreases inversely with the effective number of correlation volumes sampled by the probe.

## 4. One-scale no-go theorem

Suppose one experiment measures \(V_*\) at one declared scale \(a_*\). For every \(\ell>0\), define

\[
\sigma_x^2(\ell)
=
V_*
\left(1+\frac{2a_*^2}{\ell^2}\right)^{D/2}.
\]

Then

\[
\sigma_x^2(\ell)
\left(1+\frac{2a_*^2}{\ell^2}\right)^{-D/2}
=V_*.
\]

Thus infinitely many microscopic pairs \((\sigma_x,\ell)\) produce the same measured width:

\[
\boxed{
\text{one probe scale cannot separately identify }
\sigma_x\text{ and }\ell
}.
\]

This is an exact non-identifiability result under the declared covariance and kernel, not a statement about measurement noise or insufficient numerical precision.

## 5. Exact two-scale inverse

Measure

\[
V_i
=
\sigma_x^2
\left(1+\frac{2a_i^2}{\ell^2}\right)^{-D/2},
\qquad i\in\{1,2\},
\]

at distinct scales \(a_1\ne a_2\). Define

\[
q
=
\left(\frac{V_1}{V_2}\right)^{2/D}.
\]

The variance ratio gives

\[
q
=
\frac{1+2a_2^2/\ell^2}
{1+2a_1^2/\ell^2}.
\]

Solving for \(\ell\),

\[
q\left(1+\frac{2a_1^2}{\ell^2}\right)
=
1+\frac{2a_2^2}{\ell^2},
\]

\[
(q-1)\ell^2
=
2(a_2^2-qa_1^2),
\]

and therefore

\[
\boxed{
\ell^2
=
2\frac{a_2^2-qa_1^2}{q-1}
}.
\]

The microscopic variance follows from either measurement:

\[
\boxed{
\sigma_x^2
=
V_1
\left(1+\frac{2a_1^2}{\ell^2}\right)^{D/2}
}.
\]

Two scale measurements are therefore algebraically sufficient under the exact model. They are not automatically well conditioned.

## 6. Conditioning and experimental design

Use logarithmic outputs and parameters,

\[
y_i=\ln V_i,
\qquad
\boldsymbol\theta=(\ln\sigma_x^2,\ln\ell).
\]

Then

\[
y_i
=
\ln\sigma_x^2
-\frac D2
\ln\!\left(1+\frac{2a_i^2}{\ell^2}\right),
\]

so

\[
\frac{\partial y_i}{\partial\ln\sigma_x^2}=1,
\]

and

\[
\frac{\partial y_i}{\partial\ln\ell}
=
D\frac{2a_i^2/\ell^2}{1+2a_i^2/\ell^2}
\equiv g_i.
\]

The logarithmic Jacobian is

\[
J
=
\begin{pmatrix}
1 & g_1\\
1 & g_2
\end{pmatrix},
\qquad
\det J=g_2-g_1.
\]

Consequently:

1. \(a_1=a_2\Rightarrow g_1=g_2\): the inverse is singular.
2. \(a_1,a_2\ll\ell\Rightarrow g_1,g_2\to0\): both probes measure nearly the microscopic variance and carry little correlation-length information.
3. \(a_1,a_2\gg\ell\Rightarrow g_1,g_2\to D\): both probes lie in the same large-scale power law and again provide nearly parallel information.
4. A useful pair places one scale below and one scale above \(\ell\).

For the declared two-dimensional sensitivity case with \(\ell=5\ \mu\mathrm m\):

- \((a_1,a_2)=(5,5.05)\ \mu\mathrm m\) gives logarithmic condition number \(632.9\);
- \((0.5,50)\ \mu\mathrm m\) gives \(2.68\);
- \((50,500)\ \mu\mathrm m\) gives \(1011.1\).

Scale separation alone is insufficient. The scales must straddle the correlation length.

## 7. Exact 1D top-hat results

For a normalized top-hat window of length \(L\),

\[
w_L(x)=
\begin{cases}
1/L,&0\le x\le L,\\
0,&\text{otherwise},
\end{cases}
\]

stationarity reduces the double integral to

\[
\boxed{
V_L
=
\frac{2}{L^2}
\int_0^L(L-h)C_x(h)\,dh
}.
\]

### 7.1 Gaussian covariance

For

\[
C_x(h)=\sigma_x^2e^{-h^2/(2\ell^2)},
\]

use

\[
\int_0^L e^{-h^2/(2\ell^2)}dh
=
\ell\sqrt{\frac\pi2}
\operatorname{erf}\!\left(\frac{L}{\sqrt2\ell}\right),
\]

and

\[
\int_0^L h e^{-h^2/(2\ell^2)}dh
=
\ell^2\left(1-e^{-L^2/(2\ell^2)}\right).
\]

Therefore

\[
\boxed{
V_{L,G}
=
\frac{2\sigma_x^2}{L^2}
\left[
L\ell\sqrt{\frac\pi2}
\operatorname{erf}\!\left(\frac{L}{\sqrt2\ell}\right)
-
\ell^2\left(1-e^{-L^2/(2\ell^2)}\right)
\right]
}.
\]

### 7.2 Exponential covariance

For

\[
C_x(h)=\sigma_x^2e^{-|h|/\ell},
\]

\[
\boxed{
V_{L,E}
=
\frac{2\sigma_x^2}{L^2}
\left[
L\ell
-
\ell^2\left(1-e^{-L/\ell}\right)
\right]
}.
\]

The Gaussian and exponential models have the same point-probe limit but different finite-scale curves and different large-window constants. A two-scale inverse is therefore covariance-model dependent.

## 8. Propagation through a signed HgCdTe gap law

Let

\[
G_a=E_g(X_a,T),
\qquad
V_a=\operatorname{Var}(X_a).
\]

Expand around \(\bar x\):

\[
E_g(\bar x+\delta,T)
\simeq
E_0
+E_x\delta
+\frac12E_{xx}\delta^2.
\]

For Gaussian \(\delta\sim N(0,V_a)\),

\[
\boxed{
\mathbb E[G_a]
\simeq
E_0+\frac12E_{xx}V_a
},
\]

and, after centering the quadratic term,

\[
\boxed{
\operatorname{Var}(G_a)
\simeq
E_x^2V_a
+\frac12E_{xx}^2V_a^2
}.
\]

The second equation is exact when the gap law is quadratic in composition. To first order,

\[
\sigma_{G,a}
\simeq
|E_x|\sigma_x
\left(1+\frac{2a^2}{\ell^2}\right)^{-D/4}.
\]

Near a critical composition, the same filtering law propagates to a local critical-temperature width:

\[
\sigma_{T_c,a}
\simeq
\left|\frac{E_x}{E_T}\right|
\sigma_x
\left(1+\frac{2a^2}{\ell^2}\right)^{-D/4},
\]

provided the root remains locally unique and uncensored.

## 9. Device-relevant magnitude

Use the declared sensitivity values

\[
D=2,
\qquad
\sigma_x=0.005,
\qquad
\ell=5\ \mu\mathrm m,
\qquad
|E_x|=1.7191085\ \mathrm{eV}.
\]

Then

\[
\sigma_{G,a}
\simeq
|E_x|\sigma_{x,a}.
\]

The exact probe filtering gives:

| Gaussian probe scale | Effective \(\sigma_{x,a}\) | Linearized \(\sigma_{G,a}\) |
|---:|---:|---:|
| \(1\ \mu\mathrm m\) | 0.004811 | 8.271 meV |
| \(5\ \mu\mathrm m\) | 0.002887 | 4.963 meV |
| \(10\ \mu\mathrm m\) | 0.001667 | 2.865 meV |
| \(100\ \mu\mathrm m\) | 0.0001767 | 0.304 meV |

The same microscopic field therefore appears \(27.23\) times narrower in standard deviation when the probe scale changes from \(1\) to \(100\ \mu\mathrm m\). Around a 10-\(\mu\mathrm m\) cutoff, the corresponding first-order cutoff spread changes from approximately \(0.667\ \mu\mathrm m\) to \(0.0245\ \mu\mathrm m\).

This magnitude is large enough to alter comparisons between micro-FTIR, wafer-scale FTIR, PL, pixel-scale cutoff maps, and device-response distributions. The numerical values remain a declared sensitivity case until a specimen-specific \(\sigma_x\), \(\ell\), dimensionality, and measurement kernel are established.

## 10. Observation-operator consequences

The following quantities must remain distinct:

\[
\sigma_x
\ne
\sigma_{x,a}
\ne
\frac{\sigma_{G,a}}{|E_x|}
\ne
W_{\mathrm{Urbach}}
\ne
\mathrm{FWHM}_{\mathrm{PL}}
\ne
\sigma_{\lambda_c}.
\]

They can be related only through declared forward operators. In particular:

- a Herrmann-like apparent exponential tail can arise after convolving a local edge with a gap distribution, but its fitted slope depends on the absorption fit window;
- a Chang-like detector cutoff depends on effective thickness and response criterion in addition to the latent edge;
- a mapped cutoff distribution depends on both the underlying spatial spectrum and the map's point-spread function, aperture, step size, and pixel/electrical weighting.

The scale-dependent covariance operator supplies the missing spatial layer between microscopic composition fluctuations and any of those reported observables.

## 11. Claim boundary

The general covariance-filter identity and Gaussian convolution are established mathematics. The potentially publishable contribution must be narrower and application specific:

1. an explicit HgCdTe spatial-disorder observation operator;
2. an exact one-scale no-go result and two-scale recovery design for the declared model;
3. quantitative demonstration that realistic probe-scale changes can move inferred gap or cutoff widths by orders relevant to device interpretation;
4. a source-grounded distinction among microscopic disorder, fitted optical tails, PL linewidth, and detector cutoff variation;
5. prior-art verification that this combined HgCdTe measurement-scale result has not already been established.

No submission claim is authorized until the prior-art and significance gates are complete.
