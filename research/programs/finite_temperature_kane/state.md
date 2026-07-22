# Program state: finite-temperature Kane and electronic structure

**Portfolio contribution:** R02  
**State:** validated infrastructure with gated physical calculations

## Objective

Develop symmetry-resolved 8-band Kane parameterization and finite-temperature matrix workflows that can connect first-principles endpoint calculations to defensible HgCdTe electronic-structure models.

## Controlling issues

- #2 — finite-temperature prior-art audit;
- #4 — binary endpoint calculation sequence;
- #5 — Gamma double-group and broader Kane symmetry extensions;
- #6 — deferred generalized matrix-data pipeline;
- #46 — completed CdTe lattice and thermal-expansion provenance;
- #90 — historical electronic-structure authorization ledger;
- #261 — CdTe Born-charge and screening failure diagnosis.

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
- one CdTe A0 breadth point and one stricter-response diagnostic.

## CdTe physical-volume state

Issue #46 is complete. The accepted fixed-volume A0 reference is

```text
a_ref(0 K) = 6.476035479332049 A
conservative absolute bound = +/-0.001814959409196 A
```

The source chain uses Williams 1969, Smith and White 1975, and the endpoint-adjusted Browder and Ballard 1972 CdTe bridge. The decision is adequate only for the declared `+/-0.5%` volume-sensitivity bracket; it is not a metrology-grade universal zero-temperature lattice constant or a quasiharmonic path.

Controlling records:

```text
first_principles/a0/cdte_lattice_volume_protocol.md
first_principles/a0/cdte_lattice_execution_decision.json
first_principles/a0/cdte_a0_run_spec.json
```

## CdTe A0 polar-response state

The first A0 point and one stricter-response diagnostic do not pass the polar-response gate.

With only

```text
ecutrho        456 -> 570 Ry
ph tr2_ph      1e-10 -> 1e-14
```

changed, the diagnostics move as follows:

```text
raw acoustic magnitude       183.63 -> 20.55 cm^-1
ASR optical relative shift    26.985% -> 0.949%
absolute Born-charge sum       0.51611 -> 1.25251 e
```

The stricter point also reports approximately `31.2 kbar` pressure, a `0.4973 eV` direct Gamma gap, and `epsilon_infinity = 62.33`.

The improved phonon/ASR metrics do not compensate for an order-unity Born-charge neutrality failure that worsens under tightening. Therefore:

- polar dielectric and Born-charge outputs are not validated;
- A1 electron--phonon work remains unauthorized;
- no broad numerical ladder is authorized;
- charge-ASR projection must not be used to conceal the raw response failure.

Issue #261 records the analytical diagnosis and a possible one-run discriminating test comparing QE's independent `zeu` and `zue` charge algorithms plus sampled occupied--unoccupied separations. That run requires separate authorization.

## Unresolved scientific questions

- whether the current PBE/SOC/pseudopotential response path can satisfy charge neutrality and route agreement;
- whether the available endpoint calculations are sufficiently converged for material inference;
- how electron-phonon self-energies should be projected into the Kane basis;
- whether scalar parameter renormalization is adequate or matrix-valued temperature dependence is required;
- what alloy interpolation or disorder treatment is justified between CdTe and HgTe.

## Manuscript status

No active manuscript is recorded. The current result is infrastructure and methodological foundation, not a converged finite-temperature HgCdTe prediction.

## Authorized next gates

- complete the source-grounded Issue #261 diagnosis;
- decide whether one same-state `zeu`/`zue` comparison has sufficient decision value for separate authorization;
- validate endpoint exports and convergence before any HgTe production work;
- perform only decision-changing, bounded calculations with predeclared stopping rules;
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

No expensive calculation should begin unless it targets a decision-changing observable, has an independent validation target, and includes an explicit termination criterion. Production AHC, dense EPW, HgTe, and alloy calculations remain closed.