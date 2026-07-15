# First-principles execution stack

**Status:** provisional computational design  
**Purpose:** define the smallest credible path from code verification to a finite-temperature HgCdTe analytical model  
**Novelty status:** none claimed

## 1. Governing principle

The first material calculation should be split into two distinct validation stages:

1. **CdTe code-verification stage** — a normal, finite-gap polar semiconductor where diagonal band-edge AHC is comparatively well conditioned.
2. **HgTe scientific stress test** — an inverted, narrow-gap system where matrix-valued, frequency-dependent self-energy and symmetry-preserving state tracking are essential.

Starting only with HgTe would conflate numerical implementation errors with genuine small-denominator, band-inversion, and wavefunction-renormalization effects.

The staged sequence is therefore

$$
\boxed{
\mathrm{CdTe}
\rightarrow
\mathrm{HgTe}
\rightarrow
\mathrm{Hg}_{1-x}\mathrm{Cd}_x\mathrm{Te}\ \mathrm{VCA}
\rightarrow
\mathrm{Hg}_{1-x}\mathrm{Cd}_x\mathrm{Te}\ \mathrm{SQS/CPA}
}.
$$

## 2. Required physical content

A production calculation must include or explicitly bound the error from:

- fully relativistic spin–orbit-coupled electronic states;
- phonons and electron–phonon matrix elements from DFPT or an equivalent validated method;
- dynamical Fan–Migdal denominators;
- Debye–Waller self-energy;
- long-range polar/Fröhlich coupling;
- thermal expansion without double counting;
- matrix-valued self-energy in the low-energy band manifold;
- gauge alignment and symmetry restoration;
- numerical covariance and convergence uncertainty.

A Fan-only calculation is not an acceptable final result. Fan and Debye–Waller terms can be individually large and partially cancelling, so agreement from one term alone may be accidental.

## 3. Recommended software roles

No single code should be trusted as the sole implementation reference.

### ABINIT

Use as one independent DFPT/AHC implementation for:

- phonons;
- Fan and Debye–Waller band renormalization;
- adiabatic and nonadiabatic comparisons where supported;
- direct convergence benchmarks on coarse and intermediate grids.

### Quantum ESPRESSO

Use as an independent ground-state and DFPT implementation with the same or closely matched fully relativistic norm-conserving pseudopotentials.

### EPW/Wannier interpolation

Use for:

- dense electron and phonon interpolation;
- spinor electron–phonon coupling where validated;
- long-range polar interpolation;
- frequency-dependent self-energy and spectral functions;
- efficient evaluation on dense meshes.

EPW output should not be treated as a complete AHC result unless the Debye–Waller contribution is supplied consistently and validated against the direct DFPT implementation.

### Repository projection layer

Use `mct_research` for:

- gauge alignment into the declared Kane basis;
- principal-angle diagnostics;
- symmetry restoration;
- covariance-weighted projection;
- one-$P$ versus two-$P$ closure testing;
- parameter uncertainty and correlation;
- $k$-window stability analysis.

## 4. Pseudopotential and basis requirements

The pseudopotential campaign must test the sensitivity to:

- Hg semicore states, especially $5d$;
- Cd semicore states, especially $4d$;
- Te semicore treatment where relevant;
- fully relativistic versus scalar-relativistic-plus-SOC constructions;
- nonlinear core corrections;
- plane-wave cutoff;
- transferability across equilibrium and thermally expanded volumes.

The same valence partition should be used for the binary endpoints whenever possible. A pseudopotential that reproduces a static gap by cancellation but gives incorrect phonons or dielectric response is unsuitable for the AHC stage.

## 5. Stage A — Static binary endpoint validation

For CdTe and HgTe, converge:

- equilibrium lattice constant;
- bulk modulus;
- phonon stability and frequencies;
- dielectric constants and Born effective charges;
- $\Gamma_6$, $\Gamma_8$, and $\Gamma_7$ ordering;
- signed gap $E_g$;
- spin–orbit splitting $\Delta$;
- near-$\Gamma$ dispersion and Kane parameters.

Use at least two electronic starting points:

1. a semilocal SOC calculation used consistently for DFPT/AHC;
2. a higher-level static reference such as a validated hybrid functional, mBJ, or quasiparticle correction.

A scalar scissors shift must not be assumed harmless for HgTe. The Fan denominators, state character, and proximity of inverted bands can depend on the full corrected Hamiltonian, not only the final zone-center gap.

## 6. Stage B — CdTe AHC verification

CdTe is the code-verification material.

### Required calculations

For the band edges and split-off state, calculate separately:

$$
\Delta E_r^{\mathrm{Fan}}(T),
\qquad
\Delta E_r^{\mathrm{DW}}(T),
\qquad
r\in\{\Gamma_6,\Gamma_8,\Gamma_7\}.
$$

Compare:

- adiabatic and nonadiabatic Fan terms;
- direct and interpolated Brillouin-zone integration;
- polar correction on and off;
- ABINIT and QE/EPW implementations;
- fixed-volume and quasiharmonic contributions.

### Acceptance targets

- numerical uncertainty in each final band-edge shift below $1\ \mathrm{meV}$;
- independent-code difference below $2\ \mathrm{meV}$ or explicitly explained;
- stable total gap correction under mesh, broadening, empty-band, and polar-cutoff convergence;
- Fan and Debye–Waller decomposition reproducible within the declared convention;
- low-temperature zero-point renormalization separated from the finite-temperature increment.

The point of this stage is not to optimize agreement with experiment. It is to verify that the complete computational decomposition is internally reproducible.

