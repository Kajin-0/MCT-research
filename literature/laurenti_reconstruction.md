# Laurenti 1990 equation reconstruction

**Target:** J. P. Laurenti, J. Camassel, A. Bouhemadou, B. Toulouse, R. Legros, and A. Lusson, “Temperature dependence of the fundamental absorption edge of mercury cadmium telluride,” *Journal of Applied Physics* **67**(10), 6454-6460 (1990), DOI `10.1063/1.345119`.  
**Status:** analytical formula and typography primary-verified; experimental data reconstruction and fit reproduction remain incomplete.  
**Primary copy:** owner-supplied PDF audited visually; exact source hash recorded in `literature/papers/README.md`.  
**SHA-256:** `1e6a8805c6b2dae538b52dff4da40e4b9f10c2e8e204438c9d5917aa819fecea`.

## Primary-verified analytical form

The paper gives

$$
E_g^{\mathrm L}(x,T)=
-0.303(1-x)+1.606x-0.132x(1-x)
+10^{-4}A(x)\frac{T^2}{T+B(x)},
$$

where

$$
A(x)=6.3(1-x)-3.25x-5.92x(1-x),
$$

and

$$
B(x)=11(1-x)+78.7x.
$$

Here $E_g$ is in eV, $T$ is in K, and $x$ is the Cd mole fraction in $\mathrm{Hg}_{1-x}\mathrm{Cd}_x\mathrm{Te}$.

The previous reconstruction from Teppe et al. and an independent executable implementation is therefore confirmed by the original typeset source.

## Primary-source experimental basis

The paper reports:

- LPE-grown cadmium-rich samples covering approximately `0.5 <= x <= 1`;
- temperature-dependent transmission measurements from approximately 2 to 300 K;
- frequent use of derivative absorption to locate the edge;
- fitting with the three-dimensional theory of direct-allowed excitons to obtain the nonexcitonic interband edge;
- claimed edge-energy accuracy better than approximately `3 meV`;
- combination with selected Hg-rich and CdTe literature data;
- composition corrections of order 2% for one inherited dataset, with a reported best average correction of 2.3%;
- a nominal equation range `0 <= x <= 1`, `0 <= T <= 500 K`;
- a temperature-independent composition near `x=0.505`.

The equation is therefore an optical-edge empirical model assembled from mixed direct measurements and literature data. It is not a first-principles signed-gap equation.

## Numerical verification

For the nominal Teppe transition sample,

$$
x=0.155,
$$

the equation gives

$$
E_g^{\mathrm L}(0.155,77\ \mathrm K)
=-4.78\times10^{-5}\ \mathrm{eV}
=-0.0478\ \mathrm{meV},
$$

and the exact root is

$$
\boxed{T_c^{\mathrm L}(0.155)=77.124\ \mathrm K.}
$$

Other checks are

$$
E_g^{\mathrm L}(0.175,2\ \mathrm K)=12.08\ \mathrm{meV},
$$

$$
E_g^{\mathrm L}(0.155,2\ \mathrm K)=-24.32\ \mathrm{meV},
$$

and

$$
x_c^{\mathrm L}(77\ \mathrm K)=0.155028.
$$

Agreement with the Teppe transition is a useful transfer test, but it does not eliminate composition, strain, and measurement-class uncertainty.

## Structural interpretation

The temperature term is a composition-dependent Varshni form:

$$
\Delta E_g(x,T)=10^{-4}A(x)\frac{T^2}{T+B(x)}.
$$

Therefore

$$
\left.\frac{\partial E_g}{\partial T}\right|_{T=0}=0,
$$

unlike Hansen's exactly linear temperature term. At high temperature,

$$
\Delta E_g(x,T)
=10^{-4}A(x)\left[T-B(x)+O(T^{-1})\right].
$$

The endpoint coefficients encode the observed sign reversal:

- HgTe, $x=0$: $A=+6.3$, $B=11$ K;
- CdTe, $x=1$: $A=-3.25$, $B=78.7$ K.

## Confidence classification

| Item | Confidence | Reason |
|---|---|---|
| algebraic formula and coefficient ordering | primary-verified | visually checked in the original typeset paper |
| DOI, authors, pages, and stated range | primary-verified | original paper front matter and conclusion |
| experimental edge-extraction method | primary-verified at article level | transmission/derivative absorption and 3D exciton fitting are described |
| exact specimen-level dataset | incomplete | values remain to be transcribed from figures, tables, and cited source papers |
| fit weights, covariance, and coefficient uncertainties | unresolved | not reported in a modern reproducible form |
| use as a signed Kane gap near inversion | transfer assumption | the source measures a fundamental optical absorption edge |
| validity through 500 K | author-stated, not yet independently stress-tested | direct measurements emphasized 0-300 K |

## Benchmark rule

Laurenti may now be described as a **primary-verified published-coefficient baseline**. It must not yet be described as a reproduced fit.

Required benchmark variants are:

1. published coefficients with nominal composition;
2. published coefficients with latent composition uncertainty;
3. optical-edge-only scoring;
4. transfer scoring to signed magneto-optical gaps;
5. refit of the same functional form only after a common specimen-level dataset exists.
