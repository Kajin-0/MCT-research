# SEPARATE P2 frozen prospective PBE16 composition experiment — 2026-10-15

One new sequential stock-QE Hg8Te8 / CdHg7Te8 periodic ordered pair, x=1/8.
No retry, no HSE or reuse of an old aborted state. Parent science 60894e0.
The prior PBE16 90/360 Ry cold-smearing attempt remains failed. This is the
separately authorized exploratory PBE+SOC alternative at the accepted PBE
50/200 Ry FD method, NOT the original HSE16 target or a dilute impurity limit.

Cell rows a*(0,1,1),(1,0,1),(1,1,0), a=6.46 Angstrom; 16 fixed atoms,
one Cd at cation origin. SG15 FR NC PPs, 352 spinor bands, 288 electrons,
FD sigma=.001 Ry, conv_thr=1e-9 Ry, Davidson full accuracy, mixing .3,
atomic+random starting waves, Gamma SCF, native Td/time-reversal symmetry.
Native SCF convergence, charge residual<=1e-8 e, occupations reconstructed
within1e-9, Gamma HDF5 Gram<=1e-8, native 24 crystal operations and actual
host Gamma6/8 reference symmetry/primitive-translation coverage are required
BEFORE Cd. Selected host multiplet spread<=1e-5 eV; no quartet averaging
to hide a failed spread. No changed occupations or projector purification.

Primary observable: original accepted PBE8 40Ry host Gamma6(dim2)/Gamma8(dim4)
projectors embedded isometrically with G16=G8 Q.T, Q=ones-I. Coefficients
unchanged, exact NC metric, matching Cartesian axes/origin/lattice. Physical
reciprocal vectors independently checked from both cell and HDF5 descriptors.
Gaussian projected ordering Cd-minus-host at W=1,1.5,2,2.5,3 eV; W2 primary.
Same positive-tail/projector/IEEE conditional bounds and mass>=.05 as before.
Secondary causal inverse-resolvent response at t=0 relative each own Fermi,
eta=.025,.05,.1 eV is a separate observable; eta is resolution, not linewidth.
No unbounded-moment tail claim. No finite-cell, functional or material error
is supplied by the spectral-completion bound. No physical gap or xc inference.

Host primitive Gamma identification uses EVEN new Miller indices. New cell
Gamma folds conventional Gamma and R, so comparison to old eight-atom k3
is confounded by composition, cell and BZ sampling. Report that explicitly.
The local Te environment changes from four N=1 tetrahedra at x=.25 to four
N=1 plus four N=0 at x=.125; neither is random Bernoulli alloy statistics.

Resource contract: one two-rank local MPI family, 12GiB cgroup hard memory,
swap0, Tasks12, host floors4GiB available RAM/10GiB disk; sampled aggregate
output14GiB with all old accounting/retirement refusals. Two64MiB escrows.
Fresh short socket <=107 bytes, pinned inputs/PPs/ELFs/owner and validator.
NEW bounded wall900s/member, QE max_seconds840s, nice10/two CPU quota and
low IO/CPU weight. User permits measured bounded wall. This finite scope
allows the doubled-band/doubled-volume Davidson cost, not indefinite work.
Previous90Ry16atom native estimate4.24GB total and accepted eight-atom timing
are admission heuristics, NOT proofs of completion or process memory bounds;
kernel cap and live pressure/accounting remain authoritative. No concurrent
analysis with large arrays during native jobs. If host fails, withhold Cd.

Preserve stock, dirty DFT, old failures and all other sessions. Native local
contract does not prove host-wide foreign MPI absence/private networking.

## Prospective P2 amendment, before any P2 native service

Original scope owner FAILED before QE authorization due to socket-name mismatch;
its unit/profile/source/guard result remain unchanged. New source/root/nonces
fix server bind to SAME checked_address used by client and Account; terminal
failure is reported before reading nonexistent spectra. Actual exact-path
non-MPI bind/connect/allowlist consistency required in both fresh roots. No
change to scientific or resource criteria, no reuse of failed native state.
