# Primary-source audit for the distributional band-edge program

## Scope

This note records the first six full-text sources activated for issue #167. It separates source-established claims from project inferences and defines the role each source may play in the flagship forward model.

No source below independently identifies a universal mapping among composition variance, local-gap variance, Urbach energy, PL width, quasiparticle linewidth, and detector cutoff.

## S. Wu (1983): alloy-fluctuation contribution to bowing

**Citation:** S. Wu, “On the Energy Bandgap Bowing in Hg1-xCdxTe,” *Solid State Communications* 48, 747–749 (1983).  
**DOI:** `10.1016/0038-1098(83)91009-8`  
**Type:** theoretical/model, with comparison to experimental gap trends.

### Source-established content

- The virtual-crystal pseudopotential construction produces an approximately linear composition trend before disorder corrections.
- A second-order perturbative alloy-fluctuation potential is constructed from cation and anion disorder contributions.
- The calculated composition dependence is interpreted through band mixing and the changing inverted-to-normal band structure.
- The paper concludes that alloy fluctuation potential is an important contribution to HgCdTe bandgap bowing.

### Limitations

- The treatment uses empirical pseudopotential form factors and interpolation assumptions.
- Lattice relaxation and other effects are excluded from the final interpretation.
- The model does not provide a modern specimen-specific probability distribution of local gaps.
- The calculation does not define an optical, PL, detector, or magneto-optical observation operator.

### Authorized project use

- Microscopic motivation for separating virtual-crystal mean structure from disorder-induced corrections.
- Prior-art boundary against claiming that disorder-based bowing is new.
- Qualitative guidance that the disorder correction may change character across the inverted/normal composition range.

### Unauthorized inference

- Equating Wu's bowing correction with an Urbach energy or local-gap standard deviation.
- Treating the 1983 calculation as a quantitatively transferable modern disorder model.

## Qian Dingrong et al. (1985): degenerate carrier-filled absorption

**Citation:** Qian Dingrong, Tang Wenguo, Shen Jie, Chu Junhao, and Zheng Guozhen, “Infrared Absorption in In-Doped Degenerate Hg1-xCdxTe,” *Solid State Communications* 56, 813–816 (1985).  
**DOI:** `10.1016/0038-1098(85)90315-1`  
**Type:** experimental and theoretical.

### Source-established content

- The studied material has nominal `x=0.19` and approximately temperature-independent electron concentration `n=7.0e17 cm^-3` over the reported range.
- Transmission spectra cover approximately 7–17 micrometres from 77 to 300 K.
- Below-gap absorption is modeled using phonon and ionized-impurity scattering, including the two-mode optical-phonon character of HgCdTe.
- The fitted ionized-impurity concentration is approximately `3.4e18 cm^-3`.
- The observed optical edge is interpreted using a Burstein-Moss construction in which the transition terminates at occupied-state boundaries rather than at the unfilled band extrema.

### Limitations

- One heavily doped specimen cannot establish a universal carrier correction.
- The composition, optical constants, and band model are source-conditioned.
- The reported agreement does not separate Burstein-Moss shift from every possible many-body or tail contribution.

### Authorized project use

- High-density validation case for the carrier-filled branch of the forward model.
- Evidence that `E_opt` can differ substantially from the latent zero-density `Eg`.
- Test case for maintaining free-carrier absorption and edge filling in one spectrum.

### Unauthorized inference

- Applying the source correction to low-density detector absorbers without a carrier-statistics calculation.
- Treating the measured optical edge as a direct composition-only bandgap.

## K. H. Herrmann, K.-P. Möllmann, and J. W. Tomm (1992): multimodal broadening

**Citation:** K. H. Herrmann, K.-P. Möllmann, and J. W. Tomm, “Broadening Mechanisms Near the E0 Transition in Narrow-Gap Hg1-xCdxTe (0.2 < x < 0.6),” *Journal of Crystal Growth* 117, 758–762 (1992).  
**DOI:** `10.1016/0022-0248(92)90851-9`  
**Type:** experimental and semi-empirical model.

