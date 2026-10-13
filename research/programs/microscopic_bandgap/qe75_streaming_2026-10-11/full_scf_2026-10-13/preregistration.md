# Full-SCF paired numerical preregistration — 2026-10-13, before native launch

Starting clean7116be0. ONE new control then ONE streamed full-SCF evolution, not
another fixed-orbital experiment. Same primitive HgTe/HSE+SOC/SG15/48bands,
90/360/120Ry, k2/q2, .25/.106 screening, smearing0.001Ry, Davidson full accuracy,
conv_thr1e-10Ry, adaptive_thr with original1e-5/.1,20outer/100inner limits.
Byte-identical independent copies of the accepted48-band seed/density/schema;
no oldACE imported. Same compiler/backends/rank2/one pool/group/task. Both new
EXX/observer compilation O2/no-fast-math with bounds checks; solver accuracy and
exchange arithmetic unchanged. Native max_seconds480 is an operational soft
stop, leaves120s for old96–113s worst first-ACE and punch; external hard600s
always applies. No time-cap extension/accuracy downgrade or automatic resume.

Initial active source waves, rhoG, et/wg, physical G/FFT maps must be byte equal.
Only reconstructed rhoR/vrs use this **new expressly authorized SCF numerical
domain**: max absolute5e-14native density units /5e-12Ry. Old full-state byte
refusal remains unchanged. No phase alignment/replacement of computed potential.

Compare common completed outer steps in native full precision: total/Harris/
Fock contractions/dexx max difference1e-8Ry; eigenvalue max2e-7Ry; occupation
max1e-8; charge rhoR/rhoG max1e-9native units; vrs max1e-8Ry; gauge-invariant
occupation-weighted orbital-density relative Frobenius difference1e-7. NC Gram
self-defect<=1e-10. These fixed gates cannot be enlarged after observing results.
Runtime differences are not physical differences; compare step indices, not
elapsed time. Missing common steps means partial/no comparison, never PASS.

Native observer preserves evc, modifies no SCF operands. Snapshot after completed
new-operator/energy update and final punch; fullprecision energies plus exact
wave/density/map fields. Charge and orbital *changes* between outer snapshots
are trajectory residual diagnostics. Orbital diagnostic is a density-operator
change, **not** ||Hpsi−epsilon psi||. Native printed inner SCF estimated accuracy,
ethr and dexx retain their distinct meanings. Convergence requires native final
hybrid criterion dexx<1e-10Ry and native XML/log success, not matching two failures.

Stable orbital comparison: for orthonormal A,B and occupations Fa,Fb, set
S=A†B,R=B−AS,M=R†R,C=SFb,D=Fa−SFbS†. Then
||A Fa A†−B Fb B†||F² = ||D||F²+2tr(C M C†)+sum_ij fb_i fb_j |M_ij|².
Positive block form avoids subtracting nearly equal O(1) traces. NC numerical
Gram defects are independently bounded; no topology/gap follows from this.

Each streamed operator generation closes/deletes old qstore ONLY after old Fock
readers finish, then live both-rank reservation before next generation. Unique
request generation; actual extent/quota/block checks, no whole-store copy.
At stopped outer/inner state, retained typed oldxi/occupations sidecar+qstore
and native punch are **capture evidence**, not qualified import. New fresh
scope5 refuses restart imports; no automatic legacy restart publication. Final
native HDF5 wave/rhoG readback is required; full oldoperator/import/mix/outer-state
continuation remains a separate gate. Resume prohibited unless qualified.

Local owner kernel12GiB/swap0/tasks12/hard600s, sampled RSS12GiB/MemAvailable4GiB/
disk10GiB/output14GiB; actual ext4 per-rank64bit extents, owned escrow1GiB, unique
private outputs and live typed scope5. Same accepted sampled writer/burst risks,
no hostwide exclusion/network proof. Lifecycle recognizes clean terminal0 only
after both final post-punch receipts, exact invocation, empty group and native
JOBDONE; unsafe/incomplete/live inventory still refuses. No original job/stock/
dirty DFT/supervisor/session/goal changes. Partial trajectories if soft/hard time
reached; no false convergence, xc or whole-SCF memory benefit from unmatched work.
