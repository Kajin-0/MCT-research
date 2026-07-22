# CdTe A0 polar-response diagnosis source ledger

## Repository evidence

### Stricter-response numerical record

```text
first_principles/a0/cdte_a0_stricter_response_reference_result.json
```

Evidence identity:

```text
workflow run     29642078177
artifact         8429313337
artifact digest  sha256:9d179462706990c94376cff2499a42bb89af27d297afe1f514e8da9ff171c227
```

### SCF input

```text
first_principles/a0/templates/cdte_qe_scf_stricter_response.in.template
```

Relevant settings:

```text
occupations = fixed
noncolin    = true
lspinorb    = true
input_dft   = PBE
k grid      = 4 x 4 x 4, unshifted
```

### PH input

```text
first_principles/a0/templates/cdte_qe_ph_gamma_stricter_response.in.template
```

Relevant settings:

```text
q       = Gamma
trans   = true
epsil   = true
ldisp   = false
```

### Pseudopotential record

```text
first_principles/a0/cdte_pseudopotential_selection.json
```

Both selected pseudopotentials are PseudoDojo ONCVPSP PBE, norm-conserving, fully relativistic, spin-orbit enabled, and include nonlinear core correction.

## Official Quantum ESPRESSO documentation

### `ph.x` input definitions

```text
https://www.quantum-espresso.org/Doc/INPUT_PH.html
```

Controlling definitions:

- `epsil=true` at `q=0` computes the macroscopic dielectric constant for a nonmetal;
- `trans=true` and `epsil=true` compute effective charges;
- `zeu`, defaulting to `epsil`, computes effective charges from dielectric response;
- `zue=true` computes effective charges from phonon density responses;
- the `zeu` and `zue` results should agree within numerical noise.

### Single-q phonon guide

```text
https://www.quantum-espresso.org/Doc/ph_user_guide/node8.html
```

Controlling definitions:

- the raw Gamma dynamical matrix does not include the nonanalytic polar term;
- `epsil=true` computes the dielectric/effective-charge information required for LO--TO treatment;
- no acoustic sum rule is applied by `ph.x` automatically;
- `dynmat.x` applies selected ASR forms and LO--TO post-processing.

### `q2r.x` charge-ASR definition

```text
https://www.quantum-espresso.org/Doc/INPUT_Q2R.html
```

The `zasr` option can impose an acoustic sum rule on Born charges during post-processing. The present diagnosis treats this only as post-processing after convergence, not as evidence that a raw order-unity neutrality violation is acceptable.

## Identity used in the diagnosis

For a neutral insulating primitive cell, translational invariance requires

```text
sum_kappa Z*_(kappa,alpha,beta) = 0
```

for each Cartesian tensor component, up to numerical error.

The diagnosis does not assign the observed failure to one mechanism merely from this identity. It uses the strong response to numerical controls and the absence of a `zeu`/`zue` comparison to define the minimum discriminating test.

## Claim boundary

This source ledger supports code-behavior and diagnostic-method statements. It does not establish converged CdTe dielectric constants, Born charges, phonons, equilibrium pressure, or electron--phonon corrections.