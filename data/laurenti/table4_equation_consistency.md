# Laurenti Table IV consistency with Eq. (7)

## Purpose

Check the primary-table transcription against the published analytical expression without treating either as experimental validation.

For each of the 24 compositions and six temperatures in Table IV, define

$$
r_{x,T}
=
1000\left[E_g^{\mathrm{table}}(x,T)-E_g^{\mathrm{Eq.7}}(x,T)\right]
\quad\mathrm{meV}.
$$

There are 144 tabulated values.

## Result

Including every printed entry:

- mean absolute difference: `0.296 meV`;
- root-mean-square difference: `0.592 meV`;
- maximum absolute difference: `6.201 meV`.

The maximum is the flagged boundary value

$$
x=0.165,\qquad T=0\ \mathrm K,
$$

where the transcribed table gives `0.000 eV` but Eq. (7) gives

$$
-0.0062013\ \mathrm{eV}.
$$

Excluding that one entry:

- mean absolute difference: `0.254 meV`;
- root-mean-square difference: `0.290 meV`;
- maximum absolute difference: `0.513 meV`.

The remaining maximum occurs at

$$
x=0.950,\qquad T=400\ \mathrm K,
$$

where the table gives `1.402 eV` and Eq. (7) gives `1.401487 eV`.

Excluding both flagged entries, the maximum absolute difference is `0.500 meV`, exactly the expected half-unit scale for a table rounded to 0.001 eV.

## Interpretation

1. The Table IV transcription is consistent with Eq. (7) at its printed precision.
2. Table IV is a rounded equation grid, not an independent dataset.
3. The `x=0.165, 0 K` entry should remain flagged until the original typeset cell is independently re-inspected.
4. The apparent 1 meV-scale differences elsewhere are numerical rounding, not evidence of model discrepancy.
