# Minimal information for the next state update

PROVEN UNDER ASSUMPTIONS: let S be an invariant finite space with projectorP,
H a group-covariant linear Hermitian operator, and D an invariant density
supported inS. Both

    S_occ = S + range((I-P)HD),
    S_all = S + range((I-P)HP)

are invariant under all unitary/antiunitary symmetries. For example U_gP=P U_g
and U_gH=H U_g imply U_g (I-P)HP = (I-P)HP U_g; the range is invariant.
The same holds for D and for the antiunitary coset by real spectral calculus.

These are the SMALLEST spaces containing S and respectively Hrange(D) or HS:
every such space contains the corresponding projected residual. Their added
dimensions are the corresponding residual ranks. This is ordinary block-Krylov
algebra, not a new exact nonlinear SCF closure. It does not require a bandgap.

CALCULATED from the actual full nativeH[D0] vectors: occupied completion adds
146directions at every1e-3..1e-8Ry threshold; all-source completion adds152.
The original six auxiliary directions remain coverage directions, not solved
bands. Both actual new spaces are separately audited to the UNCHANGED1e-8
Td/Theta/translation gate. The original152 and all old source/ACE failures are
not reclassified. Numerical dimensions below roundoff are not claimed exact.

The old GalerkinFermi quartet has full-H residual .02625424Ry(~.357eV), despite
its tiny in-space eigenvalue residual and symmetry. Completing the action space
captures these existing HQ vectors to floating roundoff. The old Ritz vectors
are UNCHANGED: this does not magically turn them into full-space eigenvectors;
their residual now lies INSIDE the expanded space. One must actually obtain
H on the new directions and rediagonalize before a smaller eigenstate residual
can be claimed. H[D] must then be rebuilt after a density change.

The next minimum fixed-state acquisition is **H[D0] on only the152new residual
directions**, plus independent controls. Reuse the known152HQ columns and source
D0 from this accepted record. The missing lower-right block R*HR cannot be
deduced from symmetry, known cross-blocks, or source eigenvalues. Hermiticity
determines the reciprocal cross-block, not that lower-right block. This is
precise new information, not another full repeat of the accepted acquisition.

At the measured170directactions/185s, one similar152new+control query forecasts
~185s and~4.3GB, under the existing600s/12GiB local caps. These are forecasts,
not admission or a convergence bound. A NEW query manifest/typed profile and
validator must distinguish appended query slots from solved/source spaces,
verify identical trialD0/PP/cell/kernel/FFT/local state, and refuse incompatible
data before combining matrices. The existing private direct-action driver can
be reviewed for reuse; no binary/source or numerical physics change is implied
or silently authorized. No second native query was issued in this one-acquisition
phase, no state was resumed, and no new native job is queued.

A later FDupdate in the expanded Galerkin space remains an approximate inner
state until its full eigenpair/offspace and occupied-tail budgets pass. It is
not an HSE fixed point until same-state charge/Hartree/XC/directFock and outer
density/energy/entropy residuals converge. A finite useful whole-space upper
bound still requires complement spectral information; the new nonzero commutator
lower bound already falsifies stationarity of D0 without that information.
