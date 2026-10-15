# Chemical sign survives a different continuum-compatible probe

2026-10-15. CALCULATED from the accepted existing PBE+SOC k3/50-200Ry ordered
x=.25 host/Cd pair, using its original complex physical Gamma6/8 overlaps.
No new QE/SCF, spectra, frame, empirical coefficient or material fit.

At t=0 relative to each specimen's own Fermi level and eta=.05eV, the new
inverse-resolvent ordering response is **+0.354050668eV**, with conditional
positive-tail/frame/IEEE interval **[+0.344926560,+0.363174775]eV**.
All9preregistered t/eta choices are positive with certified numerical-model
sign intervals. Their values range+.352716880 to+.355384378eV; the smallest
conditional lower endpoint is+.331624517eV. At t=0 the three eta values change
the response by only.0933meV. This is finite tested-probe stability, not a
uniform eta->0, energy-domain or composition certificate.

The earlier W2Gaussian response remains+.392177486eV. The~38.127meV difference
is **observable dependence on the same Hamiltonian**, not new k-grid/material
error or an HSE functional correction. Neither response is the physical gap.
The result supports the direction of the Cd-induced projected response in this
ordered PBE cell through two different causal/bounded probe definitions. Both
absolute Gaussian orderings remain negative; do not turn a positive chemical
DIFFERENCE into normal band ordering or physicalx_c.

## Bound and conditions

PROVEN UNDER ASSUMPTIONS: a normalized positive projected spectral measure has
|1/(z-e)|<=1/eta without a support-free real-energy domain. Missing positive
mass r changes g by at most r/eta. The existing fixed-frame projector bound
adds2epsilon/eta, and retained-weight arithmetic adds b/eta. Put delta equal
to their sum. If |g_ret|>delta, the scalar inverse identity gives

    |g^-1-g_ret^-1| <= delta/(|g_ret|(|g_ret|-delta)).

Summing four radii bounds the paired difference. These are conditional native-
model/tail/frame estimates, with exactly the previously qualified NC/Td/IEEE
assumptions. No unknown SCF eigenpair, HSE, many-body, finite-cell, k/q or
real-alloy error is hidden in those intervals. No spectrum is renormalized.
Independent complex matrix traces reproduce each scalar contraction; energy
gauge and single-pole identity checks pass. One initial JSON serialization of
a NumPy boolean failed after arithmetic; the explicit Python-bool correction
changes no numeric criterion or native data and the retained result now writes.

Causality alone does not bound g away from zero: the equal two-pole measure at
+/-a has g(i eta)=-i eta/(a²+eta²). Its inverse grows arbitrarily with a. Thus
the inversion-margin gate is indispensable; a projected antiresonance cannot
be mistaken for a quasiparticle pole. Analytic eta is not material linewidth.
Own-Fermi alignment is a declared filling-relative probe, not a band offset.

## Decision

Retain this additional conditional PBE chemistry sign result; do not infer a
gap, composition law, alloy critical composition, topology or optical cutoff.
The current symmetry obstruction in hybrid exchange is independent of this
read-only PBE evidence. The minimum next functional input remains a jointly
symmetry-qualified self-consistent host operator/density, then matched Cd under
the same model. Another PBE mesh, endpoint fit or scalar occupation average
would not identify that missing information. Prior continuum/identifiability
negative results and all native refusals remain unchanged.

This uses established Stieltjes/resolvent perturbation mathematics; no novelty
claim. See the prior continuum_spectral/bounds.md for broader causal bounds and
the distinctions between operational orderings, peaks, poles and topology.
