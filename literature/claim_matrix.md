# Claim-level prior-art matrix

**Issue:** #2  
**Status:** breadth-first classification in progress; not a completed novelty opinion  
**Classification labels:** `established`, `incremental`, `uncertain`, `candidate novel`

A contribution is classified at the level of a precise claim, not by whether the project as a whole feels new.

## Current matrix

| ID | Proposed claim or contribution | Current class | Evidence already identified | Main missing search or validation |
|---|---|---|---|---|
| C01 | Decompose $E_g(T)$ into electron–phonon and quasiharmonic terms | established | Allen–Heine–Cardona literature; Krishnamurthy 1995 explicitly treats electron–phonon interaction and separately discusses lattice dilation | exact modern Fan/Debye–Waller/quasiharmonic decomposition for HgTe, CdTe, and HgCdTe |
| C02 | Replace Hansen's exactly linear temperature term with a nonlinear low-temperature thermal law | established in HgCdTe | Laurenti 1990 derives a composition-dependent Varshni form $T^2/[T+B(x)]$ from primary absorption-edge data | independent out-of-sample comparison of Laurenti with modern composition-calibrated datasets |
| C03 | Calculate electron–phonon band-edge shifts and temperature-dependent gaps for HgCdTe | established in HgCdTe | Krishnamurthy et al. 1995 calculate band-edge shifts, gap, band offsets, hyperbolic dispersion parameters, and effective mass | modern first-principles comparison and uncertainty analysis |
| C04 | Project a finite-temperature matrix self-energy into an 8-band Kane basis | uncertain | generalized matrix AHC and static symmetry-adapted k.p extraction/downfolding are established separately | direct prior finite-temperature full-matrix example for HgTe/HgCdTe or another narrow-gap system |
| C05 | Derive $T$-dependent $E_g,\Delta,P,F,\gamma_i$ from matrix AHC | candidate novel, unconfirmed and narrower | Krishnamurthy already gives $E_g(T)$, electron mass, and two hyperbolic dispersion parameters; DFT2kp establishes complete static CdTe extraction | determine whether prior work renormalizes the complete symmetry-resolved Kane Hamiltonian or momentum/Luttinger parameters with temperature |
| C06 | Resolve the complete CdTe linear invariant space and quantify the two-$P$ reduction | established structure; independent repository reproduction | DFT2kp publishes four CdTe linear coefficients; repository projector gives four one-dimensional sectors and reduces the two-$P$ residual from approximately 0.82018% to approximately $2\times10^{-7}$ | explicit coefficient/gauge mapping and independent numerical convergence |
| C07 | $P_{\mathrm{fit}}=(2P_8+P_7)/3$ under the declared Frobenius metric | derived but metric-specific; novelty not supported | exact repository derivation; multi-coupling zincblende Hamiltonians are prior art | retain only as an internal reduction identity |
| C08 | Temperature primarily changes $E_g$ while Kane velocity remains nearly constant | established experimentally over measured ranges | Teppe et al. 2016 report $\tilde c=(1.07\pm0.05)\times10^6$ m/s for two near-critical samples | broader composition, strain, temperature, and complete-8-band limits |
| C09 | Average cubic symmetry permits a true $\Gamma_6$–$\Gamma_8$ crossing and forbids generic mixing at $\Gamma$ | established representation theory | zincblende double-group symmetry | disorder/strain exceptions |
| C10 | Use multiple SQS configurations and restore average cubic symmetry | established methodology | SQS and group averaging are standard | HgCdTe electron–phonon application |
| C11 | Treat the inversion region through a disorder-averaged spectral function rather than one sharp gap | uncertain to incremental | alloy spectral functions and CPA are established generally; Laurenti discusses CPA consistency at the band edge | HgCdTe-specific temperature-dependent inversion treatment with quantified broadening |
| C12 | Derive a compact composition-dependent spectral-moment model from the gap-coupling spectrum | candidate novel, unconfirmed and narrowed | Laurenti already supplies nonlinear composition-dependent thermal curvature; oscillator reductions are established generally | prior HgCdTe spectral-moment equations and proof of held-out improvement beyond Laurenti |
| C13 | Outperform Hansen and Laurenti under leave-one-composition-out and held-out-temperature validation | empirical result, not yet established | common protocol defined; Hansen Table I and selected later values recovered | complete source-level datasets, uncertainties, and independent composition calibration |
| C14 | Propagate matrix covariance through gauge alignment and invariant fitting | implementation requires correction before statistical claims | deterministic linear transforms are valid for a fixed gauge, but the current 128-real-component storage duplicates an 8x8 Hermitian matrix's 64 independent real degrees of freedom | implement an independent-Hermitian 64D covariance schema and include gauge uncertainty |
| C15 | A diagonal self-energy table is insufficient to validate a finite-temperature Kane Hamiltonian | established information-content statement | dimensional/information argument | application examples useful but not required for principle |
| C16 | Near inversion, composition uncertainty must be propagated as uncertainty in the explanatory variable | established statistical necessity; HgCdTe consequence quantified here | exact sensitivity $dT_c/dx=-(\partial_xE_g)/(\partial_TE_g)$ and primary papers showing percent-level composition revisions | source-specific composition-error distributions |
| C17 | A resolved finite-$T$ turnover in $E_g(T)$ requires competing signed thermal channels and cannot be represented by Hansen, Laurenti, or one fixed-sign oscillator | mathematical limitation established; HgCdTe occurrence uncertain | monotonicity proof; Krishnamurthy Table II contains a shallow 1–20 K decrease followed by an increase | high-precision low-temperature experiment and modern calculation establishing whether the approximately 1 meV feature is physical |
| C18 | Construct the complete ten-dimensional zincblende quadratic invariant space and extract CdTe coefficients | established prior art | Weiler/Trebin classes; DFT2kp publishes a complete ten-coefficient CdTe Hamiltonian | convention mapping only; not a novelty target |
| C19 | Show that the conventional tied four-dimensional quadratic Kane/Luttinger model fails for CdTe | candidate comparative diagnostic, not a new Hamiltonian | selected-band polar reconstruction gives approximately 28.7% training and 33.2% [110] error; independently published DFT2kp coefficients also strongly reject the tied subspace | complete gauge audit, numerical convergence, and a held-out physical observable |
| C20 | Five established quadratic departure directions suffice while $N_2$ is negligible | current smoke result; not universal | selected-band polar reconstruction reduces the worst residual to approximately 0.201% with $G,G',\delta\gamma_1,\delta\gamma_2,\delta\gamma_3$; DFT2kp gives the same qualitative hierarchy | reproduce after implementation correction, gauge mapping, and independent numerical setup |
| C21 | The all-state overlap reconstruction is a valid downfolded eight-band Hamiltonian | falsified | in the complete-state limit the formula converges to $P_\Gamma H(\mathbf k)P_\Gamma$; archived matrices miss selected eigenvalues by 0.55–1.03 meV at $|k|=0.01\ \AA^{-1}$ with $k^2$ scaling | replace with selected-band polar/ispectral reconstruction and add a two-level falsification test |
| C22 | Individual finite-k quadratic coefficients are unique material observables | uncertain and generally gauge-dependent | selected-band polar transport defines one auditable gauge, while smooth $k$-dependent unitaries preserve energies but can change matrix coefficients | quantify allowed gauge variation and prioritize gauge-invariant observables/subspace distances |

