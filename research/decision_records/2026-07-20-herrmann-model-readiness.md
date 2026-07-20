# Herrmann 1992/1993 absorption-model reconstructability

**Date:** 2026-07-20  
**Issue:** #147  
**Parent program:** #132

## Question

Can the recovered Herrmann source chain be implemented as a complete HgCdTe absorption observation model without importing unstated equations or substituting definitions from newer models?

## Recovered sources

```text
K. H. Herrmann, K.-P. Möllmann, J. W. Tomm
Broadening mechanisms near the E0 transition in narrow-gap Hg1-xCdxTe
Journal of Crystal Growth 117, 758-762 (1992)
DOI 10.1016/0022-0248(92)90851-9
```

Only the official abstract and bibliographic record are recovered for the 1992 precursor.

```text
K. H. Herrmann et al.
A new model for the absorption coefficient of narrow-gap (Hg,Cd)Te that simultaneously considers band tails and band filling
Journal of Applied Physics 73, 3486-3492 (1993)
DOI 10.1063/1.352954
source asset SHA-256 f7c470601fef398239d574134f61282bef4848984e6d0178e79ba3137a53c56d
```

The copyrighted PDFs and page images are not committed.

## Explicit model content

The 1993 companion explicitly gives:

```text
alpha(E) = alpha(E0) exp((E-E0)/We)                 Eq. (1)
We(T) = Ep + a kB T                                 Eq. (2)
BFF = f(BFF_lh, BFF_hh) approximately BFF_hh       Eq. (3)
```

It also states that the exponential and modified-square-root branches are joined continuously in equilibrium, and that the model inputs include `Eg`, effective carrier temperature, `W0`, and majority/minority carrier concentrations or quasi-Fermi levels.

## Missing executable definitions

A complete numerical model cannot be reconstructed from the recovered source chain because the 1993 companion delegates essential definitions to earlier work:

1. the modified-square-root/Kane absorption branch is attributed to Anderson 1977/1980 and is not reproduced;
2. `BFF_lh` and `BFF_hh` are not explicitly defined;
3. the carrier-density to quasi-Fermi-level mapping and nonequilibrium conventions are external;
4. composition-dependent Kane and matrix-element parameters are not specified as a complete input contract;
5. the transition solver depends on those missing high-energy and band-filling definitions;
6. the full 1992 precursor is not recovered in this tranche.

Implementing the model now would require combining formulas and parameter conventions from separate sources or replacing missing terms with newer models. That would be a hybrid construction, not a reproduction of the Herrmann operator.

## Exact Table I evidence

The audit preserves all eight rows of the 1993 Table I comparison between measured and calculated transition diagnostics. Across those rows:

```text
mean signed error in calculated (E0-Eg)       -1.825 meV
mean absolute error in (E0-Eg)                  2.350 meV
median absolute error in (E0-Eg)                1.000 meV
maximum absolute error in (E0-Eg)               8.400 meV
median calculated/measured alpha(E0) ratio      0.890209
geometric-mean alpha(E0) ratio                  0.828956
maximum alpha(E0) factor error                  2.86533
```

The table is a secondary comparison compiled from multiple cited references. It is useful for auditing the historical model's published transition behavior, but it is not independent specimen-level gap evidence.

The discrepancy metrics do not prove that the model is invalid. They show that the table cannot be summarized as uniform sub-meV or fixed-factor agreement and should be preserved row by row.

## Decision

### Authorized

- preserve the exact Table I rows as secondary model-validation diagnostics;
- report deterministic transition-offset and transition-absorption discrepancies;
- use the missing-dependency inventory to guide source recovery;
- revisit implementation only after the complete dependency chain is recovered and jointly audited.

### Unauthorized

- implement a Herrmann model using Chang, Chu, or an arbitrary modern Kane expression for missing branches;
- infer explicit band-filling factors from Eq. (3)'s symbolic approximation;
- treat the Table I `Eg` values as independent primary gap observations;
- use the table in a universal band-gap fit;
- describe the recovered source chain as a complete executable operator;
- infer that the published discrepancies establish physical invalidity.

## Reopening gate

The implementation path may be reconsidered only after recovery and joint audit of:

```text
Anderson 1977 nonequilibrium conventions
Anderson 1980 absorption-constant model
full Herrmann 1992 precursor
explicit BFF_lh and BFF_hh definitions
carrier-density/quasi-Fermi mapping
composition-dependent Kane and matrix-element parameters
```

Until then:

```text
complete_model_reconstructable   false
implementation_authorized        false
hybrid_substitution_authorized   false
universal_gap_fit_authorized     false
```
