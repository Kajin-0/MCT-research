# R07 priority literature and novelty boundary — 2026-10-17

## Highest priority: Nicklas and Wilkins (2011)

Jeremy W. Nicklas and John W. Wilkins, *Accurate electronic properties for (Hg,Cd)Te systems using hybrid density functional theory*, Physical Review B 84, 121308 (2011). DOI: https://doi.org/10.1103/PhysRevB.84.121308. Open accepted manuscript: https://link.aps.org/accepted/10.1103/PhysRevB.84.121308.

Verified from full accepted manuscript (Table I, Fig. 3, Methods): HSE gives the HgTe signed Gamma6-Gamma8 gap -0.27 eV and CdTe gap +1.34 eV, with fitted alloy crossing near Cd fraction 0.17. PBE gives HgTe -0.93 eV, CdTe +0.52 eV and crossing about 0.67. Calculated alloy points use 32-atom SQS compositions 0.25, 0.50 and 0.75; a cubic fit through these and binary endpoints determines the predicted crossing. This is not a direct calculation at x=0.17. VASP PAW HSE and explicit alloy SQS are distinct from our QE7.5 NC pseudopotential primitive coherent VCA.

**Prior-art boundary:** Predicting an HSE-based HgCdTe critical composition is not, by itself, novel. Our x=0.125 VCA result adds an interior coherent-potential point, not an independently qualified physical crossing. Never treat differences from this paper as validated material error without matched observables, structures, pseudopotentials and convergence studies.

## Ranked companion papers

1. **Wang, Luo and Zunger (2019)**, *Alloy theory with atomic resolution for Rashba or topological systems*, Phys. Rev. Materials 3, 044605. https://doi.org/10.1103/PhysRevMaterials.3.044605. Author full text: https://www.colorado.edu/faculty/zunger-matter-by-design/sites/default/files/attached-files/698.pdf. Their abstract explicitly reports weak incoherent disorder weight for CdTe-HgTe within their effective-band-structure model; that does not certify this implementation of VCA or all physical observables.
2. **Krishtopenko, Antezza and Teppe (2022)**, *Disorder-induced topological phase transition in HgCdTe crystals*, Phys. Rev. B 106, 115203. https://doi.org/10.1103/PhysRevB.106.115203. Open: https://arxiv.org/pdf/2206.14561. Prior art on disorder-renormalized Kane masses and phase transitions. Verify the precise observable against the full text.
3. **Wei and Zunger (1991)**, *Disorder effects on the density of states of II-VI semiconductor alloys*, Phys. Rev. B 43, 1662. https://doi.org/10.1103/PhysRevB.43.1662. Open: https://www.colorado.edu/faculty/zunger-matter-by-design/sites/default/files/attached-files/191.pdf. Study chemical mismatch, local environments and spectral consequences beyond mean VCA.
4. **Alowa and colleagues (2025)**, *Effect of atomic configuration and biaxial strain on the electronic properties of CdZnTe and HgCdTe alloys*, J. Phys. D. https://doi.org/10.1088/1361-6463/adb2a0. Compare explicit arrangements, strain, functionals and cell sizes after inspecting full methodology.
5. **Teppe and colleagues (2016)**, *Temperature-driven massless Kane fermions in HgCdTe crystals*, Nature Communications. https://www.nature.com/articles/ncomms12576; https://pmc.ncbi.nlm.nih.gov/articles/PMC5013552/. Independent finite-temperature magneto-optical benchmark, not an identical static-lattice DFT observable.
6. **Yang and colleagues (2026)**, *Covalency-resolved band gap correction for electronic structure calculations in HgCdTe*, Computational Condensed Matter. https://doi.org/10.1016/j.cocom.2026.e01374. Methodological comparison only until calibration parameters and full method are audited; nonempirical status unverified.

**Evidence levels:** The Nicklas manuscript and Wang journal abstract were directly inspected for the statements above. The remaining papers are prioritized reading leads rather than independent full-text methodological certifications in this checkpoint.

## Revised governing question and gates

**Question:** Can R07 independently derive and validate the difference between the coherent VCA Gamma6/Gamma8 crossing and the physical disorder-dependent HgCdTe transition, without fitting either crossing to known experimental x_c?

Separate a chemical coherent operator from local-environment/disorder self-energy without double counting. Define which transition is claimed: ordered-cell Gamma level difference, unfolded spectral mobility edge, Kane mass, topological boundary, or measured optical gap. Characterize material, finite-size, composition and functional uncertainty separately from conditional numerical arithmetic. Prior HSE SQS crossover and SCBA inversion work are already published: novel contribution requires a new falsifiable mechanism, validated uncertainty/disorder correction, or independent observable prediction.

**Existing R07 evidence is unchanged:** x=0.125 VCA HSE outer convergence PASS; reference-associated candidate Gamma6-like minus Gamma8-like -98.7879687199 meV (half -49.39398435995 meV); full-density Gamma Theta 3.95518494693e-7 and Td maximum 4.95143773706e-7 both FAIL the frozen 1e-8 threshold. Host endpoint conditional difference -289.586504823 meV also fails strict symmetry. Neither candidate is an accepted physical inversion mass. No physical random-alloy x_c exists.

Before any new native job: read Nicklas, Wang and Krishtopenko deeply; inspect potentially obtainable free supplementary SQS coordinates, composition-resolved Gamma energies, HSE/PAW settings, spinor projector definitions and band-unfolding weights; identify which independent causal input or experiment would distinguish VCA from disorder-aware transition. Do not fit empirical x_c, authorize a composition scan, change symmetry thresholds, contact authors automatically, or spend money. Native HDF5 remains private on the VPS; URLs are reading references, not acquired datasets.
