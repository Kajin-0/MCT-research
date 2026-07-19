# Moazzami 2005 real-spectrum observation-model analysis

**Date:** 2026-07-19  
**Primary source:** Moazzami et al., *Journal of Electronic Materials* **34**, 773-778 (2005), DOI `10.1007/s11664-005-0019-3`  
**Figures:** 6a and 6b  
**Status:** digitized primary-figure evidence; not instrument-export data

## Recovered records

The uploaded primary PDF contains the two Figure 6 panels as embedded 1-bit bitmap objects. The solid IRSE traces were isolated as continuous connected components, calibrated from the printed linear energy and logarithmic absorption axes, and sampled every three source pixels.

- Figure 6a: `x=0.226`, `T=300 K`, `d=15.40 um`, 125 points.
- Figure 6b: `x=0.310`, `T=300 K`, `d=4.95 um`, 115 points.

The source PDF and embedded-image SHA-256 values, pixel-axis anchors, masks, centerline rule, sampling interval, and uncertainty floor are recorded in the calibration JSON files. The copyrighted source PDF and source figures are not committed.

The energy calibration floor is approximately `0.53 meV` for a declared `1.5 pixel` anchor uncertainty, below the program's `5 meV` digitization stop rule. The solid IRSE curves remain visually separable from the dashed FTIR and dotted model curves over the extracted regions.

## Contract results

The declared ensemble includes:

- free fractional power;
- fixed powers `p=0.5`, `0.7`, `1.0`;
- the source-panel fitted exponent (`0.872` or `0.849`);
- the provenance-bound Chu 1994 Kane-region candidate;
- fixed absorption crossings from `400` to `5000 cm^-1`.

| Specimen | Fractional/Chu model span | Threshold span | Combined span |
|---|---:|---:|---:|
| `x=0.226` | `6.414 meV` | `87.827 meV` | `89.865 meV` |
| `x=0.310` | `6.830 meV` | `59.470 meV` | `62.026 meV` |

The Chu 1994 candidate reaches the upper search boundary for both spectra and is therefore recorded as boundary-limited rather than treated as an identified edge. The `p=0.5` candidate is also boundary-limited for the `x=0.226` panel.

## Digitization-coordinate sensitivity

Four coherent uncertainty corners were evaluated using plus/minus the declared energy-axis uncertainty and plus/minus the pointwise logarithmic absorption uncertainty. The model-fit point population was held fixed to the base `600-5000 cm^-1` window so the audit isolates coordinate uncertainty rather than fit-window membership changes.

- Maximum fractional/Chu edge shift across both spectra: `0.891 meV`.
- Every fixed threshold through `4000 cm^-1` shifts by less than `5 meV`.
- The `5000 cm^-1` crossing for `x=0.310` shifts by `5.694 meV` and is separately flagged as calibration-sensitive.

Therefore the approximately `6-7 meV` model-family span and the fractional-model ranking result survive the declared digitization bounds. The highest threshold crossing does not pass the same reporting gate.

## Material-model ranking

For every declared fractional-power or Chu candidate, Hansen is the closest of Hansen, Laurenti, and the provisional Hansen-Pade law for both specimens.

The winner changes when the observation is defined by fixed absorption crossing:

- `x=0.226`: Hansen at low crossings, Laurenti near `800-1000 cm^-1`, provisional Hansen-Pade at higher crossings.
- `x=0.310`: Hansen through `1000 cm^-1`, provisional Hansen-Pade at `2000 cm^-1`, and Laurenti at `3000 cm^-1` and above.

This satisfies the manuscript gate that a real-spectrum conclusion changes under declared observation definitions. It does **not** imply that high fixed thresholds estimate the latent material gap. The `5000 cm^-1` crossing is excluded from precision claims because its coordinate sensitivity exceeds `5 meV` for one specimen.

## Decision

Authorized:

- use these two digitized curves as the first real-spectrum manuscript application;
- report the complete candidate ensemble and digitization provenance;
- state that fractional-power model choice contributes approximately `6-7 meV` of edge uncertainty;
- state that operational threshold choice through `4000 cm^-1` can reverse the apparent material-model ranking;
- report the `5000 cm^-1` crossing only with an explicit calibration-sensitivity warning.

Not authorized:

- select one corrected edge;
- treat a fixed high-absorption crossing as the intrinsic gap;
- infer missing carrier or composition uncertainty;
- use these two related specimens as independent cross-laboratory validation;
- refit a universal HgCdTe gap law.
