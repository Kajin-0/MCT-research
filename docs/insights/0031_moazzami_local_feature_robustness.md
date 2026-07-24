# Moazzami 2005 local-feature robustness and fit-window leverage

## Question

Does the visible plateau near `0.198 eV` in the reconstructed Moazzami 2005 Figure 6a solid IRSE trace control the fitted edge or the manuscript's observation-model conclusion?

## Source-coordinate diagnosis

The committed reconstruction preserves the raw source-image centerline coordinates. Inside the declared `600-5000 cm^-1` fit population, Figure 6a contains one objectively defined adjacent source-pixel reversal:

```text
energy_eV       source_pixel_y_center
0.196491228     160.0
0.197543860     163.0
```

Increasing image `y` maps to decreasing absorption. The three-pixel reversal is therefore the source-coordinate origin of the short plateau after nondecreasing isotonic reconstruction. The available bitmap cannot determine whether the reversal is physical, instrumental, printed, rasterization-induced, or digitization-induced.

## Exact feature-core audit

The exact two-coordinate pair is deleted without smoothing, interpolation, replacement, or any change to the remaining fit population. Every fitted observation operator is recomputed. Boundary-limited candidates remain in the machine record but are excluded from stability certification.

For `x=0.226`:

```text
maximum non-boundary shift, pair deletion only       0.116875 meV
maximum non-boundary shift, pair deletion + corners  0.959441 meV
non-boundary operator span after pair deletion        5.121875 meV
```

The exact feature core therefore does not control the multi-meV operator spread under the declared `1 meV` fitted-edge stability criterion.

Across the five smaller objectively defined reversal pairs in the `x=0.310` trace, the maximum non-boundary shifts are:

```text
pair deletion only             0.139125 meV
pair deletion + corners        0.705191 meV
```

No spectrum correction is authorized.

## Global sliding-window stress test

Every possible contiguous one-, three-, and five-point window is also removed from the fixed fit population. This is an adversarial leverage diagnostic, not a probability interval or an assertion that any omitted point is erroneous.

```text
                         x=0.226       x=0.310
leave-one-out maximum    0.900625      1.033500 meV
three-point maximum      2.330625      3.007750 meV
five-point maximum       3.595625      4.505000 meV
minimum operator span    4.984375      3.385375 meV
minimum span / H-S       19.5764       19.1746
```

The largest stress shifts are produced by the free-exponent fit when the earliest admitted fit points are removed. This identifies practical low-energy fit-window leverage. It does not invalidate those points or convert the deletion range into measurement uncertainty.

## Decision

Authorized:

- retain the reconstructed coordinates unchanged;
- mark the exact reversal core in Figure 2 as an audited source-coordinate feature;
- report the exact pair-deletion influence separately from the global sliding-window leverage stress;
- state that the questioned Figure 6a feature does not control the central operator-spread result;
- state that the free-exponent fit has material low-energy fit-window leverage;
- state that the operator-spread-versus-Hansen-Seiler conclusion survives every tested window deletion.

Not authorized:

- assign a microscopic or instrumental mechanism to the visual feature;
- smooth, interpolate, replace, or delete the pair in the nominal spectrum;
- call the sliding-window ranges confidence intervals, standard deviations, or experimental uncertainty;
- certify boundary-limited fits as stable because they remain pinned at a search bound;
- claim universal robustness beyond the two reconstructed spectra and declared operator family.
