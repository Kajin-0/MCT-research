# R08 independent QE source-formula parity — 2026-10-17

**Status: SOURCE-FORMULA PARITY PASS; NATIVE add_vuspsi EXECUTION NOT PERFORMED.** The reference comparison was bounded to saved xCd=.125 HSE Γ spinors, QE 7.5 source conventions, and separate Hg/Cd parent UPFs. No new SCF, native QE jobs, purchases or frozen R07 edits.

## Reproduce

`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 /home/User/opencode_workspace/DFT/.venv/bin/python research/programs/microscopic_ionic_scattering/qe_source_parity.py`

Outputs `qe_source_parity_results.json`. This independent numerical implementation uses QE 7.5 reference formulas for **real spherical harmonics and `rot_ylm`**, `spinor.f90` and `sph_ind.f90` Clebsch–Gordan coefficients, `init_us_1.f90` `fcoef`, `simpsn.f90` even-mesh tail Simpson integration, `beta_mod.f90` four-point 0.01 Bohr^-1 interpolation and `add_vuspsi.f90` noncollinear operator contraction. The original provisional calculation instead projected complex spin-angular harmonics directly with SciPy radial integration.

## Numerical tests

- Hg parent nonlocal Γ6−Γ8 contrast: direct prior **+4.782165231505295 eV**; independently source-mirrored QE-table result **+4.782165233120352 eV**; direct-integral parity +4.7821652315052985 eV.
- Cd parent contrast: direct prior **+5.479157333992430 eV**; QE-table +5.479157337556574 eV; direct-integral parity +5.479157333992430 eV.
- Cd−Hg nonlocal contrast: direct prior **+0.696992102487134 eV**; independent QE-table **+0.696992104436220 eV**.
- Maximum complex Cd−Hg matrix discrepancy QE source table vs previous Python: **2.4093e−9 eV**, Frobenius **4.8624e−9 eV**.
- QE interpolated tabulation versus direct radial: Hg max matrix element difference **1.3955e−9 eV**; Cd **2.6289e−9 eV**.
- Hermiticity errors of QE-derived parent matrices below 1.5e−16 eV.
- The previously calculated local +0.3877093932455 eV contrast and provisional nonlocal +0.6969921024871 eV contrast yield provisional total +1.0847014957326 eV. The independent interpolation-path contrast would shift it by ~+1.95e−9 eV, not a material accuracy bound.

**Interpretation:** A separate source-mirrored calculation reproduces parent-specific projected relativistic nonlocal matrix elements to the expected radial interpolation discrepancy. This strongly checks angular/index/phase and quadrature conventions **within those formulas**, but shares QE source definitions and cannot replace executing native `add_vuspsi` with initialized native projector arrays. The native `pw.x` executable contains the operator symbol but no isolated frozen-state interface, and the accessible QE source checkout lacks matching compiled module/object files; no free Fortran compiler executable was located in the preexisting runtime. No new build, diagnostic binary, or native operator action has been executed.

**Not claimed:** A certified exact QE operator action, a numerically bounded HSE eigenvalue, an alloy disorder linewidth, screened impurity response, physical x_c or scientific novelty. The strict 1e−8 R07 density symmetry failures persist.

**Stop/GO:** bounded independent *source-formula* check PASS; native validation gate remains OPEN. Do not expand into rebuilding QE, large tooling, new SCF/CPA or manuscript absent a separately defined executable test that genuinely yields independent physical information. Preserve input hashes and source paths.
