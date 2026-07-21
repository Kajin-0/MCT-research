# Decision: separate local, co-limited, and censored transition-uncertainty regimes

**Date:** 2026-07-21  
**Parent issue:** #167  
**Milestone issue:** #169  
**Decision status:** controlling after merge

## Decision

Use exact bounded-Gaussian composition quadrature, rather than only local derivative propagation, whenever a critical-temperature distribution is reported.

Every reported conditional critical-temperature mean or width must include the probability that exactly one transition occurs inside the declared temperature window.

## Basis

A Gaussian composition model conditioned on `0 <= x <= 1` was propagated through three existing signed-gap laws at mean composition `x=0.155` over `0-300 K`:

- reconstructed Laurenti;
- Hansen-Schmit-Casselman;
- archived provisional Hansen-Padé.

The three central critical temperatures are:

```text
Laurenti                         77.1241 K
Hansen                           52.0438 K
provisional Hansen-Padé          52.5937 K
cross-model span                 25.0803 K
```

No model prior was assigned and no universal law was selected.

## Regime I: local and latent-law limited

At `sigma_x=0.001`:

```text
model       exact sigma_Tc   local-width error   crossing probability
Laurenti      4.46435 K        +0.00221 K           1.000000
Hansen        4.55975 K        +0.00014 K           1.000000
Padé          3.80408 K        -0.00104 K           1.000000
```

The nonlinear correction is negligible. The 25.08 K latent-law span dominates the approximately 4 K composition-induced width.

**Decision:** further refinement of Taylor order is not the priority in this regime. Observation-class evidence capable of distinguishing the latent laws is the limiting need.

## Regime II: composition and latent law co-limit the result

At `sigma_x=0.005`:

```text
model       exact conditional sigma_Tc   no-transition/always-normal probability
Laurenti              22.2899 K                         0.003561
Hansen                21.8538 K                         0.013049
Padé                   18.3449 K                         0.013049
```

The composition-induced width becomes comparable to the central model span, and a small no-crossing probability appears.

**Decision:** report both latent-law spread and composition-distribution width. Neither may be collapsed into the other.

## Regime III: censored and nonlinear

At `sigma_x=0.010`:

```text
model       crossing probability   always-normal probability   mean shift   local-width error
Laurenti          0.913966                 0.086034              +5.5170 K      -6.6812 K
Hansen            0.858810                 0.141190             +11.0501 K      -9.6575 K
Padé              0.858810                 0.141190              +9.8254 K      -7.4308 K
```

The finite temperature window censors composition realizations that never cross. Conditional moments shift and differ materially from the local implicit-function Gaussian.

**Decision:** a notation such as `Tc(mean x) +/- |dTc/dx| sigma_x` is unauthorized in this regime unless accompanied by exact crossing probability and a demonstrated approximation-error bound.

## Consequences for the flagship program

1. The composition-distribution layer is now executable beyond local propagation.
2. Critical-temperature uncertainty is not always summarized by one symmetric error bar.
3. Latent-law uncertainty and composition-distribution uncertainty dominate in different regimes.
4. The observation window is part of the reported transition observable.
5. The next highest-value scientific step is an explicit spectral observation operator, beginning with the Herrmann Gaussian-gap convolution or the source-bounded Chang absorption operator.

## Claim boundaries

The screen does not establish:

- the actual composition distribution of any Teppe specimen;
- a measured phase-volume fraction;
- a bulk topological invariant;
- posterior probabilities for the three gap laws;
- selection of Laurenti, Hansen, or the archived provisional Padé law;
- equivalence between local signed-gap roots and fitted magneto-optical Kane masses.

## Reopening conditions

This decision may be revised if:

- a measured non-Gaussian composition distribution becomes available;
- spatial correlation or percolation changes the response materially;
- a magneto-optical forward operator maps the local gap distribution into a substantially different fitted-mass distribution;
- quadrature or root-grid convergence fails the declared numerical gates;
- new primary evidence changes the latent-law comparison at `x≈0.155`.
