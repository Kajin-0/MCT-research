# ONE matched HSE first-ACE diagnostic pair — freeze before native launch

Parent40d2b9e; existing research branch/session, explicit new user authorization.
One fresh sequential8atom Hg4Te4 then CdHg3Te4 pilot; no retries,fullHSESCF,
other composition,original16atom352band or existing data/source modifications.

HSE+SOC,sameSG15FR NC,176spinor bands144e,fixed6.46Angstrom cell/origin/
positions/global spin axes,50/200Ry,Fock200Ry,FDsigma.001Ry,automaticunshifted
1x1x1 Gamma (complex SOC,not the real gamma-only algorithm),q1x1x1,HSEfraction
.25,screening.106Bohr^-1,ACE=true,nativeTd. SameDavidsonfullaccuracy,beta.3,
conv_thr1e-9,max100innersteps,fresh atomic/random source. Setadaptive_thr=false
so preliminary semilocal source must meet1e-9; it is not a relaxed HSE initial
threshold. This is separately labelled coarseGamma/q sampling, not k3 physics.

Build privately from pinned pristine QE7.5 exx/electrons/run_pwscf and installed
original archive/backends. Add only diagnostic calls and a first-ACE completion
branch; retain existing exchange/ACE arithmetic, native occupation solver and
all source/PP/stock files. No legacy48-band root,streaming or owner-framework
changes. Capture all176 sourcePhi,directW,Gram,compressedXi,ACE-on-Phi,actual
rank-specific G/maps/FFT/extents,et/wg and half/full Fock energy. Additional
directFock on six ORIGINAL physical Gamma host reference vectors avoids ACE's
off-subspace assumption. Optional local-potential action before/after first
activation uses nativevloc_psi_nc_acc on the same probes; capture rhoR/rhoG
both times and require byte equality. Kinetic and NC nonlocalPP terms do not
change for this fixed density/cell; report the projected fixed-source operator
change separately from a Gaussian spectral response.

Read original40Ry fixedGamma6/8 coefficient/Miller/B-matrix file, map exact
physical(G+k)B to each current rank at50Ry, zeros on new-only vectors. Require
every source vector globally exactlyonce,matching reciprocal axes,k0,native
Gram<=1e-8,no source norm lost,no missing-mass renormalization. No naive
native-index or truncated176-state approximation to the reference action.

Stop ONLY after complete firstACE, nativeFock energy/local-potential refresh,
all-rank packets and post-punch publication. Saveconv_elec=false explicitly;
diagnostic exit0/JOBDONE means successful planned stop,NOT HSE convergence.
No second hybrid orbital iteration. Native source eigenvalues/waves are the
preliminary semilocal state; output functional label alone does not make them
HSE quasiparticle eigenvalues. No qualified restart or full gap/x_c claim.

Scientific gates: native176/144/Gamma/24Td/HSE.25/.106/cutoffs,preliminary
source convergence1e-9Ry and all-kFD charge<=1e-8e,occupations<=1e-9,
complete finite packets/actual rankPID/physical G-space/cell/source readback.
Independently reconstruct Gram and weighted unhalved Fock contraction,require
direct-versus-ACE action/Gram relative errors<=1e-8 and energy disagreement
<=1e-8*max(1,abs(energy))Ry. Negative-exchange Hermitian/sign defects use1e-8
relative numerical allowance; source normalization and actual recorded maps
must pass. These numerical gates are prospective consistency checks,not
material error bars. Source/rho readback must match recorded bytes; refuse
incomplete captures,unexpected source domain or exchange-state mutation.

Same tested local-owned policy:oneMPI family,two local ranks,kernel12GiB/
swap0/tasks12/600s each,host4GiB RAM/disk10GiB floors,ext4/quota/fresh escrow,
sampled14GiB known-path pair output and1GiB perfile. Independent preflight
source/ELF/backends/PP/input locks and all-rank typed executable leases required.
Known oldledger staysfinished/empty/byteexact. Burst/external-writer between-
sample risk remains explicit; no host-wide foreignMPI or private-network proof.
Host must pass science,owner,resources,source/state/physical-frame gates and
empty-group cleanup before Cd. Firstfailure=>stop; no native retry/downgrade.

The2.23GB subtotal and320–365s/pair are heuristics,NOT bounds. Source buffer/
packet formulas are checked beforelaunch; enforced kernel/time/output ceilings
control the unknown overhead. No large allocation/dryHSE or extra native test.
If admission fails,record concrete missinginput; do not launch. Measure actual
first-ACE timing/resources and infer only labelled cost possibilities for full
SCF. Any projected exchange/local chemicaldelta is frozen-source/operator data,
not a convergedHSE centroid/signed gap. Never add it directly to k3GaussianW2.

Preserve stock,dirtyDFT,oldFAILs,Calcura/other sessions/supervisors/goal. No
empiricalgapfit,hardwarepurchase,newsession or DFT/main commit. Focused source/
small checks then actualpilot ifgatespass; archive raw evidence,update R07,
commit/push only the existingresearchbranch with working scopedKajinSSH.
