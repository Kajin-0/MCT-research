# Implemented source, readback and unreleased execution boundary

This supplements the single decision; it is NOT launch authority.

## Source and frozen ABI

New main and gate are copied into a unique ignored MCT build directory.
`build.py` uses the pinned old compiler/include/link recipe, replacing the
old main/lease/private-PW archive with ONLY the two new objects plus STOCK
PW archive. Fortran uses CPU MPI/HDF5/ELPA/ScaLAPACK flags, fcheck=all,
-fno-fast-math, no LTO. Compile/link had no errors; no repair/rebuild cycle.
Link map/disassembly, original archive and selected unchanged members are
pinned. Builds use2GiB address-space/60s CPU/512MiB per-file limits. Never run
`r07_density_only_v1.UNEXECUTED`; removing its hard C gate is a separately
reviewed source change, not a CLI/ENV permission.

`read_xml_file` sets nks=nkstot. With actual nproc1/one pool/group, no k-point
redistribution is required; native init_igk executes ONCE. `post_xml_init`
rebuilds saved PBE potentials and bare NC-SOC coefficients; set_vrs is added
explicitly. The driver checks declared PBE/NC/FR/noNLCC, nonmagnetic SOC,
Gamma complex,50/200Ry, sigma.001Ry,288e,352 metadata, nat16,nkb712,80³ and
actual24/4 group count. It never overwrites nbnd or occupations. Extra field/
correction/plugin globals and linked preprocessor choices must still be
reviewed against exact accepted XML before release; compilation is not an
independent state-equivalence test. No generalization to HSE/PAW/NLCC.

Native canonical query (little-endian installed x86_64 ABI; Fortran order):
16 int64 header, B(3,3), cell(3,3), tau(3,16), species16int64,
Gpw(3,N)int64, Phi(2N,12)complex128, Grho(3,Ng)int64,rhoG(Ng)complex128.
Header magic71601001/version1/N21595/Ng173631/probes12/XMLbands352/e288/
case0unshared or1sharing; remaining fields reserved. Expected15,756,784 B.
Future staging must construct this from independently hashed accepted saves
and EXACT original six F plus six explicit ThetaF, not the old query binary.
No material query or staged save has been created this phase.

Every density coefficient is compared BYTE-EXACTLY by integer G label to the
accepted canonical rho before trusting the actions; no rank-index assumption
or silent repair. All query plane waves are transported by physical G using
B=bg*tpiba, cell=at*alat and tau*alat. Check source zero-G normalization
Omega*rhoG0=288 and all magnetization arrays zero. The native query still
reconstructs the PBE potential through QE; this is NOT a new SCF iteration.

Output header20int64 magic71601002/version1/world1/rank0/PID/npwx/n/Ng/
nrho/nsmooth/352/12/4/712/16/case/nsym/three reserved zeros; FFT14x2int64,
B3x3,k3,scalars8, Gpw and Grho, then Phi,Tphi,Vlocalphi,VNL,SOCphi,Hphi,
rhoG4,rhoR4,vrs4. Header/array extents and finite values are checked in the
new reader; no reuse of old two-rank reader/packets. Expected90,028,752 B
if the singleton descriptor has no padding (NOT measured); new packet count
comes from source, not the old90,028,704 B value. Driver writes an externally
precreated zero-length exact output inode, checked WRITE/FLUSH/CLOSE and
regular-file fsync; production owner must enforce the precreation/inode pins
and all error paths. No authenticated material begin/final exists in this
unreleased build. HDF5 is explicitly finalized once for pinned __HDF5 vs
_HDF5 macro discrepancy; no PW stop_run/punch/close_files side effects.

## Actual confinement test design versus evidence

`runtime_probe.c` and `qualify_runtime.py` are **NON_SCIENCE only**, separate
ELFs and fresh service/root. Fixed dummy data, regular bounded stdio,
close_range>=3, fresh file nonce after live pidfd/start/exe/cgroup checks,
no arbitrary command/QE target. No inherited socket is used as identity.
The planned rules handle all ABI5 write/create/remove/refer/truncate/IOCTL
rights, granting writes ONLY to a precreated dummy output file. Reads remain
unrestricted in this tiny test: a future material read allowlist is additional
work. Seccomp denies sockets (all families), process fork/exec and nonthread
clone, with clone3 ENOSYS fallback for threads. Kernel task/memory caps still
apply. This is a cooperative trusted-program policy, not proof against every
malicious syscall: comprehensive capability/IPC/seccomp review precedes any
stronger sandbox claim.

Negative code covers RO/foreign/TMPDIR files, /tmp and /dev/shm O_TMPFILE,
AF_INET/AF_UNIX and fork; it touches no protected originals. A disposable
preopened canary intentionally demonstrates Landlock's inherited writable-FD
exemption, then closes it and requires EBADF. This is not permission to keep
such FDs in production. Planned singleton is direct MPI_Init_thread(size1)/
finalize, no launcher; MPI helper/process/socket need fails closed. **All these
post-nonce tests were NOT EXECUTED because admission refused before nonce.**

Both service caps and regular stdio limit were configured; outside owner has
512MiB address-space,60CPU-s,1MiB file limit, bounded capture/records and
own-output sampling. Per-file limits do NOT constitute14GiB aggregate quota.
No material backend/HDF5/PMIx write envelope, hard disk quota, deleted-open
accounting or no-helper claim was qualified. Cgroup isolation does not prove
absence of foreign MPI, private network namespace, continuous host floors,
or immunity to between-sample bursts/external writers. Preserve these limits
and unknowns rather than advertising an adversarial continuous theorem.

## Separate numerical acquisition gates, not performed

1. Fix named pre-nonce diagnostics in a NEW version; actual confinement+
singleton positive/negative admission, read-only hash-checked independent
copies (no hardlinks/symlinks/wfc) and finite file/stdio/helper/owner/readback
bounds. Original DFT saves and stock binary never writable. Keep12GiB,
swap0,tasks12,600s,host4GiB/disk10GiB/output14GiB; complete actual native peak
and deadline remain unknown. Selected439.69MB payload is NOT an upper bound.
2. Independent same-rho trusted native-control and component tests: |G|²,
full local FFT convolution/PBE derivative/Hartree-G0/PP beta angular SOC,
rho transport, charge and source gauge. Old refused actions cannot be a
control. These controls add queries beyond24 and require separate scope.
3. Reader must bind exact F/G/rho/PP/XML/native state to frozen hashes,
measure HThetaF-ThetaHF<=1e-8 and Hermiticity/components/charge. Actual24/4
ionic and density/potential operations must be checked; metadata alone does
not prove full-H crystal covariance on an imperfectly closed six-space.
Extra rotated/eigenstate controls must be counted, never hidden in12/member.
4. Use S=F†F, Pi=F S^-1F†, sectors with their own exact Gram. Compute
Omega=Tr(Pi6 H)/2-Tr(Pi8 H)/4, B=(1-Pi)HF and their matched contrasts.
Independent scalar shifts cancel in Omega/B; full scalar matrix contrast
needs aligned numerical potential conventions, not own EF. `diagnostics`
and `theta_controls` are separate explicit reader checks, neither a release.
5. Achieve the previously chosen absolute2meV error ledger independently;
shared-code agreement/symmetry is insufficient. No352 spectral tail is needed
for HF in this finite basis, but QHQ/complement, functional/finite-cell/alloy
uncertainty remain missing. This measurement would test static arrangement
sensitivity and six-frame closure, NOT identify a unique local N2 or x_c.
