# Teppe et al. 2016 — signed-gap validation record

**Source:** F. Teppe et al., “Temperature-driven massless Kane fermions in HgCdTe crystals,” *Nature Communications* **7**, 12576 (2016), DOI `10.1038/ncomms12576`; open preprint `arXiv:1602.05999`.

**Role:** independent post-Hansen validation of the signed $\Gamma_6-\Gamma_8$ gap near the normal/inverted transition.

**Do not merge blindly with optical-edge data.** The reported gap is inferred from magneto-optical Landau-level transitions and a simplified Kane model, not from a conventional absorption-edge extrapolation.

## 1. Material and experiment

The paper reports two [013]-oriented MBE Hg$_{1-x}$Cd$_x$Te layers:

- approximately $3.2\ \mu\mathrm m$ thick;
- grown on semi-insulating GaAs with relaxed CdTe buffers;
- nominal compositions reported as $x=0.155$ and either $x=0.17$ or $x=0.175$ in different parts of the manuscript;
- measured by far-infrared magneto-transmission from 2 to 150 K;
- magnetic field up to 16 T;
- stated spectral resolution: 0.5 meV.

The $x=0.155$ sample is inverted at low temperature and crosses the gapless state near 77 K. The higher-Cd sample remains on the normal side over the measured range.

## 2. Operational gap definition

The paper defines

$$
E_g=E_{\Gamma_6}-E_{\Gamma_8}
$$

at the Brillouin-zone center. The value and sign are extracted by fitting inter- and intraband Landau-level transitions with a reduced $\Gamma_6\oplus\Gamma_8$ Kane model. Near zero field, the interband-transition intercept supplies the gap magnitude; the ordering of the bands and the temperature evolution determine the sign.

This is closer to a signed quasiparticle/Kane gap than to a detector cutoff or an Urbach-tailed absorption edge.

## 3. Directly usable observations

| Sample | Nominal $x$ | Temperature | Reported result | Status |
|---|---:|---:|---|---|
| B | 0.155 | 77 K | $E_g\approx0$; temperature-driven inversion transition | primary critical-point datum |
| B | 0.155 | low $T$ | inverted gap, magnitude about $20\pm4$ meV from supplementary zero-field absorption fit | sign and exact temperature require careful extraction |
| A | 0.17/0.175 | 2–4 K | positive gap about $4$–$5\pm2$ meV | composition reporting is internally inconsistent at the third decimal place |
| A and B | 0.17/0.175 and 0.155 | 2–120 K | Kane velocity nearly constant | $\tilde c=(1.07\pm0.05)\times10^6\ \mathrm{m/s}$ |

The complete temperature-series values are shown graphically and require calibrated digitization or author data before entering `measurements.csv`.

## 4. Model used by the authors

The analysis uses a simplified 6-band model containing $\Gamma_6$ and $\Gamma_8$, while neglecting:

- the split-off $\Gamma_7$ band;
- small quadratic-in-$k$ terms in the relativistic reduction;
- the complete 8-band parameter set.

The authors compare the temperature dependence with the empirical gap relation of Laurenti et al. (1990), not with the Hansen equation. The supplementary material cites:

> J. P. Laurenti et al., “Temperature dependence of the fundamental absorption edge of mercury cadmium telluride,” *J. Appl. Phys.* **67**, 6454 (1990).

Therefore Teppe 2016 is an independent validation source for a later empirical relation and for the signed transition, not a direct reconstruction source for Hansen.

## 5. Known uncertainty and provenance limitations

1. The paper gives nominal Cd fractions but the accessible text does not yet provide a full uncertainty budget or a detailed independent composition-calibration method.
2. The higher-Cd sample is labeled $x=0.175$ in the main discussion and $x=0.17$ in the methods. This $\Delta x=0.005$ difference is physically material near the inversion transition.
3. The gap is model-extracted. Uncertainty includes transition-energy resolution, Landau-level assignment, the reduced Kane approximation, and composition uncertainty.
4. The critical-point datum alone cannot separate an error in $E_g(x,T)$ from an offset in the nominal composition.

## 6. Benchmark use

Use this paper for:

- critical-temperature error at nominal $x=0.155$;
- signed-gap validation near inversion;
- testing whether a model reproduces approximately constant Kane velocity while $E_g$ changes sign;
- source-level holdout against optical-edge datasets.

Do not use it to infer:

- Hansen’s original fitting data;
- a universal optical cutoff;
- a disorder width from the mean gap alone;
- complete finite-temperature 8-band closure.

## 7. Required next extraction

- digitize the rest-mass/gap curves with figure-coordinate uncertainty;
- resolve the $x=0.17$ versus $0.175$ sample label using supplementary/source records;
- identify the exact composition-calibration procedure and uncertainty;
- reproduce the reduced-Kane fit independently;
- obtain and audit the Laurenti 1990 equation and dataset.