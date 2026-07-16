# Teppe et al. 2016 — signed-gap validation record

**Source:** F. Teppe et al., “Temperature-driven massless Kane fermions in HgCdTe crystals,” *Nature Communications* **7**, 12576 (2016), DOI `10.1038/ncomms12576`; open preprint `arXiv:1602.05999`.

**Role:** independent post-Hansen validation of the signed $\Gamma_6-\Gamma_8$ gap near the normal/inverted transition.

**Do not merge blindly with optical-edge data.** The reported quantities include both magneto-optical Landau-level gaps and zero-field absorption magnitudes.

## 1. Material and experiment

The paper reports two [013]-oriented MBE Hg$_{1-x}$Cd$_x$Te layers:

- approximately $3.2\ \mu\mathrm m$ thick;
- grown on semi-insulating GaAs with relaxed CdTe buffers;
- nominal compositions reported as $x=0.155$ and either $x=0.17$ or $x=0.175$ in different parts of the manuscript;
- measured by far-infrared magneto-transmission from 2 to 150 K;
- magnetic field up to 16 T;
- stated spectral resolution: 0.5 meV.

The $x=0.155$ sample is inverted at low temperature and crosses the gapless state near 77 K. The higher-Cd sample remains on the normal side over the measured range.

## 2. Operational gap definitions

### Landau-level Kane gap

The paper defines

$$
E_g=E_{\Gamma_6}-E_{\Gamma_8}
$$

at the Brillouin-zone center. The value and sign are extracted by fitting inter- and intraband Landau-level transitions with a reduced $\Gamma_6\oplus\Gamma_8$ Kane model. Near zero field, the interband-transition intercept supplies the gap magnitude; the known band ordering and temperature evolution determine the sign.

### Zero-field absorption magnitude

The supplement separately fits the zero-field absorption coefficient. This supplies a non-negative gap magnitude. It does not independently determine the sign of the $\Gamma_6-\Gamma_8$ ordering.

These two measurement classes are retained as separate records in `teppe2016_explicit_points.csv`.

## 3. Explicitly reported numerical observations

Only values stated numerically in the text or supplement are entered at this stage.

| Record | Sample | Nominal $x$ | $T$ | Observable | Reported value |
|---|---|---:|---:|---|---:|
| `TEPPE_A_LL_2K` | A | 0.175, but 0.17 in methods | 2 K | signed Kane gap from Landau-level fit | $+5\pm2$ meV |
| `TEPPE_A_ABS_4P2K` | A | 0.175, but 0.17 in methods | approximately 4.2 K | zero-field absorption gap magnitude | $4\pm2$ meV |
| `TEPPE_B_ABS_4P2K` | B | 0.155 | approximately 4.2 K | zero-field absorption gap magnitude | $20\pm4$ meV |
| `TEPPE_B_CRITICAL_77K` | B | 0.155 | approximately 77 K | signed Kane gap | $0$ meV; pointwise uncertainty not stated |

The complete temperature-series values are shown graphically and remain excluded until calibrated digitization is completed.

## 4. Published-coefficient model predictions

### Sample A, signed 2 K point

For the reported value $E_g=5\pm2$ meV:

| Composition interpretation | Hansen prediction | Laurenti prediction | Hansen residual | Laurenti residual |
|---|---:|---:|---:|---:|
| $x=0.170$ | 7.48 meV | 2.97 meV | $-2.48$ meV | $+2.03$ meV |
| $x=0.175$ | 16.10 meV | 12.08 meV | $-11.10$ meV | $-7.08$ meV |

Here residual means measured minus predicted. The internal composition-label difference changes each prediction by roughly 9 meV, several times the stated 2 meV gap uncertainty. At $x=0.170$, both equations are compatible at roughly the one-sigma level; at $x=0.175$, both substantially overpredict the stated gap.

This datum therefore cannot rank the equations until the sample composition is resolved.

### Sample B, low-temperature absorption magnitude

At $x=0.155$ and 4.2 K:

| Model | Signed prediction | Predicted magnitude | Residual against $20\pm4$ meV magnitude |
|---|---:|---:|---:|
| Hansen | $-17.66$ meV | 17.66 meV | $+2.34$ meV |
| Laurenti | $-24.12$ meV | 24.12 meV | $-4.12$ meV |

Both are compatible with this coarse absorption-magnitude point within approximately one standard deviation. It does not distinguish the equations.

### Sample B, 77 K transition

At nominal $x=0.155$:

- Hansen predicts $E_g=+9.21$ meV and $T_c=52.04$ K;
- Laurenti predicts $E_g=-0.0478$ meV and $T_c=77.124$ K.

This point strongly selects Laurenti at nominal composition, but it is not independent validation of Laurenti because the paper explicitly uses the Laurenti equation and the composition provenance remains unresolved.

## 5. Model used by the authors

The analysis uses a simplified 6-band model containing $\Gamma_6$ and $\Gamma_8$, while neglecting:

- the split-off $\Gamma_7$ band;
- small quadratic-in-$k$ terms in the relativistic reduction;
- the complete 8-band parameter set.

The authors compare the temperature dependence with the empirical gap relation of Laurenti et al. (1990), not with the Hansen equation.

Therefore Teppe 2016 is useful for signed-transition and Kane-velocity validation, but the plotted Laurenti agreement is not statistically independent evidence for the equation used in the comparison.

## 6. Known uncertainty and provenance limitations

1. The paper gives nominal Cd fractions but the accessible text does not provide a complete uncertainty budget or independent composition-calibration chain.
2. Sample A is labeled $x=0.175$ in the main discussion and $x=0.17$ in the methods. This $\Delta x=0.005$ difference dominates meV-level model comparison.
3. The signed gap is model-extracted. Uncertainty includes transition-energy resolution, Landau-level assignment, the reduced Kane approximation, and composition uncertainty.
4. The absorption fit gives a magnitude and should not be silently converted into an independently measured signed gap.
5. The critical-point datum alone cannot separate an error in $E_g(x,T)$ from an offset in nominal composition.

## 7. Benchmark use

Use this paper for:

- critical-temperature error at nominal $x=0.155$;
- signed-gap validation near inversion;
- consistency between Landau-level and absorption-derived gap magnitudes;
- testing whether a model reproduces approximately constant Kane velocity while $E_g$ changes sign;
- source-level holdout against optical-edge datasets.

Do not use it to infer:

- Hansen’s original fitting data;
- an independent validation of the Laurenti curve used by the authors;
- a universal optical cutoff;
- a disorder width from the mean gap alone;
- complete finite-temperature 8-band closure.

## 8. Required next extraction

- obtain a high-resolution Figure 4 asset or author data;
- digitize the rest-mass/gap series with calibrated coordinate and marker uncertainty;
- retain Sample A's composition as an unresolved categorical/latent quantity until source records settle 0.17 versus 0.175;
- identify the exact composition-calibration procedure and uncertainty;
- reproduce the reduced-Kane fit independently.
