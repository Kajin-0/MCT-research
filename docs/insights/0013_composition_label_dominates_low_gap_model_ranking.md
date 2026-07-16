# Insight 0013 — Composition-label ambiguity dominates low-gap model testing

**Status:** exact comparison using values stated explicitly by Teppe et al.  
**Novelty status:** validation and identifiability result, not a new bandgap law.  
**Scope:** one specimen and two historical equations.

## 1. Observation

Teppe et al. report for Sample A at 2 K a signed Kane gap

$$
E_g^{\mathrm{obs}}=5\pm2\ \mathrm{meV}.
$$

The sample is labeled

$$
x=0.175
$$

in the main discussion and figures, but

$$
x=0.17
$$

in the methods.

The difference is only

$$
\Delta x=0.005,
$$

but HgCdTe has a large composition derivative near the inversion regime.

## 2. Legacy-model predictions

| Model | Prediction at $x=0.170$ | Prediction at $x=0.175$ | Change from label alone |
|---|---:|---:|---:|
| Hansen | 7.48 meV | 16.10 meV | 8.61 meV |
| Laurenti | 2.97 meV | 12.08 meV | 9.11 meV |

The label-induced shifts are more than four times the stated experimental standard uncertainty of 2 meV.

The corresponding measured-minus-predicted residuals are:

| Model | Residual at $x=0.170$ | Residual at $x=0.175$ |
|---|---:|---:|
| Hansen | $-2.48$ meV | $-11.10$ meV |
| Laurenti | $+2.03$ meV | $-7.08$ meV |

At $x=0.170$, both equations are compatible with the explicit point at approximately the one-sigma level. At $x=0.175$, both overpredict it by several standard deviations.

The scientific conclusion changes from “both models are plausible” to “both models fail this point” solely through the unresolved composition label.

## 3. Consequence for model ranking

The point cannot be used as a conventional residual with exact $x$. The correct likelihood must include a specimen-level latent composition:

$$
x_A^{\mathrm{true}}\sim p(x_A\mid\text{growth and metrology records}),
$$

and both the 2 K Landau-level point and the low-temperature absorption point must share the same $x_A^{\mathrm{true}}$.

It is invalid to optimize a different composition offset for each temperature or measurement class.

## 4. General discrimination criterion

For two equations $M_1$ and $M_2$, composition is sufficiently controlled only when

$$
\left|\frac{\partial E_g}{\partial x}\right|\sigma_x
\ll
\left|E_g^{M_1}-E_g^{M_2}\right|
$$

and also smaller than the target residual accuracy.

At the Sample A point, Hansen and Laurenti differ by only

$$
4.02\text{–}4.52\ \mathrm{meV},
$$

depending on which nominal composition is used. With local composition derivatives of order 1.7 eV, three-sigma discrimination between the equations from a single gap point would require approximately

$$
\sigma_x\lesssim8\times10^{-4},
$$

before including gap-extraction and model uncertainty.

## 5. Broader implication

A future “more accurate” analytical HgCdTe equation can easily appear superior by absorbing composition calibration offsets. Therefore all reported improvements must include:

1. specimen-level composition uncertainty;
2. source-level composition offsets;
3. held-out specimens for which no gap-informed composition adjustment is allowed;
4. comparison of residual reduction against the composition-induced error floor;
5. explicit separation between independently measured $x$ and $x$ inferred from a bandgap equation.

The immediate research bottleneck is not an additional polynomial coefficient. It is whether the available historical data know composition accurately enough to distinguish analytical models at the claimed meV scale.
