# Browder 1972 CdTe expansion bridge

## Question

Can the official Browder-Ballard 10-300 K CdTe table close the missing 90-293 K integral in the CdTe zero-temperature lattice derivation?

## Evidence class

Browder and Ballard, *Applied Optics* **11**, 841-843 (1972), DOI `10.1364/AO.11.000841`, report primary three-terminal capacitance-dilatometer measurements. The exact 25-row CdTe column was transcribed from the official Optica HTML Table I.

The material is hot-pressed microcrystalline CdTe marketed as Irtran 6. It is not the single-crystal CdTe used by Smith and White or the high-purity powder used by Williams.

## Cross-source overlap

At common or interpolated temperatures, Browder minus Smith-White alpha in units of `10^-6 K^-1` is:

```text
T = 10, 15, 20, 30, 75, 85, 283 K
Delta alpha = +0.32, +0.74, +0.91, +0.70, 0.00, -0.09, +0.454
```

The overlap RMS difference is `0.558 x 10^-6 K^-1`; the maximum is `0.91 x 10^-6 K^-1`. The agreement near 75-85 K is strong, but the negative-expansion minimum is materially shallower in Irtran 6 and the high-temperature coefficient is larger.

## Zero-temperature sensitivity

Using the Williams 293.15 K anchor:

```text
Smith below 10 K + Browder 10-293 K:       a0 = 6.475761 A
Smith through 85 K + Browder 85-293 K:     a0 = 6.475904 A
same bridge shape adjusted to single-crystal endpoints:
                                             a0 = 6.476035 A
previous endpoint-linear bridge:             a0 = 6.477028 A
```

The Browder bridge shape shifts the provisional central estimate by approximately `-0.000992 A` relative to the endpoint-linear bridge. Printed table rounding contributes only about `9e-6 A`; cross-source morphology and calibration dominate.

## Decision

Browder removes the purely numerical interpolation gap but introduces an uncontrolled morphology transfer. It is therefore an informative sensitivity result, not an authorized physical geometry.

```text
ready_for_execution remains false
```

The decisive remaining source is Greenough and Palmer, *J. Phys. D* **6**, 587-592 (1973), DOI `10.1088/0022-3727/6/5/315`, because it covers single-crystal CdTe from 42 to 300 K.
