# Integrated Orlita 2014 near-critical HgCdTe constraint

**Date:** 2026-07-19  
**Source:** Orlita et al., *Nature Physics* **10**, 233-238 (2014), DOI `10.1038/nphys2857`  
**Evidence class:** conditional primary constraint

## Primary record

The source reports an MBE-grown graded HgCdTe layer with an approximately `3.2 um` region near `x approximately 0.17`. The profile was controlled during growth by in-situ single-wavelength ellipsometry.

At approximately `1.8 K`, the low-field magneto-optical model is improved by a small positive gap

```text
Eg = 4 meV.
```

The same source reports approximately

```text
EF = 15-17 meV
n  = (2-3)e14 cm^-3.
```

The reported gap is therefore coupled to a nonzero carrier state and a graded composition profile. It is not an exact homogeneous specimen-level `(x,T,Eg)` point.

## Nominal local model screen

At nominal `x=0.17`, `T=1.8 K` and reported `Eg=4 meV`:

| Model | Predicted gap | Absolute residual |
|---|---:|---:|
| Laurenti | `2.9560 meV` | `1.0440 meV` |
| provisional Hansen-Pade | `6.7855 meV` | `2.7855 meV` |
| Hansen | `7.4142 meV` | `3.4142 meV` |
| Chu 1983 | `15.7675 meV` | `11.7675 meV` |

Laurenti is the closest local comparator for this record.

## Equivalent composition diagnostic

The composition required by each model to reproduce `4 meV` at `1.8 K` is:

| Model | Required x | Offset from nominal 0.17 |
|---|---:|---:|
| Laurenti | `0.170573` | `+0.000573` |
| provisional Hansen-Pade | `0.168387` | `-0.001613` |
| Hansen | `0.168021` | `-0.001979` |
| Chu 1983 | `0.163392` | `-0.006608` |

The maximum model-equivalent composition offset is `0.006608`.

This diagnostic shows that composition uncertainty at the millifraction level can reorder the local model comparison. It does not authorize a composition remapping because the specimen is graded and the independent homogeneous uncertainty distribution is unavailable.

## Source-lineage boundary

The Orlita and Teppe records share the Mikhailov/Dvoretskii MBE and magneto-optical lineage. Orlita therefore adds a primary carrier-coupled constraint but not independent cross-laboratory validation.

The record is classified as `conditional`, not `authorized`, in the central source-recovery ledger because:

- primary full text is recovered;
- an explicit model-selected gap is recovered;
- the composition method is recovered;
- the operational measurement interpretation is recovered;
- point-level gap uncertainty is not recovered;
- the composition is a graded approximate plateau rather than an independently measured homogeneous specimen value.

## Central source-recovery effect

After integration, the central evidence ledger contains:

```text
all sources                         9
primary sources                     8
authorized primary fit sources      0
conditional primary sources         2
blocked primary sources             6
screen-only sources                 1
```

Conditional sources are:

1. Seiler 1990;
2. Orlita 2014.

The static-law reopening gate remains closed because no two independent primary point sources satisfy all provenance, uncertainty and measurement-definition requirements.

## Decision

- admit the primary constraint: **yes**;
- add it to the central recovery ledger: **yes**;
- classify it as conditional: **yes**;
- treat it as an exact homogeneous composition-gap point: **no**;
- preserve carrier filling in the observation operator: **yes**;
- record Laurenti as the closest local comparator: **yes**;
- promote Laurenti globally: **no**;
- refit any empirical coefficient: **no**;
- reopen the static HgCdTe law: **no**.

## Required next evidence

Strict validation requires a homogeneous specimen with:

1. independent composition uncertainty;
2. carrier type and density with uncertainty;
3. a gap extraction that propagates carrier-state uncertainty;
4. exact measurement definition and point uncertainty;
5. preferably independent laboratory lineage.

## Files

- `data/experimental/orlita2014_primary_near_critical_constraint.csv`
- `tools/analyze_orlita2014_near_critical_constraint.py`
- `tests/test_orlita2014_near_critical_constraint.py`
- `validation/orlita2014_near_critical_constraint_reference_result.json`
- `data/evidence/hgcdte_primary_gap_source_recovery.csv`
- `tests/test_primary_gap_source_recovery.py`
- `validation/primary_gap_source_recovery_reference_result.json`

## Claim boundary

This integration adds a primary, carrier-coupled and composition-censored near-critical constraint. It does not supply a production gap point, an independent model ranking, a universal correction, or authority to refit the HgCdTe material law.
