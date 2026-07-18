# Current research program state

**Last updated:** 2026-07-18

## Static and finite-temperature methods

The finite-k workflow uses the isospectral selected-band polar Hamiltonian. The zincblende linear and quadratic spaces and the finite-temperature reconstruction oracles are tested. The present CdTe response calculation is not suitable for a production polar electron-phonon result.

## Provisional HgCdTe thermal model

`Eg(x,T) = Eg_Hansen(x,0) + alpha (1-2x) T^3/(T^2 + tau^2)`

with `alpha = 5.918273117836612e-4 eV/K` and `tau = 18.059294367159467 K` remains a constrained model for the Seiler specimen regime. It is not a universal or production equation.

## Teppe benchmark precision

Five primary magneto-optical gap points from DOI `10.1038/ncomms12576` are included.

Sample A is repeatedly labeled `x=0.175` in the analysis and figures. Methods gives the lower-precision summary `x=0.17`. The benchmark uses `x=0.175` as nominal and treats `x=0.17` only as a sensitivity value.

At nominal `x=0.175`, Laurenti gives `4.2005 meV` combined RMSE. At sensitivity value `x=0.17`, provisional Hansen-Pade gives `5.0665 meV` combined RMSE. This is composition sensitivity, not evidence for two exact composition measurements.

No global equation ranking is supported without sample-level composition uncertainty.

## Evidence boundary

Further useful work consists of recovering primary datasets with explicit composition provenance, obtaining composition uncertainty for the Teppe specimens, correcting covariance storage from redundant 128D coordinates to 64 independent Hermitian coordinates, and preparing paired experimental acquisition when a practical collaboration exists.

Additional empirical coefficients, source-specific composition remapping, and production finite-temperature calculations from the current CdTe response state are outside the present evidence boundary.
