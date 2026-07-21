# Submission gap and acquisition queue

## Current state

The flagship manuscript now has:

- a complete analytical draft;
- stable theorem and proposition numbering;
- a C01-C23 claim/evidence matrix;
- five immutable numerical validation records;
- seven deterministic SVG figures;
- three deterministic manuscript tables;
- complete Python 3.11/3.13 CI coverage;
- an auditable DOI intake manifest and external-validation route gate.

The manuscript is **not yet ready for preferred journal submission** because one calibrated external material validation case and publication packaging remain incomplete.

## Hard scientific submission blocker

At least one real-spectrum or same-specimen multi-state case must test a merged forward operator without silently assigning missing specimen parameters.

A qualifying case should provide as many of the following as possible:

- source-native or auditable numerical spectrum;
- independently measured composition and uncertainty;
- measurement temperature;
- carrier type and density;
- physical and effective optical thickness provenance;
- reflectance or transmission convention;
- spectral resolution and calibration;
- edge/cutoff definition;
- fitted-parameter covariance or enough raw data to estimate it;
- processing and annealing state.

The validation does not need to identify every unified-model parameter. It must test at least one declared forward prediction while retaining unresolved parameters as nuisance or bounded quantities.

## Selected first validation route

The deterministic gate selects:

> **Chang multi-thickness / cutoff validation**

Current gate state:

```text
score      24
readiness  ready_after_retrieval
```

Required source pair:

```text
10.1007/s11664-007-0162-0
10.1063/1.2245220
```

The route tests the exact prediction:

```text
E_cut(d2)-E_cut(d1)=-W ln(d2/d1)
```

and the structural result:

```text
rank(J_tail) <= 2
```

for tail-only cutoffs.

### Required Chang evidence

- native or quantitatively calibratable spectra;
- same-specimen `W`, `b`, and amplitude;
- temperature and carrier state;
- effective optical thickness or optical-depth calibration;
- exact detector 50% response construction;
- evidence identifying intrinsic versus tail crossings;
- any supplement or source data behind Figure 2.

### Chang rejection gates

The route is rejected for quantitative validation when:

- Figure 2 cannot be calibrated;
- `W` and `b` cannot be assigned to the same specimen;
- effective thickness remains undefined;
- the reported temperature inconsistency cannot be resolved;
- a parameter belongs to the separate `x=0.23` calculation rather than the `x=0.21` spectrum;
- only tail-only points exist and no independent parameters can be constrained.

The source-specific `b=103+/-2 meV` value may not be transferred between specimens without explicit source ownership.

## Highest-value carrier source

The highest-value single paper for extending the physical carrier branch remains:

```text
10.1016/0038-1098(85)90315-1
```

The Dingrong route is ranked second:

```text
score      20
readiness  ready_after_retrieval
```

It can potentially replace the generic carrier marker with a source-grounded physical spectrum. It currently requires:

- complete interband filling equations;
- complete below-gap free-carrier and two-mode phonon equations;
- all band, dielectric, phonon, impurity, and scattering parameters;
- calibrated or digitizable 77-300 K spectra;
- specimen thickness and optical geometry;
- exact reported edge definition.

Dingrong remains a high-payoff request, but it requires a larger model and nuisance-state audit than the Chang route.

## Deterministic route ranking

The current acquisition state gives:

```text
1  Chang thickness/cutoff                 24
2  Dingrong carrier spectrum              20
3  Chu intrinsic absorption               19
4  Herrmann multimodal tail               18
5  Teppe transition series                18
6  Moazzami source-native recovery         16
7  Ivanov-Omskii PL joint closure          15
8  Finkman independent tail                14
9  Krishtopenko prior-art audit             2
```

The score ranks expected decision value, not truth probability. It must be recomputed after every source audit.

Controlling records:

```text
literature/acquisition/distributional_band_edge_sources.json
literature/acquisition/source_intake_protocol.md
data/validation/external_validation_route_gate.json
research/decision_records/2026-07-21-external-validation-route-selection.md
```

## User-assisted DOI request order

### Request first — selected route

```text
10.1007/s11664-007-0162-0
10.1063/1.2245220
```

Useful additions beyond an ordinary PDF:

