# R07: three-primary-paper method and identifiability audit (2026-10-17)

**Status:** full accepted Nicklas/Wilkins (2011), open full Wang/Luo/Zunger (2019) and arXiv v2 Krishtopenko/Antezza/Teppe (2022) examined. This is a methodological source audit, **not** independent replication of published numerical results, a validated physical x_c, or authorization for another computation. Use the pinned DOI/PDF URLs below as source references; complete article copies and coordinates have not been added to the repo.

## 1. Nicklas and Wilkins, Phys. Rev. B 84, 121308 (2011)

Source: https://doi.org/10.1103/PhysRevB.84.121308 ; full accepted PDF https://link.aps.org/accepted/10.1103/PhysRevB.84.121308 . Inspect Method §II, Table I, Fig. 3, Table II.

- Physical observable defined explicitly as signed **Eg = E(Gamma6)-E(Gamma8)**. A negative value for HgTe means inverted *Gamma ordering*, not a positive fundamental optical gap or insulating topological bulk gap.
- VASP PAW, PBE and screened HSE06, plane-wave cutoff **350 eV**; pure-compound primitive sampling 8x8x8 Gamma-centered. SQS supercell integrations are specified separately, including 4x3x3 for x=.25 and 3x3x3 for x=.50; do not assume an identical per-atom mesh for all x.
- **32 total-atom SQS**, Cd fractions 0.25, 0.50, 0.75; x=.25/.75 pair correlations matched through third neighbor and x=.50 through seventh neighbor. x=.25 and x=.75 derive by swapping occupations. Experimental endpoints a(HgTe)=6.46 Angstrom and a(CdTe)=6.48 Angstrom are linearly interpolated. **Local lattice relaxation omitted** due to small mismatch.
- Reported HSE Eg(HgTe)=-0.27 eV; Eg(CdTe)=+1.34 eV; PBE analogues -0.93 and +0.52 eV. HSE x_c about **0.17**, PBE about **0.67**, from a **cubic fit** to x=0,.25,.50,.75,1 (Fig.3, Table II), **not a direct native result x=.17**.
- Comparison to our VCA x=.125 is *cross-method only*. Our QE75 NC full-SO VCA k4/q4 50/200 Ry HSE(.25,.106), FD.001Ry, primitive a=6.46 Angstrom and fixed sites differs in virtual cation construction, PAW, sampling, lattice law, 32-atom disorder, and representation qualification. At x=.125 their stated Vegard a would be 6.4625 Angstrom; **difference is a geometry mismatch, not an error bar**. Our signed Gamma-like ordering -0.09878796872 eV is not symmetry certified.
- Novelty NO-GO: HSE alloy crossover alone already published; an interior composition point alone is not a new theory or physical x_c estimate.

## 2. Wang, Luo and Zunger, Phys. Rev. Materials 3, 044605 (2019)

Source: https://doi.org/10.1103/PhysRevMaterials.3.044605 ; full author PDF https://www.colorado.edu/faculty/zunger-matter-by-design/sites/default/files/attached-files/698.pdf . Inspect §II (LD/CE/BR), §III (VASP/ATAT), Fig.5 and §V.

- Their **32 formula-unit CdTe-HgTe SQS = 64 atoms**, unlike Nicklas's 32-*atom* SQS. Published unfolded compositions xCd=.125,.1875,.25,.3125; **x=.125 is already studied by atomistically resolved EBS**. 4x4x4 supercell k grid, ATAT SQS, relaxed positions, shape and volume, PAW VASP, BANDUP-like EBS unfolding.
- They separately define effects of lattice deformation (LD), charge exchange (CE) and bond relaxation (BR). The decomposition of mixing *energy* is not automatically an additive decomposition of spectral inversion mass.
- Result: around Gamma near-Fermi states have sharp unfolded dispersion and nearly fully coherent weights in their model; the incoherent contribution for CdTe-HgTe is small, and they state monomorphous models *may* adequately describe the Gamma6/Gamma8 inversion. A small heavy-hole splitting **<25 meV along Gamma-L** is still reported; local environments are not identically absent.
- **Do not infer a large disorder shift as a starting prior.** This source shifts the falsifiable target to a well-defined *upper bound or detectability criterion* for VCA error, plus observing departures where they actually occur. Their claim does not certify our fractional pseudopotential, HSE functional, zero-temperature x_c, or strict density symmetry.

## 3. Krishtopenko, Antezza and Teppe, Phys. Rev. B 106, 115203 (2022)

Source: https://doi.org/10.1103/PhysRevB.106.115203 ; arXiv v2 https://arxiv.org/pdf/2206.14561 . Inspect Eqs. (1)-(25), Fig.1, Fig.2, Fig.4, §IV.

