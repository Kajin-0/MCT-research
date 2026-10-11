# Conditional reference-irrep check without another native job

**PROVEN UNDER ASSUMPTIONS:** a nearly invariant finite-rank subspace in an
exact unitary finite-group representation has a nearby invariant projector
with a character-error bound. **CALCULATED:** earlier accepted primitive HgTe
spinors pass a conditional numerical version. No failed matched-host gate or
material accuracy is admitted. Twirling, character orthogonality and Schur
decomposition are established mathematics; no novelty is claimed.

## 1. Exact projector and multiplicity bound

Let U_g be an exact unitary representation of a finite group, P an orthogonal
rank-d projector, A an orthonormal frame, C_g=A^dagger U_g A. Assume

```text
ell = max_g ||I-C_g^dagger C_g|| < 1/4,
tau = sqrt(ell) < 1/2.                       (operator norms)
```

I-C_g^dagger C_g=A^dagger U_g^dagger(I-P)U_g A is positive, so
||(I-P)U_g P||<=tau. Equal-rank projector identities give
||U_g P U_g^dagger-P||=||(I-P)U_g P||<=tau. Define
M=mean_g U_g P U_g^dagger. M commutes with the group and ||M-P||<=tau;
its spectrum lies within tau of {0,1}. Hence Q=1_[1/2,infinity)(M) has rank d,
is invariant, and ||Q-M||<=tau, ||Q-P||<=2tau. In infinite Hilbert space the
argument is still finite rank, in the span of finitely many images of P.
No Hamiltonian gap, isolated eigenvalue, support-free D or spectral limit is
required; the small-leakage condition is an independent symmetry assumption.

rank(P-Q)<=2d implies ||P-Q||_1<=4d tau, so
|tr(P U_g)-tr(Q U_g)|<=4d tau. Character orthogonality gives an integer

```text
m_alpha(Q) = mean_g chi_alpha(g)* tr(Q U_g),
|mean_g chi_alpha(g)* tr(P U_g)-m_alpha(Q)| <= 4 d_alpha d tau.
```

For trace error <=epsilon_chi and character-dot error <=epsilon_dot, replace
the bound by d_alpha(4d tau+epsilon_chi)+epsilon_dot. Round only if distance
to the proposed integer plus error is <1/2. This classifies the **nearby Q**;
it does not prove P itself exactly invariant or physically accurate.

## 2. Native Gram metric and rounding assumptions

For raw A with G=A^dagger A, ||G-I||<=delta<1, normalize B=A G^-1/2. Since
||A^dagger U A||<=1+delta, spectral bounds on G^-1/2 give

```text
||B^dagger U B-A^dagger U A|| <= (1+delta)delta/(1-delta).
```

Adding compression error epsilon_C gives difference <=c. The exact normalized
compression is a contraction, so leakage-defect error is <=c(2+c); trace error
is <=dc. Frobenius bounds can upper-bound operator norms. This accepts independent
certified metric/compression errors, but cannot invent them.

The saved implementation instead evaluates a conservative IEEE model using
u=2^-53, gamma_n=nu/(1-nu), entry allocation 4 gamma_(32N)+16u for N complex
components, plus normalization, small-matrix product and character-dot budgets.
It assumes bounded arithmetic with no overflow/underflow, correct NC metric and
declared ideal spatial/spin lifts. Its scalar envelopes are **CALCULATED UNDER
THIS MODEL**, not directed-rounding interval certificates. Native eigenpair,
HSE operator, frame-choice, PP, material and zero-point errors remain unbounded
by this check. A strict SCF total-energy threshold alone would not bound them.

## 3. Td realization and source result

Use the 24 signed Cartesian permutations R preserving the four tetrahedral
bonds (product of signs +1). Spin transforms by the proper axial rotation
det(R)R; for lift quaternion (v,w), S=w I-i v.sigma. The orbital operation
permutes the complete closed plane-wave set: g -> g B R^T B^-1. The native
fcc reciprocal matrix is verified against the ideal diagonal -1/off-diagonal
+1 matrix up to scale. Origin, species and spin conventions are fixed; Bravais
translation phases equal one at Gamma. Different frames/metrics need their own
transport check; orbital labels alone do not suffice.

For t=2w the spin-odd characters are chi6=t, chi7=det(R)t,
chi8=det(R)(t^3-2t). Central lift reversal changes trace and character signs
together, so averaging 24 lifts equals averaging the full 48-element double
group. Independent j=1/2 and j=3/2 matrix exponentials verify the characters;
group/lift closure and orthogonality are independently tested.

The source is accepted native HgTe SG15-HSE+SOC k4/q4 e90/f120 full-accuracy
data: 6567 plane waves, Gamma6 bands 33-34, Gamma8 bands 35-38. Existing NC
spinors/metadata are read, without pw.x, bands.x or a new SCF. Byte pins and
character tables are in [reference_irrep_check.json](reference_irrep_check.json).

| Source sector | Maximum character mismatch | Nearby-Q distance model envelope | Largest multiplicity error envelope | Rounded (m6,m7,m8) |
|---|---|---|---|---|
| Gamma6, d=2 | 1.603e-15 | 7.729e-5 | 0.001237 | (1,0,0) |
| Gamma8, d=4 | 3.127e-15 | 1.094e-4 | 0.003498 | (0,0,1) |

These are dimensionless conditional envelopes. Small leakage is not a material
eigenpair-error bound. Individual substituted/random configurations need not
be Td invariant; ensemble symmetry cannot automatically admit their native P.
This source check cannot replace a converged matched host or the 1-meV gate.

## 4. Counterexample and established alternative

An exactly degenerate quartet Gamma6+Gamma7 has multiplicities (1,1,0);
two Gamma6 copies have (2,0,0). Dimension/fourfold energy degeneracy alone
does not identify Gamma8. Dense rotated-projector tests independently verify
the twirl bound; large metric error/leakage explicitly rejects classification.

QE's established bands.x [lsym classification](https://www.quantum-espresso.org/Doc/INPUT_BANDS.html)
already computes irreducible representations of the small group of k. This
saved-wavefunction check is a limited independent reference audit, not a new
physical method or a replacement for all native postprocessing. Official
documentation accessed 2026-10-11. All previous negative claims remain intact;
no empirical alloy input, new material coefficient or physical inversion follows.
