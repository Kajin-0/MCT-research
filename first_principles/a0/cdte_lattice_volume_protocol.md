# CdTe A0 lattice and fixed-volume protocol

## Status

The **physical-volume provenance gate is closed for the declared A0 fixed-volume
sensitivity calculation**.

The selected reference is

```text
a_ref(0 K) = 6.476035479332049 A
conservative absolute bound = +/-0.001814959409196 A
```

The bound corresponds to a maximum first-order volume uncertainty of
approximately `0.08410%`, or `16.82%` of one side of the declared `+/-0.5%`
volume-sensitivity bracket.

This is an uncertainty-bounded computational reference, not a metrology-grade or
universal zero-temperature CdTe lattice constant. Overall A0 execution remains
blocked until the pinned runtime binaries, release-specific syntax, runtime
pseudopotential copies, and rendered input manifests are validated.

The former `6.482 A` value is superseded and must not be used as an execution
input.

Machine-readable records:

```text
first_principles/a0/cdte_lattice_execution_decision.json
first_principles/a0/browder1972_optica_table_source.json
first_principles/a0/cdte_a0_run_spec.json
tools/derive_cdte_execution_lattice.py
```

## Why the separation matters

The computational target is the fixed-volume electron-phonon contribution,
not the total experimental temperature dependence of the gap. Use one physical
reference volume for every electron-phonon temperature point:

```text
Delta E_n^ep(T; V_ref) = E_n^ep(T; V_ref) - E_n^ep(0; V_ref)
```

A future quasiharmonic contribution is a different object:

```text
Delta E_n^qh(T) = E_n^static[V(T)] - E_n^static(V_ref)
```

Only after both pieces are independently converged may they be added once. A
calculation that changes lattice with temperature inside the electron-phonon
run and later adds a quasiharmonic term would double count volume effects.

A0 authorizes only fixed-volume static, coarse phonon, dielectric, and Born-charge
sanity work after every runtime readiness check passes. It does not authorize a
production quasiharmonic path.

## Reference-volume definition

For cubic CdTe,

```text
a(T) = a(T_anchor) exp[integral(T_anchor -> T) alpha_L(T') dT']
```

The accepted execution chain contains:

1. a primary absolute CdTe lattice anchor;
2. primary single-crystal low-temperature expansion;
3. a primary full-range CdTe bridge shape;
4. hashes identifying the exact source data;
5. an explicit morphology-transfer bound;
6. an auditable integration and decision manifest.

## Primary absolute anchor: Williams 1969

```text
M. G. Williams, R. D. Tomlinson, and M. J. Hampshire,
Solid State Communications 7, 1831-1832 (1969),
DOI 10.1016/0038-1098(69)90296-8
PDF SHA-256 963891204abd0b3c434297eec3a1d337c7bc67a3b937eda4bdfc373746702bab
```

Williams measured `99.999%` CdTe by calibrated X-ray powder diffraction. The
published polynomial gives

```text
a(293.15 K) = 6.480841894 A
```

The maximum observed-minus-fit residual plus the stated temperature-control
bound gives a conservative absolute anchor bound of `0.000579 A`.

This quantity is explicitly a reconstructed conservative bound, not a reported
standard uncertainty.

## Primary low-temperature expansion: Smith and White 1975

```text
T. F. Smith and G. K. White,
J. Phys. C: Solid State Phys. 8, 2031-2042 (1975),
DOI 10.1088/0022-3719/8/13/012
PDF SHA-256 521e58912b46c6fba70f6e7c24135d79e8aa50d8ddc93addbaf97c4d38f74237
```

Direct single-crystal CdTe data are used through `85 K`. Below `4 K`, the
published law is

```text
alpha_L(T) = -(170 +/- 10)e-12 T^3 K^-1.
```

## Primary bridge shape: Browder and Ballard 1972

```text
J. S. Browder and S. S. Ballard,
Applied Optics 11, 841-843 (1972),
DOI 10.1364/AO.11.000841
```

The official Optica HTML Table I contains 25 CdTe Irtran-6 rows over `10-300 K`.
The committed transcription matches all publisher values exactly.

```text
canonical publisher-table SHA-256
832c7b191d1a93a5f828e63125ea8dcd18e42c998b33f77b3ee1239f54a5afe7
```

The surrounding publisher HTML is dynamic and is therefore not the authoritative
source identity. The canonicalized publisher rows are the stable data object.

Browder measured microcrystalline hot-pressed CdTe rather than the single-crystal
material used by Smith and White. The curve is therefore used as a bridge shape,
not assumed to transfer exactly.

