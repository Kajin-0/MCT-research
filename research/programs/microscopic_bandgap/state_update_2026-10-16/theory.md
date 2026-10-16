# A nonmagnetic SCF update, and what qualifies it

**PROVEN UNDER ASSUMPTIONS.** Work in the declared finite plane-wave spinor
space, NC metric, Gamma/q1 sampling, FD sigma=.001Ry. For each chemical member
use its own species-preserving space group G, with the physical spin lifts,
and Theta(u_G,d_G)=(d*_{-G},-u*_{-G}). Theta²=-I. The admissible density
matrices satisfy 0<=D<=I, Tr D=144 and covariance under G and Theta.

For a symmetry-invariant ionic Hamiltonian and consistently evaluated HSE
functional, covariance gives H[gDg^-1]=gH[D]g^-1, including antiunitary g.
Thus, if D is invariant, spectral calculus of the FULL H[D] and the unique
positive-temperature FD charge root gives an invariant output

    T(D) = f_sigma(H[D]-mu(D)),  Tr T(D)=144.

The monotone charge derivative is sum_j f_j(1-f_j)/sigma>0 unless numerical
saturation destroys the bracket. This uses FD n=-99, not cold smearing n=-1
and not the private48-band cold-root solver. No eigenvalue averaging is needed.
For this Gamma experiment Kramers pairs must have equal weights; cubic host
multiplets are checked, not restored after diagonalization. The finite-cell
Gamma smearing entropy is not the physical zero-temperature alloy entropy.

Actual spatial enumeration of the FROZEN positions gives96 host operations
(24 point operations times4 fcc translations),24 Cd operations (same24 point
operations, only identity translation). This particular ordered Cd site retains
Td about its site; that is a result of species matching, not permission to
impose Td on a different impurity arrangement. Native fractional translations,
spin axes and G maps must agree with these operations. Theta symmetry does not
follow from zero local spin density. In particular QE sum_band symmetrizes the
LOCAL rho and domag=false suppresses its magnetic components; neither operation
certifies the nonlocal D used for exchange.

The smallest honest closed-loop update is therefore:

1. Start from an explicitly qualified nonmagnetic D_in. Build the SAME
   H[D_in]: kinetic, scalar ionic/local Hartree+HSE XC, NC nonlocal SOC,
   direct screened exchange from that D_in and its occupations.
2. Solve its occupied eigenproblem in the full finite plane-wave space,
   with certified occupied-tail/charge and full-action residuals. A jointly
   invariant trial space is an initializer/preconditioner, not a substitute
   for those checks. Apply the FD charge root to actual computed eigenvalues.
3. Form D_out from those orbitals/weights; independently compute all four
   local-density components and full nonlocal symmetry, charge and entropy.
   Rebuild BOTH the direct Fock source and Hartree/local XC from D_out.
4. Evaluate full-H[D_out] residuals and the FD fixed-point residual, energy
   accounting and physical six-frame actions in that same new state. Stop
   a failed qualification, not continue an unqualified trajectory. Even a
   valid one-step update is not converged SCF.

No symmetry twirl is substituted for steps2–4. A damping trial, if separately
needed, must be a genuine density mixture with its own entropy and complete
nonlinear functional; mixing local rho while silently keeping another Fock
source is insufficient. No damping parameter or indefinite retry is introduced
in this phase. Direct exchange avoids the known off-span176-ACE defect without
asserting that every ACE scheme is defective.

## Actual retained-data initial trial and a new obstruction

Let V contain the accepted304 basis, A=V†H[D0]V, and set
D1=V f_sigma(A-mu)V†. It is produced by FD variational minimization at the
known linearized Hamiltonian, NOT a density symmetrization. Charge, entropy,
all96 host density transformations and Theta are tested on actual complex G
spinors. No extra auxiliary vector is assigned a made-up solved-band energy.
176 vectors suffice to store this trial: the native saturated FD weights above
146 vanish in this captured matrix. This does not bound unmeasured whole-space
occupied states. Saturation differs from the mathematical logistic by at most
exp(-200) per saturated level, independently of the spectrum.

The stable full-density symmetry check writes transformed orbitals Y=XK+R,
where X contains the146 positively weighted natural orbitals and
K=(X†X)^-1 X†Y. Expansion of YwY†-XwX† gives the computable upper bound

    ||defect||_F <= ||X||² ||KwK†-w||_F
                    +2||X|| ||K|| ||Rw||_F + ||R sqrt(w)||_F².

