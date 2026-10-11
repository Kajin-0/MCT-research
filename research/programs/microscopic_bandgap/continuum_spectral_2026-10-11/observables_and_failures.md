# Two competing orderings and explicit failure conditions

Use the [normalized projected measures](foundation.md) and fixed eta>0.
The entire spectral function is averaged before either operation below.
Averaging per-configuration centroids/peaks is a different observable.

## Candidate C: finite-window projected centroid ordering

Predetermine a smooth compact window chi(E-r), 0<=chi<=1, half-width W.
For each sector take its retained weight m_alpha and centered first window
moment n_alpha, then

```text
C_alpha^eta = r+n_alpha/m_alpha,
Omega_C(x;eta,chi,P,state)=C6^eta-C8^eta.
```

This is a bounded ordering of *windowed projected spectral weight*. It is
not the original signed Gamma gap and is not named E_g. It retains multiple
peaks rather than selecting one. Its continuum stability requires only a
window-mass floor and the bounded moment errors in S5; no spectral-density
regularity or support-free domain is hidden. A bounded test-function contrast
F_f(mu6)-F_f(mu8) is cheaper still, but need not have even an energy-ordering
interpretation; the normalized centroid uses the window's actual weight.

In the isolated narrow-line limit, with both lines well inside a flat part
of chi and omitted/response corrections tending to zero, C_alpha tends to
its line energy. Outside that separately qualified limit, satellites and
continuum weight move it. The exact all-energy centroid of the earlier frozen
linear-substitution model is VCA for every configuration; that established
sum rule does not fix this finite-window centroid or validate a peak. An
unwindowed centroid of A^eta is generally undefined (S3).

**Inputs:** only four projected integrals m6,n6,m8,n8 per composition,
their joint errors and a physical-frame/state/response definition. Equivalently
use g6,g8 on the integration window with uniform errors and coverage/tail
certificates. A full local covariance or all finite-q tensors need not be
tomographed separately if their effects on these contractions are bounded.

**Measurability:** an independently calibrated symmetry-resolved one-particle
probe, including enough occupied/unoccupied coverage and response information,
could supply these moments. Current ARPES or magneto-optical plots do not
automatically do so. A valid forward spectral calculation in the same frame
is an alternative; binary host controls are not that calculation.

**Falsification gates:** small/unknown retained weight; state-dependent or
post-selected window; unqualified projectors; fitted-gap reconstruction of
spectra; unbounded missing nearby weight; uncontrolled many-body/zero-point
adapter. These reject physical prediction, not the conditional theorem.

## Candidate P: isolated or explicitly tracked peak ordering

On declared compact sector search windows define

```text
p_alpha^eta(x)=selected argmax_E A_alpha^eta(E,x),
Omega_P(x;eta,I,P,state)=p6^eta-p8^eta.
```

For a global dominant peak, specify ties as ambiguity rather than silently
selecting a root. For a branch-tracked local peak, specify its starting branch,
neighbourhood and continuation rule; the local maximum must remain strictly
isolated/curved throughout the path. Tracking is not the same observable as
the global maximum. S6 applies to a certified global search window or to a
predeclared tracked neighbourhood with the relevant isolation gate.

This ordering is closer to reported dispersing maxima, but demands height,
curvature, separation and possibly derivative errors. It can change while
Candidate C stays fixed, or remain fixed while C moves. Both are operationally
meaningful only after a probe adapter is supplied. Broad linewidth alone does
not prevent a stable peak; absence of a separation margin does.

For D(E+i eta)=F+iGamma, Gamma>0, its stationary equation is
Gamma'(F^2-Gamma^2)-2Gamma F F'=0. A Re D zero is stationary only if
Gamma'=0 there. Neither peak equality nor centroid equality imposes equal
damping or shared complex poles. An isolated delta measure has a peak at its
eigenvalue, but this special limit does not identify continuum peaks with poles.

**Falsification gates:** ties, peak merger, loss of curvature, window-boundary
maximum, or projector/branch swapping. Decreasing eta without a joint bound
does not rescue them. No physical eta->0 peak limit is asserted.

## Counterexamples retained from three cycles

All examples below are **PROVEN UNDER ASSUMPTIONS** mathematical information
tests; their inexpensive checks are **CALCULATED**, not material validation.

### N1. Tiny missing weight defeats an unbounded centroid

mu_tilde=delta_0 and mu=(1-s)delta_0+s delta_L have TV difference 2s. Their
first moments differ by sL, arbitrarily large for any fixed s>0. Their finite
eta spectral heights differ by at most 2s/(pi eta). Small measured residual
on a finite window cannot supply the all-energy moment or a dispersion
relation for an unknown self-energy without tail information. Candidate C
escapes the unbounded moment by fixing a bounded window; it still needs m>p.
Renormalizing an incomplete spectrum obscures this missing information.

### N2. A negligible window denominator defeats ratio stability

For a window covering -1 and +1 but excluding a distant R, compare
(1-s)delta_R+s delta_(-1) and (1-s)delta_R+s delta_(+1).
Their TV difference is 2s. Choose R so its Poisson leakage into the window
is o(s). The conditional window centroids differ by almost 2 eV as s->0.
Thus positivity and fixed eta alone give no uniform ratio Lipschitz bound.
S5's retained-weight floor is indispensable. A sharp unsmoothed window also
fails weak-continuity control: an atom crossing its boundary causes a jump;
smooth windows or explicit resolution avoid that separate obstruction.

