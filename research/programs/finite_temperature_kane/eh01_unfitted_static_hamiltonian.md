# EH01 — unfitted static inversion Hamiltonian (research start)

**Status:** mathematical null model implemented; first-principles provenance and independent validation NOT COMPLETE. This is not a new HgCdTe material prediction, and no manuscript claim is authorized.

**Controlling issue:** [#412](https://github.com/Kajin-0/MCT-research/issues/412). Parent program R02; no change to frozen finite-temperature AHC/EPW states.

## Target observable and sign
At zero temperature, and at a declared lattice, strain, XC functional and pseudopotential state, define

\[
D(x)=E_{\Gamma_6}(x)-E_{\Gamma_8}(x).
\]

Negative D is the inverted Gamma ordering. This **is not generally the fundamental optical gap, indirect overlap, sorted eigenvalue-band-count gap or coarse alloy supercell HO/LU proxy**. For a disordered supercell, Gamma6/Gamma8 symmetry labels are not exact primitive-cell irreducible representations: use a qualified character projection / spectral unfolding.

The full scientific target is a physically meaningful, symmetry-constrained **8x8 Kane effective Hamiltonian** \(\mathcal H(\mathbf k,x)\), including Gamma6/Gamma8/Gamma7, not a falsely exact two-band scalar model. Existing implementation: \`src/mct_research/kane8.py\`.

## Executable null model
Let \(A=D(0)\) be the HgTe signed Gamma separation, \(C=D(1)\) the CdTe signed Gamma separation, and \(b\) an **unprovided** signed bowing coefficient in eV:

\[
D(x)=(1-x)A+xC-bx(1-x)
=A+(C-A-b)x+bx^2.
\]

With \(b=0\), the critical composition, if the endpoints straddle zero, is

\[
x_c=-A/(C-A).
\]

For \(b\ne0\), solve the quadratic robustly and report all physical roots. The implementation rejects degenerate, no-transition and nonunique sensitivity cases. It does not estimate b from an untrusted SQS grid proxy, and does not mix endpoints from unrelated functionals.

Let \(S=\partial D/\partial x = C-A-b(1-2x_c)\). At a **single, simple** transition, implicit differentiation gives

\[
\frac{\partial x_c}{\partial A}=-\frac{1-x_c}{S},\quad
\frac{\partial x_c}{\partial C}=-\frac{x_c}{S},\quad
\frac{\partial x_c}{\partial b}=\frac{x_c(1-x_c)}{S}.
\]

For covariance \(\Sigma_{A,C,b}\) in eV squared, the *local linearized* variance is \(\nabla x_c^\top\Sigma\nabla x_c\). This excludes systematic functional bias, ambiguity in Gamma character and any long-tailed input posterior; no "95% DFT confidence interval" follows without additional calibration.

### Scale demonstration, NOT a new prediction
Using literature-scale illustrative values \(A=-0.27\) eV and \(C=+1.34\) eV (do not substitute for consistently sourced project HSE endpoints):

| Assumed b (eV) | x_c from null model |
|---:|---:|
| -0.20 | 0.15171462 |
| 0 | 0.16770186 |
| +0.20 | 0.18655291 |

A physically plausible uncertainty in unmeasured bowing can therefore move x_c by order 0.01. Agreement of the endpoint-linear value with the known ~0.17 crossing cannot by itself establish predictive power, and the underlying crossing has been studied for decades.

## Existing first-principles assets and critical limitations
- \`Kajin-0/DFT\` QE PBE+SOC raw outputs/provenance exist for binary endpoints and a **single** 40-atom x=0.20 SQS seed. On its main branch, reported CdTe gap is +0.3041 eV, HgTe overlap -0.0020 eV, and 40-atom alloy sampled gap proxy +1.2192 eV. These are **not** symmetry-resolved HSE endpoints/held-out alloy gaps; do not feed them into the null model as material D(x).
- A previously reported HgTe HSE+SOC Gamma separation -289.587 meV and x=0.125 VCA partial HSE+SOC SCF have not been verified here against archived raw runs; label provenance UNKNOWN until recovered. The x=0.125 run is not a converged alloy validation point.
- \`MCT-research\` already supports Kane Hamiltonians, symmetry checks and gauge/matrix projection. Do not rebuild those foundations without a concrete deficiency.

## What is and is not novel
Not novel:
1. A composition-dependent Kane gap formula alone.
2. Extracting Kane parameters from DFT: see [DFT2kp (2024)](https://arxiv.org/abs/2306.08554), including HgTe and CdTe.
3. The critical x near 0.17: see [Nicklas & Wilkins (2011)](https://doi.org/10.1103/PhysRevB.84.121308) and [Teppe et al. (2016)](https://doi.org/10.1038/ncomms12576).
4. Explicit electronic structure of x=0.25 alloys: see [JAP 135 114502 (2024)](https://doi.org/10.1063/5.0187006).

Possible novel direction **only if independently demonstrated**: no-experimental-gap-fit transfer of chemically interpretable, symmetry-resolved low-energy Hamiltonian invariants across composition, with mechanism-resolving nonlinearity/disorder correction, independent DFT and spectroscopy validation, and calibrated uncertainty.

## Gate sequence
**G0: provenance**. Recover raw, hash-identifiable HSE+SOC binary endpoint inputs/outputs and any alloy result; check spinor SOC, functional/PP family, lattice, k-sampling, gap sign, irrep projections, SCF and basis convergence. No new production DFT runs.

**G1: analytical benchmark**. Compare endpoint linear null and bowed null. Verify numerical root, derivatives, covariance, eight-band Gamma embedding and gauge/symmetry conventions. Do not use external data to choose a successful b ex post.

**G2: invariant extraction**. Obtain consistent Gamma energies **and wavefunction/momentum-matrix information** to determine Kane interband couplings: eigenvalues alone do not fix a DFT-derived \(P\). Compare one-P/two-P model closure and remote-band correction. Only launch justified new DFT after a separate compute gate.

**G3: held-out validation**. Freeze model before x-compositions or experimental samples withheld for testing. Quantify numerical, pseudopotential, XC, lattice and alloy-configurational uncertainties separately. The sample list x=0.125,0.20,0.25 is a **candidate** schedule, not proof that any usable data exist.

**G4: publication review**. Aspirational benchmarks: RMSE <=25 meV on trusted held-out signed Gamma gaps, absolute critical composition error <=0.02 versus independent reference with uncertainty materially smaller than the target, demonstrated improvement over both nulls, and an explanatory microscopic result. If uncertainty, external data scarcity or existing prior art prevents discrimination, report NO-GO rather than declare novelty.

## Reproduction
\`src/mct_research/inversion_baseline.py\` and \`tests/test_inversion_baseline.py\` contain no fitted material constants. At the working branch head, run \`python -m pytest -q tests/test_inversion_baseline.py\` in an installed repo. Local standalone algebra checks passed 14 cases; full in-repository Kane integration and CI verification remain pending.

**Resource constraint:** $0 new spending, no HSE SQS/large calculations without a decision-changing measurement and bounded computation memo.
