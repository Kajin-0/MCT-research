# Scott 1969 Figure 2 fixed-alpha temperature-series digitization

## Primary source

```text
M. W. Scott
Energy Gap in Hg1-xCdxTe by Optical Absorption
Journal of Applied Physics 40, 4077-4081 (1969)
DOI: 10.1063/1.1657147
Working PDF filename: scott1969(1).pdf
```

The uploaded PDF is the source used for this extraction. The article identifies Figure 2 on article page 4079 as the measured temperature dependence of the optical edge. Figure 5 is retained only as a specimen-label and measured-versus-fit-composition provenance cross-check.

## Immutable source and render record

```text
source PDF SHA256
7b2e5790745897ecd75bd22134e5d9293397820c3b7851eb5a9e648a5c441324

render command
python /home/oai/skills/pdfs/scripts/render_pdf.py scott1969(1).pdf --out_dir <render_dir> --dpi 600

renderer
pypdfium2 5.8.0

PDF page number
4

article page
4079

page image dimensions
4900 x 6580 px

page-image SHA256
1fbdea6692eec2f411b8dd0b01cddb02d46e426066cb140a87fc6ee4af63d694

Figure 2 crop bounds in page-image pixels
left=2750, top=450, right=4700, bottom=2600

Figure 2 crop SHA256
a4e9354ad30692b77b9a8e44cba9aed5b65aa2e6f1bdb7f1824dac5bddaef7a8

rectified plot dimensions
1500 x 1600 px

rectified plot SHA256
da7b37b73fce3fcafc3231b80ebf17459d20754870e58e9119d0825649d1730e
```

The page image, crop, and rectified derivative are not committed because the article is copyrighted. Their hashes, dimensions, crop bounds, plot corners, renderer version, and calibration coordinates are retained in `scott1969_figure2_calibration.csv`.

## Source observation definition

Scott states that every Figure 2 value was obtained from the photon energy at

```text
alpha = 500 cm^-1.
```

The repository observation class is

```text
fixed_absorption_optical_edge_alpha_500_cm_inverse
```

with

```text
signed_gap_eligible = false
intrinsic_gap_eligible_without_observation_operator = false
pointwise_experimental_covariance = not_reported
```

The approximately 50-micrometre specimens limited measurable absorption to about `1000 cm^-1`. Scott states that this range was too narrow for a meaningful `(alpha h nu)^2` extrapolation. These rows are not Tauc gaps and are not silently recast as model-independent intrinsic gaps.

## Figure roles

### Figure 2: direct-marker numerical source

Only the centers of the printed `x` markers were digitized. Connecting lines were not sampled. A marker was admitted only when its center was visually separable from the line, specimen label, axes, ticks, and neighboring series.

The final ledger contains 70 direct markers:

| measured composition x | printed label | marker count | extracted T range (K) | extracted edge range (eV) |
|---:|---:|---:|---:|---:|
| 0.610 | 61 | 8 | 10.944-292.631 | 0.714574-0.734595 |
| 0.530 | 53 | 6 | 99.434-293.632 | 0.609968-0.618977 |
| 0.460 | 46 | 9 | 31.365-293.632 | 0.503359-0.520377 |
| 0.405 | 40.5 | 8 | 10.343-293.231 | 0.396250-0.427282 |
| 0.385 | 38.5 | 8 | 29.963-293.031 | 0.352706-0.387241 |
| 0.350 | 35 | 8 | 38.772-292.431 | 0.300153-0.344698 |
| 0.310 | 31 | 8 | 7.140-292.831 | 0.230582-0.294647 |
| 0.250 | 25 | 7 | 40.174-292.631 | 0.155005-0.229581 |
| 0.230 | 23 | 8 | 9.342-292.631 | 0.111460-0.203554 |

No additional distinguishable Figure 2 `x` marker was omitted. The unequal series counts reflect the markers actually printed, not interpolation or curve completion.

