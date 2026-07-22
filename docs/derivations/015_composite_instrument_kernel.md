# Derivation 015: composite optical, pixel, and depth kernel

**Program:** measurement-kernel-aware spatial disorder (R04)  
**Issues:** #196, #228  
**Status:** exact lateral theorem plus controlled finite-depth and calibration analysis

## 1. Scope

Earlier R04 results treated a measurement by one Gaussian probe width. Real spatially resolved measurements commonly combine several operations:

1. optical blur;
2. finite pixel or scan-bin integration;
3. depth-dependent sensitivity through a finite absorbing layer.

This derivation replaces the single nominal width with one declared separable instrument model:

$$
w(x,y,z)=w_x(x)w_y(y)w_z(z).
$$

The lateral kernels are Gaussian point-spread functions convolved with rectangular integration windows. The depth kernel is a normalized exponential in a finite slab.

The result is a representative analytical benchmark. It is not asserted to be the point-spread function of every HgCdTe microscope, mapper, detector, or spectrometer.

## 2. Material covariance

Use an axis-aligned separable Gaussian covariance,

$$
C(\mathbf h)
=
A
\exp\left(-\frac{h_x^2}{2\xi_x^2}\right)
\exp\left(-\frac{h_y^2}{2\xi_y^2}\right)
\exp\left(-\frac{h_z^2}{2\xi_z^2}\right).
$$

Here:

- $A$ is the microscopic point variance;
- $\xi_x,\xi_y,\xi_z$ are Gaussian correlation standard deviations;
- no isotropy assumption is required.

For a normalized separable measurement kernel,

$$
X_w=\iiint w(\mathbf r)x(\mathbf r)d\mathbf r,
$$

stationarity gives

$$
\operatorname{Var}(X_w)
=
A F_xF_yF_z.
$$

This exact product follows from separability of both the covariance and the kernel.

## 3. One lateral axis

Let the measurement coordinate on one axis be

$$
R=G+U,
$$

where

$$
G\sim\mathcal N(0,\sigma^2)
$$

represents the Gaussian PSF and

$$
U\sim\operatorname{Uniform}[-p/2,p/2]
$$

represents rectangular pixel or scan-bin integration.

For two independent samples,

$$
\Delta R=R_1-R_2=\Delta G+\Delta U.
$$

The Gaussian difference obeys

$$
\Delta G\sim\mathcal N(0,2\sigma^2),
$$

while the rectangular difference has triangular density

$$
f_{\Delta U}(u)
=
\frac{p-|u|}{p^2},
\qquad |u|\le p.
$$

The required attenuation is

$$
F(\xi,\sigma,p)
=
\mathbb E\left[
\exp\left(-\frac{(\Delta R)^2}{2\xi^2}\right)
\right].
$$

## 4. Gaussian conditional integral

Condition on $\Delta U=u$. The convolution of the Gaussian difference with the Gaussian covariance factor gives

$$
\mathbb E_{\Delta G}
\left[
\exp\left(-\frac{(\Delta G+u)^2}{2\xi^2}\right)
\right]
=
\frac{\xi}{L}
\exp\left(-\frac{u^2}{2L^2}\right),
$$

where

$$
\boxed{
L^2=\xi^2+2\sigma^2.
}
$$

Therefore

$$
F(\xi,\sigma,p)
=
\frac{\xi}{L}
\int_{-p}^{p}
\frac{p-|u|}{p^2}
\exp\left(-\frac{u^2}{2L^2}\right)du.
$$

Using symmetry,

$$
F
=
\frac{\xi}{L}
\frac{2}{p^2}
\int_0^p
(p-u)
\exp\left(-\frac{u^2}{2L^2}\right)du.
$$

Direct integration gives

$$
\boxed{
F(\xi,\sigma,p)
=
\frac{\xi}{L}
\frac{2}{p^2}
\left[
 pL\sqrt{\frac{\pi}{2}}
 \operatorname{erf}\left(\frac{p}{\sqrt{2}L}\right)
 +L^2\operatorname{expm1}\left(-\frac{p^2}{2L^2}\right)
\right].
}
$$

