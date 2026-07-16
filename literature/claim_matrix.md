# Claim-level prior-art matrix

**Issue:** #2  
**Status:** breadth-first classification in progress; not a completed novelty opinion  
**Classification labels:** `established`, `incremental`, `uncertain`, `candidate novel`

A contribution is classified at the level of a precise claim, not by whether the project as a whole feels new.

## Current matrix

| ID | Proposed claim or contribution | Current class | Evidence already identified | Main missing search |
|---|---|---|---|---|
| C01 | Decompose $E_g(T)$ into Fan, Debye–Waller, and quasiharmonic terms | established | Allen–Heine–Cardona and quasiharmonic literature | exact decomposition and approximations used in historical HgCdTe work |
| C02 | Use a Bose/Einstein-oscillator expression rather than an exactly linear temperature term | established generally | semiconductor gap-renormalization models | whether already fitted systematically to HgCdTe across $x$ |
| C03 | Calculate electron–phonon band-edge shifts and temperature-dependent gaps for HgCdTe | established in HgCdTe | Krishnamurthy et al., *J. Electron. Mater.* 24, 1121–1125 (1995), DOI `10.1007/BF02653063` | full-text audit of alloy model, phonon spectrum, Fan/DW treatment, thermal expansion, and numerical assumptions |
| C04 | Project a finite-temperature self-energy into an 8-band Kane basis | uncertain | generalized matrix AHC and standard Kane downfolding exist separately | direct prior example for HgTe/HgCdTe or another narrow-gap system |
| C05 | Derive $T$-dependent $E_g,\Delta,P,F,\gamma_i$ from matrix AHC | candidate novel, unconfirmed and now narrower | historical HgCdTe work already reports gap, band-edge, valence-offset, and electron-effective-mass temperature changes | determine whether any prior work renormalizes the complete Kane Hamiltonian or momentum/Luttinger parameters |
| C06 | Test one-$P$ closure against separate effective $P_8$ and $P_7$ | candidate methodological, unconfirmed | nested model derived and executable here | equivalent multi-coupling finite-$T$ Kane literature |
| C07 | $P_{\mathrm{fit}}=(2P_8+P_7)/3$ under the declared Frobenius metric | derived but metric-specific; novelty uncertain | exact repository derivation | prior invariant-projection literature |
| C08 | Temperature primarily changes $E_g$ while Kane velocity remains nearly constant | established experimentally over measured ranges | bulk HgCdTe magnetospectroscopy | limits across composition, strain, and temperature |
| C09 | Average cubic symmetry permits a true $\Gamma_6$–$\Gamma_8$ crossing and forbids generic mixing at $\Gamma$ | established representation theory | zincblende double-group symmetry | disorder/strain exceptions |
| C10 | Use multiple SQS configurations and restore average cubic symmetry | established methodology | SQS and group averaging are standard | HgCdTe electron–phonon application |
| C11 | Treat the inversion region through a disorder-averaged spectral function rather than one sharp gap | uncertain to incremental | alloy spectral functions and CPA are established generally | HgCdTe-specific inversion-transition treatment |
| C12 | Derive a compact composition-dependent spectral-moment model from the gap-coupling spectrum | candidate novel, unconfirmed | oscillator reduction established generally | prior HgCdTe analytical spectral-moment equations |
| C13 | Outperform Hansen under leave-one-composition-out and held-out-temperature validation | empirical result, not yet established | protocol defined here | reconstructed primary data and later independent datasets |
| C14 | Current matrix covariance propagation is exact conditional on a fixed estimated gauge | established linear uncertainty propagation | repository derivation and tests | uncertainty of the estimated gauge remains excluded |
| C15 | A diagonal self-energy table is insufficient to validate a finite-temperature Kane Hamiltonian | established information-content statement | dimensional/information argument | none required for principle; application examples useful |

## First HgCdTe-specific prior-art result

Krishnamurthy, Chen, Sher, and Van Schilfgaarde published “Temperature dependence of band gaps in HgCdTe and other semiconductors” in 1995. The publisher abstract states that the work:

- calculated electron–phonon-induced band-edge shifts for HgCdTe alloys;
- started from accurate zero-temperature band structures;
- reproduced experimental temperature variations of the gaps to better than 10% for the studied materials except InAs and InSb;
- found that both the conduction and valence band edges move downward with temperature;
- reported temperature changes of valence-band offsets and electron effective mass.

Consequences for this project:

1. a scalar electron–phonon explanation of HgCdTe $E_g(T)$ is established;
2. temperature-dependent electron effective mass is also established at least at the reported level;
3. novelty must lie beyond recalculating $E_g(T)$ or $m_e^*(T)$ alone;
4. the still-open distinction is whether the complete symmetry-resolved, frequency-dependent 8-band Hamiltonian has been derived and tested for closure;
5. the 1995 full text must be audited before claiming that its method omitted matrix self-energy, Debye–Waller completeness, nonadiabatic polar corrections, disorder, or quasiharmonic effects.

## Search clusters

### A. HgTe, CdTe, and HgCdTe finite-temperature electron–phonon work

Search for:

- zero-point renormalization;
- Fan and Debye–Waller decomposition;
- nonadiabatic or Fröhlich corrections;
- temperature-dependent band inversion;
- phonon-induced topological transitions;
- binary versus alloy calculations.

### B. Temperature-dependent Kane parameters

Search separately for each parameter:

$$
E_g,\quad \Delta,\quad P,\quad E_P,\quad F,\quad
\gamma_1,\gamma_2,\gamma_3,\quad v_K.
$$

Distinguish parameters inserted from empirical formulas from parameters derived or independently measured at finite temperature.

### C. Self-energy downfolding into $k\cdot p$

Search terms must include:

- matrix electron–phonon self-energy;
- Löwdin or Schrieffer–Wolff downfolding;
- temperature-dependent effective Hamiltonian;
- quasiparticle $k\cdot p$;
- electron–phonon-renormalized effective masses and momentum matrix elements;
- topological/narrow-gap semiconductors.

### D. Analytical phonon-based gap equations

Audit:

- Varshni;
- Bose–Einstein/O'Donnell–Chen forms;
- one- and two-oscillator fits;
- spectral-density and Eliashberg-moment reductions;
- quasiharmonic separation;
- composition interpolation for semiconductor alloys.

### E. Disorder near the normal/inverted transition

Search:

- CPA, SQS, unfolded spectral functions;
- local normal/inverted regions;
- gap distributions and Urbach tails;
- topological Anderson or disorder-driven transitions;
- HgCdTe compositional fluctuation broadening.

## Classification rules

A claim can move to `candidate novel` only when:

1. its exact mathematical and physical scope is stated;
2. the closest prior approaches are identified;
3. the difference is substantive rather than a software combination;
4. the result has a falsification test;
5. a reproducible calculation or data analysis supports it;
6. negative and conflicting literature is included.

The phrase “first-principles” is not itself a novelty claim. Neither is combining AHC and an 8-band model unless the projection produces a new verified result or resolves an existing HgCdTe limitation.
