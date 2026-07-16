# Teppe 2016 experimental constant-velocity null

## Scientific question

Does modern temperature-dependent magnetospectroscopy support a large scalar temperature renormalization of the Kane velocity near the HgCdTe inversion transition?

## Primary source

F. Teppe et al., *Nature Communications* **7**, 12576 (2016), DOI `10.1038/ncomms12576`.

Owner-supplied PDF SHA-256:

```text
05747c300d2fc143d3bd8910426af8248e7fb5922886e79ea24c9c15e372279c
```

## Experimental system

Teppe studies two MBE-grown HgCdTe specimens:

| Sample | Composition | Temperature range | Low-temperature state |
|---|---:|---:|---|
| A | 0.175 | 2-120 K | positive-gap semiconductor |
| B | 0.155 | 2-120 K | inverted semimetal |

The main article does not report pointwise composition uncertainty. This prevents treating the nominal compositions as exact predictors in a composition-sensitive benchmark.

The spectra were measured in Faraday geometry up to 16 T with 0.5 meV spectral resolution.

## Model and observable

The fitted Hamiltonian retains the Gamma6 and Gamma8 bands and neglects:

- the split-off Gamma7 band;
- small terms quadratic in momentum.

The reduced dispersion is parameterized by signed rest mass `m_tilde` and velocity `c_tilde`, with

```text
Eg = 2 m_tilde c_tilde^2
```

and

```text
c_tilde = sqrt[2 P^2/(3 hbar^2)].
```

The gap, mass, and velocity are inferred jointly from inter- and intra-Landau-level magneto-optical transitions. They are not raw absorption-edge markers.

## Exact main-article annotations

### Sample A, x = 0.175

| Temperature | Signed gap |
|---:|---:|
| 2 K | +5 +/- 2 meV |
| 57 K | +28 meV |
| 77 K | +36 meV |
| 120 K | +56 meV |

The 57, 77, and 120 K values are exact figure annotations but lack pointwise uncertainties in the main article.

### Sample B, x = 0.155

| Temperature | Signed gap |
|---:|---:|
| 2 K | -24 meV |
| 37 K | -14 meV |
| 77 K | 0 meV |
| 120 K | +18 meV |

At 2 and 37 K, the figure labels `Eg/2 = 12 meV` and `7 meV`; the negative sign follows from the text and the inverted ordering. At 77 K the transitions exhibit the gapless square-root magnetic-field dependence, and at 120 K a positive gap has reopened.

## Velocity result

Teppe reports

```text
c_tilde = (1.07 +/- 0.05) x 10^6 m/s
```

for both specimens over 2-120 K.

The quoted relative uncertainty is

```text
0.05 / 1.07 = 4.673%.
```

Within the simplified model, the same fractional scale applies to the magnitude of the reduced matrix element `P`. This must not be promoted to a separately resolved conventional full 8-band `P8`, `P7`, or temperature-dependent invariant.

## Cross-paper consistency with Krishnamurthy 1995

The repository's exact reconstruction of Krishnamurthy Table II gives a maximum paper-convention hyperbolic-velocity drift of

```text
2.792% over 1-300 K at x = 0.22.
```

Relative to Teppe's quoted experimental velocity scale:

```text
2.792% / 4.673% = 0.598.
```

The historical calculated drift lies inside the modern quoted experimental uncertainty scale.

This is not a direct validation because:

- Krishnamurthy uses x = 0.22, while Teppe uses x = 0.155 and 0.175;
- the temperature intervals differ;
- the reduced Hamiltonian conventions differ;
- the two studies have different systematic and model discrepancies.

It is nevertheless a meaningful scale comparison: the two independent sources support the same approximately constant-velocity null at currently resolved precision.

## Scientific decision

```text
Modern magnetospectroscopy supports a constant reduced Kane velocity through a temperature-driven signed-gap transition.

A large scalar P(T) correction is not the leading null below 120 K.
```

A future microscopic calculation should first reproduce:

1. the signed gap crossing;
2. the approximately constant reduced velocity;
3. the observed Landau-level transitions.

Only then should non-gap matrix renormalization be claimed. Such a claim must alter a held-out observable beyond the combined approximately 5% velocity scale, composition uncertainty, numerical uncertainty, and model discrepancy.

## Prior-art consequence

Teppe establishes experimentally that temperature-dependent mass and signed gap do not, by themselves, imply a strongly temperature-dependent reduced Kane velocity.

Therefore none of the following is novel by itself:

- a temperature-dependent signed Kane mass;
- a gap closing and reopening with temperature;
- approximately constant Kane velocity near inversion;
- deriving mass from gap using a fixed reduced velocity;
- a scalar temperature-dependent simplified-Kane fit.

The remaining differentiating target is complete matrix closure in a fixed Gamma6 plus Gamma8 plus Gamma7 basis, including independent non-gap 8-band invariants and held-out observables.

## Claim boundary

The paper does not establish constant separate `P8` and `P7`, constant remote-band parameter `F`, constant Luttinger parameters, or a complete matrix-valued electron-phonon self-energy. Its velocity universality applies within a simplified Gamma6-Gamma8 Hamiltonian and a limited near-inversion energy range.

The Supplementary Information was not included in the supplied PDF. Pointwise fit tables and composition uncertainty therefore remain unavailable.

## Reproduction

```bash
python tools/analyze_teppe2016_constant_velocity_null.py
```