It bounds operator norm too, without subtracting nearly equal large traces.
Reported arithmetic is floating evaluation, not a directed-rounding enclosure.
Independent scipy.eigh/brentq and canonical two-rank packet roundtrips agree.

**New decision-relevant bound:** write R0=H[D0]V-VA and F=f_sigma(A-mu).
In an exact isometric model, the off-diagonal block of [H[D0],D1] is R0 F,
so its norm is at least ||R0 F||. Conservatively subtracting the computed
in-space commutator gives .05211828361Ry here. For any Hermitian E such that
[H[D0]+E,D1]=0,

    ||E|| >= ||[H[D0],D1]|| / diam(spec D1).

Proof: center D1 at the midpoint of its extreme eigenvalues and apply
||[E,D1]||<=2||E|| ||D1-cI||. The full-space spectrum includes0 and1,
so the denominator is1. The resulting necessary uniform correction is
**709.1054meV** in the captured exact-action model. This is NOT a chemical
six-frame error, a lower bound on Cd response, or a rigorous floating/action
enclosure. Unknown nonlinear feedback might supply such an operator change;
the bound neither proves nor disproves that possibility. It rules out claiming
stationarity of the new trial merely from its excellent symmetry or FD304 fit.
The same lower bound holds for inf_c||E-cI||: a scalar reference shift cannot
cancel the commutator. No absolute energy-zero choice creates this obstruction.

At fixed H[D0], the finite-space free-energy decrease is .01198705880Ry.
For a twice differentiable nonlinear electronic energy with same-state
gradient H[D0], the true change is this linear-plus-entropy change PLUS the
nonlinear electronic Bregman remainder. A Hessian upper bound L_F would give
remainder<=L_F ||D1-D0||_F²/2. A full-step decrease is sufficient if
L_F<6.91663866Ry here. That is a derived required certificate, NOT a measured
HSE Hessian or a license to extrapolate convergence. Exchange is quadratic in
D, Hartree quadratic in local charge, local HSE XC nonlinear in density and
its gradients. All must be accounted for in a rebuilt native state.

## Full-state and2meV gates remain distinct

Full-H eigenpair residuals (including off-space components), FD charge/root,
occupation tails and nonlocal symmetry are separate gates. A small SCF energy
scalar, a finite Ritz solution or a zero commutator alone does not certify the
correct FD occupations. A certified complement lower bound C>=L yields a
block-diagonal occupation tail <=dim(C) f_sigma(L-mu); coupled residual error
must still be included. Without such a certificate or an equivalent full-space
occupation/counting solve, unknown occupied complement states remain possible.
No lower bound is inferred from high positive Ritz values.

For normalized fixed physical projectors let
W=P6/2-P8/4, ||W||_1=2. For the matched chemical full-H trace, errors obey

    |delta Omega| <= 2(epsilon_H_host+epsilon_H_Cd)+epsilon_frame.

These epsilon_H may bound only the projected Hamiltonian error; they need not
be uniform whole-H bounds. For example **.4meV per member in projected H**,
including action/state/tail errors, plus **.4meV total frame error**, is a
sufficient2meV budget. It is a prospective allocation, not an attained bound.
The original six probes are preserved with their known nonexact Theta closure;
they are not silently replaced by the purified trial space.

One way to convert a numerical fixed-point residual r to a state error is an
independently certified contraction q<1 in a mapped invariant neighbourhood:
||D-D*||<=r/(1-q). A projected-H Lipschitz bound L then contributes
L r/(1-q) to epsilon_H, in the declared compatible norms. A verified local
inverse-Jacobian/stability theorem is an alternative. Neither q nor L nor an
equivalent certificate exists here. An observed iteration ratio, local zero
magnetization, or the small explicit odd frozen trace cannot supply it. Thus
NO full screened chemical interpretation with<=2meV is released.

## Prior-art boundary

Density-matrix SCF, damping, variational updates and convergence obstructions
are established; see [Cancès–Le Bris2000](https://numdam.org/item/M2AN_2000__34_4_749_0/).
The [Cancès–Kemlin–Levitt analysis](https://arxiv.org/abs/2004.09088) compares
SCF and minimization and depends on stability/spectral properties; its
fixed-rank-projector results are not a ready finite-temperature HSE certificate.
[Lin2016](https://arxiv.org/abs/1601.07159) constructs ACE exact on its chosen
span; it does not make an unclosed empty span globally exact or certify FD
self-consistency. Our protocol/source audit and particular measured state
obstruction make no general algorithm or novelty claim. Sources checked
2026-10-16; no new optical search or material data was used.
