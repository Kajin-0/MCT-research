# B2. The heavy-hole threshold can obstruct a sharp branch itself

**PROVEN UNDER ASSUMPTIONS; established Friedrichs/Feshbach mathematics.** The
useful new decision in R07 is to check atom eligibility before applying a
sharp-gap law or requesting a constant dynamic susceptibility. This is not
claimed as a new threshold theory or as an established HgCdTe coefficient.

## Normalization obstruction

Consider a self-adjoint, energy-independent, one-target-channel reduction

    H = [[epsilon0, <v|], [|v>, A]],
    dnu(t) = <v|dP_A(t)|v>.

Here dnu is the **eliminated coupling measure**, not the normalized sector
spectral measure dmu in B1. Assume v is in the Hilbert space and the blocks
have their usual self-adjoint domains. If an eigenvector at E has target
component a!=0, the Q equation requires

    (E-A) chi = a v.

Its spectral solution has minimum squared norm

    ||chi||^2 >= |a|^2 integral dnu(t)/(E-t)^2.              (B2.1)

Any component in ker(E-A) adds norm; v must also be orthogonal to that kernel.
Therefore if this integral diverges, **no normalizable eigenvector with
nonzero target component exists at E**. A formal real scalar pole equation
epsilon0+PV integral dnu/(E-t)=E does not repair the missing norm. A threshold
resonance and a spectral atom are different objects.

At a one-sided threshold t0, a certified lower density

    dnu(t0+epsilon) >= c epsilon^p d epsilon,
    c>0,  -1<p<=1,   0<epsilon<Lambda

makes (B2.1) infinite at E=t0. p=1 diverges logarithmically; p<1 by a power.
For p>1 this particular infrared obstruction is absent, not the whole
eigenvalue problem solved. If the inverse exists on v in the Hilbert/domain
sense, the scalar equation and kernel compatibility hold, and no bath-only
component is chosen, the normalized target weight is

    Z = [1+S]^-1,    S = integral dnu(t)/(E-t)^2.            (B2.2)

S<=1/3 would suffice for B1's Z>=3/4. The infrared contribution for a density
c epsilon^p with p>1 is c Lambda^(p-1)/(p-1); remote weight must still be
bounded. Units: dnu has energy^2, its density energy, c energy^(1-p), S
dimensionless. No off-continuum T' positivity is being extended to a retarded
principal value inside a continuum.

## Channel exponent and symmetry

For d-dimensional isotropic dispersion epsilon~q^z and a coupling amplitude
whose nonzero leading angular norm is q^l, radial phase space yields

    p = (d+2l)/z - 1.                                    (B2.3)

In a 3D quadratic heavy-hole channel, an unsuppressed amplitude (l=0) gives
p=1/2 and obstructs a target atom *at that threshold*. A linear-in-q
amplitude gives p=3/2 and removes this normalization obstruction. A 3D
linear channel with l=0 gives p=2. The theorem concerns a positive lower
certificate for the **exact or controlled eliminated measure**; a bare Born
diagnostic does not by itself certify the interacting/disordered measure.

An analytic, locally Td-covariant substitution vertex obeys

    P8 Gamma(q=0) P6 = 0

for inequivalent Gamma6/Gamma8 irreps, by Schur's lemma. If the heavy-hole
subspace remains inside the Gamma8 continuation with bounded projectors, its
Gamma6-to-heavy-hole amplitude is O(q). In contrast, a Gamma8-to-Gamma8
constant scalar amplitude is symmetry allowed. Allowed does NOT mean nonzero.
One needs the actual leading angular norm. Nonanalytic long-range vertices,
reduced local symmetry, singular band projectors at degeneracy, other orbital
copies and intersite embedding can defeat the simplified channel assignment;
these conditions must be tested, not asserted for the real alloy.

This selects a decisive missing physical quantity: does the full, aligned,
self-consistent composite substitution excite an unsuppressed heavy-hole
channel in the relevant symmetry sector, and does its controlled resummation
retain a positive infrared lower weight? If yes at the intended crossing,
the sharp-atom route fails there even if a real inverse equation has a zero.
If no, B1 is still not activated without an independent residue/tail and
transversality bound. A gap-free spectral functional remains a valid distinct
observable in either case.

## Prior-art boundary

[Gadella–Pronko, The Friedrichs Model and its use in resonance phenomena](https://arxiv.org/html/1106.5782v1)
reviews discrete-level/continuum coupling and resonances. The
[Albeverio–Lakaev–Muminov primary paper](https://arxiv.org/html/math/0604277v1),
sections2–3, distinguishes threshold eigenstates from resonances according
to the form factor and square-integrability. These already establish the
mathematical territory; (B2.1) is also derived directly above. The repository's
earlier `threshold_causal_2026-10-11` already derived infrared nonanalyticity
and divergent derivatives. B2 states the associated **target spectral-atom
eligibility** consequence, with the necessary channel/measure qualifications.
No material-specific residue, coupling coefficient or historical priority is
claimed. The random-alloy heavy-hole channel in Krishtopenko2022 is relevant
prior art, not evidence that its SCBA measure is the exact material measure.
