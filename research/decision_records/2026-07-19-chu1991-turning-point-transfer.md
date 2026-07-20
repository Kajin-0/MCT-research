# Chu 1991 turning-point transfer screen

Date: 2026-07-19  
Controlling issue: #132

## Question

Does the provisional zero-anchored Hansen-Padé temperature law retain its previously observed transfer advantage on an independent same-specimen HgCdTe temperature series?

## Primary evidence

Chu, Mi, and Tang, *Infrared Physics* **32**, 195-211 (1991), DOI `10.1016/0020-0891(91)90110-2`.

The paper reports thin-film absorption spectroscopy over `4.2-300 K` and defines the reported edge as:

> the photon energy at the turning point where the sharply rising absorption region crosses the comparatively flat intrinsic-absorption region.

The `x=0.276`, `d=6 um` specimen has seven printed Figure 2 edge labels:

```text
T (K)       6      77     100     150     200     250     300
edge (eV)   .212   .221   .227   .239   .249   .262   .273
```

The observed same-specimen increment from 6 K to 300 K is therefore `61 meV`.

Composition was estimated by density and spatially audited by electron-beam microprobe. The paper reports an RMS composition range of `0.003-0.005`; the screen conservatively propagates `x=0.276 +/- 0.005`.

The values are printed figure labels, not a numerical table or native digital export. Their retained rounding half-width is `0.5 meV` per label.

## Why the anchored comparison is stronger

For each equation, the comparison uses

```text
[Eg_model(x,T) - Eg_model(x,6 K)]
-
[edge_Chu(T) - edge_Chu(6 K)].
```

This removes most of the absolute composition/intercept error shared by the same specimen. It does not remove observation-class dependence: the source remains an absorption turning-point series rather than a magneto-optical latent-gap series.

## Results at nominal composition

Anchored thermal-increment mean absolute errors are:

```text
Laurenti reconstructed     4.269 meV
Schmit-Stelzer 1969        4.717 meV
Weiler 1977                4.883 meV
Wiley-Dexter 1969          4.883 meV
Chu 1983                   6.735 meV
Hansen 1982                7.215 meV
Seiler 1990                9.200 meV
provisional Hansen-Padé   11.725 meV
```

The 6-to-300 K increments are:

```text
observed                    61.000 meV
Hansen 1982                 70.466 meV
provisional Hansen-Padé     79.096 meV
```

Thus the provisional Padé increment overpredicts the observed turning-point shift by `18.096 meV`, compared with `9.466 meV` for Hansen.

## Composition-uncertainty robustness

Across `0.271 <= x <= 0.281`:

```text
Hansen anchored MAE envelope       6.420-8.011 meV
Hansen-Padé anchored MAE envelope 10.829-12.621 meV
```

The minimum Padé MAE exceeds the maximum Hansen MAE by approximately `2.818 meV`. The direction of the Padé-versus-Hansen transfer result is therefore not caused by the declared composition interval.

## Separate 300 K composition screen

The eight printed Figure 3 composition labels give Chu 1983 the smallest absolute MAE. That is not independent validation: the 1991 paper derives and validates the Chu relation using this experimental source family.

Absolute point ranking and same-specimen thermal-shape ranking answer different questions. The Padé form appears better than Hansen in the 300 K absolute composition screen but substantially worse in the anchored temperature transfer screen.

## Decision

Authorized conclusions:

- the provisional Hansen-Padé law does **not** retain a broad transfer advantage on the independent Chu turning-point temperature series;
- its cross-source support is materially weakened;
- the Padé law should no longer be described as the leading provisional temperature law without qualification;
- the same-specimen anchored increment is more informative about thermal shape than pooled absolute residuals;
- the result strengthens the observation-class identifiability argument.

Not authorized:

- select Hansen, Laurenti, Schmit-Stelzer, or another equation as a universal material law from this absorption series;
- identify Chu turning-point edges with method-free latent gaps;
- treat the Chu 1983 residual as independent validation;
- ignore the printed-label and composition limitations;
- refit Padé or introduce new empirical coefficients to absorb this discrepancy;
- merge this source into magneto-optical residual statistics without an observation-class offset.

## Program consequence

The prior provisional Padé form remains an archived, reproducible candidate, but its previously claimed cross-source transfer advantage is falsified for this independent absorption turning-point observation class. Further equation development remains blocked pending paired or observation-class-controlled experimental data.
