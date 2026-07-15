# Insight 0003 — Reduce the phonon spectrum, not the temperature variable

**Status:** proposed analytical strategy  
**Novelty:** unconfirmed  
**Purpose:** create a physically interpretable successor to free polynomial temperature fits

## Exact harmonic structure

At fixed volume, the thermal electron–phonon contribution to the signed gap can be written as

\[
\Delta_T E_g^{\mathrm{ep}}(x,T)
=2\int_0^\infty d\omega\,
\mathcal F_g(x,\omega)n_B(\omega,T),
\]

where \(\mathcal F_g\) is a signed gap-coupling spectral density containing the difference between the \(\Gamma_6\) and \(\Gamma_8\) Fan and Debye–Waller responses.

The empirical problem is therefore not fundamentally “what polynomial in \(T\) fits the data?” It is “how many spectral degrees of freedom are needed to represent \(\mathcal F_g\) over the desired temperature interval?”

## Effective-oscillator reduction

Approximate the spectral density by

\[
\mathcal F_g(x,\omega)
\approx
\sum_{j=1}^{N_\mathrm{osc}}
A_j(x)\delta[\omega-\Omega_j(x)].
\]

Then

\[
\boxed{
\Delta_T E_g^{\mathrm{ep}}(x,T)
\approx
\sum_{j=1}^{N_\mathrm{osc}}
A_j(x)
\left[
\coth\left(\frac{\Theta_j(x)}{2T}\right)-1
\right]
}
\]

with

\[
\Theta_j=\frac{\hbar\Omega_j}{k_B}.
\]

This representation automatically has the correct zero-temperature thermal limit and approaches linear behavior only in the classical occupation regime.

## Stronger reduction by spectral moments

Define signed moments

\[
\mu_n(x)=\int_0^\infty d\omega\,
\omega^n\mathcal F_g(x,\omega).
\]

Rather than fitting \(A_j\) and \(\Theta_j\) freely at every composition, choose the smallest oscillator set reproducing selected moments and the computed \(E_g(T)\) curve within tolerance.

Candidate constraints include:

\[
\sum_j A_j=\mu_0,
\qquad
\sum_j A_j\Omega_j=\mu_1,
\qquad
\sum_j A_j\Omega_j^2=\mu_2.
\]

Because \(\mathcal F_g\) is signed, positive-only quadrature assumptions are not automatically valid. Opposing Fan, Debye–Waller, acoustic, and optical contributions may require signed oscillator weights.

## Composition dependence

Instead of fitting a free two-dimensional polynomial in \((x,T)\), interpolate physically meaningful functions:

\[
E_g(x,0),\quad
A_j(x),\quad
\Theta_j(x),\quad
a_g(x),\quad
\alpha_V(x,T).
\]

Endpoint and smoothness constraints can be imposed using HgTe and CdTe calculations. Alloy disorder can be represented by a separate uncertainty or spectral-width model rather than silently absorbed into the mean equation.

## Candidate final analytical form

\[
\boxed{
E_g(x,T)=E_g(x,0)
+\sum_j A_j(x)
\left[
\coth\left(\frac{\Theta_j(x)}{2T}\right)-1
\right]
+\Delta E_g^{\mathrm{QH}}(x,T)
}
\]

with

\[
\Delta E_g^{\mathrm{QH}}(x,T)
=a_g(x)\int_0^T\alpha_V(x,T')\,dT'.
\]

## Tests

1. Determine the minimum \(N_\mathrm{osc}\) required for <1 meV reduction error against the full AHC curve.
2. Compare one-, two-, and three-oscillator models using held-out temperatures.
3. Verify low- and high-temperature asymptotics.
4. Compare residuals with Hansen, Varshni, and unconstrained polynomial baselines.
5. Test whether fitted oscillator parameters track recognizable acoustic, Hg–Te-like, and Cd–Te-like phonon sectors.

## Failure mode to avoid

If the oscillator parameters are fitted only to experimental \(E_g(T)\) without first-principles or spectroscopic constraints, the model may be a reparameterized empirical fit rather than a physical derivation.
