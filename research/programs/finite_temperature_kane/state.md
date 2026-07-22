# Program state: finite-temperature Kane and electronic structure

**Portfolio contribution:** R02  
**State:** hybrid architecture retained; QE 7.6 / EPW 6.1 observational full-matrix exporter path terminated

## Objective

Develop symmetry-resolved 8-band Kane parameterization and finite-temperature matrix workflows that can connect first-principles endpoint calculations to defensible HgCdTe electronic-structure models.

## Controlling issues

- #2 — finite-temperature prior-art audit;
- #4 — binary endpoint calculation sequence;
- #5 — Gamma double-group and broader Kane symmetry extensions;
- #6 — deferred generalized matrix-data pipeline;
- #46 — completed CdTe lattice and thermal-expansion provenance;
- #90 — historical electronic-structure authorization ledger;
- #261 — completed CdTe Born-charge and screening failure diagnosis;
- #271 — completed bounded CdTe `zeu`/`zue` route comparison;
- #285 — active hybrid short-range matrix AHC plus generalized-Fröhlich architecture gate;
- #287 — completed hybrid matrix and generalized-Fröhlich contracts;
- #289 — completed source-level QE 7.6 / EPW 6.1 matrix-export capability decision.

## Completed foundations

- homogeneous bulk 8-band Kane implementation;
- one-`P` and two-`P` matrix projection;
- zone-centre degeneracy handling, symmetry restoration, and gauge alignment;
- Hermitian covariance and generalized least-squares tools;
- strict selected-band first-principles adapters;
- reproducible static CdTe post-processing on an immutable artifact;
- finite-temperature matrix and reconstruction oracles;
- primary-source and uncertainty-bounded CdTe fixed-volume reference;
- pinned QE/ABINIT runtime and pseudopotential provenance;
- one CdTe A0 breadth point, one stricter-response diagnostic, and one same-state `zeu`/`zue` comparison;
- explicit termination of the failed current CdTe polar-response state;
- selection of a hybrid architecture that separates short-range matrix AHC from independently constrained long-range polar physics;
- fail-closed 8 x 8 matrix, generalized-Fröhlich input, covariance, and no-double-counting contracts;
- source-level resolution of the QE 7.6 / EPW 6.1 lower-Fan information boundary.

## CdTe physical-volume state

Issue #46 is complete. The accepted fixed-volume A0 reference is

```text
a_ref(0 K) = 6.476035479332049 A
conservative absolute bound = +/-0.001814959409196 A
```

The source chain uses Williams 1969, Smith and White 1975, and the endpoint-adjusted Browder and Ballard 1972 CdTe bridge. The decision is adequate only for the declared `+/-0.5%` volume-sensitivity bracket; it is not a metrology-grade universal zero-temperature lattice constant or a quasiharmonic path.

## Terminated CdTe polar-response state

The first A0 point and stricter-response diagnostic failed the raw Born-charge gate. The separately authorized same-state route comparison resolved the remaining immediate diagnostic question.

At the fixed stricter state, both response routes converged and produced:

```text
zeu raw neutrality residual   1.25251 e
zue raw neutrality residual   1.25502 e
maximum zeu/zue difference    0.00283 e
minimum sampled gap           0.49733490292583227 eV
```

Against the predeclared thresholds:

```text
raw neutrality residual       <= 0.05 e     FAIL for both routes
zeu/zue route difference      <= 0.05 e     PASS
sampled electronic separation  > 0.05 eV    PASS
response convergence                         PASS
same-state provenance                        PASS
```

The close route agreement disfavors a route-specific implementation defect. The positive sampled gap disfavors an explicitly sampled metallic-state explanation. The shared order-unity neutrality failure terminates the tested combined path:

```text
QE 7.4.1 + PBE + current verified fully relativistic PseudoDojo Cd/Te ONCVPSP pair
+ fixed experimental-reference volume + declared 4 x 4 x 4 SOC response state
```

