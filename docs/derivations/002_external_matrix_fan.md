# Derivation 002 — Covariant external matrix lower-Fan contraction

**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #296  
**Status:** analytical definition and synthetic oracle; no backend or material validation  
**Claim level:** established perturbation structure implemented under explicit gauge and normalization contracts

## 1. Scope

The purpose of this derivation is to define the complete lower-Fan self-energy matrix that was absent from the standard QE 7.6 / EPW 6.1 accumulation path identified in issue #289.

The matrix is computed from normalized complex electron--phonon vertices supplied by a future adapter. This derivation does not specify how a backend must generate those vertices and does not authorize a material calculation.

The long-range polar contribution and thermal expansion are excluded.

## 2. Spaces and vertex convention

At external crystal momentum `k`, select an `N`-dimensional low-energy subspace with basis states

```text
|a,k>, a = 1,...,N.
```

For one phonon wavevector and branch `(q,nu)`, select `M` intermediate electronic states

```text
|m,k+q>, m = 1,...,M.
```

Define the complex vertex matrix

```text
G_(q,nu)[m,a] = <m,k+q | Delta V_(q,nu) | a,k>.
```

The implementation contract requires `G` to have energy units and to include the complete phonon zero-point displacement normalization. The q-point weight is supplied separately. Spinor states are explicit, so no hidden spin-degeneracy factor is allowed.

## 3. Retarded denominator

At real evaluation energy `E` and positive broadening `eta`, set

```text
z = E + i eta, eta > 0.
```

For intermediate energy `epsilon_m`, occupation `f_m`, phonon energy `omega_qnu`, and Bose occupation `n_qnu`, define

```text
D_m^R(E)
  = (n_qnu + 1 - f_m) / (z - epsilon_m - omega_qnu)
  + (n_qnu + f_m)     / (z - epsilon_m + omega_qnu).
```

The two numerators are nonnegative for

```text
n_qnu >= 0,
0 <= f_m <= 1.
```

## 4. Complete matrix contraction

For one `(q,nu)` contribution,

```text
Sigma_(q,nu)^R(E) = w_q G_(q,nu)^dagger D_(q,nu)^R(E) G_(q,nu),
```

where `D` is the diagonal matrix formed from the factors above. The total lower-Fan matrix is

```text
Sigma_Fan^R(E) = sum_(q,nu) Sigma_(q,nu)^R(E).
```

A single common `E` is used for every external matrix element. Substituting a different on-shell energy for each basis vector inside this primary definition would destroy general external-subspace covariance.

## 5. Diagonal equivalence

The diagonal matrix element is

```text
Sigma_aa^R(E)
  = sum_(q,nu) w_q sum_m G_ma^* D_m^R(E) G_ma
  = sum_(q,nu) w_q sum_m |G_ma|^2 D_m^R(E).
```

This is exactly the conventional scalar lower-Fan expression under the same vertex normalization, q weights, occupations, phonon energies, broadening, and units.

Choosing

```text
E = epsilon_a
```

recovers the standard scalar on-shell result for external state `a`. This diagonal identity is the primary future backend benchmark.

## 6. External-basis covariance

Let the external basis rotate by unitary matrix `U`:

```text
|a'> = sum_a |a> U_(a,a').
```

The vertex transforms as

```text
G' = G U.
```

Therefore

```text
Sigma'^R
  = (G U)^dagger D (G U)
  = U^dagger G^dagger D G U
  = U^dagger Sigma^R U.
```

The common-frequency matrix is covariant under any unitary rotation of the selected external subspace.

## 7. Intermediate-gauge invariance and its boundary

Let the intermediate states rotate by unitary matrix `V`. With the convention

```text
G' = V^dagger G,
```

the transformed contraction is

```text
Sigma'^R = G^dagger V D V^dagger G.
```

It equals the original matrix only when

```text
[V,D] = 0.
```

This condition holds for rotations within an exactly degenerate intermediate block whose energies and occupations produce identical denominator factors. It does not hold for arbitrary rotations mixing unequal energies or occupations.