### Figure 5: provenance cross-check only

Figure 5 overlays the measurements with Equation (3) curves. The numbers on the right are measured density compositions; the parenthesized numbers on the left are compositions required to fit Equation (3).

Permitted uses:

- check specimen labels;
- preserve measured-versus-fit-required composition provenance;
- identify a source transcription conflict.

Prohibited uses:

- sample an Equation (3) curve as data;
- add Figure 5 markers as independent observations;
- average Figure 2 and Figure 5 coordinates;
- replace a density-measured composition with a fit-required value;
- infer a missing Figure 2 point from the equation or connecting line.

The digitized ledger therefore uses the measured labels `23`, `25`, `31`, `35`, `38.5`, `40.5`, `46`, `53`, and `61`.

## Axis calibration

The plot was rectified from four fitted border intersections. Labeled source ticks were then detected independently and fit with linear least squares.

```text
temperature_k
= 0.200203995237 * rectified_pixel_x
  - 0.267693527909

temperature calibration
8 labeled ticks: 0, 40, 80, 120, 160, 200, 240, 280 K
maximum absolute tick residual: 0.514745 K
tick-fit RMSE: 0.254841 K
```

```text
fixed_alpha_edge_ev
= -0.000500509426406 * rectified_pixel_y
  + 0.799660915146

energy calibration
9 labeled ticks: 0.0 through 0.8 eV in 0.1 eV increments
maximum absolute tick residual: 0.00162907 eV
tick-fit RMSE: 0.000845608 eV
```

Equation (3) was not used to calibrate either axis or to place any marker.

## Coordinate-extraction bounds

Each `x` marker center is assigned a conservative visual half-width of 6 rectified pixels in both directions. The committed extraction bounds add the marker-center allowance linearly to the maximum calibration residual:

```text
temperature extraction half-width = +/-1.75 K
energy extraction half-width      = +/-0.0047 eV
```

These are bounded digitization uncertainties. They are not source measurement covariance.

## Source uncertainty and specimen structure

Scott reports:

```text
density composition precision
+/-0.005 in fractional x

maximum composition variation across the illuminated area
approximately 0.02 in x, typically less

approximate article-level comparison uncertainty
1-2 mole % CdTe
+/-0.01 eV
```

These statements are retained separately from the digitization bounds. They are not assigned as independent Gaussian errors to every marker, and no pointwise covariance matrix is reported.

Every row from one printed composition series shares one `shared_specimen_group`. This prevents the temperature markers from being treated as independent composition measurements.

Source quality flags are retained:

- `38.5` and `53`: kinked absorption edges attributed to compositional nonuniformity;
- `25`: high residual absorption attributed mainly to inhomogeneity;
- `61`: directly measured but outside Equation (3)'s stated `x <= 0.6` range;
- remaining Figure 2 series: no additional specimen-specific exclusion inferred.

## Canonical files

```text
data/experimental/scott1969_figure2_calibration.csv
data/experimental/scott1969_figure2_digitized.csv
data/experimental/scott1969_figure2_extraction_gate.csv
data/experimental/scott1969_figure2_extraction_README.md
tests/test_scott1969_figure2_extraction_gate.py
.github/workflows/scott-figure2-extraction-gate.yml
```

## Current disposition

```text
Figure 2 scientific extraction target       approved
Figure 2 page asset provenance               materialized and hashed
axis calibration                             complete
direct-marker ledger                         70 rows
Figure 5 independent numerical dataset       rejected
Equation (3) curve samples                    absent
model fitting or ranking                     not performed
```

## Claim boundary

This tranche reconstructs the Figure 2 fixed-absorption marker ledger with reproducible pixel provenance and bounded coordinate-extraction uncertainty. It does not treat Scott as independent validation of Hansen, fit Scott's equation, infer pointwise experimental covariance, convert the rows into signed intrinsic gaps, authorize a production equation, or authorize a manuscript.