The `expm1` form avoids subtracting nearly equal numbers.

The implementation evaluates the same expression through the previously verified Gaussian-covariance top-hat formula at the enlarged scale $L$, multiplied by $\xi/L$.

## 5. Limits

### 5.1 Point pixel

For $p\rightarrow0$,

$$
\boxed{
F(\xi,\sigma,0)
=
\frac{\xi}{\sqrt{\xi^2+2\sigma^2}}.
}
$$

This is the ordinary Gaussian-PSF result.

### 5.2 Point PSF

For $\sigma\rightarrow0$,

$$
F(\xi,0,p)
=
\frac{2}{p^2}
\left[
 p\xi\sqrt{\frac{\pi}{2}}
 \operatorname{erf}\left(\frac{p}{\sqrt{2}\xi}\right)
 +\xi^2\operatorname{expm1}\left(-\frac{p^2}{2\xi^2}\right)
\right],
$$

which is the exact one-dimensional rectangular-window result.

### 5.3 Point instrument

For $p=0$ and $\sigma=0$,

$$
F=1.
$$

### 5.4 Small rectangular width

Let $q=p/L$. The triangular integral has the stable expansion

$$
1-rac{q^2}{12}+rac{q^4}{120}-\frac{q^6}{1344}+O(q^8).
$$

Thus second-moment matching is asymptotically correct for sufficiently small $p/L$, but it need not preserve the exact attenuation at finite width.

## 6. Two-dimensional lateral kernel

For axis-aligned elliptical PSF widths $(\sigma_x,\sigma_y)$ and rectangular dimensions $(p_x,p_y)$,

$$
\boxed{
F_{xy}
=
F(\xi_x,\sigma_x,p_x)
F(\xi_y,\sigma_y,p_y).
}
$$

The formula remains valid for anisotropic but axis-aligned Gaussian covariance.

It does not cover a rotated rectangular pixel relative to the covariance principal axes. Rotation destroys the simple product and requires a two-dimensional integration or Fourier treatment.

## 7. Finite-depth kernel

For front incidence in a slab of thickness $d$,

$$
w_z(z)
=
\frac{\alpha e^{-\alpha z}}
{1-e^{-\alpha d}},
\qquad 0\le z\le d.
$$

Back incidence reflects the kernel about the slab midplane. For stationary covariance in a homogeneous slab, front and back give the same filtered variance.

Define

