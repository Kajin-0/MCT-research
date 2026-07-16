# CdTe A0 lattice and fixed-volume protocol

## Status

This protocol resolves the definition of the volume variable but does **not**
select an execution lattice constant. The A0 readiness gate remains closed until
an absolute bulk CdTe lattice measurement and its uncertainty are acquired from
a primary source and hashed.

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

1. an absolute bulk lattice parameter `a(T_anchor)` from calibrated diffraction;
2. the measurement temperature and standard uncertainty;
3. sample form, stoichiometry and observable definition;
4. a SHA-256 of the acquired primary source;
5. if `T_anchor != 0 K`, a primary measured linear-expansion function
   `alpha_L(T)` and an auditable integration/uncertainty manifest.

For cubic CdTe,

```text
a(T) = a(T_anchor) exp[integral(T_anchor -> T) alpha_L(T') dT']
```

The repository has identified the following primary thermal-expansion citation:

```text
G. K. White, J. G. Collins, J. A. Birch, and T. F. Smith,
J. Phys. C 13, 1649 (1980).
```

P. Pfeffer and W. Zawadzki cite this paper specifically as measured CdTe
`alpha_th(T)` data in their dilatational-gap construction
(`doi:10.1063/1.3703584`). The White et al. article has not yet been acquired and
hashed in this repository, and an acceptable primary absolute lattice anchor is
still unresolved. Therefore neither source is promoted to an execution input.

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

- the absolute lattice source is primary, acquired and hashed;
- its measurement temperature, observable and uncertainty are recorded;
- any extrapolation to `0 K` has a separate primary thermal-expansion source and
  uncertainty propagation;
- the generated grid reproduces `V/V_ref = (a/a_ref)^3` within numerical
  tolerance;
- all electron-phonon temperatures use the identical `V_ref`.

Stop and write a new decision memo before introducing a temperature-dependent
volume path, equation-of-state fit or quasiharmonic correction.

## What this protocol does not establish

- no primary absolute CdTe lattice value has been verified;
- no DFT equilibrium volume has been calculated;
- no equation of state or deformation potential has been fitted;
- no static, phonon, dielectric or electron-phonon calculation has been run;
- no gap or Kane-parameter claim changes.
