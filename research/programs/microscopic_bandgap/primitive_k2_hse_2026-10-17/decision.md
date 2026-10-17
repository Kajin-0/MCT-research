# Primitive k2/q2 control develops severe occupied-density symmetry breaking

2026-10-17 UTC, baseline53ca7b3. **CALCULATED: scientific candidate REJECTED.**
ONE fresh stock-QE7.5 HgTe HSE+SOC run actually executed on two local ranks.
No source/build/solver changes, restart, second candidate, Cd or PBE job.
No qualified nonmagnetic host, signed inversion mass or physical x_c.

**Scope and stop are important:** the six-hour allowance was real, not a600s
restriction. After sustained growth to~315meV candidate-quartet splitting,
the investigator requested stock `r07pk2.EXIT` at00:38:11UTC. QE saved all
and exited00:38:20UTC after16source builds. This was an early scientific
stop, **not a prospectively specified plateau trigger**, timeout, resource
failure, full convergence or proof that no symmetric fixed point exists.
The frozen acceptance thresholds were not relaxed. The experiment establishes
failure of this tested SCF trajectory to remain nonmagnetic; the long-time
endpoint/convergence question was not completed. No automatic retry follows.

## Actual model and observations

Same SG15 FR NC Hg/Te, a6.46Å primitive fcc2atom HgTe/36e/44spinors,
HSE(.25,.106Bohr^-1),50/200/Fock200Ry,FD sigma.001Ry,stock ACE,atomic start.
Native output confirms24crystal Td operations and3irreducible points:
Gamma,L,X with weights1/8,4/8,3/8. XML k coordinates/weights and q2 dimensions
are checked. XML does **not** store explicit q coordinates: stdout's actual8
k+q source coordinates, including Gamma, are checked separately. EXX FFT40³.
No `open_grid` or additional native postprocessor was run.

| Measured terminal quantity | Result |
|---|---:|
| Corrected total, Ry |−484.0601044561862|
| Fock/2, Ry, native displayed |−8.96881784|
| Final outer dexx, Ry |6.23e-6; threshold1e-9 FAILED|
| Last inner SCF energy error, Ry |8.73726e-11|
| XML outer convergence / reachedEXX message |false / absent|
| Charge error from weighted occupations, e |−1.57243e-11|
| Independently saved rhoG zero-mode error, e |−1.57172e-11|
| Maximum FD formula error |1.003e-18|
| Native Gamma density Theta op norm |0.903711721344|
| Native L / X density Theta op norms |0.01691385 /0.01365988|
| Gamma Td density max defect |0.99742603|
| Gamma8-character spread |315.272216901meV|
| Gamma6-character spread |0.895450316meV|

The15measured outer residuals first decreased to5.3e-9Ry, then grew with the
quartet splitting, reaching3.77e-4Ry before falling to~6e-6Ry. Native inner
SCF convergence/exit0/JOBDONE do not certify an outer stationary state.
Complete trajectory and displayed intermediate level intervals are in
`state_result.json`; displayed bands have .0001eV resolution. Labels at
intermediate iterations are provisional index tracking, not proved adiabatic
subspaces. Final complex overlaps confirm bands33–34 Gamma6-character,
35–38 Gamma8-character, each original-frame weight>.99985 and>.99995.
They are **not exact irreps** of this broken state: native span leakage reaches
.01060/.002987, above1e-8. Do not average the split levels into a signed gap.
Negative-dexx warnings are retained in stdout; the printed absolute indicator
is not treated as a rigorous operator/eigenpair-error norm.

**Direct Kramers evidence:** Gamma35 is occupied.99999053, while its largest
Theta-overlap partner38 has occupation9.12e-6 and overlap probability.79003.
Likewise36 principally maps to37 across the occupation split. These are
largest-overlap diagnostics; degenerate spaces need not possess unique native
band partners. Full density norms retain all44states and do not assume them.
An independent manually mapped native-band35 scalar witness is.81670669,
confirming a large defect without QR or an assumed closed six-state frame.
The minimum operator-norm distance to any Theta-even density is at least
.90371172/2=.45185586 (triangle inequality). No tiny rounding correction repairs it.

At L and X all36occupied bands are filled; their highest occupied energies
are8.14142/6.45572eV versus mu9.12661eV. Only the four Gamma levels have
fractional occupations. Thus the added coarse sampling still leaves the
near-Fermi partial occupation concentrated at one star; it is not a resolved
heavy-hole infrared continuum. The independent monotone FD charge root has
zero displayed residual and moves mu by only4.40e-8eV. This is not the old
cold-smearing spurious charge-root failure.

## What is independently known about the full BZ and frame

