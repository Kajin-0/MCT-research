# Blue 1964 does not identify a modern signed gap

## Question

Can the positive optical-fit parameters tabulated by Blue 1964 be compared directly with a modern signed `Gamma6-Gamma8` gap relation?

No source-supported one-to-one map is available.

The obstruction is stronger than a historical sign convention. Blue's absorption model separates the observed edge position from the positive band-curvature scale used to reproduce the high-absorption spectral shape.

## Reconstructed Blue observable

The seven room-temperature rows are stored as

```text
theory_conditioned_positive_optical_gap_parameter
```

because Blue selected each value by comparing the measured absorption curve with theoretical direct-transition curves at absorption approximately above

```text
10^3 cm^-1.
```

All seven values are positive:

```text
0.030, 0.040, 0.120, 0.220, 0.250, 0.280, 0.365 eV.
```

The table does not report a signed `Gamma6-Gamma8` separation.

## Two distinct source scales

Blue states that the curvature of the conduction band is not given directly by the energy associated with the observed absorption-edge position. The edge position at a given temperature also contains lattice-dilation and lattice-vibration effects not included in the rigid-lattice Kane band structure used for the curve shape.

The source then gives an explicit hypothetical example:

```text
actual energy gap at 50 K = 0
band shape corresponds to a gap scale = 0.03 eV
```

This establishes within Blue's own interpretation that

```text
positive curvature scale != actual edge gap.
```

The equality fails even at the zero-gap boundary. The positive curvature parameter therefore cannot identify whether a modern signed band-ordering quantity is negative, zero, or positive.

## High-energy magnitude non-uniqueness

For room-temperature HgTe, Blue compares the measured absorption with theoretical curves calculated using positive gap scales of

```text
0.02 eV
0.03 eV
0.04 eV.
```

The source reports that these alternatives give essentially the same result at higher photon energies because their density-of-states contributions are similar.

This matters because the seven tabulated parameters were selected by comparison with theory in the high-absorption region. The declared fitting region is therefore also the region where the source reports weak discrimination among nearby positive curvature scales.

The source supports the statement

```text
magnitude is weakly and non-uniquely constrained in the declared comparison region.
```

It does not support a unique inversion from the tabulated parameter to an actual edge gap.

## Structural commensurability result

Let

```text
q_Blue
```

be the positive parameter used to choose a theoretical absorption-curve shape, and let

```text
E_signed = E(Gamma6) - E(Gamma8)
```

be a modern signed band-ordering quantity.

Blue's observation contract contains no source-supported function

```text
E_signed = F(q_Blue)
```

with identified sign and unique magnitude.

The source explicitly demonstrates that the actual edge gap and curvature scale can differ, and it reports weak high-energy discrimination among several curvature scales. Therefore, direct evaluation of

```text
q_Blue - E_signed_model(x,T)
```

would combine non-commensurate observables. A small or large residual would not have a defined material-law interpretation.

## Cross-source context

Later work uses an explicit signed band-ordering convention for HgTe:

- Scott 1969 describes the `Gamma6-Gamma8` gap as negative in HgTe and Hg-rich alloys;
- Groves 1967 obtains a negative HgTe separation from interband magneto-optical transitions.

Blue reports a positive room-temperature HgTe optical-fit parameter. The difference cannot be repaired by simply changing a sign label because Blue's source parameter describes a curve-shape scale that the paper itself distinguishes from the actual edge gap.

This cross-source context establishes non-commensurability. It does not establish a universal numerical correction between the optical-fit parameter and the signed magneto-optical gap.

## Executable certificate

The deterministic audit in

```text
tools/audit_blue1964_sign_identifiability.py
```

verifies:

- exactly seven source rows;
- every tabulated parameter remains positive;
- every row remains `signed_gap_eligible=false`;
- the exact source counterexample `0` versus `0.03 eV`;
- the exact near-degenerate set `0.02, 0.03, 0.04 eV`;
- zero fitted parameters;
- zero correction coefficients;
- zero signed-model evaluations.

The immutable result is

```text
validation/blue1964_sign_identifiability_reference.json.
```

## Scientific decision

The Blue table remains useful for:

- historical absorption-model analysis;
- sign-convention audits;
- observation-operator development;
- testing whether a proposed optical model reproduces the reported positive curve-shape parameter.

It is excluded from direct residual ranking of signed gap equations unless an independently validated forward observation operator is supplied.

## Not established

This audit does not establish:

- the corrected signed gap for any Blue specimen;
- whether the Blue parameter equals an absolute value of the signed gap;
- a universal offset, scale factor, or nonlinear conversion;
- validation or rejection of Hansen, Laurenti, Seiler, or Hansen-Pade;
- a unique band-curvature parameter from Blue's high-energy data;
- production-equation status;
- manuscript or submission authorization.

## Reproduction

```bash
python tools/audit_blue1964_sign_identifiability.py \
  --output-json /tmp/blue-sign-certificate.json
```
