# CdTe A0 lattice and fixed-volume protocol

## Status

The absolute room-temperature CdTe anchor and low-temperature CdTe expansion
have been acquired, hashed, and audited. The A0 execution gate remains closed
because the approximately `90-293 K` thermal-expansion integral is not bounded
tightly enough to define a validated `0 K` lattice constant.

The common `6.482 Angstrom` value remains a planning candidate only.

The detailed source audit is recorded in:

```text
docs/insights/cdte_lattice_primary_source_chain.md
tools/analyze_cdte_lattice_source_chain.py
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
calculation that changes the lattice with temperature inside the electron-phonon
run and later adds a quasiharmonic term would double count volume effects.

A0 authorizes only the fixed-volume static/phonon sanity work after the physical
volume gate closes. It does not authorize a production quasiharmonic path.

## Reference-volume definition

The preferred physical reference is the cubic zincblende lattice at `0 K`, or a
traceable extrapolation to `0 K` from primary measurements. For cubic CdTe,

```text
a(T) = a(T_anchor) exp[integral(T_anchor -> T) alpha_L(T') dT']
```

An acceptable execution source chain requires:

1. an absolute bulk CdTe lattice parameter from calibrated diffraction;
2. measurement temperature, sample state, observable definition, and uncertainty;
3. hashes of the exact primary source bytes;
4. CdTe-specific expansion data spanning the integration interval, or an
   approved uncertainty-bounded interval model;
5. an auditable integration and uncertainty manifest.

## Audited primary source A: absolute anchor

```text
M. G. Williams, R. D. Tomlinson, and M. J. Hampshire,
X-ray determination of the lattice parameters and thermal expansion of
cadmium telluride in the temperature range 20-420 C,
Solid State Communications 7, 1831-1832 (1969),
DOI 10.1016/0038-1098(69)90296-8.
PDF SHA-256 963891204abd0b3c434297eec3a1d337c7bc67a3b937eda4bdfc373746702bab
```

Williams measured `99.999 percent` CdTe with a Unicam 19 cm X-ray powder
camera. The fitted polynomial gives

```text
a(20 C) = 6.480841894 A
```

and the observed table value is `6.4809 A`. The maximum observed-minus-fit
residual over the nine rows is approximately `0.000418 A`. Combining that
envelope with the stated `+/-5 C` temperature-control bound gives a conservative
anchor bound of approximately `0.000579 A`.

The printed calculated value at `206 C` is a typographical error: the published
polynomial gives `6.4871809 A`, consistent with the observed `6.4870 A`.

The absolute approximately room-temperature anchor sub-gate is therefore closed.
It is not yet an execution lattice because the transformation to `0 K` remains
incomplete.

## Audited primary source B: low-temperature CdTe expansion

```text
T. F. Smith and G. K. White,
The low-temperature thermal expansion and Gruneisen parameters of some
tetrahedrally bonded solids,
J. Phys. C: Solid State Phys. 8, 2031-2042 (1975),
DOI 10.1088/0022-3719/8/13/012.
PDF SHA-256 521e58912b46c6fba70f6e7c24135d79e8aa50d8ddc93addbaf97c4d38f74237
```

Smith and White measured CdTe with a three-terminal capacitance dilatometer
below approximately `33 K`, between approximately `55-90 K`, and at room
temperature. For CdTe below `4 K` they report

```text
alpha_L(T) = -(170 +/- 10) e-12 T^3 K^-1.
```

Their table gives direct CdTe values through `85 K` and a room-temperature
endpoint near `283 K`. The `57.5 K` and `65 K` rows are explicitly literature
values reprinted by the authors and remain distinguished in the audit.

The low-temperature sign, negative-expansion curvature, and endpoint scale are
therefore source-anchored.

## Explicitly excluded citation

```text
J. G. Collins, G. K. White, J. A. Birch, and T. F. Smith,
J. Phys. C 13, 1649-1656 (1980),
DOI 10.1088/0022-3719/13/9/011.
```

This article reports ZnTe and HgTe, not CdTe. It is excluded from the CdTe
execution chain.

## Remaining 90-293 K interval

The accepted primary sources do not directly constrain the full expansion curve
between approximately `90 K` and room temperature. A planning-only diagnostic
using a linear central bridge and monotone endpoint bounds gives

```text
a0 central = 6.477028 A
bounded range = 6.474443 to 6.479614 A.
```

This range is not a confidence interval. It is a deliberately conservative
envelope dominated by the unmeasured bridge and is too broad for execution.

Priority primary bridge candidates are:

```text
J. S. Browder and S. S. Ballard,
Applied Optics 11, 841-843 (1972),
DOI 10.1364/AO.11.000841
```

for `10-300 K` polycrystalline CdTe, and

```text
Greenough and Palmer,
Journal of Physics D 6, 587-592 (1973),
DOI 10.1088/0022-3727/6/5/315
```

for `42-300 K` single-crystal CdTe expansion.

Before execution, either acquire and audit an adequate CdTe bridge source or
approve a separate decision memo whose uncertainty is smaller than the volume
sensitivity being tested. Do not substitute ZnTe/HgTe data.

## Volume-sensitivity points

The A0 sensitivity bracket is defined in **volume**, not lattice constant:

```text
Delta V / V_ref = -0.005, 0, +0.005
a / a_ref = (V / V_ref)^(1/3)
```

| Delta V / V_ref | a / a_ref | Delta a / a_ref |
|---:|---:|---:|
| -0.005 | 0.9983305478136913 | -0.0016694521863087 |
| 0 | 1 | 0 |
| +0.005 | 1.001663896579312 | +0.001663896579312 |

Applying `+/-0.5%` directly to the lattice constant would change volume by
approximately `+/-1.5%`, three times the intended first-order strain.

Planning grids require the explicit non-executable flag:

```bash
python tools/cdte_volume_grid.py \
  --allow-planning-candidate \
  --output-json runs/cdte_a0/planning-volume-grid.json
```

## Acceptance and stopping rules

Do not execute A0 until:

- an accepted CdTe bridge closes or tightly bounds the `90-293 K` integral;
- the final `0 K` derivation has a machine-readable manifest and propagated uncertainty;
- `cdte_a0_run_spec.json` contains the validated execution source chain;
- the generated grid reproduces `V/V_ref = (a/a_ref)^3` within tolerance;
- all electron-phonon temperatures use the identical `V_ref`.

Stop before introducing a temperature-dependent volume path, equation-of-state
fit, quasiharmonic correction, or borrowed expansion data from another material.

## What this protocol establishes

- the absolute approximately room-temperature CdTe anchor is primary and hashed;
- the low-temperature CdTe expansion is primary and hashed;
- the earlier Collins 1980 CdTe attribution is invalid;
- the `90-293 K` integral is the remaining physical-volume blocker.

## What this protocol does not establish

- no validated `0 K` execution lattice has been selected;
- no DFT equilibrium volume or equation of state has been calculated;
- no A0 static, phonon, dielectric, or electron-phonon run is authorized;
- no gap or Kane-parameter claim changes.
