# HgCdTe disorder and spectral-gap prior art

## Question

Near the normal-to-inverted transition, is the alloy adequately represented by one sharp scalar

$$
E_g(x,T)=E_{\Gamma_6}-E_{\Gamma_8},
$$

or must the analytical object include disorder-induced energy width and spectral weight?

## 1. First-principles unfolded alloy spectra are established

Rubel, Bokhanchuk, Ahmed, and Assmann, *Physical Review B* **90**, 115202 (2014), use supercell band unfolding to recover Bloch spectral weight in disordered semiconductor alloys. Their HgCdTe example explicitly treats the topological band crossover and the emergence of Kane-like states.

This establishes that:

- atomistic Hg/Cd disorder can be represented in supercells;
- the disordered alloy should be interpreted through spectral weight rather than raw folded eigenvalues;
- the HgCdTe topological crossover has already been examined in an unfolded first-principles alloy calculation.

It does not provide a temperature-dependent electron-phonon plus alloy-disorder self-energy, nor a specimen-calibrated analytical width equation.

## 2. Matrix disorder self-energy and disorder-driven inversion are established

Krishtopenko, Antezza, and Teppe, *Physical Review B* **106**, 115203 (2022), study bulk HgCdTe with a self-consistent Born approximation applied to a six-state $\Gamma_6\oplus\Gamma_8$ Kane model.

They include two independent random potentials:

1. a scalar impurity potential;
2. a random mass or gap-fluctuation potential representing Cd-composition fluctuations.

The disorder-averaged Green function is

$$
G(\mathbf k,\varepsilon)
=
\left[
\varepsilon-H_{\mathrm K}(\mathbf k)
-\Sigma_{\mathrm{dis}}(\mathbf k,\varepsilon)
\right]^{-1},
$$

with a structured matrix self-energy containing conduction, light-hole, heavy-hole, and interband components.

The paper follows the density of states and interprets the transition through a disorder-renormalized Kane mass. It also finds that the heavy-hole band makes the HgCdTe transition sensitive to weaker disorder than conventional three-dimensional topological-insulator models.

Therefore the following are already established prior art:

- disorder-renormalized Kane mass in bulk HgCdTe;
- a matrix disorder self-energy in a reduced Kane manifold;
- Cd-composition fluctuations modeled as a random mass;
- disorder-induced normal/inverted transitions;
- density-of-states evolution rather than only a sharp scalar gap.

## 3. What is not established by those papers

The current audit has not identified a single calculation that simultaneously supplies:

$$
\Sigma_{\mathrm{tot}}
=
\Sigma_{\mathrm{ep}}(T)
+
\Sigma_{\mathrm{dis}}(x)
+
\Sigma_{\mathrm{defect}}
$$

in the complete conventional $\Gamma_6\oplus\Gamma_8\oplus\Gamma_7$ eight-band basis and then projects it into temperature-dependent Kane invariants with covariance.

Also not identified:

- a composition- and temperature-dependent analytical equation for both mean signed gap and spectral width;
- held-out experimental validation of a disorder-width law near inversion;
- a joint treatment of electron-phonon shifts and alloy broadening that distinguishes spectral, optical, transport, and topological transition criteria;
- a demonstrated temperature dependence of the disorder correlation length or local gap distribution in HgCdTe.

## 4. Revised claim boundary

The broad claim

> disorder matters near the HgCdTe inversion transition

is established.

The claim

> a single sharp scalar gap is always sufficient near inversion

is not defensible without a resolution check.

The narrower candidate contribution is a joint analytical output

$$
\boxed{
\left\{
\bar E_g(x,T),
\Gamma_g(x,T),
\xi_g(x,T)
\right\}
}
$$

or an equivalent spectral-moment representation, where:

- $\bar E_g$ is the disorder-averaged signed edge separation;
- $\Gamma_g$ is an operational spectral or distribution width;
- $\xi_g$ is a correlation or coarse-graining length when identifiable.

The model must state whether the width describes:

- local composition statistics;
- quasiparticle linewidth;
- optical Urbach or edge broadening;
- disorder-averaged density of states;
- sample-to-sample composition variation.

These are not interchangeable.

## 5. Required comparisons

Any future SQS, CPA, or SCBA result should be compared against:

1. virtual-crystal or mean-parameter $E_g(x,T)$;
2. unfolded supercell spectral weight;
3. disorder-renormalized mass from a reduced Kane model;
4. optical-edge width or tail measurements;
5. specimen-level composition metrology and gradients;
6. the empirical-temperature eight-band null model.

## 6. Stop rule

Do not begin SQS electron-phonon calculations merely to show that random alloys broaden bands.

A disorder calculation is justified only when it is designed to determine one unresolved quantity, such as:

- whether $\Gamma_g$ is comparable to $|\bar E_g|$ in the target inversion window;
- whether disorder changes the sign of the effective mass before the clean mean gap closes;
- whether a measured optical tail can be predicted from independently measured composition statistics;
- whether configuration-to-configuration spread dominates the proposed non-gap electron-phonon invariant.

If existing optical and composition data already bound the width below the model-separation scale, deeper alloy calculations should stop.

## Primary sources

- O. Rubel, A. Bokhanchuk, S. J. Ahmed, and E. Assmann, “Unfolding the band structure of disordered solids: from bound states to high-mobility Kane fermions,” *Physical Review B* **90**, 115202 (2014), arXiv:1405.4218.
- S. S. Krishtopenko, M. Antezza, and F. Teppe, “Disorder-induced topological phase transition in HgCdTe crystals,” *Physical Review B* **106**, 115203 (2022), arXiv:2206.14561.