## Hansen empirical baseline: primary-paper audit

Hansen, Schmit, and Casselman combine a heterogeneous historical evidence base rather than one uniform experiment:

- data from 22 different studies;
- practical fit support over approximately $0\le x\le0.6$, plus CdTe;
- temperatures from 4.2 to 300 K;
- optical criteria including $\alpha=500$ and $1000\ \mathrm{cm^{-1}}$, half-peak detector cutoff, and 50% detector cutoff;
- several magneto-optical methods;
- composition from density, transmission cutoff, vendor calibration, and destructive chemistry;
- four low-$x$ Schmit–Stelzer samples excluded for mercury inclusions;
- selected Weiler compositions revised using additional measurements.

Their staged fitting procedure first fits a linear temperature slope for each temperature-dependent sample, then fits slope versus composition, normalizes data to 80 K, and finally fits the composition dependence. The paper reports a 13 meV standard error of estimate and describes the high-Cd composition dependence beyond roughly $x=0.6$ as conjectural.

Consequences:

1. Hansen is a cross-source engineering regression, not a uniform fundamental-gap measurement.
2. Its 13 meV error scale must be retained when evaluating claimed improvements.
3. Modern sub-meV or few-meV comparisons require source, composition, and observable uncertainty that the published equation does not provide.
4. The complete underlying source dataset still requires reconstruction even though the primary paper is now available.

