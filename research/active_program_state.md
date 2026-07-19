# Current research program state

**Last updated:** 2026-07-19

## Static and finite-temperature methods

The finite-k workflow uses the isospectral selected-band polar Hamiltonian. The zincblende linear and quadratic spaces and the finite-temperature reconstruction oracles are tested. The present CdTe response calculation is not suitable for a production polar electron-phonon result.

Hermitian Hamiltonian covariance uses 64 independent coordinates; genuinely non-Hermitian dynamical operators retain 128. Deterministic static coefficients remain valid, but redundant Hamiltonian degrees of freedom and variance-scaled standard errors are superseded.

## Provisional HgCdTe thermal model

`Eg(x,T) = Eg_Hansen(x,0) + alpha (1-2x) T^3/(T^2 + tau^2)`

with `alpha = 5.918273117836612e-4 eV/K` and `tau = 18.059294367159467 K` remains a constrained model for the Seiler specimen regime. It is not a universal or production equation.

## Near-critical primary evidence

Teppe 2016 contributes five primary magneto-optical gap points. Sample A uses nominal `x=0.175`; the lower-precision Methods summary `x=0.17` is retained only as a sensitivity case. At nominal composition, Laurenti gives `4.2005 meV` combined RMSE. No global ranking is supported without composition uncertainty.

Orlita 2014 contributes a carrier-coupled primary constraint at approximately `1.8 K`: a graded `x approximately 0.17` plateau of roughly `3.2 um`, a low-field model improved by `Eg=4 meV`, `EF approximately 15-17 meV`, and `n approximately (2-3)e14 cm^-3`.

At nominal `x=0.17`, Laurenti predicts `2.9560 meV` and is the closest local comparator. Equivalent compositions required by the screened models span `0.163392-0.170573`, so local ranking is dominated by unrecovered homogeneous composition uncertainty.

The Orlita and Teppe records share the Mikhailov/Dvoretskii MBE and magneto-optical lineage. They are not independent cross-laboratory validation. Orlita is conditional evidence, not an exact homogeneous point.

## Absorption observation contract

Absorption-derived records preserve calibrated raw spectra, complete measurement metadata, every declared model and threshold candidate, exclusions, and separate/combined sensitivity envelopes. The exporter never selects a corrected material gap.

The candidate ensemble contains fractional-power fits, fixed thresholds, and an optional Chu 1994 Kane-region model with a fail-closed source range of `0.170 <= x <= 0.443` and `77 <= T <= 300 K`.

## Manuscript program

Breadth-first development is frozen. The immediate research product is:

> **Observation-model uncertainty and identifiability in HgCdTe bandgap extraction.**

The manuscript must apply the existing contract to `2-4` real calibrated primary spectra, preserve complete specimen metadata, and show whether the model/threshold ensemble changes a real material-model ranking or conclusion.

The static CdTe selected-band result remains the parallel higher-value computational target, but only one independently converged reproduction is authorized. Full AHC, alloy calculations, additional empirical coefficients, and new source-specific screens are deferred.

## Evidence boundary

The central source ledger contains zero authorized primary fit sources, two conditional primary sources, six blocked primary sources, and one secondary screen.

New work must close a manuscript-critical evidence gap. Additional source accumulation, synthetic oracles, or ledger-only changes are not authorized unless they change a controlling scientific decision.
