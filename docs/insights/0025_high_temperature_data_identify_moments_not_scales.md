# Insight 0025: high-temperature data identify thermal moments before oscillator scales

## Question

The two-scale Laurenti surrogate fit improved held-out predictions but selected different scale pairs across temperature folds:

| Held-out range | Selected scales | Training condition number |
|---|---:|---:|
| $T\le40$ K | $(15,320)$ K | 13,883 |
| $40<T\le200$ K | $(15,160)$ K | 5,354 |
| $T>200$ K | $(20,160)$ K | 1,603 |

Does this scale movement imply that the thermal representation contains no stable information?

No. The leading inverse-scale moment is substantially more stable than the individual scales.

## Observable moment

For

$$
\Delta E(T)
=
\sum_j A_j
\left[
\coth\left(\frac{\Theta_j}{2T}\right)-1
\right],
$$

the high-temperature slope is

$$
\boxed{
s_\infty(x)
=
2\sum_j\frac{A_j(x)}{\Theta_j}
}.
$$

This is the moment $2\mu_{-1}(x)$.

The Laurenti target has exact asymptotic slope

$$
s_\infty^{\mathrm L}(x)
=
10^{-4}
\left[
6.3-15.47x+5.92x^2
\right]
\ \mathrm{eV/K}.
$$

## Numerical result

### HgTe endpoint, $x=0$

| Held-out range | Selected scales | Fitted slope | Laurenti target |
|---|---:|---:|---:|
| low temperature | $(15,320)$ K | 0.63059 meV/K | 0.63000 meV/K |
| intermediate temperature | $(15,160)$ K | 0.63317 meV/K | 0.63000 meV/K |
| high temperature | $(20,160)$ K | 0.63178 meV/K | 0.63000 meV/K |

The second scale moves by a factor of two, but the leading slope moment spans only

$$
0.00258\ \mathrm{meV/K}.
$$

### Detector-relevant composition, $x=0.2$

| Held-out range | Fitted slope | Laurenti target |
|---|---:|---:|
| low temperature | 0.34420 meV/K | 0.34428 meV/K |
| intermediate temperature | 0.34495 meV/K | 0.34428 meV/K |
| high temperature | 0.34310 meV/K | 0.34428 meV/K |

### CdTe endpoint, $x=1$

| Held-out range | Fitted slope | Laurenti target |
|---|---:|---:|
| low temperature | $-0.32170$ meV/K | $-0.32500$ meV/K |
| intermediate temperature | $-0.31544$ meV/K | $-0.32500$ meV/K |
| high temperature | $-0.30261$ meV/K | $-0.32500$ meV/K |

The endpoint slope becomes less stable when the high-temperature range itself is withheld, as expected, but remains far more interpretable than the individual scale pair.

## Higher moments are not equally stable

The next inverse-temperature coefficient is

$$
\frac{\mu_1(x)}{6T},
\qquad
\mu_1(x)=\sum_j A_j(x)\Theta_j.
$$

At $x=1$, the fitted coefficient $\mu_1/6$ changes across folds from approximately

$$
-1026\ \mathrm{meV\,K}
$$

to

$$
-450\ \mathrm{meV\,K}.
$$

Thus the data screen identifies the leading slope moment much more strongly than the higher curvature moment.

## Interpretation

The previous conclusion

> two fixed scales are representationally capable but not physically identified

can now be sharpened:

$$
\boxed{
\text{the leading thermal moment is identifiable before the discrete scale decomposition}
}
$$

The moving scale pairs are alternative coordinate representations of approximately the same leading thermal response.

## Consequence for the analytical model

The next experimental benchmark should report, in order:

1. held-out predictions;
2. the composition-dependent leading moment $\mu_{-1}(x)$;
3. higher moments only when stable across folds;
4. individual oscillator scales only when low-temperature data resolve their exponential activation.

If individual scales remain unstable while moments are stable, use a spectral-moment or regularized thermal-basis model rather than assigning phonon energies to the fitted scales.

## Computation consequence

A future CdTe AHC pilot should export the gap-coupling spectral density or enough frequency-resolved information to calculate

$$
\mu_p^{\mathrm{AHC}}
=
\int d\omega\,g_{E_g}(\omega)\Theta(\omega)^p.
$$

The first comparison should be between calculated and experimentally inferred moments—not between an arbitrary fitted discrete oscillator and one selected phonon frequency.

## Reproducibility

- derivation: `docs/derivations/007_oscillator_thermal_moments.md`;
- executable study: `tools/run_laurenti_surrogate_moment_stability.py`;
- numerical table: `data/validation/laurenti_surrogate_thermal_moment_stability.csv`.
