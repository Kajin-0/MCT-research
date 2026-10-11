# P3 — what one periodic response cannot determine

## A1. Periodic aliasing of distinct localized impurity profiles

**PROVEN UNDER ASSUMPTIONS.** For a lattice period L, periodize a finite-support
scalar onsite impurity profile v by summing all its L-translates. For any
finite-support u, the profile difference

```text
delta v(j)=u(j)-u(j-L)
```

has identically zero periodization. Therefore v and v+delta v produce exactly
the same L-periodic Hamiltonian, all spectra, every projected Green function,
every finite-eta centroid and every finite-box reaction kernel in that cell.
They need not have the same isolated impurity or larger-cell response.
The difference has zero sum of onsite coefficients; neither Hermiticity nor
causality removes it. This is not an assertion of physical charge neutrality.
Profiles are held fixed while the period changes.

Explicitly take `v_A=.1 delta_0` and
`v_B=.13 delta_0-.03 delta_L` in a nearest-neighbor tight-binding host. Their
period-L potentials coincide. In an isolated host with resolvent matrix
elements g00 and g0L, their forward second-Born difference is

```text
2 u(v+u)(g00-g0L),  v=.1, u=.03,
```

up to the common Bloch normalization and the scattering-strength squared.
For real energy above the host band, g00!=g0L generically. Away from poles
the exact T is analytic in an overall strength lambda; the unequal lambda²
coefficient proves that the exact isolated amplitudes cannot be identical as
functions of lambda. One same periodic-cell dataset does not identify them.
No Born approximation is asserted to describe physical Hg/Cd substitution.

An independent nonperturbative check is available in the infinite chain at
E=3 (hopping -1, host spectrum [-2,2], L=4). Write
`g00=1/sqrt(5)`, `kappa=(3-sqrt(5))/2`, `g04=kappa^4/sqrt(5)` and
`G_loc=[[g00,g04],[g04,g00]]`. The exact off-shell Gamma forward amplitudes,
with the same external plane-wave normalization suppressed, are

```text
tau_A=.1/(1-.1 g00),
tau_B=ones^T D (I-G_loc D)^(-1) ones, D=diag(.13,-.03).
```

Their difference exceeds 0.003 eV in the focused test; `||G_loc D||<0.1`.
E lies above both perturbed spectra, so no pole or continuum continuation is
used to manufacture the difference. This proves different exact isolated
responses for the fixed profiles, independently of the finite-ring witness.

The independent test uses a 4-site ring, where the profiles coincide exactly,
and a 12-site ring, where their dense Green functions/reaction kernels differ.
This is a causal information counterexample, **not HgCdTe validation**. The
construction extends along any superlattice vector in three dimensions and
to a Hermitian orbital component of a spinful impurity. No composition fitting,
sample disorder law or background-dependent interaction is invoked.

## A2. The precise extra assumption that would remove this obstruction

One periodization can identify an onsite profile only after independently
excluding competing tails outside a known nonoverlapping fundamental support,
or bounding their effect on the intended contraction. For a nonlocal HSE
operator, an onsite support assertion alone is insufficient: nonlocal tails
and the self-consistent periodic-image response must also be controlled.
Neutrality and near lattice matching do not supply those bounds.

If two matched isolated operators differ by a certified bounded tail operator
delta_tail at eta>0, the resolvent identity yields
`||R-R_tilde||<=delta_tail/eta²`; more economical direct functional bounds can
also suffice. There is no numerical delta_tail in the accepted repository
inputs. A second cell would be a convergence test, not a universal proof of
the tail, and is not proposed as an automatic new queue.

**FALSIFIED:** a complete same-frame spectrum of one prepared periodic
fraction 1/8 by itself identifies an isolated Cd-in-HgTe T or a physical
endpoint slope. This supplements the preserved finite-box on-shell T zero
and endpoint/interior hidden-interaction counterexamples; none is weakened.
The prior conditional 1/Ncell omitted-weight theorem still requires its
localization hypothesis. Multiplying a finite reaction kernel by eight does
not certify a thermodynamic amplitude or HgCdTe inversion.

## A3. A useful discriminator that survives this limitation

In a matched **specified finite static operator**, with a spectral host
projector P (`[P,H0]=0`) and H=H0+V, the reaction kernel is

```text
K(z)=V_PP+PHQ(z-QHQ)^(-1)QHP,
L(z)=-Im K(E+i eta)/eta
    =PHQ[(E-QHQ)^2+eta²]^(-1)QHP >=0.
```

For eta>0, L=0 iff QHP=0 (the resolvent is injective). Thus a strictly positive
certified sector trace of L rejects an energy-independent closed-P model for
that operator, without a continuum support gap. It diagnoses leakage into
the eliminated space, not a finite raw T', intrinsic linewidth or the total
physical alloy A. This is established Feshbach spectral positivity used as
an acquisition discriminator; no novelty is claimed.

This substitution interpretation requires the spectral-host condition.
An embedded primitive frame may fail it for an independently self-consistent
supercell host. In that case the same Schur formula diagnoses total H coupling,
including host mixing; subtraction of host leakage is not generally positive.
Either align a qualified pure-supercell spectral projector or explicitly
budget the noncommuting host residual. Do not attribute host leakage to Cd.

If `||R-R_B||<=e`, `J=||R_B^-1||`, `Je<1`, the existing inverse certificate
gives `beta_K<=J²e/(1-Je)` plus independent host/alignment/operator errors.
Sector-averaged leakage error is <=beta_K/eta. Reject a causal approximation
if its negative leakage exceeds that budget; certify nonzero coupling only
if its positive leakage exceeds it. A small static mass projection and a
large leakage can coexist, but this data packet is not yet available.

Windowed moments need neither amputation nor inverse conditioning. With
unresolved sector probability sigma and the fixed quartic window,

```text
0<=m_tail<=sigma, |n_tail|<=[16W/(25sqrt(5))]sigma,
|C-C_B| <=[W+16W/(25sqrt(5))]sigma/p, if m_B>=p.
```

This follows from positivity and bounded test functions after Poisson
convolution; no distance to the omitted spectrum is required. Unknown
eigenpair/model errors are **additional**, and a spectral prefix is never
renormalized. These contractions, with frame and law metadata, are a smaller
necessary acquisition than an arbitrary full Wannier vertex decomposition.

**Decision:** a chemistry-bearing spectral packet is indispensable now.
The [single unexecuted acquisition design](minimum_acquisition.md) can test
finite-operator leakage and measure spectral contractions. It cannot alone
solve the unrestricted thermodynamic alloy, even if its native SCF converges.
Stop before launching it; no additional analytic cycle or repeat search follows.

## Independent symmetry check on P2's negative result

The Q/V-orientation obstruction is not removed by enforcing the physical
Gamma6 doublet and Gamma8 quartet dimensions. Embed the P2 first-branch
construction as three equivalent Gamma6 copies:
`H_A,6=diag(.2,-1,+1) tensor I2`,
`H_B,6=diag(.2,+1,-1) tensor I2`, and
`V6=.4*(|1><2|+|2><1|) tensor I2` in copy space. Add the same uncoupled
`H8=-.2 I4`, and retain the first Gamma6 copy plus the Gamma8 quartet.
All operators intertwine the corresponding Td double-group representations
and preserve time reversal. Both hosts have identical sorted spectra and
retained Green functions, but the substituted Gamma6 mass contraction still
has opposite real sign at z=i eta. Thus the missing relative Q/V information
survives the correct irrep multiplicities. The 10x10 focused check is an
exact symmetry-compatible counterexample, not a material Hamiltonian.
