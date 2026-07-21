# Derivation 010: scale-dependent spatial disorder in HgCdTe observables

## 1. Spatial observation operator

Let the local CdTe mole fraction be

\[
x(\mathbf r)=\bar x+\delta x(\mathbf r),
\qquad
\mathbb E[\delta x]=0,
\]

with stationary covariance

\[
C_x(\mathbf h)=
\mathbb E[\delta x(\mathbf r)\delta x(\mathbf r+\mathbf h)].
\]

A normalized probe kernel satisfies

\[
\int w_a(\mathbf r)\,d^D r=1,
\]

and reports

\[
X_a=\int w_a(\mathbf r)x(\mathbf r)\,d^D r.
\]

Direct expansion gives

\[
\boxed{
\operatorname{Var}(X_a)=
\iint w_a(\mathbf r)w_a(\mathbf r')
C_x(\mathbf r-\mathbf r')\,d^D r\,d^D r'
}.
\]

Equivalently,

\[
\boxed{
\operatorname{Var}(X_a)=
\frac{1}{(2\pi)^D}\int
S_x(\mathbf k)|W_a(\mathbf k)|^2\,d^D k
}.
\]

A finite measurement therefore returns a filtered spatial spectrum, not the point variance \(C_x(0)\).

## 2. Gaussian covariance and Gaussian probe

For

\[
C_x(\mathbf h)=\sigma_x^2
\exp\left(-\frac{|\mathbf h|^2}{2\ell^2}\right)
\]

and

\[
w_a(\mathbf r)=
(2\pi a^2)^{-D/2}
\exp\left(-\frac{|\mathbf r|^2}{2a^2}\right),
\]

the difference of two independent probe coordinates is Gaussian with covariance \(2a^2I\). Evaluating the Gaussian expectation yields

\[
\boxed{
V(a)=\operatorname{Var}(X_a)=
\sigma_x^2\left(1+\frac{2a^2}{\ell^2}\right)^{-D/2}
}.
\]

The existing core evaluates the anisotropic generalization

\[
V=\sigma_x^2
\sqrt{\frac{\det\Lambda}{\det(\Lambda+2\Sigma_w)}}
\]

through stable log determinants.

The isotropic asymptotes are

\[
V(a)=\sigma_x^2
\left[1-D\frac{a^2}{\ell^2}+O(a^4/\ell^4)\right]
\quad(a\ll\ell),
\]

and

\[
V(a)=\sigma_x^2 2^{-D/2}
\left(\frac{\ell}{a}\right)^D
\left[1-\frac D4\frac{\ell^2}{a^2}+O(\ell^4/a^4)\right]
\quad(a\gg\ell).
\]

## 3. Exact one-scale no-go result

Suppose one experiment reports \(V_*\) at scale \(a_*\). For every positive \(\ell\), define

\[
\boxed{
\sigma_x^2(\ell)=V_*
\left(1+\frac{2a_*^2}{\ell^2}\right)^{D/2}
}.
\]

Substitution returns exactly \(V_*\). Thus one scale supplies only one combination of two microscopic parameters:

\[
\boxed{
\text{one probe scale cannot separately identify }\sigma_x^2\text{ and }\ell.
}
\]

This is structural non-identifiability, not inadequate numerical precision.

## 4. Exact two-scale inverse

For distinct scales,

\[
V_i=\sigma_x^2
\left(1+\frac{2a_i^2}{\ell^2}\right)^{-D/2},
\qquad i=1,2.
\]

Define

\[
q=\left(\frac{V_1}{V_2}\right)^{2/D}.
\]

Then

\[
q=\frac{1+2a_2^2/\ell^2}{1+2a_1^2/\ell^2},
\]

so

\[
\boxed{
\ell^2=2\frac{a_2^2-qa_1^2}{q-1}
}
\]

and

\[
\boxed{
\sigma_x^2=V_1
\left(1+\frac{2a_1^2}{\ell^2}\right)^{D/2}.
}
\]

The inverse is exact under the declared covariance, kernel, and dimension. It does not test those assumptions.

## 5. Conditioning theorem

Use logarithmic outputs and parameters,

\[
y_i=\ln V_i,
\qquad
\theta=(\ln\sigma_x^2,\ln\ell).
\]

The Jacobian row is

\[
\boxed{
J_i=(1,g_i),
\qquad
g_i=D\frac{2a_i^2/\ell^2}{1+2a_i^2/\ell^2}.
}
\]

Hence

\[
\det J=g_2-g_1.
\]

The inverse becomes singular or badly conditioned when:

1. \(a_1=a_2\);
2. both \(a_i\ll\ell\), where \(g_i\to0\);
3. both \(a_i\gg\ell\), where \(g_i\to D\).

A useful experiment places one scale below and one above the correlation length. For \(D=2\) and \(\ell=5\,\mu\mathrm m\):

| Probe scales | Log-parameter condition number |
|---|---:|
| 5 and 5.05 µm | 632.90 |
| 0.5 and 50 µm | 2.683 |
| 2.5 and 10 µm | 4.838 |
| 50 and 500 µm | 1011.13 |

Large scale separation alone is not sufficient; the pair must sample different sensitivity regimes.

## 6. Exact one-dimensional top-hat kernels

For a normalized top-hat window of length \(L\), stationarity gives

\[
\boxed{
V_L=\frac{2}{L^2}\int_0^L(L-h)C_x(h)\,dh.
}
\]

For Gaussian covariance,

\[
\boxed{
V_{L,G}=\frac{2\sigma_x^2}{L^2}
\left[
L\ell\sqrt{\frac\pi2}
\operatorname{erf}\left(\frac{L}{\sqrt2\ell}\right)
-\ell^2\left(1-e^{-L^2/(2\ell^2)}\right)
\right].
}
\]

For exponential covariance,

\[
\boxed{
V_{L,E}=\frac{2\sigma_x^2}{L^2}
\left[
L\ell-\ell^2\left(1-e^{-L/\ell}\right)
\right].
}
\]

The two models share the point-probe limit but differ at finite scale. A multi-scale inversion is therefore covariance-family dependent.

## 7. Propagation through a signed HgCdTe gap law

Let \(G_a=E_g(X_a,T)\) and \(V_a=\operatorname{Var}(X_a)\). A quadratic expansion around \(\bar x\) gives

\[
E_g(\bar x+\delta,T)
\simeq E_0+E_x\delta+\frac12E_{xx}\delta^2.
\]

For Gaussian \(\delta\),

\[
\boxed{
\mathbb E[G_a]\simeq E_0+\frac12E_{xx}V_a
}
\]

and

\[
\boxed{
\operatorname{Var}(G_a)\simeq
E_x^2V_a+\frac12E_{xx}^2V_a^2.
}
\]

The variance result is exact for a quadratic composition dependence. To first order,

\[
\sigma_{G,a}\simeq
|E_x|\sigma_x
\left(1+\frac{2a^2}{\ell^2}\right)^{-D/4}.
\]

For \(\lambda_c=hc/E_c\),

\[
\boxed{
\sigma_{\lambda_c}\simeq
\frac{\lambda_c}{|E_c|}\sigma_{E_c}.
}
\]

## 8. Quantitative HgCdTe sensitivity screen

Declare

\[
D=2,
\quad \sigma_x=0.005,
\quad \ell=5\,\mu\mathrm m,
\quad |E_x|=1.7191085\,\mathrm{eV}.
\]

The same microscopic field then gives:

| Gaussian probe sigma | Effective composition sigma | Linearized gap sigma | 10-µm cutoff sigma |
|---:|---:|---:|---:|
| 1 µm | 0.004811 | 8.271 meV | 0.6671 µm |
| 5 µm | 0.002887 | 4.963 meV | 0.4003 µm |
| 10 µm | 0.001667 | 2.865 meV | 0.2311 µm |
| 100 µm | 0.0001767 | 0.304 meV | 0.02450 µm |

The apparent standard deviation changes by a factor of

\[
\boxed{27.2336}
\]

between 1 and 100 µm probe scales without changing the underlying specimen model.

This is large enough to alter comparisons among micro-FTIR, wafer FTIR, PL, mapped detector cutoff, and pixel/device distributions. The values remain a sensitivity calculation until specimen-specific covariance and measurement kernels are established.

## 9. Claim boundary

The general filtering identity and Gaussian integration are established mathematics. The candidate contribution is narrower:

1. an explicit HgCdTe spatial-disorder observation layer;
2. an exact one-scale no-go result and constructive multi-scale design;
3. quantitative demonstration that realistic probe changes can alter apparent gap/cutoff widths materially;
4. explicit separation of microscopic variance, probe-averaged variance, Urbach energy, PL linewidth, and cutoff spread;
5. source-grounded measurement requirements.

No journal submission is authorized until prior-art, uncertainty, covariance-family, and manuscript-strength gates pass.
