# Hansen dataset reconstruction

**Issue:** #1  
**Status:** primary paper acquired; 22-study citation graph reconstructed; 16 Table I points extracted; raw specimen-level dataset remains incomplete  
**Rule:** do not generate pseudo-data from the published polynomial and call it the Hansen dataset

## Objective

Reconstruct, at datum level, the evidence underlying G. L. Hansen, J. L. Schmit, and T. N. Casselman, “Energy gap versus alloy composition and temperature in HgCdTe,” *Journal of Applied Physics* **53**(10), 7099–7101 (1982), DOI `10.1063/1.330018`.

The published equation is

$$
E_g(x,T)=
-0.302+1.93x-0.81x^2+0.832x^3
+5.35\times10^{-4}T(1-2x),
$$

with $E_g$ in eV and $T$ in K.

## Primary-paper findings

### Evidence domain

The authors state that the fit combines data from 22 different studies. The practical fit domain was

$$
0\le x\le0.6
$$

plus the CdTe endpoint $x=1$, over

$$
4.2\le T\le300\ \mathrm K.
$$

Although the final expression spans $0\le x\le1$, the paper explicitly calls the true composition dependence for approximately $x\gtrsim0.6$ conjectural.

### Exact 22-study count

The 22 data sources are now resolved at citation and role level in `hansen_1982_source_graph.csv`.

The paper has only 21 numbered data references because Ref. 6 contains two independent private datasets:

- Rawe photoconductors;
- Tobin photodiodes.

The count is

$$
4\text{ sources in Refs. 1--4}
+2\text{ datasets in Ref. 6}
+14\text{ sources in Refs. 7--20}
+2\text{ endpoint sources in Refs. 24--25}
=22.
$$

Ref. 5 is a comparison equation, not a fitted data source. Refs. 21--23 support composition calibration rather than gap observations.

This citation-level reconstruction does not yet identify the 22 specimen-level temperature series used in the slope fit. Source count and sample count must remain distinct.

### Measurement heterogeneity

The fit combines optical and magneto-optical measurements. The optical data do not share one operational gap definition:

- Finkman–Nemirovsky: optical transmission at $\alpha=1000\ \mathrm{cm^{-1}}$;
- Scott: optical transmission at $\alpha=500\ \mathrm{cm^{-1}}$;
- Schmit–Stelzer: detector half-peak cutoff, argued to approximate $\alpha=500\ \mathrm{cm^{-1}}$ for their 10 µm detectors;
- Tobin photodiodes and Rawe photoconductors: 50% detector cutoff, approximately $\alpha=500\ \mathrm{cm^{-1}}$;
- magneto-optical sources: several distinct techniques inherited from the cited literature.

The paper acknowledges that optical experiments directly measure a cutoff energy $E_{co}$ rather than necessarily the fundamental quasiparticle gap. Hansen et al. associate $E_{co}$ with $E_g$ because the optical and magneto-optical datasets appeared mutually consistent at the precision then available.

### Composition heterogeneity

Composition was obtained by several methods:

- vendor optical-cutoff calibration tied to destructive chemistry;
- density with an assumed linear density–composition relation;
- detector/transmission cutoff calibration;
- re-evaluation of selected Weiler samples using additional transmission-cutoff measurements.

For Schmit–Stelzer and the Tobin/Rawe data, the stated density conversion is

$$
x=3.628-0.44924\rho.
$$

For Weiler’s samples, alternative density measurements would have shifted the reported Cd fraction by approximately $+0.01$ to $+0.035$. This is much larger than the composition precision required for modern meV-level validation near band inversion.

### Exclusions

Four lowest-composition samples from the original Schmit–Stelzer set were excluded because of mercury inclusions.

## Published fitting sequence

The equation was not obtained from one global polynomial fit to raw points.

1. For each of the 22 samples having temperature-dependent data, fit a linear $E_g(T)$ relation.
2. Fit the resulting slopes versus composition:

