# Seiler 1990 TPMA provenance audit

## Scientific question

Which Seiler two-photon magnetoabsorption results can independently constrain the low-temperature composition dependence of the HgCdTe gap, and which results are circular or incompletely sourced?

## Primary source

D. G. Seiler, J. R. Lowney, C. L. Littler, and M. R. Loloee, *Journal of Vacuum Science & Technology A* **8**, 1237-1244 (1990), DOI `10.1116/1.576952`.

Owner-supplied PDF SHA-256:

```text
5bc624ca8292fcba72ae55d13c5be03d07af03b57afc4584c2314ca08e459a49
```

## Table I sample provenance

| Sample | x | Composition source | Independent for an Eg(x) test? |
|---:|---:|---|---|
| 1 | 0.239 | Honeywell infrared-cutoff assignment | No |
| 2 | 0.253 | Eg measured, then x assigned using HSC | No |
| 3 | 0.259 +/- 0.0015 | Cominco value tied to wet chemistry | Yes |
| 4 | 0.277 +/- 0.0010 | Cominco value tied to wet chemistry | Yes |
| 5 | 0.300 +/- 0.0035 | Cominco value tied to wet chemistry | Yes |

Seiler explicitly excludes sample 2 from the composition-dependence analysis because its composition was inferred from the measured gap through the HSC relation. It cannot then be used as independent evidence for HSC or any competing composition law.

Sample 1 is less strongly circular but still not independently calibrated: its composition came from an infrared cutoff assignment. It must remain excluded from a strict independent-composition score.

## Table II transcription

Table II contains 18 low-temperature magneto-optical gap values:

| Measurement class | Rows |
|---|---:|
| Interband magnetoabsorption | 11 |
| Electron spin resonance | 1 |
| Cyclotron, combined, and cyclotron-phonon resonance | 1 |
| Four-photon mixing with ESR analysis | 1 |
| Present-work two-photon magnetoabsorption | 4 |

The table is a selected historical compilation, not one homogeneous experiment. The fourteen literature rows retain unresolved composition provenance until their original sources are audited.

The four present-work TPMA rows map to samples 1, 3, 4, and 5:

| Sample | x | Eg | Direct Eg uncertainty | Composition status |
|---:|---:|---:|---:|---|
| 1 | 0.239 | 122 meV | 1 meV | cutoff derived, not independent |
| 3 | 0.259 +/- 0.0015 | 158.5 meV | 1 meV | wet-chemistry tied |
| 4 | 0.277 +/- 0.0010 | 195 meV | 1 meV | wet-chemistry tied |
| 5 | 0.300 +/- 0.0035 | 224 meV | 2 meV | wet-chemistry tied |

Thus only three present-work points are admissible as independently composition-calibrated TPMA anchors.

## Observable boundary

TPMA is substantially cleaner than a conventional absorption-edge definition because the resonant transitions occur between quantized Landau levels and excitonic corrections are reported to be small.

Nevertheless, the tabulated gap is not a raw marker. Seiler determines `Eg` by fitting the transition energies with a modified Pidgeon-Brown band model while holding a published set of other band parameters fixed. The correct measurement class is therefore:

```text
two-photon magnetoabsorption, model-inferred signed gap
```

It must remain distinct from detector cutoff, ordinary absorption edge, excitonic transition, and modern simplified-Kane Landau-level fits.

## Composition-uncertainty scale

For a local diagnostic only, propagate each reported `sigma_x` through the derivative of the published Hansen equation:

```text
dEg/dx = 1.93 - 1.62x + 2.496x^2 - 2(5.35e-4)T.
```

Over the Table II present-work temperature range of 2-10 K:

| Sample | Composition-induced sigma(Eg) | Reported direct sigma(Eg) |
|---:|---:|---:|
| 3 | 2.501-2.514 meV | 1 meV |
| 4 | 1.662-1.671 meV | 1 meV |
| 5 | 5.803-5.833 meV | 2 meV |

The Hansen derivative is used only as a local sensitivity scale; this calculation does not validate Hansen.

For every independently calibrated TPMA anchor, the composition contribution exceeds the quoted direct gap uncertainty. Any benchmark that scores only the vertical error bars will be overconfident.

## Temperature-series admissibility

The composition provenance restriction differs between two scientific questions:

### Composition-law validation

Use only samples 3, 4, and 5 among Seiler's present-work TPMA results.

Do not use:

- sample 1, because x is cutoff derived;
- sample 2, because x was assigned using HSC.

### Within-specimen temperature shape

All five specimens may potentially constrain temperature dependence, provided that:

1. each specimen keeps one shared composition assignment across all temperatures;
2. sample 2 is not scored as independent evidence for the composition dependence;
3. source-level and digitization uncertainties are retained;
4. the plotted fitted equation is not sampled and relabeled as experimental data.

This distinction makes Figure 7 worth digitizing even though sample 2 is circular for an `Eg(x)` benchmark.

## Scientific decision

```text
Seiler contributes three independently composition-calibrated present-work TPMA anchors: x=0.259, 0.277, and 0.300.

The x=0.239 point and x=0.253 specimen cannot independently validate a composition law.

Composition uncertainty exceeds the quoted direct gap uncertainty for all three independent anchors.
```

The paper strongly supports low-temperature nonlinearity and a vanishing slope as `T -> 0`, but its proposed analytical equation remains an empirical fit and is not itself an observation.

## Next evidence task

Digitize the repeated-temperature measurements in Seiler Figure 7 by specimen. Preserve the specimen grouping and composition covariance, and exclude sample 2 from any composition-law score while retaining it for temperature-shape tests.

## Claim boundary

This audit does not establish that Seiler's equation is superior to Hansen or Laurenti. It does not merge the five magneto-optical classes into one likelihood and does not audit the original composition provenance of the fourteen literature points.

## Reproduction

```bash
python tools/analyze_seiler1990_tpma_provenance.py
```
