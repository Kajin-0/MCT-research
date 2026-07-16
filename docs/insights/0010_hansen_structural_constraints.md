# Insight 0010 — Structural constraints of the Hansen baseline

**Status:** exact consequences of the published functional form  
**Novelty status:** not a new physical result; benchmark diagnostic  
**Data dependency:** none for the derivation, experimental data required for falsification

The Hansen baseline is

$$
E_g(x,T)=P_3(x)+aT(1-2x),
$$

where

$$
P_3(x)=-0.302+1.93x-0.81x^2+0.832x^3,
\qquad
a=5.35\times10^{-4}\ \mathrm{eV/K}.
$$

Its apparent flexibility hides strong, testable restrictions.

## 1. Temperature dependence is exactly affine

At every fixed composition,

$$
\frac{\partial E_g}{\partial T}=a(1-2x),
$$

and

$$
\boxed{
\frac{\partial^2E_g}{\partial T^2}=0
}
$$

for all $x$ and $T$.

Therefore the model forbids:

- low-temperature Bose–Einstein curvature;
- crossover between acoustic and optical phonon scales;
- temperature-dependent thermal-expansion slope;
- anharmonic curvature;
- any temperature-dependent change in the effective coupling coefficient.

A statistically resolved nonzero temperature curvature at fixed $x$ falsifies the functional form, not merely its coefficients.

## 2. The temperature coefficient is constrained to one linear function of composition

The model requires

$$
\boxed{
\alpha_T(x)=\frac{\partial E_g}{\partial T}=a(1-2x)
}
$$

with a single zero at

$$
x=\frac12.
$$

Thus it predicts a temperature-independent gap at $x=0.5$ and opposite temperature slopes on either side. The mixed derivative is globally constant:

$$
\boxed{
\frac{\partial^2E_g}{\partial x\,\partial T}=-2a
=-1.07\times10^{-3}\ \mathrm{eV/(K\,composition)}.
}
$$

Any curvature of the measured temperature coefficient versus composition falsifies this restriction.

## 3. Temperature and composition are not separable, but their coupling has rank one

The complete temperature dependence occupies only the basis function

$$
T(1-2x).
$$

In a linear-model design matrix, every temperature-dependent datum informs one global coefficient $a$. The model cannot distinguish separate HgTe-like, CdTe-like, acoustic, optical, thermal-expansion, or disorder contributions.

This is important statistically: a small residual may reflect limited temperature/composition coverage rather than physical adequacy.

## 4. Composition sensitivity

The composition derivative is

$$
\frac{\partial E_g}{\partial x}
=1.93-1.62x+2.496x^2-2aT.
$$

Near detector-relevant compositions the derivative is large. For example:

| $x$ | $\partial E_g/\partial x$ at 77 K | at 300 K |
|---:|---:|---:|
| 0.15 | 1.661 eV | 1.422 eV |
| 0.20 | 1.623 eV | 1.385 eV |
| 0.25 | 1.599 eV | 1.360 eV |
| 0.30 | 1.586 eV | 1.348 eV |

Therefore a composition uncertainty $\sigma_x=0.001$ already corresponds to roughly

$$
\sigma_{E,x}
\approx
\left|\frac{\partial E_g}{\partial x}\right|\sigma_x
\sim1.3\text{–}1.7\ \mathrm{meV}
$$

in this range. A claimed sub-meV equation cannot be validated unless composition uncertainty is substantially below $10^{-3}$ or is modeled explicitly.

## 5. Critical-composition trajectory

Define the signed-gap transition by

$$
E_g(x_c(T),T)=0.
$$

Implicit differentiation gives

$$
\boxed{
\frac{dx_c}{dT}
=-\frac{a(1-2x_c)}
{1.93-1.62x_c+2.496x_c^2-2aT}
}.
$$

The Hansen baseline predicts:

| $T$ (K) | $x_c(T)$ |
|---:|---:|
| 0 | 0.16608 |
| 77 | 0.14945 |
| 150 | 0.13224 |
| 225 | 0.11292 |
| 300 | 0.09178 |

and the local slope becomes more negative with temperature, from approximately

$$
-2.07\times10^{-4}\ \mathrm{K^{-1}}
$$

at 0 K to

$$
-2.95\times10^{-4}\ \mathrm{K^{-1}}
$$

at 300 K.

This trajectory is a stronger validation target than isolated gap values because it probes the coupled $x$–$T$ structure directly.

## 6. Exact falsification hierarchy

The benchmark should test the Hansen assumptions in this order:

1. **Affine-$T$ test:** is $\partial^2E_g/\partial T^2$ resolved as nonzero at fixed composition?
2. **Linear-composition slope test:** is $\partial E_g/\partial T$ nonlinear in $x$?
3. **Common-coefficient test:** can one coefficient $a$ explain all source-consistent compositions?
4. **Critical-trajectory test:** does the measured $x_c(T)$ agree with the implicit Hansen trajectory?
5. **Residual-source test:** are apparent violations actually caused by mixed gap definitions or composition bias?

Only after source and measurement heterogeneity are controlled should curvature be interpreted as electron–phonon physics.

## 7. Consequence for the analytical successor

A minimal physical successor should add only the degrees of freedom required by rejected Hansen constraints. For example:

$$
E_g(x,T)=E_g(x,0)
+A(x)\left[\coth\left(\frac{\Theta(x)}{2T}\right)-1\right]
+\Delta E_g^{\mathrm{QH}}(x,T),
$$

but the oscillator scale $\Theta(x)$ is justified only if held-out data resolve temperature curvature beyond composition and measurement uncertainty.

The immediate analytical question is therefore not “Can a more complicated equation fit better?” It is:

> Which exact Hansen constraint is rejected by provenance-controlled data, by how many meV, and over what composition–temperature domain?
