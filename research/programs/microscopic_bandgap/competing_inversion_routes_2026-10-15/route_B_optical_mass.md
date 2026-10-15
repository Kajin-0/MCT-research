# RouteB: a signed spectroscopic Kane criterion without a zero-field atom

All theorems here are **PROVEN UNDER ASSUMPTIONS** for the declared model.
The Kane Landau spectrum and magneto-optical extraction are established by
Orlita2014/Teppe2016, not new discoveries. No measured material coefficient or
gap-law fit is imported. The purpose is a falsifiable independent observable
and an explicit boundary for using it as a physical inversion criterion.

## B1. Start with a transition that the experiment can actually see

In the six-state spherical linear Kane model, reference the flat HH energy
to zero, set the signed Gamma6/Gamma8 separation to2M, and keep one fixed,
identified electron Landau family at p_z=0. Its HH-to-electron transition has

    T(B)=M+sqrt(M^2+a B),    B>0, a>0.                     (B1.1)

a contains velocity, field units, index and Zeeman-family factor. This follows
from the two bright states' quadratic equation E(E-2M)=aB; HH supplies the
zero-energy dark state. In the usual convention a=(e hbar v^2/2)(4n-2+sigma).
Index/spin and optical selection MUST be tracked; two different families
cannot be substituted as two field values of the same a. Independent small
oscillator-matrix tests use the actual circular current of a Kane block,
not an arbitrary transition between optically dark eigenvectors.

Positive T(B) exists for both signs of M. At B->0 its limit is2M for M>0 and
zero for M<0: an inverted cubic Kane system remains excitation-gapless even
with a negative signed Gamma separation. The optical model parameter is not
a negative excitation threshold. Finite split-off, HH curvature, warping,
BIA, carrier filling, p_z integration and self-energy/vertex terms change
(B1.1) and require independently bounded remainders, not silent neglect.

For 0<B1<B2 let t_j=T(B_j),

    Q=B2 t1^2-B1 t2^2,   D=B2 t1-B1 t2.

Eliminating a gives the velocity-independent signed witness

    M=Q/(2D),   D>0,   sign M=sign Q.                     (B1.2)

Proof of D>0: T(B)/B=a/[sqrt(M^2+aB)-M] decreases strictly. This is algebra
within the standard Kane model, not a new microscopic composition law. A
third field independently tests that [T(B)^2-2M T(B)]/B is constant. A
successful two-field extraction alone cannot test the two-parameter family.

**Operational definition.** M_opt(B1,B2,x) is the right side of(B1.2), for
precisely specified transition centers on a common specimen/state/field path,
only when the D margin and identification/error gates below pass. Its zero
is a finite-field spectroscopic reversal. Identification with a zero-field
real-inverse Kane mass, sharp order, mobility transition or topology needs
separate physical hypotheses; it is not a consequence of the definition.

## B2. An exact no-atom model in which this criterion retains signed order

Let H_c(B) be this finite Kane Landau model and let

    H_omega(B)=H_c(B)+C_omega I,

where C has a non-atomic continuous distribution. Average single-particle
spectra have no atoms. At fixed particle number the occupied eigenvectors,
energy DIFFERENCES and all current matrix elements are unchanged in every
configuration. The exact absorption transition measure therefore still has
the Kane transitions and M_opt=M. Instrument convolution can make the
observed lines finite-width without changing that conclusion if its center
and tails are controlled. Thus lack of a zero-field one-particle delta atom
does not, by itself, invalidate a signed optical Kane criterion.

This is an existence/cancellation theorem, not a claim that real short-range
HgCdTe disorder is a global scalar shift. Spatial scalar disorder generally
does not commute with the kinetic operator. At fixed grand-canonical chemical
potential even a global C can change Pauli weights; the canonical occupation
hypothesis must not be omitted. Homogeneous linewidths or a finite eta are
not automatically this cancellation model.

## B3. Bounded measured centers: no unbounded Lorentzian moments

