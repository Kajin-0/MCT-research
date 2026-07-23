# Decision: retain the Moazzami reconstruction and disclose fit-window leverage

**Date:** 2026-07-23  
**Program:** R03 distributional band-edge observables with R01 comparator impact  
**Pull request:** #338

## Decision

Retain every committed Moazzami 2005 reconstructed coordinate unchanged. The visible Figure 6a plateau near `0.198 eV` is marked as an objectively defined source-pixel reversal core and is subjected to an exact deletion influence audit. It is not smoothed, interpolated, replaced, or assigned a physical mechanism.

Report the global contiguous-window omission result separately as a fit-window leverage stress diagnostic. Do not describe it as experimental uncertainty or a probability interval.

## Evidence

For the Figure 6a pair at `0.196491228` and `0.197543860 eV`:

```text
maximum identified-edge shift, pair deletion         0.116875 meV
maximum identified-edge shift, deletion + corners    0.959441 meV
identified operator span after pair deletion          5.121875 meV
```

Across every contiguous one-, three-, and five-point omission:

```text
minimum non-boundary operator span, x=0.226    4.984375 meV
minimum non-boundary operator span, x=0.310    3.385375 meV
minimum span / Hansen-Seiler separation        19.5764, 19.1746
```

The largest multi-point shifts occur when the earliest fit points are removed from flexible fractional-power fits, not when the visible Figure 6a reversal core is removed.

## Interpretation

The questioned visual feature does not control the central operator-spread result under the declared fitted-edge stability criterion. The broader stress test nevertheless establishes practical low-energy fit-window leverage, especially for the free-exponent operator.

## Authorized claims

- exact reversal-core influence is sub-meV, including the declared coordinate corners;
- no correction of the nominal reconstructed trace is warranted;
- flexible fitted edges are conditioned by lower fit-window membership;
- the operator-spread-versus-equation-separation conclusion survives all tested window omissions;
- the robustness result is deterministic and observation-family-conditioned.

## Prohibited claims

- the plateau is proven physical or proven artifactual;
- the deleted-window ranges are confidence intervals or experimental covariance;
- all fitted operators are locally stable below 1 meV under arbitrary multi-point deletion;
- a boundary-limited fit is identified because deletion does not move it;
- the result generalizes to native spectra, other specimens, or other operator families without further evidence.

## Publication consequence

Figure 2 should display the reconstructed coordinates and fitted operators without correcting the plateau. The exact reversal core may be marked as an audited source-coordinate region. The manuscript must distinguish coordinate perturbation, exact feature influence, global fit-window leverage, and observation-model spread.