for use as the polar-response basis of A1.

Therefore:

- the tested polar-response path remains terminated for A1;
- no retry, convergence ladder, altered calculation, or charge-ASR repair is authorized;
- the failed Born tensors and any projected derivatives are prohibited as long-range physical inputs;
- the termination does not automatically invalidate all short-range electron–phonon information or all later QE releases;
- any new calculation still requires separate authorization and a decision-changing observable.

Controlling records:

```text
first_principles/a0/cdte_a0_zeu_zue_reference_result.json
research/decision_records/2026-07-22-cdte-zeu-zue-termination.md
```

## Selected continuation architecture

Issue #285 retains the hybrid decomposition:

```text
Sigma_ep
  = Sigma_SR_lower_Fan
  + Sigma_SR_upper_Fan
  + Sigma_SR_DW
  + Sigma_LR_Frohlich.
```

The long-range polar tranche must be independently implemented from traceable dielectric, LO-mode, branch-resolved carrier-dispersion, degeneracy, volume, and temperature evidence. It must not use the failed CdTe Born tensors.

The short-range tranche must preserve complete complex matrices, a declared smooth gauge, separate lower-Fan/upper-Fan/Debye--Waller terms, explicit long-range exclusion, and exact diagonal recovery.

ABINIT EPH remains excluded as the primary endpoint backend because its documented EPH path does not support SOC/noncollinear spinors. EPW/ZG special displacement remains only a possible independent total-shift cross-check.

Controlling records:

```text
research/decision_records/2026-07-22-r02-hybrid-short-range-frohlich.md
first_principles/b0/r02_hybrid_matrix_contract.json
first_principles/b0/r02_generalized_frohlich_contract.json
```

## QE 7.6 / EPW 6.1 source decision

Issue #289 tested whether the required full matrices could be exposed through a disabled-by-default **observational exporter** without changing the scientific algorithm.

The pinned GitHub mirror source state is:

```text
qe-7.6 tag commit
9f93ddec427d2b9a45bb72d828c6d324f62fcabd

EPW/src/selfen.f90 blob
be4858854d1ab26d27b3acf52a9a30c21fa8b472

EPW/src/wfpt.f90 blob
526405829090c4214eb87cff2af90bbd257efe3d
```

Source inspection established:

```text
upper-Fan complex matrix intermediate     available
Debye--Waller complex matrix intermediate available
lower-Fan complex matrix accumulator      absent
```

The standard lower-Fan loop forms

```text
|g_(m,n,nu)|^2
```

for one external band `n` and accumulates a scalar band-diagonal self-energy. It does not retain the second external-band index needed for

```text
g*_(m,n,nu) g_(m,n',nu).
```

Consequently, a complete lower-Fan matrix cannot be obtained by merely writing an existing array. Adding the missing contraction would be a new scientific implementation.

The issue-289 result is therefore:

```text
QE 7.6 / EPW 6.1 observational full-matrix exporter path  STOP
combined SOC + WFPT build                                NOT EXECUTED
CdTe short-range smoke-test design                       NOT AUTHORIZED
```

The build was not performed because it could not change the mandatory information-gate failure. This is a fail-closed source decision, not a claim that QE or EPW is generally incorrect or unable to perform diagonal SOC electron--phonon calculations.

Controlling records:

```text
first_principles/b0/qe76_epw61_matrix_export_capability_result.json
research/decision_records/2026-07-22-r02-epw-lower-fan-matrix-stop.md
```

## Current B0 state

Completed:

- primary-source and pinned-source capability audit;
- explicit matrix and generalized-Fröhlich contracts;
- synthetic Hermiticity, covariance, diagonal-recovery, branch-multiplicity, and no-double-counting tests;
- source-level classification of lower Fan, upper Fan, and Debye--Waller information retention;
- termination of the QE/EPW observational-export strategy before unnecessary build cost.

