# MCT Research

A private, hypothesis-driven research program for developing stronger analytical models of Hg\(_{1-x}\)Cd\(_x\)Te (MCT), with an initial focus on the composition- and temperature-dependent bandgap.

## Objective

Develop an analytical successor to purely empirical bandgap equations by connecting:

1. relativistic electronic structure,
2. alloy disorder,
3. electron–phonon renormalization,
4. thermal expansion,
5. the 8-band Kane model,
6. and experimentally measurable optical and magneto-optical observables.

The intended output is not merely another polynomial fit. The target is a compact, uncertainty-aware analytical model whose terms have identifiable physical origins and whose predictive performance can be tested against held-out data.

## Scientific status

This repository is exploratory research. A derivation, conjecture, or numerical result is **not treated as novel or correct merely because it appears here**. Claims advance through the following states:

- `conjecture`
- `derived`
- `numerically checked`
- `experimentally benchmarked`
- `literature-audited`
- `candidate novel result`

No novelty claim should be made until both a systematic literature audit and an independent reproducibility check are complete.

## Core research question

Can the signed bulk gap

\[
E_g(x,T)=E_{\Gamma_6}(x,T)-E_{\Gamma_8}(x,T)
\]

be replaced by a physics-constrained expression of the form

\[
E_g(x,T)=E_g^{\mathrm{stat}}(x)
+\Delta E_g^{\mathrm{ep}}(x,T)
+\Delta E_g^{\mathrm{QH}}(x,T)
+\Delta E_g^{\mathrm{disorder}}(x,T),
\]

where the electron–phonon term is obtained from Fan–Migdal and Debye–Waller self-energies, the quasiharmonic term accounts for thermal expansion, and the result is projected into a symmetry-preserving 8-band Kane Hamiltonian?

## Current leading hypothesis

Temperature primarily renormalizes the relative \(\Gamma_6\) and \(\Gamma_8\) band-edge energies, while the Kane coupling \(P\) or velocity \(v_K\) changes much less:

\[
\left|\frac{\Delta v_K}{v_K}\right|
\ll
\left|\frac{\Delta E_g}{E_g}\right|.
\]

Bulk magnetospectroscopy reporting an approximately composition- and temperature-independent Kane velocity near \(1.07\times10^6\ \mathrm{m\,s^{-1}}\) motivates this as a falsifiable hypothesis, not an assumption.

## Research program

### Phase 1 — Baselines and definitions

- Reconstruct Hansen-type empirical equations and their source datasets.
- Separate the static-lattice, quasiparticle, optical, and detector-cutoff definitions of bandgap.
- Establish uncertainty propagation from \(x\), \(T\), strain, carrier density, and spectral-edge criterion.

### Phase 2 — Binary endpoint validation

- Validate relativistic calculations for HgTe and CdTe.
- Compute Fan–Migdal, Debye–Waller, and thermal-expansion corrections.
- Extract finite-temperature 8-band parameters.

### Phase 3 — Alloy treatment

- Compare virtual-crystal, coherent-potential, and special-quasirandom-structure treatments.
- Restore macroscopic cubic symmetry after configurational averaging.
- Quantify disorder-induced broadening and uncertainty.

### Phase 4 — Analytical reduction

- Build a compact oscillator or spectral-moment representation of the electron–phonon correction.
- Fit composition dependence subject to endpoint, symmetry, and monotonicity constraints.
- Test whether one Kane parameter set remains closed under temperature renormalization.

### Phase 5 — Validation

- Use magnetoabsorption, Landau-level spectroscopy, absorption-edge data, and carefully modeled photoluminescence.
- Hold out entire compositions and temperature intervals from fitting.
- Compare against established engineering equations in meV, critical-composition error, and equivalent cutoff-wavelength error.

## Quantitative targets

Initial targets for the detector-relevant composition range are:

- bandgap mean absolute error: `< 5 meV`
- numerical convergence error: `< 1 meV`
- critical-composition error: `< 0.003`
- critical-temperature error: `< 5 K`
- Kane-velocity error: `< 5%`
- held-out magneto-optical transition error: `< 3–5 meV`

These are research targets, not current achievements.

## Repository organization

- `docs/program/` — research charter, roadmap, definitions, validation protocol
- `docs/derivations/` — formal mathematical derivations
- `docs/insights/` — concise numbered research insights and conjectures
- `literature/` — source ledger, prior-art audit, and evidence tables
- `models/` — analytical and numerical model implementations
- `data/` — provenance-controlled experimental or calculated datasets

## Initial literature anchors

- Hansen, Schmit, and Casselman: empirical \(E_g(x,T)\) relation for HgCdTe.
- Novik et al.: standard 8-band Kane treatment for HgTe/CdTe heterostructures.
- Allen–Heine–Cardona theory: Fan and Debye–Waller temperature renormalization of electronic structure.
- Teppe et al.: temperature-driven massless Kane fermions and approximately universal Kane velocity in bulk HgCdTe.
- Recent dielectric-dependent hybrid-functional/SQS work: static HgCdTe band structure and defect calculations with spin–orbit coupling.

Full bibliographic records and claim-level notes belong in `literature/ledger.md`.

## Working rule

Every important result should include:

1. assumptions,
2. derivation or computational provenance,
3. dimensional and limiting-case checks,
4. uncertainty estimate,
5. comparison to prior literature,
6. and a clearly stated falsification test.
