# Hansen dataset reconstruction

**Issue:** #1  
**Status:** primary paper and source data not yet fully acquired  
**Rule:** do not generate pseudo-data from the published polynomial and call it the Hansen dataset

## Objective

Reconstruct, at datum level, the evidence underlying G. L. Hansen, J. L. Schmit, and T. N. Casselman, “Energy gap versus alloy composition and temperature in HgCdTe,” *Journal of Applied Physics* **53**, 7099 (1982).

The commonly reproduced equation is

$$
E_g(x,T)=
-0.302+1.93x-0.81x^2+0.832x^3
+5.35\times10^{-4}T(1-2x),
$$

with $E_g$ in eV and $T$ in K. The equation is a baseline to be verified against the primary source, not evidence for its own source data or uncertainty.

## Required primary-source extraction

For every datum or plotted point, record:

| Field | Meaning |
|---|---|
| `source_id` | primary paper, cited predecessor, table, or figure |
| `sample_id` | specimen identity if available |
| `material_form` | bulk, epitaxial layer, film, or other |
| `growth_method` | source growth/process description |
| `x_reported` | reported Cd mole fraction |
| `x_method` | composition measurement method |
| `sigma_x` | stated or reconstructed composition uncertainty |
| `temperature_k` | measurement temperature |
| `sigma_temperature_k` | stated temperature uncertainty |
| `gap_ev` | reported energy gap in eV |
| `sigma_gap_ev` | stated or reconstructed gap uncertainty |
| `gap_definition` | fundamental, optical absorption edge, magneto-optical, extrapolated edge, etc. |
| `measurement_method` | exact experimental method |
| `edge_criterion` | extrapolation or threshold rule used to define the edge |
| `fit_role` | fitted, validation-only, endpoint constraint, or excluded |
| `weight` | published or reconstructed fitting weight |
| `digitization_source` | table, text, or figure coordinates |
| `digitization_sigma_ev` | added digitization uncertainty |
| `notes` | strain, carrier concentration, defects, or caveats |

## Files planned

- `source_inventory.csv` — every primary and inherited data source.
- `measurements.csv` — one row per reconstructed datum.
- `digitization_log.csv` — figure-coordinate provenance and calibration.
- `fit_reproduction.json` — exact model, weights, optimizer, and coefficient covariance.
- `residuals.csv` — residuals in energy before any wavelength conversion.

## Reconstruction gates

The Hansen fit is not considered reproduced until all of the following are known or explicitly marked irrecoverable:

1. definition of $E_g$;
2. composition determination method;
3. composition and temperature ranges;
4. whether data came from this paper, prior papers, or both;
5. weighting and exclusion rules;
6. coefficient uncertainty or a defensible reconstruction;
7. residuals in meV;
8. endpoint treatment for HgTe and CdTe;
9. whether repeated temperatures on one sample were treated as independent data;
10. whether strain, carrier concentration, or optical-edge tails were controlled.

## Energy-first residual rule

All model comparison is performed first in energy:

$$
r_i=E_{g,i}^{\mathrm{measured}}-E_g(x_i,T_i).
$$

Only after residuals are established in meV may an equivalent wavelength error be reported. Because

$$
\lambda=\frac{hc}{E_g},
$$

wavelength residuals diverge and become strongly asymmetric near $E_g=0$; they are not a stable primary objective.

## Current verified versus pending information

### Verified from widely reproduced bibliographic records

- authors: G. L. Hansen, J. L. Schmit, T. N. Casselman;
- title: “Energy gap versus alloy composition and temperature in HgCdTe”;
- journal: *Journal of Applied Physics*;
- volume/year/start page: 53 (1982), 7099;
- the cubic-in-$x$, linear-in-$T(1-2x)$ equation above is widely attributed to this paper.

### Pending primary-paper verification

- DOI and full page range;
- abstract and stated purpose;
- exact measurement methods;
- source data and cited predecessor datasets;
- sample count and composition range;
- temperature range;
- fitting objective and weights;
- residual statistics and uncertainty;
- interpretation of $E_g$ near the inverted/zero-gap regime.

## Prohibited shortcuts

- Sampling the polynomial on a grid and treating those samples as observations.
- Converting a detector cutoff wavelength to a fundamental gap without modeling the edge criterion.
- Combining later datasets with Hansen points without a source label.
- Assigning equal uncertainty merely because the original uncertainty is unavailable.
- Fitting in wavelength and reporting the result as an energy-gap reconstruction.
