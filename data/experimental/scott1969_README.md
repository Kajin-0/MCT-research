# Scott 1969 optical-edge source audit

**Program:** R01 empirical bandgap reconstruction  
**Issue:** #265  
**Source:** M. W. Scott, “Energy Gap in Hg1-xCdxTe by Optical Absorption,” *Journal of Applied Physics* **40**, 4077–4081 (1969), DOI `10.1063/1.1657147`  
**Hansen relationship:** confirmed fitted source `HSC_R02`; not independent validation of Hansen 1982

## Source availability

The primary PDF is available in the user File Library as `scott1969.pdf`. The binary is not materialized in the active repository runtime, so a SHA256 has not been computed. The repository records that state explicitly rather than inventing a digest.

## Experimental material and composition metrology

Scott used specimens cut from modified-Bridgman ingots.

The nominal CdTe mole fraction was obtained from density measurements with stated precision

```text
+/- 0.005 in fractional x.
```

Composition profiles were checked by electron-beam microprobe on the optical specimen or on adjacent ingot slices. The maximum reported variation across the illuminated area was approximately `0.02` in `x`, with typical variation described as lower.

These statements must remain distinct:

- `0.005` is the stated nominal density-measurement precision;
- approximately `1–2 mole % CdTe` is the later article-level uncertainty attached to the plotted gap-versus-composition comparison;
- neither statement is a datum-level Gaussian standard deviation;
- no pointwise composition covariance is reported.

## Specimen preparation and optical measurement

The specimens were lapped and polished to approximately `50 um`. Thickness was measured both directly with a micrometer and through interference fringes.

The transmission apparatus used:

```text
Perkin-Elmer model 112 infrared spectrometer
CaF2, NaCl, or KBr prism according to spectral range
continuous-flow cryostat spanning 4.2–300 K
Cu-Au (0.005% Co) thermocouple attached to the specimen
```

The source reports measurable transmittance down to approximately `1e-4` while retaining spectral resolution of `0.01 eV` or better.

## Operational gap definition

The temperature-dependent optical edge was defined as the photon energy at

```text
alpha = 500 cm^-1.
```

This criterion was selected to reduce sensitivity to residual absorption. The approximately `50 um` specimens limited the highest measurable absorption coefficient to about

```text
alpha = 1000 cm^-1.
```

The source therefore could not apply a conventional `(alpha h nu)^2` extrapolation over a sufficiently broad absorption range.

The stored measurement class is

```text
fixed_absorption_optical_edge_alpha_500_cm_inverse.
```

It is not silently equated with:

- an excitonic reflectivity gap;
- a derivative-absorption excitonic gap;
- a two-photon magnetoabsorption gap;
- a detector cutoff;
- a model-independent quasiparticle gap.

## Article-level uncertainty

Scott describes the approximate gap uncertainty in the composition comparison as

```text
+/- 0.01 eV in energy
1–2 mole % CdTe in composition.
```

These are source-level approximate uncertainty statements. They are not assigned independently to every future digitized marker and are not converted into a diagonal covariance matrix.

## Figure 1 specimen inventory

The room-temperature absorption curves in Figure 1 carry the following composition labels, in mole percent CdTe:

```text
21, 23, 25, 31, 35, 38.5, 40.5, 46, 53, 61
```

They are encoded in `scott1969_figure1_specimens.csv` without any inferred gap coordinate.

Source-specific quality notes are retained:

- specimens `38.5` and `53` have kinked absorption edges attributed to composition nonuniformity;
- specimen `25` has high residual absorption attributed mainly to inhomogeneity rather than free carriers;
- no additional specimen-specific exclusion is inferred for the other Figure 1 labels.

A quality flag is not a corrected composition or a fitted nuisance parameter.

## Source equation and validity

Scott reported

$$
E_g(x,T)=-0.303+1.73x+5.6\times10^{-4}(1-2x)T+0.25x^4,
$$

with energy in eV and temperature in K.

The source states that the closed expression is strictly intended for approximately

```text
x <= 0.6
100 K <= T <= 300 K.
```

It also notes low-temperature departures from the imposed linear temperature dependence.

The equation is a source result and historical comparator. Sampling it does not reconstruct the experimental marker dataset.

## Hansen lineage

Scott is one of the optical-absorption sources used by Hansen, Schmit, and Casselman in 1982. It therefore cannot be used as an independent held-out validation of Hansen.

Its high-value role is narrower:

```text
observation-definition bridge between the historical alpha=500 cm^-1 edge
and later exciton-conditioned or magneto-optical gap observables.
```

A future comparison with Camassel must distinguish model transfer from observable transfer.

## Fail-closed figure state

The current file interface supports a reliable textual audit of the source and Figure 1 composition labels. It does not yet support an auditable calibrated marker ledger for Figures 2 or 5.

Accordingly:

- no Figure 2 or Figure 5 energy coordinate is committed;
- no marker count is inferred from the empirical equation or connecting curves;
- no plotted fitted-composition label is substituted for a measured density composition;
- no source curve is sampled as pseudo-data.

A future marker extraction requires a rendered source asset and must preserve:

1. figure and panel identity;
2. specimen identity and measured composition label;
3. marker-center pixel coordinates;
4. calibrated axis bounds;
5. coordinate-extraction uncertainty;
6. source-level uncertainty separately from digitization uncertainty;
7. repeated-temperature grouping by specimen;
8. measured labels separately from equation-required fit labels;
9. exclusions or quality flags for nonuniform specimens.

## Scientific decision

The Scott source is acquired and suitable for a provenance-controlled observable-transfer audit. The numerical temperature-series reconstruction remains blocked at calibrated figure access.

This source audit does not:

- digitize Figures 2 or 5;
- fit or rank a bandgap relation;
- independently validate Hansen;
- explain the Camassel discrepancy;
- impose pointwise Gaussian uncertainties;
- authorize a production equation or manuscript.
