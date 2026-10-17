# Eight-atom HSE, 152 bands / eight transfers: execution NO-GO under 12 GiB

2026-10-17; clean baseline **305327988ae72196c07eaf32856809c65136a820**.
One bounded **read-only** assessment is complete. No QE/MPI/postprocessor,
material action, build, source edit, service, retry or paid resource was used.
The PBE diagnostic stays closed. No new owner, launcher or streaming design.

**Verdict:** stock/model compatibility is **YES under the stated centered
k2/q2 assumptions**, but **execution admission is NO-GO**. A complete resident
peak below 12 GiB has not been established. This is an evidence limitation,
not a proof that the candidate must exceed the cap. The stop boundary is the
unqualified peak for this exact profile, not a plan to tolerate a cgroup OOM.

## 1. Decoupled meshes are real; eight transfers are not always eight sources

The [QE7.5 manual](https://www.quantum-espresso.org/Doc/INPUT_PW.html#nqx1)
allows a smaller exchange mesh than the electronic mesh. The operative
[exx_base.f90](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/exx_base.f90#L160-L487)
distinguishes **nqs**, transfers per electronic representative, from **nkqs**,
the distinct stored union of its translated k+q fibers. It generates the
available star using actual crystal rotations and, for the specified
nonmagnetic SOC flags, time reversal. All required translations must exist
in that star. Invalid requested meshes may be changed automatically.

Defaults are input nqx=0, resolved to the electronic grid dimensions. There
is also an explicit **nkstot==nspin_lsda** override: a single irreducible
noncollinear point forces q1. This includes the fully shifted conventional
k2 grid, not only a Gamma-only input. The first downward fallback from an
incompatible equal-axis q2 request is q1; the source's conditional warning
need not print on that first adjustment. Always inspect the final native
q-grid and source list, not just input or absence of a warning.

**PROVEN UNDER STATED GEOMETRY/GROUP/GRID ASSUMPTIONS; independently
CALCULATED by exact rational replay:**

| Conventional electronic mesh | Requested / effective q mesh | Irreducible k | Stored nkqs | Nominal 152-band buffer |
|---|---|---:|---:|---:|
| centered 2³ |2³ /2³|4|8|8.405 GB|
| all-axis half-shifted 2³ |2³ /**1³**|1|1|1.051 GB|
| centered 3³ |2³ /**1³**|4|4|4.202 GB|
| centered 4³ |2³ /2³|10|**56**|**58.835 GB**|
| all-axis half-shifted 4³ |2³ /2³|4|32|33.620 GB|
| centered 4³ |4³ /4³|10|64|67.240 GB|

The shifted cases omit Gamma. Counts assume the actual frozen ideal motif
and ordinary nonmagnetic symmetry reduction, one pool and two local ranks.
They are predictions from exact stock source, **not newly executed native
lists**. Any future run would still have to confirm actual operations,
effective q and k+q maps. Disabling symmetry or changing geometry changes
these counts. For example a four-operation D2 subgroup with TR gives 27
electronic representatives and 64 sources for centered k4/q2, increasing
both source storage and ACE/wave caches. SOC/noncollinear ACE itself is
supported by the stock complex-spinor path; it does not reduce these arrays
to scalar Gamma-only storage.

Independent validation transforms the Td rotations into primitive reciprocal
coordinates and reproduces **all eight k4 representatives, weights and 64
sources of the accepted native primitive run**. A separate q2 parity-coset
count gives 7×8=56 for conventional k4/q2. See [audit](audit.json) and
[verification](verification.json); no native code was invoked.

### Physical folding and the chemical symmetry correction

The recorded folding matrix has determinant four. Primitive 4³ folds to
**16 conventional fibers**, uniformly weighted 1/16: the union of centered
conventional 2³ and its (.25,.25,.25) shifted coset. Centered k2 samples only
the first half, with Gamma weight 1/8 instead of 1/16. Shifted k2 samples
the other half and has no Gamma. Centered k4 contains all 16 but includes 48
additional fibers and different weights. Exact discrete-rule total-variation
distances from the folded rule are respectively .5, .5 and .75. These are
**quadrature mismatches, not energy-error estimates**. Without a bound on the
actual integrand/couplings, errors can have either sign and no meV bound.

Even an explicit, correctly weighted folded 16-point electronic list needs
**16 stored source fibers** with q2 and nominal 16.810 GB at 152 bands.
Its eight transfers connect only the same half-grid coset; they do not
reproduce the full folded 16-transfer exchange rule. Exact electronic
folding alone therefore does not make the HSE operator equivalent. No
supported arbitrary 16-transfer input or matching material execution is claimed.

**The frozen one-Cd motif does not have a lower point group than the host.**
Cd at (0,0,0), Hg at the three face-center cation sites and the four original
Te sites retain all **24 Td rotations** about that origin. They lose three
of the four fcc primitive translations of the pure conventional cell. Exact
species-preserving site permutations and both retained native XML files
independently confirm this. Lower *translation* symmetry must not be confused
with lower *point* symmetry. This does not certify the SCF density: old states
remain nonstationary/rejected. A Gamma8 quartet is permitted if the new state
really preserves that symmetry, not forced by averaging or a geometry flag.
Other distorted/configurational motifs require their actual subgroups.

## 2. 152 bands: source-legal, with new coverage and initialization questions

Actual SG15 headers are fully relativistic NC, Hg=20, Cd=20, Te=16 valence
electrons; both cells have **144 electrons**. [setup.f90](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/setup.f90#L371-L403)
requires at least 144 noncollinear spinors. Thus 152 is legal. It means eight
states above the electron count, **not eight proven empty bands**: fractional
FD occupations can make more than 144 states occupied. The runtime metallic
default would be 172 here; old 176 was explicit. Default handling is traced
through read_namelists, not inferred from an overridden module initializer.

Stock [EXX/ACE](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/exx.f90#L480-L552)
normally projects onto nbnd in SCF and allocates the real-space source
buffer over **every band**, despite separately finding occupied support.
Changing 176→152 reduces this payload by 13.64%, but also changes the ACE
span and off-span approximation. No symmetry, accuracy or convergence
guarantee follows from the number 152 or the earlier unrelated 152-vector
symmetry constructor.

**Retained numerical evidence, not a prospective certificate:** after one
old inner relaxation, band152 lay 2.290 eV above mu in HgTe and 2.846 eV in
the Cd cell; stored bands153–176 had zero displayed/native occupations.
The rejected 79-build host's dominant Gamma6-like bands141–142 and Gamma8-like
bands143–146 are below 152. Nevertheless its original six physical probes
have **4.06e-5 to1.60e-4 probability in bands153–176**. Therefore 152 contains
the dominant labels in that old state but not its complete unoccupied
projected spectral support. These different, nonstationary q1 states cannot
bound coverage or errors of a new stationary q2 calculation.

Conditional on all omitted ordered eigenvalues being at least mu+delta,
FD gives f_tail≤1/(1+exp(delta/sigma)). At sigma=.001 Ry, an operator-tail
target 1e-8 needs delta≥.250626 eV; bounding charge from only 24 omitted
states by1e-8e needs delta≥.293866 eV. A whole finite-basis tail requires the
larger actual omitted dimension. Neither uncomputed eigenvalue ordering,
physical-projector energy moments nor a full-H residual is certified here.
Small occupation alone does not certify an unoccupied observable or ACE action.

There is an additional **stock initialization change**. Both native cells
have natomwfc=152. In [wfcinit.f90](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/wfcinit.f90#L286-L345),
atomic+random with nbnd=152 perturbs the complete atomic starting set;
with nbnd=176 it instead supplements 152 atomic columns with extra random
columns. This must be declared in a new protocol; it cannot be described as
the same initial wavefunction or an isolated exchange-mesh comparison.

## 3. Resident memory: a substantial source subtotal, no complete safe peak

For the retained 60³ EXX descriptor, two ranks, one pool/EXX band group,
no GPU, 152 spinors and **nkqs=8**, exact complex128 payload arithmetic is:

    exxbuff = 60³ ×2 ×152 ×8 ×16 = 8,404,992,000 bytes.

This is decimal 8.405 GB, versus **12 GiB=12,884,901,888 bytes**. It is not
the total resident footprint. The [vexx_k CPU path](https://github.com/QEF/q-e/blob/qe-7.5/PW/src/exx.f90#L1798-L1825)
simultaneously allocates two full spinor real-space batches. Together these
add **2,101,248,000 bytes**, giving **10.506 GB before other storage**.

| Named payload in nominal ACE-build phase | Aggregate model bytes |
|---|---:|
| Source buffer plus two spinor batches |10,506,240,000|
| rhoc/vc, native jblock=7 |48,384,000|
| xi for four irreducible fibers |210,650,112|
| evc, evc_exx, direct-action result |3×52,662,528|
| Four in-memory wave records |210,650,112|
| Replicated 24-operation rotation map |41,472,000|
| Coulomb cache grid-extent estimate/ceiling |55,296,000|
| **Extended nominal payload model** |**11,230,679,808**|
| Difference from 12 GiB |**1,654,222,080**|

The last two rows are **not a peak interval or a reserved margin**. Plane-wave
payloads use the old Gamma count10827; actual k2 rank maxima/padding and cache
residency remain to be established. G/kinetic maps, beta/SOC arrays, potentials,
mixing history, FFT plans/work, MPI/HDF5/BLAS workspace, allocator high-water
behavior, loaded libraries, temporary save copies and cgroup-charged file
cache are not all bounded by this model. No source-complete upper fits the
remaining1.654GB. The credible overall peak is **UNKNOWN**.

The phases are distinguished rather than incorrectly summed: MPI global FFT
copies in exxinit are released before the ACE batches; NC Davidson has no
US/PAW overlap spsi and uses the effective default workspace factor2. Its
psi/hpsi payload is about210.65MB plus replicated small matrices, but it is
not simultaneous with the direct EXX-build batches when stock ACE is active.
Persistent source/xi/wave storage remains during inner solves. The actual
stock q1/176 peak4.225GB and diagnostic4.549GB are evidence for **different
workloads**, not a constant overhead that can be subtracted and reused.
Memory buffers allocate individual written records; their initial index
capacity1024 is not 1024 allocated wavefunctions.

This assessment does not certify disk/time/output bounds for a launch.
It does not treat the cgroup kill mechanism as permission to plan an OOM.
No independently qualified HPC allocation is present in the accepted evidence.
Changing pool/layout/IO or using another package would need its own concrete
evidence; no custom code or speculative alternative acquisition is recommended.

## 4. One best candidate and the exact stop boundary

The best **unadmitted** narrow candidate is a fresh matched host then Cd-at-
origin pair: conventional8atom/a6.46Å, identical frozen axes/sites/FR-NC SG15,
**centered electronic2³, q2³, nbnd152**, HSE(.25,.106 Bohr^-1),50/200/Fock200Ry,
FD.001Ry, noncolin/SOC, stock ACE, Davidson/full_acc/default workspace2,
mixing.3,adaptive_thr=false,conv_thr1e-9Ry and independently fresh atomic+
random initialization as actually implemented. This is a **new coarse ordered
model**, not the primitive k4 Hamiltonian. No runnable launch deck is emitted.

**Missing decision-changing resource evidence:** a trustworthy complete
resident-memory envelope for precisely that two-rank profile, including
native descriptor/rank extents and backend/cache high water. Current source
and archives do not establish it below12GiB. No numerical new cap or arbitrary
HPC size is invented. Stop this finite study here; no resource probe is
authorized by this assessment.

Even with resource admission, host release would require genuine outer HSE
convergence, FD charge/entropy, full occupied D and actual spatial/Theta
qualification at the original1e-8 threshold. The latest primitive host still
fails that stringent density threshold and cannot be imported as a same-cell
passing control. Cd needs its own stationary state, group/physical-sector
association and matrix/spectral test if symmetry is lower or labels mix.
No host/Cd sign is inferred from sorted indices or unaligned potential zeros.

If retaining the prior2meV **numerical** contrast goal, an independently
sufficient condition for fixed orthogonal projectors W=P6/2−P8/4 is
2(epsilon_host+epsilon_Cd)+epsilon_frame≤2meV, because ||W||1=2.
The epsilons must bound the relevant common-frame operator/observable errors;
dexx alone supplies none. This conditional inequality is not a relaxed density
gate, an achieved error bar or a functional/alloy bound. An ordered mass/sign
or bracket additionally requires justified spectral-sector stability and
complement coupling; physical random-alloy x_c needs composition statistics
and further microscopic information. No empirical fitting or novelty claim.

## Verification and preservation

[audit.py](audit.py) reads the exact local **qe-7.5 tag**, whose pristine EXX
archive is byte-identical, and records official source URLs/hashes in
[audit.json](audit.json). The dirty working EXX source is explicitly excluded.
[verify.py](verify.py) uses a different fcc rotation representation to reproduce
the real primitive native grid, independent q2 cosets, actual PP/electron data,
allocation arithmetic and relevant source branches. All72focused checks pass.

Rerun with the existing DFT/.venv Python, PYTHONDONTWRITEBYTECODE=1 and
OPENBLAS_NUM_THREADS=1, invoking audit.py then verify.py from MCT. They write
only this scoped research directory. All822protected pins,76historical files,
stock ELF/backends,DFTdirty bytes and previous host acceptances/refusals are
unchanged. No protected source/saves, main, credentials or other session changed.
**STOP: no new scientific execution, infrastructure phase or automatic retry.**
