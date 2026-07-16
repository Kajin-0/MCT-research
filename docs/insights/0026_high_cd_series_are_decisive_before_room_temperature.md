# Insight 0026: the high-Cd Laurenti series are decisive before room temperature

## Question

The direct Laurenti LPE series extend from approximately 2 to 300 K. Full-curve digitization is useful for model fitting, but it is not necessary for the first empirical decision:

> At what minimum temperature does a same-specimen thermal shift distinguish the Hansen and Laurenti laws at three standard deviations?

## Observable

For a fixed specimen and a 2 K reference, define

$$
D(x,T)
=
\left[E_g^{\mathrm L}(x,T)-E_g^{\mathrm L}(x,2)\right]
-
\left[E_g^{\mathrm H}(x,T)-E_g^{\mathrm H}(x,2)\right].
$$

This removes absolute intercept differences and most fixed source calibration offsets.

The nominal uncertainty model is

$$
\sigma_D^2
=
2\left(\sigma_E^2+\sigma_{\mathrm{digit}}^2\right)
+
\left(
\frac{\partial D}{\partial x}\sigma_x
\right)^2,
$$

with

$$
\sigma_E=3\ \mathrm{meV},
\qquad
\sigma_x=0.003.
$$

The 3 meV value is the article-level Laurenti edge-accuracy statement. It is used here as an experiment-design scale, not assigned as a verified independent uncertainty to every plotted point.

The threshold condition is

$$
\boxed{
|D(x,T)|\ge3\sigma_D
}.
$$

## Minimum temperatures without additional digitization uncertainty

| Direct series | Minimum $T$ for $3\sigma$ separation |
|---:|---:|
| $x=0.970$ | 34 K |
| $x=0.955$ | 36 K |
| $x=0.925$ | 39 K |
| $x=0.805$ | 63 K |
| $x=0.710$ | 119 K |
| $x=0.620$ | not reached by 300 K |
| $x=0.550$ | not reached by 300 K |
| $x=0.500$ | not reached by 300 K |

Thus the three highest-Cd direct specimen series should already discriminate the two thermal laws by approximately 40 K under the nominal uncertainty model.

Room-temperature points are not required for the first Hansen-versus-Laurenti shape decision.

## Robustness to digitization uncertainty

The minimum temperatures shift as follows when an independent digitization uncertainty is assigned to each plotted point:

| Series | 0 meV | 1 meV | 2 meV | 3 meV | 5 meV |
|---:|---:|---:|---:|---:|---:|
| $x=0.970$ | 34 K | 36 K | 42 K | 51 K | 74 K |
| $x=0.955$ | 36 K | 38 K | 44 K | 53 K | 78 K |
| $x=0.925$ | 39 K | 41 K | 48 K | 59 K | 87 K |
| $x=0.805$ | 63 K | 68 K | 81 K | 101 K | 156 K |
| $x=0.710$ | 119 K | 128 K | 156 K | 197 K | not reached |

Even with 5 meV digitization uncertainty per point, the three highest-Cd series remain decisive below 90 K.

## Null and intermediate controls

At 300 K, the nominal model separations are:

| $x$ | $|D(x,300\,\mathrm K)|$ | nominal significance |
|---:|---:|---:|
| 0.500 | 1.17 meV | 0.28$\sigma$ |
| 0.550 | 5.15 meV | 1.21$\sigma$ |
| 0.620 | 12.37 meV | 2.91$\sigma$ |
| 0.710 | 24.38 meV | 5.71$\sigma$ |
| 0.805 | 40.21 meV | 9.40$\sigma$ |
| 0.925 | 64.60 meV | 15.04$\sigma$ |
| 0.955 | 71.43 meV | 16.61$\sigma$ |
| 0.970 | 74.96 meV | 17.42$\sigma$ |

The $x=0.500$ series remains valuable as a null control because both equations predict weak temperature dependence. It tests extraction drift and systematic error rather than thermal-law separation.

The $x=0.620$ series is a near-threshold control: under the nominal model it reaches only 2.91 standard deviations at 300 K.

## Revised digitization strategy

The first-pass extraction need not digitize every marker in Figure 2.

Use the following sequence:

1. extract the 2 K anchor and one point near 40--60 K for $x=0.970$, 0.955, and 0.925;
2. extract an $x=0.500$ low/high pair as a systematic null control;
3. repeat each coordinate extraction independently to estimate digitization scatter;
4. only then digitize complete high-Cd curves for oscillator or moment fitting;
5. defer the lower-Cd inherited series until their composition provenance is reconstructed.

If the early high-Cd pairs do not show the predicted large separation, inspect coordinate calibration, marker assignment, specimen identity, and edge definition before adding model complexity.

## Limits

This calculation assumes:

- independent pointwise edge and digitization errors;
- one fixed specimen composition across temperature;
- a first-order composition-uncertainty propagation;
- the published equations as the two hypotheses;
- no additional correlated temperature-calibration or extraction bias.

Correlated errors may change the numerical significance. A constant energy offset cancels in the within-specimen shift, while a temperature-dependent systematic does not.

## Consequence

The efficient empirical decision is not

> digitize the entire historical figure before learning anything.

It is

$$
\boxed{
\text{use a few high-information same-specimen temperature pairs first}
}
$$

and deepen the digitization only if those pairs validate the expected signal scale.

## Reproducibility

- executable study: `tools/run_laurenti_series_minimum_temperature_design.py`;
- numerical table: `data/validation/laurenti_series_minimum_discrimination_temperature.csv`;
- source-series manifest: `data/laurenti/figure2_series_manifest.csv`.
