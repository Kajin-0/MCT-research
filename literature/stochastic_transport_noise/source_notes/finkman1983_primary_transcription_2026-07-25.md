# R06 Phase 1C — Finkman 1983 primary transcription

**Date:** 2026-07-25  
**Controlling issue:** #346  
**Source:** E. Finkman, *Journal of Applied Physics* **54**, 1883–1886 (1983)  
**DOI:** `10.1063/1.332241`  
**Decision:** use recovered experimental metadata and fitted outputs as historical evidence; keep symbol-exact replication and material fitting blocked

## 1. Recovery status

An author-uploaded full-text copy was recovered. Its text layer is sufficient to
transcribe the experimental domain, sample metadata, error terms, fitting
procedure, and final fitted parameter values.

The mathematical typography of the conduction-band integral and several
intermediate equations remains corrupted in the extracted text. Those equations
are not authorized for implementation until visually checked against the primary
page image.

## 2. Experimental domain

The study used HgCdTe samples with:

```text
0.205 < x < 0.310.
```

Most samples were n-type with approximately:

```text
4e14 < N_D - N_A < 6e15 cm^-3.
```

Low-impurity p-type samples were also included. Their impurity concentrations
were adjusted separately in the analysis.

For a net impurity concentration near `1e15 cm^-3`, the reported near-intrinsic
regimes were approximately:

```text
x near 0.2: T >= 160 K,
x near 0.3: T >= 200 K.
```

The upper measurement temperature did not exceed 345 K to avoid material
degradation.

## 3. Sample characterization and reported error sources

Composition was determined by microprobe analysis using a sample with `x=0.215`
as the calibration standard.

The paper reports:

```text
sample homogeneity: better than +/- 0.002 in x,
maximum sample-thickness error: +/- 3%,
repeatability after more than one year in vacuum: within 1%.
```

The thickness determination was identified as the largest possible experimental
error source.

These are source-level error statements. They are not point-by-point standard
uncertainties and therefore do not satisfy the PR #385 material-evidence
contract.

## 4. Hall inversion and neutrality procedure

At elevated temperature the electron concentration was inferred from the Hall
coefficient using the one-carrier expression:

```text
n = -1/(q R_H).
```

The paper justifies this approximation by the high electron-to-hole mobility
ratio in HgCdTe.

For n-type samples, the net impurity concentration was taken from the
low-temperature Hall constant. The intrinsic carrier concentration was then
computed using the neutrality relation before fitting the Kane model.

The extracted text preserves the structure of Eq. (1), but its donor/acceptor
subscripts and radical typography require visual confirmation. No normalized
version is committed as an implementation equation in this gate.

## 5. Model assumptions

The analysis states the following assumptions:

1. the Kane nonparabolic model is applied at elevated temperature even though
   the underlying model is strictly valid at 0 K;
2. the band gap is linear in temperature at fixed composition;
3. the momentum matrix element `P` is independent of composition and
   temperature;
4. the heavy-hole mass is independent of composition and temperature;
5. holes are nondegenerate in the experimental regime;
6. `Eg0(x)` and `dEg/dT` were initially represented with linear composition
   dependence, followed by a CdTe endpoint correction.

The fitting procedure adjusted `Eg0`, `dEg/dT`, `P`, and the heavy-hole mass to
obtain intrinsic neutrality across the measured temperatures and compositions.

## 6. Recovered final results

The reported fitted momentum matrix element is:

```text
P = (8.0 +/- 0.4)e-8 eV cm.
```

The reported heavy-hole mass ratio is:

```text
m_h*/m0 = 0.63 +/- 0.06.
```

The reported gap relation is:

```text
Eg(x,T) = -0.287
          + 1.717 x
          + 5.805e-4 T (1 - 2.01 x)
          + 0.2415 x^4
```

with `Eg` in eV and `T` in kelvin.

The paper states that the final term was added to reach the CdTe endpoint. The
reported fitted composition range is approximately `0.2 < x < 0.3`.

The extracted text renders the gap standard deviation as `4 MeV`. This is almost
certainly an OCR unit error, but this gate does not silently replace it with
`meV`. The primary page must be visually checked before the unit is normalized.

## 7. Recovered figure-level examples

Figure 1 is identified as an `x=0.225` carrier-concentration-versus-temperature
comparison with:

```text
n-type: N_D - N_A = 3.4e15 cm^-3,
p-type: N_A - N_D = 4.9e14 cm^-3.
```

Figure 2 is identified as an `x=0.290` comparison with approximately:

```text
n-type: N_D - N_A = 1.4e15 cm^-3,
p-type: N_A - N_D = 6.1e14 cm^-3.
```

The plotted points have not been digitized. These figure labels do not constitute
accepted density observations.

## 8. Equation exactness boundary

The following source elements remain visually unresolved:

- the complete normalized transcription of the neutrality relation in Eq. (1);
- the prefactors, variables, and limits in the conduction integral in Eq. (2);
- the exact secular-dispersion typography in Eq. (3);
- the effective-mass expression in Eq. (5);
- the heavy-hole concentration expression in Eq. (6).

Eq. (4), the final reported parameter values, and Eq. (7) are readable at useful
fidelity. The unresolved equations prevent a claim of exact Finkman 1983 model
replication.

## 9. Relation to the project-defined Kane closure

The source provides valuable historical constraints on the interband matrix
element, heavy-hole mass, gap law, sample domain, and Hall-analysis assumptions.

It does not directly provide the project parameters:

```text
N_*,
alpha.
```

No direct substitution or silent conversion is authorized. A future mapping
would require:

- a derivation from the declared project dispersion;
- unit and degeneracy audits;
- explicit heavy-hole and neutrality treatment;
- validation against independent density or compressibility evidence.

## 10. Material-evidence decision

The primary recovery materially improves provenance but does not create an
accepted PR #385 point because:

- no point-level Hall/density table with positive standard uncertainty is
  recovered;
- reduced chemical potential is not independently known;
- the neutrality closure is not independently validated for R06;
- no direct compressibility or generalized-Einstein observation is supplied.

The material status remains:

```text
blocked_no_accepted_hgcdte_reference_set
```
