# ONE next input: full-space occupied solve and same-state rebuild

**NOT launch admitted.** This is the smallest decision-changing host state
qualification protocol, not another frozen-response query or an SCF campaign.
Offline candidate coordinates and the two actual rank/G layouts are tested;
the native reader/solver integration below is NOT implemented/compiled/tested.

Use the accepted explicitly invariant144e trial D0 and its original frozen
8atom HSE/SOC/SG15 Gamma/q1 model. Use the supplied D1 coordinates as an
INITIAL GUESS to the fixed-H[D0] occupied solve, never as a certified FD solution.
Do not reuse an old stopped SCF or claim cross-run byte replay of old actions.
The archived expected_trial_density is for D1 ONLY. Once the occupied solve
changes orbitals/weights, independently reconstruct density from its actual
D_out; do not compare or rebuild against D1's old expected local density.

Required deliverable in ONE future host execution, with deterministic stops:

1. Native direct-exchange fixed-H occupied solve in the full50Ry plane-wave
   space. Keep a symmetry-complete eigensolver trial space and the actual FD
   root. Measure full kinetic/local/SOC/direct-Fock residuals independently
   of the diagonalizer. Require charge<=1e-8e, full nonlocal Theta and every
   actual host space operation<=1e-8, native occupations/entropy, and controlled
   omitted occupation. A304-Ritz or symmetrized density cannot pass this gate.
   If the whole-FD1e-8 claim is made, supply its full-space error certificate;
   do not quietly replace the former gate with a finite-space residual.
   The D0 direct source and local potential stay fixed THROUGH this inner
   solve while native evc is replaced by the eigensolver trials. Replacing
   evc must not prematurely rebuild exxbuff/x_occupation from the guess.
2. ONLY after that inner gate, form the new orbitals/weights D_out. Rebuild
   native sum_band density, exxinit direct source, v_of_rho HSE Hartree/XC,
   set_vrs and NC SOC state from this SAME D_out. Compare independent four-
   component FFT density with native rhoR/rhoG; capture source weights and
   entropy. Never average old/new local XC or use old ACE off-span.
3. Capture full H[D_out] actions on all positively occupied trial orbitals
   plus the original6 physical and6 explicit Theta probes. The minimal tested
   transport has176 source capacity,146 active and158 queries. If a solve has
   another active rank or uncertified tail, refuse this narrow layout; do not
   truncate to fit it. A single158 call fits the already reviewed176 EXX table
   domain, but new becp/FFT/capture/lifetime paths still require native source
   and build qualification. Preserve old source/binary/guards, use new typed
   input version; no boolean authorization bypass or tolerance relaxation.
4. Measure rebuilt full-H eigenpair/FD residuals, charge/entropy, native
   electronic energy accounting and original-frame actions. Report accepted
   inner solve versus unconverged outer update separately. A small matrix
   counterexample in independent_results.json proves why the stale-H residual
   cannot replace the rebuilt-H residual. No Cd launch follows automatically.

**First tested current blocker:** the pinned single-state304 native reader
enforces weights(1:142)=1,weights(143:146)=.5 and the rest0, then returns before
electrons/c_bands. The NEW FD304 candidate fails that exact weight contract.
The original profile, not the weight predicate alone, pins D0 orbital bytes:
other orbitals could share those weights. That is not an information no-go.
This executable remains a fixed-trial diagnostic, not a qualified state-update
executable. Relaxing its equality guard would still leave the
occupied solve, same-D rebuild, tail and new-H residual bridge unqualified.
Those missing paths, not socket length or free disk, stop THIS assignment.

**Resource gate for that future source-qualified input:** derive total live
two-rank arrays, native FFT/becp/FD/eigensolver workspace and files from the NEW
code, not from an unrelated prior peak. Current candidate transport measured
58,006,960/57,974,824B per rank, source exxbuff nominal1,216,512,000B unchanged.
Prior fixed-D304+12 query measured329.21s/kernel5.56GB; the proposed occupied
solve has UNKNOWN iteration/time/peak requirements. Fewer readback queries do
not bound that solve. No current12GiB/600s total admission is claimed.

Before any future service independently verify exact source/ELF/PP/input,
fresh roots and both planned member socket byte lengths<=107; live typed rank
lease/pidfd/terminal cleanup and sampled aggregate paths; ONE two-rank local
family;12GiB memory/swap0/tasks12/600s, host MemAvailable>=4GiB,
disk>=10GiB, owned output<=14GiB. Never reinterpret local cgroup isolation as
host-wide exclusion. This phase created no job/root/lease/reservation and did
not probe foreign process inventories or alter supervisors.

**Decision-changing acceptance:** a native full-space nonmagnetic inner solve
and same-D rebuilt-H residual are the first evidence that the former symmetry
failure can be avoided during a real electronic-state update. A residual failure
rejects that state, not the original historical experiments. For screened Cd
physics require the separately matched Cd subgroup/state/source qualification
and the actual<=2meV chemical error certificate in theory.md. No physical gap,
material uncertainty or x_c follows from the host pilot alone.