Use a positive, isolated transition measure (absorption structure factor with
known optical factors removed), not a raw minimum of normalized transmission.
Its center t_j is an admissible line parameter only with an independently
qualified line shape/window. Symmetric finite-first-moment broadening preserves
the full centroid; a Lorentzian has no absolute first moment, so that argument
does not apply to it. Broad 3D Landau-band thresholds are generally asymmetric
and their centroids/peaks need not be the p_z=0 value in(B1.1).

For a measured window and a reference energy E*, let retained mass and
centered moment be d,n, with t_win=E*+n/d. If missing positive mass<=tau and
missing absolute centered moment<=tau1, then

    |t_full-t_win| <= [tau1+|t_win-E*| tau]/d.             (B3.1)

If measured d_hat,n_hat have errors epsilon0,epsilon1 and d_hat>epsilon0,
the retained centroid error is bounded by

    [epsilon1+|n_hat/d_hat| epsilon0]/(d_hat-epsilon0).    (B3.2)

These are positive-measure ratio bounds, not estimates of unknown material
tails. Include calibration, overlap/background, occupations, p_z/HH/8-band
model and self-energy/vertex remainder in a prospective total delta_j. A
finite observed window alone cannot bound tau1. For a longitudinal momentum
cutoff p_max, the bright energy correction is bounded by
v^2 p_max^2/[2 sqrt(M^2+aB)] in consistent momentum units; an actual bulk
optical kernel must justify such a cutoff and omitted contribution.

Given t_hat_j>0, |t_hat_j-t_j|<=delta_j and |Bhat_j-B_j|<=beta_j, set

    epsilon_Q = Bhat2(2|t_hat1|delta1+delta1^2)
              +Bhat1(2|t_hat2|delta2+delta2^2)
              +beta2(|t_hat1|+delta1)^2+beta1(|t_hat2|+delta2)^2,
    epsilon_D = Bhat2 delta1+Bhat1 delta2
              +beta2(|t_hat1|+delta1)+beta1(|t_hat2|+delta2).

If D_hat>epsilon_D, then with M_hat=Q_hat/(2D_hat),

    |M-M_hat| <= [epsilon_Q+2|M_hat|epsilon_D]
                   /[2(D_hat-epsilon_D)].                (B3.3)

The sign is certified if |Q_hat|>epsilon_Q and the denominator stays positive.
Units: M,t in energy, a in energy^2/field, Q in field energy^2 and D in
field energy. No delta spectral atom or common eliminated-support gap is used.
The line-to-Kane remainder is part of delta_j, not presumed zero because a
curve looks Kane-like. Uncertain transition assignment is a separate refusal.

## B4. A zero-mean mass distribution creates a NORMAL optical bias

**PROVEN within an incoherent domain-mixture model**, not exact coherent alloy
SCBA. Let each domain have T_omega(B)=M_omega+sqrt(M_omega^2+a_omega B),
a_omega>0, with field-independent positive NORMALIZED line weights. The
intensity-corrected centroid is t(B)=E T_omega(B). This weight assumption
does not follow from Kane oscillator strengths or carrier occupation; it must
be tested/corrected. If the joint weighted law is symmetric under M->-M,

    t(B)=E sqrt(M^2+aB),
    t(B)/sqrt(B)=E sqrt(M^2/B+a).

The latter decreases strictly with B whenever P(M!=0)>0. Hence Q>0 and the
two-field M_opt is positive even though E M=0. Mean criticality, optical
centroid criticality and the positive-measure disorder crossover differ.

For equal weights M=+/-m and fixed a, exactly

    t(B)=sqrt(m^2+aB),
    M_opt=m^2(B2-B1)/[2(B2 sqrt(m^2+aB1)-B1 sqrt(m^2+aB2))]>0. (B4.1)

For m^2 << a B1 the leading bias is

    M_opt = m^2/(2sqrt(a)) (1/sqrt(B1)+1/sqrt(B2))
               + higher terms.                          (B4.2)

