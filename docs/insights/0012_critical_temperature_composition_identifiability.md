# Insight 0012 — Critical-temperature validation is composition-limited near inversion

**Status:** exact local sensitivity derived from an analytical gap equation  
**Novelty status:** diagnostic/statistical consequence, not a new physical bandgap law  
**Use:** determine whether a reported critical temperature can discriminate competing equations

## 1. General result

Let a signed bandgap equation satisfy

$$
E_g(x,T_c(x))=0.
$$

Implicit differentiation gives

$$
\boxed{
\frac{dT_c}{dx}
=-\frac{\partial E_g/\partial x}
{\partial E_g/\partial T}
}.
$$

Therefore a small composition error produces, to first order,

$$
\boxed{
\delta T_c
\approx
-\frac{\partial E_g/\partial x}
{\partial E_g/\partial T}\,\delta x
}.
$$

This sensitivity diverges whenever the temperature coefficient becomes small. A transition-temperature datum can therefore appear precise in kelvin while remaining weakly informative about the equation unless the composition is independently known.

## 2. Hansen sensitivity near the Teppe sample

For the Hansen equation,

$$
\frac{\partial E_g}{\partial T}
=a(1-2x),
\qquad
a=5.35\times10^{-4}\ \mathrm{eV/K},
$$

and

$$
\frac{\partial E_g}{\partial x}
=1.93-1.62x+2.496x^2-2aT.
$$

At the nominal Teppe critical point

$$
x=0.155,
\qquad
T=77\ \mathrm K,
$$

these are

$$
\frac{\partial E_g}{\partial T}
=3.6915\times10^{-4}\ \mathrm{eV/K},
$$

$$
\frac{\partial E_g}{\partial x}
=1.65648\ \mathrm{eV}.
$$

Hence

$$
\boxed{
\frac{dT_c}{dx}
\approx-4.487\times10^3\ \mathrm{K/composition}
}.
$$

Equivalently,

$$
\boxed{
\left|\frac{dT_c}{d(x/0.001)}\right|
\approx4.49\ \mathrm K
}.
$$

A Cd-fraction uncertainty of only

$$
\sigma_x=0.001
$$

therefore creates approximately

$$
\sigma_{T_c,x}\approx4.49\ \mathrm K
$$

under the Hansen mapping.

The composition shift previously found between the nominal Teppe point and the Hansen 77 K root,

$$
\Delta x\approx0.00555,
$$

maps to

$$
|\Delta T_c|\approx24.9\ \mathrm K,
$$

which accounts for essentially the complete nominal 25 K discrepancy.

## 3. Information criterion for a critical-point experiment

Suppose two analytical models predict critical temperatures separated by

$$
\Delta T_c^{(12)}.
$$

A composition measurement can discriminate them only if the composition-induced uncertainty is substantially smaller:

$$
\left|
\frac{dT_c}{dx}
\right|\sigma_x
\ll
|\Delta T_c^{(12)}|.
$$

For a three-sigma discrimination requirement,

$$
\boxed{
\sigma_x
\lesssim
\frac{|\Delta T_c^{(12)}|}
{3|dT_c/dx|}
}.
$$

At the Teppe/Hansen sensitivity:

| Target model separation | Required $\sigma_x$ for 3-sigma discrimination |
|---:|---:|
| 25 K | $<1.86\times10^{-3}$ |
| 10 K | $<7.43\times10^{-4}$ |
| 5 K | $<3.71\times10^{-4}$ |
| 2 K | $<1.49\times10^{-4}$ |
| 1 K | $<7.43\times10^{-5}$ |

Thus a model comparison at the 1–2 K level would require composition metrology at roughly the $10^{-4}$ level under this local sensitivity, before adding gap-extraction, strain, and temperature uncertainty.

## 4. Inverse use: critical points as composition calibrators

If the analytical equation is trusted, the same sensitivity allows a measured transition temperature to infer an effective composition:

$$
E_g(x_{\mathrm{eff}},T_c^{\mathrm{obs}})=0.
$$

However, this is a calibration *conditional on the equation*. It cannot then be reused as independent evidence that the same equation is correct. Doing so would be circular.

The benchmark must therefore distinguish:

- independently measured composition;
- composition inferred from a bandgap equation;
- composition adjusted as a source-level latent parameter.

## 5. Consequence for model validation

A critical-temperature residual should be decomposed as

$$
\delta T_c
\approx
\delta T_c^{\mathrm{model}}
+rac{dT_c}{dx}\delta x
+\delta T_c^{\mathrm{measurement}}
+\delta T_c^{\mathrm{gap\ definition}}.
$$

Without an independent bound on $\delta x$, the model-error term is not identifiable from one sample.

The most informative evidence is therefore not one nominal $(x,T_c)$ pair, but one of:

1. a complete $E_g(T)$ curve for the same specimen, where a constant composition offset cannot remove curvature;
2. several independently calibrated compositions sharing one analytical law;
3. a measured $x_c(T)$ trajectory with composition uncertainties;
4. cross-method agreement on the same specimen.

## 6. Research implication

The immediate research target is not simply to reduce gap-equation error below a few meV. It is to reduce it below the combined floor from

$$
\sigma_{E,\mathrm{total}}^2
=
\sigma_{E,\mathrm{measurement}}^2
+\left(
\frac{\partial E_g}{\partial x}\sigma_x
\right)^2
+\sigma_{E,\mathrm{definition}}^2
+\sigma_{E,\mathrm{source}}^2.
$$

Near inversion, composition uncertainty is likely to be one of the dominant terms. Any new equation that ignores this term may appear more precise numerically while being less defensible physically.