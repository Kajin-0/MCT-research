# Probe-scale calibration limit in multiscale disorder inference

## Scope

This derivation applies to the declared two-dimensional Gaussian covariance and Gaussian-probe benchmark

$$
V(s)=\frac{A}{1+2s^2/\xi^2},
$$

where:

- $A>0$ is the point composition variance;
- $\xi>0$ is the lateral correlation length;
- $s\geq 0$ is the Gaussian probe standard deviation;
- $V(s)$ is the apparent variance after probe averaging.

The result is a local linear-Gaussian identifiability statement. It does not establish a Gaussian covariance law for any specimen and does not calibrate an experimental probe.

## Physics-parameter Jacobian

Use dimensionless parameters

$$
\theta=
\begin{pmatrix}
\log A\\
\log \xi
\end{pmatrix}.
$$

Define

$$
q=\frac{2s^2}{\xi^2},
\qquad
r=\frac{q}{1+q}.
$$

Then

$$
\frac{\partial V}{\partial \log A}=V,
$$

and

$$
\frac{\partial V}{\partial \log \xi}=2Vr.
$$

The correlation-length sensitivity is small for $s\ll\xi$, approaches $2V$ for $s\gg\xi$, and changes most rapidly around $s\sim\xi$.

## Probe-scale Jacobian

A multiplicative probe error is naturally represented as an error in $\log s$. Direct differentiation gives

$$
\frac{\partial V}{\partial \log s}=-2Vr.
$$

Therefore

$$
\boxed{
\frac{\partial V}{\partial \log s}
=-
\frac{\partial V}{\partial \log \xi}
}.
$$

This identity is exact within the declared model, not a small-$s$ or large-$s$ approximation.

## General calibration modes

Let $n$ probe measurements use nominal scales $s_i$. Represent log-scale error by a lower-dimensional Gaussian nuisance vector $z\in\mathbb R^k$:

$$
\delta\log s = Bz,
\qquad
z\sim\mathcal N(0,C_z),
$$

where $B\in\mathbb R^{n\times k}$ declares the calibration modes and $C_z$ is positive definite.

Examples include:

- one common multiplicative calibration: $B=\mathbf 1$;
- independent scale errors: $B=I$;
- common magnification plus a focus-dependent distortion mode: two columns in $B$;
- correlated instrument-specific calibration modes from an external optical model.

Let $J_\theta$ be the $n\times2$ physics Jacobian, let

$$
D_s=\operatorname{diag}\left(
\frac{\partial V_i}{\partial\log s_i}
\right),
$$

and define the nuisance Jacobian

$$
J_z=D_sB.
$$

For observation covariance $C_y$, the augmented local Fisher matrix is

$$
F_{\rm aug}=
\begin{pmatrix}
J_\theta^T C_y^{-1}J_\theta & J_\theta^T C_y^{-1}J_z\\
J_z^T C_y^{-1}J_\theta & J_z^T C_y^{-1}J_z+C_z^{-1}
\end{pmatrix}.
$$

Marginalizing the calibration nuisance gives the Schur complement

$$
F_{\theta,\rm marg}
=F_{\theta\theta}
-F_{\theta z}F_{zz}^{-1}F_{z\theta}.
$$

The implementation evaluates these expressions through Cholesky solves and never requires explicit inversion of the observation covariance.

## Exact common-calibration theorem

For one common scale offset $\delta$,

$$
\log s_i\rightarrow\log s_i+\delta
$$

for every measurement. Because

$$
J_\delta=-J_{\log\xi},
$$

the likelihood depends on the combination

$$
\eta=\log\xi-\delta,
$$

not on $\log\xi$ and $\delta$ separately.

Assume an independent Gaussian calibration prior

$$
\delta\sim\mathcal N(0,\tau_s^2).
$$

The data determine $(\log A,\eta)$. Since

$$
\log\xi=\eta+\delta,
$$

the exact local covariance identity is

$$
\boxed{
\operatorname{Cov}(\log A,\log\xi)_{\rm calibrated}
=
\operatorname{Cov}(\log A,\log\xi)_{\rm exact\ scale}
+
\begin{pmatrix}
0&0\\
0&\tau_s^2
\end{pmatrix}
}.
$$

Consequences:

1. The common scale calibration does not change the local variance of $\log A$.
2. It does not change the covariance between $\log A$ and the data-identified relative correlation length.
3. It adds exactly $\tau_s^2$ to the variance of $\log\xi$.
4. With no informative absolute scale prior, the absolute correlation length is unidentifiable regardless of measurement precision or number of scales.
5. Additional measurements sharing the same unknown magnification cannot average down this systematic floor.

The appropriate experimental statement is therefore not merely that probe calibration contributes uncertainty. It sets an exact lower bound on recoverable absolute correlation-length precision within this model.

## Reference design

For

$$
A=0.01,
\qquad
\xi=2,
\qquad
s=(0,0.4,2,10),
$$

with independent 5% relative uncertainty in each measured variance, the exact-scale local covariance is

$$
C_0=
\begin{pmatrix}
0.0013152930 & -0.0008021380\\
-0.0008021380 & 0.0009321046
\end{pmatrix}.
$$

A common log-scale calibration standard deviation $\tau_s=0.02$ produces

$$
C_{\rm common}=
\begin{pmatrix}
0.0013152930 & -0.0008021380\\
-0.0008021380 & 0.0013321046
\end{pmatrix},
$$

where the only change is

$$
0.0013321046-0.0009321046=0.0004=\tau_s^2.
$$

The standard deviation of $\log\xi$ increases by a factor of approximately $1.1955$.

Independent 2% log-scale errors at each probe are not a pure common mode. For the same design, both parameters degrade:

$$
\frac{\sigma_{\log A}}{\sigma_{\log A,0}}\approx1.0073,
\qquad
\frac{\sigma_{\log\xi}}{\sigma_{\log\xi,0}}\approx1.1329.
$$

## Experimental-design implications

A multiscale experiment intended to recover an absolute $\xi$ should declare separately:

- absolute scale calibration uncertainty;
- relative scale uncertainty between measurements;
- shape uncertainty in the effective kernel;
- observation noise and cross-scale covariance.

The common calibration floor cannot be repaired by denser sampling alone. It requires an independent scale reference. Relative and shape-changing errors can be reduced through repeated calibration, instrument modeling, or experimental design because they are not exactly equivalent to $\xi$.

## Claim restrictions

This result does not support:

- a specimen-specific correlation length;
- a universal Gaussian covariance family;
- replacing a measured point-spread function with a nominal pixel pitch;
- treating the local Fisher covariance as a global nonlinear posterior;
- identifying apparent variance with an optical tail energy or linewidth;
- any random-mass Kane or topological conclusion.