$$
F_z
=
\int_0^d\int_0^d
w_z(z)w_z(z')
\exp\left[-\frac{(z-z')^2}{2\xi_z^2}\right]
dz\,dz'.
$$

The present implementation evaluates $F_z$ using the existing deterministic Gauss--Legendre covariance quadratic form. No new closed finite-slab Gaussian-depth formula is claimed here.

The complete result is

$$
\boxed{
\frac{\operatorname{Var}(X_w)}{A}
=
F(\xi_x,\sigma_x,p_x)
F(\xi_y,\sigma_y,p_y)
F_z(\xi_z,\alpha,d).
}
$$

## 8. Equivalent Gaussian approximation

The variance of one lateral measurement coordinate is

$$
\operatorname{Var}(R)
=
\sigma^2+\frac{p^2}{12}.
$$

The moment-matched Gaussian width is therefore

$$
\boxed{
\sigma_{\rm eq}^2
=
\sigma^2+\frac{p^2}{12}.
}
$$

Replacing the true Gaussian-plus-rectangular kernel by this Gaussian gives

$$
F_{\rm eq}
=
\frac{\xi}
{\sqrt{\xi^2+2\sigma_{\rm eq}^2}}.
$$

Moment matching preserves the kernel covariance but not the triangular higher moments generated by finite rectangular integration. The relevant deterministic error is

$$
\epsilon_{\rm eq}
=
\frac{F_{{\rm eq},x}F_{{\rm eq},y}}
{F_xF_y}-1.
$$

The depth factor cancels because the exact and approximate models use the same $F_z$.

## 9. Controlled reference case

Use consistent length units and declare

```text
xi_x = xi_y = xi_z = 2
sigma_x = sigma_y = 2
p_x = p_y = 5
alpha = 0.5
thickness = 10
```

The calculated factors are

```text
F_x = F_y                         0.494664
F_z                               0.664446
exact measured / point variance   0.162585
```

The moment-matched Gaussian gives

```text
equivalent measured / point variance  0.164399
relative error                         1.116%
```

Thus the instrument reports only about $16.3\%$ of the microscopic point variance in this controlled design. Treating the full kernel as one equivalent Gaussian already shifts the predicted measured variance by slightly more than $1\%$.

## 10. Pixel-dominated stress case

For

```text
xi_x = xi_y = 5
sigma_x = sigma_y = 3.8
p_x = p_y = 44.2
```

with the same declared depth case,

```text
exact measured / point variance       0.040204
equivalent-Gaussian variance ratio    0.043773
relative error                         8.876%
```

The approximation error is therefore not uniformly negligible when rectangular integration is large compared with the material correlation length.

## 11. Dimensionless stress grid

The committed validation record evaluates

```text
sigma/xi = [0, 0.25, 0.5, 1, 2, 4]
p/xi     = [0, 0.5, 1, 2, 4, 8, 16]
```

for an isotropic two-dimensional lateral kernel.

Among the 42 declared cases:

- 18 exceed $1\%$ equivalent-Gaussian variance error;
- the maximum is $9.045\%$;
- the maximum occurs at $\sigma/\xi=2$ and $p/\xi=16$.

This grid is a controlled dimensionless stress test, not a survey of real commercial or laboratory instruments.

## 12. Instrument calibration sensitivity

Let the instrument log-parameter vector be

$$
\boldsymbol\eta
=
(
\log\sigma_x,
\log\sigma_y,
\log p_x,
\log p_y,
\log\alpha,
\log d
)^T.
$$

Define the local sensitivity of the exact variance ratio $R$ by

$$
\boxed{
g_i
=
\frac{\partial\log R}{\partial\eta_i}.
}
$$

For declared instrument log-covariance $\Sigma_\eta$, first-order propagation gives

$$
\boxed{
\operatorname{Var}(\log R)
=
\mathbf g^T\Sigma_\eta\mathbf g.
}
$$

The implementation evaluates $\mathbf g$ by symmetric log-parameter perturbation. This numerical differentiation is separate from the exact lateral attenuation formula.

For the reference case,

```text
g = [-0.48340, -0.48340,
     -0.27491, -0.27491,
      0.40900, -0.06543]
```

for $(\sigma_x,\sigma_y,p_x,p_y,\alpha,d)$.

With independent log-standard deviations

```text
[5%, 5%, 1%, 1%, 10%, 5%]
```

the propagated first-order relative standard deviation of the measured variance is

```text
5.35%.
```

In this declared case, calibration uncertainty is larger than the $1.12\%$ moment-matching error. This does not make kernel shape irrelevant; it shows that shape and calibration must be reported separately rather than merged into one nominal width.

## 13. Measurement consequence

A nominal spot size is insufficient when pixel integration and depth weighting are material. A defensible multiscale inference should report:

1. optical PSF widths and orientation;
2. pixel or scan-bin dimensions;
3. absorption coefficient and thickness;
4. the covariance family used for inversion;
5. kernel calibration covariance;
6. exact or independently verified filtering;
7. the error introduced by any equivalent-width reduction.

The main practical consequence is not that the equivalent Gaussian always fails. It is that its validity is regime-dependent and testable.

## 14. Claim restrictions

This result does not establish:

- a universal HgCdTe instrument kernel;
- a specimen-specific disorder amplitude or correlation length;
- that every PSF is Gaussian;
- that every pixel is exactly rectangular;
- a rotated or nonseparable kernel theorem;
- a closed finite-slab Gaussian depth formula;
- that the declared stress grid represents typical instruments;
- manuscript readiness or novelty relative to the full finite-aperture literature.

The next R04 gate is to combine this calibrated instrument kernel with covariance-family, fitting-convention, and observation-operator uncertainty in one design calculation, then test it against a public or experimentally specified measurement path.
