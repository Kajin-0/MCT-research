# Temperature-series acquisition priority

**Purpose:** identify the smallest set of primary data capable of testing curvature, endpoint sign, and near-inversion behavior before any production AHC calculation.

## Ranking criteria

A source is more valuable when it provides:

1. repeated temperatures on the same specimen;
2. independently measured composition;
3. a stable operational gap definition;
4. dense coverage below 50 K;
5. reported energy and composition uncertainty;
6. a signed gap where band ordering matters;
7. numerical tables or figures suitable for calibrated digitization.

## Tier 1 — immediate extraction

### Laurenti et al. 1990

**Strengths**

- same LPE specimen series measured from approximately 2 to 300 K;
- direct measurements primarily over $0.5\lesssim x\le1$;
- nonexcitonic interband edge extracted through three-dimensional exciton fits;
- reported edge accuracy better than approximately 3 meV;
- direct endpoint fits for CdTe and compiled HgTe data;
- explicit low-temperature curvature.

**Limitations**

- direct specimens are Cd-rich rather than detector-range $x\approx0.2$;
- many values are figure-only;
- composition corrections were applied to inherited Hg-rich data;
- the measurement is an optical edge, not a direct signed Kane-gap measurement.

**Use**

- select between Hansen-linear and nonlinear thermal laws at the Cd-rich endpoint;
- test the temperature-independent composition near $x=0.505$;
- constrain one- versus two-scale thermal models where the data precision permits.

### Teppe et al. 2016

**Strengths**

- fixed MBE specimens measured from 2 to approximately 150 K;
- signed $\Gamma_6-\Gamma_8$ gap extracted from Landau-level spectroscopy;
- stated spectral resolution about 0.5 meV;
- directly crosses the inversion transition;
- Kane velocity is measured simultaneously.

**Limitations**

- only two near-critical compositions;
- one specimen is labeled both $x=0.17$ and $x=0.175$;
- composition-calibration uncertainty is not yet reconstructed;
- full numerical temperature series is figure-only;
- the authors use the Laurenti equation, so agreement with that curve is not independent validation.

**Use**

- validate signed-gap and critical-temperature behavior;
- test whether a composition offset can remove the full curve residual;
- constrain finite-temperature Kane velocity and mass together with $E_g$.

## Tier 2 — acquire next

### Seiler et al. 1990

D. G. Seiler, J. R. Lowney, C. L. Littler, and M. R. Loloee, “Temperature and composition dependence of the energy gap of Hg$_{1-x}$Cd$_x$Te by two-photon magnetoabsorption techniques,” *J. Vac. Sci. Technol. A* **8**, 1237 (1990), DOI `10.1116/1.576952`.

**Why high priority**

- independent post-Hansen magneto-optical measurement class;
- explicitly targets both temperature and composition dependence;
- cited as an experimental comparator by Krishnamurthy et al.;
- likely offers the cleanest historical bridge between Hansen and modern magnetospectroscopy.

**Current blocker**

- primary full text and numerical data are not yet in the repository.

### Hansen predecessor papers

Highest acquisition priority within the 22-study graph:

1. Schmit–Stelzer 1969;
2. Scott 1969;
3. Finkman–Nemirovsky 1979;
4. Weiler 1981;
5. magneto-optical sources with multi-temperature series in Refs. 7–20.

These are required to reproduce Hansen, but their heterogeneous composition and observable definitions make them weaker than modern fixed-specimen series for sub-meV claims.

## Tier 3 — theory comparators

### Krishnamurthy et al. 1995

Use the recovered table as a historical microscopic prediction, not as experimental validation. Its main roles are:

- test whether new calculations reproduce the sign and scale of historical predictions;
- compare temperature-dependent mass and nonparabolicity;
- investigate the unresolved shallow low-temperature turnover;
- identify which new results exceed the historical model’s approximately 10–15 meV accuracy.

## Immediate sequence

1. Digitize Laurenti’s direct full-square specimen series with calibrated figure uncertainty.
2. Acquire and audit Seiler 1990.
3. Obtain a high-resolution Teppe temperature-series figure or author data.
4. Reconstruct the highest-value Hansen predecessor temperature series.
5. Run the common Hansen/Laurenti/oscillator benchmark only after specimen grouping and composition uncertainty are retained.

No production AHC calculation is authorized by this evidence ranking alone.
