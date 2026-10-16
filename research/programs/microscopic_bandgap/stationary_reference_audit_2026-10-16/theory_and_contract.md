# Reuse a converged numerical host; do not substitute it for screened chemistry

All statements below distinguish **PROVEN UNDER ASSUMPTIONS**, **CALCULATED**
native-packet checks and **OPEN** material input. No native job is authorized
or executed by this assignment. Existing SCF acceptance is unchanged.

## 1. Three different objects, not three versions of one stationary solution

1. Original primitive HgTe SG15-HSE+SOC, a=6.46 Å, e90/rho360, k4/q4,
   44 spinor bands/36e, **cold smearing** .001 Ry. f360 and f120 are different
   numerical exchange operators. Their original `r07.save` states survive.
2. `open_grid` exports contain symmetry-expanded orbitals, eigenvalues and
   occupations on 64 points. Their XML has placeholder SCF error/energy fields;
   the original eight-point SCF XML, not those placeholders, proves the recorded
   convergence status. Export is not a new SCF or direct-Fock residual test.
3. H304[D0] uses an eight-atom, e50/rho200/f200, Γ/q1 **FD trial**, with a
   constructed 144e density. It is operator-symmetric and demonstrably
   nonstationary. Neither its 5.56-GB action query nor its state is the original
   primitive reference, an HSE convergence certificate or a cost bound here.

The old primitive reference can replace D0 **as the starting numerical host
reference and physical Γ projector source**. It does not establish an exact
stationary FD state or a self-consistent chemical response in a different cell.
Keeping cold smearing defines the old numerical model honestly. Changing to FD,
averaging a quartet's occupations or changing k/q/cutoffs defines a new state
problem; it cannot inherit the old convergence flag.

## 2. Common-frame transfer theorem and its limits

Let J be an isometry between two commensurate plane-wave Hilbert spaces with
the same physical spin axes, origin, lattice, NC metric and reciprocal vectors.
Set P_h=ΦΦ†, Φ†Φ=I. Unitary rotations inside Γ6 or Γ8 are gauge choices;
sector traces and projector overlaps are invariant. Multiplying only one
specimen by an unrecorded scalar energy shift is not a common gauge for an
ensemble propagator.

**PROVEN UNDER ASSUMPTIONS:** if an exact native host satisfies
H_h[D_h]Φ=Φh_h, then a physical commensurate embedding uses unchanged
coefficients at

    (G_s+k_s) = (G_p+k_p) R^T,  A_s=R A_p.

No second 1/sqrt(det R) multiplies the normalized coefficients. This transfers
states and projectors, **not** self-consistency. Stationarity transfers only
if the full density including k weights/filling, charge, HSE finite-q kernel,
local/core/SOC potential, discretization and energy convention also obey

    H_s[J D_h J†] J = J H_h[D_h]

on the required occupied/reference space (plus controlled complement error).
For BZ folding the isometry acts on the direct sum of primitive Bloch blocks,
not six Γ spinors alone. A commensurate k/q spacing is necessary, not a proof
of this identity: exchange singularity/cell corrections, ACE spans, band
coverage and FFT realizations also matter. The old pure-supercell gate remains.

At e50, the original e90 Γ6 vectors lose about 2.038e-6 probability and Γ8
about 1.278e-7. Normalizing after discarding these coefficients changes the
observable; amplitude losses are ~.001428 and .0003575, respectively. These
are actual frame-tail measurements, not energy-error estimates. e90↔e50 is
therefore not a byte-exact/isometric state transfer into the smaller space.
Zero-padding an existing lower-cutoff vector into a larger space is isometric,
but does not recover the larger-cutoff solution or its self-consistency.

## 3. The new native counterqualification: occupation symmetry

For orthonormal U, D=U diag(f) U†. Under a symmetry with transformed frame V,
O=U†V and R=V−UO, compression yields

    U†(D−V diag(g)V†)U = diag(f)−O diag(g)O†.

Thus this finite matrix is a lower witness for the full density defect. A
stable upper Frobenius estimate is

    ||diag(f)−O diag(g)O†||F
      +2||O diag(g)||2 ||R||F + ||g||∞ ||R||F².

The implementation includes explicit measured-Gram corrections. R may include
empty-state span error, so this upper bound can be loose; a small compressed
witness does not prove the whole defect small. No interval rounding enclosure
is claimed. Source-space and occupied-density symmetry are different tests.

On one exact Γ8 irrep, Schur requires invariant occupations to be scalar.
Consequently `range(f_Γ8)/2` is a lower distance to any scalar occupation on
that copy. The retained f360/f120 arrays give 4.2773e-7 / 5.3019e-7, with
calculated direct cubic density witnesses 8.5390e-7 /1.04147e-6. Their near-exact
Γ irrep **spans** do not remove these native occupation differences. No physical
magnetism or 0.655-eV broken-host behavior is inferred from this small defect.

The saved Γ ACE action on six physical probes also fails a literal 1e-8
relative cubic probe target (f120 max9.153e-8). These are reconstructed ACE
actions, not independently acquired direct-Fock actions or full-H residuals.
Lin's source-span exactness theorem needs the matching source and does not
certify global ACE accuracy, symmetry, or stationarity from an energy flag.

## 4. A cold-SCF flag is not a whole-space FD residual

QE's native .001-Ry cold occupations are wgauss((μ−ε)/σ,−1), not FD logit.
At fixed **stored eigenvalues**, independently solving the monotone FD charge
root moves μ by −1.895584 meV and changes occupations by up to 3.51e-7.
This is an algebraic reinterpretation only. It is not a calculation of
H[D_FD], its eigenstates, FD entropy, variational minimum or nonlinear energy.
Numerical smearing is not specimen temperature. Cold smearing has its own
energy correction and is not the physical FD free-energy functional.

