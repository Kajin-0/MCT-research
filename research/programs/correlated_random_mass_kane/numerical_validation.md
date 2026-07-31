# R05 Phase 0 minimal numerical oracle validation

**Controlling issue:** #390  
**Program:** R05 — Correlated random-mass Kane regime  
**Evidence class:** deterministic synthetic one-dimensional model validation  
**Numerical decision:** `GO_PHYSICAL_SCREENING`  
**Material decision:** unchanged; HgCdTe activation remains blocked

## 1. What was implemented

The restricted PR 2 oracle implements

\[
H=-i\hbar v_K\sigma_x\partial_x+M(x)\sigma_z
\]

on a periodic one-dimensional grid with a Fourier-pseudospectral momentum operator.

Modules:

```text
src/mct_research/random_mass_covariance.py
src/mct_research/random_mass_dirac.py
src/mct_research/random_mass_scalar_null.py
src/mct_research/random_mass_dos.py
```

Reproducible runner:

```text
python tools/run_r05_phase0_oracle.py
```

Immutable summaries:

```text
data/validation/r05_phase0_reference.json
data/validation/r05_convergence_summary.json
```

The committed summaries retain all decision thresholds, convergence metrics, seeds, selected DOS samples, and hashes of the complete generated records. The generator reproduces the full energy-grid DOS arrays.

## 2. Normalization

The solver uses

\[
\xi=1,
\qquad
\hbar v_K=1,
\]

and therefore

\[
\varepsilon=\frac{E\xi}{\hbar v_K},
\qquad
m=\frac{\overline M\xi}{\hbar v_K},
\qquad
g=\frac{\sigma_M\xi}{\hbar v_K}.
\]

The DOS is reported per dimensionless length, per dimensionless energy, and per two-component Dirac species.

## 3. Primary numerical case

The frozen primary case is

```text
m = 0
g = 0.3
L/xi = 32
a/xi = 0.125
grid points = 256
numerical Gaussian broadening = 0.08
periodic realizations = 16
antiperiodic realizations = 16
total boundary-averaged realizations = 32
```

Seeds:

```text
periodic seed = 39005
antiperiodic seed = 139008
```

The field generator removes the finite-box sample mean but does not normalize each realization's variance.

Realized statistics:

```text
mean realized sigma_M = 0.2995356
SD of realized sigma_M = 0.0516429
maximum absolute mean-mass error = 2.78e-17
```

## 4. Analytical and structural validation

| Test | Result | Threshold | Status |
|---|---:|---:|---|
| Hamiltonian Hermiticity residual | `0.0` | `< 1e-12` | pass |
| Homogeneous finite-box maximum eigenvalue error | `3.91e-14` | `< 1e-12` | pass |
| Particle-hole paired-spectrum residual | `4.38e-15` | `< 1e-10` | pass |
| Exact zero-mean Gaussian scalar-null error | `4.44e-16` | `< 2e-12` | pass |
| Finite-box scalar-null integrated discrepancy | `0.003488` | `< 0.01` | pass |

The finite-box scalar reference uses both periodic and antiperiodic homogeneous spectra and 192-point Gauss-Hermite quadrature.

## 5. Covariance validation

A 512-realization Gaussian-field ensemble produced

```text
ensemble point variance = 1.008373
maximum correlation error over first 16 lags = 0.024491
RMS correlation error over first 16 lags = 0.013818
```

This validates the discrete periodic field generator at the declared statistical tolerance. It does not validate a specimen covariance model.

## 6. Domain-wall mechanism benchmark

A smooth periodic mass profile with two sign-changing walls was tested at fixed

```text
a / wall_width = 0.25.
```

The minimum absolute eigenvalue decreased with wall separation:

| `L` | grid points | minimum `|epsilon|` |
|---:|---:|---:|
| `20` | `80` | `1.9177e-4` |
| `40` | `160` | `8.3355e-9` |
| `60` | `240` | `3.6523e-13` |

The exponential suppression of wall-pair splitting confirms the expected coherent sign-change mechanism. It is not evidence for topological transport, percolation, or a domain-wall network in HgCdTe.

## 7. Primary correlated-versus-scalar result

The scalar null uses the same one-point Gaussian mass distribution as the correlated field.

Selected pre-experimental-convolution DOS values after the common numerical broadening are:

| `epsilon` | correlated DOS | sampling SE | scalar DOS |
|---:|---:|---:|---:|
| `-1.0` | `0.33242` | `0.00519` | `0.33833` |
| `-0.5` | `0.25741` | `0.01103` | `0.36787` |
| `0.0` | `0.38355` | `0.00942` | `0.08157` |
| `+0.5` | `0.25741` | `0.01103` | `0.36787` |
| `+1.0` | `0.33242` | `0.00519` | `0.33833` |

The correlated model transfers low-energy spectral weight toward zero energy. The matched scalar null remains strongly suppressed there because its smooth-distribution asymptote is linear in `|E|`.

This is a one-dimensional coherent-interface result. It must not be transferred directly to a bulk HgCdTe DOS.

