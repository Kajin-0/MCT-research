# Scott 1969 fixed-alpha temperature coefficients

## Scope

Scott 1969 Figure 2 provides 70 direct experimental marker centers from nine HgCdTe specimens. Each marker is the photon energy satisfying

```text
alpha = 500 cm^-1
```

at the plotted temperature. The observation is therefore

```text
fixed_absorption_optical_edge_alpha_500_cm_inverse
```

and not a model-independent intrinsic signed bandgap.

This analysis asks only whether the composition dependence of the within-specimen temperature slope is resolved well enough to distinguish the Hansen temperature term from a free linear composition trend.

## Specimen-centered observation model

For specimen `i` and marker `j`, define

```text
t_ij = T_ij - mean_j(T_ij)
e_ij = E_ij - mean_j(E_ij)
```

so every specimen has an unconstrained intercept removed analytically. The centered model is

```text
e_ij = b_i t_ij + r_ij.
```

Three slope structures are compared.

### S0: independent specimen slopes

```text
b_i free for every specimen.
```

For each specimen,

```text
b_i = sum_j(t_ij e_ij) / sum_j(t_ij^2).
```

S0 is an in-sample linearity reference. It has no held-out specimen prediction.

### S1: shared linear composition trend

```text
b_i = b0 + b1 x_i.
```

The centered design has rows

```text
[t_ij, x_i t_ij]
```

and the deterministic central-coordinate estimate is

```text
[b0, b1]^T = (X^T X)^-1 X^T e.
```

No likelihood is asserted because pointwise experimental covariance was not reported.

### SH: Hansen-fixed temperature trend

Hansen's temperature coefficient is

```text
b_H(x) = 5.35e-4 (1 - 2x) eV/K
```

or

```text
b0,H = 5.35e-4 eV/K
b1,H = -1.07e-3 eV/K per unit x.
```

Only this coefficient is tested. Hansen's absolute composition polynomial does not enter the calculation.

## First-order coordinate and composition box

Every marker has bounded digitization half-widths

```text
delta_T = 1.75 K
delta_E = 0.0047 eV.
```

Scott's stated density-composition precision is retained as

```text
delta_x = 0.005.
```

These are deterministic sensitivity bounds, not Gaussian standard deviations.

For a model with composition slope `b1`, the conservative first-order residual envelope is

```text
B_ij = delta_E
     + |b_i| delta_T
     + |b1| delta_x |t_ij|.
```

For S0, the composition term is omitted. The normalized box residual is

```text
u_ij = |r_ij| / B_ij.
```

`u_ij <= 1` means that the fitted line intersects the declared first-order coordinate/composition box for that marker. It is not a confidence statement.

Reported deterministic diagnostics are

```text
maximum u
fraction with u <= 1
sum(max(0, u - 1)^2)
central-coordinate RMSE
specimen-level maximum u.
```

## Leave-one-specimen-out prediction

For S1, one specimen is removed, `b0` and `b1` are fitted to the remaining specimens, and the resulting slope is applied at the held-out composition. Only the held-out intercept is fitted.

For SH, the slope is fixed externally and only the held-out intercept is fitted.

S0 has no admissible held-out slope prediction because its slope is specimen-specific.

## Linearized box sensitivity of S1 coefficients

The sensitivity calculation perturbs each independent bounded input symmetrically:

- every marker energy by its `+/-0.0047 eV` half-width;
- every marker temperature by its `+/-1.75 K` half-width;
- every specimen composition by `+/-0.005`.

For each perturbation coordinate `q_k`, the symmetric secant contribution to the coefficient half-width is

```text
Delta beta_k = 0.5 |beta(q_k + delta_k) - beta(q_k - delta_k)|.
```

The reported componentwise box half-width is the sum of absolute contributions:

```text
Delta beta_box = sum_k Delta beta_k.
```

This is labeled `linearized_box_sensitivity`. It is not a confidence interval, posterior interval, or covariance estimate.

## Central results

### Full nine-specimen central fit

The shared linear trend is

```text
b0 = 5.49783543e-4 eV/K
b1 = -1.076209537e-3 eV/K per unit x.
```

This is numerically close to Hansen:

```text
b0,H = 5.35e-4 eV/K
b1,H = -1.07e-3 eV/K per unit x.
```

The numerical proximity does not establish compatibility because the full S1 and SH residual boxes both fail:

```text
full S1 maximum u = 1.483597188054
full SH maximum u = 1.820916077360.
```

The full leave-one-specimen-out maximum values are

```text
S1 = 2.305028838147
SH = 1.820916077360.
```

### Controlling unflagged within-range core

The controlling subset is

```text
x = {0.23, 0.31, 0.35, 0.405, 0.46}
41 markers
5 specimens.
```

The S1 central fit is

```text
b0 = 6.03872734e-4 eV/K
b1 = -1.235286852e-3 eV/K per unit x.
```

Its deterministic diagnostics are

```text
RMSE                       2.505852041 meV
maximum u                  1.418088512811
fraction within box        0.951219512195
box feasible               false.
```

The Hansen-fixed diagnostics are

```text
RMSE                       2.942101293 meV
maximum u                  1.820916077360
fraction within box        0.951219512195
box feasible               false.
```

The held-out core tests also fail complete box feasibility:

```text
S1 maximum held-out u      1.628014211258
SH maximum held-out u      1.820916077360.
```

The failures are concentrated at the low- and high-composition ends of the core rather than resolved by a single shared linear trend.

## Coefficient sensitivity result

For the controlling core, the S1 coefficient center and componentwise sensitivity envelope are

```text
b0 center =  6.03872734e-4 eV/K
b0 range  = [3.91485115e-4, 8.16260353e-4] eV/K

b1 center = -1.235286852e-3 eV/K per x
b1 range  = [-1.809474839e-3, -6.61098865e-4] eV/K per x.
```

The Hansen coefficient pair lies inside this nonprobabilistic componentwise envelope.

The dominant sensitivity is marker-energy extraction:

```text
core b0 half-width contribution
marker energy          1.75221024e-4 eV/K
marker temperature     1.2863579e-5 eV/K
specimen composition   2.4303017e-5 eV/K

core b1 half-width contribution
marker energy          4.76811592e-4 eV/K per x
marker temperature     3.1332984e-5 eV/K per x
specimen composition   6.6043412e-5 eV/K per x.
```

Thus publication-marker energy resolution, rather than composition precision, is the controlling limitation in this test.

## Decision

The predeclared controlling decision is

```text
non_identifiable_at_figure_precision.
```

The result is not `Hansen-compatible` because SH fails the core and held-out box-feasibility gates.

The result is not `observable-specific correction required` because S1 also fails those gates and Hansen remains inside the S1 linearized sensitivity envelope.

The correct interpretation is:

> The full Scott fixed-alpha temperature trend is numerically close to Hansen, but the source figure does not resolve whether that agreement is physical, observation-operator dependent, or accidental at the declared extraction precision.

## Claim boundary

Supported:

- the nine specimen-centered central slopes;
- deterministic S0, S1, and SH residual diagnostics;
- leave-one-specimen-out S1 and SH prediction;
- the declared first-order box and coefficient-sensitivity calculations;
- non-identifiability at the precision of the reconstructed Figure 2 marker centers.

Not supported:

- validation or rejection of Hansen's absolute `E_g(x,T)` polynomial;
- identification of Scott's fixed-alpha edge with intrinsic signed `E_g`;
- a new universal temperature coefficient;
- Gaussian pointwise uncertainty or coefficient covariance;
- pooling Scott with excitonic, magneto-optical, or detector-cutoff observations;
- a production equation or manuscript claim.
