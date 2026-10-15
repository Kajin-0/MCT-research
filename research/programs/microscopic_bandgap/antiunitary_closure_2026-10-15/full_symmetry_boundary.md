# Falsification of TR completion as a sufficient cubic-host repair

2026-10-15. This is an independent retained-data check during the separately
admitted operator test, not a new native job or a changed acceptance condition.

PROVEN: for a finite unitary symmetry group G commuting with the antiunitary T,
the smallest jointly invariant superspace containing S is

    M = span { U_g S, T U_g S : g in G }.

Every invariant superspace must contain these images; the span is invariant by
group multiplication and T²=-I. The exact dimension is the rank of the concatenated
images, not n plus a guessed number of bands. For approximate numerical covers,
certify generator leakage and propagate finite-word residuals explicitly.

PROVEN: T symmetry alone allows a4dimensional Hermitian block with energies
(a,a,b,b), paired by T²=-I, a!=b. It does not imply the scalar Gamma8 block
required by an irreducible cubic representation. A Kramers-pair check is not a
Gamma8-quartet check, and their means cannot be substituted for either spectrum.

CALCULATED: C3 cyclic axis permutation and S4 improper fourfold rotation generate
all24spatial Td operations (closure independently enumerated). On the actual
preliminary PBE176source, direct physical-G/spin residuals have maxima
.99427646 and.84793004, respectively. On the paired364auxiliary cover including
the reference6frame, maxima are.99993245 and.99995708. Each has300resolved
missing directions at1e-8 on that larger cover. Thus the new paired cover is
not a jointly invariant source space. Large leakage is a subspace statement,
not a measured full-density/operator Td defect or a material phase claim.

The very small noisy directions needed to cover the original numerical source
can be almost arbitrary crystal representations; adding them with their TR
partners does not automatically close their crystal orbits. Conversely, dropping
them or projecting the source changes the numerical state and must be bounded
under an explicit new protocol. Completing every exact noisy group orbit may
be unnecessarily costly; the relevant target is a symmetry-adapted variational
state with controlled density/action error, not guessed empty-band augmentation.

For the pure conventional8atom host, primitive translations are an additional
required symmetry to distinguish folded sectors. The existing physical6frame
transport tests remain valid; an enlarged solver space must independently check
its translation action rather than inherit that qualification from the frame.

**Decision:** even a passing native TR-constrained operator constructor cannot
release full host/Cd HSE SCF under a cubic Gamma6/Gamma8 interpretation. The
minimum next input is a self-consistent nonmagnetic **jointly symmetry-qualified**
host density/operator, from a symmetry-adapted constrained solver or independently
qualified direct exchange. A source-resolved residual and consistent finite-T
occupation/entropy/energy equations are needed; SCF energy error, local-zero spin,
near-degenerate PBE eigenvalues or a positive old Gram cannot replace them.
No additional repeated SCF trajectory is justified by the present information.

## Why an actual spectral residual is necessary at fixed FD width

For finite Hermitian H and fixed sigma>0, let f(E)=(1+exp((E-mu)/sigma))^-1.
In Hilbert-Schmidt norm the divided-difference Fréchet derivative gives
||f(H)-f(K)||_HS <= ||H-K||_HS/(4sigma): diagonalize H along the straight
Hermitian interpolation and bound every divided difference by sup|f'|.
Put K=THT^-1. Its spectrum and fixed-charge chemical potential are identical,
so ||D-TDT^-1||_HS <= ||H-THT^-1||_HS/(4sigma) for an EXACT FD solution.
At sigma=.001Ry the multiplier is250/Ry. This is a sensitivity bound, not an
SCF contraction or explanation of the measured instability. The retained
total-energy SCF error is not ||H-THT^-1|| or an eigenpair residual. Approximate
diagonalization and finite source tails need additional certified terms; the
bound cannot certify the observed density from a scalar SCF tolerance.

This identifies a concrete missing input: a source-resolved Hamiltonian residual
and jointly invariant spectral/occupation construction, or an independent
direct-exchange control meeting the same full-state symmetry gates. No guessed
two-band completion or postprocessed level average supplies that input.

The present native job has a narrower predeclared TR/operator scope and remains
scientifically informative: it measures enlarged direct actions, Gram positivity,
energy accounting and exactness of the new compression. It does not test or claim
cubic SCF, native integrated ACE, HSE convergence, chemistry or physicalx_c.
