# R05 Phase 0 HgCdTe parameter envelope

**Controlling issue:** #390  
**Status:** source-bounded where possible; exploratory values are explicitly separated  
**Primary conclusion:** `v_K` is reasonably bounded, `Mbar` is controllably tunable, but neither the near-critical mass variance nor the continuum correlation length `xi` is presently source-qualified.

## 1. Constants and normalization

Use

```text
hbar = 6.582119569e-16 eV s
v_K,nominal = 1.07e6 m/s
hbar v_K,nominal = 0.704286793883 eV nm
```

Dimensionless controls:

\[
m=\frac{\overline M\xi}{\hbar v_K},
\qquad
g=\frac{\sigma_M\xi}{\hbar v_K}.
\]

Under the Phase 0 convention `Eg = 2M`, the existing R05 `kappa` equals `g`.

## 2. Parameter table

| Symbol | Physical definition | Lower | Nominal | Upper | Units | Temperature/composition | Evidence | Quality | Conversion/uncertainty |
|---|---|---:|---:|---:|---|---|---|---|---|
| `v_K` | Simplified Kane velocity near the transition | `1.02e6` | `1.07e6` | `1.12e6` | m/s | broad near-transition range in Teppe et al. | Teppe et al., *Nat. Commun.* 7, 12576 (2016), DOI `10.1038/ncomms12576` | direct experimental model fit | reported `+/-0.05e6 m/s`; systematic model dependence remains |
| `hbar v_K` | Dirac energy-length scale | `0.671376` | `0.704287` | `0.737197` | eV nm | inherited from `v_K` | derived | high arithmetic confidence | linear conversion from `v_K` |
| `P` | Kane momentum coupling in repository units | `7.6` | `8.0` | `8.4` | eV angstrom | Finkman samples `0.205 < x < 0.310` | Finkman 1983 repository transcription | historical experimental fit | `P=(8.0+/-0.4)e-8 eV cm`; `1e-8 eV cm = 1 eV angstrom` |
| `Mbar` | Mean symmetric Dirac mass `Eg/2` | `-21.93` | `0` | `+29.87` | meV | exploratory near-transition box `0.14 <= x <= 0.17`, `4 <= T <= 150 K` | repository Hansen model | model output, not measured envelope | model extrema give `Eg=-43.85` to `+59.74 meV` |
| `sigma_x,macro` | reported sample-composition homogeneity bound | not a standard deviation | — | approximately `0.002` | Cd fraction | Finkman 1983 samples, not the Teppe near-critical specimens | repository primary transcription | source statement, weak for R05 | “better than +/-0.002”; no spatial kernel, covariance, or probability model |
| `sigma_x` | local composition standard deviation used for screening | `0.0005` | `0.002` | `0.010` | Cd fraction | near-transition exploratory sweep | exploratory | not material validated | spans below reported macro bound through deliberately aggressive disorder |
| `sigma_M` | local mass standard deviation | `0.415` | `1.661` | `8.306` | meV | near `x_c(77 K)` under Hansen slope | derived exploratory | model-conditioned | `sigma_M = 0.5 abs(dEg/dx) sigma_x`, with `dEg/dx approximately 1.661 eV` |
| `xi` | continuum correlation length of the signed mass field | none accepted | none accepted | none accepted | nm | near-critical HgCdTe | no direct qualifying source identified | unresolved | must specify field, specimen, temperature, kernel, and covariance convention |
| `xi_explore` | numerical screening length | `0.65` | `100` | `2000` | nm | not a material claim | exploratory | synthetic only | lower value is lattice-scale order of magnitude; upper values test growth-scale structure |
| `T` | specimen temperature | `4` | `77` | `150` | K | near-transition screening | experiments and gap-model domain | mixed | 77 K is the reported transition temperature for one `x approximately 0.155` specimen |

## 3. Gap-to-mass mapping near the transition

The repository Hansen law is

\[
E_g(x,T)=
-0.302+1.93x-0.81x^2+0.832x^3
+5.35\times10^{-4}(1-2x)T
\]

in eV.

At `T=77 K`, the model critical composition is

```text
x_c = 0.1494464216
```

and

```text
dEg/dx at x_c = 1.661253 eV per Cd fraction.
```

Therefore

