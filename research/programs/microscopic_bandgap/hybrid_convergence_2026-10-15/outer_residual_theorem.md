# What the native outer residual can certify

**PROVEN UNDER ASSUMPTIONS, not new material validation.** Work in a fixed finite
spinor/G basis, with density matrix D=sum_i w_i|phi_i><phi_i|, w_i>=0. The FD
occupation protocol supplies positive w. Write exact exchange V[D]=-K(D), with
self-adjoint linear exchange superoperator K. Define
F(D,E)=Tr[D V[E]]=-<D,K(E)>_HS and E_x(D)=F(D,D)/2. Fix all ionic/local/frame/
kernel parameters; the statements concern exchange, not the whole SCF map.

## 1. Direct versus compressed cross energy

Let A=-V[D_old]>=0, S the old source columns, and assume S†AS invertible on the
retained compression space. ACE gives

    A_ACE = A S (S†AS)^(-1) S† A
          = A^(1/2) Pi A^(1/2),  0<=Pi<=I.

Consequently V_ACE[D_old]-V[D_old]=A-A_ACE>=0. For positive D_new,

    epsilon_ACE = Tr[D_new (V_ACE[D_old]-V[D_old])] >= 0.

For the native nonlocalized ACE outer formula,

    d_ACE = F_ACE(D_new,D_old)
            -[F(D_old,D_old)+F(D_new,D_new)]/2
          = <DeltaD,K(DeltaD)>_HS/2 + epsilon_ACE,

where DeltaD=D_new-D_old. This follows by expanding the symmetric quadratic
form; it is not the assumption that old ACE equals old direct exchange on new
orbitals. Source-space exactness alone never supplies that equality. The actual
old-xi/new-Phi contraction reconstructs the native cross term, not the missing
old-direct cross term. Singular Gram matrices require the appropriate supported
pseudoinverse and compatible source range; unsupported regularization is excluded.

## 2. Conditional exchange-observable step bound

If additionally K is positive as a superoperator on the relevant Hermitian
matrices, then ||DeltaD||_K^2<=2 d_ACE. For a Hermitian fixed-frame test T,

    |Tr[T (V[D_new]-V[D_old])]| <= ||T||_K sqrt(2 d_ACE).

For this experiment T=P_Gamma6/2-P_Gamma8/4. No new empirically fitted number
enters. ||T||_K is a computable kernel/reference property, not a bandgap slope.
The proof is Cauchy-Schwarz in the K semidefinite form, including its quotient
by the null space. Units: d in Ry, ||T||_K in sqrt(Ry), step bound in Ry.

For the untruncated positive screened real-space Coulomb kernel,
<DeltaD,K(DeltaD)> equals the positive weighted integral of squared spinor
density-kernel entries. **This does not prove positivity for the actual native
cutoff/FFT/divergence-treated discrete superoperator.** That requires a separate
kernel-domain check. Nonnegative reciprocal Coulomb factors can ensure A>=0
without ensuring the stronger superoperator property needed here.

Counterexample: take the real-space two-site kernel
W=[[1,-1/2],[-1/2,1]]>=0 and K(D)=W elementwise-multiplied by D. Schur's theorem
makes K(D)>=0 for every D>=0. But for same-charge rank-one positive matrices
D_plus=[[1,1],[1,1]]/2 and D_minus=[[1,-1],[-1,1]]/2, DeltaD has off-diagonal1
and <DeltaD,K(DeltaD)>=-1. Thus a negative exact direct d=-1/2 coexists with
negative-semidefinite exchange operators. The stronger density-metric premise
cannot be inferred just from a negative Fock operator or a valid causal spectrum.

## 3. A step is not an infinite-tail or gap certificate

Even under the stronger positivity premise, the bound covers one exchange step.
It does not cover the local Hartree/XC response, all later steps, or quasiparticle
and thermodynamic errors. If an independently proved SCF contraction modulus
q<1 in a specified state norm and an observable Lipschitz constant L are supplied,
then the usual a posteriori estimate is

    |O(D_*)-O(D_n)| <= L q ||D_n-D_(n-1)||/(1-q).

Observed residual ratios or successive trace differences are not proofs of q.
For arbitrary finite trajectories, smooth continuation can preserve every observed
iterate yet change the later limit, lose convergence or enter another basin.
Native dexx alone is therefore not a rigorous Gamma-gap/material uncertainty.

**Decision:** retain native dexx as the frozen numerical stopping condition and
report actual projected step sizes separately. A mathematically certified outer
remainder needs a verified contraction/response bound (plus the proper kernel
premises), or further explicitly bounded updates; it cannot be invented from the
first relaxation. These are applications of established ACE/Schur-complement and
fixed-point mathematics. No novelty or physicalx_c claim is made.
