# Research Charter

## Program title

**Physics-constrained analytical electronic-structure models for Hg\(_{1-x}\)Cd\(_x\)Te**

## Primary objective

Develop and validate a compact analytical model for the bulk signed bandgap

\[
E_g(x,T)=E_{\Gamma_6}(x,T)-E_{\Gamma_8}(x,T)
\]

that improves on conventional empirical polynomial equations by assigning explicit physical meaning to composition, electron–phonon, thermal-expansion, strain, carrier-density, and alloy-disorder contributions.

The program remains open to additional analytical results involving finite-temperature Kane parameters, effective masses, magneto-optical transitions, alloy broadening, critical composition, and detector-relevant optical edges.

## Why this problem matters

A conventional engineering relation provides a useful mapping from composition and temperature to an apparent gap. It does not, by itself, distinguish:

- static-lattice electronic structure,
- quasiparticle correction,
- zero-point renormalization,
- finite-temperature electron–phonon renormalization,
- thermal expansion,
- strain,
- carrier-density effects,
- random-alloy broadening,
- or measurement-definition bias.

Near the zero-gap composition, small energy errors can produce large composition and cutoff-wavelength errors. A more structured model may improve extrapolation, uncertainty quantification, and interpretation of apparently inconsistent experimental datasets.

## Central research object

The strongest target is not initially a scalar equation. It is the projected finite-temperature Green function

\[
\overline{\mathbf G}_8^{-1}(\mathbf k,\omega;x,T)=
\hbar\omega\mathbf I
-\mathbf H_{8K}^{0}(\mathbf k;x)
-\boldsymbol\Sigma_{8}^{\mathrm{ep}}(\mathbf k,\omega;x,T)
-\boldsymbol\Sigma_{8}^{\mathrm{alloy}}(\mathbf k,\omega;x)
-\mathbf H_{8}^{\mathrm{QH}}(x,T).
\]

A compact analytical equation should be obtained only after this object, or a controlled approximation to it, has been validated.

## Definitions that must remain distinct

### Signed Kane gap

\[
E_g^{\mathrm{signed}}=E_{\Gamma_6}-E_{\Gamma_8}.
\]

- \(E_g<0\): inverted ordering.
- \(E_g=0\): critical composition or temperature.
- \(E_g>0\): normal ordering.

### Static-lattice gap

Electronic gap at fixed equilibrium nuclear positions without zero-point motion.

### Quasiparticle gap

Pole separation of the interacting one-electron Green function.

### Optical gap

Optical threshold after excitonic and line-shape effects.

### Detector cutoff

Operational wavelength obtained from a stated response criterion. It is not automatically identical to \(hc/E_g\).

Any dataset entered into the project must identify which quantity was actually measured or inferred.

## Core decomposition

The first controlled decomposition is

\[
E_g(x,T)=E_g^{\mathrm{stat}}(x,V_0)
+\Delta E_g^{\mathrm{ep}}(x,T;V_0)
+\Delta E_g^{\mathrm{QH}}(x,T)
+\Delta E_g^{\mathrm{extrinsic}}.
\]

Here

\[
\Delta E_g^{\mathrm{ep}}
=\operatorname{Re}\left[
\Sigma_{\Gamma_6}^{\mathrm{Fan}}
-\Sigma_{\Gamma_8}^{\mathrm{Fan}}
+\Sigma_{\Gamma_6}^{\mathrm{DW}}
-\Sigma_{\Gamma_8}^{\mathrm{DW}}
\right].
\]

The extrinsic term may include strain, carrier density, defects, and measurement-model corrections. Alloy disorder should ultimately be treated at the Green-function or spectral-function level rather than represented only by a deterministic scalar correction.

## Research hypotheses

### H1 — Band-edge renormalization dominates Kane-velocity renormalization

\[
\left|\Delta v_K/v_K\right|
\ll
\left|\Delta E_g/E_g\right|.
\]

**Falsification:** a projected first-principles Hamiltonian or independent magneto-optical dataset shows a statistically significant temperature dependence of \(v_K\) comparable to the relative gap change.

### H2 — The empirical linear temperature coefficient is an intermediate-temperature reduction

The finite-temperature correction is expected to have the spectral form

\[
\Delta_T E_g^{\mathrm{ep}}(x,T)
=2\int_0^\infty d\omega\,
\mathcal F_g(x,\omega)n_B(\omega,T),
\]

