# Aliev et al. 1970 HSC_R12 primary-source audit

## Source

E. M. Aliev, S. A. Aliev, T. G. Gadzhiev, and M. I. Aliev, "Electron Effective Mass in the Hg1-xCdxTe System," *physica status solidi* **40**, K41-K44 (1970), DOI `10.1002/pssb.19700400238`.

The repository owner supplied the complete four-page article as `aliev1970.pdf`. The observed binary SHA256 is:

```text
be08dc3f926a42f7549b1a7734337fd72701cbcec3d3759373eed772006e44bf
```

The copyrighted PDF is not committed.

## Corrected measurement classification

Hansen grouped HSC_R12 with magneto-optical gap evidence. The primary source is not optical. It reports strong-field thermomagnetic transport on polycrystalline n-type Hg1-xCdxTe at 300 K.

The measured quantities are thermoelectric power and Hall coefficient in strong magnetic field. The transverse Nernst-Ettingshausen effect is used as a consistency check. These observations are converted into conduction-band effective masses through Fermi-integral and Kane-model relations.

No direct optical absorption edge, magnetoreflection resonance, or independent scalar bandgap measurement is reported.

## Material and population provenance

The alloys were prepared by melting the initial components for `0 <= x <= 0.2`. Composition determination and composition uncertainty are not stated.

Table 1 contains eleven carrier-density records:

```text
x = 0.05   one row
x = 0.10   seven rows
x = 0.14   one row
x = 0.15   one row
x = 0.20   one row
```

The text says the number of specimens at `x=0.05`, `0.15`, and `0.20` was limited. It does not identify individual specimens or establish whether the seven `x=0.10` density states are seven physical specimens, multiple states of fewer specimens, or another grouping. Repository record IDs are therefore audit surrogates only.

HgTe (`x=0`) concentration-dependent mass data are taken from the authors' preceding paper and are not reconstructed as observations of this source.

## Table 1 reconstruction

Table 1 prints carrier density, adopted signed gap, high-field thermoelectric power, theoretical and source-labelled experimental band-edge mass, and theoretical and source-labelled experimental conduction-band mass.

The eleven rows are transcribed exactly. The `exp.` labels are preserved, but these quantities are derived through the paper's transport and band-model inversion. They are not raw observables and have no reported covariance.

## Gap provenance: the central audit result

The Table 1 gap values are not independent measurements made by Aliev et al. The paper explicitly states that the following empirical expression was used to determine `epsilon_g`:

```text
epsilon_g(x,T) = -0.3 + 5e-4 T + [1.91 - 1e-3 T] x  eV
```

At 300 K this becomes:

```text
epsilon_g(x,300 K) = -0.15 + 1.61 x  eV
```

The Table 1 values are its rounded evaluations:

```text
x=0.05  -0.07 eV
x=0.10  +0.01 eV
x=0.14  +0.07 eV
x=0.15  +0.09 eV
x=0.20  +0.17 eV
```

Equation 3 is attributed to reference 7, Wiley and Dexter (1969). Equation 4, `Ep=(18+3x) eV`, is likewise an adopted model input. Consequently, the table cannot be treated as five or eleven independent Aliev bandgap observations.

Figure 1 for `x=0.10` shows a transformed mass quantity versus `n^(2/3)`. The authors state that the linear extrapolation permits determination of the band-edge mass and energy gap and that both are nearly zero. No separate numerical intercept-derived gap or uncertainty is printed. The only numerical value in Table 1 remains the Equation 3 input `+0.01 eV`.

## Mass model

Equation 2 is a Kane nonparabolic dispersion relation:

```text
m*/m0 = [1 + (2/3) * ((|epsilon_g|/Ep)^2
         + 4 hbar^2 K^2/(3 m0 Ep))^(-1/2)]^(-1)
```

At `K=0`, it gives the theoretical band-edge mass. The use of `|epsilon_g|` means this mass relation does not determine the sign of the gap.

The paper assumes a spherical isoenergetic surface and a degenerate electron gas, with `K^2=(3 pi^2 n)^(2/3)`. Equation 1 converts thermopower and density to a band-edge mass using Fermi integrals and `delta=k0T/epsilon_g`.

The source reports no pointwise covariance, cross-density covariance, composition uncertainty, or statistical confidence intervals.

## Hansen HSC_R12 boundary

Traceable candidates are the five distinct Equation 3 gap values at 300 K and the qualitative near-zero statement for the `x=0.10` Figure 1 intercept.

Hansen does not expose source-labelled HSC_R12 markers and does not state whether it ingested the five unique table gaps, duplicated all eleven rows, selected effective-mass-derived points, or used another transcription.

Because the numerical gaps are inherited from a relation already attributed to Wiley and Dexter, treating them as independent fitted evidence would create lineage duplication.

```text
controlling decision
primary_source_recovered_thermomagnetic_effective_mass_table_reconstructed_gap_values_are_adopted_wiley_dexter_equation_inputs_hansen_marker_mapping_unresolved
```

Aliev 1970 belongs to Hansen's fitted lineage and cannot independently validate Hansen's empirical relation.

## Authorized and prohibited uses

Authorized:

- retain the eleven 300 K thermomagnetic/effective-mass records with composition and density attached;
- use the source as evidence for the Kane-model mass-versus-density treatment;
- preserve the qualitative near-zero result near `x=0.10`;
- track the five distinct Equation 3 values as possible Hansen ingestion candidates;
- flag the Wiley-Dexter equation lineage explicitly.

Not authorized:

- treat the Table 1 gap column as independent Aliev gap measurements;
- count the seven `x=0.10` rows as seven independent gap observations;
- infer composition uncertainty or physical specimen count;
- invent covariance or statistical errors;
- digitize Figure 2 theoretical curves as observations;
- assign Hansen markers by plot proximity;
- use this fitted-lineage source as independent validation;
- construct a production HgCdTe bandgap relation from this source alone.
