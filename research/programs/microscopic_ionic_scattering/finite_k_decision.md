# R08 bounded finite-k bare-ionic coupling — 2026-10-17

**Status:** EXECUTED limited frozen-wavefunction operator calculation. No QE DFT, no expenditures, no R07 edits, no screened rate/linewidth claim. Source: [finite_k_bare_probe.py](finite_k_bare_probe.py), data [finite_k_bare_results.json](finite_k_bare_results.json).

## Input and implementation

Previously converged HSE+SOC VCA xCd=.125 case; eight saved irreducible k-points, 44 spinor bands per point, with 2,692–2,733 plane waves per spinor. Six initial Γ spinors: candidate Γ6-like bands 33–34, Γ8-like 35–38. The substituted cation sits at Cartesian origin. Hg and Cd full-relativistic SG15 norm-conserving potentials projected independently into the plane-wave spinor states.

**Local:** reciprocal kernel 4π/Ω ∫r²(V_Cd−V_Hg)j₀(|k_i+G_i−k_f−G_f|r)dr; odd N=49 Fourier convolution, radial tabulation step .01 Bohr^-1. The local phase includes k_i−k_f; at a nonzero impurity site the complete e^{i(k_i−k_f)·R} factor is essential, but for this cation R=0.

**Nonlocal:** each Hg/Cd relativistic |β_{ljm_j}(k+G)> D <β_{ljm_j}(k'+G')| with radial spherical-Bessel and complex spin-angular Clebsch–Gordan factors. Matrix results are coherent *single-site periodic-cell-normalized* perturbation amplitudes and require the 1/Ncell factor for one impurity in a large crystal. No lattice-disorder concentration or Fermi golden rule applied.

## Internal validation

At Γ the generalized code reproduces prior local six-state matrix to **1.49515e−16 eV max**, and nonlocal to **2.22139e−15 eV max**. Both are numerically exact restatements with shared formulas, **not independent native QE validation**. Explicit reverse-forward Hermitian local reciprocity tested for Γ↔k2 and Γ↔k4 (zero-based internal indices 1 and 3) under 3e−10 eV. No independent cross-k QE action. VCA and host full-density strict 1e−8 symmetry failures remain unchanged.

## Bare matrix-element survey

Sum over all 44 final bands of |<final k|ΔV_ion|Γ initial>|² (eV²), summed over two Γ6-like or four Γ8-like initial states:

| k index | |k| Bohr^-1 | Γ6-like initial | Γ8-like initial |
|---:|---:|---:|---:|
|1|0.0000|1.5416|4.9855|
|2|0.2229|2.1812|15.1429|
|3|0.4457|4.4552|44.9215|
|4|0.2573|2.4316|18.7061|
|5|0.5609|6.8628|67.9513|
|6|0.3639|3.3807|31.9934|
|7|0.5147|5.8313|59.4199|
|8|0.5754|7.3750|72.0806|

This sum is over *different initial-sector dimensions*, a finite arbitrary truncated 44-band final-space, and differing |k| and symmetry directions; it is not a normalized per-state comparison or an on-shell scattering measure. Finite-k matrix elements can be large despite Γ6↔Γ8 off-block selection rule. A larger bare coupling does not by itself predict a broad spectral function.

For ±0.5 eV around each initial sector's Γ mean, Γ itself has six final bands in the window; at **non-Γ k2, the Γ6-like initial has 2 eligible final bands (35,36) with total squared bare strength 3.0949110e−14 eV²**, while Γ8-like initial has no eligible k2 states. Other six non-Γ saved k-points have no final states in that ±0.5 eV window. Neither the finite window nor sparse k sample defines a converged energy conservation delta; 3.09e−14 is **not** an error bound or evidence of generally negligible low-energy scattering. The zero-weight counts are simply missing sampled states.

## Qualification and strict stop

Calculated bare Γ-to-k coupling matrices using the existing saved states: **feasibility PASS**. The weak near-edge coupling hypothesis remains **UNDECIDED** because of sparse sampling, unqualified irreducible-BZ expansion, absent additional states, no screened impurity response, no random-alloy statistics, R07 strict symmetry FAIL, and no native QE operator-action comparison. Do not infer lifetime, linewidth, disorder mass, mobility, transition composition, or novelty. Do not start QE/CPA or paid jobs merely because amplitudes can be calculated.

Next falsifiable data need: verified dense near-Γ *same-Hamiltonian* final states and reference-aligned bands or independently accepted native operator output, with screening and alloy disorder identified separately. Current sparse archive cannot yield a physical scattering rate.