$$
\frac{\partial E_g}{\partial T}
=-1.08\times10^{-3}x+5.35\times10^{-4}\ \mathrm{eV/K}.
$$

3. Normalize each temperature-dependent sample to 80 K using its fitted slope:

$$
E_g(x,80)=E_g(x,T)-(T-80)\frac{\partial E_g}{\partial T}.
$$

4. Average the normalized values for each sample.
5. Perform a nonlinear least-squares composition fit to those 80 K values together with data lacking temperature sweeps, including the HgTe and CdTe endpoints.

The paper does not report datum-level weights, coefficient covariance, or a machine-readable residual table.

This staged regression cannot independently test low-temperature curvature because each raw specimen series is first compressed into a linear slope and an 80 K value. The exact aliasing and normalization bias are derived in `docs/insights/0016_hansen_staged_fit_cannot_test_curvature.md`.

## Reported fit quality

For the new expression, Hansen et al. report:

- average deviation: $-0.001\ \mathrm{eV}$;
- standard error of estimate: $0.013\ \mathrm{eV}$.

The standard error is therefore 13 meV, which is already comparable to or larger than many modern model differences being discussed in this project. It is not a direct test of whether $\partial^2E_g/\partial T^2=0$, because linearity was imposed during the first reduction stage.

## Recovered numerical data

`measurements.csv` now contains the 16 numerical values printed in Table I:

- 7 Tobin photodiode cutoff points at 80 K;
- 9 Rawe photoconductor cutoff points at 80 K.

These are direct primary-table transcriptions, but they represent detector cutoff energies rather than a uniform modern fundamental-gap observable. They have no stated datum-level uncertainty in the paper.

## Files

- `hansen_1982_source_graph.csv` — every numbered reference, its role, and the exact reconstruction of the 22 data sources.
- `source_inventory.csv` — broader primary, inherited, theoretical, and later-validation inventory.
- `acquisition_log.md` — acquisition and audit record, including file hash.
- `measurements.csv` — recovered numerical observations; currently the 16 Table I points.
- `digitization_log.csv` — figure-coordinate provenance and calibration.
- `fit_reproduction.json` — exact model, weights, optimizer, and coefficient covariance when reproducible.
- `residuals.csv` — residuals in energy before wavelength conversion.

## Remaining reconstruction gates

The Hansen fit is not fully reproduced until the following are recovered or explicitly declared irrecoverable:

1. primary papers and specimen mapping for the fitted sources;
2. raw or digitized values for the 22 temperature-dependent sample series;
3. non-temperature-dependent points used in the 80 K composition fit;
4. source-specific composition methods and uncertainties;
5. source-specific optical or magneto-optical gap definitions;
6. any implicit weighting and averaging choices;
7. coefficient covariance or a defensible bootstrap reconstruction;
8. datum-level residuals in meV;
9. correlation from repeated temperatures on the same specimen;
10. sensitivity to excluding endpoints and mixed measurement classes.

## Energy-first residual rule

All model comparison is performed first in energy:

$$
r_i=E_{g,i}^{\mathrm{measured}}-E_g(x_i,T_i).
$$

Only after residuals are established in meV may an equivalent wavelength error be reported. Since

$$
\lambda=\frac{hc}{E_g},
$$

wavelength residuals become divergent and asymmetric near $E_g=0$ and are unsuitable as the primary objective.

## Prohibited shortcuts

- Sampling the polynomial and treating those samples as observations.
- Treating all cutoff criteria as one exact fundamental-gap definition.
- Combining different studies without source and specimen grouping.
- Assigning zero composition uncertainty when the source did not report it.
- Fitting in wavelength and reporting the result as an energy-gap reconstruction.
- Describing the $x>0.6$ cubic behavior as strongly data constrained.
- Treating the reported 13 meV error as evidence that temperature curvature is absent.
