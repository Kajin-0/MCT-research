# Dingrong 1985 degenerate-carrier source audit

## Citation

Qian Dingrong, Tang Wenguo, Shen Jie, Chu Junhao, and Zheng Guozhen, “Infrared Absorption in In-Doped Degenerate Hg1-xCdxTe,” *Solid State Communications* **56**, 813–816 (1985).

DOI: `10.1016/0038-1098(85)90315-1`

## Source-established facts

The publisher abstract and the repository's earlier full-text audit establish:

- nominal alloy composition `x=0.19`;
- electron concentration approximately `7.0e17 cm^-3`;
- reported temperature range approximately `77-300 K`;
- reported wavelength range approximately `7-17 um`;
- experimental and theoretical treatment of the absorption edge and below-gap absorption;
- use of a Burstein-Moss interpretation for the degenerate edge;
- adaptation of free-carrier absorption theory developed for InSb;
- use of a two-mode Callen effective charge to represent HgCdTe optical phonons;
- good reported agreement for the below-gap absorption spectra;
- fitted ionized-impurity concentration approximately `3.4e18 cm^-3`.

## Physical role in the flagship model

The source provides a high-density validation regime in which the optical edge cannot be treated as a composition- and temperature-only latent gap.

The source requires one forward chain to contain both:

```text
occupied-state interband threshold
+
free-carrier below-gap absorption
```

while preserving their distinct mechanisms.

## Current executable scope

The first repository implementation includes:

- zero-temperature density-to-Fermi-wavevector mapping;
- a declared Kane-type nonparabolic conduction dispersion;
- parabolic valence recoil at the same transition wavevector;
- independent band-gap-renormalization and observation shifts;
- local identifiability diagnostics for density-series optical edges.

It does not yet implement:

- the source's complete temperature-dependent carrier statistics;
- the full free-carrier absorption equations;
- two-mode phonon scattering coefficients;
- ionized-impurity scattering amplitudes;
- source-native temperature-dependent masses and dielectric constants;
- a digitized source spectrum.

## Key source boundary

The paper studies one heavily doped specimen. It can demonstrate that carrier filling matters, but it cannot identify a universal correction applicable to low-density detector absorbers.

The reported optical edge may include:

$$
E_{\mathrm{opt}}
=E_g^{(0)}
+\Delta E_{\mathrm{BM}}
+\Delta E_{\mathrm{BGR}}
+\Delta E_{\mathrm{tail}}
+\Delta E_{\mathrm{operator}}.
$$

The source does not justify collapsing these terms into one composition-only gap.

## Authorized use

- validation anchor for the high-density carrier-filled branch;
- proof-of-need for nonparabolic state filling;
- requirement that free-carrier absorption and edge filling share one carrier-state record;
- test case for density, temperature, and impurity provenance;
- prior-art boundary against claiming Burstein-Moss filling in HgCdTe as new.

## Unauthorized inference

- assigning the source correction to low-density HgCdTe detectors;
- treating `7.0e17 cm^-3` as a universal degeneracy threshold;
- inferring the zero-density material gap directly from the reported optical edge;
- treating the ionized-impurity concentration as equal to the mobile-electron concentration;
- conflating free-carrier absorption with the interband edge;
- claiming a full source reproduction from the current bounded sensitivity model.

## Missing information for full reproduction

1. source-native numerical spectra or an auditable high-resolution digitization;
2. complete transcription of all equations and parameter tables;
3. temperature-resolved bandgap and effective-mass conventions;
4. dielectric and two-mode optical-phonon parameters;
5. absorption inversion and sample-thickness details;
6. uncertainty on density, composition, and fitted impurity concentration;
7. exact edge coordinates used in the Burstein-Moss comparison.

Until these are recovered, the Dingrong branch remains a high-density sensitivity and identifiability result rather than an external numerical validation.
