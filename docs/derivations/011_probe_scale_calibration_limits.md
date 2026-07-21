# Derivation 011: probe-scale calibration limits in multiscale disorder inference

## 1. Scope

This derivation belongs to the measurement-kernel-aware spatial-disorder program, contribution R04.

The physical benchmark is the isotropic two-dimensional Gaussian covariance/Gaussian probe model

\[
V_i
=
V(s_i;A,\xi)
=
\frac{A}{1+2s_i^2/\xi^2},
\]

where

- \(A>0\) is the microscopic point variance;
- \(\xi>0\) is the spatial correlation length;
- \(s_i\ge0\) is the nominal Gaussian probe standard deviation;
- \(V_i\) is the predicted probe-averaged variance.

Previous work treated the probe scales as known exactly. This derivation introduces uncertainty in their multiplicative calibration.

The result is a local linear-Gaussian identifiability calculation. It is not an instrument calibration, specimen fit, universal covariance law, or experimental validation.

## 2. Physical log-parameter Jacobian

Define

\[
\theta
=
\begin{pmatrix}
\log A\\
\log\xi
\end{pmatrix},
\qquad
q_i=\frac{2s_i^2}{\xi^2}.
\]

Then

\[
V_i=A(1+q_i)^{-1}.
\]

The physical derivatives are

\[
\frac{\partial V_i}{\partial\log A}=V_i,
\]

and

\[
\frac{\partial V_i}{\partial\log\xi}
=
2V_i\frac{q_i}{1+q_i}.
\]

Thus the physical Jacobian row is

\[
J_{\theta,i}
=
\begin{pmatrix}
V_i & 2V_i q_i/(1+q_i)
\end{pmatrix}.
\]

## 3. Probe-log calibration coordinates

Represent the actual probe scales by

\[
\log s_i^{\rm actual}
=
\log s_i^{\rm nominal}
+
(B\eta)_i,
\]

where

- \(B\in\mathbb R^{N\times K}\) is a declared calibration basis;
- \(\eta\in\mathbb R^K\) contains nuisance calibration coordinates.

Examples include:

1. **common calibration:** \(B=\mathbf 1\), one shared magnification or resolution factor;
2. **independent calibration:** \(B=I_N\), one error per scale;
3. **correlated modes:** columns of \(B\) may represent common offset, scale-dependent tilt, wavelength dependence, or another calibrated low-dimensional basis.

Because \(q_i\propto s_i^2/\xi^2\),

\[
\boxed{
\frac{\partial V_i}{\partial\log s_i}
=
-
\frac{\partial V_i}{\partial\log\xi}
}
\]

exactly. Define the vector

\[
j_s
=
\begin{pmatrix}
\partial V_1/\partial\log s_1\\
\vdots\\
\partial V_N/\partial\log s_N
\end{pmatrix}.
\]

The nuisance Jacobian is

\[
\boxed{
J_\eta
=
\operatorname{diag}(j_s)B.
}
\]

## 4. Joint Fisher matrix

Let \(C_y\) be the positive-definite observation covariance. Whiten the Jacobians with a Cholesky factor \(C_y=LL^T\):

\[
\widetilde J_\theta=L^{-1}J_\theta,
\qquad
\widetilde J_\eta=L^{-1}J_\eta.
\]

Let the nuisance prior be Gaussian with precision \(P_\eta\succeq0\). The joint information matrix is

\[
F_{\rm joint}
=
\begin{pmatrix}
F_{\theta\theta} & F_{\theta\eta}\\
F_{\eta\theta} & F_{\eta\eta}
\end{pmatrix},
\]

where

\[
F_{\theta\theta}
=
\widetilde J_\theta^T\widetilde J_\theta,
\]

\[
F_{\theta\eta}
=
\widetilde J_\theta^T\widetilde J_\eta,
\]

and

\[
F_{\eta\eta}
=
\widetilde J_\eta^T\widetilde J_\eta+P_\eta.
\]

Marginalizing the calibration nuisance coordinates gives the Schur complement

\[
\boxed{
F_{\rm marg}
=
F_{\theta\theta}
-
F_{\theta\eta}
F_{\eta\eta}^{+}
F_{\eta\theta},
}
\]

where \((\cdot)^+\) is the symmetric Moore--Penrose pseudoinverse. Rank, condition number, covariance, correlation, and null directions are calculated from \(F_{\rm marg}\).

## 5. Exact common-calibration confounding

For one common log-scale error \(\eta_c\),

\[
B=\mathbf 1,
\qquad
J_{\eta_c}
=-J_{\log\xi}.
\]

