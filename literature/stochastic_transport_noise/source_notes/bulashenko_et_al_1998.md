# Bulashenko et al. (1998) equation-level audit

**Source:** O. M. Bulashenko, G. Gomila, J. M. Rubí, and V. A. Kochelap, “Extension of the impedance field method to the noise analysis of a semiconductor junction: Analytical approach,” *Journal of Applied Physics* **83**, 2610–2618 (1998).  
**DOI:** `10.1063/1.367023`  
**Verification status:** user-supplied publisher PDF inspected in full; drift-diffusion operator, impedance-field expression, local source normalization, equilibrium decomposition, cross terms, and stated frequency limitations verified.

## 1. Scope

The paper derives an analytical impedance-field method for local and terminal voltage noise in a one-dimensional semiconductor junction when both drift and diffusion contribute. The worked structure is an inhomogeneous `n+–n` homojunction with nonuniform electric field and carrier density.

It is not a generation-recombination photoconductor theory. Its relevance to R06 is methodological:

- it provides an independent terminal-noise transfer formulation;
- it distinguishes primitive local source strength from terminal weighting;
- it demonstrates that electrostatic cross terms are required for equilibrium Nyquist consistency.

## 2. Stationary drift-diffusion model

The device current density is written in Eq. (2) as

\[
J=q\mu nE+qD\frac{dn}{dx}
+\frac{\varepsilon}{4\pi}\frac{\partial E}{\partial t},
\]

in the paper's Gaussian-unit convention.

The steady-state analysis uses drift and diffusion with Poisson electrostatics and permits field-dependent mobility and diffusivity. The example has a strongly inhomogeneous `n+–n` junction.

The paper then restricts the analytical noise calculation to frequencies low compared with dielectric relaxation, so the displacement-current term is neglected in deriving the impedance field. This is an explicit limitation: the complete current equation contains displacement current, but the published transfer solution is quasistatic in that sense.

## 3. Terminal impedance-field formula

For constant-current operation, the paper writes the terminal voltage PSD as Eq. (1):

\[
S_V
=A\int_{-L}^{L}
|\nabla Z(x)|^2K(x)\,dx,
\]

where:

- `A` is cross-sectional area;
- `K(x)` is the primitive local microscopic noise source;
- `\nabla Z(x)` is the scalar one-dimensional impedance field mapping a local current fluctuation to terminal voltage.

For equilibrium diffusion noise with weak carrier heating, the local source is

\[
K(x)=4q^2n(x)D(x)
\]

under the paper's one-sided convention.

The formulation is therefore the continuous adjoint analogue of the R06 resolvent expression

\[
H_y=C(i\omega M-J)^{-1}B+D.
\]

The paper's specific result is low-frequency and scalar, while R06 requires a full-frequency multi-state operator. The transfer principle itself is established prior art.

## 4. Impedance-field structure

The paper derives a closed analytical impedance field for the inhomogeneous drift-diffusion junction from the linearized transport equation. The weighting depends on:

- stationary density and electric-field profiles;
- differential conductivity;
- diffusion;
- junction asymmetry;
- contact-to-junction coupling.

The result can be decomposed into contributions associated with:

1. the homogeneous sample resistance;
2. the junction perturbation;
3. sample-contact or interface cross terms.

The exact decomposition is represented in the paper by the functions `s_1(x)`, `s_2(x)`, and `s_3(x)`.

## 5. Equilibrium Nyquist recovery

At equilibrium, Eq. (35) gives the separate local contributions. Their sum satisfies

\[
s_V^{eq}(x)=4k_BT R(x),
\]

where `R(x)` is the local differential resistance contribution.

The paper explicitly states that **all contributions, including the cross correlations, are necessary** to recover the Nyquist theorem. Near the junction/interface, the cross terms associated with electric-field fluctuations dominate substantial parts of the local terminal-noise contribution.

This is a direct acceptance requirement for R06:

- local conduction-noise sources alone are insufficient if electrostatic response and observation cross terms are omitted;
- an apparently positive local source map is not equivalent to a terminal contribution map;
- negative or cross contributions are physically required by the transfer decomposition.

## 6. Spatial interpretation

The paper's figures show that:

- primitive local source intensity follows local carrier density and diffusion;
- impedance weighting concentrates terminal sensitivity near the inhomogeneous junction;
- cross terms can be positive or negative;
- the total equilibrium contribution recovers the local resistance profile only after summation.

R06 visualizations must distinguish:

1. primitive source covariance;
2. adjoint/impedance weighting;
3. weighted diagonal contribution;
4. cross-correlation contribution;
5. total terminal PSD.

A statement that noise “originates” at a position is incomplete without specifying which of these quantities is plotted.

## 7. Direct implications for R06

### Established prior art

R06 cannot claim novelty for:

- impedance-field propagation of distributed semiconductor noise;
- analytical terminal-noise evaluation in a nonuniform one-dimensional drift-diffusion device;
- local terminal-contribution maps;
- field/source cross terms required for equilibrium Nyquist consistency;
- using an adjoint weighting field as an alternative to direct stochastic-state propagation.

### Required independent solver

Selected benchmarks must be evaluated by both:

1. direct resolvent covariance propagation;
2. adjoint/impedance-field propagation.

Agreement must be checked over frequency in the R06 formulation, even though the published Bulashenko solution is quasistatic relative to dielectric relaxation.

### Required equilibrium metric

Define

\[
\epsilon_{FDT}(\omega)
=
\frac{
|S_V^{model}(\omega)-4k_BT\operatorname{Re}Z(\omega)|
}
{4k_BT\operatorname{Re}Z(\omega)}.
\]

The error budget must separate:

- spatial discretization;
- linear-solver tolerance;
- source normalization;
- omitted cross terms;
- frequency-range violation of any quasistatic approximation.

## 8. Contact interpretation

The “sample-contact” and junction cross terms in this paper arise from an inhomogeneous drift-diffusion junction and its electrostatic transfer field. They are not a stochastic finite-surface-recombination boundary and do not supply forward/reverse contact exchange propensities.

Thus this paper does not close the R06 finite-contact covariance question.

## 9. Limitations relative to R06

- unipolar electron example;
- no optical generation;
- no explicit electron-hole-trap GR closure;
- no HgCdTe material specialization;
- no dynamic trap population;
- no finite stochastic surface-recombination boundary;
- analytical noise solution limited to frequencies below dielectric relaxation;
- primitive source is assumed from diffusion-noise theory rather than derived from a complete event network.

## 10. Mandatory benchmark

A reduced R06 implementation should reproduce:

1. the stationary inhomogeneous drift-diffusion junction;
2. the published impedance-field weighting;
3. the local source `K=4q^2nD` after convention translation;
4. the separate `s_1`, `s_2`, and `s_3` contribution structure;
5. equilibrium recovery of `4k_BTR(x)` only when cross terms are included;
6. agreement between direct and adjoint terminal voltage PSDs in the same low-frequency limit.

## 11. Novelty consequence

A terminal transfer-function or adjoint formulation is established methodology. R06 novelty, if any, must lie in the physical closure and controlled HgCdTe/contact reductions, not in using a Green function, impedance field, local contribution map, or adjoint to compute terminal noise.