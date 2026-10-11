# Endpoint impurity slopes depend on the declared volume path

**PROVEN (chain rule and the dilute-impurity expansion):** an isolated
substitution at fixed host geometry gives a concentration derivative at that
geometry. It does not include the homogeneous strain caused by a changing
alloy lattice parameter. This distinction is necessary when the two binary
references use different lattice constants.

Let the signed gap be E(x,a), with a a conventional cubic lattice parameter,
and declare a composition path a(x), with a(0)=a_H and a(1)=a_C. Write

    v_H = a'(0) [partial_a E_H(a)] at a_H,
    v_C = a'(1) [partial_a E_C(a)] at a_C.

Both v quantities have units of eV per unit Cd fraction. Let
tau_H = <6|T_Cd|Hg(E_6)|6> - <8|T_Cd|Hg(E_8)|8>, and let tau_C be the
corresponding full Hg-in-CdTe gap projection. These are full impurity
operators relative to the fixed-geometry pure hosts, not VCA residuals.
Then the endpoint slopes along the declared volume path are

    g_0 = tau_H + v_H,
    g_1 = -tau_C + v_C.

The sign reversal in g_1 comes from the dilute Hg fraction y=1-x. The
strain term keeps its d/dx sign. If the impurity potential is already
defined relative to a composition-dependent strained reference, subtract
that reference derivative once and add the strain derivative once; do
not count either twice.

For an affine lattice path, a'(0)=a'(1)=a_C-a_H. The present companion
calculations use a_H=6.46 and a_C=6.48 Angstrom from
[Nicklas and Wilkins (2011)](https://link.aps.org/accepted/10.1103/PhysRevB.84.121308).
Their difference is not an impurity response. No numerical deformation
potential has been calculated in this tranche, and the strain contribution
cannot yet be declared negligible at a few-meV accuracy target.

## Effect on the endpoint reductions

Let DeltaE=E_C-E_H, Ebar=(E_H+E_C)/2, and x_0=-E_H/DeltaE. Within the
reciprocal boundary completion, adding the path terms changes the inferred
coefficients by

    delta A_slope = (v_H+v_C)/DeltaE,
    delta C = (E_C v_H+E_H v_C)/DeltaE,
    delta rho = [x_0 v_C-(1-x_0)v_H]/DeltaE.

These are exact boundary-data identities; they do not identify strain as
a dynamical impurity susceptibility. Thus agreement of A_slope with an
energy derivative of T requires the same volume-path convention, in
addition to the reciprocal-law assumptions.

For the common-mode mass, define w_H=a'(0) partial_a M_H and
w_C=a'(1) partial_a M_C, with the same prescription for the common-mode
reference energy at both endpoints. At pure, energy-independent binary
Hamiltonians, M=E/2 and w_H=v_H/2, w_C=v_C/2. If tau_mH and tau_mC are the
full fixed-volume common-mode impurity mass projections, the mass slopes
are u_0=tau_mH+w_H and u_1=-tau_mC+w_C. Therefore

    mu_3 = M_H+DeltaM x
           + [(tau_mH+tau_mC+w_H-w_C)/2] k
           + [(tau_mH-tau_mC+w_H+w_C-2DeltaM)/2] k s,

where k=x(1-x), s=1-2x. In particular, the pair-dominance diagnostic is

    u_0+u_1-2DeltaM
    = tau_mH-tau_mC+w_H+w_C-2DeltaM.

It is not the bare opposite-impurity mismatch if strain is omitted from
those impurity operators. This retains the full/residual reference correction
derived in [the impurity reference note](impurity_reference_and_threshold.md).

## Required microscopic implementation

Declare either a single fixed lattice for the complete electronic problem,
or a specific a(x). For the latter, obtain endpoint deformation potentials
from binary calculations at nearby lattice constants with unchanged
electronic settings. Converge the finite difference independently; never
infer it from measured alloy gaps. Local ionic relaxation around a defect
is a separate contribution to the impurity potential and is still deferred
for the first fixed-ion electronic test.

**CALCULATED:** no new bandgap or strain number here.
**HYPOTHESIS:** none needed for the chain-rule correction.
**NOVELTY CANDIDATE:** none; this is an established strain/impurity
separation applied to the current microscopic endpoint protocol.