## 7. Stage C — HgTe matrix AHC

HgTe is the scientific stress test.

The low-energy quasiparticle poles should be obtained from

$$
\det\left[
\hbar\omega I
-H_0(\mathbf k)
-\Sigma^{\mathrm{Fan}}(\mathbf k,\omega,T)
-\Sigma^{\mathrm{DW}}(\mathbf k,T)
\right]=0.
$$

The diagonal approximation must be compared against diagonalization of the self-energy matrix in a controlled band subspace. At minimum include the states mapping to

$$
\Gamma_6\oplus\Gamma_8\oplus\Gamma_7,
$$

plus enough remote bands to converge the downfolded result.

### Required diagnostics

- principal angles and minimum subspace overlap versus temperature and $\mathbf k$;
- zone-center symmetry residual;
- time-reversal residual;
- diagonal versus matrix Dyson solution;
- on-shell versus frequency-linearized solution;
- quasiparticle residues;
- linewidth matrix;
- dependence on remote-band window;
- dependence on static electronic starting point.

### Primary outputs

$$
E_g(T),\quad
\Delta(T),\quad
P_8(T),\quad
P_7(T),\quad
F(T),\quad
\gamma_1(T),\quad
\gamma_2(T),\quad
\gamma_3(T).
$$

The result should also report the conventional constrained quantity

$$
P_{1P}(T)=\frac{2P_8(T)+P_7(T)}{3}
$$

under the current unweighted Frobenius convention, together with the covariance-weighted generalization.

## 8. Stage D — Thermal expansion

Use one of two non-double-counting protocols.

### Fixed-volume decomposition

$$
H(T)=H[V_0]+\Sigma^{\mathrm{ep}}[T;V_0]
+\left(H[V(T)]-H[V_0]\right).
$$

### Volume-consistent calculation

$$
H(T)=H[V(T)]+\Sigma^{\mathrm{ep}}[T;V(T)].
$$

The second protocol must not receive an additional thermal-expansion shift.

For the initial binary study, compute several volumes around equilibrium and obtain the gap and Kane-parameter deformation derivatives. The quasiharmonic volume curve can then be incorporated after the fixed-volume electron–phonon calculation is converged.

## 9. Stage E — Alloy hierarchy

### Virtual-crystal stage

Use a virtual-crystal or interpolated dynamical-matrix model only as a controlled pipeline test. It cannot establish final disorder physics.

### SQS stage

For detector-relevant compositions, use multiple statistically independent SQS configurations. Each configuration requires:

- static SOC electronic structure;
- local structural relaxation under a declared constraint;
- unfolded low-energy spectral weight;
- phonons or a justified local-mode approximation;
- configuration-resolved electron–phonon response where computationally feasible.

Average the Green functions or spectral functions when possible, rather than only averaging scalar gaps.

### Macroscopic symmetry restoration

After configuration averaging, apply the explicit cubic symmetry projection. Report both the restored mean and the removed configuration-dependent norm.

## 10. Temperature and composition grid

### Binary temperatures

$$
T=0,\ 25,\ 50,\ 77,\ 100,\ 150,\ 200,\ 250,\ 300\ \mathrm{K}.
$$

The denser low-temperature grid is needed to test the predicted departure from exact linearity.

### Initial alloy compositions

$$
x=0.15,\ 0.18,\ 0.20,\ 0.22,\ 0.25,\ 0.30,\ 0.40.
$$

Near the critical composition, refine adaptively where the predicted signed gap is comparable to the disorder width or model uncertainty.

## 11. Convergence ledger

Every reported temperature-dependent parameter should carry a structured error budget:

$$
\sigma_p^2
=
\sigma_{k/q}^2
+\sigma_{\mathrm{bands}}^2
+\sigma_{\mathrm{cutoff}}^2
+\sigma_{\mathrm{PP}}^2
+\sigma_{\mathrm{gauge}}^2
+\sigma_{\mathrm{sym}}^2
+\sigma_{\mathrm{fit}}^2
+\sigma_{\mathrm{window}}^2
+\sigma_{\mathrm{starting\ point}}^2.
$$

Not every contribution is statistically independent. The equation is an organizational ledger, not a license to add correlated errors blindly in quadrature.

## 12. Decision gates

### Gate A — CdTe code agreement

Proceed to HgTe only after the complete Fan + Debye–Waller gap correction is reproducible across two implementations within the target uncertainty.

### Gate B — HgTe matrix necessity

Determine whether the diagonal and matrix Dyson solutions differ by more than the numerical floor. If not, retain the simpler model but document the null result.

### Gate C — Kane closure

Determine whether a one-$P$ or two-$P$ static Hamiltonian predicts held-out matrices and dispersions within propagated uncertainty.

### Gate D — Analytical reduction

Only after the full temperature curves are validated should the mode-resolved response be reduced to an oscillator or spectral-moment equation.

## 13. Immediate executable next task

Construct a machine-readable import format for external projected matrices containing:

- composition;
- temperature;
- volume;
- $\mathbf k$;
- complex Hamiltonian or self-energy matrix;
- basis overlaps with the Kane reference;
- covariance or replicate information;
- electronic and phonon convergence metadata;
- and provenance hashes.

Then run a synthetic end-to-end test that deliberately introduces:

- random degenerate-subspace gauges;
- finite-SQS symmetry breaking;
- correlated matrix noise;
- and a known one-$P$ or two-$P$ temperature trend.

The pipeline should recover the injected physical parameters and correctly assign the remaining effects to gauge, symmetry, covariance, or model-closure residuals.
