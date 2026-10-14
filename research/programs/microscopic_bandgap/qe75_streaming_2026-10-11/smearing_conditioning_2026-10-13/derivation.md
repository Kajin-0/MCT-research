# Cold-smearing conditioning and the actual numerical boundary

## PROVEN: scalar conditioning, not whole-SCF stability

Put y=x−1/sqrt(2), f(x)=erf(y)/2+exp(−y²)/sqrt(2pi)+1/2.
Then f'(x)=exp(−y²)(1−sqrt(2)y)/sqrt(pi). Stationary points of f'
are y=(1±sqrt(5))/(2sqrt(2)); compare both and the vanishing tails to obtain
L=sup|f'|=0.7541710171545021 (rounded displayed value). The positive maximum is
at the minus root. With sigma>0 and any REAL epsilon,mu pairs,

    |f((muA−epsilonA)/sigma)−f((muB−epsilonB)/sigma)|
       <= (L/sigma)(|delta mu|+|delta epsilon|).

A common shift of BOTH mu and epsilon leaves occupations unchanged; the
bound stated with separate differences is conservative and reference dependent
in its decomposition, although the occupation observable is reference invariant.
A sharper bound uses |delta(mu−epsilon)|. Compare the same energy reference;
do not subtract an independently fitted offset to rescue a failure.

For the QE implementation, exp argument is min(200,y²). Its difference from the
unclipped real function is between0 and exp(−200)/sqrt(2pi) at each point. Add
TWICE this constant for a pair. In its clipped tails w0gauss is not literally the
derivative of clipped wgauss; the former retains an exponentially tiny linear
factor. Do not extrapolate a numerical w0gauss tail as a global exact derivative.
Floating-point function evaluation has a separate allowance eta_f, requiring
independent qualification at each actual input; a compiler/libm is not a theorem
of correctly rounded erf. The new native gate reconstructs weighted wg bitwise
with the unedited compiled gweights_only AND checks analytic f independently.

## PROVEN UNDER ASSUMPTIONS: local neutrality inversion

N(mu)=sum_nk wk f((mu−epsilon_nk)/sigma), positive wk summing1. If on a
CERTIFIED interval I, N'_A(mu)>=m>0 and both compared chemical potentials lie
in I, then

    |muA−muB| <= [|rA|+|rB|+(L/sigma) sum_nk wk |delta epsilon_nk|]/m,

where r=N(mu)−Ne. Proof: MVT for N_A and triangle inequality comparing N_A(muB)
with N_B(muB). No such global inverse follows from charge neutrality alone.
For the ideal function, |f''|<= [2sqrt(2)/e+2/sqrt(2e)+sqrt(2)]/sqrt(pi)<2,
so N'(mu0)−96 radius(I)/sigma² is a conservative lower bound with48 bands.
This is a finite-interval, fixed-spectrum statement; it does not establish a
unique global Fermi root or a contractive self-consistent density map.

The new pilot instead captures native ef independently and bounds its difference
directly. The neutrality theorem is retained as a conditional alternative, not
a concealed proof that QE always produces a suitably conditioned root.

## FALSIFIED: generic monotonicity / charge neutrality implies unique mu

f' changes sign at x=sqrt(2); f overshoots1. For target1.04 there are two roots
x=1.046828646906396 and2.014193996060466. Thus a cold occupation's neutral-root
inversion needs a branch/interval hypothesis. The fractional target is a
mathematical counterexample, not the electron number of this HgTe specimen.
QE7.5 efermig first Gaussian-bisects, then Newton-minimizes the squared charge
error, accepting cold/MP residual<0.01 electrons before possible cold bisection.
A successful return is NOT a universal1e-10 electron charge certificate.

## PROVEN: independent weighted-density metric

Let gammaA=A Fa A† and gammaB=B Fb B† in the identical actual reciprocal basis,
Fa,Fb real diagonal occupation matrices. QR A=Q RA, Q†Q=I, S=Q†B,
R=B−QS, M=R†R, C=S Fb, D=RA Fa RA†−S Fb S†. Orthogonal block decomposition gives

    ||gammaA−gammaB||F² = ||D||F² +2 tr(C M C†)+tr(Fb M Fb M).

