# Literature and Prior-Art Ledger

This file records claim-level evidence. Entries must distinguish what a source actually establishes from what this project infers.

## Evidence codes

- `E` — experimental evidence
- `T` — theoretical derivation
- `C` — first-principles computation
- `M` — model or parameterization
- `R` — review
- `PENDING` — metadata or full-text verification incomplete

## Core sources

### L001 — Hansen empirical HgCdTe gap relation

- **Citation:** G. L. Hansen, J. L. Schmit, and T. N. Casselman, “Energy gap versus alloy composition and temperature in HgCdTe,” *Journal of Applied Physics* 53, 7099 (1982).
- **Type:** `E`, `M`
- **Metadata status:** `PENDING` DOI and full-text verification.
- **Relevant equation:** commonly reported as

  $$
  E_g(x,T)= -0.302+1.93x-0.81x^2+0.832x^3
  +5.35\times10^{-4}T(1-2x).
  $$

- **What it supports:** a widely used empirical composition/temperature parameterization.
- **What it does not establish:** a first-principles decomposition of the temperature coefficient into electron–phonon and thermal-expansion contributions.
- **Required action:** obtain the original paper, reconstruct the dataset, definitions, valid range, weighting, and reported residuals.

### L002 — Standard 8-band Kane framework for HgTe/HgCdTe

- **Citation:** E. G. Novik et al., “Band structure of semimagnetic $\mathrm{Hg}_{1-y}\mathrm{Mn}_y\mathrm{Te}$ quantum wells,” arXiv:cond-mat/0409392.
- **URL:** https://arxiv.org/abs/cond-mat/0409392
- **Type:** `T`, `M`
- **What it supports:** explicit 8-band basis, Hamiltonian conventions, envelope-function implementation, and empirical temperature-dependent material parameters.
- **What it does not establish:** a first-principles AHC derivation of those finite-temperature parameters.
- **Project use:** basis conventions and matrix templates for projection.

### L003 — Temperature-driven bulk Kane fermions

- **Citation:** F. Teppe et al., “Temperature-driven massless Kane fermions in HgCdTe crystals: verification of universal velocity and rest-mass description,” arXiv:1602.05999.
- **URL:** https://arxiv.org/abs/1602.05999
- **Type:** `E`, `M`
- **Reported result relevant to this project:** the gap changes sign while the characteristic Kane velocity is reported as approximately

  $$
  v_K=(1.07\pm0.05)\times10^6\ \mathrm{m\,s^{-1}}
  $$

  over the investigated composition and temperature range.
- **What it supports:** the hypothesis that temperature changes the Kane mass primarily through $E_g$ rather than a large change in $v_K$.
- **What it does not establish:** that $P$ is exactly temperature independent, or that this remains true over the entire alloy range.
- **Project use:** independent validation observable and falsification target.

### L004 — Generalized AHC including wavefunction renormalization

- **Citation:** J.-M. Lihm and C.-H. Park, “Phonon-induced renormalization of electron wave functions,” arXiv:2003.01316.
- **URL:** https://arxiv.org/abs/2003.01316
- **Type:** `T`, `C`
- **What it supports:** matrix-valued electron–phonon self-energies, off-diagonal Debye–Waller terms, and treatment of temperature-driven topological changes where wavefunction renormalization matters.
- **Project use:** formal basis for projecting a finite-temperature self-energy into the Kane manifold.
- **Caution:** bulk zincblende symmetry still constrains which matrix elements survive at $\Gamma$.

### L005 — Polar long-range correction to band renormalization

- **Citation:** J. P. Nery and P. B. Allen, “Influence of Fröhlich polaron coupling on renormalized electron bands in polar semiconductors,” arXiv:1603.04269.
- **URL:** https://arxiv.org/abs/1603.04269
- **Type:** `T`, `C`
- **What it supports:** adiabatic Brillouin-zone integrations can require an explicit long-range Fröhlich correction in polar semiconductors.
- **Project use:** warning against an unqualified static AHC calculation for HgCdTe.
- **Required action:** determine the appropriate long-range polar treatment for narrow-gap, relativistic HgTe/CdTe and alloy calculations.

### L006 — Modern hybrid-functional/SOC HgCdTe alloy treatment

- **Citation:** W. Chen, G.-M. Rignanese, J. Liu, and G. Hautier, “Native point defects in HgCdTe infrared detector material: Identifying deep centers from first principles,” arXiv:2311.05283; later published in *Journal of Applied Physics*.
- **URL:** https://arxiv.org/abs/2311.05283
- **Type:** `C`
- **What it supports:** dielectric-dependent hybrid-functional calculations with spin–orbit coupling and an SQS representation for $\mathrm{Hg}_{0.75}\mathrm{Cd}_{0.25}\mathrm{Te}$; static bandgap trends across composition are discussed.
- **What it does not establish:** finite-temperature AHC-renormalized Kane parameters.
- **Project use:** static electronic-structure benchmark and alloy-supercell precedent.

### L007 — Foundational AHC temperature dependence

- **Citation:** P. B. Allen and V. Heine, “Theory of the temperature dependence of electronic band structures,” *Journal of Physics C: Solid State Physics* (1976).
- **Type:** `T`
- **Metadata status:** exact volume/pages/DOI to verify.
- **What it supports:** perturbative decomposition of finite-temperature electronic energy shifts into electron–phonon terms including Fan and Debye–Waller contributions.
- **Project use:** foundational derivation.

## Prior-art questions requiring targeted search

1. Has a full Fan + Debye–Waller calculation already been performed for bulk HgTe, CdTe, or HgCdTe?
2. Has any HgCdTe calculation used nonadiabatic AHC with spinor wavefunctions?
3. Has an electron–phonon self-energy been explicitly downfolded into an 8-band Kane Hamiltonian for HgCdTe?
4. Are finite-temperature values of $P$, $F$, or $\gamma_i$ available from experiment or first principles?
5. Has random-alloy broadening near the normal/inverted transition been treated through a spectral function rather than a scalar bowing equation?
6. Have published analytical equations separated constant-volume electron–phonon and quasiharmonic contributions?
7. Which historical datasets underlie the coefficients and claimed accuracy of the Hansen equation?

## Evidence table for current hypotheses

| Hypothesis | Supporting source | Contradicting source | Status |
|---|---|---|---|
| $|\Delta v_K/v_K|\ll|\Delta E_g/E_g|$ | L003 | none entered | plausible; unproved |
| Low-temperature gap should deviate from exact linearity | L004, L005, L007 establish nontrivial phonon occupation physics generally | HgCdTe-specific evidence pending | theoretical expectation |
| Standard one-$P$ Kane model may not be closed under temperature renormalization | L004 permits matrix/wavefunction renormalization | no HgCdTe calculation entered | open |
| Disorder may broaden the zero-gap transition | L006 establishes atomistic alloy treatment precedent | quantitative broadening source pending | open |

## Source-ingestion template

For each added paper, record:

```text
ID:
Full citation:
Persistent identifier:
Source type: E/T/C/M/R
Material and composition:
Temperature range:
Measured or calculated quantity:
Bandgap definition:
Main equations:
Main numerical results:
Uncertainty:
Assumptions:
What the paper supports:
What it does not support:
Data/code availability:
Relevance to novelty:
Open verification questions:
```