# Seiler 1990 Figure 7 direct-marker digitization

## Scientific question

Can the experimental markers in Seiler et al. Figure 7 be converted into a calibrated specimen-level temperature ledger without sampling the fitted curve?

Yes. The ledger contains only the open-circle markers. The solid curves are excluded.

## Source and observable

- D. G. Seiler et al., *J. Vac. Sci. Technol. A* **8**, 1237-1244 (1990).
- DOI `10.1116/1.576952`.
- PDF SHA256 `5bc624ca8292fcba72ae55d13c5be03d07af03b57afc4584c2314ca08e459a49`.

The plotted value is a TPMA gap inferred by fitting resonant Landau-level transitions with a modified Pidgeon-Brown model. It remains separate from cutoff, ordinary absorption edge, excitonic transition, and simplified-Kane signed-gap measurements.

## Digitization

The page was rendered at 400 dpi. Plot boundaries and marker centers are retained in the CSV. A conservative two-pixel center half-width corresponds to:

| Panel | Sample | Temperature | Gap |
|---|---:|---:|---:|
| a | 1 | 0.381 K | 0.125 meV |
| b | 2 | 0.381 K | 0.125 meV |
| c | 3 | 0.191 K | 0.100 meV |

These are digitization bounds, not experimental uncertainties. Figure 7 does not report pointwise experimental gap uncertainties.

## Marker ledger

| Sample | Reported x | Markers | Composition use |
|---:|---:|---:|---|
| 1 | 0.239 | 14 | shape only; cutoff-derived x |
| 2 | 0.253 | 11 | shape only; x assigned using HSC |
| 3 | 0.259 +/- 0.0015 | 9 | independently composition calibrated |

Total: 34 direct markers.

## Approximately 5-10 K plateau

| Sample | Interval | Observed change | Hansen change | Difference |
|---:|---:|---:|---:|---:|
| 1 | 5.148-9.724 K | +0.499 meV | +1.278 meV | -0.779 meV |
| 2 | 4.377-9.324 K | +0.250 meV | +1.308 meV | -1.058 meV |
| 3 | 5.243-10.200 K | -0.100 meV | +1.278 meV | -1.378 meV |

All three move less than Hansen's fixed linear temperature term, reproducing the reported low-temperature plateau. This is not a standalone high-significance rejection because pointwise measurement covariance is unavailable.

## Specimen-offset shape comparison

One additive energy offset is fitted per specimen, leaving only thermal shape.

| Shape | Pooled MAE | Pooled RMSE | Maximum residual |
|---|---:|---:|---:|
| Hansen linear T | 1.583 meV | 1.824 meV | 3.013 meV |
| Seiler nonlinear | 0.903 meV | 1.061 meV | 1.994 meV |

The pooled RMSE decreases by 41.82% for the published nonlinear shape.

Per-specimen RMSE is 2.165, 1.759, and 1.223 meV for Hansen, versus 1.135, 0.998, and 1.016 meV for Seiler.

## Claim boundary

This is an in-sample reproduction. Seiler derived the nonlinear relation from these same three specimen series. The lower residual therefore does not establish predictive superiority.

Sample 2 cannot validate a composition law because its composition was assigned using HSC. Samples 1 and 2 remain valid for within-specimen temperature shape. Sample 3 is the only Figure 7 specimen with independently reported composition and uncertainty.

## Scientific decision

```text
Figure 7 is now an auditable direct experimental marker ledger.
The low-temperature plateau and nonlinear thermal shape are reproduced.
The ledger does not independently validate Seiler over Hansen.
```

It does not identify a phonon energy, separate Fan and Debye-Waller terms, or justify another oscillator family.

## Reproduction

```bash
python tools/analyze_seiler1990_figure7_digitization.py \
  --summary-json /tmp/seiler1990_figure7_digitization.json
```
