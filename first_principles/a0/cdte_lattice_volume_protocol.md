# CdTe A0 lattice and fixed-volume protocol

## Status

This protocol resolves the definition of the volume variable but does **not**
select an execution lattice constant. The A0 readiness gate remains closed until
an absolute bulk CdTe lattice measurement and a complete CdTe thermal-expansion
source chain are acquired from primary sources, hashed, and uncertainty-audited.

The common `6.482 Angstrom` value remains a planning candidate only.

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

A0 authorizes only the fixed-volume static/phonon sanity work. It does not
authorize a production quasiharmonic path.

## Reference-volume definition

The preferred physical reference is the cubic zincblende lattice at `0 K`, or a
traceable extrapolation to `0 K` from primary measurements. This aligns the
fixed-volume finite-temperature correction and zero-point reference without
embedding thermal expansion in the electron-phonon term.

An acceptable source chain requires:

1. an absolute bulk lattice parameter `a(T_anchor)` from calibrated CdTe diffraction;
2. the measurement temperature and standard uncertainty;
3. sample form, stoichiometry, and observable definition;
4. a SHA-256 of every acquired primary source;
5. if `T_anchor != 0 K`, primary measured CdTe linear-expansion data spanning the
   integration interval, or a separately approved uncertainty-bounded interval model;
6. an auditable integration and uncertainty manifest.

For cubic CdTe,

```text
a(T) = a(T_anchor) exp[integral(T_anchor -> T) alpha_L(T') dT']
```

## Primary source candidates

### Absolute anchor and expansion above room temperature

```text
M. G. Williams, R. D. Tomlinson, and M. J. Hampshire,
X-ray determination of the lattice parameters and thermal expansion of
cadmium telluride in the temperature range 20-420 C,
Solid State Communications 7, 1831-1832 (1969),
DOI 10.1016/0038-1098(69)90296-8.
```

The primary abstract confirms direct X-ray powder-camera measurements of cubic
CdTe lattice parameters and thermal expansion over 20-420 C and gives

```text
alpha_L(T_C) = 4.932e-6 + 1.165e-9 T_C + 1.428e-12 T_C^2.
```

The article bytes have not been acquired and hashed. The abstract alone does
not establish the execution lattice value, standard uncertainty, sample state,
or exact primary location of the anchor.

### Low-temperature CdTe expansion

```text
T. F. Smith and G. K. White,
The low-temperature thermal expansion and Gruneisen parameters of some
tetrahedrally bonded solids,
J. Phys. C: Solid State Phys. 8, 2031-2042 (1975),
DOI 10.1088/0022-3719/8/13/012.
```

The primary record states that CdTe was measured with a three-terminal
capacitance dilatometer below 30 K and between 57 and 90 K. The article bytes,
actual data representation, calibration, sample details, and uncertainties have
not yet been acquired and hashed.

### Excluded citation

```text
J. G. Collins, G. K. White, J. A. Birch, and T. F. Smith,
J. Phys. C 13, 1649-1656 (1980),
DOI 10.1088/0022-3719/13/9/011.
```

This article is titled `Thermal expansion of ZnTe and HgTe and heat capacity of
HgTe at low temperatures`. It does not report CdTe and must not appear in the
CdTe execution transformation.

## Uncovered temperature interval

The current CdTe-specific candidates do not yet supply one accepted continuous
path from `0 K` to the approximately room-temperature absolute anchor. Smith and
White cover CdTe below 30 K and 57-90 K; Williams begins near 293 K.

The approximately 90-293 K interval requires either:

1. an acquired primary CdTe expansion source; or
2. a separate fail-closed decision memo defining the interpolation/model,
   physical basis, source discrepancy, and propagated uncertainty.

Do not substitute ZnTe or HgTe expansion and do not silently interpolate the gap.

## Volume-sensitivity points

The A0 sensitivity bracket is defined in **volume**, not in lattice constant:

```text
Delta V / V_ref = -0.005, 0, +0.005
```

For a cubic cell,

```text
a / a_ref = (V / V_ref)^(1/3)
```

Therefore the exact lattice scale factors are:

| Delta V / V_ref | a / a_ref | Delta a / a_ref |
|---:|---:|---:|
| -0.005 | 0.9983305478136913 | -0.0016694521863087 |
| 0 | 1 | 0 |
| +0.005 | 1.001663896579312 | +0.001663896579312 |

Applying `+/-0.5%` directly to the lattice constant would instead change the
volume by approximately `+/-1.5%`, three times the intended first-order strain.

Use:

```bash
python tools/cdte_volume_grid.py \
  --allow-planning-candidate \
  --output-json runs/cdte_a0/planning-volume-grid.json
```

The explicit flag produces a visibly non-executable planning grid. Without that
flag the tool refuses to use the candidate value while the primary execution
anchor is unresolved.

## Acceptance and stopping rules

Do not execute A0 until:

- the absolute lattice source is primary, acquired, and hashed;
- its measurement temperature, observable, sample state, and uncertainty are recorded;
- the complete `0 K` to anchor expansion chain is CdTe-specific and source-covered;
- any source gap has a separately reviewed uncertainty-bounded decision memo;
- the generated grid reproduces `V/V_ref = (a/a_ref)^3` within numerical tolerance;
- all electron-phonon temperatures use the identical `V_ref`.

Stop and write a new decision memo before introducing a temperature-dependent
volume path, equation-of-state fit, quasiharmonic correction, or borrowed
expansion data from a different material.

## What this protocol does not establish

- no primary absolute CdTe lattice value has been verified;
- no complete CdTe thermal-expansion chain has been acquired;
- no DFT equilibrium volume has been calculated;
- no equation of state or deformation potential has been fitted;
- no A0 static, phonon, dielectric, or electron-phonon calculation has been run;
- no gap or Kane-parameter claim changes.
