# CdTe static Kane method smoke

## Decision

The physical CdTe A0 readiness gate remains unchanged and closed. It still requires a fully sourced execution lattice, verified installed binaries, rendered inputs, and runtime hashes.

A separate static method smoke is permitted at a declared planning geometry because its claim is narrower:

> The fixed-basis finite-k projection, two-radius derivative extraction, eight-parameter fit, covariance propagation, and unused-[110] prediction execute coherently.

It cannot claim a converged or accepted CdTe lattice constant or physical Kane parameter set.

## Planning geometry

The smoke uses zincblende CdTe at `a = 6.4760 angstrom`. This is a rounded sensitivity center from the primary-source lattice audit, not an execution reference for phonons or electron-phonon work.

## Equal-magnitude stencil

Use Cartesian magnitudes `h = 0.010 inverse angstrom` and `h/2 = 0.005 inverse angstrom`, with both signs along:

- training: `[001]` and `[111]`;
- held out: `[110]`.

Every direction is normalized before multiplication by `|k|`; this prevents the crystallographic direction vector from changing the derivative radius.

Odd and even finite differences are extrapolated with

```text
X0 = [4 X(h/2) - X(h)] / 3.
```

## Projection and closure

The fixed reference subspace is the Gamma6 plus Gamma8 plus Gamma7 spinor manifold at Gamma. Reconstruct each finite-k Hamiltonian using the overlap metric rather than eigenvector relabeling.

Train `Eg`, `Delta`, `P8`, `P7`, `F`, `gamma1`, `gamma2`, and `gamma3` only on Gamma, `[001]`, and `[111]`. Predict `[110]` without refitting and score the correlated residual with the propagated full parameter covariance.

Use 12 target/guard states initially and repeat with 16. Report every overlap singular value and the matrix change under window expansion. No universal absolute overlap threshold is invented before the first physical smoke.

## Hard stops

Stop without a scientific claim if any of the following occurs:

- runtime pseudopotential hashes differ from the pinned Cd/Te hashes;
- installed `pw.x` identity is missing;
- Hermiticity or time-reversal residuals are unexplained;
- the extracted parameters change materially between `h`, `h/2`, and the extrapolated limit;
- the 12-to-16-state reconstruction is unstable;
- the unused `[110]` covariance-aware closure fails.

No phonon, AHC, HgTe, or alloy calculation is authorized by this smoke.
