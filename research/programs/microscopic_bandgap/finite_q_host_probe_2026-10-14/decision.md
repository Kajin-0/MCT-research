# Physics-first decision — retained native contraction completed

**2026-10-14.** Starting clean `1de0171`, executed one bounded existing-data
calculation after a source-unit intake correction. No QE/HSE/MPI process,
supercell, queue or supervisor operation was launched. All previous failures,
stock QE, dirty DFT and other sessions remain unchanged.

## Actual physics evidence

The accepted HgTe primitive HSE+SOC f120/k4/q4 reference has native signed Γ gap
−289.770114 meV and Td-qualified Γ6/Γ8 spinors. Its saved original and expanded
native occupations both sum to 36.0 electrons. This source is distinct from the
newer 48-band control12, which remains unconverged with its owner FAIL preserved.

The defined finite-q wavepacket contraction on its actual 64-point/44-band
spectra gives:

| Quantity | Γ6 reference probe | Γ8 reference probe |
|---|---:|---:|
| Retained probability |0.8097202595|0.7609124313|
| Uncomputed band probability |0.1902797404|0.2390875669|
| Unresolved plane-space probability |1.30e-10|1.78e-9|
| η-smoothed window mass |0.0125750289|0.0210681592|
| Centroid relative to native r |−126.670559 meV|−41.899075 meV|
| Conditional tail error upper |0.859415 meV|0.568715 meV|
| Raw non-Γ weight within ±0.5 eV of r |2.42e-17|0.0534063137|

**CALCULATED:** this coherent-host wavepacket ordering is −84.771483 meV;
its conditional spectral-completion interval is [−86.199614,−83.343353] meV.
It is a different observable from the −289.770114-meV Γ gap, and is not a
chemical response or physical uncertainty interval. The non-Γ Γ8-probe weight
provides finite-grid evidence of near-common-mode channels; interpreting those
channels as a bulk continuum or as an impurity susceptibility remains conditional.

The calculation took 6.9483 s, peak process RSS 511127552 bytes under the
512-MiB address-space/60-s analysis cap. It streamed existing files one at a
time and retained only contractions; no raw QE data or potentials were copied
into Git. Independent integral, basis/origin/relabel, closure and tail tests
pass. No empirical gap coefficient enters.

## Source intake and preserved negative findings

All six inspected prepared host/Cd-member schemas have zero eigenvalue sets;
these are dry initialization records, not spectra. The exploratory 16-atom PBE
host is incomplete and its Cd member has only input. The accepted CdTe binary
Γ gap (+1.575364691 eV) is not Cd substituted in HgTe. Its earlier 26-trial frame
is not an accepted scattering host: time-reversal error 2.951369 meV exceeds
the unchanged 1-meV gate and no common physical basis is established.

The initial helper import had no mpmath dependency available; standard-library
Decimal arithmetic avoided any install. The first actual intake refused a
k-coordinate mismatch before completing the contraction. Native source and
headers show XML coordinates use 2π/alat while HDF5 stores inverse-Bohr values;
the explicit conversion corrected the comparison without changing its 1e-12
tolerance or the spectra. The refusal, original evaluator/preregistration and
correction are retained. No old result was retroactively passed.

## Go/no-go and next minimum input

**GO: bounded retained-data physics diagnostic completed.** The large missing
global probability does not automatically require more bands for a narrow
η-smoothed observable: its known high-energy separation tightly limits the
window tail. This can reduce future input demands once the *actual substituted*
prefix and its separation are known. It does not justify lowering the original
352-band target or transferring a binary tail bound to an impurity.

**NO-GO: physical Cd response/x_c or new native chemical acquisition under the
existing tiny-fixture profile.** The qualified private root explicitly accepts
only 48 bands, three k points, 36 electrons and its fixed weights. The prepared
chemical target has 352 bands and 288 electrons; using that solver/profile would
refuse. The terminal owner is tested non-MPI prospectively, not yet a native
352-band admission. Resource, input/frame, numerical and restart gates are not
weakened or bypassed. No full-size launch or covert smaller-cell substitute.

The single highest-information missing physical input remains an accepted
self-consistent Cd-in-HgTe Γ spectrum with complex cross-overlaps against a
qualified matched pure-host six-spinor frame, retained coverage, electrostatic
alignment and source/residual metadata. Both matched SCFs remain necessary
unless uniform folding/operator equivalence is independently certified.
That packet would distinguish actual static mass response from P-to-Q leakage;
another binary scalar gap or unqualified sorted edge cannot. Existing
`physical_input_qualification_2026-10-11/minimum_acquisition.md` retains the exact
design and limitations. Successful runtime/resource/error reduction remains
unknown; no physical x_c uncertainty improvement is claimed.

Stop at this concrete chemical-input/admission boundary. No infrastructure
campaign, new fit, parameter sweep, or fabricated convergence follows.

## Publication

Existing `id_ed25519_kajin` SSH authentication now works: the prior `89922a7`
and `1de0171` commits are on the existing research branch. Earlier publication
failure files remain historical; no key, permission, remote or force changes
were made. Commit/push this verified physics package to that same branch only.
