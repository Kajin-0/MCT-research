# Exhaustive reduction frontier for the static CdTe Weiler space

## Status

The conventional quadratic Kane model removes six established directions from the complete ten-dimensional Weiler space:

```text
N2, G, G',
delta_gamma1, delta_gamma2, delta_gamma3.
```

All `2^6 = 64` subsets were tested to determine whether a compact extension can reproduce the validated complete-space static CdTe signal.

The target in this analysis is the complete ten-dimensional projection recorded in

```text
first_principles/a0/cdte_weiler_class_reference_result.json.
```

It is not a new fit to the raw DFT matrices. The complete projection differs from those matrices only at the previously reported approximately `1e-5` relative closure level.

## Reduction basis

The four-dimensional conventional tied space is augmented by an orthonormal six-dimensional departure basis:

1. `N2`;
2. `G`;
3. `G'`;
4. the direction in `gamma1/gamma1'` orthogonal to the conventional tie;
5. the direction in `gamma2/gamma2'` orthogonal to the conventional tie;
6. the direction in `gamma3/gamma3'` orthogonal to the conventional tie.

The combined basis is orthonormal to `6.28e-16` and spans the complete projector to `9.30e-15`.

Every subset is refit on `[001]` and `[111]`; `[110]` remains unused.

## Pareto frontier

The best model for each number of added departures is:

| Added departures | Best subset | Dimension | Training residual | `[110]` residual | Worst residual |
|---:|---|---:|---:|---:|---:|
| 0 | none | 4 | 48.19% | 48.53% | 48.53% |
| 1 | `delta_gamma3` | 5 | 41.57% | 38.89% | 41.57% |
| 2 | `delta_gamma2`, `delta_gamma3` | 6 | 33.66% | 35.09% | 35.09% |
| 3 | `G'`, `delta_gamma2`, `delta_gamma3` | 7 | 27.68% | 26.66% | 27.68% |
| 4 | `G'`, all three gamma departures | 8 | 20.86% | 19.95% | 20.86% |
| 5 | `G`, `G'`, all three gamma departures | 9 | 15.22% | 10.47% | 15.22% |
| 6 | all six | 10 | <1e-12 | <1e-12 | <1e-12 |

The minimum numbers of departures required to place both training and holdout below each threshold are:

| Maximum allowed residual | Minimum departures |
|---:|---:|
| 25% | 4 |
| 20% | 5 |
| 10% | 6 |
| 5% | 6 |
| 1% | 6 |

## Leave-one-out diagnosis

Starting from the complete model, omit one departure at a time:

| Omitted departure | Training residual | `[110]` residual | Worst residual |
|---|---:|---:|---:|
| `N2` | 15.22% | 10.47% | 15.22% |
| `G` | 14.27% | 16.99% | 16.99% |
| `delta_gamma1` | 18.19% | 17.69% | 18.19% |
| `G'` | 19.16% | 22.81% | 22.81% |
| `delta_gamma2` | 24.39% | 16.77% | 24.39% |
| `delta_gamma3` | 24.37% | 29.02% | 29.02% |

This ordering is specific to the present directions and repository normalization. It should not be interpreted as a universal hierarchy of Weiler parameters.

## Decision

The static smoke does not support a quantitatively accurate compact extension of the conventional quadratic model.

- Four added departures are needed merely to reach approximately 20% error.
- Five departures still leave a worst residual of approximately 15.2%.
- All six are required to pass the declared 10% decision threshold.

Therefore the appropriate static model decision is:

> Freeze the quadratic matrix model at the complete ten-dimensional Weiler space. Do not invent a smaller parameterization merely for algebraic convenience.

This does not mean every future HgCdTe model must always fit ten unconstrained parameters. Physical relations may emerge across composition, temperature, or higher-quality calculations. They are not supported by this single static CdTe smoke point.

## Program consequence

The bounded depth-first sprint has answered its intended question:

1. the linear two-`P` sector closes;
2. the conventional quadratic sector fails;
3. finite-radius error does not explain the failure;
4. the complete established Weiler space closes;
5. no compact subset of the six missing directions reaches 10% train-and-holdout accuracy.

Further static Hamiltonian elaboration now has low marginal value. Program effort should return to breadth:

- independent Hg-rich experimental/provenance data;
- CdTe A0 lattice and execution readiness;
- exact standard Weiler normalization as a documentation task;
- novelty and publication framing;
- no phonon, AHC, HgTe, or alloy computation until the broader gates are satisfied.
