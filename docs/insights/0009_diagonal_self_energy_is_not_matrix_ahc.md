# Insight 0009 — A diagonal self-energy table cannot validate a finite-temperature Kane Hamiltonian

**Status:** exact information-content statement and enforced conversion rule  
**Novelty:** not claimed  
**Importance:** prevents scalar output from being overinterpreted as matrix AHC

## Statement

Suppose a code reports only diagonal self-energy elements

$$
\Sigma_{nn}(\mathbf k,\omega,T).
$$

These values can determine band-energy shifts in a declared basis or eigenstate gauge, subject to the approximations used. They do not determine the off-diagonal elements

$$
\Sigma_{mn}(\mathbf k,\omega,T),\qquad m\ne n.
$$

Therefore they cannot uniquely determine the renormalized eigenvectors or the complete effective Hamiltonian.

## Information-count argument

A general complex $8\times8$ matrix contains 64 complex entries. Hermiticity reduces a static Hamiltonian to 64 real degrees of freedom, while a general dynamical retarded self-energy remains complex and energy dependent.

A diagonal table contains at most eight complex entries at each $(\mathbf k,\omega,T)$. No algebraic postprocessing can reconstruct the omitted off-diagonal information without introducing additional assumptions.

## What diagonal output can support

A diagonal calculation may support:

- the on-shell shifts of identified band states;
- a diagonal approximation to $E_g(T)$ and $\Delta(T)$;
- linewidths from diagonal imaginary parts;
- convergence studies for meshes, broadening and polar corrections;
- comparison of Fan, Debye–Waller and quasiharmonic scalar contributions when each is available.

## What it cannot support by itself

It cannot establish:

- phonon-induced wavefunction renormalization;
- $P_8(T)$ or $P_7(T)$ from matrix derivatives;
- a one-$P$ versus two-$P$ closure test;
- off-diagonal quasiparticle residues;
- symmetry-restored matrix Dyson solutions;
- or a complete temperature-dependent 8-band Kane Hamiltonian.

## Repository enforcement

`mct_research.code_exports` accepts only explicit full complex $8\times8$ exports for `MatrixDataset` conversion. A diagonal self-energy table is rejected rather than embedded into a diagonal matrix and mislabeled as a full result.

A diagonal matrix may be constructed only as an explicitly named **model assumption**, with metadata recording that all off-diagonal elements were set to zero rather than calculated.

## Consequence for the staged campaign

The CdTe verification stage may begin with diagonal AHC output to establish cross-code scalar convergence. The HgTe scientific stage must then add a genuine matrix-valued extraction before drawing conclusions about temperature-dependent Kane couplings or model closure.
