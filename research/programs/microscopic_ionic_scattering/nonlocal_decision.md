# R08 full bare-ion Γ projection — bounded checkpoint (2026-10-17)

**Status:** CALCULATED PROVISIONAL; independent native QE nonlocal action NOT VALIDATED. No new DFT, no spending, R07 retained unchanged.

## Reproduction

Run from MCT-research:
`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/User/opencode_workspace/DFT/.venv/bin/python research/programs/microscopic_ionic_scattering/nonlocal_gamma_probe.py`

Outputs: `nonlocal_gamma_provisional.json` and `complete_bare_gamma_provisional.json` (combined local+nonlocal; constructed by direct addition of the committed local matrix and newly projected nonlocal one). All are six saved Γ candidates 33-38 at x_Cd=.125. Input Hg, Cd, virtual_x=.125 SG15 full-SO UPFs, saved spinors, XML are read-only with hashes.

## Definitions and numerics

For each chemical species separately, evaluate the fully relativistic norm-conserving separable nonlocal operator, preserving its own radial projectors and diagonal D_ij. Matrix elements are formed in the **same spinor plane-wave Hilbert space**. The code uses complex spherical harmonics and normalized Clebsch–Gordan angular spinors for j=l±1/2; because D_ij is diagonal and spherical, the sum over m_j is invariant under unitary real-versus-complex harmonic representation. Radial Fourier coefficients use 4π/sqrt(Ω) times a Simpson integral of UPF radial β(r)×r×spherical-Bessel; prefactor (-i)^l. Cation site at the primitive origin. The parent projectors have 14 Hg radial channels, 10 Cd radial channels; VCA UPF has their 24 combined channels and weighted D blocks. The matrix is not created by subtracting unlike projector coefficient arrays.

**Numeric results (eV):**
- Local Γ6-like minus Γ8-like trace contrast: **+0.3877093932455**.
- Relativistic nonlocal Γ6-like minus Γ8-like trace contrast: **+0.6969921024871**.
- Full bare ionic Γ6-like minus Γ8-like trace contrast: **+1.0847014957326**.
- Full bare local+nonlocal Γ6-like mean: **+0.5254691369181**; Γ8-like mean **−0.5592323588146**.
- Full Γ6-like↔Γ8-like off-block Frobenius norm: **2.51587624556e−7** (symmetry-suppressed, not a general scattering cross section).
- VCA nonlocal matrix versus .875 Hg + .125 Cd parents: **max element error 2.2658e−15 eV**, Frobenius 2.4428e−15 eV. This tests weighted construction, not absolute QE operator fidelity.
- Hermiticity per-parent and difference at machine precision. Original even FFT grid local-potential path was replaced by odd grids 41/49, numerical tests preserved.

**Explicitly not independently qualified:** There is no native QE exported β(G) matrix or independent application of native V_NL to these frozen spinors. Source-formula consistency and weighted identity do **not** exclude an overall missing factor, radial convention error common to parents, or angular-spinor phase bug. No physical error bound is assigned. Full-operator validation stays PENDING, not PASS; a separate genuinely independent native action or benchmark is necessary before elevating the numerical matrix.

**Never infer** a 1.0847 eV bandgap/composition derivative, alloy linewidth, screened self-energy, physical x_c, numerical uncertainty or novel material mechanism. Bare ionic exchange is not the screened self-consistent HSE impurity perturbation. Γ points alone cannot establish finite-k alloy scattering. Original R07 1e−8 full-density symmetry failure remains unchanged.

## Decisive next gate

**Do not launch native QE.** Accept this as a source-informed provisional matrix and STOP until a controlled independent check of the projector action is available. If available, qualify Fourier angular/radial conventions with a parent QE nonlocal reference and then only consider saved finite-k channels. No CPA, supercell, HSE, or manuscript follows automatically.
