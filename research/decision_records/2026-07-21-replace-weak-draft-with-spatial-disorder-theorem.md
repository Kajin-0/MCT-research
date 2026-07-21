# Decision record: replace the weak flagship draft with a scale-dependent disorder theorem

**Date:** 2026-07-21  
**Issue:** #196  
**Status:** active and controlling

## Decision

The merged PR #194 manuscript and submission package are superseded and are not publication-ready.

All future manuscript work is anonymous only. Named manuscript files, cover letters, personal metadata, journal packaging, and the superseded dashboard figures are removed from the active branch.

The scientific program is reset around one equation-dense result hierarchy:

1. the exact covariance-filter operator for a finite measurement kernel;
2. the Gaussian-covariance/Gaussian-probe closed form;
3. an exact one-scale non-identifiability theorem;
4. an exact two-scale inverse;
5. a conditioning theorem for experimental scale selection;
6. propagation through a signed HgCdTe gap law;
7. device-relevant consequences for apparent gap and cutoff spread.

## Why the prior draft is insufficient

The previous draft contains valid component calculations, but it presents them as a collection of sensitivities:

- critical-temperature broadening;
- absorption-tail fit-window dependence;
- detector-cutoff thickness dependence;
- carrier-filling sensitivity;
- structural-rank examples;
- source-table consistency.

That structure does not create one result strong enough to carry a theoretical journal paper. The figures function as summary dashboards rather than evidence for a central theorem. Packaging the draft would increase apparent completion without increasing scientific value.

## Selected replacement result

For a stationary composition field and normalized kernel,

```text
Var(X_a) = int int w_a(r) w_a(r') C_x(r-r') dr dr'.
```

For Gaussian covariance and a `D`-dimensional Gaussian probe,

```text
Var(X_a) = sigma_x^2 (1 + 2 a^2/ell^2)^(-D/2).
```

A single scale identifies only the displayed combination. Two distinct scales permit the exact inverse

```text
q = (V1/V2)^(2/D)
ell^2 = 2 (a2^2 - q a1^2)/(q - 1)
sigma_x^2 = V1 (1 + 2 a1^2/ell^2)^(D/2).
```

The inversion is useful only when probe scales carry sufficiently different logarithmic sensitivities to `ell`.

## First significance screen

For the declared two-dimensional case

```text
sigma_x = 0.005
ell = 5 um
|dEg/dx| = 1.7191085 eV
```

changing Gaussian probe scale from `1 um` to `100 um` changes the linearized apparent gap standard deviation from `8.271 meV` to `0.304 meV`, a factor of `27.23`.

Around a `10 um` cutoff, the corresponding first-order cutoff spread changes from approximately `0.667 um` to `0.0245 um`.

This magnitude is sufficient to justify deeper work because it can change interpretation across micro-FTIR, wafer FTIR, PL, cutoff maps, and device/pixel distributions. It remains a sensitivity case, not a fitted specimen result.

## Claim restrictions

- The general random-field convolution is established mathematics.
- The Gaussian integral is not claimed as new probability theory.
- No source is said to have measured `ell` unless it reports a spatial covariance or equivalent multi-scale evidence.
- Herrmann tail energy is not equated with microscopic composition variance.
- PL linewidth is not equated with probe-averaged gap variance.
- Detector cutoff spread is not equated with gap variance without a declared optical/device operator.
- Two-scale identifiability is conditional on the covariance family, kernel, dimension, and nuisance-parameter controls.
- No journal submission is authorized until prior-art, uncertainty, and manuscript-strength gates pass.

## Required evidence before a new anonymous PDF

1. complete CI verification of exact formulas and independent quadrature;
2. full-text audit of the most relevant spatial mapping papers;
3. uncertainty propagation through the two-scale inverse;
4. covariance-family misspecification analysis;
5. at least one HgCdTe-relevant measurement design with plausible scales and errors;
6. a focused manuscript with derivations and figures organized around the theorem rather than a list of earlier milestones.
