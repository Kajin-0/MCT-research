# Orlita 2014 near-critical HgCdTe constraint

**Date:** 2026-07-18  
**Source:** Orlita et al., Nature Physics 10, 233-238 (2014), DOI `10.1038/nphys2857`

## Primary evidence

The source reports an MBE-grown graded HgCdTe layer with an approximately `3.2 um` region near `x approximately 0.17`. The profile was controlled during growth by in-situ single-wavelength ellipsometry.

Low-field magneto-optical modeling is improved by a small gap `Eg = 4 meV`. The same analysis estimates `EF approximately 15-17 meV` and electron concentration `n approximately (2-3)e14 cm^-3` at approximately `1.8 K`.

## Local model screen

At nominal `x=0.17` and `T=1.8 K`:

- Laurenti predicts `2.9560 meV`;
- provisional Hansen-Pade predicts `6.7855 meV`;
- Hansen predicts `7.4142 meV`;
- Chu 1983 predicts `15.7675 meV`.

Laurenti is the closest comparator for this record.

The composition required to reproduce `4 meV` is:

- Laurenti: `0.170573`;
- provisional Hansen-Pade: `0.168387`;
- Hansen: `0.168021`;
- Chu 1983: `0.163392`.

## Decision

1. Admit the record as a primary carrier-coupled near-critical constraint.
2. Do not treat it as an exact homogeneous composition-gap point.
3. Preserve carrier filling as part of the gap observation operator.
4. Record Laurenti as the closest comparator for this MBE/magneto-optical source family.
5. Do not promote Laurenti globally.
6. Do not refit any coefficient.
7. Require independent homogeneous composition metrology and carrier-aware gap uncertainty for strict validation.

## Interpretation

The record reinforces the result from Teppe 2016: near the critical composition, millifraction-level composition uncertainty is comparable to the differences among analytical gap models. It also supplies direct evidence that a nonzero carrier population participates in the optical inference.

The Orlita and Teppe records share the Mikhailov/Dvoretskii MBE and magneto-optical lineage. They are not independent cross-laboratory validation sets.

## Reproducibility

- validated analysis head: `7835810f78082d4c1a4c3bc0ee6a8df78855ed12`
- workflow run: `29662896606`
- artifact: `8434859963`
- digest: `sha256:cc8a23aaa3440c726ccf8e1d1b589b549b8dce6064930f50845a973d1d73c55f`
- compact result: `validation/orlita2014_near_critical_constraint_reference_result.json`

## Claim boundary

The source gives an approximate graded composition, a model-selected small gap, and optically inferred carrier statistics. The audit supports local consistency and observation-operator conclusions, not a universal material-law ranking.
