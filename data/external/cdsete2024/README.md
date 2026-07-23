# Bowman et al. 2024 CdSeTe public source data

## Source

```text
Article
A. R. Bowman et al.
Spatially resolved photoluminescence analysis of the role of Se in
CdSe_xTe_1-x thin films
Nature Communications 15, 8729 (2024)
DOI 10.1038/s41467-024-52889-z

Dataset
DOI 10.5281/zenodo.13869384
Archive Datasets.zip
License CC BY 4.0
```

## Immutable archive identity

```text
size       14969970 bytes
MD5        1401ee9b5372edb78f888d152940fc79
SHA-256    cc3e1ce1a02266da2d0e0f301464a9d8a519855f33a597adeb7f16048684c9a6
members    61
```

The Zenodo MD5 was reproduced exactly in the Phase-1 workflow.

## Repository policy

The public archive and extracted source files are not committed to Git. They are
small enough for a bounded workflow acquisition but are still third-party data.
The repository preserves:

- persistent source identifiers;
- immutable archive hashes;
- a deterministic acquisition and structural-audit tool;
- a source-data qualification record;
- attribution and claim boundaries.

For a local run, place the exact archive at:

```text
<workdir>/Datasets.zip
```

or allow:

```text
python tools/r04_cdsete_phase1_audit.py --workdir <workdir>
```

to acquire it from the declared Zenodo record. The tool verifies the MD5 before
extracting or inspecting any member.

## Phase-1 result

The archive contains:

```text
54 CSV source-data tables
5 PNG images
1 JPG image
1 Windows thumbnail database
```

It does not contain the raw per-pixel PL spectral cube, raw interferograms,
per-pixel fit covariance, measured native sample-plane PSF, repeat maps, drift
records, timestamps, or analysis code.

It does contain complete source-data-derived two-dimensional PL maps with
physical coordinate axes. The admitted primary field is:

```text
file         Datasets/Figure 3e.csv
sample       Cl-treated 200 nm CdSe-underlayer CdSe_xTe_1-x film
observable   Gaussian-fitted PL peak wavelength
units        nm
map          24 x 24
coordinates  0 to 12.545 micrometres on both axes
spacing      approximately 0.54545 micrometre
missing      0 values
```

## Qualification

```text
RESTRICTED_GO
```

The field is admitted for a real-semiconductor numerical-kernel and finite-map
demonstration. Because the native sample-plane kernel is not measured or
numerically bounded, the analysis must not report a latent physical correlation
length, deconvolve the instrument, or treat the result as HgCdTe validation.

The authoritative decision record is:

```text
data/validation/r04_cdsete_phase1_decision.json
```
