# ONE native cutoff pair and a non-executing HSE assessment

2026-10-14; clean research parent31e872e. User authorizes ONE fresh sequential
matched host/Cd SCF pair at50/200Ry; no rerun of40Ry and no alternate sweep.

Keep Hg4Te4/CdHg3Te4 atx=.25, fixed cubic6.46Angstrom cell/origin/spin axes,
SG15FR NC potentials,176spinor bands/144electrons,PBE+SOC,FDsigma.001Ry,
unshifted2x2x2 Gamma-containing mesh and nativeTd symmetry. Same1e-9Ry SCF,
full-accuracy Davidson,beta.3,max100steps,atomic/random fresh starts and
max_seconds500. Only ecutwfc40→50Ry and ecutrho160→200Ry change. Native
weighted all-k charge<=1e-8electron,occupation reconstruction<=1e-9,expected
four stars/weights(1,3,3,1)/8,uniqueGamma,convergedSCF/JOBDONE,typed actual
two-rank leases,retained terminal manager/exit0 and empty cgroup must pass.
Cd only after host passes all gates; no native retry on failure or timeout.

Resource admission: existing40Ry K2 pair measured162.92/158.32s and kernel
memory .693/.690GB. Plane-wave/FFT continuum-volume scaling(50/40)^1.5=1.398
suggests~228/221s; an additional2x timing allowance~455/443s fits500s softstop
and600s hard cap. This is an estimate, not a convergence guarantee. Conservative
4x measured memory<2.8GB and expected new retained waves<1GB/pair fit12GiB
kernel/familyRSS. Actual ext4/quota/disk and available physical RAM are checked
before launch. Same12GiB/swap0/tasks12/600s/member,one local family,4GiB hostRAM
and10GiB disk floors,real64MiB escrow/member,sampled14GiB aggregate known-path
inode/block/FD output policy and1GiB per-file cap. Final aggregate is explicitly
checked too. No continuous/adversarial disk guarantee or host-wide MPI absence.
No stock, dirtyDFT, originalHSE16/352, old datasets/failures, other sessions,
supervisors or historicalgoal modifications.

## Cross-cutoff physical frame (freeze before new spectra)

PRIMARY projectors remain original qualified40Ry Gamma-only host Γ6/Γ8 frames,
as in31e872e. NC plane waves are labelled by Cartesian reciprocal momentum and
spin: match cell/reciprocal matrices/Bloch k/origin/spin axes, then embed each
old coefficient into the50Ry slot for the SAME Miller vector. Set new-only
coefficients to zero. Verify unique labels, ALL source vectors present, identical
physical reciprocal axes and k,old/new Gram metrics,zero-fill norm preservation
and exact group-intertwining on24 Td operations. Never use array-index overlap,
truncate a50Ry eigenstate without counting its norm,or renormalize missing
probability. Different native FFT ordering is allowed; different physical cell/
spin conventions or missing source vectors refuse the comparison.

Evaluate the embedded frame against both actual50Ry Gamma spectra. Compare
W=1,1.5,2,2.5,3eV with40Ry K2,own-Fermi AND own dominant projectedΓ8-quartet
reference recipes,using the identical trace-functional definition and massfloor
.05. Old projector envelope carries through the isometry; arithmetic budgets
use actual higher PW component count. Omitted-band spectral probability and
Gaussian tail bounds retain the joint denominator. No ordinary unbounded
first-moment/material/eigenpair error bound is inferred. Report measured
DeltaOmega_50-DeltaOmega_40 and conservative conditional difference intervals.

Independently identify native50Ry host sectors by primitive-translation/Td
characters, record principal angles to embedded originals, their high-G norm
outside40Ry and separately labelled new50Ry host-frame responses. This exposes
frame/cutoff effects rather than silently changing the primary observable.
No dependence on empirical HgCdTe alloy gaps.

Decision: numerical convergence/ownership/frame refusal stops native work. If
absolute W2 cutoff response change>10meV, call this input poorly qualified for
the few-meV target and stop at that result; no alternate cutoff. Smaller changes
are measured sensitivity only, not infinite-cutoff or BZ convergence. All
functional/cell/ionic/many-body errors remain OPEN; no physical x_c.

## Next HSE question — analytical only, no launch authority

After the pair or its first refusal, inspect pinned native QE7.5 EXX/ACE
allocations,existing small-HSE timings and measured states. Assess smaller
8atom/176band x=.25 host/Cd HSE+SOC options with explicit k/q/fock-cutoff errors,
RAM/disk and time uncertainty. Avoid original16atom352band domain and private
48band-only root. Standard stockFD occupations are already qualified for this
176band NC domain; no generalized solver/execution engineering is issued.
Recommend one best next physics design/cost or precise insufficient admission
input. HSE is NOT authorized to run by this assessment; no dry/native HSE,
firstACE,NSCF,queues or broad jobs without a separately admitted scope.