## Endpoint adjustment and conservative morphology bound

The bridge calculation:

1. integrates Smith and White through `85 K`;
2. interpolates Browder Table I from `85 K` to `293.15 K`;
3. linearly adjusts the bridge so `alpha(85 K)` matches Smith and White and
   `alpha(293.15 K)` matches the Williams polynomial derivative;
4. integrates the adjusted curve to the Williams absolute anchor.

This gives

```text
a_ref(0 K) = 6.476035479332049 A
```

The largest observed absolute Browder-minus-Smith coefficient difference is

```text
0.91e-6 K^-1
```

To bound morphology transfer conservatively, that **largest discrepancy is
applied as a constant signed error over the entire unresolved 85-293.15 K
interval**. Exact exponential propagation gives

```text
morphology-transfer lattice bound = 0.001226784157284 A
```

The total absolute bound is the linear sum

```text
Williams anchor bound             0.000579000000000 A
morphology-transfer bound         0.001226784157284 A
publisher-table rounding bound    0.000009175251911 A
----------------------------------------------------------------
total conservative bound          0.001814959409196 A
```

This deliberately avoids assigning a probability distribution or calling the
result a standard uncertainty.

## Cross-check containment

Every existing independent or alternative bridge result lies inside the bound:

| Bridge | a0 (A) | Offset from selected value (A) |
|---|---:|---:|
| Bagot/Bogucki secondary analytic fit | 6.476427457559 | +0.000391978227 |
| previous endpoint-linear bridge | 6.477027844498 | +0.000992365166 |
| Smith below 10 K + raw Browder | 6.475761132656 | -0.000274346676 |
| Smith through 85 K + raw Browder | 6.475903772580 | -0.000131706752 |

The largest cross-check offset is smaller than the morphology-transfer component
alone.

## Greenough and Palmer scope correction

```text
R. D. Greenough and S. B. Palmer,
Journal of Physics D 6, 587-592 (1973),
DOI 10.1088/0022-3727/6/5/315
PDF SHA-256 3f6a2a39b2047d3d00c375a7441068ba88712429719b5826318876230bf46781
```

This source is accepted for the single-crystal `50-100 K` anomaly and sample
provenance. The printed article does not expose a numerical or graphical
`100-293 K` expansion curve, so it is not the high-temperature bridge.

## Explicitly excluded citation

Collins et al., J. Phys. C 13, 1649-1656 (1980), DOI
`10.1088/0022-3719/13/9/011`, reports ZnTe and HgTe rather than CdTe and is
excluded from the CdTe execution chain.

## Volume-sensitivity points

The A0 bracket is defined in **volume**, not lattice constant:

```text
Delta V / V_ref = -0.005, 0, +0.005
a / a_ref = (V / V_ref)^(1/3)
```

| Delta V / V_ref | a / a_ref | Delta a / a_ref |
|---:|---:|---:|
| -0.005 | 0.9983305478136913 | -0.0016694521863087 |
| 0 | 1 | 0 |
| +0.005 | 1.001663896579312 | +0.001663896579312 |

The conservative provenance interval produces a maximum volume difference of
`0.000841009`, which is below the declared maximum of `20%` of one side of the
`0.005` sensitivity offset.

## Remaining execution gates

The physical-volume gate is no longer blocking. Do not execute A0 until:

- Quantum ESPRESSO and ABINIT installed version outputs and executable hashes are recorded;
- release-specific syntax is validated against the pinned source versions;
- runtime pseudopotential copies match the verified selection hashes;
- every rendered QE and ABINIT input has a hash manifest;
- the generated grid reproduces `V/V_ref = (a/a_ref)^3` within tolerance.

## Stopping rules

- Keep the selected `V_ref` identical for every electron-phonon temperature point.
- Do not introduce a temperature-dependent volume path in A0.
- Do not fit an equation of state or add quasiharmonic corrections automatically.
- Do not narrow the conservative lattice bound without new primary evidence.
- Bagot primary-source acquisition is now optional validation, not a prerequisite
  for the bounded A0 sensitivity calculation.

## Claim boundary

This protocol establishes a traceable, conservative reference volume adequate
for the declared A0 sensitivity test. It does not establish:

- a universal or metrology-grade `0 K` CdTe lattice constant;
- morphology independence of CdTe thermal expansion;
- a DFT equilibrium volume;
- a quasiharmonic volume path;
- any CdTe gap, Kane-parameter, HgTe, or alloy result.
