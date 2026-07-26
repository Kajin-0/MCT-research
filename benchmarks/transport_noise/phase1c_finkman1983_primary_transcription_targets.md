# R06 Phase 1C Finkman 1983 primary-transcription targets

**Controlling issue:** #346  
**Scope:** primary-source transcription only  
**Material status:** blocked

## F0 — Source identity

The record must identify:

- E. Finkman;
- *Journal of Applied Physics* **54**, 1883–1886 (1983);
- DOI `10.1063/1.332241`.

## F1 — Full-text recovery without full equation authorization

The source may be marked full-text recovered while retaining a partial
symbol-exactness status. Full-text availability does not imply that corrupted
mathematical typography is safe to implement.

## F2 — Experimental composition domain

The recovered domain is:

```text
0.205 < x < 0.310.
```

## F3 — Impurity and temperature domain

The record must preserve:

- the reported n-type net-donor range;
- the near-intrinsic onset near 160 K for `x approximately 0.2`;
- the near-intrinsic onset near 200 K for `x approximately 0.3`;
- the 345 K upper-temperature limit.

## F4 — Sample uncertainty statements

The record must preserve separately:

- composition homogeneity better than `+/-0.002`;
- maximum thickness error `+/-3%`;
- long-term repeatability within `1%`.

These must not be converted into point-level standard uncertainties.

## F5 — Hall inversion boundary

The one-carrier relation

```text
n = -1/(q R_H)
```

may be transcribed with its high-mobility-ratio justification. The neutrality
formula must remain visually pending where subscripts or radicals are ambiguous.

## F6 — Model assumptions

The record must include the elevated-temperature Kane assumption, linear gap
versus temperature, constant `P`, constant heavy-hole mass, and nondegenerate
holes.

## F7 — Fitted matrix element

The source value must remain:

```text
P = (8.0 +/- 0.4)e-8 eV cm.
```

## F8 — Fitted heavy-hole mass

The source value must remain:

```text
m_h*/m0 = 0.63 +/- 0.06.
```

## F9 — Fitted gap equation

The source relation must remain:

```text
Eg = -0.287 + 1.717x + 5.805e-4 T(1 - 2.01x) + 0.2415x^4.
```

## F10 — OCR unit uncertainty

The extracted `4 MeV` gap-standard-deviation text must be flagged as requiring
visual confirmation. The repository must not silently replace it with `meV`.

## F11 — Figure labels are not point data

The recovered `x=0.225` and `x=0.290` example labels may be recorded. They must
not count as digitized uncertainty-bearing density points.

## F12 — Project-parameter mapping remains blocked

Historic `P`, heavy-hole mass, and `Eg` may not be mapped directly onto project
`N_*` or `alpha` without a new derivation, neutrality audit, and independent
validation.

## F13 — Authorization state

The transcription must retain:

```text
countable_material_points = 0,
project_N_star_authorized = false,
project_alpha_authorized = false,
screening_authorized = false,
detector_coupling_authorized = false.
```

## Exit criterion

This transcription branch may merge when F0–F13 are represented in the source
record, source note, tests, and decision record. Material fitting and model
replication remain blocked after merge.
