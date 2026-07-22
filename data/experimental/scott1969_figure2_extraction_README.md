# Scott 1969 Figure 2 fixed-alpha temperature-series extraction gate

## Primary source

```text
M. W. Scott
Energy Gap in Hg1-xCdxTe by Optical Absorption
Journal of Applied Physics 40, 4077-4081 (1969)
DOI: 10.1063/1.1657147
File Library asset: scott1969.pdf
```

The full rendered PDF is available in the user File Library. The binary and page raster are not materialized in the repository runtime, so this tranche does not invent a PDF hash, page-image hash, pixel calibration, or marker coordinates.

## Source observation definition

The article states that every Figure 2 energy value was obtained from the photon energy at

```text
alpha = 500 cm^-1.
```

The repository observation class is therefore

```text
fixed_absorption_optical_edge_alpha_500_cm_inverse
```

with

```text
signed_gap_eligible = false
intrinsic_gap_eligible_without_observation_operator = false
pointwise_experimental_covariance = not_reported
```

The approximately 50-micrometre specimens limited the highest measurable absorption coefficient to about `1000 cm^-1`. The paper states that the available range was too narrow for a meaningful `(alpha h nu)^2` extrapolation. Figure 2 must not be relabeled as a Tauc-gap dataset.

## Figure-role decision

### Figure 2: direct-marker source

Figure 2 is the only approved numerical extraction source in this tranche. It displays the fixed-alpha edge versus temperature for individual specimen series.

A point may be admitted only when the direct marker center is distinguishable from:

- the connecting line;
- a specimen label;
- an axis or tick;
- another specimen series.

### Figure 5: provenance cross-check only

Figure 5 overlays measured values with curves generated from Equation (3). It prints density-measured compositions on the right and equation-fit-required compositions on the left.

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

## Required page-asset contract

Before numerical extraction, materialize one rights-compliant page image containing Figure 2 and record:

```text
source PDF identity
source PDF SHA256 or explicit unavailable status
rendering tool and version
rendering resolution or DPI
page number in the source PDF
page-image width and height in pixels
page-image SHA256
crop bounds containing the complete axes and labels
```

The page image itself need not be committed if rights or repository-size policy prohibit it, but its immutable digest and rendering recipe are mandatory.

## Required axis-calibration contract

The calibration ledger must contain at least two separated reference positions for each axis and must retain:

```text
axis name
pixel coordinate
source tick value
units
calibration role
visual half-width in pixels
```

The expected source axes are temperature in kelvin and fixed-alpha edge energy in electron volts. Exact tick values must be read from the materialized page image rather than reconstructed from Equation (3).

## Required marker ledger

Every admitted row must preserve:

```text
source_id
figure_id
article_page
specimen_label
nominal_density_composition_x
shared_specimen_group
pixel_x
pixel_y
temperature_k
fixed_alpha_edge_ev
pixel_half_width_x
pixel_half_width_y
temperature_extraction_half_width_k
energy_extraction_half_width_ev
visibility_status
marker_assignment_basis
measurement_class
signed_gap_eligible
intrinsic_gap_eligible_without_observation_operator
pointwise_experimental_covariance
```

Coordinate-extraction bounds are not source measurement covariance. Scott's article-level approximate uncertainty of `1-2 mole % CdTe` and `+/-0.01 eV` remains a separate source statement.

## Fail-closed conditions

Reject a point when:

- its center is not visually separable from a line or label;
- specimen assignment depends on following a fitted curve through an overlap;
- the local axis mapping is ambiguous;
- its coordinate is inferred from the empirical equation;
- its temperature or energy is copied from Figure 5 rather than Figure 2;
- its composition is a Figure 5 fit-required value rather than the source density value.

Partial specimen series are acceptable. Every omitted candidate must be recorded by reason before the issue closes.

## Current disposition

```text
Figure 2 scientific extraction target       approved
Figure 5 independent numerical dataset      rejected
page image available in File Library         yes
page image materialized in repo runtime      no
calibrated pixel extraction                  blocked
numerical marker ledger                      absent by design
model fitting or ranking                     prohibited
```

## Reopening condition

Proceed with numerical extraction only after a pixel-addressable Figure 2 page image is materialized with an immutable rendering record. Until then, absence of `scott1969_figure2_digitized.csv` is the correct fail-closed state.

## Claim boundary

This record establishes source and extraction governance. It does not reconstruct any marker coordinate, estimate a specimen gap, fit Scott's equation, validate or reject Hansen, infer covariance, authorize a production equation, or authorize a manuscript.
