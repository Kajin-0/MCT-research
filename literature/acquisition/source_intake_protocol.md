# Source intake protocol for the distributional band-edge program

## Purpose

This protocol converts a user-retrieved or publicly obtained paper into an auditable research input without silently changing a scientific operator or redistributing copyrighted source files.

The controlling source manifest is:

```text
literature/acquisition/distributional_band_edge_sources.json
```

## Accepted source forms

A source may arrive as:

- publisher PDF;
- author-accepted manuscript;
- preprint;
- supplementary information;
- source-native numerical data;
- parameter table;
- high-resolution figure;
- correspondence containing data or methodological clarification.

The source form must be recorded. A bibliographic match by title alone is not sufficient; DOI, journal metadata, or another persistent identifier must be verified.

## Intake sequence

### 1. Preserve the original artifact

Keep the original filename. Do not edit, resave, optimize, or OCR the only copy.

When redistribution rights are unclear, the source file remains outside the public repository. The repository may store:

- DOI and citation metadata;
- acquisition provenance;
- cryptographic hash;
- permitted notes;
- equations transcribed for analysis;
- independently generated digitizations;
- derived data whose provenance is explicit.

### 2. Record acquisition metadata

Update the matching manifest record with:

```text
availability
rights
local_file
sha256
acquisition_provenance
```

`local_file` is a private intake reference, not evidence of redistribution permission.

Allowed rights states are:

```text
open_access
publisher_restricted_notes_only
unknown_do_not_redistribute
```

Never infer open-access rights merely because a PDF was downloadable.

### 3. Verify source identity

Confirm:

- DOI;
- exact title;
- author order;
- journal;
- year, volume, issue, and pages or article number;
- whether the file is the cited version, a preprint, a supplement, or a later expansion.

The Chang 2006 and Chang 2007 papers must remain separate source records.

### 4. Audit specimen ownership

For every equation, parameter, spectrum, and fitted value, record which specimen or calculation owns it.

Required fields include, when available:

```text
composition and uncertainty
temperature
carrier type and density
impurity or vacancy state
annealing and processing history
physical thickness
effective optical thickness
measurement geometry
spectral resolution
calibration convention
edge or cutoff definition
```

A parameter from one specimen may not be transferred to another merely because the nominal compositions are similar.

### 5. Audit equations and conventions

For each equation, record:

- equation number and page;
- variable definitions and units;
- sign and normalization conventions;
- external equations or papers required for execution;
- assumptions omitted from the displayed formula;
- parameter source and ownership;
- valid composition, temperature, density, and energy domain.

An operator remains blocked when an external definition cannot be recovered.

### 6. Audit figures and data

For a potential quantitative spectrum:

- determine whether axes are linear, logarithmic, wavelength, energy, or wavenumber;
- identify background subtraction and normalization;
- preserve plotted units;
- record line width and raster/vector quality;
- identify whether multiple curves share a specimen;
- determine whether thickness, reflectance, and collection efficiency are included;
- record calibration anchors and digitization uncertainty.

A figure can support auditable digitization only when its coordinate system and curve ownership are unambiguous.

### 7. Update audit state

Allowed audit states are:

```text
not_started
partial_missing_equations
partial_missing_native_data
complete_for_current_claims
```

`complete_for_current_claims` means only that the source is sufficient for its current bounded role. It does not authorize new specimen-level claims.

### 8. Re-score validation routes

After source audit, update only criteria changed by evidence:

```text
same_specimen_state
composition_provenance
carrier_provenance
thickness_provenance
calibrated_spectrum
equation_completeness
falsification_power
reproducibility_rights
flagship_relevance
nuisance_penalty
implementation_cost
```

Run the deterministic gate and preserve the changed ranking. A score is expected decision value, not a probability that a model is true.

### 9. Separate source intake from operator changes

Obtaining a paper does not authorize modifying a scientific operator.

Any operator change requires a new issue and PR containing:

- source audit;
- equation derivation;
- provenance-bound parameter transcription;
- tests;
- immutable result record;
- claim-boundary update;
- full CI.

### 10. Preserve negative results

A source may be rejected for quantitative validation because:

- native data are unavailable;
- spectra are not calibratable;
- parameter ownership is ambiguous;
- specimen state is incomplete;
- required external equations cannot be recovered;
- the observable does not test a merged operator.

Record the rejection explicitly. A failed source audit prevents repeated unproductive work and is a valid research result.

## Current user request order

The deterministic gate selects the Chang route as the best first validation target. Request these together:

```text
10.1007/s11664-007-0162-0
10.1063/1.2245220
```

Desired additions beyond ordinary PDFs:

```text
supplement
source data
high-resolution figures
same-specimen W and b
amplitude and effective thickness
carrier state
detector 50-percent response construction
```

The highest-value single source for extending the carrier physics remains:

```text
10.1016/0038-1098(85)90315-1
```

Desired additions:

```text
complete interband and free-carrier equations
all material and scattering parameters
77-300 K spectra
specimen thickness and optical geometry
edge-definition details
```

## Public-repository rule

Do not commit a publisher PDF solely because it was supplied by the user. Commit only material whose redistribution is authorized or whose inclusion is independently permissible. Hashes, citations, audit notes, derived calculations, and auditable digitizations remain the default public artifacts.
