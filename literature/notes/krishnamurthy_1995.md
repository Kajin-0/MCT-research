# Krishnamurthy et al. (1995) - HgCdTe electron-phonon gap shifts

## Bibliographic record

S. Krishnamurthy, A.-B. Chen, A. Sher, and M. Van Schilfgaarde, “Temperature dependence of band gaps in HgCdTe and other semiconductors,” *Journal of Electronic Materials* **24**, 1121-1125 (1995). DOI `10.1007/BF02653063`.

**Primary copy:** owner-supplied PDF audited visually; exact source hash recorded in `literature/papers/README.md`  
**SHA-256:** `790994754e9d0137e48be7f62fb1fe23ff51e203d78059b65120b0f4122c283b`  
**Full-text audit status:** initial method and claim audit complete; numerical reproduction pending.

## Method actually used

The paper is not a modern density-functional AHC calculation. It uses a hybrid empirical-pseudopotential/tight-binding (HPTB) Hamiltonian:

- empirical pseudopotential form factors plus a minimum $sp^3$ tight-binding correction;
- an added site-diagonal spin-orbit Hamiltonian;
- band-structure parameters tuned to experiment;
- a valence-force-field dynamical matrix for phonons;
- first and second derivatives of interatomic matrix elements with respect to atomic displacement.

The band shift is written as a first-order expectation value of the second-order displacement potential plus a second-order sum over the first-order displacement potential. In modern language, this contains Debye-Waller-like and Fan-like contributions, although the paper does not formulate the calculation as a contemporary matrix-valued AHC workflow.

Additional verified details:

- both first- and second-displacement terms are retained to preserve symmetry;
- all phonon branches are included;
- polar coupling is included in the longitudinal-optical contribution;
- direct-gap shifts are evaluated at $k=0$;
- nonzero-$k$ and full-zone sums are used for effective-mass or indirect-gap changes;
- the electronic bands entering the perturbation theory are zero-temperature bands rather than self-consistently renormalized finite-temperature bands;
- the authors explicitly state that higher-order perturbation and finite-temperature renormalized bands would be needed at higher temperature.

The paper separately discusses lattice dilation. It formulates the dilation contribution using thermal expansion, bulk modulus, and pressure dependence from the literature; the quoted heterojunction band-offset change explicitly excludes the dilation contribution.

## HgCdTe results verified from the full text

For approximately $\mathrm{Hg}_{0.78}\mathrm{Cd}_{0.22}\mathrm{Te}$:

- the direct gap increases with temperature;
- calculated gap changes are typically within about 10-15 meV of the experimental curves shown;
- the zero-point correction is reported as 13.6 meV;
- both $E_c$ and $E_v$ move downward, with $E_v$ moving farther so that the gap increases;
- acoustic phonons contribute about 75% of the calculated band-edge shifts at 300 K;
- polar LO phonons do not dominate because relevant interband matrix elements are suppressed by selection rules;
- temperature-dependent gap, effective mass, and hyperbolic-band parameters are tabulated;
- the calculated valence-band offset between the alloy and CdTe changes substantially with temperature in the electron-phonon-only estimate.

The full paper also confirms the abstract-level result that the general trends agree with experiment for the studied materials, while InAs and InSb gap changes are underestimated by roughly a factor of two.

## Claim impact

The following are established prior art and cannot support novelty by themselves:

- perturbative electron-phonon calculation of HgCdTe band-edge shifts;
- calculation of HgCdTe $E_g(T)$ from an electronic and phonon Hamiltonian;
- separate conduction- and valence-edge temperature shifts;
- phonon-branch and intermediate-band decomposition of the scalar edge shifts;
- zero-point gap correction;
- temperature-dependent electron effective mass and related nonparabolic parameters;
- temperature-dependent valence-band-offset estimates.

Potentially differentiating claims remain narrower:

- a full complex, frequency-dependent matrix self-energy rather than only band-energy corrections;
- projection into a fixed complete $\Gamma_6\oplus\Gamma_8\oplus\Gamma_7$ 8-band Kane manifold;
- extraction and closure testing of $P$, $F$, $\gamma_i$, and separate effective $P_8/P_7$;
- modern nonadiabatic polar convergence and momentum-dependent Debye-Waller treatment;
- disorder-aware alloy averaging and spectral broadening near inversion;
- uncertainty-aware analytical compression with held-out experimental validation.

## Important limitations of the 1995 work

The primary text does not establish:

- a first-principles quasiparticle calculation;
- a gauge-fixed 8-by-8 self-energy matrix;
- off-diagonal self-energy projection into Kane parameters;
- separate finite-temperature renormalization of the full standard 8-band parameter set;
- SQS/CPA disorder broadening near the zero-gap transition;
- nonadiabatic dense-grid convergence of the long-range polar interaction;
- coefficient covariance or uncertainty propagation;
- held-out predictive validation across composition.

Spin is included in the electronic structure, but the tabulated band-by-band decomposition is spin averaged. This is materially different from demonstrating closure of the complete spinor Kane Hamiltonian.

## Next reproducibility tasks

1. digitize Fig. 1 and Table II for $\mathrm{Hg}_{0.78}\mathrm{Cd}_{0.22}\mathrm{Te}$;
2. reconstruct the HPTB and valence-force-field parameters from the cited predecessor papers;
3. separate the electron-phonon and dilation contributions quantitatively;
4. map the paper's two perturbative terms onto modern Fan/Debye-Waller notation without overstating equivalence;
5. compare its scalar $E_g(T)$ and effective-mass predictions against Hansen, Laurenti, and modern magnetospectroscopy;
6. document exactly which quantities cannot be recovered without the original code or parameter files.
