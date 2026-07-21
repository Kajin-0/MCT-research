# Derivation 016: Gaussian-disorder tails are only locally exponential

## Scope

This derivation belongs to the distributional band-edge observables program, contribution R03 and Issue #225.

It analyzes the controlled observation model

\[
\alpha_p(E)
=
A\,\mathbb E[(E-G)_+^p],
\qquad
G\sim\mathcal N(\mu_G,\sigma_G^2),
\qquad p\ge0.
\]

The model represents a sharp local power-law edge averaged over a Gaussian distribution of local gaps. It is not a complete HgCdTe absorption theory and does not establish the microscopic origin of a measured tail.

## Dimensionless reduction

Define

\[
z=\frac{E-\mu_G}{\sigma_G}
\]

and set

\[
t=\frac{E-G}{\sigma_G}.
\]

Then

\[
\boxed{
\alpha_p(E)=A\sigma_G^p F_p(z)
}
\]

with

\[
F_p(z)
=
\int_0^\infty t^p\phi(z-t)\,dt,
\]

where

\[
\phi(y)=\frac{1}{\sqrt{2\pi}}e^{-y^2/2}.
\]

All differential lineshape information therefore depends only on \(z\) and \(p\). The amplitude \(A\) cancels from logarithmic derivatives, while \(\sigma_G\) supplies the energy scale.

## Exact derivative identities

Differentiate the Gaussian kernel rather than the thresholded power:

\[
\frac{\partial}{\partial z}\phi(z-t)
=-(z-t)\phi(z-t)
=(t-z)\phi(z-t).
\]

Therefore

\[
\begin{aligned}
F_p'(z)
&=\int_0^\infty t^p(t-z)\phi(z-t)\,dt\\
&=F_{p+1}(z)-zF_p(z).
\end{aligned}
\]

Thus

\[
\boxed{
F_p'=F_{p+1}-zF_p
}.
\]

Differentiate once more:

\[
\begin{aligned}
F_p''
&=F_{p+1}'-F_p-zF_p'\\
&=F_{p+2}-zF_{p+1}-F_p-z(F_{p+1}-zF_p),
\end{aligned}
\]

so

\[
\boxed{
F_p''
=F_{p+2}-2zF_{p+1}+(z^2-1)F_p
}.
\]

These identities evaluate the differential tail using three nonnegative Gaussian moments. No finite difference of \(\log\alpha\) is required.

## Local apparent tail energy

Let

\[
L(E)=\log\alpha_p(E).
\]

Then

