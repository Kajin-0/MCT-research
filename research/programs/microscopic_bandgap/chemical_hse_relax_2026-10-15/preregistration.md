# Prospective one-relaxation / second-ACE matched HSE experiment

Baseline clean pushed bce98cc. New user authorization: one fresh host, then one
Cd member only after all host gates pass. No retries, old state/restart reuse,
full-SCF convergence target, other composition or native campaign.

Frozen physics: 8 atoms Hg4Te4/CdHg3Te4 (ordered x=.25), a=6.46 Å, same origin,
positions/spin axes/SG15 FR NC, 176 spinor bands/144 electrons, HSE fraction .25,
screen .106 Bohr^-1, 50/200/Fock200 Ry, FD sigma .001 Ry, unshifted Gamma/q1,
native Td, Davidson/full accuracy, mixing .3, conv_thr1e-9, adaptive_thr=false,
maximum100 inner steps, atomic/random fresh initial state. The sole input change
from first-ACE physics is exx_maxstep=2, a diagnostic outer budget. Native
max_seconds500 and owned600s are retained, with no prolongation.

Three private QE objects add observations and a deterministic stop. Cycle1 is
the preliminary semilocal density/first ACE; it proceeds without a forced stop.
Cycle2 is exactly one converged hybrid inner solve using the first ACE followed
by second EXX/ACE reconstruction. Stop after native energy/Fock/dexx calculation,
before another outer iteration or native budget branch that could label merely
exhausted iterations converged. Native punch saves false HSE convergence and
publishes both rank completion packets. This is not qualified restart state.

Capture cycle-indexed Phi/direct/Gram/xi/ACE/reference direct action, local action,
rhoR/rhoG/G/FFT/et/wg, summary energy/scf_error/inner_steps and native fock0/1/2,
dexx plus raw signed dexx. All native exchange, compression, Fermi, local XC,
mixing and diagonalization arithmetic is unchanged. No duplicated exxbuff store.
The same original six physical Gamma references embed exactly by actual G labels
from7809 to10827 vectors. No norm truncation or renormalization. Both cycle direct
reference actions are used; ACE off-span reference action is never substituted.

Primary observable: for member m, A1_m is the fixed-reference Gamma6-Gamma8
trace of local1-local0 plus direct Fock1. R_m is the trace of local(c2)-local(c1)
plus direct Fock2-Fock1. Report chemical A1_Cd-A1_host, relaxation R_Cd-R_host,
and their sum (HSE operator at rho1 relative to PBE at rho0), separately. It is
not HSE-minus-PBE at the relaxed density, a spectral centroid, or converged gap.
Final orbitals/eigenvalues solve the first frozen ACE with relaxed local density;
they have not been iterated against the rebuilt second Fock operator.

Scientific gates unchanged from first ACE on each source:176/144/Gamma/24Td/
HSE/settings, finite complete packets and rank PID/physical G-frame, SCF error
<=1e-9Ry and actual captured weighted charge<=1e-8e, direct/ACE action and Gram
relative<=1e-8, native contraction disagreement<=1e-8*max(1,abs energy)Ry,
normalization<=1e-8, negative exchange Hermiticity/sign allowance1e-8 relative.
The final source wave must read back bitwise from final HDF5; cycle1 source is
retained in actual packets/Gram, not falsely claimed separately HDF5-verified.
Within each rebuild rhoR/rhoG/G/probe bytes must remain identical. Intercycle
density/orbital differences are physics and are measured, not byte-rejected.
Final XML numeric export tolerance2e-14 Ry, FD occupations<=1e-9.

Cycle1 FD consistency is independently checked against the monotone charge root
of all176 captured eigenvalues; its native chemical potential is not separately
captured and reconstructed value must be labelled accordingly. Cycle2 native
Fermi/XML is used directly. Signed dexx=fock1-.5*(fock0+fock2) must be >= minus
1e-8*max(1,abs fock0,abs fock2) Ry; capture negative raw value even if native
prints abs. Native raw values and first/second contractions must agree. Numerical
consistency does not certify unknown physical/operator/eigenpair errors.

Admission: fresh private root h8r_20261015/p1, distinct fresh jobs/nonces, both
absolute Unix addresses <=107 UTF8 bytes (108 with NUL) and actual disposable
bind/identity-safe removal BEFORE any service. Same typed live rank/kernel/ELF
owner, one family/two local ranks, 12GiB cgroup/swap0/tasks12/600s/member, host
MemAvailable>=4GiB/disk>=10GiB, sampled14GiB tracked pair output and1GiB/file.
Known lock/old ledger/protected DFT/source/PP/backend/hash gates all pass. This
is the accepted local-owned contract; original host-wide exclusion and private
network proof remain unpassed. Between-sample producer/external-writer risks
remain explicit. First failure ends scope without Cd/retry or threshold changes.

Earlier measured firstACE walls216/201s and kernel4.23GB are not full iteration
bounds. Two builds plus hybrid inner solve are controlled by hard caps and native
stop only. Timeout/incomplete update is a finite partial FAIL, not convergence.
Archive actual raw/provenance/residuals or exact failure; preserve all historical
failures, stock/dirty DFT/16atom352band, Calcura/sessions/supervisors/goal/main.
Only research commit/push; no empirical fitting, spending, new agents or sessions.
