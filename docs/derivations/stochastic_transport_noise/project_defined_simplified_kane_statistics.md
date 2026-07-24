# R06 project-defined simplified Kane statistics

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Status:** dimensionless mathematical prototype; not an HgCdTe material closure

## 1. Purpose

PR #381 established that density and chemical compressibility must be returned by one thermodynamically consistent statistics closure. The historic Madarasz/Lowney equations remain unavailable at symbol-exact implementation quality.

This derivation defines an independent project benchmark based on the simplified isotropic Kane dispersion

\[
E(1+\alpha E)=\frac{\hbar^2k^2}{2m^*}.
\]

This relation captures one standard form of conduction-band nonparabolicity. It is not the complete three-band HgCdTe model described by the 1991 NIST precursor and is not claimed to reproduce Madarasz or Lowney.

## 2. Density of states

Including spin degeneracy, the number of states per unit volume inside a sphere of radius `k` is

\[
\mathcal N(k)=\frac{k^3}{3\pi^2}.
\]

Therefore

\[
g(E)=\frac{d\mathcal N}{dE}
=\frac{1}{\pi^2}k^2\frac{dk}{dE}.
\]

From the simplified dispersion,

\[
k(E)=\left(\frac{2m^*}{\hbar^2}\right)^{1/2}
\sqrt{E(1+\alpha E)},
\]

and

\[
\frac{dk}{dE}
=\frac{1}{2}
\left(\frac{2m^*}{\hbar^2}\right)^{1/2}
\frac{1+2\alpha E}{\sqrt{E(1+\alpha E)}}.
\]

Thus

\[
g(E)=
\frac{1}{2\pi^2}
\left(\frac{2m^*}{\hbar^2}\right)^{3/2}
\sqrt{E(1+\alpha E)}(1+2\alpha E).
\]

At `alpha=0`, this reduces exactly to the three-dimensional parabolic density of states.

## 3. Dimensionless normalization

Define

\[
\epsilon=\frac{E}{k_BT},
\qquad
\eta=\frac{\mu-E_c}{k_BT},
\qquad
\beta=\alpha k_BT.
\]

Let `N_*` denote the explicit parabolic density scale that would multiply the normalized complete Fermi integral `F_{1/2}`. Then

\[
n=N_* I_n(\eta,\beta),
\]

where

\[
I_n(\eta,\beta)
=\frac{2}{\sqrt\pi}
\int_0^\infty
\frac{
\sqrt{\epsilon(1+\beta\epsilon)}
(1+2\beta\epsilon)
}
{1+\exp(\epsilon-\eta)}
\,d\epsilon.
\]

The normalization is chosen so that

\[
I_n(\eta,0)=\mathcal F_{1/2}(\eta).
\]

The present prototype supplies `N_*` explicitly. It does not infer it from an HgCdTe effective-mass relation.

## 4. Chemical compressibility

Differentiating with respect to chemical potential gives

\[
\frac{\partial n}{\partial\mu}
=\frac{N_*}{k_BT}I_\chi(\eta,\beta),
\]

with

\[
I_\chi(\eta,\beta)
=\frac{2}{\sqrt\pi}
\int_0^\infty
\sqrt{\epsilon(1+\beta\epsilon)}
(1+2\beta\epsilon)
f(1-f)
\,d\epsilon,
\]

where

\[
f=\frac{1}{1+\exp(\epsilon-\eta)}.
\]

By construction,

\[
I_\chi=\frac{\partial I_n}{\partial\eta}.
\]

At `beta=0`, integration by parts gives

\[
I_\chi(\eta,0)=\mathcal F_{-1/2}(\eta).
\]

## 5. Generalized Einstein factor

The thermodynamic factor consumed by the transport architecture is

\[
\Theta
=\frac{n}{k_BT\,\partial n/\partial\mu}
=\frac{I_n}{I_\chi}.
\]

This identity is evaluated from the same quadrature as density and compressibility. No independent fitted Einstein correction is permitted.

In the nondegenerate limit, `f << 1` and `f(1-f) -> f`, so

\[
\Theta\rightarrow1
\]

for any fixed nonparabolic density of states.

## 6. Numerical transformation

Use

\[
\epsilon=y^2,
\qquad
 d\epsilon=2y\,dy.
\]

The density integral becomes

\[
I_n
=\frac{4}{\sqrt\pi}
\int_0^\infty
 y^2
 \sqrt{1+\beta y^2}
 (1+2\beta y^2)
 f(y^2;\eta)
\,dy.
\]

This removes the square-root endpoint and permits fixed Gauss-Legendre quadrature on a tail-truncated interval. The same nodes and density-of-states factor are used for `I_chi`.

## 7. Accepted checks

The prototype must demonstrate:

1. positivity of the density-of-states factor;
2. exact parabolic reduction as `alpha -> 0`;
3. analytical compressibility agreement with a centered density derivative;
4. monotonic density versus reduced chemical potential;
5. Boltzmann-limit recovery of `Theta -> 1`;
6. quadrature refinement stability;
7. linear scaling with the explicit density scale;
8. agreement with frozen high-precision dimensionless reference points;
9. compliance with the merged carrier-statistics protocol.

## 8. Scientific boundary

This derivation does not establish:

- an HgCdTe value or formula for `alpha`;
- an HgCdTe effective mass or density scale;
- split-off-band coupling;
- heavy-hole neutrality;
- the full three-band secular equation;
- equivalence to Madarasz 1985 or Lowney 1992;
- material-accurate intrinsic density or susceptibility;
- predictive screening, transport, or noise.

The prototype is an architecture and reduction benchmark only.

## 9. Source identity

The primary historical origin of narrow-gap `k.p` nonparabolicity is E. O. Kane, *Journal of Physics and Chemistry of Solids* **1**, 249-261 (1957), DOI `10.1016/0022-3697(57)90013-6`.

The explicit simplified dispersion used here is treated as the project model form associated with the simplified Kane relation discussed by B. R. Nag and A. N. Chakravarti, *physica status solidi (b)* **71**, K45-K48 (1975), DOI `10.1002/pssb.2220710153`.

Those citations support the model identity and lineage. They do not supply HgCdTe parameter validation for this implementation.
