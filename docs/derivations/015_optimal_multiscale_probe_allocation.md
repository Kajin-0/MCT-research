# Derivation 015: optimal allocation of a multiscale spatial-disorder experiment

## 1. Scope

This derivation concerns the local two-parameter Gaussian benchmark used by the measurement-kernel-aware spatial-disorder program:

\[
V(s)=\frac{A}{1+2s^2/\xi^2},
\]

where \(A>0\) is point variance, \(\xi>0\) is correlation length, and \(s\) is a declared effective Gaussian probe standard deviation.

At probe scale \(s_i\), suppose \(n_i\) independent repeats are averaged and the single-repeat relative standard deviation is \(\sigma_y\). To first order in relative error,

\[
y_i=\log V(s_i)+\epsilon_i,
\qquad
\operatorname{Var}(\epsilon_i)=\frac{\sigma_y^2}{n_i}.
\]

The total repeat budget is

\[
N=\sum_i n_i.
\]

This is a local optimal-design result under homoscedastic log-variance noise. It is not a universal prescription for physical spot sizes or specimen sampling.

## 2. Log-parameter sensitivity

Use

\[
u=\log A,
\qquad
v=\log\xi.
\]

Then

\[
\log V(s)=u-\log\left(1+2s^2e^{-2v}\right).
\]

Define \(r=s/\xi\). The derivatives are

\[
\frac{\partial\log V}{\partial u}=1,
\]

and

\[
\boxed{
 g(r)
 =
 \frac{\partial\log V}{\partial v}
 =
 \frac{4r^2}{1+2r^2}
 }.
\]

The sensitivity is strictly increasing:

\[
g(0)=0,
\qquad
g(\infty)=2.
\]

The Fisher contribution from one averaged scale is

\[
F_i
=
\frac{n_i}{\sigma_y^2}
\begin{pmatrix}
1 & g_i\\
g_i & g_i^2
\end{pmatrix}.
\]

Therefore

\[
F
=
\frac{1}{\sigma_y^2}
\begin{pmatrix}
N & \sum_i n_i g_i\\
\sum_i n_i g_i & \sum_i n_i g_i^2
\end{pmatrix}.
\]

## 3. Fisher determinant as weighted sensitivity variance

Let

\[
\bar g=\frac{1}{N}\sum_i n_i g_i.
\]

The determinant is

\[
\begin{aligned}
\det F
&=
\frac{1}{\sigma_y^4}
\left[
N\sum_i n_i g_i^2
-\left(\sum_i n_i g_i\right)^2
\right]\\
&=
\boxed{
\frac{N}{\sigma_y^4}
\sum_i n_i(g_i-\bar g)^2
}.
\end{aligned}
\]

Thus D-optimality is equivalent to maximizing the weighted variance of the correlation-length sensitivity.

## 4. Exact endpoint D-optimal theorem

Suppose the feasible scales lie in

\[
s\in[s_{\min},s_{\max}],
\]

so the sensitivity lies in

\[
g\in[g_{\min},g_{\max}].
\]

For any probability distribution supported on a bounded interval, Popoviciu's inequality gives

\[
\operatorname{Var}(g)
\le
\frac{(g_{\max}-g_{\min})^2}{4}.
\]

Equality holds only when half the weight is placed at each endpoint. Hence the continuous locally D-optimal design is

\[
\boxed{
w_{\min}=w_{\max}=\frac12}
\]

with no weight at interior scales.

For integer repeat budget \(N\), the exact endpoint allocation is

\[
\boxed{
 n_{\min}=\left\lfloor\frac N2\right\rfloor,
 \qquad
 n_{\max}=\left\lceil\frac N2\right\rceil
 }.
\]

The determinant is

\[
\boxed{
\det F_{\mathrm D}
=
\frac{n_{\min}n_{\max}}{\sigma_y^4}
(g_{\max}-g_{\min})^2
}.
\]

The integer-rounding efficiency relative to an exactly equal continuous allocation is

\[
\boxed{
\eta_{\mathrm{integer}}
=
\frac{4n_{\min}n_{\max}}{N^2}
}.
\]

It equals one for even \(N\) and approaches one rapidly for odd \(N\).

## 5. Loss from unequal endpoint allocation

Let fraction \(x\) of the budget be assigned to the lower endpoint:

\[
n_{\min}=Nx,
\qquad
n_{\max}=N(1-x).
\]

Then

\[
\det F(x)
=
\frac{N^2x(1-x)}{\sigma_y^4}
\Delta g^2,
\qquad
\Delta g=g_{\max}-g_{\min}.
\]

Relative to the D-optimal design,

\[
\boxed{
\eta_D(x)=4x(1-x)
}.
\]

A 10/90 split retains only 36% of the determinant; a 25/75 split retains 75%.

## 6. Correlation-length variance criterion

For two endpoint scales, inversion gives

\[
F^{-1}
=
\frac{\sigma_y^2}{n_{\min}n_{\max}\Delta g^2}
\begin{pmatrix}
 n_{\min}g_{\min}^2+n_{\max}g_{\max}^2
 &-\left(n_{\min}g_{\min}+n_{\max}g_{\max}ight)\\
 -\left(n_{\min}g_{\min}+n_{\max}g_{\max}ight)
 &N
\end{pmatrix}.
\]

Therefore

\[
\boxed{
\operatorname{Var}(\log\xi)
=
\frac{\sigma_y^2N}
{n_{\min}n_{\max}\Delta g^2}
}.
\]

This is minimized by the same balanced endpoint allocation as D-optimality.

For even \(N\),

\[
\boxed{
\operatorname{SD}(\log\xi)
=
\frac{2\sigma_y}{\sqrt N\,|\Delta g|}
}.
\]

