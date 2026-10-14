# Separate HSE feasibility assessment — no native HSE run

**Decision: full self-consistent 8-atom HSE is NOT ADMITTED under the present
600-second limit.** This is incomplete resource/time qualification, not proof
that a small HSE calculation is impossible on this machine. The completed
50/200 Ry PBE pair is independent of this assessment.

The proposed physical domain would be the same fixed Hg4Te4/CdHg3Te4 cell,
SG15 fully relativistic NC potentials, 176 spinor bands, 144 electrons and
FD sigma 0.001 Ry. HSE uses its usual fraction 0.25 and screening 0.106 Bohr^-1.
The 48-band/36-electron private cold-smearing solver is outside this domain;
no adaptation of that solver is needed or claimed. Original 16-atom/352-band
HSE input, stock executable and all previous failures remain untouched.

## Allocation and timing evidence

**PROVEN UNDER SOURCE/LAYOUT ASSUMPTIONS:** pinned pristine QE 7.5
`PW/src/exx.f90` allocates complex `exxbuff(nrxxs,npol,nbnd,Nkqs)` and
`xi(npwx*npol,nbndproj,nks)`. Here npol=2, nbnd=nbndproj=176,
nrxxs is the local EXX FFT extent, and each complex value costs 16 bytes.
Spinor Gamma calculations cannot use the real-wave shortcut. `aceinit_k`
applies the direct operator to all 176 projectors. Source hashes, upstream
commit and independently enumerated unique k+q counts are in
[hse_feasibility.json](hse_feasibility.json) and reproduced by
[assess_hse.py](assess_hse.py).

The current PBE dense FFT is measured as 60^3. Using that grid for HSE is
conditional on the same cell, backend/layout and Fock cutoff; a native HSE
descriptor has NOT been measured. Use ecutfock=200 Ry, not the older 120-Ry
small-fixture setting: QE defaults ecutfock to ecutrho, and changing it would
add a separate approximation. Defaults and limitations are documented in
[QE's primary input reference](https://www.quantum-espresso.org/Doc/INPUT_PW.html).

**CALCULATED:** the retained actual 2-atom/48-band stock HSE run used k2/q2,
three irreducible k points and a 32^3 EXX FFT. It accumulated 352.64 s in
42 ACE calls, or 25.19 s per complete three-k rebuild. It stopped after
14 outer updates without convergence. Its cold-smearing/90/360/120 Ry regime
differs from the proposed FD/50/200/200 Ry domain; it is a timing anchor only.

| Separate candidate | Unique k+q | EXX buffer, GiB | Buffer + xi bound + measured PBE peak, GiB | Estimated first rebuild including startup, s | Estimated 14 rebuilds, s |
|---|---:|---:|---:|---:|---:|
| Gamma k1/q1 | 1 | 1.133 | 2.156 | 158 | 1,477 |
| Same k2/q1 | 4 | 4.532 | 6.407 | 632 | 5,908 |
| Same k2/q2 | 8 | 9.064 | 10.939 | 3,473 | 45,684 |

The memory column is a **subtotal, not an RSS upper bound**: other EXX workspaces,
FFT plans, backend/MPI allocations, cache and output are not completely bounded.
The xi bound uses sum_rank(max_k local PW count) <= sum_k(global PW count),
conditional on the stated one-pool wave distribution. The k2/q2 subtotal alone
leaves little room below 12 GiB. Gamma/q1 looks memory-plausible, not admitted.

**HYPOTHESIS / COST HEURISTIC:** timing scales the measured rebuild by
trial-band * occupied-source-band * irreducible-k * q-count * FFT-volume.
144 source bands is an approximation; FD tails can increase work. FFT logarithms,
different kernels, SCF histories and convergence rates are omitted. These
estimates are neither lower bounds nor a forecast of successful convergence.
Fourteen outer steps is a comparison horizon, not a convergence requirement.

## Minimum next input and next physics experiment

If HSE is prioritized, the smallest new admission input is **actual 8-atom
Gamma/q1 first-ACE timing, whole-family peak memory and the native descriptor**,
under a separately authorized bounded scope. It can discriminate whether a
future full matched HSE pair deserves a longer time budget. It would still not
be a self-consistent chemical response. No such pilot was launched here.

Under the existing 600-second budget, the best next chemistry uncertainty test
is a matched PBE+SOC 50/200 Ry unshifted 3x3x3 pair with the same physical host
frames. Exact nonmagnetic Td plus time-reversal orbits have sizes 1,6,12,8:
four representatives from 27 points. Current k2 also has four representatives.
A 220–260 s/member cost is a provisional estimate, not admission or BZ
convergence. This next pair is proposed only; no input queue or launch exists.

For a future insulating Cd spectrum, a charge residual alone may not tightly
locate the chemical potential. Keep the dominant projected Gamma8 reference
primary and report the own-Fermi recipe separately. Do not infer an intrinsic
signed gap, HSE convergence, disorder inversion composition or physical x_c
from these periodic finite-cell centroid observables.
