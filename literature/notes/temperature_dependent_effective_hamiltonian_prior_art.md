# Temperature-dependent effective-Hamiltonian prior art

## Scope

This note asks a narrower question than whether temperature-dependent HgCdTe band structures exist:

> Has prior work already derived a complete finite-temperature Kane or related low-energy Hamiltonian from a microscopic electron-phonon self-energy?

The answer is split by claim level.

## 1. Temperature-dependent 8-band Kane calculations in HgTe structures are established

Krishtopenko et al. (2016), *Pressure and temperature driven phase transitions in HgTe quantum wells*, use the full 8-band $k\cdot p$ basis containing $\Gamma_6$, $\Gamma_8$, and $\Gamma_7$ to calculate temperature- and pressure-driven phase diagrams in HgTe/CdHgTe quantum wells.

Their Hamiltonian contains

$$
E_c,\ E_v,\ \Delta,\ E_P,\ F,
\gamma_1,\gamma_2,\gamma_3,\kappa,
$$

together with deformation potentials, elastic constants, lattice constants, and valence-band offsets.

This establishes that the following claim is not novel:

> Insert temperature-dependent bulk material parameters into an 8-band Kane Hamiltonian and calculate temperature-dependent HgTe/HgCdTe heterostructure bands and topological transitions.

However, the parameter provenance is empirical or semi-empirical rather than a projection of a matrix electron-phonon self-energy. In the paper's parameter table, $E_P$, $F$, $\gamma_i$, $\kappa$, $\Delta$, and deformation potentials are treated as temperature-independent inputs; temperature enters mainly through empirical gap, valence-band-offset, lattice, and elastic-constant laws. The authors cite the experimentally near-constant Kane velocity as justification for temperature-independent $E_P$.

Therefore this work is a strong prior-art comparator but not an example of matrix-AHC-to-Kane downfolding.

## 2. Experimental temperature-dependent 8-band validation is established

Ikonnikov et al. (2016) and Marcinkiewicz et al. (2017) compare temperature-dependent magnetospectroscopy of HgTe quantum wells with realistic 8-band Kane calculations. The later work reports agreement over 2--150 K and identifies a temperature-driven topological transition near 90 K.

This establishes:

- temperature-dependent 8-band Kane modeling of HgTe structures;
- experimental validation through Landau-level transitions;
- temperature-dependent topological phase diagrams;
- the practical importance of gap, valence-band offset, lattice constant, and elastic constants.

It does not establish independent microscopic temperature renormalization of all non-gap Kane invariants.

## 3. Off-diagonal AHC and phonon-renormalized wavefunctions are established generally

Lihm and Park generalized Allen-Heine-Cardona theory to electron energies and wavefunctions, including diagonal and off-diagonal Debye-Waller self-energy. Their BiTlSe$_2$ demonstration follows a temperature-driven topological transition and calculates phonon-renormalized band structure and hidden spin polarization.

Thus the following general claims are established:

- matrix electron-phonon self-energy near a topological transition;
- phonon-induced wavefunction rotation;
- the need for off-diagonal self-energy when nearby bands mix;
- temperature-dependent effective electronic structure beyond diagonal energy shifts.

The remaining HgCdTe question is application and symmetry-resolved compression into the conventional 8-band Kane invariant set.

## 4. Phonon renormalization of Dirac velocity is established generally

First-principles electron-phonon self-energy calculations in graphene found a 4--8% reduction of the effective Dirac velocity. Therefore a claim that electron-phonon coupling can renormalize a linear-band velocity is not novel by itself.

For HgCdTe, the scientifically useful question is narrower:

$$
\delta P(T),\quad
\delta P_8(T),\quad
\delta P_7(T),
$$

and whether those changes are experimentally constrained by the approximately constant Kane velocity reported near the inversion transition.

## 5. Closest-prior-art decomposition

| Proposed result | Status after audit |
|---|---|
| temperature-dependent 8-band Kane calculation for HgTe/HgCdTe | established |
| empirical temperature-dependent gap and VBO inserted into 8-band Kane | established |
| temperature-driven HgTe quantum-well topological transition from 8-band Kane | established |
| off-diagonal AHC and wavefunction renormalization across a topological transition | established generally |
| electron-phonon renormalization of Dirac velocity | established generally |
| matrix AHC projected into the full conventional HgCdTe 8-band invariant set | not identified |
| independent $T$-dependent $E_g,\Delta,P,F,\gamma_1,\gamma_2,\gamma_3$ from one microscopic calculation | not identified |
| one-$P$ versus $P_8/P_7$ closure test under finite-temperature self-energy | not identified |
| uncertainty-qualified matrix-AHC-to-Kane projection for a disordered alloy | not identified |

## 6. Revised defensible contribution

The broad claim

> a temperature-dependent 8-band Kane model for HgCdTe

is not novel.

The narrower candidate contribution is

$$
\boxed{
\Sigma^{\mathrm{ep}}_{8\times8}(\mathbf k,\omega,T)
\longrightarrow
\{E_g,\Delta,P,F,\gamma_1,\gamma_2,\gamma_3\}(T)
}
$$

with:

1. a fixed and declared Kane convention;
2. gauge and symmetry control;
3. off-diagonal self-energy retained;
4. closure residuals against one-$P$ and two-$P$ models;
5. covariance propagated conditional on the estimated gauge;
6. comparison against empirical-temperature-input 8-band calculations;
7. held-out experimental constraints on gap, velocity, mass, and transition temperature.

## 7. Stop rule

Do not claim novelty from reproducing an HgTe quantum-well phase diagram with temperature-dependent empirical parameters.

A microscopic calculation becomes scientifically differentiating only if it resolves at least one quantity not already supplied by empirical 8-band work, for example:

- a statistically significant $\delta P$ or $P_8-P_7$;
- a non-gap contribution to $m^*(T)$;
- a temperature-dependent $\Delta$, $F$, or $\gamma_i$;
- off-diagonal mixing that changes an observable relative to an $E_g$-only model;
- a microscopic explanation of the HgTe endpoint sign problem.

## Primary sources audited

- S. S. Krishtopenko et al., *Phys. Rev. B* **94**, 245402 (2016), arXiv:1607.03083.
- A. V. Ikonnikov et al., *Phys. Rev. B* **94**, 155421 (2016), arXiv:1606.05485.
- M. Marcinkiewicz et al., *Phys. Rev. B* **96**, 035405 (2017), arXiv:1702.06869.
- J.-M. Lihm and C.-H. Park, *Phys. Rev. B* **101**, 121102(R), arXiv:2003.01316.
- C.-H. Park et al., *Phys. Rev. Lett.* **99**, 086804 (2007), arXiv:0707.1666.
