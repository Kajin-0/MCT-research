# Research contribution and manuscript registry

This registry tracks distinct scientific works that share the repository. It records contribution status without forcing one work to become the repository-wide flagship.

## Status vocabulary

- `foundation`: validated infrastructure or result used by other works;
- `active-result`: a scoped scientific result under development;
- `candidate-work`: a coherent potential paper or completed technical work;
- `manuscript-authorized`: writing is authorized for a defined work;
- `submission-ready`: work-specific evidence and packaging gates passed;
- `gated`: work may proceed only after stated prerequisites;
- `retired`: the artifact is preserved historically but is not an active scientific output.

## Registry

| ID | Working contribution | Program | Current status | Manuscript state | Main evidence or issues |
|---|---|---|---|---|---|
| R01 | Provenance-controlled reconstruction and comparison of HgCdTe empirical gap laws | Empirical bandgap reconstruction | Foundation / active data acquisition | No active manuscript recorded | #1, #8, #17, #20 |
| R02 | Symmetry-resolved Kane projection and finite-temperature matrix infrastructure | Finite-temperature Kane and electronic structure | Foundation with gated computations | No active manuscript recorded | #2, #4, #5, #6, #46, #90 |
| R03 | Distributional, modality-aware theory of reported HgCdTe band edges | Distributional band-edge observables | Candidate work; analytical foundations implemented | No active manuscript; prior weak draft retired | #22, #167; distributional and observation modules |
| R04 | Scale-dependent spatial disorder under finite measurement kernels | Measurement-kernel-aware spatial disorder | Active-result / candidate work | Manuscript not yet authorized; experimental specification, validation-path, and prior-art gates remain | #196, #215, #218, #220, #224, #228, #230, #232; PRs #199, #202, #204, #207, #210, #212, #216, #219, #221, #227, #229, #231, #233 |
| R05 | Correlated random-mass Kane regime with finite correlation length | Correlated random-mass Kane | Gated | No manuscript authorized | Requires independent length-scale, novelty, and model-validity gates |

## Historical manuscript note

The manuscript and submission bundle associated with PR #194 were later judged scientifically insufficient and removed from active publication status. Their history remains in Git and issue/PR records, but they do not define the state of R03, R04, or the repository as a whole.

## Registry update rule

Update this file when any of the following occurs:

- a result becomes a distinct candidate work;
- manuscript writing is authorized or halted;
- a submission gate passes or fails;
- a work is split into separate papers;
- a contribution is merged into another work;
- a work is retired;
- a shared foundation changes the scientific scope of multiple works.

A code merge alone does not automatically promote a contribution to `candidate-work`, `manuscript-authorized`, or `submission-ready`.