The equation exposes two failure regimes:

1. nearly coincident feasible scales give \(\Delta g\to0\);
2. a feasible interval entirely within the small- or large-probe asymptote also gives \(\Delta g\to0\).

More repeats cannot compensate efficiently for an interval with negligible sensitivity span.

## 7. A-optimal endpoint allocation

A-optimality minimizes

\[
\operatorname{tr}(F^{-1}).
\]

Let

\[
a=g_{\min},
\qquad
b=g_{\max}.
\]

For continuous lower-endpoint fraction \(x\),

\[
\operatorname{tr}(F^{-1})
=
\frac{\sigma_y^2}{N(b-a)^2}
\frac{1+xa^2+(1-x)b^2}{x(1-x)}.
\]

Differentiation yields

\[
(a^2-b^2)x^2+2(1+b^2)x-(1+b^2)=0.
\]

The physical root simplifies to

\[
\boxed{
 x_A
 =
 \frac{\sqrt{1+b^2}}
 {\sqrt{1+a^2}+\sqrt{1+b^2}}
 }.
\]

Because \(b>a\), A-optimality assigns more than half the observations to the lower-sensitivity endpoint. This reduces the joint trace by improving \(\log A\) precision, while D-optimality and the \(\log\xi\)-variance criterion remain balanced.

The selected criterion must therefore be declared. There is no single allocation that is simultaneously optimal for every scalar summary of the covariance matrix.

## 8. Absolute probe-scale calibration floor

Let all physical probe scales share an unknown multiplicative calibration:

\[
s_i^{\mathrm{true}}=s_i e^\delta,
\qquad
\delta\sim p_\delta.
\]

The Gaussian model depends on

\[
\frac{s_i e^\delta}{\xi}
=
\frac{s_i}{e^{v-\delta}}.
\]

The data identify only

\[
\lambda=v-\delta.
\]

For an independent calibration prior and broad absolute-length support, the established exact posterior result is

\[
\boxed{
\operatorname{Var}(v)
=
\operatorname{Var}(\lambda)
+\operatorname{Var}(\delta)
}.
\]

No allocation can drive absolute correlation-length uncertainty below independent absolute probe-scale calibration uncertainty. Optimal allocation improves relative-scale information; it does not remove the common calibration floor.

## 9. Why a third scale is still required

Two endpoint scales identify \(A\) and \(\xi\) under the Gaussian family but cannot test that family. In two dimensions,

\[
\frac{1}{V(s)}
=
\frac{1}{A}
+
\frac{2}{A\xi^2}s^2
\]

is exactly affine in \(s^2\). A third scale supplies the first reciprocal-linearity residual.

For ordered scales \(s_0<s_1<s_2\), define

\[
f=\frac{s_1^2-s_0^2}{s_2^2-s_0^2}.
\]

The residual is

\[
R
=
\frac{1}{V_1}
-(1-f)\frac{1}{V_0}
-f\frac{1}{V_2}.
\]

Under independent relative errors and repeat counts,

\[
\operatorname{Var}(R)
\simeq
\sigma_y^2
\left[
\frac{(1-f)^2}{n_0V_0^2}
+
\frac{1}{n_1V_1^2}
+
\frac{f^2}{n_2V_2^2}
\right].
\]

For a fixed declared alternative covariance family, family-test-only optimal allocation follows the Neyman rule

\[
\boxed{
 n_i
 \propto
 \frac{|c_i|}{V_i},
 \qquad
 (c_0,c_1,c_2)=(-(1-f),1,-f)
 }.
\]

This generally differs from the endpoint D-optimal allocation. The experiment therefore has a genuine Pareto tradeoff between parameter precision and covariance-family falsification power.

## 10. Deterministic constrained design

The implemented optimizer enumerates all positive integer allocations satisfying

\[
n_1\ge n_{1,\min},
\qquad
n_0+n_1+n_2=N.
\]

For each allocation it computes:

1. Gaussian Fisher information and parameter covariance;
2. D-efficiency relative to the balanced endpoint design;
3. absolute correlation-length uncertainty after the common calibration floor;
4. standardized reciprocal-linearity residuals for Matérn \(\nu=1/2,3/2,5/2\);
5. the worst-case absolute residual over those alternatives.

The recommendation maximizes the worst-case family residual subject to a declared minimum D-efficiency.

For

\[
(s_0,s_1,s_2)/\xi=(0.1,1,2),
\qquad
\sigma_y=0.03,
\qquad
\eta_D\ge0.8,
\]

the controlled integer results are:

| Total repeats | Recommended allocation | D-efficiency | Worst-case Matérn residual |
|---:|---:|---:|---:|
| 12 | (5, 3, 4) | 0.8082 | 2.4024 |
| 30 | (11, 7, 12) | 0.8007 | 3.7816 |
| 60 | (24, 15, 21) | 0.8045 | 5.4040 |

The middle-scale fraction remains approximately one quarter because the selected 80% precision floor leaves enough budget for covariance-family testing without discarding endpoint information.

These allocations are dimensionless local designs. Physical scales require a prior design value or range for \(\xi\), and composite-kernel calibration must be inserted before experimental use.

## 11. Claim boundary

Weighted-variance optimality, Popoviciu's inequality, Fisher information, A-optimality, and Neyman allocation are established mathematics. The candidate R04 contribution is their explicit integration with:

- HgCdTe finite-resolution disorder measurements;
- the one-scale/two-scale theorem hierarchy;
- common absolute probe-scale calibration limits;
- covariance-family falsification;
- deterministic integer-budget design.

The result does not identify a specimen covariance, prescribe universal spot sizes, or authorize a manuscript.