## HgCdTe-specific electron–phonon prior art

Krishnamurthy, Chen, Sher, and Van Schilfgaarde (1995) use a hybrid pseudopotential tight-binding Hamiltonian with:

- empirical pseudopotential plus minimum $sp^3$ tight-binding basis;
- site-diagonal spin–orbit coupling;
- a valence-force-field phonon model;
- first- and second-displacement terms retained to preserve symmetry;
- all phonon branches, including the polar long-range contribution through the LO treatment;
- $k=0$ evaluation for direct gaps and broader Brillouin-zone treatment for masses and indirect quantities;
- zero-temperature electronic bands as the perturbative reference;
- a separately described lattice-dilation contribution.

For Hg$_{0.78}$Cd$_{0.22}$Te, the paper reports:

- a zero-point gap correction of 13.6 meV;
- calculated $E_g(T)$ from 1 to 600 K;
- hyperbolic conduction-band parameters $\gamma(T)$ and $c(T)$;
- an effective-mass ratio reaching 1.634 at 300 K relative to the low-temperature value;
- both conduction and valence edges moving downward, with the valence edge moving farther so the gap increases;
- major acoustic-phonon contributions at 300 K;
- an explicit warning that higher-order perturbation and finite-temperature-renormalized bands become important at high temperature.

Consequences:

1. scalar electron–phonon HgCdTe $E_g(T)$ is established;
2. finite-temperature dispersion and mass changes are established at a reduced-parameter level;
3. recalculating $E_g(T)$ or $m_e^*(T)$ alone is not novel;
4. the open target is a complete symmetry-resolved matrix self-energy and an auditable projection into the full 8-band parameter manifold;
5. any new analytical equation should be compared with the tabulated historical microscopic curve, not only with Hansen and Laurenti.

## Laurenti nonlinear thermal prior art

Laurenti et al. (1990) directly measured LPE Hg$_{1-x}$Cd$_x$Te samples primarily over $0.5\lesssim x\le1$ from approximately 2 to 300 K. They extracted the nonexcitonic interband edge using derivative-transmission spectra fitted with three-dimensional direct-allowed exciton theory, reporting edge accuracy better than approximately 3 meV.

Their final equation is

$$
E_g^{\mathrm L}(x,T)=
-0.303(1-x)+1.606x-0.132x(1-x)
+10^{-4}A(x)\frac{T^2}{T+B(x)},
$$

with

$$
A(x)=6.3(1-x)-3.25x-5.92x(1-x),
$$

$$
B(x)=11(1-x)+78.7x.
$$

The authors combine their Cd-rich measurements with selected Hg-rich literature data, apply average composition corrections of about 2.3% to reconcile historical series, state a nominal equation range $0\le x\le1$ and $0\le T\le500$ K, and identify a temperature-independent composition near $x=0.505$ with $E_g\approx0.628$ eV.

This establishes:

1. nonlinear low-temperature HgCdTe gap equations as prior art;
2. a composition-dependent effective thermal scale as prior art;
3. endpoint-interpolated thermal amplitudes with opposite HgTe/CdTe signs as prior art;
4. explicit composition adjustment as part of historical model construction;
5. the requirement that a new model beat Laurenti under held-out, composition-aware tests rather than only fit the same compiled data.

## Signed-gap validation result

