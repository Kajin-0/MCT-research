# R06 Phase 1C decision — Finkman 1983 primary transcription

**Date:** 2026-07-25  
**Controlling issue:** #346  
**Decision:** accept the recovered experimental metadata and fitted outputs; retain the symbol-exact and material-use blocks

## Accepted source recovery

The author-uploaded full text of Finkman 1983 supplies substantially more
primary evidence than the previously available abstract-level record.

The following source facts are now accepted for provenance and validation design:

- measured composition range `0.205 < x < 0.310`;
- n-type net-donor range approximately `4e14` to `6e15 cm^-3`;
- near-intrinsic onset near 160 K for `x approximately 0.2` and near 200 K for
  `x approximately 0.3`, for net impurity near `1e15 cm^-3`;
- maximum measurement temperature 345 K;
- microprobe composition analysis with an `x=0.215` calibration sample;
- composition homogeneity better than `+/-0.002`;
- maximum thickness error `+/-3%`;
- repeated stored-sample results within 1%;
- Hall inversion using `n=-1/(qR_H)` under the high mobility-ratio
  approximation;
- fitted `P=(8.0+/-0.4)e-8 eV cm`;
- fitted heavy-hole mass ratio `0.63+/-0.06`;
- the reported composition-temperature gap relation.

## Restricted equation status

The full text does not yield a safe symbol-exact extraction of the complete
model equation set through its text layer.

The following remain visually pending:

- neutrality Eq. (1) typography;
- conduction integral Eq. (2);
- secular relation Eq. (3);
- effective-mass Eq. (5);
- heavy-hole concentration Eq. (6).

No implementation may claim to reproduce Finkman 1983 until these are checked
against primary page images and independently audited for units and degeneracy.

## OCR-unit boundary

The extracted text renders the reported gap standard deviation as `4 MeV`.
Physical context strongly suggests an OCR capitalization error, but the record
must not silently convert this to `meV`. Visual primary-page confirmation is
required.

## Evidence-contract consequence

This source recovery does not create a countable PR #385 material point.

The recovered `+/-3%`, `+/-0.002`, and within-1% statements are experiment-level
or sample-level constraints, not point-by-point positive standard uncertainties
on carrier concentration. The plotted carrier data remain undigitized, reduced
chemical potential is not independently known, and the neutrality model remains
part of the historic inversion.

## Project-model consequence

The recovered historical `P`, heavy-hole mass, and gap relation are useful inputs
to a future source-grounded mapping analysis. They are not identical to the
project-defined simplified-Kane inputs `N_*` and `alpha`.

No direct substitution is authorized. Any mapping must:

1. start from the declared project dispersion;
2. derive all units and degeneracy factors;
3. include heavy-hole and intrinsic-neutrality accounting;
4. state whether parameters are local or functional in `(x,T)`;
5. validate against independent density or compressibility evidence.

## Authorization state

The material status remains:

```text
blocked_no_accepted_hgcdte_reference_set
```

Unauthorized:

- project `N_*` and `alpha` values;
- material equilibrium density and compressibility;
- screening;
- detector coupling;
- predictive transport or noise.

## Next action

The next primary-source action is visual confirmation of the unresolved Finkman
1983 equations and standard-deviation unit. In parallel, the Nemirovsky–Finkman
1979 full PDF must be recovered at page-text or image fidelity sufficient to
transcribe actual Hall-derived density points and their uncertainty metadata.
