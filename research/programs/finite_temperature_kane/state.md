# Program state: finite-temperature Kane and electronic structure

**Portfolio contribution:** R02  
**State:** validated infrastructure with current CdTe polar-response path terminated

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
- #271 — completed bounded CdTe `zeu`/`zue` route comparison.

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
- one CdTe A0 breadth point, one stricter-response diagnostic, and one same-state `zeu`/`zue` comparison.

## CdTe physical-volume state

Issue #46 is complete. The accepted fixed-volume A0 reference is

```text
a_ref(0 K) = 6.476035479332049 A
conservative absolute bound = +/-0.001814959409196 A
```

The source chain uses Williams 1969, Smith and White 1975, and the endpoint-adjusted Browder and Ballard 1972 CdTe bridge. The decision is adequate only for the declared `+/-0.5%` volume-sensitivity bracket; it is not a metrology-grade universal zero-temperature lattice constant or a quasiharmonic path.

## CdTe A0 polar-response state

The first A0 point and stricter-response diagnostic failed the raw Born-charge gate. The separately authorized same-state route comparison has now resolved the remaining immediate diagnostic question.

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

- the current tested polar-response path is terminated for A1;
- A1 electron--phonon work remains unauthorized;
- no retry, convergence ladder, altered calculation, or charge-ASR repair is authorized;
- no separate k-grid/cutoff design review is authorized from this failed gate;
- any future alternative backend, functional, pseudopotential, or short-range/nonpolar design requires a new analytical decision record and independent authorization.

Controlling records:

```text
first_principles/a0/cdte_a0_zeu_zue_reference_result.json
research/decision_records/2026-07-22-cdte-zeu-zue-termination.md
```

## Unresolved scientific questions

- whether a different independently validated backend or response model can support polar CdTe AHC;
- whether a scientifically useful short-range/nonpolar finite-temperature tranche can be defined without concealing the missing polar contribution;
- how electron-phonon self-energies should be projected into the Kane basis;
- whether scalar parameter renormalization is adequate or matrix-valued temperature dependence is required;
- what alloy interpolation or disorder treatment is justified between CdTe and HgTe.

## Manuscript status

No active manuscript is recorded. The current result is infrastructure and methodological foundation, not a converged finite-temperature HgCdTe prediction.

## Authorized next gates

- perform analytical architecture selection only;
- compare alternative backends or short-range/nonpolar decompositions without executing them;
- validate endpoint exports and convergence before any HgTe production work;
- perform only separately authorized, decision-changing calculations with predeclared stopping rules;
- compare projected parameters against independent experimental observables.

## Unsupported claims

This program does not currently support:

- converged phonons, dielectric response, or Born charges for the tested CdTe setup;
- A1 readiness or converged AHC corrections for CdTe, HgTe, or HgCdTe;
- a validated finite-temperature 8-band parameter set;
- production SQS, CPA, SCBA, or alloy calculations;
- a new universal bandgap equation derived from incomplete endpoint data;
- treating software projection correctness as material validation.

## Shared dependencies

Kane Hamiltonians, symmetry utilities, matrix datasets, endpoint provenance, and gap benchmarks are shared with distributional observables and any future correlated-random-mass program.

## Computation gate

No expensive calculation should begin unless it targets a decision-changing observable, has an independent validation target, and includes an explicit termination criterion. Production AHC, dense EPW, HgTe, alloy calculations, and any retry of the terminated CdTe polar-response path remain closed.
