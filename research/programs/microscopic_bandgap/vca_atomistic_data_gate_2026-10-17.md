# R07 — xCd=0.125 VCA-to-atomistic data availability and comparability gate
Date: 2026-10-17. Status: PUBLIC_NUMERIC_DATA_NOT_LOCATED; QUANTITATIVE_COMPARISON_NO_GO.

## Scope and public sources checked

Target: Wang, Luo & Zunger, "Alloy theory with atomic resolution for Rashba or topological systems", Physical Review Materials 3, 044605 (2019); https://doi.org/10.1103/PhysRevMaterials.3.044605. Free full article at https://www.colorado.edu/faculty/zunger-matter-by-design/sites/default/files/attached-files/698.pdf; APS abstract https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.3.044605; arXiv https://arxiv.org/abs/1901.01289; CU author publication list https://www.colorado.edu/faculty/zunger-matter-by-design/publications-0.

Public article Figure 5 displays effective band structures at xCd=0.125, 0.1875, 0.25, 0.3125. The public article gives EBS formalism in §IV and LDA+U/PAW/VASP setup in §III. It does not supply machine-readable SQS coordinate sets, per-state unfolded weights, numeric Gamma projector-resolved energies, or spectral peak widths in its main text. The CU author publication listing links the PDF but lists no supplemental material or supporting-data link on this entry (unlike some neighboring entries). Targeted public web/Zenodo-like searches and GitHub code/repository search for DOI, SQS POSCAR and HgCdTe/BANDUP did not locate a unique matching numerical bundle. This is a search-limited negative finding, **not proof of data nonexistence**. A figure's plotted sharpness is not a measured numeric linewidth.

**Availability**
- Full manuscript / published Figure 5: CONFIRMED OPEN.
- Exact x=.125 64-atom SQS occupancy, cell and relaxed coordinates: NOT LOCATED.
- Raw spinor wavefunctions, unfolded Gamma spectral weights / A(k,E), window moments or resolvable widths: NOT LOCATED.
- Published near-Gamma qualitative coherence: CONFIRMED IN PAPER, not a quantitative dispersion/error bound.
- Matched HSE/SOC Hamiltonian dataset at x=.125 using same QE virtual-cation/functional protocol: NOT LOCATED.
- No author contact, licensed retrieval bypass, paid material or DFT execution.

## Crucial previously unqualified comparison discrepancy

**Wang HgTe/CdTe model is LDA+U, not HSE**: Table I reports LDA+U(Ud=10 eV) with 400 eV plane-wave cutoff for BOTH constituents, PAW VASP; HgTe signed band order -0.26 eV, CdTe bandgap +0.86 eV. 8x8x8 primitive k points; HgCdTe SQS 32 formula units = 64 atoms and 4x4x4 *supercell* k grid. The authors use ATAT SQS, full relaxation of atomic coordinates, cell shape, volume, and a modified BANDUP unfolding tool. They report weak near-Gamma incoherent weight and <25 meV heavy-hole splitting away from Gamma (toward L); neither value is an error bar on VCA Gamma ordering.

Our x=.125 VCA run: stock QE7.5 NC full-SO fractional-cation virtual pseudo, HSE(.25,.106), primitive two atoms, fixed a=6.46 Å, 50/200 Ry, Fock200 Ry, k4/q4, FD degauss .001 Ry; Gamma-like -98.7879687199 meV (half -49.39398435995 meV). Frozen full-density Gamma Theta 3.95518494693e-7 and Td 4.95143773706e-7 **FAIL strict 1e-8**. The cross-paper offset at fixed x, *even if extracted from a figure*, is confounded by functionals, pseudopotentials, spatial structure, smearing, model disorder and energy/projector conventions. **It is not delta_Delta_Gamma due to disorder**. Do not subtract or fit.

For context, Nicklas & Wilkins 2011 is a different VASP HSE/PAW **32-atom SQS** (16 formula units) model that includes x=.25,.50,.75 and predicts a fitted crossover x~.17, but no native x=.125 state. Wang's 64-atom x=.125 **LDA+U** SQS is not that matched HSE state.

## Predeclare distinct candidate observables (not yet computable)

(1) Coherent energy bias: delta_Delta_Gamma(x) = Delta_Gamma(disordered, matched H) - Delta_Gamma(VCA, matched H), where the disordered 'Delta' must be a predetermined Gamma6-like versus Gamma8-like **unfolded spectral estimator**, with matched spinor projector, reference alignment and fixed energy window. In a disordered finite supercell, individual folded bands need not carry exact cubic irreps. Do not select arbitrary nearest bands.

(2) Spectral redistribution: project each disordered supercell eigenstate onto primitive Gamma sector and obtain A_s(Gamma,E)=sum_j w_sj delta(E-E_j). Record w_sj sum/normalization, resolved peaks/centroids, spectral variance or separately controlled kernel broadening, and non-coherent weight. Define reference windows, selection weights and peak/centroid conventions before inspecting. A narrow spectral function **does not guarantee** a small VCA energy bias.

(3) Off-Gamma heavy-hole/symmetry response, e.g. Gamma-L splitting and its dependence on local environments, is a separate observable and must not be silently folded into Gamma mass.

**Same-H control requirements:** same physical cell density and strain, same exchange-correlation functional, same pseudopotential/spin-orbit operator, comparable k sampling/finite-size convergence, consistent potential energy zero, compatible projector and unfolding conventions, matched occupation/smearing/electron counting, quantitative source/residual and disorder-configuration uncertainty. Numerical scalar shifts cannot be compared across pseudopotential choices without defining reference alignment. Error budgets require each controlled source; no universal error bounds from Wang's qualitative coherence.

## Result and strict stopping rule

Observed evidence supports the *hypothesis* that coherent VCA may suffice near Gamma, but quantitative VCA bias, disorder spectral width, and physical critical composition are **UNIDENTIFIED** from the data located. Neither strong disagreement nor agreement can be quantified. Do not manufacture synthetic SQS spectra, extract false precision from Figure 5 pixels, manufacture atomistic disorder Hamiltonians, claim a physical xc, loosen the strict density gate, or authorize another HSE scan.

**STOP / NO-GO** for a matched x=.125 quantitative comparison until a verified numerical 64-atom structure + energy/weight dataset is obtained AND same-H methodological alignment is established; even then resolving native VCA symmetry failure is a separate independent acceptance gate. Permitted next acquisition is free supplementary archives/source search, or optional narrowly scoped author inquiry when separately approved. Record missing inputs, not speculative computed corrections. No spending and no new native QE run.