The implementation therefore checks the denominator commutator directly and rejects inadmissible intermediate rotations rather than claiming unrestricted gauge invariance.

## 8. Retarded causality

For a scalar denominator

```text
1 / (x + i eta), eta > 0,
```

the imaginary part is

```text
-eta / (x^2 + eta^2) <= 0.
```

Because both statistical numerators are nonnegative,

```text
-Im D_m^R(E) >= 0.
```

Define the linewidth matrix

```text
Gamma(E) = i [Sigma^R(E) - Sigma^R(E)^dagger].
```

Then

```text
Gamma(E)
  = sum_(q,nu) w_q G^dagger [-2 Im D^R(E)] G.
```

For nonnegative q weights, every diagonal factor in brackets is nonnegative. Hence

```text
x^dagger Gamma x
  = sum_(q,nu) w_q ||[-2 Im D]^(1/2) G x||^2
  >= 0
```

for every vector `x`. The linewidth matrix is Hermitian positive semidefinite. A negative or zero `eta` is rejected because it does not satisfy the declared retarded convention.

## 9. Energy derivative

Since

```text
d/dE [1/(E-a+i eta)] = -1/(E-a+i eta)^2,
```

the derivative factors are

```text
dD_m^R/dE
  = -(n+1-f_m)/(z-epsilon_m-omega)^2
    -(n+f_m)/(z-epsilon_m+omega)^2.
```

Therefore

```text
d Sigma^R/dE = sum_(q,nu) w_q G^dagger (dD^R/dE) G.
```

The synthetic oracle compares this expression with a centered finite difference. No production quasiparticle-weight matrix is constructed in the present gate.

## 10. Hermitian reductions

The raw retarded self-energy is generally non-Hermitian at real energy because it contains finite linewidths. It must not be mislabeled as a Hermitian Hamiltonian correction.

### 10.1 Common-energy Hermitian part

At one common energy,

```text
H_common(E) = [Sigma^R(E) + Sigma^R(E)^dagger] / 2.
```

This retains full external-subspace covariance.

### 10.2 Symmetrized on-shell form

In the eigenbasis of the unperturbed external Hamiltonian, define

```text
H_ab^OS
  = 1/2 [Sigma_ab^R(epsilon_a)
         + Sigma_ba^R(epsilon_b)^*].
```

This matrix is Hermitian and its diagonal satisfies

```text
H_aa^OS = Re Sigma_aa^R(epsilon_a).
```

Its covariance claim is narrower than that of the common-energy matrix. It is covariant only under rotations that commute with the unperturbed external Hamiltonian, including arbitrary rotations inside exactly degenerate blocks. Rotations mixing unequal unperturbed energies are rejected.

## 11. Long-range separation

The matrix kernel accepts only records with

```text
long_range_included = false
thermal_expansion_included = false.
```

A future backend adapter must remove or never include the analytic long-range vertex before supplying `G`. The generalized-Fröhlich correction remains a separately validated term added exactly once under the existing hybrid contract.

## 12. Synthetic validation targets

The implementation requires:

- exact scalar and multiband diagonal equivalence;
- external covariance at common frequency;
- invariance under admissible intermediate rotations;
- rejection of noncommuting intermediate rotations;
- Hermitian positive-semidefinite linewidth matrices;
- analytic derivative agreement with finite differences;
- Hermiticity and diagonal recovery of both declared reductions;
- degenerate-block covariance of the on-shell form;
- exact zero-coupling behavior;
- explicit normalization, provenance, and fail-closed authorization metadata.

## 13. Current claim boundary

A passing synthetic oracle establishes the algebra and the executable information contract. It does not establish:

- that QE, EPW, ABINIT, or another backend can export the required normalized vertices;
- that a finite band window is converged;
- that a CdTe, HgTe, or HgCdTe self-energy is correct;
- that the long-range polar correction is known;
- that a static Hermitian reduction is adequate near the normal/inverted transition;
- that a finite-temperature Kane parameter set has been validated.

A separate upstream raw-vertex fixture is required before any material design review.
