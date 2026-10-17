# Exploratory R08 candidate: bare local ionic contrast in HgCdTe
Date: 2026-10-17. This is **not** an authorized new R07 HSE campaign, a full defect-scattering result, or an official portfolio registration.

## Physical target

Which Hg/Cd microscopic ionic channels couple the near-Gamma Gamma6-like and Gamma8-like electronic states, and can the weak coherent-band scattering observed in HgCdTe be explained without relying on phenomenological CPA disorder parameters?

Prior-art boundary: Hass, Ehrenreich & Velicky (1983), Phys Rev B 27 1088, spin-orbit CPA; Camassel et al. (1988), Phys Rev B 38 3948, cancellation hypothesis; Rubel et al. (2014), arXiv:1405.4218, unfolding/HgCdTe; Berlijn, Volja & Ku (2011), Phys Rev Lett 106 077005, Wannier disorder; Lu et al. (2020), npj Comput Mater, ab-initio defect matrix interpolation. Specific methodological claims require checking full texts before novelty is asserted.

## Actual finite-basis calculation

Reproduce using: PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/User/opencode_workspace/DFT/.venv/bin/python research/programs/microscopic_ionic_scattering/bare_ionic_local_gamma.py

The script uses only *read-only native files*: fully relativistic SG15 Hg/Cd PBE norm-conserving UPFs (20 valence electrons each; 14 vs 10 nonlocal radial projectors) and QE 7.5 HSE+SOC xCd=.125 VCA Gamma spinors, six bands 33-38 (2,733 G vectors per spin component). Same-charge -40/r Ry tails cancel. Spherical Fourier transforms of the **local** potential difference are integrated radially, embedded into primitive-cell Gamma plane-wave space, and projected as a finite 6x6 Hermitian scalar matrix. Raw matrix and SHA256 input pins: bare_local_gamma_result.json.

**CALCULATED local-only observable** (eV): Γ6-like trace mean +3.4042002225; Γ8-like +3.0164908293; difference **+0.3877093932**; Γ6↔Γ8 cross block Frobenius norm 4.1626891e−7 eV. Hermiticity 3.919e−16 eV. Independent odd FFT grid 41/49 discrepancy 8.308e−15 eV; q-grid spacing .01/.005 bohr−1 changes at most 1.112e−8 eV; unchanged radial tail below 1e−5 Ry. These diagnostics establish numerical interpolation/FFT stability **within this local-only definition**, not physical scattering accuracy. Earlier even-length FFT Nyquist assertion failed; replaced by odd-length grids rather than masking imaginary contamination. Preserved source is the corrected, rerun version.

**DO NOT INTERPRET AS** (i) 0.388 eV HSE bandgap derivative, (ii) a screened Hg/Cd impurity operator, (iii) the physical variance or broadening near Gamma, or (iv) accurate off-Gamma scattering. The very small Γ6↔Γ8 local block at Gamma is symmetry/near-symmetry compatible and may conceal strong coupling to other momenta/remote states. Missing full relativistic nonlocal-projector difference, consistent shared angular/radial embedding, Hartree/xc/HSE screened defect perturbation, local relaxation, finite-k spectral summation, disorder statistics and independent validation. Native Γ states also fail frozen 1e−8 full-density symmetry certification.

**Decision:** One genuine numerical artifact obtained at $0 without native QE; finite local subproblem PASS, claim of physical weak-scattering mechanism **UNDETERMINED**. Do not register a new independent scientific discovery or proceed to CPA, a native defect calculation or a manuscript. Next decisive requirement is a correct common-basis fully relativistic nonlocal operator and physical-screening separation with an independent check; if not possible from saved data, record NO-GO. Keep R07 stopping conditions and original data unchanged.
