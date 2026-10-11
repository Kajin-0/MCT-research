# Foundation: two projected spectral measures inside a continuum

## F1. Model and observable, before any approximation

Work first in finite volume, with a static self-adjoint configuration operator
H_omega(x), a declared disorder law and normalized physical density operators
rho_alpha=P_alpha/d_alpha, alpha=6,8, d6=2, d8=4. All comparisons use one physical
Hilbert space or a specified unitary transport between spaces. Define

```text
g_alpha(z,x) = E_x Tr[rho_alpha(x) (z-H_omega(x))^(-1)]
mu_alpha(B;x) = E_x Tr[rho_alpha(x) 1_B(H_omega(x))].
g_alpha(z,x) = integral dmu_alpha(t;x)/(z-t),
mu_alpha >= 0, mu_alpha(R)=1.
```

These are probability measures (dimensionless), distinct from the eliminated
kernel measures nu_alpha, which have units energy squared. The sign convention
is anti-Herglotz: -Im g>=0 in the upper half-plane. Self-adjoint unbounded
operators also admit this normalized representation for trace-class rho;
bounded test functions require no finite energy moments or density assumption.
For a thermodynamic Gamma Bloch projection, specify the normalized finite-cell
embeddings and require their projected measures to converge weakly to a
probability measure. Tightness/normalization and uniform errors are additional
gates, not consequences of knowing the almost-sure spectrum. An infinite
Bloch wave is not silently treated as a normalizable Hilbert-space vector.

For fixed eta>0, expressly an analytical resolution in eV,

```text
P_eta(u)=eta/[pi(u^2+eta^2)],
A_alpha^eta(E,x)=-(1/pi) Im g_alpha(E+i eta,x)
              = integral P_eta(E-t) dmu_alpha(t;x).
```

A>=0, integral A dE=1 and A is smooth in E even for atoms, thresholds,
singular-continuous measures or full-support continua. No eliminated-measure
gap D, real-energy derivative sign or limiting-absorption assumption is used.
Eta is not the intrinsic disorder linewidth, instrument resolution or a
parameter chosen to obtain an inversion. Instrument response must be supplied
separately; a measured Gaussian response is not automatically this Poisson
response. Fix eta, the window and the projection rule before interpreting signs.

## F2. Exactly what symmetry and a causal kernel reduce

Under ensemble translations, nonmagnetic Td double-group symmetry, and one
specified retained copy of each inequivalent irrep, Schur's lemma gives
g6 I2 direct-sum g8 I4. Individual disorder configurations need not have Td.
Several copies of an irrep instead have a matrix in copy space; symmetry does
not select the physical retained copy. Strain or applied magnetic field changes
the symmetry and requires a separately specified matrix/observation adapter.

In the static augmented-space construction with a well-defined Feshbach block,

```text
g_alpha=[z-e_alpha-K_alpha(z,x)]^(-1),
K_alpha=integral dnu_alpha(t;x)/(z-t), nu_alpha>=0.
```

Thus Im(z-e-K)>=eta and |g|<=1/eta in the upper half-plane. The old common/mass
algebra D6=F_s-M and D8=F_s+M still holds. Inside spectral support it gives
neither a monotone real common trajectory nor equivalence of peaks and mass
zeros. This sprint uses g or mu directly, avoiding unstable inverse extraction.
Reference repartition e->e+delta, K->K-delta leaves g unchanged. Do not add a
full host T as a residual to a binary chord. The prior strain/full-residual T,
reaction-kernel, retarded-versus-reactance and SOC directional results remain
requirements for any microscopic input adapter.

## F3. Physical projection and energy-reference gates

Predetermine P6(x),P8(x) by transport of physical reference spinors, or another
explicit symmetry-resolved injection with a certified error. A spectral Riesz
projector for an isolated band cannot be presumed inside a continuum. A fixed
host-orbital injection can exist there, but measures its projected character,
not a unique surviving eigenbranch. The window must not select a desired peak
and then use that peak to define its projector. Basis rotations within P and
consistent ambient unitary transformations leave traces invariant; changing P
physically changes the observable. Labels and scalar ensemble symmetry do not
remove this ambiguity. [Bounds](bounds.md) quantify it through trace distance.

Choose one declared energy reference r(x) and one compact window relative to
it. Under H->H+delta I, r->r+delta and window->window+delta, both sector centroids
shift by delta and their difference is unchanged. Keeping an absolute window
fixed while shifting only H changes the observable. Residual alignment errors
belong in the operator/window budget. The composition path must specify lattice
parameter, homogeneous and local strain, carriers, disorder correlations and
physical temperature, including whether ions are frozen.

The static HSE/QSGW auxiliary spectrum is not automatically the physical
many-body spectral function. For canonical fermion addition/removal Green
functions the positive normalized Lehmann measure supplies the same functional
bounds, provided both addition and removal weight and the chosen physical
frame are included. A static-operator norm comparison does not bound an unknown
many-body self-energy: supply a Green-function/measure error instead. Physical
0-K includes a declared zero-point electron/phonon convention. Frozen-ion and
finite-temperature data need a bounded adapter before any such physical claim.

## F4. Relation to measurements and sharp inversion

ARPES intensities include occupations, matrix elements, surface/momentum
selection, backgrounds and instrument convolution. They are not directly
mu6 or mu8; unoccupied weight and symmetry decomposition may be missing.
Optical magnetotransmission measures transitions/current vertices and filling,
not two independently normalized one-particle measures. Inferring them requires
an independently justified observation operator and its uncertainty. No raw
archive is recovered here, and the Stage-0 gates are unchanged.

Two operational orderings are defined in [the comparison](observables_and_failures.md).
Neither generally equals sharp Gamma eigenvalue ordering, the real inverse-Green
crossing, a shared complex resonance, an absorption/support edge or topology.
Sharp inversion remains **OPEN**. No analytic sheet for resonances is assumed:
a general positive measure need not continue through its cut meromorphically.
