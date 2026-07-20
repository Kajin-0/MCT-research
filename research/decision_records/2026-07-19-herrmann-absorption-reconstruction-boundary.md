# Herrmann absorption reconstruction boundary

Date: 2026-07-19  
Controlling issue: #132

## Question

Can the Herrmann et al. 1993 tail-plus-band-filling model be added to the real-spectrum edge ensemble as a fully reproducible observation operator?

## Recovered primary source

Herrmann et al., *Journal of Applied Physics* **74** (1993), DOI `10.1063/1.352954`.

The recovered full text explicitly provides three mathematical primitives:

```text
alpha(E) = alpha(E0) exp[(E-E0)/W0]
W0(T) = E_permanent + a k_B T
BFF_equilibrium = tanh[(E-delta_mu)/(4 k_B T)]
```

The source uses `E_p` for permanent tail broadening. The implementation names this quantity `permanent_broadening_ev` so it cannot be confused with the Kane matrix-element energy that is also commonly written `E_P`.

## Missing full-operator information

The 1993 paper does not reproduce a self-contained complete Kane-region absorption expression with every convention required by its calculations. It also relies on prior work for the detailed band-filling and quasi-Fermi-level treatment.

The most direct unresolved precursor is:

```text
Broadening mechanisms near the E0 transition in narrow-gap Hg1-xCdxTe
Journal of Crystal Growth 117, 758-761 (1992)
DOI 10.1016/0022-0248(92)90851-9
```

That full text has not been recovered or audited.

The Urbach-to-Kane transition condition cannot independently determine an edge from the explicit tail equation. It requires the missing Kane branch and its parameter conventions. Combining the Herrmann tail with a different repository Kane law would create an undocumented hybrid operator.

## Implementation

The repository adds only:

- `herrmann_urbach_width_ev`;
- `herrmann_urbach_tail_alpha_cm1`, restricted to `E <= E0`;
- `herrmann_equilibrium_band_filling_factor`, exposed only as the reported limiting primitive.

The primitives are vectorized, unit-explicit, source-identified, and fail closed outside their declared domains.

## Decision

Authorized:

- reproduce the three explicit 1993 equations;
- use them for unit tests, source reconstruction, and future complete-operator assembly;
- state that Herrmann provides direct evidence that tail broadening and band filling alter near-edge spectra;
- request DOI `10.1016/0022-0248(92)90851-9` as the next source needed for reconstruction.

Not authorized:

- label the current implementation a full Herrmann absorption model;
- fit it to the Moazzami spectra as a complete edge candidate;
- update the existing `6.414-6.830 meV` edge envelope;
- infer an Urbach-to-Kane transition energy from the tail law alone;
- substitute a fractional-power, Chu, or other Kane-region expression and attribute the hybrid to Herrmann;
- fit new universal material-gap coefficients.

## Consequence

The literature search identified a scientifically relevant observation model, but the correct immediate result is a **reproducibility boundary**, not another numerical edge estimate. Recovering and auditing the 1992 precursor is the gate for the next implementation tranche.