### Source-established content

- Near-edge transmittance, photoconductive, and luminescence measurements are treated in a common semi-empirical framework.
- The below-gap absorption follows an exponential law over more than three decades in high-quality specimens.
- The reported tail parameter contains permanent and temperature-dependent contributions.
- Convolution of the above-gap response with a Gaussian-like gap distribution produces an approximately exponential tail over a relevant absorption interval.
- The paper distinguishes alloy/gap-fluctuation broadening, temperature-dependent broadening, and shallow-level contributions, including Hg-vacancy-related levels.
- One illustrated luminescence fit uses a broadening energy represented as approximately `1.2 meV + 0.5 kT`.

### Limitations

- The full executable high-energy branch depends on Anderson formulas and source-specific band-filling conventions.
- The Gaussian-gap convolution is an explanatory model, not a unique inversion of composition variance.
- Shallow levels and excitonic contributions prevent one-parameter interpretation of all spectra.

### Authorized project use

- Primary prior art for the noncommutation between local-gap averaging and edge extraction.
- Target for reproducing the Gaussian-gap-to-exponential-tail mapping.
- Cross-modal test case because absorption, photoconductivity, and luminescence are treated together.

### Unauthorized inference

- Directly setting the Urbach parameter equal to a composition-induced gap standard deviation.
- Using the incomplete recovered equations as a production operator before all external definitions are audited.

## V. I. Ivanov-Omskii et al. (2009): processing-conditioned PL disorder proxy

**Citation:** V. I. Ivanov-Omskii et al., “Study of Alloy Disorder in (Hg,Cd)Te with the Use of Infrared Photoluminescence,” *Physica B* 404, 5035–5037 (2009).  
**DOI:** `10.1016/j.physb.2009.08.210`  
**Type:** experimental and model-based inference.

### Source-established content

- MBE HgCdTe specimens with nominal `x=0.38` and `x=0.57` were studied from 4.2 to 300 K in as-grown, Hg-vapor-annealed, and He-annealed states.
- The PL peak is red-shifted from the expected band-to-band maximum and the shift grows as temperature decreases.
- The interpretation is exciton localization at compositional fluctuations.
- The reported table gives, for `x=0.38`, fluctuation measures of 17, 13, and 14 meV for as-grown, Hg-annealed, and He-annealed states, with PL FWHM values 18, 10, and 14 meV.
- For `x=0.57`, the corresponding fluctuation measures are 90, 60, and 60 meV, with FWHM values 30, 16, and 18 meV.
- Post-growth annealing reduces the inferred disorder measure.

### Limitations

- The inferred fluctuation parameter is obtained through a PL localization model and a selected comparison temperature.
- Annealing also changes inferred composition and defect state.
- At `x=0.57`, the inferred fluctuation scale, cutoff parameter, and FWHM differ substantially, showing that the observables are not interchangeable.

### Authorized project use

- Processing-state validation case for PL displacement and linewidth.
- Direct evidence that a single nominal composition does not fix the optical emission observable.
- Falsification target for any one-parameter distribution model.

### Unauthorized inference

- Calling the tabulated fluctuation measure a direct composition standard deviation.
- Attributing every annealing change solely to alloy homogenization.

## Y. Chang et al. (2007): nonparabolic intrinsic absorption, Urbach tail, and cutoff geometry

**Citation:** Y. Chang et al., “Absorption of Narrow-Gap HgCdTe Near the Band Edge Including Nonparabolicity and the Urbach Tail,” *Journal of Electronic Materials* 36, 1000–1006 (2007).  
**DOI:** `10.1007/s11664-007-0162-0`  
**Type:** experimental and analytical model.

### Source-established content

