# Current research program state

**Last updated:** 2026-07-18

## Static and finite-temperature methods

The finite-k workflow uses the isospectral selected-band polar Hamiltonian. The zincblende linear and quadratic spaces and the finite-temperature reconstruction oracles are tested. The present CdTe response calculation is not suitable for a production polar electron-phonon result.

## Provisional HgCdTe thermal model

`Eg(x,T) = Eg_Hansen(x,0) + alpha (1-2x) T^3/(T^2 + tau^2)`

with `alpha = 5.918273117836612e-4 eV/K` and `tau = 18.059294367159467 K` remains a constrained model for the Seiler specimen regime. It is not a universal or production equation.

## Primary near-critical benchmarks

Teppe 2016 contributes five primary magneto-optical gap points. Sample A uses nominal `x=0.175`; the lower-precision Methods summary `x=0.17` is retained only as a sensitivity case. At nominal composition, Laurenti gives `4.2005 meV` combined RMSE. No global ranking is supported without composition uncertainty.

Orlita 2014 contributes a carrier-coupled constraint at approximately `1.8 K`: a graded `x approximately 0.17` plateau of roughly `3.2 um`, a low-field model improved by `Eg=4 meV`, `EF approximately 15-17 meV`, and `n approximately (2-3)e14 cm^-3`.

At nominal `x=0.17`, Laurenti predicts `2.9560 meV` and is the closest comparator. This record is not an exact homogeneous composition-gap point and shares the Mikhailov/Dvoretskii MBE and magneto-optical lineage with Teppe.

## Evidence boundary

Further useful work consists of recovering primary datasets with explicit composition provenance, obtaining independent composition uncertainty, correcting covariance storage from redundant 128D coordinates to 64 independent Hermitian coordinates, and preparing paired experimental acquisition when a practical collaboration exists.

Additional empirical coefficients, source-specific composition remapping, global equation promotion, and production finite-temperature calculations from the current CdTe response state are outside the present evidence boundary.
