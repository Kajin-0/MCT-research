# Semiconductor Science and Technology submission package

## Selected article type

**Paper**

The work is not being submitted as a Letter because the theorem hierarchy, source audits, and measurement-design consequences require a full-length treatment.

## Scope fit

The manuscript fits the journal through four explicit scope elements:

1. theoretical study of semiconductor properties;
2. new analytical technique for semiconductor characterization;
3. simulation and reproducible numerical verification;
4. relevance to semiconductor materials, devices, and optical cutoff interpretation.

The manuscript should be classified and described as semiconductor optical metrology and inverse-problem analysis, not as generic mathematical identifiability theory.

## Submission title

> From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability

## Short title

> Identifiability of HgCdTe band-edge measurements

## Journal-positioning paragraph

HgCdTe band-edge measurements are usually reduced to one reported energy or cutoff wavelength, although the observation depends on composition distributions, carrier filling, absorption physics, effective optical thickness, and the selected edge operator. This work formulates those dependencies as a reproducible semiconductor forward model and applies established structural-identifiability methods to derive the exact parameter combinations recoverable from common spectra and cutoff measurements. The result is a new HgCdTe-specific analytical technique for distinguishing latent material properties from observation-operator effects and for designing the independent measurements needed to recover them.

## Cover-letter draft

Dear Editors,

Please consider the manuscript **“From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability”** for publication as a Paper in *Semiconductor Science and Technology*.

The manuscript addresses a persistent semiconductor-characterization problem: a precisely fitted optical edge or detector cutoff does not necessarily identify a precise latent material bandgap. We combine source-grounded HgCdTe composition, absorption-tail, nonparabolic carrier-filling, and effective-thickness operators into a reproducible forward hierarchy. Using established structural-identifiability methods, we derive the explicit parameter combinations and rank bounds of the declared HgCdTe observation model.

The principal result is that five nominal parameters—latent gap, carrier translation, gap width, absorption amplitude, and effective thickness—enter the unmarked dense spectrum through only three combinations. Two physically distinct parameterizations therefore produce 281-point spectra that agree to machine precision. Supporting results quantify transition-root censoring, a 60.1% fit-window change in apparent tail energy, a model-specific rank-two limit for tail-only detector cutoffs, and severe nonparabolic carrier sensitivity. A finite-temperature reproduction of Dingrong et al.'s real degenerate-HgCdTe source table identifies an 11.297 meV RMS inconsistency between the printed density equation, printed momentum matrix, and reported Fermi elevations, while preserving the result as a source-consistency audit rather than a revised universal constant.

The work fits the journal's scope as a theoretical semiconductor study, a new analytical technique, and a simulation-based framework relevant to semiconductor properties, optical characterization, and infrared detector interpretation. The manuscript does not claim new general identifiability mathematics, a universal HgCdTe bandgap equation, or complete native-spectrum validation. All repository-generated data, code, immutable numerical records, and deterministic figure scripts will be publicly archived under a persistent DOI.

This manuscript is original, has not been published elsewhere, and is not under consideration by another journal.

Sincerely,

[Author name]
[Affiliation]
[Correspondence email]

## Data availability statement

> The repository-generated data that support the findings of this study, together with the analysis code, immutable validation records, tests, and deterministic figure-generation scripts, will be openly available in an archived repository under a persistent DOI at the time of publication. Restricted publisher PDFs are not redistributed. Source-conditioned quantities are identified by their original DOI and are accompanied by provenance and transformation records in the archived repository.

## Code availability statement

> The complete analysis implementation and regression tests will be openly available in the archived project repository under a persistent DOI. The repository contains versioned Python source code, machine-readable validation records, and deterministic scripts for regenerating all manuscript figures and tables.

## Restricted-source statement

> Copyrighted source articles used for equation and table audits are not redistributed by the project. The public archive contains citations, source hashes, permitted audit notes, and repository-generated derived quantities only.

## Contribution statement for single-author submission

> The author conceived the study, developed the methodology and software, performed the formal analysis and numerical investigations, curated the source and derived data, prepared the visualizations, and wrote and revised the manuscript.

Final CRediT terms:

```text
Conceptualization
Methodology
Software
Validation
Formal analysis
Investigation
Data curation
Visualization
Writing – original draft
Writing – review and editing
Project administration
```

## Funding statement template

> This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

Replace this statement if any relevant funding supported the work.

## Conflict-of-interest statement

> The author declares no competing interests.

## Evidence statement

The initial SST submission is authorized without a newly digitized spectrum because:

- the article is primarily an analytical and computational semiconductor Paper;
- exact and numerical results are reproducible;
- Herrmann and Chang components are source-conditioned;
- Dingrong Table 1 supplies a qualified real-specimen source test;
- the manuscript explicitly states that complete native-spectrum validation is absent.

A digitized spectrum remains optional strengthening or a reviewer-response action. It is not a pre-submission blocker.

## Submission checklist

- [ ] final author and affiliation information;
- [ ] archive release and DOI;
- [ ] journal-style bibliography generated from `references_verified.json`;
- [ ] vector figures converted to accepted journal format;
- [ ] table placement and numbering finalized;
- [ ] data availability statement inserted;
- [ ] CRediT, funding, conflict, and acknowledgements completed;
- [ ] cover letter finalized;
- [ ] suggested reviewers and exclusions documented;
- [ ] final PDF inspected at one-column and two-column scale;
- [ ] all CI workflows green on the submission tag.
