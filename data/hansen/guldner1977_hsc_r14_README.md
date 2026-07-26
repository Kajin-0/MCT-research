# Guldner et al. 1977 HSC_R14 primary-source audit

## Source

Y. Guldner, C. Rigaux, A. Mycielski, and Y. Couder, "Magnetooptical Investigation of Hg1-xCdxTe Mixed Crystals. I. Semimetallic Configuration," *physica status solidi (b)* **81**, 615-627 (1977), DOI `10.1002/pssb.2220810225`.

The repository owner supplied the complete thirteen-page article as `guldner1977(1).pdf`. The observed binary SHA256 is:

```text
e460fcc11e7627b1a3ec7346483bf88494b18e4fb69272b2af7e6ab61da3ef5b
```

The copyrighted PDF is not committed.

The primary article corrects Hansen's printed author list: the third author is **A. Mycielski**, not M. Grynberg.

## Measurement class

This source is a genuine 4.2 K magnetooptical experiment. It combines:

- interband magnetoabsorption from `120` to `370 meV` in fields to `60 kG`;
- submillimeter and far-IR magnetotransmission below `16 meV` in fields to `50 kG`;
- Faraday geometry with circular polarization;
- Voigt geometry with linear polarization parallel and perpendicular to the field;
- magnetic-field sweeps at fixed photon energy.

The same unoriented alloy samples are used across the two spectral regions. The direct observations are transmission minima and resonance fields. Interaction gaps and other band parameters are obtained from the zero-field convergence and Pidgeon-Brown interpretation of transition series.

## Material and specimen provenance

P-type ingots were grown by a modified Bridgman method. Slices were polished, bromine-methanol etched, and annealed in saturated mercury vapor to reduce mercury vacancies and produce nearly intrinsic material at `4.2 K`. The empirical annealing prescription is:

```text
Ta(deg C) = 180 + 400 x
```

IR transmission specimens were about `2 um` thick and mounted freely between sapphire or calcium-fluoride plates to avoid strain.

No source-native specimen identifiers, composition measurement method, or composition uncertainty are printed. Five composition groups with numerical interaction gaps are traceable:

```text
x approximately 0.010
x = 0.025
x = 0.050
x approximately 0.105
x approximately 0.115
```

The exact physical specimen count and cross-figure specimen linkage remain unresolved. The low-composition samples have electron concentration approximately `1-2 x 10^15 cm^-3`; the `x approximately 0.115` group is reported in the `1-2 x 10^16 cm^-3` range.

## Source-native interaction-gap candidates

The source defines the interaction gap as

```text
epsilon0 = E_Gamma6 - E_Gamma8
```

and states that it is directly obtained from the convergence region of the interband Gamma6-to-Gamma8 transition energies. The remaining Kane and Luttinger parameters are obtained by fitting transition energies.

Five scalar 4.2 K candidates are printed:

```text
x approximately 0.010   epsilon0 = -285 meV
x = 0.025               epsilon0 = -261 meV
x = 0.050               epsilon0 = -207 meV
x approximately 0.105   epsilon0 = -110 meV
x approximately 0.115   epsilon0 =  -90 meV
```

No pointwise gap uncertainty or covariance is reported. These are source-native, model-assisted magnetooptical interaction-gap determinations, not raw transmission observables.

The plotted experimental transition points and theoretical curves in Figures 3, 5, 6, and 7 are not digitized. No theoretical curve is converted into pseudo-data.

## Resonant acceptors are a separate evidence layer

The paper separates intrinsic interband transitions from broader impurity transitions involving resonant acceptor states.

For `0 <= x <= 0.06`, the A1 state has:

```text
EA1(H=0) = 2.5 +/- 0.3 meV
field coefficient approximately +0.25 meV/T
```

It is nearly composition independent in this range and is attributed to a mercury vacancy. A lower A0 state is estimated at approximately `0.8 meV` at zero field.

For `x approximately 0.115`, with `epsilon0=-90 meV`, the A1 state has:

```text
EA1(H=0) = 5.5 +/- 0.5 meV
field coefficient approximately +0.5 meV/T
```

Figure 9 plots acceptor binding energy against interaction gap using magnetooptical and external transport points. The figure is not digitized and does not authorize a pointwise intrinsic-gap ledger. Acceptor binding energies are not intrinsic bandgaps.

## Band parameters and uncertainty semantics

The Pidgeon-Brown model depends on interaction gap, Kane energy, spin-orbit splitting, and modified Luttinger parameters. The audit preserves the printed constraints:

```text
Delta = 1 eV                         fixed and composition independent
gamma1 = 4.5 +/- 1.5
kappa = -1 +/- 0.5
gamma1 - 2 gamma = 2.5 +/- 0.5
m_h*/m0 = 0.4 +/- 0.1
Ep(HgTe) = 18 eV                     printed starting value
```

`Ep` rises rapidly over approximately `-300 < epsilon0 < -200 meV` and varies more slowly for larger epsilon0, but individual alloy values are not printed in Part I. The source identifies neglected valence-band warping as the main uncertainty in `gamma` and the heavy-hole mass.

The model also neglects inversion asymmetry, Gamma8 anisotropy, and Kane `F` and `G` matrix elements in its principal calculation. An observed `Delta n=-3` transition is noted as possibly caused by inversion asymmetry, and a roughly `1 meV` anomaly near a `16.5 meV` LO-phonon resonance is reported without a definitive interpretation.

## Part I versus Part II boundary

Part I states that Part II contains:

- the interaction-gap relation `epsilon0(x)` over `0 <= x <= 0.3` in Figure 11;
- the Kane-energy dependence on interaction gap in Figure 12;
- semiconducting-region and transition-region results.

Those figures and their data are **not present in the HSC_R14 article**. They are cross-source references to HSC_R15 and are not reconstructed here. Specimen identity between Parts I and II remains unresolved.

## Hansen HSC_R14 boundary

Hansen does not expose source-labelled HSC_R14 markers. It is unclear whether Hansen ingested:

- the five printed Part I scalar interaction gaps;
- selected transition-derived points;
- a relation or ledger from Part II;
- or another transcription.

```text
controlling decision
primary_source_recovered_semimetallic_magnetotransmission_gap_candidates_reconstructed_part_ii_relation_and_hansen_marker_mapping_unresolved
```

Guldner 1977 belongs to Hansen's fitted lineage and cannot independently validate Hansen's empirical relation.

## Authorized and prohibited uses

Authorized:

- retain the five printed 4.2 K interaction-gap candidates with their composition precision qualifiers;
- retain sample preparation, spectral regions, geometry, field range, and carrier-density ranges;
- preserve the printed band-parameter constraints and their uncertainty semantics;
- preserve A0 and A1 acceptor records as a separate impurity evidence layer;
- record Part II references without importing Part II values.

Not authorized:

- invent composition uncertainties, specimen identifiers, or cross-figure specimen linkage;
- treat acceptor binding energies as intrinsic gaps;
- digitize Figure 9 or theoretical curves without an explicit resolution gate;
- import Figure 11 or Figure 12 values from Part II into HSC_R14;
- invent pointwise covariance or statistical confidence intervals;
- assign Hansen markers by plot proximity;
- use this fitted-lineage source as independent validation;
- construct a production HgCdTe bandgap relation from this source alone.