```text
supplement
source-native data
high-resolution figures
fitted parameter tables
same-specimen W and b
amplitude and effective thickness
carrier state
50-percent response construction
```

### Request alongside — highest physics payoff

```text
10.1016/0038-1098(85)90315-1
```

Useful additions:

```text
complete equations
all source parameters
77-300 K numerical spectra
specimen thickness
optical geometry
edge-definition details
```

### Remaining queue

```text
10.1016/0020-0891(91)90110-2    Chu broad intrinsic absorption
10.1016/0022-0248(92)90851-9    Herrmann multimodal broadening
10.1038/ncomms12576              Teppe transition series and supplement
10.1007/s11664-005-0019-3        Moazzami source-native Paper I data
10.1016/j.physb.2009.08.210     Ivanov-Omskii PL/annealing
10.1063/1.333828                  Finkman independent tail
10.1103/PhysRevB.106.115203      Krishtopenko prior-art boundary
```

## Source intake procedure

Every retrieved paper or supplement follows:

```text
literature/acquisition/source_intake_protocol.md
```

Minimum sequence:

1. preserve the original filename and unmodified artifact;
2. verify DOI and source version;
3. classify rights and redistribution status;
4. compute and record SHA-256;
5. audit specimen ownership for every parameter and spectrum;
6. audit equations, units, conventions, external definitions, and valid domain;
7. audit figure calibration and curve ownership;
8. update the source manifest;
9. recompute validation-route ranking;
10. open a separate issue and PR before changing any operator.

A publisher PDF is not committed to the public repository merely because the user supplied it. Citations, hashes, permitted notes, equation audits, digitizations, and derived data remain the default public artifacts.

## Completed manuscript packaging

### Analytical core

Complete:

- abstract through conclusion;
- theorem index;
- claim matrix;
- prior-art boundaries;
- reproducibility statement;
- submission boundary.

### Figures and tables

Complete deterministic review package:

```text
python -m tools.build_distributional_band_edge_manuscript_assets \
  --repository-root . \
  --output-dir distributional-generated
```

Outputs:

```text
7 SVG figures
3 Markdown tables
1 machine-readable asset summary
```

The assets are regenerated from immutable records and public package functions. Final journal PDF conversion remains pending but may not alter numerical content.

## Publication packaging still required

### External validation

- intake and audit the selected Chang source pair;
- execute the route only if the sources pass rejection gates;
- otherwise record rejection and recompute the gate;
- preserve exact theorem claims regardless of validation outcome.

### Bibliography

- verify title, author order, year, volume, pages, and DOI for every cited source;
- distinguish the 2006 and 2007 Chang papers;
- verify all reconstructed historical gap-law citations;
- add Paper I citation only after its archival identifier exists.

### Manuscript editing

- integrate stable theorem labels into the journal-formatted manuscript;
- perform final notation review for `Eg0`, signed gap, `G`, `sigma_G`, `W`, `s`, `A`, and `d`;
- separate material-state parameters from observation-operator parameters in every caption and table;
- reduce repeated caveats without weakening claim boundaries.

### Administrative packaging

- authors and affiliations;
- CRediT roles;
- conflicts and funding statements;
- data/code availability statement;
- archive DOI and immutable release;
- suggested reviewers and exclusions;
- cover letter;
- journal-specific formatting.

## Journal positioning

Position the work as analytical and computational **semiconductor optical metrology / inverse-problem research**, not as:

- a new universal HgCdTe bandgap equation;
- a converged first-principles material calculation;
- a universal Urbach-to-disorder conversion;
- or a production detector correction.

The final venue should be selected after the validation outcome determines whether the dominant framing is applied physics, semiconductor characterization, or measurement science.

## Submission decision rule

Preferred submission is authorized when:

- all exact theorem statements pass code/manuscript consistency checks;
- all synthetic results remain visibly labeled;
- one external validation case is complete;
- final SVG-to-PDF conversion is verified;
- bibliography and prior-art boundaries are complete;
- archive and authorship metadata are complete.

A later explicit decision may authorize theorem/methods-only submission if the documented acquisition program fails to yield a qualifying external dataset. That decision may not imply specimen-level validation.

External collaborators are not a prerequisite. Public full texts, author manuscripts, supplements, auditable digitization, and reproducible computation remain the primary acquisition strategy.
