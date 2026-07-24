# R06 Phase 1C mobility and static-permittivity source audit

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Status:** source domains and model boundaries clarified; universal material closures remain unauthorized

## 1. Scope

This audit reviews the source basis for three Phase 1C inputs:

1. low-temperature electron mobility;
2. low-temperature hole mobility;
3. static HgCdTe permittivity.

The purpose is not to select convenient textbook numbers. It is to determine what the cited primary evidence actually supports and what remains unresolved.

## 2. Electron mobility

### 2.1 Wiley and Dexter (1969)

**Source:** J. D. Wiley and R. N. Dexter, "Helicons and Nonresonant Cyclotron Absorption in Semiconductors. II. Hg1-xCdxTe," *Physical Review* **181**, 1181-1190 (1969).

The primary source reports microwave-helicon and nonresonant-cyclotron measurements of electron density, effective mass, and mobility for specimens with approximately

```text
0.135 <= x <= 0.203
```

Most measurements were performed at 77 K, with some values at 1.3 K. Reported 77 K carrier concentrations span approximately

```text
8e20 to 2e22 m^-3.
```

The repository's existing table transcription retains specimen-conditioned mobility values of roughly

```text
18 to 64 m^2 V^-1 s^-1
```

for the audited specimens. These values are direct anchors only when composition, density, temperature, and measurement method remain attached.

One specimen near `x=0.149` was measured from 77 to 185 K; the reported mobility was approximately proportional to `T^-2` over that restricted interval. This does not authorize a global `T^-2` law for all HgCdTe.

### Decision

Wiley-Dexter is accepted as a Tier-A specimen-conditioned anchor. It is not a composition-only or temperature-only mobility law.

### 2.2 Scott (1972)

**Source:** W. Scott, "Electron Mobility in Hg1-xCdxTe," *Journal of Applied Physics* (1972), DOI `10.1063/1.1661217`.

The source abstract reports Hall and resistivity measurements over compositions extending to approximately `x=0.6`, generally at carrier concentrations below `2e15 cm^-3`. It describes:

- a room-temperature mobility maximum near the semiconductor-semimetal transition;
- failure of a simple nondegenerate parabolic optical-mode model to fit accurately near low `x`;
- low-temperature mobility behavior consistent with singly ionized donor scattering for the measured specimens.

The exact data tables, fitted relation, and specimen metadata have not been transcribed into R06.

### Decision

Scott is accepted as model-form and composition-trend evidence. No Scott interpolation or universal low-temperature relation is authorized until the primary tables and equations are audited.

## 3. Hole mobility

### 3.1 Elliott et al. (1972)

**Source:** C. T. Elliott, John Melngailis, T. C. Harman, J. A. Kafalas, and W. C. Kernan, "Pressure Dependence of the Carrier Concentrations in p-Type Alloys of Hg1-xCdxTe at 4.2 and 77 K," *Physical Review B* **5**, 2985-2996 (1972).

The existing repository audit identifies variable-field Hall and magnetoresistance measurements on p-type specimens near

```text
0.138 <= x <= 0.149
T = 4.2 and 77 K
pressure = 0 to 9 kbar.
```

The paper resolves multiple populations and regime-dependent transport, including impurity-band conduction. This makes it direct evidence against treating a single heavy-hole mobility as a universal function of composition and temperature.

The numerical table needed for a specimen-level hole-mobility anchor remains visually untranscribed.

### 3.2 Detector-model benchmark

Smith (1984) uses

```text
mu_n = 2e5 cm^2 V^-1 s^-1
mu_p = 500 cm^2 V^-1 s^-1
```

for a model-conditioned `x approximately 0.20`, 77 K photoconductor benchmark. Iverson and Smith (1985) independently describe an electron-to-hole mobility ratio of approximately 400 near `x approximately 0.21`.

These are useful detector-model sensitivity centers. They are not direct universal hole-mobility measurements.

### Decision

No source-exact universal low-temperature hole-mobility closure is accepted. Phase 1 may use only:

- explicitly labeled specimen-conditioned primary anchors after table transcription;
- the Smith value as a Tier-B model benchmark;
- dimensionless mobility-ratio sensitivity studies.

## 4. Static permittivity

### 4.1 Baars and Sorger (1972)

**Source:** J. Baars and F. Sorger, "Reststrahlen spectra of HgTe and CdxHg1-xTe," *Solid State Communications* **10**, 875-878 (1972), DOI `10.1016/0038-1098(72)90211-6`.

The source reports infrared reflection spectra for

```text
0 <= x <= 0.54
T = 77 and 300 K
1000 to 25 cm^-1.
```

The spectra were analyzed by Kramers-Kronig integration. The alloys show two transverse-optical modes, and an additional temperature-sensitive band near `100 cm^-1` for `x<0.34`.

This source is accepted as primary phonon/reststrahlen evidence and as a domain constraint for dielectric reconstruction. It does not, by itself, establish the later commonly quoted quadratic static-permittivity polynomial.

### 4.2 Existing benchmark bracket

The repository currently retains two nearly identical benchmark curves:

```text
epsilon_s,lower(x) = 20.5 - 15.6*x + 5.7*x^2
epsilon_s,upper(x) = 20.5 - 15.5*x + 5.7*x^2
```

Their difference is

```text
epsilon_s,upper - epsilon_s,lower = 0.1*x.
```

Near `x=0.20`, this is only `0.02`. That narrow separation quantifies coefficient-lineage ambiguity between two reported forms. It is not a defensible estimate of total physical uncertainty, specimen variation, temperature dependence, or model discrepancy.

### Decision

For architecture-level Poisson and screening tests, R06 may publish both curves as a provenance bracket, with the lower curve as a nominal benchmark. Neither curve is yet authorized as a predictive material closure.

The electrostatic model must use static permittivity `epsilon_s`, not high-frequency optical permittivity `epsilon_infinity` and not passivation or oxide permittivity.

## 5. Parameter policy

Until the remaining source gaps close:

- electron mobility must retain specimen, density, temperature, method, and processing metadata;
- hole mobility must be treated as unresolved or as an explicitly labeled model benchmark;
- mobility-ratio sweeps are preferred to unsupported universal scalar values;
- the static-permittivity pair is a provenance sensitivity bracket only;
- no mobility or permittivity source in this gate supports predictive detector performance claims.

## 6. Remaining source actions

1. Transcribe Scott's primary tables and equations.
2. Visually transcribe Elliott et al. Table I and retain population/regime labels.
3. Recover the Brice-Capper pages and their primary reference lineage for the quadratic permittivity curves.
4. Recover numerical Baars-Sorger oscillator data sufficient for an independent Lyddane-Sachs-Teller consistency calculation.
5. Define material uncertainty only after source covariance, specimen scatter, or a defensible inter-source ensemble is available.

## 7. Gate conclusion

The mobility and permittivity inputs are sufficiently constrained for dimensionless sensitivity studies, but not for a material-accurate HgCdTe solver. The appropriate Phase 1 action is **proceed with explicit benchmark labels and unresolved-parameter flags**, not to insert universal empirical laws.