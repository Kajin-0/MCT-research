# Absorption-edge uncertainty export contract

**Date:** 2026-07-19  
**Status:** validated research export contract

## Problem

The observation-model benchmark proved that model family, fit window, absorption threshold, tails, and carrier state can move an inferred HgCdTe edge by multiple meV. Reporting one absorption-derived gap without those assumptions hides a material uncertainty source.

A universal correction is not justified because the bias is scenario-dependent.

## Contract

Every input explicitly records:

- specimen and measurement identifiers;
- source reference and calibration record;
- modality, temperature, and thickness;
- composition, uncertainty, and measurement method;
- carrier type, density, and density status;
- tail treatment;
- fit absorption window;
- edge-search interval;
- threshold set;
- free or fixed fractional-power exponents;
- the energy and absorption arrays.

Unknown metadata are allowed only when their status is explicit.

## Output

The exporter returns:

- every fitted model candidate;
- every threshold-crossing candidate;
- excluded candidates with reasons;
- model-family envelope;
- threshold envelope;
- combined minimum, maximum, descriptive median, full span, and half-range;
- SHA-256 of the complete input and assumptions.

It does not return a recommended edge or corrected material gap.

## Deterministic example

A synthetic fractional-power spectrum with latent edge `0.100 eV` was evaluated using free, `p=0.5`, and `p=1.0` fits plus thresholds at `600`, `1000`, `1500`, and `2000 cm^-1`.

```text
free fractional-power edge = 0.099999 eV
free fitted exponent       = 0.7000438
minimum candidate edge     = 0.09185625 eV
maximum candidate edge     = 0.11180848 eV
combined full span         = 19.95223 meV
combined half-range        = 9.97612 meV
model-family span          = 9.14375 meV
threshold span             = 9.95726 meV
```

The example is a contract validation, not a material result.

## Decision

- research uncertainty export: **authorized**;
- single corrected gap selection: **forbidden**;
- production observation correction: **not authorized**;
- full candidate ensemble: **required**;
- edge-model uncertainty envelope: **required**.

## Reproducibility

- validated head: `a6b2d5c041c76ef0a9601305e3feb5fda59fa562`
- workflow run: `29667950404`
- artifact: `8436340042`
- digest: `sha256:24a1a552717063e4cdf117dbe6e9ad4223d1605d2660181a871806fefe97b7d4`
- input digest: `04428b5b432f50ad09f3361d98d315d980c3dd82689a4edfe5f12402cbb53e8f`

Machine-readable records:

- `data/templates/absorption_edge_uncertainty_input.schema.json`
- `validation/absorption_edge_uncertainty_contract_reference_result.json`