- They introduce a **six-state Gamma6/Gamma8 Kane model**, with heavy-hole and light-hole branches explicitly retained. The clean inversion parameter is **M=(Ec-Ev)/2** (Eq.9): M>0 trivial semiconductor, M<0 inverted topological semimetal in their idealized rotational model. This is the same *half-ordering convention* as our candidate m, but **not** an independent state mapping or stationary DFT result. The paper neglects small cubic-anisotropy and bulk-inversion-asymmetry terms (end of Eq.5 discussion).
- Two **zero-mean, independent Gaussian** random fields are postulated: a scalar impurity potential Vimp(r)*I6 and mass-fluctuation potential UM(r)*diag(1,1,-1,-1,-1,-1), with strengths v and u and correlation functions g and xi (Eq.11). Different microscopic sources are *assumed*, not derived from fully relaxed atomistic Hg/Cd substitution.
- For the final **white-noise specialization** g_tilde(q)=xi_tilde(q)=1 (around Eq.19), the self-energy becomes momentum independent; Sigma_p=0 and Sigma_hh=Sigma_lh. The equations depend only on **W²=v²+u²**. Within this specialization, the same W produces identical predicted DOS/spectral functions for infinitely many (v,u) pairs. **PROVEN CONDITIONAL ON THEIR PUBLISHED MODEL:** this is a structural non-identifiability of the two variance components from those outputs; it is not a new general theorem for correlated realistic disorder. Retain independent finite-range correlations or extra observables to distinguish channels.
- Their renormalized mass (Eq.23) is **m(epsilon,W)=M+[Re Sigma_c(epsilon)-Re Sigma_lh(epsilon)]/2**; simultaneous chemical-potential shift follows the sum. The transition m(epsilon,W)=0 is **energy- and disorder-dependent** in the chosen SCBA theory, and the DOS gap-edge equations (Eq.24) require consistent self-energy. It is not automatically the zero of our coherent static x-dependent DFT Gamma level difference.
- Their illustrative figure compares x=.155, x~.168, x=.18, and varies W, explicitly including the heavy-hole band; heavy holes can substantially lower the predicted critical disorder strength compared with two-band 3D BHZ (Fig.4). These are *model parameters/results*, **not** composition-resolved HSE+SQS critical compositions. No transfer of the numerical critical disorder strength to R07 without matched parameters, scatterer correlations, and cutoff.
- **Prior-art NO-GO:** generic SCBA Kane-mass renormalization, m=0 transition logic, and heavy-hole-assisted disorder transition already established. Merely replacing M by our candidate VCA half-gap in their equation neither derives the unknown disorder covariance nor solves a new materials problem.

## 4. R07 synthesis: what can and cannot be inferred

**Available:** conventional HSE numerical SCF and G-labelled reference-*like* Gamma sector weights, including x=0 and x=.125, and ordered PBE environment contrasts. Our x=.125 Gamma difference =-98.7879687199 meV; candidate half =-49.39398435995 meV. The x=0 signed difference -289.586504823 meV is conditional. The x=.125 native full-density Theta op=3.95518494693e-7, Td max=4.95143773706e-7. Both strict 1e-8 symmetry gates **FAIL**. Preserve all historical no-go findings.

**Missing, not inferred:** symmetry-accepted static reference mass, fully stationary/eigenpair and material error bounds; specific coherent reference definition compatible with disorder operators; conditional scalar and mass disorder *covariances* and their cross terms, their finite spatial correlations, atomistic local Te environments; SQS ensemble/unfolded spectral data under a matched Hamiltonian; zero-temperature physical disorder-aware x_c; independent material validation.

The strongest immediate claim is **a prospective material-specific bound or falsifier on replacing disordered HgCdTe by a coherent VCA near Gamma**, conditional on a well-defined ensemble/model and a matched observable. Existing Wang evidence suggests that the deviation may be small; report that as a hypothesis to test, not an a priori vanishing correction.

### Concrete falsifiable gate before more computation

Define a **same-Hamiltonian** comparison at x=.125: (a) coherent VCA gamma-sector energy and wavefunction/projector definition, (b) ensemble/SQS unfolded A(Gamma,E) centroid and width, with error bars for finite configurations and k resolution, (c) finite-k heavy-hole shift. State the symmetry and reference alignment requirement and a quantitative tolerance chosen *before* inspecting the data. If both match within certified uncertainty, the result should support VCA adequacy and **refute** a claimed large disorder correction. If they differ, test whether local environment covariance accounts for the difference **without adding already-averaged physics twice**. The current 1e-8 symmetry failure blocks physical acceptance until resolved under the frozen gate.

**Data needed first:** published SQS coordinates/correlation targets, full Gamma energies/spinor or s/p projection conventions, reciprocal unfolding weights and widths near .125/.1875, functional and pseudopotential exact specifications, experimental measurement temperature/sample strain and operational transition definition. The three accessible full texts do *not* provide these as a complete numerical replication bundle in the material examined. No data requests have been sent.

**Execution decision:** **STOP**. Do not launch HSE composition scan, new native runs, paid resources or threshold relaxation. Focus on source reconstruction, analytical identifiability, and no-cost data acquisition. Any additional scientific calculation requires its own separately admitted protocol and approval. No new claims of novelty or manuscript readiness.
