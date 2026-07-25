# R06 Phase 1C Kane parameter-validation targets

**Controlling issue:** #346  
**Scope:** structural identifiability and external-evidence acceptance policy  
**Material status:** blocked

## V0 — Positive parameter coordinates

`N_* > 0` and `alpha > 0` are required for logarithmic sensitivity analysis.
The parabolic endpoint `alpha=0` remains a reduction benchmark, not a valid
log-parameter identification point.

## V1 — Positive observation contract

Accepted observation kinds are:

- `density_cm3`;
- `compressibility_cm3_per_ev`;
- `generalized_einstein_factor`.

Every observation must declare positive relative standard uncertainty, finite
`eta`, positive temperature, and a condition identifier.

## V2 — Exact density-scale sensitivity

For density and compressibility,

```text
partial log(y)/partial log(N_*) = 1.
```

## V3 — Scale-free Einstein factor

For `Theta`,

```text
partial log(Theta)/partial log(N_*) = 0.
```

## V4 — Repeated identical density is rank one

Repeating density at the same `eta`, temperature, and parameterization must not
create artificial two-parameter identifiability.

## V5 — Density plus Einstein factor is locally full rank

At positive nonparabolicity where `Theta` has nonzero alpha sensitivity, one
absolute density observation plus one scale-free Einstein-factor observation
must identify the two parameter directions locally.

## V6 — Matched density plus compressibility is locally full rank

At one condition, the density/compressibility ratio supplies shape information
and must separate `alpha` from `N_*` when their alpha sensitivities differ.

## V7 — Relative-uncertainty weighting

Multiplying an observation's relative uncertainty by a factor must divide the
corresponding sensitivity row by the same factor.

## V8 — Rank and conditioning report

The report must include:

- weighted sensitivity matrix;
- singular values;
- Fisher matrix;
- numerical rank;
- full-rank flag;
- condition number or infinity for rank-deficient designs;
- observation count and temperature coverage.

## V9 — Minimum point count

Material evidence requires at least three uncertainty-bearing points.

## V10 — Provenance independence

Material evidence requires at least two provenance groups and every point must
be primary or independently generated.

## V11 — Temperature span

Material evidence requires at least two temperatures.  This is an adequacy
stress test, not authorization to treat `N_*` or `alpha` as temperature
independent.

## V12 — Absolute scale and shape information

The evidence set must contain:

- density or compressibility for absolute scale; and
- generalized Einstein factor, or a matched density/compressibility pair, for
  nonparabolic shape.

## V13 — Chemical-potential basis

Every material point must have independently known `eta` or a separately
validated neutrality model.

## V14 — HgCdTe specificity

Every accepted point must be explicitly HgCdTe-specific.  Synthetic benchmark
points and generic Kane calculations cannot satisfy this target.

## V15 — Empty accepted-evidence list

The committed machine-readable gate must retain an empty
`accepted_material_evidence` list and keep material parameter values,
equilibrium density, compressibility, screening, detector coupling, and
predictive noise claims unauthorized.

## V16 — Simplified-model adequacy decision

After future parameter identification, the gate must require hold-out residual
analysis across composition and temperature and an explicit decision between:

- a restricted-domain simplified dispersion; or
- a full three-band secular model.

## Exit criterion

This branch may merge when V0-V16 are represented in code, tests, configuration,
and the decision record.  The material-validation gate itself remains open until
real accepted evidence satisfies V9-V16.