with approximately linear behavior only when the dominant phonons are thermally populated.

**Falsification:** high-quality low-temperature data show exact linearity within uncertainty over a range in which the relevant phonon occupations are demonstrably nonclassical, or the calculated coupling spectrum fails to reproduce the observed curvature.

### H3 — The conventional one-\(P\) 8-band model may not be closed under finite-temperature renormalization

A projected self-energy may produce distinct effective couplings

\[
P_8(T)\ne P_7(T)
\]

between \(\Gamma_6\leftrightarrow\Gamma_8\) and \(\Gamma_6\leftrightarrow\Gamma_7\).

**Falsification:** the difference remains below numerical, gauge, and experimental uncertainty across all tested compositions and temperatures.

### H4 — A single sharp critical composition becomes ill-conditioned near disorder broadening

If

\[
|E_g(x,T)|\lesssim\Gamma_{\mathrm{alloy}}(x,T),
\]

a spectral or probabilistic description may be more defensible than a unique deterministic \(x_c(T)\).

**Falsification:** configuration-resolved calculations and spectroscopy show a gap distribution much narrower than the inferred crossing scale.

## Candidate novelty areas

The following are possible novelty targets, not current novelty claims:

1. A disorder-averaged, nonadiabatic AHC calculation for bulk HgCdTe with spin–orbit coupling.
2. Projection of the finite-temperature self-energy into a symmetry-preserving 8-band Kane Hamiltonian.
3. First-principles temperature dependence of the full parameter set

   \[
   \{E_g,\Delta,P_8,P_7,F,\gamma_1,\gamma_2,\gamma_3\}(x,T).
   \]

4. A formal closure test determining whether the standard Kane parameter manifold remains adequate after electron–phonon renormalization.
5. A compact analytical surrogate derived from spectral moments rather than a free polynomial in \(x\) and \(T\).
6. An uncertainty-aware relation connecting composition, temperature, signed gap, and experimentally defined spectral cutoff.

## Minimum evidence required for a candidate novel result

A result must satisfy all of the following:

- explicit derivation or executable implementation;
- dimensional and limiting-case checks;
- numerical convergence study;
- comparison with at least two independent literature baselines;
- held-out prediction not used in calibration;
- quantified uncertainty;
- documented prior-art search;
- and independent reproduction from repository instructions.

## Validation observables

A model should be tested against more than one scalar gap dataset. Preferred observables are:

- magnetoabsorption transition energies;
- Landau-level spectra;
- Kane velocity;
- cyclotron mass;
- spin–orbit splitting;
- absorption-edge line shape;
- critical composition \(x_c(T)\);
- critical temperature \(T_c(x)\);
- and configuration-dependent spectral broadening.

## Initial quantitative targets

For approximately \(0.15\lesssim x\lesssim0.40\) and \(4\le T\le300\ \mathrm K\):

| Metric | Initial target |
|---|---:|
| Bandgap MAE | < 5 meV |
| Numerical convergence uncertainty | < 1 meV |
| Critical-composition error | < 0.003 |
| Critical-temperature error | < 5 K |
| Kane-velocity error | < 5% |
| Cyclotron-mass error | < 5% |
| Held-out transition-energy error | < 3–5 meV |

These thresholds may be revised after the experimental uncertainty floor is reconstructed.

## Decision gates

### Gate 1 — Historical reconstruction

Can the standard empirical equation and its residuals be reproduced from traceable source data?

### Gate 2 — Binary endpoint correctness

Can the method reproduce HgTe and CdTe ordering, gaps, spin–orbit splitting, and finite-temperature trends?

### Gate 3 — Kane projection stability

Are the extracted parameters stable under basis gauge, \(k\)-window, frequency-linearization point, and symmetry restoration?

### Gate 4 — Alloy convergence

Are SQS/configuration averages stable with respect to cell size and configuration count?

### Gate 5 — Predictive improvement

Does the physics-constrained model outperform empirical baselines on held-out compositions or temperatures?

### Gate 6 — Novelty

Does a systematic prior-art audit support a claim that the result has not already been published?

## Research integrity rules

- Do not conflate detector cutoff with the quasiparticle gap.
- Do not infer novelty from an equation assembled from known components.
- Do not hide fit parameters inside physically named terms.
- Do not use the same data both to define and independently validate a model.
- Preserve failed hypotheses and negative results.
- Record every manual data extraction and transformation.
- Report uncertainty in energy before converting to wavelength.
