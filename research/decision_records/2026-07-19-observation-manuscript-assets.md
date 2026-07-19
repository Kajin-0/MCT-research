# Observation-model manuscript comparator and asset freeze

**Date:** 2026-07-19  
**Manuscript:** Observation-model uncertainty and identifiability in HgCdTe bandgap extraction  
**Status:** draft manuscript-asset baseline

## Published Seiler comparator

The published Seiler 1990 rational-temperature relation is now an explicit historical comparator:

```text
Eg(x,T) = Eg_Hansen(x,0)
          + 5.35e-4(1-2x)(A+T^3)/(B+T^2)
A = -1822 K^3
B = 255.2 K^2
```

Primary source DOI: `10.1116/1.576952`.

For both Moazzami 2005 spectra, published Seiler is nominally closest for every fractional-power and Chu 1994 fitted edge. The prediction separation from Hansen is only:

```text
x=0.226: 0.254612 meV
x=0.310: 0.176556 meV
```

This nominal ordering is not an identified material-law ranking. Specimen-level composition uncertainty is unreported, and both spectra belong to one source study. No universal equation promotion is authorized.

## Manuscript assets

The deterministic builder exports five tables:

1. specimen and measurement provenance;
2. observation-candidate definitions and source domains;
3. complete edge ensemble with digitization-coordinate sensitivity;
4. four-model material comparison;
5. claim and evidence boundaries.

It also exports three SVG figures:

1. one real IRSE spectrum with every fitted observation model;
2. extracted edge versus observation definition for both specimens;
3. material-model residual intervals for fitted models and stable `400-4000 cm^-1` thresholds.

The figures contain no copyrighted source image. They are reconstructed only from the committed derived spectrum and analytical outputs.

## Controlling conclusions

- Fitted observation-model choice contributes `6.414-6.830 meV` of edge spread.
- Declared coordinate perturbations move fitted edges by at most `0.891 meV`.
- Fixed absorption definitions change the nominal closest material comparator.
- Published Seiler is nominally closest for fitted-model edges, but only by `0.177-0.255 meV` over Hansen.
- The sub-meV Seiler-Hansen ordering is not identifiable with the available composition metadata.
- The `5000 cm^-1` threshold remains calibration-sensitive for one specimen and is excluded from precision plots.
- No corrected edge, production edge, or preferred universal material law is selected.

## Next manuscript work

The next work is prose and the two conceptual figures already authorized by Issue #129:

- latent-gap/observation/carrier/vacancy identifiability diagram;
- paired `2 x 2 x 2` acquisition-design diagram;
- methods, results, discussion, limitations, and claim-boundary sections.

Additional source screening is not authorized unless a clean low-temperature or independent real spectrum becomes available and changes a manuscript conclusion.
