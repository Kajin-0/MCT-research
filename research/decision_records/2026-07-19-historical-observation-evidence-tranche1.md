# Historical HgCdTe observation evidence - tranche 1

**Date:** 2026-07-19  
**Issue:** #132  
**Relationship to PR #131:** separate post-manuscript evidence work; no manuscript claim changes.

## Decision

The recovered primary sources authorize a bounded provenance and exact-record integration. They do not authorize a new universal `Eg(x,T)` fit.

This tranche contains no digitized curves and no copyrighted source pages. Every record is either:

- an exact source table value;
- an exact reported fitted value;
- a source-stated sign constraint; or
- an explicitly approximate note-added-in-proof value.

## Included source roles

- Schmit and Stelzer 1969: 56 half-peak detector-cutoff records from Table III.
- Wiley and Dexter 1969: specimen and transport provenance for the McCombe sample lineage.
- McCombe et al. 1970: one model-conditioned combined-resonance gap anchor.
- Groves et al. 1971: same-specimen gap-sign constraints at 4 K and 77 K.
- Groves, Brown, and Pidgeon 1967: temperature-qualified HgTe magnetoreflectance endpoint records.
- Herrmann et al. 1993: candidate tail-plus-band-filling observation operator, without point promotion.
- Shao et al. 2008: impurity and feature-class mechanism evidence, without point promotion.

## Important corrections preserved

### Schmit-Stelzer

The 1969 values are not method-free material gaps. The source defines cutoff at half the peak detector response and converts it using

```text
Eg[eV] = 1.24 / lambda_cutoff[um].
```

It also reports nominal and fit-adjusted compositions. Both are retained.

### Wiley-McCombe lineage

McCombe note 6 identifies its specimen as sample `4(1)` of Wiley and Dexter. Wiley Table I identifies sample `4` at `x=0.203`; McCombe supplies the same liquid-nitrogen carrier density (`9e14 cm^-3`) and rounded mobility (`2e5 cm^2/V s`). These records share one lineage and must not be treated as independent specimens.

### Groves 1971

The source gives a negative/positive sign change between 4 K and 77 K. The repository stores censored sign constraints rather than inventing numerical gaps.

### HgTe endpoint

The main 1967 result is `-0.283 +/- 0.001 eV`, with its temperature later estimated near 30 K. A note added in proof reports a magnitude near `0.30 eV` at 1.5 K. They remain separate records.

## Authorized conclusions

- Historical measurements must be modeled by observation class.
- Source lineage and model conditioning materially affect identifiability.
- Exact historical cutoff and resonance records can be ingested reproducibly.
- The current observation-model manuscript conclusion remains unchanged.

## Unauthorized conclusions

- pooling detector cutoff, absorption, photoluminescence, and magneto-optical values as interchangeable gaps;
- treating adjusted composition as independently measured composition;
- counting Wiley and McCombe as independent specimens;
- assigning numerical values to the Groves sign constraints;
- fitting a replacement universal HgCdTe bandgap equation from this tranche.
