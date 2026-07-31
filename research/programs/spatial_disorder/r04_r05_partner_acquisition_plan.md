# R04/R05 partner-acquisition plan

**Controlling issue:** #395  
**Predecessor decision:** `PARTNER_DATA_REQUIRED`  
**Purpose:** convert the negative public-data audit into a bounded evidence-acquisition campaign

## Scope

This plan authorizes contact and feasibility assessment only. It does not authorize R05 reactivation, a new random-mass calculation, specimen claims, manuscript drafting, or public attribution of unpublished capabilities.

The campaign seeks one defensible path to a matched evidence package containing:

```text
near-critical HgCdTe specimen state
local mass or convertible composition covariance
measured spatial transfer function
local low-energy spectroscopy
measured energy-resolution kernel
same-specimen or quantitatively justified same-population linkage
raw data and calibration metadata
```

## Priority 1 — near-critical HgCdTe specimen group

### Target capability

The group associated with the 2025 HgCdTe quantum-well phase-diagram work has the strongest audited evidence for a controlled near-critical specimen series, structural characterization, magneto-optics and k.p modeling.

### Request

Ask whether the following exist or can be acquired on archived material or sister chips:

- specimen-level composition, thickness and growth identifiers;
- raw structural and magneto-optical records;
- local composition maps or spectrum images;
- archived wafers or sister chips suitable for cryogenic STM/STS;
- surface-preparation knowledge for HgCdTe;
- quantitative rules for treating sister specimens as exchangeable;
- permission to preserve raw and derived records with provenance.

### Decision value

This path best satisfies the near-critical and same-population foundations. It still requires local covariance and low-energy spectroscopy.

## Priority 2 — archived HgCdTe STM/STS

### Target capability

The 2012 etched p-type HgCdTe STM/STS work demonstrates material-specific tunneling spectroscopy and explicitly identifies tip-induced band bending and pit-associated in-gap states.

### Request

Ask whether the following archived records remain available:

- spatially indexed current-imaging tunneling spectroscopy or individual `I(V)`/`dI/dV` curves;
- registered topography and pit masks;
- exact specimen composition, thickness, growth method and electrical properties;
- temperature, bias setpoint, current setpoint, modulation amplitude and frequency;
- tip material, conditioning and stability records;
- etch chemistry, timing, transfer atmosphere and elapsed time before UHV insertion;
- repeated spectra sufficient to separate instrumental, surface and spatial variance.

### Decision value

A retained archive could satisfy part of the spectroscopy gate and establish a realistic HgCdTe surface-systematics model. It cannot pass the joint gate without a linked composition or mass field.

## Priority 3 — HgCdTe local composition metrology

### Target capability

Groups that have performed HgCdTe/CdZnTe STEM-EDX, Laue profiling, SIMS or interface characterization may retain raw spectrum images, line scans, lamella metadata or parent-wafer identifiers.

### Request

Ask for:

- raw EDX spectrum images rather than plotted line profiles;
- pixel coordinates, dwell time, accelerating voltage, probe current and detector geometry;
- lamella thickness and thickness uncertainty;
- standards, absorption correction and quantification covariance;
- beam-damage or element-loss tests;
- parent-wafer and region identifiers;
- information on whether adjacent or sister material remains available for spectroscopy.

### Decision value

This path can address local composition variance and instrument response. A single cross-sectional line scan is insufficient for a stationary lateral covariance claim.

## Priority 4 — coordinated user-facility experiment

### Facility-screening questions

Before a proposal is prepared, obtain written answers to:

1. Are Hg-containing specimens accepted under the facility safety and contamination policy?
2. Can HgCdTe be cleaved, etched, annealed or otherwise prepared without compromising the instrument?
3. Is in-vacuum or vacuum-transfer surface preparation available?
4. Can cryogenic UHV STM/STS deliver a measured effective energy kernel in the exploratory 1–2 meV range?
5. Can the same chip or a registered sister region be transferred to composition microscopy?
6. Are raw topography, spectroscopy and calibration files exportable?
7. Can instrument PSF, pixel integration and energy broadening be independently characterized?
8. Are external proprietary or publication-embargo constraints compatible with immutable provenance records?

### Preferred workflow

```text
wafer-scale screening
-> near-critical region selection
-> fiducial definition and specimen split plan
-> low-temperature STS on registered region
-> adjacent-region or sister-chip STEM-EDX/APT
-> exchangeability and transfer-function analysis
-> joint R04/R05 inference gate
```

The order may change if the composition method is destructive, but specimen identity and registration must be frozen before measurements begin.

## Standard response vocabulary

Every contacted path must be assigned exactly one outcome:

```text
DATA_ARCHIVE_EXISTS
NEW_MEASUREMENT_POSSIBLE
PARTIAL_DATA_ONLY
DATA_NOT_RETAINED
MATERIAL_NOT_ACCEPTED
SAME_POPULATION_INFEASIBLE
NO_RESPONSE_AFTER_DEFINED_FOLLOWUP
```

`DATA_ARCHIVE_EXISTS` and `NEW_MEASUREMENT_POSSIBLE` require a concrete inventory or facility statement. Informal optimism is recorded as `PARTIAL_DATA_ONLY` until decisive details are supplied.

## Minimum follow-up protocol

- one initial request;
- one concise follow-up after a defined interval;
- one final closure request if the recipient previously engaged but did not resolve access;
- no repeated solicitation after an explicit decline;
- record dates, recipients, scope and outcome without publishing private correspondence.

## Partner-stage gate

Return `GO_PARTNER_DATA_INGESTION` only if at least one path provides:

- an identifiable specimen or exchangeable specimen population;
- a credible route to both local covariance and low-energy spectroscopy;
- measured or measurable spatial and energy kernels;
- raw-data access or a written commitment to provide it;
- sufficient provenance to instantiate the PR1 evidence schema.

Return `PARTNER_DATA_PARTIAL` if useful records exist but one decisive modality or linkage remains missing.

Return `EXTERNAL_DATA_BLOCKED` if all priority paths resolve to one or more of:

- data not retained;
- Hg-containing material not accepted;
- required surface preparation unavailable;
- same-population linkage technically infeasible;
- raw data or calibration metadata cannot be shared;
- the achievable transfer band cannot identify the required covariance or spectroscopy effect.

No-response alone is insufficient for `EXTERNAL_DATA_BLOCKED` unless the defined contact campaign is completed across multiple independent paths.

## Stop rule

Do not replace a failed acquisition campaign with:

- digitized figures treated as raw data;
- unrelated specimens combined into a synthetic specimen;
- nominal instrument resolution treated as a measured kernel;
- wafer tolerance treated as local variance;
- a larger R05 simulation;
- a full-Kane calculation without material overlap.

## Claim boundary

A successful partner contact establishes access, not physical validation. R05 reactivation still requires ingestion, schema validation, joint inference and a separate reopening decision.
