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

### L008 — Gauge construction for composite bands

- **Citation:** N. Marzari and D. Vanderbilt, “Maximally-localized generalized Wannier functions for composite energy bands,” *Physical Review B* 56, 12847 (1997); arXiv:cond-mat/9707145.
- **URL:** https://arxiv.org/abs/cond-mat/9707145
- **Type:** `T`, `M`
- **What it supports:** unitary gauge freedom inside a composite band subspace and systematic construction of a smooth localized gauge.
- **Project use:** conceptual basis for treating the projected Kane basis as a gauge-fixed composite subspace rather than a list of independently ordered eigenvectors.
- **What it does not establish:** the specific block-restricted $\Gamma_6\oplus\Gamma_8\oplus\Gamma_7$ alignment or the AHC-to-Kane closure metric developed here.

### L009 — Disentanglement of entangled bands

- **Citation:** I. Souza, N. Marzari, and D. Vanderbilt, “Maximally-localized Wannier functions for entangled energy bands,” *Physical Review B* 65, 035109 (2001); arXiv:cond-mat/0108084.
- **URL:** https://arxiv.org/abs/cond-mat/0108084
- **Type:** `T`, `M`
- **What it supports:** selection of an optimally connected low-energy subspace when target bands are entangled with remote states.
- **Project use:** required precursor if the HgTe/HgCdTe eight-state manifold cannot be isolated by energy alone over the fitting $\mathbf k$ window.
- **Caution:** subspace selection error must be propagated into principal-angle and Kane-parameter uncertainty.

### L010 — Nonadiabatic and polar convergence of AHC

- **Citation:** S. Poncé, Y. Gillet, J. Laflamme Janssen, A. Marini, M. Verstraete, and X. Gonze, “Temperature dependence of the electronic structure of semiconductors and insulators,” arXiv:1504.05992.
- **URL:** https://arxiv.org/abs/1504.05992
- **Type:** `T`, `C`, `R`
- **What it supports:** systematic $q$-mesh and broadening convergence analysis; in polar materials, the adiabatic band-edge integral remains divergent and requires nonadiabatic treatment.
- **Project use:** methodological basis for requiring dynamical denominators and explicit convergence/extrapolation for polar CdTe/HgTe.
- **What it does not establish:** convergence behavior for inverted HgTe specifically.

### L011 — EPW spinor and polar interpolation capability

- **Citation:** S. Poncé, E. R. Margine, C. Verdi, and F. Giustino, “EPW: Electron-phonon coupling, transport and superconducting properties using maximally localized Wannier functions,” arXiv:1604.03525; *Computer Physics Communications*.
- **URL:** https://arxiv.org/abs/1604.03525
- **Type:** `C`, `M`
- **What it supports:** Wannier interpolation of electron–phonon matrix elements, electronic self-energies and spectral functions, with spin–orbit coupling and long-range polar interpolation.
- **Project use:** candidate dense-grid and spectral-function engine after direct DFPT verification.
- **Caution:** EPW Fan/self-energy capability alone does not guarantee a complete Debye–Waller treatment for the final AHC gap model.

### L012 — Modern cross-code verification of AHC methods

- **Citation:** S. Poncé, J.-M. Lihm, and C.-H. Park, “Verification and Validation of zero-point electron-phonon renormalization of the bandgap, mass enhancement, and spectral functions,” *npj Computational Materials* 11, 117 (2025); arXiv:2410.14319.
- **URL:** https://arxiv.org/abs/2410.14319
- **DOI:** https://doi.org/10.1038/s41524-025-01587-5
- **Type:** `C`, `M`
- **What it supports:** cross-verification among ABINIT, Quantum ESPRESSO, EPW, and special-displacement approaches; agreement between DFPT AHC and Wannier-function perturbation theory; explicit comparison of real and imaginary self-energies and spectral functions.
- **Important result:** the Debye–Waller term is momentum dependent and simplified Luttinger-type approximations can affect mass enhancement.
- **Project use:** direct precedent for a two-implementation CdTe verification stage and for requiring momentum-dependent Debye–Waller contributions when extracting $F$ and $\gamma_i$.
- **What it does not establish:** the HgTe/HgCdTe finite-temperature Kane projection proposed here.

## Prior-art questions requiring targeted search

1. Has a full Fan + Debye–Waller calculation already been performed for bulk HgTe, CdTe, or HgCdTe?
2. Has any HgCdTe calculation used nonadiabatic AHC with spinor wavefunctions?
3. Has an electron–phonon self-energy been explicitly downfolded into an 8-band Kane Hamiltonian for HgCdTe?
4. Are finite-temperature values of $P$, $F$, or $\gamma_i$ available from experiment or first principles?
5. Has random-alloy broadening near the normal/inverted transition been treated through a spectral function rather than a scalar bowing equation?
6. Have published analytical equations separated constant-volume electron–phonon and quasiharmonic contributions?
7. Which historical datasets underlie the coefficients and claimed accuracy of the Hansen equation?
8. Which available code path supplies a complete, nonadiabatic, spinor Fan + Debye–Waller matrix self-energy for HgTe without a diagonal or Luttinger approximation?

## Evidence table for current hypotheses

| Hypothesis | Supporting source | Contradicting source | Status |
|---|---|---|---|
| $|\Delta v_K/v_K|\ll|\Delta E_g/E_g|$ | L003 | none entered | plausible; unproved |
| Low-temperature gap should deviate from exact linearity | L004, L005, L007, L010 establish nontrivial phonon occupation and convergence physics generally | HgCdTe-specific evidence pending | theoretical expectation |
| Standard one-$P$ Kane model may not be closed under temperature renormalization | L004 permits matrix/wavefunction renormalization | no HgCdTe calculation entered | open |
| Disorder may broaden the zero-gap transition | L006 establishes atomistic alloy treatment precedent | quantitative broadening source pending | open |
| Momentum-dependent Debye–Waller terms may renormalize effective masses and quadratic Kane parameters | L012 | HgCdTe-specific calculation pending | strong general-method evidence |
| Raw eigenvalue ordering is insufficient for stable Kane-state tracking | L008, L009 | none entered | established gauge/subspace principle |

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
