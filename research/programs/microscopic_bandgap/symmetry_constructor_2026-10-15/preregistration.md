# NEW finite TR-constrained ensemble operator experiment

2026-10-15, parent3ce4dc0, active long-horizon user authorization. ONE fresh
two-rank host operator job, no SCF, ACE native solver, restart, Cd or retry.
This explicitly changes the test density to the invariant ensemble Dbar, not
the original noninvariant density. No old gate or refused result is changed.

Retain8atom HgTe,176physical source spinors/144electrons/SG15FR/6.46Angstrom,
50/200/Fock200Ry/HSE.25/.106/Gamma-q1. Import canonical preliminary PBE Phi,
FD.001Ry occupations and their exact physical-G time reversals. These are NOT
new self-consistent HSE eigenstates. Source truncation eps_occ1e-8 is unchanged.

Build a Kramers-paired auxiliary cover of Phi and the original physical6frame;
at most364columns, plus12independent direct reference trials P,ThetaP. Solved
band count remains176. Use unchanged native vexx in batches<=176 for BOTH D
and ThetaD. Reuse one exxbuff sequentially. Capture every source/trial/kernel/
FFT/map/action packet. Construct Abar=-.5(V[D]+V[ThetaD]) and its auxiliary ACE
OFFLINE; do not call the old176-column aceinit with new dimensions. No native
ACE integration or variational SCF qualification is claimed.

Prospective gates (all required):

- Actual source, et/wg, trial and physical-G bytes read back exactly; actual
  rank/PID/kernel leases and canonical source/PP/ELF/backend pins match.
- Cover, Gram and Kramers-closure errors<=1e-10; charge error<=1e-8electrons.
- Independent direct covariance on ALL auxiliary columns and12reference trials
  <=1e-8relative; both source orders explicitly measured.
- Retained old direct action is a NEW norm control<=1e-8relative. The old BYTE
  comparison remains REFUSED; this is not another attempt to pass that contract.
- Enlarged Gram H=Q†AbarQ Hermiticity<=1e-8relative, minimum eigenvalue>1e-6Ry,
  condition<1e8. Otherwise no Cholesky/ACE interpretation.
- Offline ACE source/reference action and energy identities<=1e-8relative;
  explicit TR commutator<=1e-8relative. Report floating residuals separately.
- Capture actual nonnegative convolution spectrum, max|c_G| and real-space
  source density maximum. With unchanged FFT normalization, the exchange bound
  a=alpha max|c_G| max_r sum_j w_j|phi_j(r)|²/Omega bounds ||A||. Projection
  residual action bound a*delta<=1e-8Ry is required, not assumed.
- Contract energy with ORIGINAL physical occupied weights, NOT auxiliary
  columns. Report the constrained ensemble half exchange, original half exchange
  and their difference; energy is not a full HSE total/gap/chemical activation.

## Finite cost and safety

Measured prior source176+6direct actions average159.8s/build. Prior fresh24trial
probe takes19.41s in vexx. At most752trial actions suggest~608s plus input/FFT/
store overhead; this is a forecast, not a completion guarantee. A separately
scoped **900s HARD deadline** is justified for this single operator acquisition,
below the accepted eight-build1800s experiment. Old600s protocols unchanged.
Use actual two-core CPUQuota200%, Nice10/CPUWeight10/IOWeight10, one family,
12GiB memory/swap0/tasks12, host4GiB/disk10GiBfloors, sampled aggregate14GiB,
fresh short socket<=107bytes, immutable old ledger, pidfd/manager terminal proof.
Current host resources must independently pass before launch. Expected new
retained files<1.5GiB, one1.216GB aggregate qbuffer; hard caps enforce safety,
not scientific completion. No force/stress, US/PAW, GPU, other q/k/pools/ranks.

The accepted sampled output contract retains between-sample burst/external-writer
limitations; no aggregate continuous quota or host-wide foreign-MPI/netns proof.
On first runtime/science/owner/resource failure, retain original result and STOP
this job; no retry or Cd launch. If successful, a consistent constrained-state
occupation/local-potential/variational SCF driver remains a separate missing
qualification. Do not resume the broken host or manufacture physicalx_c.
