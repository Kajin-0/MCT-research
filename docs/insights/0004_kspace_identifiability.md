# Insight 0004 — A valid Kane fit requires a designed $\mathbf{k}$ grid

**Status:** analytically derived and numerically verified  
**Novelty:** methodological result; prior-art status unconfirmed  
**Importance:** prevents false parameter extraction from underinformative first-principles samples

## Statement

The full bulk 8-band parameter vector

$$
\mathbf p=
\left(E_v,E_g,\Delta,P,F,\gamma_1,\gamma_2,\gamma_3\right)
$$

cannot be recovered from matrices sampled only along the Cartesian axes.

For axis-only points,

$$
k_xk_y=k_xk_z=k_yk_z=0.
$$

The mixed quadratic invariants vanish, so the design matrix loses the $\gamma_3$ direction. The executable projection has rank

$$
\operatorname{rank}(A)=7<8.
$$

This is an exact identifiability failure, not a convergence problem.

## Minimum correction

Include at least one direction with two or more nonzero Cartesian components, for example

$$
[110],\quad [101],\quad [011],\quad [111].
$$

The tested mixed-direction grid restores

$$
\operatorname{rank}(A)=8.
$$

For robust cubic averaging, all symmetry-related mixed directions should eventually be included rather than relying on one direction.

## Conditioning tradeoff

The parameter templates scale as

$$
M_P=O(k),
\qquad
M_F,M_{\gamma_i}=O(k^2).
$$

Therefore, shrinking the fitting region toward $\Gamma$ makes the quadratic parameters increasingly sensitive to matrix noise:

$$
\delta\gamma_i,\delta F
\sim
\frac{\delta H}{k_{\max}^2}.
$$

The limit $k_{\max}\to0$ is therefore statistically singular even though the low-order $k\cdot p$ expansion becomes formally more accurate.

## Consequence for the AHC program

A temperature-dependent change in $\gamma_i$ or $F$ is credible only if it is stable under:

1. mixed-direction grid completion;
2. $k$-window variation;
3. covariance propagation;
4. basis-gauge changes;
5. and higher-order invariant augmentation.

Without these controls, apparent finite-temperature parameter changes can be projection artifacts.