## 8. Experimental-resolution convolution

The frozen integrated statistic is evaluated over

\[
|\varepsilon|\le1.
\]

Results versus Gaussian experimental-resolution width:

| `delta_epsilon_exp` | `Delta_1` | `Delta_infinity` |
|---:|---:|---:|
| `0.10` | `0.23687` | `1.48511` |
| `0.25` | `0.14093` | `0.41959` |
| `0.50` | `0.03977` | `0.08145` |
| `1.00` | `0.004845` | `0.008390` |

The predeclared decision width is `0.25`, and the threshold is

```text
Delta_1 > 0.10.
```

The primary case passes. The rapid collapse between widths `0.25` and `0.50` shows that experimental resolution is a controlling physical gate rather than a cosmetic plotting choice.

## 9. Sampling uncertainty

Four independent boundary-averaged batches gave

```text
Delta_1 = [
  0.1408585,
  0.1272169,
  0.1506018,
  0.1460655
]
```

with

```text
batch standard error = 0.005064.
```

The predeclared requirement was `<= 0.02`; the sampling gate passes.

## 10. Finite-size and discretization checks

At fixed `a/xi=0.125`:

| `L/xi` | grid points | `Delta_1` at width `0.25` |
|---:|---:|---:|
| `16` | `128` | `0.15934` |
| `32` | `256` | `0.14431` |
| `64` | `512` | `0.12460` |

The accepted largest-box drift is

```text
0.019715 < 0.03.
```

At fixed `L/xi=32`:

| `a/xi` | grid points | `Delta_1` |
|---:|---:|---:|
| `0.1250` | `256` | `0.14431` |
| `0.0833` | `384` | `0.13340` |
| `0.0625` | `512` | `0.13837` |

The discretization spread is

```text
0.010908 < 0.03.
```

Both gates pass, although the systematic finite-size drift remains larger than the primary sampling standard error and is retained separately.

## 11. Numerical broadening check

| numerical broadening | `Delta_1` at width `0.25` |
|---:|---:|
| `0.06` | `0.13186` |
| `0.08` | `0.14127` |
| `0.12` | `0.11924` |

The spread is

```text
0.022034 < 0.03.
```

The numerical-broadening gate passes.

## 12. Covariance-family robustness

At matched `m=0`, `g=0.3`, marginal distribution, box, grid, and broadening:

| covariance family | `Delta_1` |
|---|---:|
| Gaussian | `0.11720` |
| Matérn `nu=1/2` | `0.12400` |
| Matérn `nu=3/2` | `0.12219` |
| Matérn `nu=5/2` | `0.13214` |

The minimum value is

```text
0.117198 > 0.10.
```

The effect survives the declared covariance-family variation. This does not identify the covariance family of any specimen.

## 13. Field-conditioning sensitivity

| finite-box conditioning | `Delta_1` |
|---|---:|
| remove sample mean; do not normalize variance | `0.12603` |
| remove sample mean; normalize variance | `0.12581` |
| retain zero mode; do not normalize variance | `0.11761` |

The total spread is

```text
0.008424 < 0.03.
```

The result is not created by per-realization variance normalization or zero-mode conditioning.

## 14. Predeclared gate summary

| Gate | Metric | Threshold | Status |
|---|---:|---:|---|
| minimum accepted converged effect | `0.12460` | `> 0.10` | pass |
| primary batch SE | `0.005064` | `<= 0.02` | pass |
| finite-size drift | `0.019715` | `<= 0.03` | pass |
| discretization drift | `0.010908` | `<= 0.03` | pass |
| numerical-broadening drift | `0.022034` | `<= 0.03` | pass |
| minimum covariance-family effect | `0.11720` | `> 0.10` | pass |
| field-conditioning drift | `0.008424` | `<= 0.03` | pass |
| scalar-null discrepancy | `0.003488` | `<= 0.01` | pass |

All declared numerical checks pass.

## 15. Claims supported

The synthetic model supports the following restricted statements:

1. A finite-range correlated signed mass can produce a low-energy DOS that differs from a matched incoherent scalar mass mixture.
2. In the declared 1D oracle, the distinction is already greater than 10% at `g=0.3` after a dimensionless resolution convolution of `0.25`.
3. The effect survives the declared size, grid, numerical-broadening, covariance-family, boundary, seed, and finite-box field-conditioning checks.
4. The low-energy excess is consistent with coherent sign-changing-wall physics absent from the scalar null.

## 16. Claims not supported

The calculation does not establish:

- that bulk 3D HgCdTe exhibits the same DOS feature;
- that a real HgCdTe specimen reaches `g=0.3`;
- a measured mass correlation length;
- an optical, tunneling, transport, or magneto-optical signal;
- a topological invariant or topological Anderson phase;
- a mobility edge, percolation transition, or domain-wall conduction network;
- that full Kane structure is unnecessary for experimental prediction.

## 17. Numerical decision

```text
GO_PHYSICAL_SCREENING
```

This authorizes only the PR 3 material-overlap, experimental-resolution, and final activation decision. It does not authorize a full-Kane production calculation.