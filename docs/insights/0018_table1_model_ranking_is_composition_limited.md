# Insight 0018 — Hansen Table I cannot rank gap equations below the composition floor

**Status:** exact calculation using the 16 values printed in Hansen Table I.  
**Novelty status:** validation and identifiability result, not a new bandgap law.  
**Scope:** 80 K Tobin photodiode and Rawe photoconductor cutoff energies.

## 1. Nominal-composition residuals

Residuals are defined as

$$
r_i=E_{co,i}^{\mathrm{measured}}-E_g^{\mathrm{model}}(x_i,80\ \mathrm K).
$$

Using the published coefficients:

| Model | Mean residual | MAE | RMSE | Maximum absolute residual |
|---|---:|---:|---:|---:|
| Hansen | $-1.448$ meV | $2.158$ meV | $2.742$ meV | $4.985$ meV |
| Laurenti | $+2.899$ meV | $2.962$ meV | $3.776$ meV | $10.279$ meV |

At nominal reported composition, Hansen fits these points better. This is expected because the points were included in Hansen's historical evidence base. It is an in-sample result, not independent validation.

## 2. Composition sensitivity

Across the Table I range

$$
0.199\le x\le0.216,
$$

at 80 K, the local composition derivatives are approximately

$$
1.611\le
\frac{\partial E_g^{\mathrm H}}{\partial x}
\le1.621\ \mathrm{eV},
$$

and

$$
1.735\le
\frac{\partial E_g^{\mathrm L}}{\partial x}
\le1.743\ \mathrm{eV}.
$$

Hansen states that a typical historical composition variance near $x=0.2$ was

$$
\delta x=\pm0.003,
$$

which corresponds to an energy uncertainty of roughly

$$
4.8\text{–}5.2\ \mathrm{meV}.
$$

That uncertainty is larger than either model's nominal MAE and comparable to the maximum Hansen residual.

## 3. Diagnostic common-composition shifts

As an identifiability test only, optimize one common composition shift $\delta x$ against all 16 points. No claim is made that this is an independent composition calibration.

The results are:

| Model | Optimized $\delta x$ | MAE after shift | RMSE after shift |
|---|---:|---:|---:|
| Hansen | $-0.000896$ | $1.845$ meV | $2.329$ meV |
| Laurenti | $+0.001666$ | $1.750$ meV | $2.421$ meV |

Both inferred shifts are smaller than the historical $\pm0.003$ composition variance.

The nominal MAE ranking therefore reverses after a plausible gap-informed composition adjustment, while the RMSE values become nearly equal. Because the adjustment used the same gap data, it is circular and cannot be used as evidence that Laurenti is superior. Its valid purpose is to demonstrate non-identifiability.

## 4. Direct sample scatter

At the same nominal composition $x=0.199$, the two Table I detector datasets report

$$
E_{co}^{\mathrm{Tobin}}=87.3\ \mathrm{meV},
$$

and

$$
E_{co}^{\mathrm{Rawe}}=79.0\ \mathrm{meV},
$$

which differ by

$$
8.3\ \mathrm{meV}.
$$

The difference may contain specimen variation, composition error, detector-cutoff differences, or other source effects. It is larger than the nominal Hansen-versus-Laurenti difference at this composition.

## 5. Consequence

The 16 explicit Hansen points establish that both historical equations are operating inside a few-meV residual regime over this narrow 80 K interval. They do not establish which equation has the more accurate physical temperature law.

A valid model ranking requires:

1. independently calibrated composition;
2. repeated temperatures on each specimen;
3. one shared latent composition per specimen;
4. measurement-class-aware likelihoods;
5. held-out sources or specimens;
6. comparison against the source's composition-induced energy floor.

The result reinforces the central benchmark rule:

> A reduction in nominal residual below roughly 5 meV near $x\approx0.2$ is not automatically a better bandgap equation when historical composition uncertainty is of the same size.

The complete pointwise calculations are stored in `data/hansen/table1_model_residuals.csv`.
