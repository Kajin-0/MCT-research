# Laurenti 1990 Figure 2 asset-resolution gate

## Source identity

- primary paper: J. P. Laurenti et al., *Journal of Applied Physics* **67**, 6454--6460 (1990);
- DOI: `10.1063/1.345119`;
- owner-supplied filename: `laurenti1990.pdf`;
- SHA-256: `1e6a8805c6b2dae538b52dff4da40e4b9f10c2e8e204438c9d5917aa819fecea`;
- figure: Figure 2 on printed page 6455;
- observable: nonexcitonic fundamental absorption edge extracted from transmission or derivative-absorption spectra using a three-dimensional direct-allowed exciton model.

The paper states that the direct Cd-rich LPE measurements use the same specimen series from approximately 2 to 300 K and that interband transition energies could be deduced with article-level accuracy better than approximately 3 meV.

## Direct series relevant to the first benchmark

The full-square series include adjusted compositions

$$
x=0.970,\ 0.955,\ 0.925,\ 0.805,\ 0.710,\ 0.620,\ 0.550,\ 0.500.
$$

The first-pass extraction priority remains

1. $x=0.970$;
2. $x=0.955$;
3. $x=0.925$;
4. $x=0.500$ as a null control.

## Current rendering limitation

The primary PDF is available, but the currently accessible page render compresses the Figure 2 plotting region to only a few hundred pixels in the vertical direction while the plotted energy range spans approximately

$$
-0.4\ \mathrm{eV}\ \text{to}\ 1.6\ \mathrm{eV}.
$$

At that display scale, one vertical pixel corresponds to several meV and the square markers occupy multiple pixels. Marker-center placement, antialiasing, curve overlap and page compression therefore produce coordinate uncertainty comparable to or larger than the approximately 5 meV stop threshold for the intended first-pass analysis.

This is a limitation of the accessible render, not evidence that the underlying publisher PDF lacks sufficient native information.

## Decision

No numerical marker coordinates are entered from the current rendered preview.

Acceptable next assets are:

- native vector extraction from the publisher PDF;
- a lossless high-resolution crop of Figure 2;
- author-supplied numerical data;
- repeated independent digitizations from a render demonstrated to achieve less than approximately 5 meV coordinate uncertainty.

## Uncertainty separation

Keep the following quantities distinct:

1. approximately 3 meV article-level edge-extraction accuracy;
2. specimen composition uncertainty;
3. coordinate digitization uncertainty;
4. common axis-calibration uncertainty;
5. within-specimen correlation between temperature points.

The article-level accuracy statement must not be assigned automatically as an independent standard deviation to every marker.

## Active tracking

- Issue #29 owns the actual calibrated digitization task.
- Issue #31 records the current asset-resolution limitation.

Do not create a model-ranking result until the coordinates and digitization covariance satisfy the Issue #29 acceptance checks.