The expansion is conditional, but the sign statement is exact. Three distinct
fields reject an EXACT homogeneous Kane representation of(B4.1) if m!=0:
the equation m^2+(a-a_eff)B-2M_eff sqrt(m^2+aB)=0 is strictly convex or
concave if M_eff!=0 and cannot vanish at three ordered points; with M_eff=0
it is affine and cannot do so unless m=0. Finite error bars may obscure the
third-field discrepancy, and general mixtures can reproduce finitely many
data: passing this test is not distribution identification.

Conversely, if ALL weighted domains have M>0, t(B)/sqrt(B) decreases; if all
have M<0 it increases, since the derivative of each is

    -M/[2 B^(3/2)] [1+M/sqrt(M^2+aB)].

Thus field-independent mixtures preserve a common mass-support sign, but a
measured sign alone does not prove that all domains share it or identify mean
M. Field-dependent oscillator/Pauli weights can defeat even this inference.

### The bias also survives a real Kane-current weighting example

For the actual flat-HH Landau block and its circular current, the isolated
HH-to-electron line strength is g_n times(1+M/s)/2, s=sqrt(M^2+aB), with a
geometric g_n independent of M. For equal-volume domains M=+/-m with the SAME
current, the intensity-normalized center of their two lines is therefore

    t_current(B)=s+m^2/s.                                (B4.3)

It also produces Q>0 for m!=0: t_current/sqrt(B)=sqrt(a+y)+y/sqrt(a+y),
y=m^2/B, decreases with B because its derivative with respect to y is
(3a+2y)/[2(a+y)^(3/2)]>0. Thus the normal bias is not solely an artifact of
assigning equal oscillator weights. This is an incoherent-domain current
calculation; coherent short-range alloy disorder requires the vertex treatment
in `transition_disorder_closure.md`. Tests diagonalize the native-free Kane
oscillator block and use its actual circular current to verify(B4.3). Photon
prefactors must be removed to recover this defined S_J center; it is not a
raw-transmission peak formula. No universal third-field theorem for arbitrary
coherent disorder is asserted.

### Quantitative third-field falsification

With the mass error eM from(B3.3), infer a_hat=(t_hat1^2-2M_hat t_hat1)/Bhat1
only as a test parameter. An explicit interval is |a-a_hat|<=ea, where

    eN=2|t_hat1|delta1+delta1^2
         +2[|M_hat|delta1+(|t_hat1|+delta1)eM],
    ea=(eN+|a_hat|beta1)/(Bhat1-beta1).

Require a_min=a_hat-ea>0, B3_min=Bhat3-beta3>0 and ordered field intervals.
The predicted third-center error is at most

    2eM + B3_max ea/[2sqrt(a_min B3_min)]
          +a_max beta3/[2sqrt(a_min B3_min)].

Add the independent third-line error delta3. A measured discrepancy exceeding
this sum rejects the constant-parameter Kane/line adapter at that precision,
not Kane physics with all possible field-dependent self-energies. Passing
does not establish atom, topology or a unique disorder distribution. M_opt
and a_hat are diagnostic outputs; a nonempirical forward theory must supply
its own Hamiltonian/disorder inputs before comparison with experiment.

## B5. Conditional root and physical phase boundary

If a microscopic/observational model independently bounds
|M_opt(x)-mu_K(x)|<=epsilon_model and numerical/experimental error<=epsilon_num,
and the intended physical real-inverse mass has a valid common trajectory,
unique branch and composition modulus s>0, sign brackets and

    |x_opt-x_K| <= (epsilon_model+epsilon_num)/s

follow on the verified interval. Independent composition assay/spatial errors,
T->0, strain, carrier and lattice-path corrections enter separately. This is
a possible sharp-atom-free **operational** route, not yet a material interval.
Without the adapter it predicts only x_opt for specified fields/centers.
An insulating or mobility/topological phase boundary needs its own global
hypotheses; finite damping and Green zeros prohibit assuming equivalence.

The original physical x_c remains OPEN. Theorems B1–B4 construct a measurable,
falsifiable route and show exactly how disorder can fool it, rather than
postulating a scalar mass and declaring its zero a phase transition.
