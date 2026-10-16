# STOP before native: qualify the occupied solve/rebuild bridge

**2026-10-16 11:38 UTC; baseline clean/pushed be13479.** No QE/MPI service,
build, source edit, DFT write, Cd or owner admission was attempted. The original
failed symmetry, byte-replay, owner, occupation and convergence gates survive.

**CALCULATED — a concrete new state input is available.** The FD304 matrix
itself was already known. Here its actual full-G spinors were constructed as
a176-capacity trial source, without density symmetrization or level averaging,
and independently qualified for transport/charge/nonlocal symmetry:

| Retained-data trial D1 check | Result |
|---|---:|
| FD charge / independent FFT charge |144.00000000000006 /144.00000000000009e|
| Full nonlocal-density Theta Frobenius upper |6.97673e-12|
| Maximum all96 host spatial-density Frobenius upper |7.76627e-12|
| Source176 Gram operator defect |4.46646e-15|
| Independent eigensolver/FD density difference |4.40865e-12op|
| Independently reconstructed maximum local spin |3.27612e-14Bohr^-3|
| Local charge-density change from D0, maximum |.00685046760Bohr^-3|

These are floating retained-data calculations, NOT actual native symmetry
qualification of a new state. [Trial coordinates](trial_coordinates.npz) and
[expected four-component density](expected_trial_density.npz) are reproducible
inputs, not a saved QE checkpoint. Both actual rank/G frame transports roundtrip
bitwise (58,006,960/57,974,824B), with146 active source states and158 full-H
queries including the ORIGINAL6 probes and their explicit Theta images.
Native code to consume that new layout is not claimed implemented or tested.

**Actual chemical subgroup verified independently:** the frozen host has96
space operations; Cd at the origin retains24, removing fcc translations while
retaining Td about that site. No host symmetry is imposed on a Cd state.
No native Cd state passes by virtue of this geometry result.

**PROVEN UNDER ASSUMPTIONS / CALCULATED obstruction.** Symmetry and a finite
FD fit do not imply full-space stationarity. The known full-action commutator
requires a uniform Hamiltonian correction of at least709.1054meV before THIS
supported D1 could even commute with it (exact-action model, no directed
roundoff enclosure). This is NOT a projected chemical-error bound. Nonlinear
H[D1] might supply a correction; it has never been measured. A full step's
nonlinear free-energy decrease would require, for example, an independent
electronic Hessian upper below6.91664Ry in the stated norm. None exists.
The old FD304 nonstationarity is preserved, not retrospectively repaired.

**FIRST concrete source refusal:** the pinned qualified reader enforces
the old occupation template (142 ones/four halves) and returns before the occupied
solve. The new candidate fails that exact reader contract. Removing its equality
guard would NOT implement the missing full-space FD solve, rebuilt local XC/
direct Fock and new-H stationary-residual bridge. A standalone nonlinear8state
test catches precisely that defect: stale-H FD residual0 becomes.0214043 after
the correct rebuild; the genuinely closed-loop model reaches5.42e-11 in11
steps. This tests the logic, not native or HgCdTe convergence.
Other orbitals could share the old weights; it is the original profile that
pins D0 bytes. The refusal is an existing executable-contract boundary, not a
proof that constructing a suitable state-update program is impossible.

**ONE next input:** [the tested prospective protocol](next_input.md) specifies
a direct-exchange, symmetry-qualified full-space occupied solve initialized by
the new trial, followed by same-D density/Fock/local-XC rebuild and independent
full-H residual/readback. It is a host qualification, not another frozen-action
batch or an unchanged176-ACE continuation. Complete occupied-solver resource
and native interface qualification are still absent; old5.56GB/329s query
measurements do not certify that solve under12GiB/600s. New owner/resource
admission is deliberately NOT attempted after the first source/state refusal.

**Chemical interpretation remains refused.** Theory gives the explicit
prospective<=2meV error budget and required state-to-H stability certificate.
Neither it nor a qualified matched HSE state exists. The finite+39.8115meV
activation and95.54meV mostly-even leakage retain their original definitions;
they are not full screened Cd physics, an inversion gap or x_c. No new physical
coefficient, fitted bowing, manuscript or novelty claim. Registry status stays
unchanged. Stop this bounded phase at the executable state bridge.

Reproduce: single-threaded Python `analyze.py`, `independent_checks.py`, then
`verify.py` in this directory, using the repository venv and
`PYTHONDONTWRITEBYTECODE=1`. Raw native packets remain private/pinned; the
coordinates alone require the original accepted full-G basis, not an invented
replacement. See [theory](theory.md), [results](result.json),
[independent checks](independent_results.json) and [verification](verification.json).
