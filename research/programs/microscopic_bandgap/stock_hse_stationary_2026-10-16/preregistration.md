# Fresh stock-QE HSE8 stationary-host attempt

2026-10-16; baseline a3f49cb. New user authorization explicitly replaces the
previous600s scope with a finite approximately3hour candidate budget. Historical
protocols/results remain unchanged. No new solver, owner, launcher or monitor
implementation; standard systemd transient service and stock local MPI only.

Frozen inputs/PP/ELF/backends and fresh paths: `preregistration.json` and
`host_pw.in` / `cd_pw.in`. Existing stock QE7.5, ACE=true, full outer SCF up to
100 outer/100 inner steps; conv_thr1e-9Ry, adaptive_thr=false, unchanged physical
176spinor/144e,FD.001Ry,HSE(.25,.106),50/200/Fock200Ry,Gamma/q1,6.46A SG15FRNC.
Atomic initial potential/waves, no reused saves. Host first; Cd only following
independently accepted host. No retries, alternate configurations or source edits.

Standard OS contract: one visible local MPI family, two local ranks, one BLAS/
OMP thread each, low-priority200%CPU; MemoryMax12GiB, MemorySwapMax0, TasksMax12,
OOMPolicy=kill, KillMode=control-group, Restart=no, RuntimeMaxSec10800,
native max_seconds10440 reserves checkpoint time, LimitCORE0, LimitFSIZE2GiB.
Systemd owner/unit/mainPID/start/cgroup and actual kernel limits are recorded.
No claim of host-wide foreign-MPI absence or private network isolation.
Read only old data; all fresh native paths and TMPDIR in new private root.
Sample host MemAvailable>=4GiB, disk free>=10GiB and owned aggregate<=14GiB;
stop this own unit on hazard. Sampling is not a continuous disk quota theorem;
per-file limit is not aggregate. No new FD/inventory/owner infrastructure.
Monitor while active; record actual cgroup charge/peak, RSS(shared overcount),
time, disk and stdout progression. No unattended unlimited continuation.

Acceptance requires native final outer dexx<1e-9Ry and inner convergence,
same-model XML/wave/density/occupation readback,144e within1e-8e, FD distribution
and entropy, full-density Theta and actual spatial symmetry qualifications
at1e-8 with Kramers/quartet/Gamma-character checks in physical G frame.
Reaching exx_maxstep may set native conv_elec true for restart output: that
flag/JOBDONE alone is explicitly insufficient. Rebuilt exchange energy/source
consistency and available Hamiltonian/eigenstate residual evidence must be
reported separately; no universal proof or unsupported2meV certificate.
Stock ACE may reproduce the old symmetry failure; if the saved host fails,
reject it and withhold Cd. Nonconvergence/resource/native failure stops this
trajectory without retry. No averaging or retroactive tolerance changes.

Stock native max_seconds/restart support is source-documented, but a saved
checkpoint is not independently restart-qualified merely by existing. This
attempt does not automatically continue an interrupted state. A converged
periodic ordered-cell mass, if its irrep association is valid, is distinct
from finite-smearing/static-lattice/material accuracy and random-alloy x_c.
PBE static diagnostic stays permanently closed;822pins/76oldfiles,stock,
dirtyDFT,originalHSE16,other sessions and historical blocked goal protected.
