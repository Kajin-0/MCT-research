# Decision: frame the flagship as HgCdTe optical metrology and inverse-problem methods

**Date:** 2026-07-21  
**Issue:** #189

## Decision

The flagship manuscript will be framed as an **HgCdTe-specific semiconductor optical-metrology and inverse-problem methods paper**.

It will not be framed as a new general theory of structural identifiability.

## Reason

The audit separates established ingredients from project-specific results:

- structural identifiability is foundational prior art;
- output-preserving parameter symmetries are established methodology;
- identifiable parameter combinations are established methodology;
- Beer-Lambert attenuation already contains an absorption/path-length product;
- Chang already establishes effective-thickness-dependent detector cutoff;
- Herrmann already establishes gap-distribution-induced apparent tails.

The defensible contribution is the HgCdTe-specific composition of those ingredients into one source-grounded forward hierarchy, followed by explicit parameter combinations, model-specific rank bounds, exact counterexamples, and measurement-design consequences.

## Primary claim hierarchy

1. **Central application-specific result:** the declared distributed HgCdTe spectrum depends on five nominal parameters through only `Eg0+Delta`, `sigma_G`, and `A*d`.
2. **Supporting application-specific result:** tail-only Chang cutoffs have rank at most two for four nominal parameters.
3. **Strong quantitative demonstrations:** machine-precision spectral equivalence, 60.1% fit-window dependence, mixed-branch conditioning, and the Dingrong printed-parameter inconsistency.

## Required language

Use:

> We derive model-specific structural-identifiability bounds for a distributional HgCdTe band-edge operator.

Do not use:

> We introduce a new structural-identifiability theory for spectroscopy.

Use:

> The reduced single-pass model inherits the standard optical-depth product degeneracy.

Do not use:

> We discover the amplitude-thickness degeneracy.

Theorem labels remain permitted because the statements are exact under declared assumptions. A theorem label does not imply unprecedented mathematics.

## Consequences

- General identifiability and optical-inversion sources must appear in the bibliography and prior-work discussion.
- The abstract and introduction must describe the rank bounds as model-specific.
- The discussion must identify the Beer-Lambert and Chang components as prior art.
- The manuscript must include the Dingrong source-table reproduction and its source-internal consistency boundary.
- Additional infrastructure work remains frozen unless required for submission or direct scientific validation.

## Rejected alternatives

- universal HgCdTe bandgap-equation paper;
- general mathematical identifiability paper;
- complete microscopic absorption theory;
- claim of complete external spectrum validation.

## Revisit condition

Reopen this decision only if a prior source is found that states one of the application-specific rank bounds at comparable HgCdTe and observation-operator specificity, or if a journal requires a fundamentally different contribution hierarchy.
