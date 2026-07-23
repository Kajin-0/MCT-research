# Scott 1969 optical-edge source audit

**Program:** R01 empirical bandgap reconstruction  
**Issues:** #265 source audit; #303 Figure 2 extraction  
**Source:** M. W. Scott, “Energy Gap in Hg1-xCdxTe by Optical Absorption,” *Journal of Applied Physics* **40**, 4077–4081 (1969), DOI `10.1063/1.1657147`  
**Hansen relationship:** confirmed fitted source `HSC_R02`; not independent validation of Hansen 1982

## Source availability

The primary PDF was materialized from the user-uploaded source and audited under SHA256

```text
7b2e5790745897ecd75bd22134e5d9293397820c3b7851eb5a9e648a5c441324
```

Figure 2 was rendered from PDF page 4 / article page 4079 at 600 dpi. The page image and derivative crops are not committed because the article is copyrighted; their immutable hashes, dimensions, crop bounds, plot corners, renderer version, and calibration coordinates are preserved in `scott1969_figure2_calibration.csv`.

## Experimental material and composition metrology

Scott used specimens cut from modified-Bridgman ingots.

The nominal CdTe mole fraction was obtained from density measurements with stated precision

```text
+/- 0.005 in fractional x.
```

Composition profiles were checked by electron-beam microprobe on the optical specimen or on adjacent ingot slices. The maximum reported variation across the illuminated area was approximately `0.02` in `x`, with typical variation described as lower.

These statements remain distinct:

- `0.005` is the stated nominal density-measurement precision;
- approximately `1–2 mole % CdTe` is the article-level uncertainty attached to the plotted gap-versus-composition comparison;
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

These are source-level approximate uncertainty statements. They are not assigned independently to every digitized marker and are not converted into a diagonal covariance matrix.

The Figure 2 extraction instead records bounded coordinate-digitization half-widths of `+/-1.75 K` and `+/-0.0047 eV`. Those bounds are not source measurement covariance.

## Figure 1 specimen inventory

The room-temperature absorption curves in Figure 1 carry the following composition labels, in mole percent CdTe:

```text
21, 23, 25, 31, 35, 38.5, 40.5, 46, 53, 61
```

They are encoded in `scott1969_figure1_specimens.csv` without duplicating pointwise Figure 2 coordinates.

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

A comparison with Camassel must distinguish model transfer from observable transfer.

## Figure 2 numerical extension

Issue #303 / PR #304 reconstructs 70 visually identifiable direct `x` marker centers from Figure 2 across the nine measured-composition series `23`, `25`, `31`, `35`, `38.5`, `40.5`, `46`, `53`, and `61`.

The numerical extension preserves:

1. the exact source and page-image hashes;
2. four plot-border intersections and 17 labeled axis references;
3. marker-center page and rectified pixel coordinates;
4. calibrated temperature and fixed-alpha edge energy;
5. bounded coordinate-extraction uncertainty;
6. source-level uncertainty separately from digitization uncertainty;
7. repeated-temperature grouping by specimen;
8. measured density labels separately from Equation (3) fit-required labels;
9. source quality flags for nonuniform specimens.

Only direct Figure 2 marker centers are admitted. Connecting lines and Equation (3) were not sampled.

Figure 5 remains a provenance cross-check only. It may be used to verify specimen labels and preserve measured-versus-fit-required composition distinctions, but it is not an independent observation ledger and no `scott1969_figure5_digitized.csv` exists.

Canonical extension files are:

```text
data/experimental/scott1969_figure2_calibration.csv
data/experimental/scott1969_figure2_digitized.csv
data/experimental/scott1969_figure2_extraction_gate.csv
data/experimental/scott1969_figure2_extraction_README.md
```

## Scientific decision

The Scott source is acquired and its Figure 2 fixed-alpha marker series is reconstructed with calibrated pixel provenance. This numerical extension does not:

- fit or rank a bandgap relation;
- independently validate Hansen;
- sample Equation (3) or Figure 5 curves as data;
- convert fixed-alpha edges into signed intrinsic gaps;
- explain the Camassel discrepancy;
- impose pointwise Gaussian uncertainties;
- authorize a production equation or manuscript.
