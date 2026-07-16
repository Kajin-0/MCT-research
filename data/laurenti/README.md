# Laurenti 1990 data reconstruction

**Primary source:** J. P. Laurenti et al., “Temperature dependence of the fundamental absorption edge of mercury cadmium telluride,” *Journal of Applied Physics* **67**, 6454–6460 (1990), DOI `10.1063/1.345119`.

## Epistemic separation

This directory deliberately separates four different objects that appear in the paper.

### 1. Direct experimental series

Figure 2 full squares represent the authors’ LPE specimens measured by transmission or derivative absorption from approximately 2 to 300 K. The interband edge was obtained with a three-dimensional direct-allowed exciton model. The paper reports article-level edge accuracy better than approximately 3 meV.

These are experimental observations, but the individual coordinates are not printed in a table. They are mapped in `figure2_series_manifest.csv` and remain pending calibrated digitization.

### 2. Inherited literature series

Figure 2 open squares include Hg-rich values compiled through Weiler. Several plotted compositions were adjusted relative to nominal Scott values. Laurenti reports roughly 2% composition uncertainty and a best overall average correction of 2.3%.

Adjusted and nominal values must remain separate. A composition corrected to improve gap agreement is not independent composition metrology.

### 3. Published equation grid

`laurenti1990_table4_gap_grid.csv` transcribes Table IV. Those values were calculated from Eq. (7). They are useful for reproduction and regression testing but are **not validation data**.

Two entries are flagged:

- at `x=0.950`, the printed 400 K value is 1.402 eV, while direct evaluation of Eq. (7) gives 1.401487 eV;
- at `x=0.165`, the printed/OCR 0 K boundary value is 0.000 eV, while Eq. (7) gives approximately -0.006201 eV.

The printed values are preserved rather than silently overwritten.

### 4. Model-derived effective masses

`laurenti1990_table5_effective_mass_grid.csv` transcribes Table V. The values come from a five-band $k\cdot p$ expression using the empirical gap relation and assumed/interpolated band parameters. They are model propagation, not independent effective-mass measurements.

## Figure 2 digitization protocol

A pointwise digitization must record:

1. the exact page image and crop hash;
2. pixel coordinates of the four axis calibration points;
3. whether the point is a full square, open square, triangle, or fitted line;
4. adjusted and nominal composition labels separately;
5. temperature and energy pixel uncertainty;
6. overlap or occlusion with the fitted curve;
7. source class and specimen grouping;
8. an added energy uncertainty no smaller than the calibration/digitization error;
9. the article-level approximately 3 meV edge-extraction scale separately from digitization uncertainty.

Fitted lines must never be sampled and entered as observations. Table IV must never be used as a surrogate for the experimental points in Figure 2.

## Present status

- analytical formula: primary verified;
- Table IV gap grid: transcribed with two flags;
- Table V mass grid: transcribed;
- Figure 2 series identities: mapped;
- Figure 2 point coordinates: not yet digitized;
- specimen-level composition uncertainties: not fully recovered;
- full reproduction of the least-mean-squares fit: incomplete.