Therefore the measurements depend on

\[
\log\xi-\eta_c,
\]

not on \(\log\xi\) and \(\eta_c\) separately.

### 5.1 No calibration prior

With no prior information on \(\eta_c\), the common scale is exactly confounded with correlation length. The marginalized information has the form

\[
F_{\rm marg}
=
\begin{pmatrix}
F_{AA}-F_{A\xi}^2/F_{\xi\xi} & 0\\
0 & 0
\end{pmatrix}.
\]

Hence

\[
\boxed{
\operatorname{rank}(F_{\rm marg})=1,
\qquad
\text{null direction}=(0,1)^T.
}
\]

The point-variance coordinate retains information, but the absolute correlation length is unidentified.

### 5.2 Gaussian common-scale prior

Let

\[
\eta_c\sim N(0,\tau_s^2).
\]

Introduce the measured relative-length coordinate

\[
\lambda=\log\xi-\eta_c.
\]

The likelihood supplies the exact-scale covariance for \((\log A,\lambda)\), while the independent prior supplies variance \(\tau_s^2\) for \(\eta_c\). Since

\[
\log\xi=\lambda+\eta_c,
\]

we obtain the exact identity

\[
\boxed{
\operatorname{Cov}(\log A,\log\xi)_{\rm calibrated}
=
\operatorname{Cov}(\log A,\log\xi)_{\rm exact\ scale}
+
\begin{pmatrix}
0&0\\
0&\tau_s^2
\end{pmatrix}.
}
\]

Consequences:

- the variance of \(\log A\) is unchanged;
- the covariance between \(\log A\) and \(\log\xi\) is unchanged;
- the variance of \(\log\xi\) increases by exactly \(\tau_s^2\);
- no amount of repeated multiscale variance data can remove a common absolute scale uncertainty without external calibration.

## 6. Independent and correlated calibration errors

For independent per-scale errors,

\[
B=I_N,
\qquad
P_\eta=\operatorname{diag}(\tau_1^{-2},\ldots,\tau_N^{-2}).
\]

Unlike the common mode, independent errors perturb relative scale spacing as well as absolute scale. They can inflate uncertainty in both \(\log A\) and \(\log\xi\).

For correlated calibration modes, choose a physically declared basis. For example,

\[
B
=
\begin{pmatrix}
1 & b_1\\
\vdots & \vdots\\
1 & b_N
\end{pmatrix}
\]

may represent a common offset plus a scale-dependent tilt. A full prior covariance between the two nuisance coordinates is allowed. The Schur complement retains those correlations exactly in the local Gaussian approximation.

## 7. Numerical reference design

Use

\[
A=0.03,
\qquad
\xi=1.4,
\qquad
s=(0.2,0.7,2.0,6.0),
\]

with independent observation noise equal to four percent of each predicted variance.

The exact-scale physical covariance is

\[
C_0
\approx
\begin{pmatrix}
1.23886\times10^{-3} & -7.8060\times10^{-4}\\
-7.8060\times10^{-4} & 7.2639\times10^{-4}
\end{pmatrix}.
\]

For a common log-scale prior \(\tau_s=0.08\),

\[
C_{\rm cal}
\approx
\begin{pmatrix}
1.23886\times10^{-3} & -7.8060\times10^{-4}\\
-7.8060\times10^{-4} & 7.12639\times10^{-3}
\end{pmatrix},
\]

which differs from \(C_0\) only by \(0.08^2=0.0064\) in the \(\log\xi\) variance. The \(\log\xi\) standard-deviation inflation is approximately \(3.1322\), while the \(\log A\) inflation is exactly one.

For five independent two-percent scale priors in the design

\[
s=(0.15,0.5,1.5,4.5,12.0),
\]

the local standard-deviation inflation factors are approximately

\[
(1.03115,\ 1.28794)
\]

for \((\log A,\log\xi)\).

These are model-conditioned design calculations, not calibrated instrument performance.

## 8. Claim boundary and falsification

The exact common-mode identity follows from the declared ratio structure \(s/\xi\). It would fail if the observation operator contained an independently calibrated absolute length dependence not reducible to that ratio.

The broader nuisance analysis is local and linearized. It can fail when:

- calibration errors are too large for a log-linear approximation;
- the covariance family is incorrect;
- the probe kernel is not represented by the declared basis;
- observation errors are non-Gaussian or parameter dependent beyond the supplied covariance;
- nuisance modes alter thickness, spectral response, or another operator component simultaneously.

Therefore the implementation reports information under declared assumptions and does not convert synthetic recoverability into material validation.
