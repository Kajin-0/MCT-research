# Weiler 1981 HSC_R04 lineage reconciliation

## Exact source identity

```text
M. H. Weiler
Chapter 3: Magnetooptical Properties of Hg1-xCdxTe Alloys
Semiconductors and Semimetals, Volume 16
Pages 119-191 (1981)
DOI 10.1016/S0080-8784(08)60130-1
```

Publisher metadata and the publisher summary are available. The chapter full text is not currently present in the user File Library or the repository runtime. No source-file hash is therefore reported.

The publisher summary identifies the chapter as a review of magneto-optical techniques and the quasi-germanium description of HgCdTe, including composition- and temperature-dependent parameters and conduction-band intraband transitions. That summary does not expose the chapter's tables, figures, specimen registry, fitted point series, or uncertainty ledger.

## Existing underlying primary evidence

PR #158 already established a provenance-controlled record for:

```text
M. H. Weiler, R. L. Aggarwal, and B. Lax
Interband magnetoreflectance in semiconducting Hg1-xCdxTe alloys
Physical Review B 16, 3603-3607 (1977)
DOI 10.1103/PhysRevB.16.3603
```

The immutable evidence path is:

```text
data/evidence/guldner_weiler_1977_magneto_core.json
```

That record contains the published 1977 measurement class, specimen-count and range summary, temperatures, composition methods and uncertainties, model-conditioned gap relation, and interband/intraband discrepancy. This tranche does not copy, replace, or edit those values.

The 1981 chapter is likely part of the same scientific lineage, but the current evidence does not prove that every chapter datum maps one-to-one onto the ten 1977 specimens. The repository therefore records

```text
relationship_to_weiler1977 = likely_review_lineage_not_specimen_identity_proof
specimen_identity_mapping_status = unresolved
```

## Hansen's three composition layers

Hansen 1982 distinguishes three composition records associated with the Weiler source:

1. **Published Weiler values.** The recovered 1977 paper used electron microprobe for most specimens and a room-temperature transmission cut-on for the remainder.
2. **Micklethwaite private values.** Hansen states that it adopted B. Micklethwaite's transmission-cutoff compositions as the most accurate values for the Weiler source.
3. **Reine private alternatives.** Hansen states that M. Reine's density-derived compositions would be approximately `0.01` to `0.035` higher than the Weiler values.

The two private per-specimen records are unavailable. The reported Reine shift range is not a transformation rule and is not applied to any published composition.

Required repository contract:

```text
private per-specimen values available = false
synthetic reconstruction authorized = false
universal composition correction authorized = false
```

## HSC_R04 numerical status

Hansen labels the Weiler source as fitted magneto-optical evidence. The current repository can identify its source class and provenance conflict but cannot reconstruct the exact numerical points used by Hansen because:

- the 1981 chapter full text is unavailable;
- Hansen's adopted Micklethwaite composition values are private and not printed;
- the mapping from Hansen's plotted points to chapter specimens and temperature series is unresolved;
- substituting the 1977 published values would silently change the composition provenance Hansen declared.

Therefore:

```text
HSC_R04 numerical reconstruction = blocked
chapter figure digitization = not authorized
private composition reconstruction = not authorized
1977-to-1981 specimen identity = unresolved
```

## Acquisition gate

A later tranche may proceed only after an authorized full-text copy of the 1981 chapter is available. It must then determine:

- whether the chapter reproduces the 1977 ten-specimen dataset or adds other specimens;
- which figures or tables Hansen used;
- whether the chapter prints the compositions later replaced by Micklethwaite values;
- the exact temperature-series and point mapping;
- the uncertainty semantics of any chapter-level parameter table.

Even with the chapter, the private Micklethwaite values remain unavailable unless a separate source is obtained.

## Claim boundary

This reconciliation supports exact bibliographic identity, review-level publisher scope, the link to the existing 1977 evidence lineage, and Hansen's three-layer composition-provenance problem.

It does not establish chapter-level numerical data, reconstruct private compositions, prove one-to-one specimen identity, digitize a figure, fit a gap equation, apply a composition shift, rank material laws, authorize a production equation, or authorize a manuscript.
