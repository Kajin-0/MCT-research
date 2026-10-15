# The one-specimen optical discrimination test and intake gate

This is an acquisition/acceptance specification, **not executed analysis**.
The prior derivation is
[Route B, B1–B3 and third-field test](../competing_inversion_routes_2026-10-15/route_B_optical_mass.md).
No new physical coefficient, target root or numerical precision is assumed.

## Exactly what can change the science decision

For one unchanged specimen/state, track the **same** HH-to-electron Landau
index/spin/polarization family at 0<B1<B2<B3. The conditional homogeneous Kane
adapter is

    t(B) = M + sqrt(M^2 + a B),   a>0.
    Q = B2 t1^2 - B1 t2^2,  D = B2 t1 - B1 t2,
    M_opt = Q/(2D),  a = (t1^2 - 2 M_opt t1)/B1.

B1,B2 determine the two parameters; reserve B3 before inspecting its line
center. Compare its entire admitted center/error interval with
M_opt+sqrt(M_opt^2+a B3). Reject the constant-parameter line/observation
adapter if they are disjoint after including all model/calibration errors.
Do not refit the two parameters using B3 and call that an independent test.
An isolated minimum in a normalized transmission plot is not automatically t.

Use the existing explicit epsilon_Q, epsilon_D, M interval and held-out-field
bounds. Require separated positive field intervals, D_hat>epsilon_D and a>0
throughout the admitted parameter domain. A sign is certifiable only if
|Q_hat|>epsilon_Q. Include common calibration covariance; shared B=0 references
and repeated scans are not independent errors. Conservative interval propagation
is allowed without assuming independence. A failed third field rejects the
adapter at that precision, not uniquely a microscopic disorder mechanism.

## Necessary records and calibration specifications

1. **Provenance/specimen:** original run identifiers/timestamps and immutable
   file list/hash; sample A/figure correspondence, same illuminated position,
   thickness, orientation, growth/anneal history and layer/buffer profile.
   Do not merge three temperatures or different spin families into three fields.
2. **Acquisition:** native interferograms if retained, otherwise original
   numerical spectral scans with disclosed processing; B=0, substrate/reference,
   dark and repeat scans. Preserve linear detector counts, units, energy axis,
   complete measured windows, rejected bins and saturation/opacity masks.
   A scan export is useful only with its processing/provenance chain; a plot
   export is insufficient. No demand to create new measurements is implied.
3. **Instrument/state:** energy-axis standard, uncertainty and correlations;
   resolution/line-spread function, apodization/phase corrections, detector
   response/nonlinearity and drift; actual B calibration, polarity, remanence,
   stability and orientation; specimen T sensor calibration, gradients/stability
   and distinction from bolometer temperature. No published resolution is a
   substitute for center-error or systematic calibration bounds.
4. **Polarization/physics adapter:** actual measured channels, handedness relative
   to B/propagation and leakage calibration. Unpolarized data must be labelled
   as such, not retrospectively assigned sigma+/sigma−. Need family assignment
   and overlap bounds, carrier filling/Hall uncertainties, strain/inhomogeneity,
   phonon/substrate background and finite-k_z/HH/remote-band corrections.
5. **Composition independent of the target gap:** method, calibration/reference
   standards, measured x and uncertainty, specimen/spot/depth correspondence and
   spatial variability over the optical footprint. Growth ellipsometry can be
   useful if independently calibrated with these errors; it is not rejected
   merely for being optical. A composition inferred by fitting Kane/gap laws
   is circular for the present purpose and fails this column.
6. **Windows/tails:** positive transition/absorption measure or a qualified
   observation operator from transmission. Report retained weight/moment,
   overlap/background errors and omitted-mass/absolute-moment bounds (or an
   independently validated finite-window line adapter). Unseen tails cannot
   be bounded by the last plotted pixel; Lorentzian full first moments are
   not justified. Fix windows/line extraction before the held-out result.

No arbitrary meV/Δx precision threshold is invented. Required errors follow the
actual Q/D margins and third-field separation. If unavailable calibration or
line-adapter terms cannot be bounded, the result is inconclusive/refused, not
zero error. A single finite-T specimen can test an operational model, **not**
bracket physical zero-T x_c. Independent composition/temperature and a qualified
microscopic-to-optical relation plus composition transversality would still
be needed; no endpoint interpolation or empirical gap fit closes those gaps.

## Access/consent and stopping rule

Obtain an authorized custodian's confirmation of retention and sample mapping,
re-use/analysis permissions, attribution and any redistribution/embargo limits.
Record a persistent public link/version if offered; otherwise distinguish private
access from public availability. Article CC licensing is not evidence that
unseen raw records have been released. Consent to share privately is not consent
to publish raw files. If records are unavailable or only fitted/figure data
survive, stop this intake; no replacement measurement, outreach or fit is
authorized by this report. The request below remains an unsent draft.
