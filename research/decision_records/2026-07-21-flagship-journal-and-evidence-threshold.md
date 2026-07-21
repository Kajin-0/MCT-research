# Decision: submit the flagship first to Semiconductor Science and Technology

**Date:** 2026-07-21  
**Issue:** #191

## Decision

The primary submission venue is:

> **Semiconductor Science and Technology — Paper**

The fallback venue is:

> **Journal of Applied Physics**

Measurement Science and Technology is retained as a stretch venue but is not authorized for the current evidence state.

## Basis

The official scope of Semiconductor Science and Technology explicitly includes:

- fundamental and applied theoretical semiconductor studies;
- fundamental properties, materials, interfaces, and devices;
- new analytical techniques;
- simulation.

That scope directly matches the manuscript's actual contribution: an HgCdTe-specific analytical and computational forward framework, source-conditioned mechanism studies, exact model-specific identifiability results, deterministic simulations, and a qualified real-specimen source-table test.

Measurement Science and Technology has a stronger performance-demonstration threshold. Its official scope requires advancement of a measurement method, method characterization, demonstrated performance through examples or applications, and explicit uncertainty, precision, or accuracy treatment. The present Dingrong four-row source-table reproduction is useful external evidence but does not demonstrate end-to-end performance of the unified method on a calibrated spectrum.

Journal of Applied Physics is a reasonable broad applied-physics fallback, but the fit is less explicit than Semiconductor Science and Technology's direct inclusion of semiconductor analytical techniques and simulation.

## Evidence threshold for initial SST submission

The current scientific evidence is sufficient for initial submission after bibliography and administrative packaging.

A newly digitized spectrum is **not required before initial submission**.

Required:

1. audited novelty boundary from PR #190;
2. complete core bibliography metadata;
3. Dingrong finite-temperature Table 1 reproduction with the partial-validation boundary intact;
4. deterministic code, records, figures, and tables;
5. data and code availability statement;
6. archive release and persistent identifier;
7. journal-format manuscript and figures;
8. author, affiliation, CRediT, funding, conflict, and cover-letter materials.

The existing evidence must be described accurately:

- Herrmann: source-conditioned reproduction and fit-window test;
- Chang: source-bounded analytical operator and calculated thickness dependence, not external multi-thickness validation;
- Dingrong: real-specimen source-table reproduction and source-consistency audit, not complete free-carrier spectrum validation;
- unified model: exact statements under declared assumptions, not universal microscopic physics.

## Digitization decision

Digitization is reserved for one of three conditions:

1. the SST editor or reviewers explicitly require a full-spectrum demonstration;
2. a source-native or calibratable spectrum becomes available with sufficient specimen and axis provenance;
3. a pre-submission editorial inquiry indicates that the four-row source-table test is insufficient.

Digitization is not authorized merely to make the manuscript appear more empirical.

## Measurement Science and Technology threshold

Submission to Measurement Science and Technology would require, before submission:

- at least one calibrated digitized or source-native spectrum;
- quantified digitization and measurement uncertainty;
- explicit nuisance parameters and parameter ownership;
- a recovery or falsification metric;
- comparison against a baseline edge-extraction procedure;
- an under-100-word measurement-context novelty and significance statement.

The current package does not meet that threshold.

## Journal-facing thesis

> HgCdTe band-edge extraction is an inverse problem whose reported edge depends on material-state distributions, carrier filling, effective optical thickness, and the observation operator. This work combines source-grounded HgCdTe models into a reproducible forward hierarchy and derives the exact parameter combinations and external measurements required for latent-gap recovery.

## Cover-letter thesis

> We submit an analytical and computational semiconductor-metrology study that resolves a recurring HgCdTe characterization problem: a precise fitted optical edge does not necessarily identify a precise latent material gap. The manuscript derives model-specific structural-identifiability bounds, supplies exact spectral counterexamples, quantifies fit-window and effective-thickness effects, and includes a finite-temperature reproduction of a real degenerate HgCdTe source table. The work is positioned as a new analytical technique and simulation-based measurement framework for semiconductor properties and devices.

## Data availability position

The article will state that all repository-generated data, code, immutable validation records, and figure-generation scripts are publicly archived under a persistent DOI. Restricted source PDFs are not redistributed. Source-derived numerical values and permitted digitizations are accompanied by DOI, provenance, and transformation records.

## Rejected alternatives

- delaying submission until a spectrum is digitized without a journal requirement;
- reframing the paper as general measurement science without a performance demonstration;
- reopening broad journal ranking;
- adding a new physical mechanism to increase apparent breadth;
- presenting Chang's calculated thickness curve as experimental validation.

## Revisit condition

Reopen the decision only when:

- an SST editor or reviewer provides a specific evidence requirement;
- the primary venue rejects the manuscript for scope;
- a new calibratable source dataset materially changes the evidence state;
- the manuscript contribution hierarchy changes.
