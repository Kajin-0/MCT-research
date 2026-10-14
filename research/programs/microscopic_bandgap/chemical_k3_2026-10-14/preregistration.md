# ONE matched k3 PBE+SOC chemistry test — frozen before launch

2026-10-14; clean parent3fe5ef2, existing research branch/session. Authorize one
fresh stock-QE two-rank sequential Hg4Te4 then CdHg3Te4 SCF pair only. No retry,
NSCF, HSE, altered physical input, other composition or additional mesh job.

Relative to the accepted k2 pair, ONLY automatic k points change2→3 in each
axis (unshifted Gamma-containing3x3x3), plus unique private output paths.
Keep cubic6.46Angstrom cell/origin/ionic positions/global spin axes, identical
SG15FR NC PPs,PBE+SOC,nosym=false,176spinor bands144electrons,50/200Ry,
FDsigma.001Ry,conv_thr1e-9,mixingbeta.3,full-accuracy Davidson,max100SCFsteps,
fresh atomic/atomic+random starts,max_seconds500. No old aborted density/waves.

Exact Td plus nonmagnetic time-reversal orbits of{0,+1/3,-1/3}^3 have sizes
1,6,12,8 by number of nonzero components. Both species arrangements must
preserve24Td operations about the same origin. Native input/symmetry flags,
24rotation matrices and native four representative weights (1,6,12,8)/27,
unique Gamma and its actual complex HDF capture are mandatory. If native
symmetry or mesh differs, REFUSE; do not reinterpret more points as success.
Independently reconstruct all-k FD charge<=1e-8e,occupationerror<=1e-9,
SCF error<=1e-9Ry,convergence=true/JOBDONE,176bands144e,actual50/200Ry.
Cd only after host science,retained manager exit0/kernel-rank exits/empty group
and physical Gamma frame/source qualification pass.

Reuse the tested local owned cgroup/typed-live-lease policy without global
changes:12GiB RAM including shared-RSS overcount guard,swap0,tasks12,
600s/member,oneMPI family,hostRAM4GiB/disk10GiB floors,ext4/quota admission,
64MiB escrow/member,1GiB per-file and sampled14GiB retained pair aggregate.
Retained closed generations/inodes/blocks/metadata and owned FD paths count;
unknown paths/identity or any guard failure aborts, no retry. Between-sample
producer/external-writer risk remains explicit; this is not a hard quota or
foreign-MPI absence/network-isolation proof. Known old ledger/lock and actual
resource margins are checked before launch and continually within the family.

The native k2 pair measured226.27/212.73s and kernel<.954GB. Four k3 symmetry
representatives keep the same diagonalization count; actual per-k PW counts,
occupancy and SCF histories can change. 2x prior wall=453/426s is a conservative
heuristic under500s soft/600s hard stop, NOT a convergence guarantee. 4x prior
kernel<3.82GB and wave save count4/member fit the12GiB/14GiB ceilings with
independent physical admission. Stop on an unsafe admission or native timeout.

## Observable and immutable comparison policy

PRIMARY fixed projectors are the original40Ry Gamma-only physical hostGamma6
(rank2) andGamma8(rank4), exactly as in3fe5ef2. Map physical reciprocal(G+k)B
and spin coefficients into native50Ry Gamma slots; verify matching cell,origin,
axes,k,unique labels,all source labels present,zero-fill isometry/Gram and all24
Td intertwining. No naive array-index overlap,truncation,missing-mass renormalization
or replacement of the primary host frame. Pin original waves,frames/spectra,
analysis code and previous50Ry k2 results before new data are acquired.

For W=1,1.5,2,2.5,3eV,phi=exp[-(E-reference)^2/(2W^2)],normalize trace weights
by physical frame rank,not computed probability. c=sum(w*t*phi)/sum(w*phi),
Omega=c6-c8,DeltaOmega=OmegaCd-OmegaHost. Primary reference is ownFermi;
secondary is each member's dominant projectedGamma8 quartet mean. Both recipes
are evaluated separately even if new Fermi no longer equals that quartet.
Primary W2k2baseline=+.3933370319603723eV. Report measured k3-minus-k2 changes,
conservative summed conditional response radii and finite-spectrum masses/tails.

Use unchanged massfloor.05 and bound
(r+2epsilon+rho)*(W/sqrt(e)+abs(c))/(M-2epsilon-rho),positive joint denominator.
Carry old projector epsilon through the physical isometry; update arithmetic
component count from actual PW. Unknown eigenpair/material/operator errors
remain excluded. Gaussian widths/reference choices are probe sensitivity,
not a BZ or physical uncertainty bar. Independently identify new hostGamma6/8
by primitive translations and complexTd characters; separately measure newhost
frame effect and k2-to-k3 principal angles without changing the primary result.

GO requires native/source/frame/resource/terminal gates and computable bounded
observables. If |W2primary grid change|>10meV, mark sampling poorly qualified
for the few-meV goal; do not launch a further grid. Otherwise record measured
sensitivity only. No BZ convergence from two meshes,convergedHSE,bulk random
alloy signed-gap,x_c,originalHSE16/352 downgrade or repaired historicFAIL.

After the measured pair/refusal, recommend ONLY a future smallest matched
8atom HSE Gamma/q1 first-ACE timing/resource pilot OR composition test, grounded
in actual cost/info. No HSE/composition launch or queue is authorized here.
Preserve stock QE,dirtyDFT,priorwaves/data/failures,Calcura/other sessions/
supervisors/historicalgoal. Commit/push validated science on the existingbranch.