\[
\sigma_M
\simeq
0.8306265\,\mathrm{eV}\times\sigma_x.
\]

Examples:

| `sigma_x` | `sigma_E` | `sigma_M` | `xi` required for `g=1` |
|---:|---:|---:|---:|
| `0.0005` | `0.831 meV` | `0.415 meV` | `1696 nm` |
| `0.0010` | `1.661 meV` | `0.831 meV` | `848 nm` |
| `0.0020` | `3.323 meV` | `1.661 meV` | `424 nm` |
| `0.0050` | `8.306 meV` | `4.153 meV` | `170 nm` |
| `0.0100` | `16.613 meV` | `8.306 meV` | `84.8 nm` |

These are mathematical consequences of the declared model, not measured HgCdTe disorder values.

## 4. Dimensionless disorder screening

Using `hbar v_K = 0.704287 eV nm`:

| `sigma_M` | `g(xi=0.65 nm)` | `g(10 nm)` | `g(100 nm)` | `g(500 nm)` |
|---:|---:|---:|---:|---:|
| `0.415 meV` | `0.00038` | `0.00589` | `0.0589` | `0.295` |
| `0.831 meV` | `0.00077` | `0.0118` | `0.118` | `0.590` |
| `1.661 meV` | `0.00153` | `0.0236` | `0.236` | `1.179` |
| `4.153 meV` | `0.00383` | `0.0590` | `0.590` | `2.948` |
| `8.306 meV` | `0.00767` | `0.1179` | `1.179` | `5.897` |

### Interpretation

- Atomic-scale or nearly random alloy correlations imply `g << 1` for all but implausibly large mass variance.
- `g approximately 1` requires either large composition variance, a correlation length of tens to hundreds of nanometres, or both.
- The reported `+/-0.002` sample homogeneity statement is not a local standard deviation and cannot be paired with an assumed `xi` as material evidence.
- The 1988 alloy-cluster study reports nearly random occupation tendencies but does not establish the continuum electronic-mass covariance length required here.
- The 2009 PL study establishes composition-related localization/optical disorder at `x=0.38` and `0.57`, but the accessible record does not provide a qualifying near-transition `xi`.

## 5. Mean-mass screening

For a selected correlation length,

\[
|m|=1
\quad\Longleftrightarrow\quad
|\overline M|=\frac{0.7043\,\mathrm{eV\,nm}}{\xi}.
\]

Examples:

| `xi` | `|Mbar|` for `|m|=1` | corresponding `|Eg|` |
|---:|---:|---:|
| `1 nm` | `704 meV` | `1.409 eV` |
| `10 nm` | `70.4 meV` | `140.9 meV` |
| `100 nm` | `7.04 meV` | `14.1 meV` |
| `500 nm` | `1.41 meV` | `2.82 meV` |

Near the temperature/composition-tuned transition, `m` can be made small even when `xi` is large. The harder physical gate is therefore `g`, not `m`.

## 6. Source-quality boundary for `xi`

A qualifying source must provide or permit reconstruction of:

```text
specimen identity
growth method
composition and temperature
measured spatial field
lateral and depth resolution
sampling geometry
point-spread or voxel kernel
covariance or pair-correlation definition
uncertainty
reported or reconstructable correlation length
```

The following do not qualify by themselves:

- PL linewidth or red shift;
- a macroscopic composition tolerance;
- nominal growth-layer thickness;
- a synthetic covariance fit;
- smoothing one raster at several scales;
- theoretical nearest-neighbour alloy correlation without mapping to the continuum mass field.

## 7. Preliminary physical gate

```text
v_K gate: PASS
mean-mass tunability gate: PASS
mass-variance gate: UNRESOLVED
correlation-length gate: FAIL_NO_QUALIFYING_SOURCE
nontrivial g regime: EXPLORATORY_ONLY
```

The current evidence does not support a physically credible claim that near-critical HgCdTe reaches `g approximately 1`.

## 8. Consequence for computation

A low-cost minimal oracle may still be useful to answer a bounded methodological question:

> What minimum combination of `sigma_M`, `xi`, and experimental resolution is required for a matched correlated-versus-scalar DOS difference above 10%?

That calculation is a threshold and experiment-design benchmark. Until a qualifying `xi` source is found, it cannot activate an HgCdTe material claim.