Theta maps every stored TRIM via **G->−G−2k**, checked with Theta²=−I. All44
states/occupations are used; no spectral atom, Gamma-only approximation or
discarded QR directions. Three actual native representative tests are direct.
The8full-BZ fibers are **symmetry-transported reconstructions**, not native
full-BZ exports/bitwise EXX-buffer replay. All24×8 covariance paths are tested
without averaging. Broken little-group covariance means a unique symmetric
extension is not certified; the reconstructed maxTd.9974 is not a symmetry
PASS. Its Gamma witness is already a native-fiber failure. Theta norm is
unchanged by the unitary star transport, so every generated L/X fiber remains
TR-odd. Do not claim independently acquired eight native wave packets.

Physical reference labels use true primitive G matching to the accepted e90
frame. Its lost e50 probabilities are~2.038e-6(Gamma6),~1.278e-7(Gamma8),
explicitly retained without renormalization. Cell/origin/PP/spin axes match;
the e90 stationary state is **not** transferred as an e50 same-D state.
Full-H eigenpair/source residual packets are unavailable; energy/dexx and the
retained spectral Theta commutator do not replace them. No numerical2meV or
functional/material uncertainty certificate is issued.

## Discrimination and next scientific boundary

**CALCULATED:** adding this coarse primitive k2/q2 sampling did not prevent
the severe stock FD-HSE trajectory pathology. Its~315meV character splitting
is smaller than the old8atom~661meV, but both fail symmetry. This does not
prove a universal HSE/ACE bug, physical magnetism, k independence or eventual
nonexistence of a symmetric solution. A finite uncompleted trajectory cannot
establish those claims.

**PROVEN UNDER ASSUMPTIONS / CALCULATED:** [folding_bound.md](folding_bound.md)
and the read-only old-state test show that conventional8atom Gamma folds
primitive Gamma+3X if primitive translations hold. New k2 adds4L. The old
primitive-translation defect is only~1.24e-5; exact translation twirling can
move its density by at most9.23e-6 and leaves Theta lower expression.99997850.
Translation breaking alone therefore cannot explain away its order-one defect.
Twirling is an algebraic diagnostic, **not** a new self-consistent state.

**HYPOTHESIS:** coarse near-Fermi quadrature and nonlinear exchange/occupation
feedback may sustain the unstable trajectory; source compression/numerics can
also contribute. No exact response Jacobian or isolated causality is measured.
The old accepted primitivee90/k4/q4 cold run changed cutoff, Fock grid and
occupation law relative to this run; it does not isolate the cure. Relative to
the failed8atom run, functional/cutoffs/FD law are held, but cell representation,
BZ/source weights and initial orbital realization differ.

**ONE next discriminating physics input, not admitted or queued here:** a
separately frozen stock primitive **k4/q4 at these same e50/FD settings** would
change quadrature while holding the occupation law/cutoffs. Gamma weight drops
from1/8to1/64. At an unchanged40³grid, the nominal source-buffer capacity
scales from.721GB to5.767GB before padding/other allocations. Native current
Fock wall792.14s/16builds gives a source-count forecast
792.14×(8/3)×(64/8)=16899s(~4.69h) for16builds, NOT a convergence/runtime bound.
Actual descriptor/peak/full cost and independent admission would be required.
No automatic direct-exchange or denser-mesh launch. Even a passing primitive
host would still need a matched k-sampled Cd state and composition/disorder
evidence; it would not produce random-alloy x_c.

## Resources, negative records and closeout

OS wall856.338783s; native855.66s. Kernel peak1,042,771,968B; sampled RSS
1,114,423,296B(shared overcount),tasks7,swap0,no observedOOM/limit events.
Sampled host available>=27.756GB,disk>=49.354GB,owned files+metadata37.303MB;
12GiB/swap0/tasks12/6h caps held. Sampled output/floors are not hard quota or
continuous external-writer guarantees. Standard local MPI/cgroup is not proof
of host-wide MPI absence or private network isolation.

Prelaunch user-bus env was absent; an ordinary manager query failed before any
service. Invocation-local existing bus env fixed it; exactlyONE service/native
run launched. First OFFLINE parser incorrectly counted XML's48Bravais entries
as24crystal entries; failure retained, filter corrected by actual info tags,
geometry thresholds unchanged. No native error was hidden/retried. Final
resource observer completed normally, unlike the old terminal sampler failure.
Both ranks/launcher gone,cgroup absent,own unit unloaded. All822protected pins,
76originals,dirtyDFT,stock/old source/failed runs and permanent PBE closure
verified unchanged. No other session/service/main/credential changes.

**STOP.** Native result is a rejected partial symmetry-breaking control.
`verification.json` validates that negative conclusion, not SCF/material PASS.
Raw wave/ACE/density files remain private at the manifest paths; Git carries
stdout/XML/hashes and rerunnable read-only analysis, not those raw arrays.