Still permitted only through a new authorization:

- analytical derivation of an external frequency-dependent matrix Fan contraction;
- synthetic matrix-Fan implementation and covariance tests;
- alternative backend audit for a natively retained full matrix;
- diagonal QE/EPW AHC only as a later independent benchmark, not as the matrix source;
- generalized-Fröhlich analytical implementation using independent inputs.

Not authorized:

- CdTe, HgTe, or alloy AHC calculations;
- an EPW patch that adds off-diagonal lower-Fan physics under the label of an exporter;
- rebuilding or modifying the terminated QE 7.4.1 response point;
- A1, A2, A3, dense EPW, or production special-displacement work;
- use of charge-ASR-repaired Born tensors;
- fitting a new HgCdTe gap equation.

## Most promising next analytical gate

The hybrid short-range plus generalized-Fröhlich architecture remains open, but its short-range path now requires an explicit **external matrix Fan contraction** or another backend.

A defensible external contraction gate must establish before any material run:

1. the retarded frequency-dependent matrix Fan expression;
2. a Hermitian quasiparticle reduction and its domain of validity;
3. exact recovery of the standard diagonal formula;
4. unitary covariance within degenerate subspaces;
5. causality, conjugation, denominator-sign, and zero-coupling limits;
6. separation of lower Fan, upper Fan, Debye--Waller, and long-range terms;
7. a raw complex-vertex export contract with immutable gauge and provenance;
8. synthetic and upstream scalar benchmark agreement;
9. explicit stopping rules for ill-conditioned or strongly frequency-dependent cases.

A pass would authorize only a separate software-fixture issue. It would not authorize CdTe.

## Unresolved scientific questions

- whether an external matrix Fan contraction can be made gauge-covariant and independently validated without an invasive backend fork;
- whether another backend natively retains all three complete matrix components under nonmagnetic SOC;
- whether independent dielectric, LO-mode, and branch-resolved carrier-dispersion evidence can support a generalized-Fröhlich correction at the required uncertainty;
- how the frequency-dependent matrix self-energy should be reduced into the Kane basis;
- whether scalar parameter renormalization is adequate or matrix-valued temperature dependence is required;
- what alloy interpolation or disorder treatment is justified between CdTe and HgTe.

## Manuscript status

No active manuscript is recorded. The current result is infrastructure and methodological foundation, not a converged finite-temperature HgCdTe prediction.

## Authorized next gates

- complete and merge the issue-289 source-level stop record;
- open a separate analytical matrix-Fan derivation issue only after the stop record is immutable;
- continue the generalized-Fröhlich derivation independently of the failed Born tensors;
- perform only separately authorized, decision-changing synthetic or upstream tests;
- keep all material computations closed until both short- and long-range components pass their own gates.

## Unsupported claims

This program does not currently support:

- converged phonons, dielectric response, or Born charges for the terminated CdTe setup;
- A1 readiness or converged AHC corrections for CdTe, HgTe, or HgCdTe;
- a validated generalized-Fröhlich correction for CdTe;
- a validated complete lower-Fan matrix from QE 7.6 / EPW 6.1;
- a validated finite-temperature 8-band parameter set;
- production SQS, CPA, SCBA, or alloy calculations;
- a new universal bandgap equation derived from incomplete endpoint data;
- treating software projection correctness as material validation;
- treating internal upper-Fan or Debye--Waller arrays as completion of the full matrix requirement.

## Shared dependencies

Kane Hamiltonians, symmetry utilities, matrix datasets, endpoint provenance, and gap benchmarks are shared with distributional observables and any future correlated-random-mass program.

## Computation gate

No expensive calculation should begin unless it targets a decision-changing observable, has an independent validation target, and includes an explicit termination criterion. CdTe/HgTe/alloy AHC, dense EPW, production special displacement, any retry of the terminated CdTe polar-response path, and any unreviewed off-diagonal Fan implementation remain closed.