\[
\frac{dL}{dE}
=\frac{1}{\sigma_G}\frac{F_p'}{F_p}.
\]

Define the local apparent exponential energy by

\[
W_{\rm loc}(E)
=\left(\frac{dL}{dE}\right)^{-1}.
\]

Hence

\[
\boxed{
\frac{W_{\rm loc}}{\sigma_G}
=\frac{F_p}{F_p'}
}.
\]

A true Urbach exponential

\[
\alpha_U(E)=\alpha_0\exp(E/W_U)
\]

has constant \(W_{\rm loc}=W_U\).

## Log-concavity theorem

The Gaussian density is log-concave. The one-sided power function

\[
h_p(y)=y_+^p
\]

is log-concave for every \(p\ge0\): for \(p>0\), \(\log h_p=p\log y\) is concave on its convex support \(y>0\); for \(p=0\), \(h_0\) is the indicator of a half-line.

The absorption is the convolution

\[
\alpha_p(E)=A(h_p*f_G)(E).
\]

The convolution of log-concave functions is log-concave by the established Prékopa-Leindler result. Therefore

\[
\boxed{
\frac{d^2\log\alpha_p}{dE^2}\le0
}.
\]

Since \(d\log\alpha_p/dE>0\) in the subgap tail,

\[
\frac{dW_{\rm loc}}{dE}
=-
\frac{d^2\log\alpha_p/dE^2}
{(d\log\alpha_p/dE)^2}
\ge0.
\]

Thus

\[
\boxed{
W_{\rm loc}(E)\text{ is nondecreasing with photon energy.}
}
\]

The distributed-gap spectrum can resemble an exponential over a finite interval, but its local exponential energy cannot remain constant over the complete tail.

## Deep-subgap asymptotic

Set

\[
z=-a,
\qquad a>0.
\]

Then

\[
F_p(-a)
=\int_0^\infty t^p\phi(a+t)\,dt
=\phi(a)\int_0^\infty t^p e^{-at-t^2/2}\,dt.
\]

Use \(y=at\):

\[
F_p(-a)
=\phi(a)a^{-(p+1)}
\int_0^\infty y^p e^{-y}e^{-y^2/(2a^2)}\,dy.
\]

As \(a\to\infty\), dominated convergence gives

\[
\boxed{
F_p(z)
\sim
\Gamma(p+1)\phi(z)(-z)^{-(p+1)},
\qquad z\to-\infty.
}
\]

The next correction follows by expanding \(e^{-y^2/(2a^2)}\):

\[
F_p(-a)
=
\Gamma(p+1)\phi(a)a^{-(p+1)}
\left[
1-
\frac{(p+1)(p+2)}{2a^2}
+O(a^{-4})
\right].
\]

Therefore

\[
\log F_p(z)
=-\frac{z^2}{2}
-(p+1)\log(-z)
+\text{constant}
+O(z^{-2}).
\]

Differentiation gives

\[
\boxed{
\frac{d\log F_p}{dz}
=-z-\frac{p+1}{z}+O((-z)^{-3})
}
\]

and

\[
\boxed{
\frac{d^2\log F_p}{dz^2}
=-1+\frac{p+1}{z^2}+O((-z)^{-4}).
}
\]

In physical units,

\[
\boxed{
\frac{d^2\log\alpha_p}{dE^2}
\longrightarrow
-\frac{1}{\sigma_G^2}
}
\]

and

\[
\boxed{
\frac{W_{\rm loc}}{\sigma_G}
\sim
\left[-z-\frac{p+1}{z}\right]^{-1}.
}
\]

A true exponential has zero log curvature. The Gaussian-disorder tail instead approaches curvature \(-1/\sigma_G^2\). Its deepest subgap behavior is Gaussian with an algebraic prefactor, not Urbach-exponential.

## Herrmann square-root benchmark

For \(p=1/2\), the dimensionless local tail energy changes substantially across the subgap domain:

```text
z       W_local / sigma_G     sigma_G^2 d2 log(alpha)/dE2
-8      0.12223768            -0.97895032
-6      0.16038506            -0.96519098
-4      0.23088740            -0.93409938
-2      0.39483481            -0.84918406
 0      0.95597762            -0.59421979
```

Between \(z=-6\) and \(z=0\), the local apparent tail energy increases by a factor of approximately \(5.96\). This differential result explains why the same convolved spectrum produced distinct high-\(R^2\) fitted tail energies in PR #172 when the absorption fitting window changed.

## Experimental interpretation

The theorem supplies a falsification diagnostic, not a mechanism identification:

- a constant local tail energy is compatible with a true exponential over the resolved interval;
- systematic increase of local tail energy is expected from the Gaussian distributed-gap power-edge model;
- positive log curvature cannot be produced by this log-concave model family;
- finite spectral range, noise, baseline error, and instrumental convolution can obscure curvature;
- observing the predicted curvature does not prove composition disorder because other mechanisms may produce similar finite-window behavior.

A practical comparison should fit several nonoverlapping windows or estimate a regularized derivative of \(\log\alpha\), then compare the trend against the model prediction with the full measurement covariance.

## Claim boundary

The Prékopa-Leindler theorem and generic convolution log-concavity are established mathematics. The project-specific result is their explicit application, differential implementation, deep-tail asymptotic, and HgCdTe observation consequence for the controlled Gaussian-gap power-edge operator.

This derivation does not identify:

- a specimen gap distribution;
- a composition variance;
- a spatial correlation length;
- an Urbach microscopic mechanism;
- a PL or quasiparticle linewidth;
- a complete Kane, excitonic, phonon, defect, or free-carrier absorption law.
