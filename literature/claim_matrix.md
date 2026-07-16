# Claim-level prior-art matrix

**Issue:** #2  
**Status:** initial breadth-first classification; not a completed novelty opinion  
**Classification labels:** `established`, `incremental`, `uncertain`, `candidate novel`

A contribution is classified at the level of a precise claim, not by whether the project as a whole feels new.

## Current matrix

| ID | Proposed claim or contribution | Current class | Evidence already identified | Main missing search |
|---|---|---|---|---|
| C01 | Decompose $E_g(T)$ into Fan, Debye–Waller, and quasiharmonic terms | established | Allen–Heine–Cardona and quasiharmonic literature | HgCdTe-specific implementation details |
| C02 | Use a Bose/Einstein-oscillator expression rather than an exactly linear temperature term | established generally | semiconductor gap-renormalization models | whether already fitted systematically to HgCdTe across $x$ |
| C03 | Calculate electron–phonon band-edge shifts for HgCdTe | established or incremental | historical HgCdTe electron–phonon calculation reported in secondary search | acquire and audit the primary paper |
| C04 | Project a finite-temperature self-energy into an 8-band Kane basis | uncertain | generalized matrix AHC and standard Kane downfolding exist separately | direct prior example for HgTe/HgCdTe or another narrow-gap system |
| C05 | Derive $T$-dependent $E_g,\Delta,P,F,\gamma_i$ from matrix AHC | candidate novel, unconfirmed | no direct HgCdTe example yet entered | exhaustive k·p/self-energy/downfolding search |
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
