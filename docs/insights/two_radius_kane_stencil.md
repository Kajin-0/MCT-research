# Two-radius finite-k Kane stencil

## Question

What is the minimum finite-k protocol that can extract the eight target parameters without confusing higher-order dispersion with temperature-dependent Kane motion?

The target vector is

```text
{Eg, Delta, P8, P7, F, gamma1, gamma2, gamma3}.
```

This note records an analytical protocol check using synthetic normalized data. It is not a CdTe or HgCdTe calculation.

## Odd and even separation

For every direction use paired `+k` and `-k` matrices.

For an odd block

```text
L(k) = P k + beta k^3 + O(k^5),
```

define

```text
D(h) = [L(+h)-L(-h)]/(2h) = P + beta h^2 + O(h^4).
```

For an even block

```text
E(k) = E(0) + c k^2 + d k^4 + O(k^6),
```

define

```text
K(h) = [E(+h)+E(-h)-2E(0)]/(2h^2)
     = c + d h^2 + O(h^4).
```

Using radii `h` and `h/2`, remove the leading contamination with

```text
X0 = [4 X(h/2) - X(h)]/3.
```

## Training directions

Use `[001]` and `[111]` for the fit.

In curvature units `C = hbar^2/(2m0)`:

```text
c6 = C(1+2F)
cHH001 = -C(gamma1-2gamma2)
cLH001 = -C(gamma1+2gamma2)
cHH111 = -C(gamma1-2gamma3)
cLH111 = -C(gamma1+2gamma3).
```

The two independent estimates of `gamma1` must agree within numerical and projection uncertainty.

## Held-out direction

Do not use `[110]` in the fit. Predict

```text
s110 = sqrt(gamma2^2 + 3 gamma3^2)
cHH110 = -C(gamma1-s110)
cLH110 = -C(gamma1+s110).
```

Compare these predictions to independently projected `[110]` matrices or curvatures.

## Synthetic result

The executable check adds cubic contamination to the linear blocks and quartic contamination to every quadratic branch. A single-radius extraction is measurably biased. The two-radius Richardson extraction recovers all eight planted parameters and the unused `[110]` curvatures to numerical precision.

## Production decision

A static or finite-temperature parameter set is admissible only if:

1. paired `+k/-k` matrices separate odd and even components;
2. the `h` and `h/2` estimates support removal of leading `O(h^2)` contamination;
3. `[001]` and `[111]` give consistent `gamma1`;
4. the unused `[110]` matrix residual is below the declared numerical, fixed-basis projection, and model-truncation uncertainty;
5. the result is stable when the fit window is reduced.

Failure of the `[110]` holdout is evidence that the standard eight-parameter Kane manifold is incomplete over the selected k window, even if the training directions fit exactly.