- The model combines nonparabolic conduction/light-hole bands, a parabolic heavy-hole band, and an Urbach tail.
- It is reported to fit absorption from the tail region to at least 300 meV above the gap for the studied narrow-gap regime.
- The experimental focus is high-quality MBE LWIR HgCdTe near `x=0.21–0.23` and approximately 77 K.
- Transmissivity and photoconductivity were measured at the same specimen locations.
- Static disorder dominates the low-temperature Urbach energy, while structural disorder depends on growth, substrate, processing, crystalline quality, and doping.
- The detector 50% cutoff depends on effective absorber thickness; reducing effective thickness shifts the response cutoff to higher absorption coefficients and shorter wavelengths.
- Burstein-Moss effects are excluded from the main low-density regime but are expected at high temperature or heavy doping.

### Limitations

- The source domain is narrow and does not justify unrestricted transfer across composition and temperature.
- The reported Urbach energy combines static and dynamic contributions.
- Native numerical spectra and every same-specimen fitted parameter are not available in the repository.

### Authorized project use

- Above-gap nonparabolic absorption branch.
- Source-specific tail/intrinsic continuity model.
- Geometry-dependent detector-cutoff operator.
- Low-density contrast to the Dingrong degenerate case.

### Unauthorized inference

- Treating a detector cutoff as a direct material gap.
- Transferring one fitted `W` or band parameter to another specimen without provenance.

## F. Teppe et al. (2016): temperature-driven near-critical Kane target

**Citation:** F. Teppe et al., “Temperature-Driven Massless Kane Fermions in HgCdTe Crystals,” *Nature Communications* 7, 12576 (2016).  
**DOI:** `10.1038/ncomms12576`  
**Type:** experimental and simplified Kane-model inference.

### Source-established content

- Magneto-optical transmission is used to follow HgCdTe band-structure evolution with temperature and field.
- Sample B has nominal `x=0.155` and crosses the inverted/normal transition near `Tc≈77 K`.
- The inferred Kane rest mass changes sign through the transition.
- The reported characteristic velocity is approximately `(1.07 ± 0.05)e6 m/s` over the investigated compositions and temperatures.
- The paper explicitly states that inherent Cd-composition fluctuations impede fine tuning by composition, motivating temperature as the tuning coordinate.

### Limitations

- The extracted gap and mass are conditioned on a simplified Kane/Landau-level model.
- Nominal composition does not include a specimen-resolved composition distribution.
- Local composition variation does not by itself determine the bulk topological invariant.

### Authorized project use

- Near-critical validation target for transition-width propagation.
- Test of the constant-velocity null model.
- Magneto-optical observation class for comparison with absorption and PL operators.

### Unauthorized inference

- Treating the nominal composition label as exact.
- Interpreting a local opposite-sign probability as direct evidence for mixed topological domains without a spatial or spectral model.

## Cross-source synthesis

The six sources define a coherent forward chain:

```text
alloy potential and bowing                    Wu 1983
composition/gap distribution -> tail          Herrmann 1992
carrier filling and free-carrier absorption   Dingrong 1985
processing-dependent PL localization          Ivanov-Omskii 2009
Kane + Urbach + thickness response             Chang 2007
near-critical magneto-optical mass             Teppe 2016
```

The project-level novelty target is not any individual mechanism. It is a validated distributional model that keeps these mechanisms and observation operators distinct while predicting when their reported gaps agree, diverge, or become non-identifying.

## Immediate acquisition gaps

1. Native numerical Chang absorption and same-specimen fitted parameter records.
2. Complete Herrmann/Anderson executable definitions and carrier-to-quasi-Fermi mapping.
3. Digitizable Dingrong edge and table values with uncertainty.
4. Teppe supplementary composition and fit covariance details.
5. The Ivanov-Omskii localization equation lineage and its sensitivity to the selected latent gap law.
6. Spatial composition-variance or correlation-length data suitable for distinguishing metrology uncertainty from microscopic disorder.
