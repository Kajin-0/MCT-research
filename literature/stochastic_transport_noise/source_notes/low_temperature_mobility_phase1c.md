# R06 Phase 1C low-temperature mobility source audit

**Program:** R06 — stochastic transport and finite-size noise  
**Controlling issue:** #346  
**Decision:** `SPECIMEN_CONDITIONED_ELECTRON_ANCHORS_ACCEPTED_UNIVERSAL_MOBILITY_CLOSURE_BLOCKED`

## 1. Why a single mobility constant is not accepted

HgCdTe mobility is not determined by composition and temperature alone. The reviewed sources expose sensitivity to:

- carrier density and degeneracy;
- compensation and impurity ionicity;
- alloy and polar-optical-phonon scattering;
- band nonparabolicity;
- p-type versus n-type transport;
- impurity-band participation;
- magnetic-field extraction method;
- pressure and proximity to the zero-gap regime;
- processing and specimen structure.

R06 therefore separates direct measured anchors from model-paper benchmark inputs and theoretical calculations.

## 2. Direct 77 K electron-mobility anchors

Wiley and Dexter report carrier density and electron mobility measured at 77 K by helicon and nonresonant cyclotron-absorption methods. Their Table I covers seven specimens from `x=0.135` to `x=0.203`.

The measured mobility values span approximately

```text
18 to 64 m^2/(V s)
= 1.8e5 to 6.4e5 cm^2/(V s)
```

across specimens whose electron densities range from approximately `9e20` to `2.3e22 m^-3`.

These values are accepted as **Tier A specimen-level anchors**. They are not converted into a composition-only interpolation because the table itself shows substantial variation with both composition and carrier density, and the two measurement bands do not agree identically for every sample.

## 3. Variable-field p-type evidence

Elliott, Melngailis, Harman, Kafalas, and Kernan measured p-type material near `x=0.15` at 4.2 and 77 K under hydrostatic pressure. Electron and hole densities and mobilities were inferred from variable-field Hall and magnetoresistance data.

The paper is important primarily because it demonstrates why a universal hole mobility is unsafe:

- the electron-to-hole mobility ratio is very large;
- the extraction becomes inaccurate in some conductivity regimes;
- impurity-band conduction is invoked for some samples;
- multiple hole populations are considered;
- mobility varies with pressure more strongly than inverse effective mass alone predicts.

The numerical Table I values have not been entered into R06 because the available machine extraction does not preserve the table reliably. The source is retained as methodological and uncertainty evidence, not as a detector-grade hole-mobility law.

## 4. Detector-model benchmark at x≈0.20 and 77 K

Smith's 1984 photoconductor calculation uses a model operating point with

```text
mu_n = 2e5 cm^2/(V s)
mu_p = 500 cm^2/(V s)
```

for n-type `x≈0.20` HgCdTe at 77 K. Iverson and Smith independently state that the electron mobility is about 400 times the hole mobility for `x≈0.21`, which cross-checks the same pair.

These are accepted only as **Tier B model-conditioned benchmark inputs**. They are useful for dimensionless transport tests and sensitivity centers, but they are not direct evidence that every processed detector at the same nominal composition has those mobilities.

## 5. Yoo-Kwack ledger correction

DOI `10.1063/1.364212` corresponds to:

> Sang-Dong Yoo and Kae Dal Kwack, “Theoretical calculation of electron mobility in HgCdTe,” *Journal of Applied Physics* **81**, 719–725 (1997).

It is not a 1989 experimental mobility relation. The calculation includes multiple scattering mechanisms, nonparabolic band effects, degeneracy, compensation, and impurity ionicity.

This source is classified as **Tier C theoretical architecture** until its equations, constants, and limiting cases are audited.

## 6. Accepted hierarchy

### Tier A — direct measurement

Required metadata:

- composition;
- temperature;
- carrier density;
- conductivity type;
- specimen/process description;
- extraction method;
- uncertainty.

Tier A values may anchor a matching specimen class but may not be extrapolated silently.

### Tier B — model-conditioned benchmark

A value selected in a detector theory paper may be used to reproduce that paper's operating point or define a sensitivity center. It is not promoted to a material constant.

### Tier C — theoretical relation

A scattering calculation may be implemented only after equation-level audit and must retain its required density, compensation, impurity, phonon, and band-structure inputs.

## 7. Decision

Accepted now:

- Wiley-Dexter 77 K electron-mobility table as direct specimen-level anchors;
- Smith/Iverson `2e5/500 cm^2/(V s)` pair as a model-conditioned benchmark;
- Elliott et al. as evidence that p-type and hole mobility require regime-aware extraction;
- Yoo-Kwack as a 1997 theoretical source requiring later equation audit.

Still blocked:

- a universal `mu_n(x,T)` relation;
- a universal `mu_p(x,T)` relation;
- a material-grounded mobility uncertainty ensemble;
- predictive transport runs using nominal composition alone.

The next mobility work should target primary 77 K hole-mobility measurements in detector-relevant `x≈0.18–0.30` material and recover the full Scott and Yoo-Kwack equations.
