# MCT research portfolio state

**Last updated:** 2026-07-21  
**Repository-wide coordination issue:** #213  
**Scope:** repository governance and cross-program navigation

This repository is a **research portfolio** containing multiple scientific programs that share models, datasets, literature records, validation utilities, and computational infrastructure.

This file is the repository-wide navigation ledger. It does not replace the scientific state file of any individual program.

## Interpretation rules

Terms such as `active`, `frozen`, `authorized`, `blocked`, `submission-ready`, and `retired` are **program-specific** unless a statement is explicitly marked repository-wide.

A decision in one program does not automatically:

- supersede another program;
- prohibit another program's work;
- transfer ownership of a shared module;
- determine another manuscript's publication state;
- convert a model-conditioned result into a repository-wide claim.

## Portfolio programs

| Program | State | Primary role | State file | Main issues |
|---|---|---|---|---|
| Empirical bandgap reconstruction | Active foundation | Reconstruct and benchmark composition- and temperature-dependent gap laws with explicit provenance | `research/programs/empirical_bandgap/state.md` | #1, #8, #17, #20 |
| Finite-temperature Kane and electronic structure | Gated active infrastructure | Build symmetry-resolved Kane and first-principles adapters; authorize expensive calculations only through decision gates | `research/programs/finite_temperature_kane/state.md` | #2, #4, #5, #6, #46, #90 |
| Distributional band-edge observables | Active research program | Connect latent gap distributions and specimen state to modality-specific reported edges | `research/programs/distributional_band_edge/state.md` | #22, #167 |
| Measurement-kernel-aware spatial disorder | Active research program | Determine how spatial covariance and finite probes control apparent disorder widths and cutoffs | `research/programs/spatial_disorder/state.md` | #196 |
| Correlated random-mass Kane regime | Gated future program | Study finite-correlation-length random mass in Kane/Dirac descriptions only after independent physical and novelty gates pass | `research/programs/correlated_random_mass_kane/state.md` | none controlling yet |

## Repository-wide publication state

The repository currently has **no globally designated flagship manuscript** and no repository-wide submission authorization.

Publication state is recorded per candidate work in:

- `research/contribution_registry.md`;
- the relevant program `state.md`;
- manuscript-specific decision records, when created.

A manuscript can be active, frozen, retired, or submission-ready without changing the status of unrelated works.

## Shared foundations

Shared scientific and software foundations are mapped in:

- `research/shared_foundations.md`.

Shared modules are maintained for the portfolio. A module may support several works and is not scientifically owned by the first manuscript that uses it.

## Cross-program governance

Every research PR should declare:

1. program or programs affected;
2. contribution type;
3. claim status;
4. shared dependencies;
5. manuscript impact;
6. files intentionally touched;
7. files intentionally untouched;
8. validation and falsification criteria.

The default pull-request structure is in `.github/pull_request_template.md`.

## Repository-wide standards

All programs share these minimum standards:

- explicit observable and assumption definitions;
- primary-source provenance for material claims;
- dimensional, limiting-case, and numerical checks;
- separation of source-established facts from project inference;
- uncertainty, identifiability, and sensitivity analysis where applicable;
- a stated falsification or termination test;
- no novelty claim based only on repository presence;
- no conversion of synthetic recovery into material validation;
- no expensive computation without a decision-changing target and stopping rule.

## Coordination protocol for parallel agents

Before implementation, an agent should:

1. identify the relevant program state file;
2. identify shared modules that may affect other programs;
3. open or reference a scoped issue;
4. work on a dedicated branch;
5. avoid editing another program's state or manuscript unless the PR explicitly spans both;
6. update the contribution registry when a result changes the status of a candidate work.

## Compatibility note

`research/active_program_state.md` is retained as a historical compatibility path. It redirects to this portfolio ledger and must not become a second global authority.