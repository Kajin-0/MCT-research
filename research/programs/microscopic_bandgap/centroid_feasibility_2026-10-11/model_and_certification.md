# Exact synthetic model and numerical certificate

## M1. Existing family; three justified alternatives

Reuse [N3](../continuum_spectral_2026-10-11/observables_and_failures.md) and its
independent centroid test. Let sigma be uniform probability on [-2,2] eV,
b=0.05, h(x)=16[x(1-x)]^2 and e(x)=-0.3+1.1x eV. The latter numbers are the
illustrative atomic model in `tests/test_r07_analytical_first.py`, not material
inputs. For a in {-1,0,1} define

```text
S_a = 0.4(1+a) delta_(+1) + 0.4(1-a) delta_(-1)
    + 0.1(1-a) delta_(+4) + 0.1(1+a) delta_(-4),
mu6_a(x)=(1-h) delta_e(x)+h[b sigma+(1-b)S_a],
mu8(x)=sigma.
```

**PROVEN UNDER ASSUMPTIONS:** all are positive normalized measures on a bounded
support; each mixed S has mean zero, so every alternative has the same full
Gamma6-type centroid `(1-h)e(x)` and Gamma8-type centroid zero. Their entire
projected endpoint spectra and first x derivatives agree because h has double
endpoint zeros. This does not assert equality of full endpoint impurity
operators. For every interior x the Gamma6-type measure has a nonzero continuum
component; Gamma8-type is continuous. No eliminated support gap is assumed.

a=0 is the symmetric midpoint of the two previously tested rebalancings;
a=+1 puts the main weight at +1 and its compensating satellite at -4 eV;
a=-1 reverses them. This isolates unresolved spectral balancing at fixed
coherent first moment. These are exact causal alternatives, not an atomic
Bernoulli law, spatial correlations or physical impurity potentials. Their
extreme weights are deliberate information witnesses, not an uncertainty
range claimed for HgCdTe. No Td/SOC directional channel is presumed negligible.

## M2. One physical model space, fixed retained projections

In a scalar sector take D(x)=diag(e(x),1,-1,4,-4) direct-sum multiplication
by t on L2([-2,2],dt/4). Its first basis vector is e0. Let w_a, orthogonal
to e0, have squared discrete components `(1-b)` times the S_a weights and
constant continuum component sqrt(b), so ||w_a||=1. Define a unitary U_a(x)
by the rotation `U e0=sqrt(1-h)e0+sqrt(h)w_a`,
`U w_a=-sqrt(h)e0+sqrt(1-h)w_a`, identity on the remaining complement.
Then H6_a=U_a^* D(x) U_a, with fixed P=|e0><e0|, has exactly mu6_a.
Both endpoint rotations are identity. Differences between alternatives
are in H, not a post-selected physical projector. Replicate this operator
twice with the Gamma6 irrep and the uniform multiplication operator four
times with the Gamma8 irrep. Sector trace/dimension gives the measures above.

This bounded self-adjoint realization qualifies the **synthetic** model. It
is not a local zincblende Hamiltonian, a many-body alloy, or an ARPES/optical
observation operator. There is no physical lattice, carrier, zero-point or
strain adapter. The old TB rejection and R07 physical-input gates remain.

## M3. Observable and exact integration

Use A=P_eta*mu, the registered quartic window, and r=0. Define
`m_alpha=int chi A_alpha`, `n_alpha=int E chi A_alpha`, `C_alpha=n_alpha/m_alpha`
and `Omega=C6-C8`. The uniform measure and even window give n8=C8=0 exactly.
All quantities come from full normalized measures; taper/exclusion is a
specified observation choice, not a silently discarded numerical tail.

For an atom at t, set u_L=-W-t,u_R=W-t. For j=0,...,5 let B_j be the difference
of primitives of eta*u^j/(u^2+eta^2):

```text
B0 = atan(u_R/eta)-atan(u_L/eta),
B1 = (eta/2) log[(u_R^2+eta^2)/(u_L^2+eta^2)],
Bj = eta*(u_R^(j-1)-u_L^(j-1))/(j-1) - eta^2 B_(j-2), j>=2,
J_l(t) = (1/pi) sum_(j=0)^l binom(l,j) t^(l-j) B_j.
m_atom=J0-2J2/W^2+J4/W^4,
n_atom=J1-2J3/W^2+J5/W^4.
```

For sigma with half-width L=2, its A(E) is the sum
`[atan((L-E)/eta)+atan((L+E)/eta)]/(2*pi*L)`.
Let Q(E)=E-2E^3/(3W^2)+E^5/(5W^4). Evenness and integration by parts give

```text
m_sigma = { [Q(E) atan((E+L)/eta)]_(-W)^W
            -pi[J1(-L)-2J3(-L)/(3W^2)+J5(-L)/(5W^4)] }/(pi*L),
n_sigma = 0.
```

These identities are **PROVEN UNDER ASSUMPTIONS** by polynomial division,
the binomial theorem and integration by parts. They integrate the full
continuum contribution; no eta->0 limit or spectral grid approximation is used.

## M4. Outward arithmetic, verification and sign semantics

Interval endpoints use Decimal operations at fixed precision with floor/ceiling
rounding. Positive logarithms are evaluated with the standard-library correctly
rounded nearest contract and enlarged by one adjacent representable value
on each side. Arctangents reduce to |u|<=1/2 using reciprocal and angle-addition
identities, then sum 64 alternating terms with absolute remainder at most
`|u|^129/129`. Machin's identity `pi=16 atan(1/5)-4 atan(1/239)` is enclosed
by the same series. Every algebraic/transcendental error propagates into m,n,C
and Omega. The guarantee is conditional on Python Decimal's documented
arithmetic contract; no floating-point quadrature difference is called a proof.

Interval signs mean lower Omega>0 or upper Omega<0; otherwise unresolved.
The registered 1-meV margin is an additional model usefulness gate, not a
material uncertainty. Floors are lower bounds on m6 and m8. Differences between
widths, eta and alternatives are **changes of the declared observable/model**,
not numerical error. They cannot be absorbed into the rounding interval.

Independent fixed composite Gauss-Legendre quadrature checks all registered
integrals using positive Lorentz kernels and the closed uniform spectral
density rather than the primitive recurrence. Tests also check explicit small
matrix fixed-projector realizations, normalization, endpoint/coherent controls,
energy-reference/unit covariance and preregistration/source hashes.
