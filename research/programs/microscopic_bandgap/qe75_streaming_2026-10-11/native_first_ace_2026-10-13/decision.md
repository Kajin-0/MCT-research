# Actual stock HSE progress retained; matched first-ACE release remains blocked

2026-10-13 17:18 UTC; starts clean MCT `066e27e`. This is a separate finite
engineering assignment. The historical blocked goal is unchanged.

**CALCULATED — actual native experiment, not a synthetic test:** the user's
two-rank stock QE7.5 two-atom HgTe HSE+SOC calculation completed **14 EXX outer
iterations**, then stopped at MAX_SECONDS420 (native elapsed429.15s). Last total
energy **−484.05790653 Ry**, estimated exchange error **3.87e−6 Ry**, last Fock
ACE term **−8.96709093 Ry**. XML independently gives −484.0579065266556 Ry and
`convergence_achieved=false`. **JOB DONE does not mean fully converged HSE.**

Exact own-unit journal (`r07-small-hgte-hse-20261013.service`, invocation
`ccd6ca6666f84679a01a048dbb6d6990`) verifies the stock launcher and **706,560,000
bytes cgroup memory peak, swap0, 431.497914s journal interval**. Original
configured limits are from the supplied manifest; the collected service cannot
retrospectively attest its old kernel limit settings. Current stock/PP hashes,
input/output hashes, full stdout/stderr, XML and HDF5 metadata/file hashes are
retained here. Save logical bytes **93,390,854**, allocated bytes **93,417,472**.

**Corrected evidence pitfalls:** supplied `all_total_energies_ry` is a 14-record
tail, not the whole history: stdout contains **39** total-energy reports. XML's
first input-section Fock cutoff is zero; its output section is **60Ha=120Ry**, in
agreement with native stdout. Do not parse the first XML match as actual physics.
The small 160-band PBE case is independently confirmed rejected at setup for
`too few bands noncolin case`; the larger host ends in slow Davidson without a
completed material packet. Its stopping action is user-reported. **No Cd result.**

**CALCULATED — independent common-state qualification:** all three actual saved
48-band spinor wave datasets have NC Gram defects ≤**3.200e−15**. Three k-points,
geometry, SOC, cutoffs, k/q meshes and PP pins match the small fixture. Separate
private control/stream copies of the wave/density/schema seed were prepared;
no hardlink shares writable state with the protected reference. They define a
new common numerical initialization (`startingwfc/pot=file`), not the user's
original random startup or a fully converged restart. Old ACE files are excluded.
Actual two-member startup capture/parity is still unobserved.

**IMPLEMENTED CANDIDATE / NOT NATIVE-QUALIFIED:** the scope4 owner now contains
fixed command/profile pins, live Unix nonce/JOB/PROFILE checks, actual cgroup
rank membership/ELF validation, initial/FFT/action certificate callbacks and
checked per-rank stream reservations. This uses the already built private
candidates, without rebuilding or modifying stock. Its native rank callbacks,
crash/lease lifecycle and numerical comparison **have not run**. Do not call
this fully authenticated native ownership or restart qualification.

**MEASURED OS COMPONENT PASS:** one actual production launch-gate probe verifies
MainPID1857813/UID1001, invocation `e2c471e71307486ab0e354488dec6101`, kernel
memory.max12GiB/swap.max0/pids.max12/OOM-group1 and effective hard AS896MiB,
file limit1GiB, control-group kill/no-restart. A wrong launch receipt is refused;
the group becomes empty and the unique failed unit is reset/collected. Elapsed
**0.348345s**, memory peak **20,160,512 bytes**. **NON-MPI:** it deliberately
cancels before exec. No scientific/native rank receipt is issued by this test.

The proposed task/AS box bounds summed resident mappings by 11.3125GiB including
the proposed bounded outside owner/client, under the documented no-raise/no-
migration assumptions. This is not an error-free `/proc` RSS theorem; summed RSS,
host MemAvailable and kernel pressure remain separate runtime checks. The
full outside-owner/native descendant enforcement path is source-only.

**Actionable native release failure:** the candidate's **14GiB output allowance
is not a certified aggregate allocation bound**. Per-file FSIZE and a sampled
tree counter do not cap retained closed MPI/PMIx/backend file generations. The
native-release call was exercised and refuses **before flock acquisition,
registry writes, reservations, service creation or MPI**. Saved low output and
low stock memory cannot promote this allowance to a proof. Accordingly **no new
QE/HSE/MPI run or matched numerical equivalence result exists**.

**Precise necessary remedy:** provide a pinned finite live-inode/generation
table for the fixed first-ACE QE/HDF5/MPI/temp producers, including metadata,
or enforce aggregate file-growth/allocation admission across those producers.
Then connect that real certificate to the live phase5/7 release. Do not delete
the refusal or set a Boolean. Additional raw stock SCFs, process-map searches,
namespace probes or broad synthetic suites cannot supply this missing input.
All-rank ownership/lease crash qualification must also pass before actual native
release. This package makes those unpassed conditions explicit.

**Additional native semantic correction:** QE `errore(...,85)` prints diagnostic
85 but calls **MPI_ABORT(1)**. Future success requires actual two-rank phase6
receipts, complete operator evidence, the exact intentional-stop message and
the corresponding native terminal status; an exit85 check or arbitrary nonzero
exit would be wrong. Acceptance code is corrected; real path remains untested.

No physical Γ6/Γ8 gap, fully converged HSE, Cd response, impurity T-matrix or
material `x_c` is claimed. Original 16-atom/352-band HSE settings, stock QE,
dirty DFT data, supervisors and other sessions are preserved. No historical
goal change, main merge, DFT commit, new Codex session/agent, paid action or
native campaign. Stop at this concrete resource/ownership boundary.