Teppe et al. 2016 provide a near-inversion constraint based on far-infrared magneto-transmission and Landau-level fitting:

- nominal $x=0.155$ reaches $E_g\approx0$ near 77 K;
- the Kane velocity remains approximately constant while signed gap and mass change sign;
- the analysis uses a reduced $\Gamma_6\oplus\Gamma_8$ model;
- the paper compares against Laurenti rather than Hansen.

At the nominal point, Hansen predicts $+9.21$ meV and $T_c\approx52$ K, whereas Laurenti predicts $-0.0478$ meV and $T_c=77.124$ K. The Laurenti agreement verifies the transcription because Teppe used Laurenti; it is not independent validation of Laurenti’s physical accuracy.

The higher-Cd Teppe sample is also labeled both $x=0.17$ and $x=0.175$. That difference shifts either historical equation by roughly 9 meV, demonstrating that composition provenance can dominate low-gap model rankings.

## Static k.p prior-art and method correction

The controlling static audit is recorded in:

```text
research/decision_records/2026-07-18-static-kane-method-audit.md
```

Nearest prior methods:

- DFT2kp, Cassiano et al., arXiv:2306.08554 / SciPost Physics Codebases 25 (2024);
- Jocić and Vukmirović (2020), symmetry-adapted ab-initio k.p construction;
- VASP2KP (2023), automatic symmetry and k.p extraction.

The audit establishes:

1. the complete linear space is four-dimensional, not the repository's former two-dimensional two-$P$ space;
2. the complete quadratic space is ten-dimensional and established prior art;
3. the all-state reconstruction converges to the bare $P_\Gamma H(\mathbf k)P_\Gamma$ block rather than an isospectral effective Hamiltonian;
4. the selected-eight polar construction preserves the target DFT bands exactly;
5. the corrected tied-quadratic failure is approximately 30–33%;
6. five established departure directions suffice at smoke level, while $N_2$ is negligible;
7. individual matrix coefficients require an explicit gauge definition and sensitivity audit.

The former approximately 49% residual, large $N_2$, all-six-required conclusion, and proposed 120-band run are superseded.

## Search clusters

### A. HgTe, CdTe, and HgCdTe finite-temperature electron–phonon work

Search for zero-point renormalization, complete Fan/Debye–Waller decomposition, nonadiabatic and Fröhlich corrections, temperature-dependent inversion, and binary-versus-alloy calculations.

### B. Temperature-dependent Kane parameters

Search separately for

$$
E_g,\quad \Delta,\quad P,\quad E_P,\quad F,\quad
\gamma_1,\gamma_2,\gamma_3,\quad v_K.
$$

Distinguish empirically inserted parameters from independently derived or measured finite-temperature parameters.

### C. Self-energy downfolding into $k\cdot p$

Search matrix electron–phonon self-energy, Löwdin/Schrieffer–Wolff downfolding, temperature-dependent effective Hamiltonians, quasiparticle $k\cdot p$, and renormalized momentum matrix elements.

### D. Analytical phonon-based gap equations

Audit Varshni, Bose–Einstein/O'Donnell–Chen, one- and two-oscillator, spectral-moment, quasiharmonic, and alloy-composition interpolation models.

### E. Disorder near the normal/inverted transition

Search CPA, SQS, unfolded spectral functions, local normal/inverted regions, gap distributions, Urbach tails, and disorder-driven transitions.

### F. Composition metrology and cross-source comparability

Search composition determination and gradients in bulk, LPE, and MBE HgCdTe; strain and substrate effects; source-level offsets; and whether reported $x$ was measured independently or inferred from a gap equation.

## Classification rules

A claim can move to `candidate novel` only when:

1. its exact mathematical and physical scope is stated;
2. the closest prior approaches are identified;
3. the difference is substantive rather than a software combination;
4. the result has a falsification test;
5. reproducible calculation or data analysis supports it;
6. negative and conflicting literature is included.

The phrase “first-principles” is not itself a novelty claim. Combining AHC and an 8-band model is not sufficient unless the projection produces a new verified result or resolves an existing HgCdTe limitation.
