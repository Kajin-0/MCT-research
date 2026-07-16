# Camassel 1988 to Laurenti 1990 Cd-rich specimen crosswalk

## Scientific question

Can the priority Laurenti Figure 2 temperature curves at `x = 0.970`, `0.955`, and `0.925` be assigned to specific specimens and given defensible 2 K anchors without treating fitted curves as observations?

Yes. Laurenti 1990 states that it reused the same cadmium-rich sample series as Camassel 1988. Camassel Table I identifies the specimens, growth methods, measured transverse exciton energies, estimated exciton binding energies, and derived interband gaps.

## Primary-source provenance

- Camassel et al., *Physical Review B* **38**, 3948-3959 (1988), DOI `10.1103/PhysRevB.38.3948`.
- Owner-supplied PDF SHA-256: `b499954072eaadbcb80c2cfabe42133051553e504896807bc9d8d61e4b328de4`.
- Laurenti et al., *Journal of Applied Physics* **67**, 6454-6460 (1990), DOI `10.1063/1.345119`.

Laurenti explicitly says it used the same LPE sample series as Ref. 5, which is Camassel 1988. The phrase “same series” must be interpreted together with Camassel Table I, which contains one bulk THM reference among the epitaxial samples.

## Resolved crosswalk

| Laurenti composition | Camassel specimen | Growth | Experimental transverse exciton energy at 2 K | Binding energy used | Derived interband gap |
|---:|---|---|---:|---:|---:|
| 0.970 | MCT 83 | LPE | 1.5315 eV | 9.0 meV, theoretical | 1.5405 eV |
| 0.955 | bulk reference | THM | 1.4992 eV | 8.7 meV, theoretical | 1.5079 eV |
| 0.925 | MCT 51 | LPE | 1.4416 eV | 8.2 meV, theoretical | 1.4498 eV |

The arithmetic closes exactly at printed precision:

```text
Eg = E_transverse + R_exciton.
```

## Correction to the open task wording

The previous shorthand “Laurenti Figure 2 LPE series x=.970, .955, .925” is inaccurate.

```text
x = 0.970: LPE
x = 0.955: bulk THM reference
x = 0.925: LPE
```

The corrected wording is:

```text
Cd-rich Laurenti temperature series at x=0.970, 0.955, and 0.925.
```

Growth method must remain a specimen-level field. The three curves must not be pooled as an all-LPE series.

## Observable boundary

Camassel's directly observed quantity for these rows is the transverse `n=1` exciton-polariton energy from reflectivity.

The tabulated interband gap is not a raw optical marker. It is obtained by adding a theoretical exciton binding energy estimated from a hydrogenic, three-band construction. Therefore:

- `E_transverse` is experimental;
- `R_exciton` is model derived for these rows;
- `Eg` is experimental plus model correction;
- the data class remains exciton-polariton reflectivity, not direct quasiparticle-gap measurement.

This distinction must survive any later benchmark ingestion.

## Uncertainty consequence

Camassel reports a standard composition accuracy of approximately `+/-0.5%`, or

```text
sigma_x approximately 0.005.
```

The paper also states that the gap changes by approximately 20 meV per composition percent in this region. The corresponding explanatory-variable uncertainty scale is therefore approximately

```text
20 meV/% * 0.5% = 10 meV.
```

Laurenti reports better than approximately 3 meV extraction accuracy for the fitted interband transition energy.

Thus the composition-induced energy scale is more than three times the stated spectral-extraction scale. Repeated temperatures from each curve must share one latent specimen composition rather than receiving independent composition errors.

## Scientific decision

```text
The three priority Laurenti curves now have specimen-level 2 K anchors.
The x=0.955 curve is a bulk THM reference, not LPE.
Composition uncertainty dominates the nominal spectral-extraction uncertainty.
The 2 K interband gaps remain exciton-model corrected.
```

This unblocks calibrated digitization, but it does not itself provide the higher-temperature Figure 2 observations.

## Digitization requirements now enabled

For each future digitized point:

1. preserve specimen ID and growth method;
2. use one shared latent composition for all temperatures from that specimen;
3. retain the 2 K Camassel anchor separately from digitized Laurenti points;
4. do not force the digitized 2 K point to equal the Camassel gap during extraction;
5. compare any extracted 2 K marker against both the experimental transverse energy and the model-corrected gap;
6. preserve a source-level digitization covariance or uncertainty;
7. do not mix the THM reference with the LPE subset in a growth-method holdout.

## Claim boundary

This result does not show that Hansen or Laurenti is superior. It does not provide independent validation of the Laurenti equation and does not identify a phonon scale. It is a provenance and uncertainty result that prevents an incorrect measurement-class and growth-method pooling decision.

## Reproduction

```bash
python tools/analyze_camassel1988_laurenti1990_crosswalk.py
```