### N3. Equal coherent centroids, different continuum-window orderings

Let sigma be the uniform probability density on [-2,2] eV. Define

```text
mu_plus  = b sigma+(1-b)[0.8 delta_(+1)+0.2 delta_(-4)],
mu_minus = b sigma+(1-b)[0.8 delta_(-1)+0.2 delta_(+4)], 0<b<1.
```

Both total masses are one and both exact full first moments are zero, but
an even window on [-1.5,1.5] eV has opposite nonzero centroids for sufficiently
small fixed eta. Both measures have continuous support through the retained
window; no gap is required or present. A Gamma8 spectator with measure sigma
has centroid zero. Set h(x)=16[x(1-x)]^2 and mix each candidate with the same
binary reference measure: (1-h)mu_ref(x)+h mu_plus/minus. All binary measures,
first endpoint jets and full centroids agree, but interior Omega_C differs.
This is a causal spectral-family counterexample, not a full fixed-interaction
Bernoulli realization. The earlier I1 separately supplies that stronger local
Hamiltonian non-identifiability theorem. Symmetry copies of these scalar baths
can realize the retained doublet/quartet traces.

### N4. Arbitrarily small causal changes switch the dominant peak

mu_s=(1/2+s)delta_(-1)+(1/2-s)delta_(+1). At small fixed eta it has two
strictly curved local peaks. At s=0 they have equal global height; the global
maximum jumps from one to the other as s changes sign although TV(mu_s-mu_-s)
=4|s|->0. A small common continuous density can be added without removing
this failure. Local curvature alone does not guarantee global peak stability;
the missing global separation margin is decisive. Candidate C remains
continuous. Even two distinct equal peaks in one sector prevent a unique
scalar gap without an extra, physical selection rule.

### N5. No universal sharp spectral limit from finite eta

Compare mu=delta_0 and mu_h=uniform[-h,h]. For Im z>=eta,
|g_h(z)-1/z|<=h^2/(3eta^3), by subtracting the zero first moment and using
the exact second-order resolvent identity. One measure has an atom, the other
has none, and both are causal. Arbitrarily accurate finite-resolution data
therefore cannot by themselves certify a sharp pole.
For mu_N=delta_(1/N), A_N^eta(0)=eta/[pi(N^(-2)+eta^2)]. Taking N->infinity
then eta->0 gives infinity; reversing these limits gives zero. This exact
causal example forbids a general interchange of volume/parameter/boundary
limits. Composition-dependent moving atoms give the analogous warning.
Fixed-eta bounded functionals can remain continuous despite this failure.

### N6. Positive spectra do not supply composition transversality

Take a Gamma6 line at v(x-x*)^3 and a Gamma8 line at zero, with v>0.
Their fixed-eta peaks give Omega_P=v(x-x*)^3. A constant ordering error
epsilon shifts its root by (epsilon/v)^(1/3). No universal linear error
certificate follows from causality, finite eta or smooth energy dependence.
More generally, finite composition samples can be preserved while an added
smooth interior bump changes derivatives or adds crossings. S7's lower
modulus or a certified narrow sign bracket cannot be supplied by endpoint fits.

### N7. Gamma spectral information does not fix bulk topology

An explicit two-band information witness is
h_c(k)=sin(kx)sigma_x+sin(ky)sigma_y+
[1-c(2-cos(kx)-cos(ky))]sigma_z. At Gamma, h_c=sigma_z for all c.
For c=0 the gapped vector has positive z component and degree zero.
For c=1 the north-pole preimage is only Gamma, with positive local orientation,
so the normalized Bloch-vector map has degree one. Gap closure is absent in
either endpoint model: the four sin-zero points have nonzero z masses.
Their Gamma resolvents are identical for every eta while occupied Chern
numbers differ in magnitude. Time-reversed block partners give the analogous
spin-conserving TR information example. This is an established two-dimensional
model class, not a zincblende/HgCdTe Hamiltonian. Alternatively a decoupled
topological spectator is wholly invisible to the retained projection.
The logic is that projection discards global information; no material-specific
Td/topology inference is repaired without that information and its gap gates.

### N8. Symmetry labels do not select one irrep copy

For two equivalent Gamma6 copies at energies e1,e2, a symmetry-covariant
injection mixing their copy index by angle theta has mean
e1 cos^2(theta)+e2 sin^2(theta). Its spectrum is a positive two-line mixture.
Rotations inside an already fixed copy are harmless, but changing the retained
copy changes windowed centroids and peaks. Scalar symmetry, labels and the
absence of a spectral gap cannot determine the physical projector rule.

## Comparison and stopping boundary

| Property | Candidate C | Candidate P |
|---|---|---|
| Inputs for value | Four window integrals and positive mass floors | Two spectra on selected search windows |
| Continuum hypotheses | Positivity, bounded functions, declared frame/resolution | Same plus isolation and curvature |
| Error dependence | Linear in qualified moment errors | Square-root in height errors; linear with derivative bounds |
| Multiple components | Included with their weights | Ambiguous unless physical tracking rule supplied |
| Resolution/window dependence | Explicit and bounded where input permits | Explicit; merging/switching can destroy stability |
| Zero interprets | Reversal of windowed projected weight ordering | Reversal of selected maxima ordering |
| Original sharp x_c / topology | Neither certified | Neither certified |

Candidate C is the minimum-input continuation **if** new qualified physical
contractions become available. At present neither candidate passes the material
input gate, so no physical prediction or acquisition is advanced.
