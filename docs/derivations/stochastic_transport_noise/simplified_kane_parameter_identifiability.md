# Simplified-Kane parameter identifiability and evidence design

**Program:** R06  
**Controlling issue:** #346  
**Model:** `project_defined_isotropic_simplified_kane`  
**Status:** structural design only; no accepted HgCdTe material parameters

## 1. Purpose

The merged simplified-Kane closure contains two explicit positive inputs:

- the parabolic density scale `N_*`;
- the nonparabolicity `alpha`.

The present gate asks which observables can distinguish these inputs and what
external evidence would be required before either is treated as an HgCdTe
material quantity.

A full-rank synthetic sensitivity matrix is not material validation.

## 2. Closure quantities

For

```text
E (1 + alpha E) = hbar^2 k^2 / (2 m*)
```

write

```text
beta = alpha k_B T.
```

The merged closure evaluates two normalized integrals from the same quadrature:

```text
I_n(eta, beta)
I_chi(eta, beta) = partial I_n / partial eta.
```

The physical outputs are

```text
n = N_* I_n,
chi_mu = (N_*/k_B T) I_chi,
Theta = I_n / I_chi.
```

Here `chi_mu = partial n / partial mu` is positive chemical compressibility.

## 3. Exact scale separation

The logarithmic sensitivities to `N_*` are exact:

```text
partial log(n) / partial log(N_*) = 1,
partial log(chi_mu) / partial log(N_*) = 1,
partial log(Theta) / partial log(N_*) = 0.
```

Therefore:

- density and compressibility carry the absolute scale;
- the generalized Einstein factor is scale-free;
- repeated measurements of one absolute observable at one identical condition
  cannot separate `N_*` from `alpha`;
- density plus `Theta`, or matched density plus compressibility, can be locally
  full rank when the alpha sensitivity is nonzero.

## 4. Nonparabolicity sensitivities

Because `beta = alpha k_B T`,

```text
partial log(n) / partial log(alpha)
  = (beta/I_n) partial I_n/partial beta,

partial log(chi_mu) / partial log(alpha)
  = (beta/I_chi) partial I_chi/partial beta,

partial log(Theta) / partial log(alpha)
  = partial log(I_n/I_chi) / partial log(alpha).
```

The implementation evaluates these derivatives by centered multiplicative
perturbations in `alpha`.  The parameter coordinates are

```text
log(N_*), log(alpha).
```

Positive parameters and positive observables are therefore required.

## 5. Weighted design matrix

For observation `i` with positive prediction `y_i` and relative standard
uncertainty `s_i`, the row is

```text
J_i = (1/s_i) [
  partial log(y_i)/partial log(N_*),
  partial log(y_i)/partial log(alpha)
].
```

The design report records:

- the weighted sensitivity matrix `J`;
- singular values;
- rank;
- condition number when rank is two;
- Fisher matrix `J^T J`;
- observation kinds and temperature coverage.

Rank two is necessary but not sufficient.  Poor conditioning, model
misspecification, unknown reduced chemical potential, or non-independent data
can still invalidate inference.

## 6. Chemical-potential basis

The closure takes reduced chemical potential `eta` as an input.  A material
reference point is not directly usable unless either:

1. `eta` is independently known; or
2. a separately validated neutrality model supplies `eta`.

Intrinsic carrier concentration alone does not close this requirement unless
heavy-hole, split-off-band, and charge-neutrality accounting are independently
specified and validated.

## 7. Minimum external-evidence policy

The machine-readable gate requires at least:

1. three positive uncertainty-bearing HgCdTe evidence points;
2. two provenance groups;
3. two temperatures;
4. one absolute scale observable:
   - density, or
   - chemical compressibility;
5. one shape observable:
   - generalized Einstein factor, or
   - matched density and compressibility at one condition;
6. primary or independently generated status for every point;
7. known `eta` or a validated neutrality model for every point.

These are minimum metadata requirements.  Passing them does not automatically
establish model adequacy.

## 8. Temperature and composition domain

The current executable closure accepts `N_*` and `alpha` directly.  It does not
define `N_*(x,T)` or `alpha(x,T)`.

A multi-temperature sensitivity calculation therefore tests a declared
parameterization, not a universal constant-parameter material law.  Before
material acceptance, the project must specify whether:

- parameters are local values at each `(x,T)` state;
- a source-grounded functional form is used; or
- a full three-band secular relation replaces the simplified parameterization.

At least two temperatures are required so that inadequacy cannot be hidden by a
single-state fit.

## 9. Simplified-versus-three-band decision

After parameter identification, the simplified dispersion is accepted only if
hold-out residuals are statistically consistent across the declared domain and
do not show systematic composition or temperature structure.

A full three-band model becomes mandatory when any of the following occurs:

- one `alpha` parameter cannot represent the accepted references;
- heavy-hole or split-off-band terms are required to close neutrality;
- compressibility is inconsistent with density-derived parameters;
- residuals show systematic `x` or `T` dependence beyond uncertainty;
- the restricted-domain error exceeds the declared acceptance tolerance.

## 10. Current decision

The identifiability design is authorized as numerical architecture.

No HgCdTe parameter value, equilibrium density, chemical compressibility,
screening length, or detector prediction is authorized by this gate because the
accepted material-evidence list is empty.
