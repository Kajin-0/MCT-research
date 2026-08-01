# Decision record: R04/R05 literature batch 001

**Date:** 2026-07-31  
**Controlling issue:** #400  
**Input mode:** user-supplied published papers only

## Papers assessed

- DOI `10.1016/j.jcrysgro.2005.01.051`
- DOI `10.1063/1.4756938`

## Decision

```text
PARTIAL_REANALYSIS_FEASIBLE
```

## Basis

Chang et al. supplies quantitative wafer-scale HgCdTe composition and thickness summaries, a 100 um infrared-microscope aperture, and figure-level maps. The reported standard deviations are strongly affected by deterministic corner or edge gradients. The paper does not supply raw map coordinates, an explicit sampling pitch, a measured spatial PSF, repeated maps, or nanoscale covariance.

Zha et al. supplies HgCdTe-specific evidence that STM topography and apparent spectral gaps are strongly modified by tip-induced band bending, transport limitation, pit gap states, and tip-surface forces. It reports 20-30 nm bias-dependent apparent pit-depth changes and a roughly 0.40 eV flat-region current plateau compared with a reported 0.27 eV bulk gap. It does not report measurement temperature, lock-in modulation, an energy-resolution kernel, raw spatially indexed spectra, or a composition field.

Selected figures may therefore be digitized only for bounded coarse-map and nuisance-model studies. No source independently passes the eight evidence gates, and the two sources cannot be combined into one specimen.

## Gate consequences

- R04 may use the papers to test detrending, nonstationarity, aperture averaging, TIBB, surface-state, and topography-artifact safeguards.
- PR3 matched-data ingestion remains unauthorized.
- R05 material activation remains blocked.
- No outreach is authorized.

## Prohibited interpretations

- Chang wafer sigma as nanoscale random-mass variance;
- the 100 um aperture as a measured PSF;
- contour-map smoothing as a physical correlation length;
- Zha single-bias topography as geometric depth or composition;
- the 0.40 eV plateau as a direct bulk gap or calibrated local DOS;
- cross-paper same-specimen or exchangeability claims.

## Next evidence request

The next priority papers are:

```text
10.1103/PhysRevMaterials.9.054602
10.3724/SP.J.1010.2012.00222
10.1107/S1600577520013211
```

This decision changes only if a later supplied paper contains raw or recoverable same-specimen spatial and spectroscopic evidence with identifiable measurement kernels.