Native total-energy convergence, charge neutrality and tiny negative `dexx`
(converted to its absolute value by QE) are scalar checks. They do not bound
`||H[D]U−U ε||`, `||[H[D],D]||`, or `||D−fσ(H[D]−μ)||` by1e-8.
The accepted SCF flags are not invalidated; the stronger inference is refused.

For FD in a finite Hilbert space the established HS bound is

    ||fσ(A)−fσ(B)||F <= ||A−B||F/(4σ).

An approximate diagonalization must include occupied full-H residuals and a
certified omitted FD tail/complement bound, not just solved-column Gram error.
Charge-to-μ error requires a susceptibility lower bound χ_min>0; then
`|δμ|<=|δN|/χ_min` on the relevant interval. None is supplied by an SCF flag.
If the complete nonlinear fixed-point map F is a contraction with q<1 in
the chosen norm, a measured fixed-point residual ε gives

    ||D−D*|| <= ε/(1−q).

This follows by the triangle inequality. q<1 is **not established** here,
especially near a fractional heavy-hole shell. Positive Hessian/stability and
selection of the intended nonmagnetic solution are separate requirements.

## 5. Unavoidable nonlinear chemical step, with no double counting

In a matched finite cell and aligned energy gauge, define

    H_h = H_Hg[D_h],  H_c = H_Cd-in-Hg[D_c],
    V_scr = H_c−H_h
          = ΔV_ion+ΔV_SOC/core+ΔV_H+ΔV_xc,local+ΔV_x,Fock.

Reusing D_h can initialize D_c; it cannot determine it. A fixed-D ionic change
is the unscreened substitution experiment, not the self-consistent impurity.
The formal linearization

    δD = χ0(δV_ion+K_Hxcx δD)

requires an invertible dielectric response and a bounded nonlinear remainder.
Those response/kernel inputs are missing; a large Hg/Cd contrast is not proven
perturbatively small. No binary host wavefunction audit can supply this missing
induced Te/charge-transfer/exchange response. A stationary host reduces the
reference problem, not the number of independent chemical quantities.

This is not a fundamental indeterminacy of a fully specified finite HSE
problem. With a complete discretization, PP/functional and state, H[D] is in
principle evaluable; its residual is a missing computational qualification.
Likewise a specified substituted configuration/functional supplies a nonlinear
state problem, with stability/solution selection still to resolve. The claim
is that its solution and screened response cannot be read algebraically from
the old host packets. Physical alloy/statistical/material inputs remain a
separate identifiability question.

For a specified configuration law use `Hbar=E H_ω[D_ω]`, `W_ω=H_ω−Hbar` and
define Σ_dis by the Dyson identity relative to that Hbar. Generally
`E H[D_ω] != H[E D_ω]`. Add neither a separate fitted bowing nor the same
screened mean shift again as disorder. At a dilute endpoint with reference H_h,
full impurity T enters the concentration expansion; if the coherent reference
already includes a uniform composition response, use the correspondingly
subtracted residual convention. Full T and P-irreducible K are not interchangeable.

For exact spectral P_h, retained substituted eigenvalues/complex overlaps
give `R_c(z)=Φ†(z−H_c)^−1Φ`, `K=(z−h_h)−R_c^-1`. If host invariance is only
approximate, retain `K=R_h^-1−R_c^-1` and bound the host leakage; do not set it
to zero from sorted bands. This preserves the existing
[host-invariant theorem](../../../../docs/derivations/host_invariant_reaction_kernel.md).
Periodic images, finite-volume amputation and retarded/PV distinctions remain.

## 6. Observable-specific numerical threshold and physical inversion

For a matched static projected gap functional
`g_P(H)=tr(P6 H)/2−tr(P8 H)/4`,

    |δg_P| <= 2 ||P δH P||;  |δ(g_P/2)| <= ||P δH P||.

For two cells the gap-contrast errors add. A *prospective* 2-meV numerical
contrast budget can allocate <=1meV to each cell's TOTAL g_P error:

    2 epsilon_H + epsilon_frame + epsilon_other <= 1meV per member.

For example, epsilon_H<=0.25meV leaves0.5meV for the remaining errors.
A uniform scalar energy shift cancels in g_P; it is not an extra alignment
error here. Ensemble resolvents still require an aligned common energy gauge.
This is a sufficient allocation, not an achieved bound or new admission
replacing old1e-8 gates. A 1e-8 density norm cannot be converted
to meV without a bound on H's density derivative. Scalar `dexx` cannot replace it.
For spectral Γ energies, eigenpair residual r gives distance <=r to some true
eigenvalue, but unique sector/cluster association and complement isolation must
also be justified. Finite-η inverse ordering is still not a signed physical mass.

The old finite-window spectral pilot's 2-meV response budget, mass floor and
tail gate remain as originally specified; it is a different observable.
Neither budget is a material error bar. The f360/f120 Γ gap difference is
6.7014 μeV in these references; it does not bound finite-q substitution error,
e50 changes, functional/core error or zero-point physics.

A real common-mode mass-zero criterion additionally needs real branch/pole
eligibility and a controlled self-energy/continuum prescription. Optical,
complex-resonance, mobility and topological reversals are not inferred here.
For a genuinely qualified physical mass with error ε_m and independently known
composition slope lower bound s>0, `|δx_c|<=ε_m/s` on a monotone bracket.
Neither ε_m nor s is identified by these binaries or ordered PBE configurations.
No empirical endpoint interpolation or fabricated x_c is introduced.
