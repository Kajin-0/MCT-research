# Insight 0011 — Hansen versus the 77 K signed-gap transition

**Status:** exact comparison of a published equation with a later primary experimental constraint  
**Novelty status:** diagnostic, not a new bandgap equation  
**Interpretation status:** unresolved because composition calibration and gap definitions differ

## 1. Later experimental constraint

Teppe et al. report that an MBE Hg$_{1-x}$Cd$_x$Te layer with nominal

$$
x=0.155
$$

crosses the signed $\Gamma_6-\Gamma_8$ gapless state at approximately

$$
T_c=77\ \mathrm K.
$$

The gap is obtained from magneto-optical Landau-level spectroscopy and a reduced Kane model.

## 2. Hansen prediction at the same nominal composition

For

$$
E_g^{\mathrm H}(x,T)=
-0.302+1.93x-0.81x^2+0.832x^3
+5.35\times10^{-4}T(1-2x),
$$

the critical temperature at fixed $x$ is

$$
T_c^{\mathrm H}(x)
=-\frac{-0.302+1.93x-0.81x^2+0.832x^3}
{5.35\times10^{-4}(1-2x)}.
$$

At $x=0.155$,

$$
\boxed{T_c^{\mathrm H}=52.04\ \mathrm K.}
$$

Equivalently, at 77 K Hansen gives

$$
\boxed{E_g^{\mathrm H}(0.155,77\ \mathrm K)=+9.21\ \mathrm{meV}.}
$$

The nominal critical-temperature discrepancy is therefore approximately

$$
\Delta T_c\approx25\ \mathrm K.
$$

## 3. Equivalent composition offset

At 77 K, the Hansen equation gives the critical composition

$$
\boxed{x_c^{\mathrm H}(77\ \mathrm K)=0.14945.}
$$

Thus the discrepancy is exactly equivalent, to first order, to a composition shift

$$
\Delta x
=0.155-0.14945
\approx0.00555.
$$

The local Hansen composition sensitivity is

$$
\left.\frac{\partial E_g}{\partial x}\right|_{x=0.155,T=77\mathrm K}
=1.6565\ \mathrm{eV},
$$

so

$$
(1.6565\ \mathrm{eV})(0.00556)
\approx9.21\ \mathrm{meV}.
$$

The entire apparent equation error can therefore be represented by a Cd-fraction offset of about 0.56 percentage points.

## 4. Why this is not yet a Hansen falsification

The comparison mixes:

1. Hansen's historical empirical relation, whose original gap definition and data provenance are not yet reconstructed;
2. a nominal MBE composition whose full uncertainty and calibration method have not yet been extracted;
3. a signed magneto-optical Kane gap rather than necessarily the same optical-edge observable used in Hansen;
4. a later paper that explicitly compares with the Laurenti 1990 equation rather than Hansen.

Therefore the valid conclusion is:

> The nominal $(x,T_c)$ point is inconsistent with Hansen by 9.2 meV or 25 K, but the discrepancy is degenerate with a composition offset of only $\Delta x\approx0.0056$ and with measurement-definition differences.

It is not yet valid to conclude that the 9.2 meV is intrinsic functional-form error.

## 5. Internal evidence that composition precision matters

The same Teppe paper labels its higher-Cd sample as both

$$
x=0.17
$$

and

$$
x=0.175
$$

in different sections. Under Hansen, this reporting difference alone changes the 2 K gap prediction from

$$
E_g^{\mathrm H}(0.170,2\ \mathrm K)=7.48\ \mathrm{meV}
$$

to

$$
E_g^{\mathrm H}(0.175,2\ \mathrm K)=16.10\ \mathrm{meV},
$$

a difference of

$$
\boxed{8.61\ \mathrm{meV}.}
$$

This is comparable to the full Hansen-versus-critical-point discrepancy.

The point is not that the paper is unreliable. It is that third-decimal composition reporting is insufficient for sub-10-meV equation validation near inversion unless the actual calibration and uncertainty are retained.

## 6. Consequence for the benchmark

Composition must be treated as an uncertain explanatory variable, not as exact metadata. A suitable likelihood is

$$
x_i^{\mathrm{true}}\sim
\mathcal N(x_i^{\mathrm{reported}},\sigma_{x,i}^2),
$$

with

$$
E_{g,i}^{\mathrm{obs}}
\sim
\mathcal N\!\left(
E_g(x_i^{\mathrm{true}},T_i),
\sigma_{E,i}^2
\right).
$$

For sources without reported $\sigma_x$, the benchmark should either:

- assign a source-level latent composition offset with a defensible prior;
- perform sensitivity analysis over a declared range;
- or exclude the source from claims below the implied composition-error floor.

## 7. Falsification path

Hansen is meaningfully challenged by the Teppe series only if at least one of the following survives composition calibration:

1. the full $E_g(T)$ curve has systematic curvature or slope error that no constant $\Delta x$ removes;
2. multiple independently calibrated compositions require inconsistent offsets;
3. the measured critical trajectory $x_c(T)$ disagrees after propagating $\sigma_x$;
4. the gap-definition difference is modeled and remains too small to explain the residual.

This converts a tempting single-point contradiction into a properly identifiable model test.