This identity avoids cancellation between large traces and works for imperfectly
orthonormal native A; it never forms the large gamma matrix. The implementation
has finite QR/BLAS roundoff, checked independently against a direct small matrix
including nonorthonormal columns. Native NC Gram remains an independent gate.
Normalize by max(||Fa||F,1). Phase/unitary gauge covariance requires transforming
F together with the orbitals; arbitrary mixing of unequally occupied columns
while leaving F diagonal unchanged alters gamma and is NOT a harmless gauge.

For any bounded one-body O, |tr(O delta gamma)| <= ||O||F||delta gamma||F,
or <=||O||op sqrt(rank(delta gamma))||delta gamma||F. With two48-column states,
rank(delta gamma)<=96. The pilot density tolerance therefore has a concrete
one-body meaning. It does NOT by itself bound an unbounded Hamiltonian, HSE
nonlinear feedback, or convergence to a physical ground state. Energy, charge,
local potential, eigenvalue and ef gates remain independent.

## CALCULATED: actual retained all-k Fermi/occupation audit

All6 rank/k packets per member per step are hashed, checked for exactly replicated
all-k et/wg, actual basis correspondence and retained48-band extent. QE's
UNEDITED efermig/sumkg/gweights/wgauss/w0gauss/w1gauss source is compiled with
explicit serial ONE-POOL reduction identities. This is a source-level replay,
not a rerun of MPI/QE/SCF. The actual experiment had one pool: no reduction of
partitioned k points is being simulated. Replayed mu is computed from et alone,
independent of retained wg; all weighted occupations reconstruct bitwise.
A direct native high-precision ef packet did not exist in the old experiment;
replay is not relabelled a nonexistent native observation.

First sampled differences ALREADY EXIST at outer1: max eigen delta2.93099e−14 Ry
at band2/k3, mu delta5.99520e−15 Ry, occupation delta5.89040e−12 at band38/k1.
Outer2: eigen4.24105e−13 Ry (band5/k3), mu1.93068e−13 Ry.
Outer3: eigen1.36202e−12 Ry (band36/k1), mu1.51212e−13 Ry.
Outer4: eigen1.919420178353448e−11 Ry (band36/k1), mu2.984279490192421e−13 Ry;
occupation1.4692691729933927e−8; bandwise MVT upper1.470077639241613e−8.
All-k weighted charge36 within1.42109e−14 electrons; no extra spin factor in
this noncollinear spinor convention. Only bands35–38 at k1 are substantially
partial. Do NOT assert their physical irreps solely from band indices.

Their pair splittings grow IN BOTH members: control35/36 from1.29478e−10 Ry
at step1 to6.71224e−6 at step4;37/38 from3.52212e−10 to1.02258e−5 Ry.
Individual nearly degenerate orbital labels need not be stable; weighted gamma
is the operationally relevant independent comparison. Positive local aggregate
charge response is about368.45 electrons/Ry at step1 and361.96 at step4.
Independent120-digit Decimal evaluation differs from captured unweighted f by
at most1.11023e−16 at these actual input points. The analytic erf series has
alternating remainder<1e−75 once terms decrease; |y|>=12 uses its explicit
Gaussian tail bound, and bounded120-digit arithmetic is far below the stated
binary64 allowance. This is a pointwise numerical qualification, not a universal
libm certification or material result.

## HYPOTHESIS / OPEN, kept separate

Cold-smearing conditioning fully accounts for the observed occupation mismatch
GIVEN the measured/replayed eigenvalue and mu differences. It does not explain
why the eigenvalue/orbital differences first arose, prove lossless whole-SCF
iteration arithmetic, prove symmetry breaking, or prove SCF contraction. Initial
rhoR/vrs reconstruction roundoff and iterative amplification are possible causes,
not isolated causes. Four completed streamed states cannot determine later SCF
convergence or qualified restart. Historical step4 FAIL remains FAIL.
