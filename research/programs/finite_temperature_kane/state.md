# Program state: finite-temperature Kane and electronic structure

**Portfolio contribution:** R02  
**State:** hybrid short-range/generalized-Fröhlich architecture selected; B0 source audit active

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
- #285 — active hybrid short-range matrix AHC plus generalized-Fröhlich architecture gate.

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
- selection of a hybrid architecture that separates short-range matrix AHC from independently constrained long-range polar physics.

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

Issue #285 selects a hybrid decomposition:

```text
Sigma_ep
  = Sigma_SR_lower_Fan
  + Sigma_SR_upper_Fan
  + Sigma_SR_DW
  + Sigma_LR_Frohlich.
```

The preferred candidate for the short-range tranche is a pinned QE 7.6 / EPW 6.1 Wannier-function perturbation-theory AHC path, subject to source-level proof of:

- complete nonmagnetic SOC compatibility;
- separate lower-Fan, upper-Fan, and Debye–Waller export;
- complete complex matrix preservation;
- stable gauge transfer into the canonical Kane basis;
- explicit long-range exclusion;
- mode/frequency-resolved signed information.

The long-range polar tranche must be an independently implemented generalized-Fröhlich model using traceable dielectric, LO-mode, band-degeneracy, and effective-mass evidence. It must not use the failed CdTe Born tensors.

ABINIT EPH is not the primary endpoint backend because its current documentation states that spin–orbit and noncollinear EPH are unsupported. EPW/ZG special displacement remains a possible independent total-shift cross-check, not a replacement for Fan/Debye–Waller matrix decomposition.

Controlling records:

```text
research/decision_records/2026-07-22-r02-hybrid-short-range-frohlich.md
research/capability_audits/qe76_epw61_soc_ahc_initial.md
```

## B0 state

Authorized:

- primary-source and pinned-source capability audit;
- call-graph inspection of QE/EPW AHC, SOC, WFPT, and long-range handling;
- analytical generalized-Fröhlich derivation;
- uncertainty and no-double-counting contracts;
- parser and schema prototypes using synthetic or upstream test data;
- cost and output-volume estimates;
- a final `go`, `restricted go`, or `stop` record.

Not authorized:

- CdTe, HgTe, or alloy AHC calculations;
- rebuilding or modifying the terminated QE 7.4.1 response point;
- altered cutoffs, grids, pseudopotentials, functionals, or structural states;
- A1, A2, A3, dense EPW, or production special-displacement work;
- use of charge-ASR-repaired Born tensors;
- fitting a new HgCdTe gap equation.

## First target after B0

If B0 returns `go` or `restricted go`, the first proposed physical target must remain bounded to the fixed-volume Gamma blocks:

```text
Delta E_Gamma6(T)
Delta E_Gamma8(T)
Delta E_Gamma7(T)
Delta Eg(T)
Delta DeltaSO(T)
```

Finite-k closure of `P8`, `P7`, `F`, and `gamma1-3` remains later work. HgTe and alloy calculations remain closed.

## Unresolved scientific questions

- whether QE 7.6 / EPW 6.1 can export the required short-range SOC AHC matrices without an invasive fork;
- whether lower Fan, upper Fan, and Debye–Waller contributions remain separately identifiable under the full spinor path;
- whether the short-/long-range split is explicit and auditable in the WFPT AHC implementation;
- whether independent dielectric, LO-mode, and effective-mass evidence can support a generalized-Fröhlich correction at the required uncertainty;
- how electron–phonon self-energies should be projected into the Kane basis;
- whether scalar parameter renormalization is adequate or matrix-valued temperature dependence is required;
- what alloy interpolation or disorder treatment is justified between CdTe and HgTe.

## Manuscript status

No active manuscript is recorded. The current result is infrastructure and methodological foundation, not a converged finite-temperature HgCdTe prediction.

## Authorized next gates

- complete issue #285 B0 source-capability audit;
- pin the exact QE/EPW release and source commit before executable validation;
- specify immutable short-range matrix and generalized-Fröhlich schemas;
- prove no-double-counting algebraically and with synthetic tests;
- perform only separately authorized, decision-changing upstream or synthetic executable tests;
- propose a CdTe smoke test only after B0 passes.

## Unsupported claims

This program does not currently support:

- converged phonons, dielectric response, or Born charges for the terminated CdTe setup;
- A1 readiness or converged AHC corrections for CdTe, HgTe, or HgCdTe;
- a validated generalized-Fröhlich correction for CdTe;
- a validated finite-temperature 8-band parameter set;
- production SQS, CPA, SCBA, or alloy calculations;
- a new universal bandgap equation derived from incomplete endpoint data;
- treating software projection correctness as material validation;
- treating internal EPW matrix arrays as a validated user-facing export.

## Shared dependencies

Kane Hamiltonians, symmetry utilities, matrix datasets, endpoint provenance, and gap benchmarks are shared with distributional observables and any future correlated-random-mass program.

## Computation gate

No expensive calculation should begin unless it targets a decision-changing observable, has an independent validation target, and includes an explicit termination criterion. CdTe/HgTe/alloy AHC, dense EPW, production special displacement, and any retry of the terminated CdTe polar-response path remain closed.