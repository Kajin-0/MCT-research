# What the first-ACE experiment measures

**CALCULATED:** two actual native HSE+SOC first-activation operators in an ordered,
fixed 8-atom cell, with one Cd among four cations. Each member independently
converged its preliminary semilocal Γ-only density before exchange activation.
The functional, occupations, geometry, reciprocal axes, pseudopotentials, cutoffs,
and native solver are matched. This is periodic x = 0.25 chemistry, not a dilute
impurity or a random-alloy average.

Let U6 and U8 be the original physical host reference matrices (two and four
orthonormal complex spinors), embedded from 7,809 to 10,827 plane waves by exact
physical reciprocal labels. No source norm is discarded or renormalized. For
member m, the captured activation operator is

    δH_m = δV_local,m + V_Fock,m[Phi_m, wg_m].

The local term is the difference of native local-potential actions before and
after first EXX activation, on the same six probes. The exchange term is direct
native Fock acting on those probes, not ACE acting off its interpolation span.
Kinetic and NC nonlocal pseudopotential operators are unchanged within this
activation. Actual rhoR, rhoG and their reciprocal labels match byte-for-byte
between the local captures. The pristine QE first branch activates EXX and
recomputes XC without an intervening orbital/density solve; the source excerpts
are pinned in activation_source_evidence.json. The HSE GGA driver subtracts the
short-range semilocal exchange contribution only after activation. Thus the
source-conditioned interpretation is HSE minus semilocal activation at a fixed
preliminary density, with the actual action difference independently captured.

Define the projected ordering correction

    s_m = Tr(U6† δH_m U6)/2 - Tr(U8† δH_m U8)/4,
    Δs = s_Cd - s_host.

**PROVEN UNDER ASSUMPTIONS:** these normalized traces are unchanged by unitary
basis rotations within either fixed subspace, and s_m cancels an additive scalar
operator constant. The independent check explicitly rotates both blocks and
finds a 3.47e-18 Ry difference. This does not remove the physical choice of
projectors or turn a projected trace into a spectral pole. All six vectors are
retained at the same physical cell, origin and spin axes; the old projector
identification and its uncertainty remain inherited inputs.

**CALCULATED:** Δs = +44.1840971934 meV, consisting of +55.9563268497 meV direct
exchange and −11.7722296564 meV local-potential response. The separate member
activation corrections and complete complex matrices are in numerical_result
and the NPZ files. The small measured block splittings and intersector terms
are numerical observations, not a new symmetry proof.

## Uncertainty and non-equivalent observables

Native direct/ACE action and Gram residuals are below 6e-16 on the 176 source
states. Independent per-column complex contractions reproduce the six-vector
matrices within 7.22e-16 Ry and the unhalved Fock energy within 2.85e-14 Ry.
Reference embedding and source wave readback are exact; source Gram defects are
below 1.34e-14. Independent 70-digit Decimal FD charge residuals are −9.55e-12
and +4.265e-11 electrons. These are numerical consistency checks. They do not
supply a rigorous bound on exact operator, eigenpair, cutoff or material error.

The uncomputed HSE orbital/density relaxation can materially change Δs, including
its sign. Γ/q1 sampling, SG15 PBE-generated pseudopotentials used with HSE, the
ordered finite cell, static lattice, numerical FD width 0.001 Ry, and the fixed
reference choice remain physical/method limitations. There is no material error
bar or zero-smearing/zero-point extrapolation. The k3 PBE Gaussian-centroid
response +0.392177486293 eV is a different observable and uses a different SCF
sampling. Adding 44.1841 meV to it would not predict an HSE response or bandgap.

The saved eigenvalues and waves belong to the preliminary semilocal state. HSE
activation total energies are native fixed-source values; the stop deliberately
saves convergence_achieved=false after first ACE. No hybrid self-consistency,
sharp Γ6–Γ8 crossing, absorption edge, topological boundary, or physical x_c is
established. No restart qualification was attempted. The original failed owner,
old numerical failures and 16-atom/352-band target remain unchanged.
