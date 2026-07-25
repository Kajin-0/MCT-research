# R06 Phase 1C Kane material-evidence recovery targets

**Controlling issue:** #346  
**Scope:** source recovery and evidence classification only  
**Material status:** blocked

## E0 — Fixed blocked status

The candidate ledger must retain:

```text
status = blocked_no_accepted_hgcdte_reference_set
accepted_material_evidence = []
countable_pr385_point_count = 0
```

## E1 — Unique source identity

Every candidate must have a unique source identifier, DOI, and declared
provenance group.

## E2 — Direct and calculated evidence separation

Primary Hall measurements, calculated intrinsic-density fits, model curves, and
magneto-optical band-structure constraints must remain separate source classes.

## E3 — Nemirovsky–Finkman priority

The 1979 Hall-based intrinsic-density source must be classified as the highest
priority direct density recovery target, while remaining non-countable until
point values, uncertainties, and neutrality metadata are recovered.

## E4 — Finkman parameter-inversion boundary

The 1983 high-temperature Hall source may be treated as a primary parameter-
inversion candidate. Its fitted historic Kane quantities must not be mapped
silently onto the project-defined `N_*` or `alpha`.

## E5 — Hansen–Schmit benchmark boundary

The 1983 analytic fit remains a bounded model benchmark, not an independent set
of uncertainty-bearing experimental points.

## E6 — NIST precursor boundary

The 1991 NIST source may supply:

- the declared three-band architecture;
- parameter choices;
- model curves;
- experimental band-gap checks.

Its intrinsic-density curves must not count as independent material density
observations.

## E7 — Lowney fit remains blocked

The 1992 journal fit remains unusable for regression until its coefficients and
point-level numerical references are recovered.

## E8 — Magneto-optical evidence is indirect

Teppe et al. 2016 must remain an uncertainty-bearing band-structure adequacy
source, not a density, compressibility, or generalized-Einstein point.

## E9 — Missing shape evidence

The ledger must report zero recovered direct sources for:

- chemical compressibility;
- generalized Einstein factor.

## E10 — Chemical-potential basis remains open

No density candidate may be accepted without independently known `eta` or a
separately validated neutrality model.

## E11 — Existing authorization boundary is unchanged

The PR #385 material-validation configuration must retain:

- an empty accepted-evidence list;
- unauthorized material parameters;
- unauthorized equilibrium density and compressibility;
- unauthorized screening and detector coupling;
- unauthorized predictive noise claims.

## E12 — Recovery actions are explicit

The ledger must prioritize:

1. full primary recovery of Nemirovsky–Finkman 1979;
2. full primary recovery of Finkman 1983;
3. visual transcription of the NIST equations and model curves;
4. targeted searches for direct compressibility or Einstein-factor evidence;
5. a primary-theory mapping test for modern magneto-optical band parameters.

## Exit criterion

This source-recovery branch may merge when E0–E12 are represented in the
machine-readable ledger, tests, source note, and decision record. The material
closure remains blocked after merge.
