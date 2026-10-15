# Interpretation and source checks, before pair analysis

The primary spectral probes retain each configuration's own Fermi reference,
as frozen. A common +/-0.5eV displacement tests probe choice only. No separately
aligned impurity potential, vacuum level or common-mode T matrix is inferred.
The native HDF5 reciprocal basis is independently matched to the identical cell;
internal unitary rotations and arbitrary physical-G reorderings must preserve
the actual complex-overlap traces to1e-12. Full matrix and scalar inverse
resolvents are different contractions in the reduced-symmetry member.

QE7.5 `PW/src/v_of_rho.f90:v_h` fixes HartreeG0=0; `setlocal.f90` builds ionic
localG0 from species structure factors and the same PP transforms. Equal
composition/cell fixes this ionic constant. This supports a common code gauge,
but no local potential alignment is measured here; the primary analysis does
not use cross-run absolute eigenvalues as an impurity Hamiltonian. Changes in
the XC spatial mean are physical within the method, not automatically a gauge.

QE `PW/src/electrons.f90:1141` includes `demet` in `etot`; lines1717-1718
separately print `etot-demet`. Report BOTH the same-composition finite-FD
free-energy contrast and the internal-energy contrast. They are periodic-cell
configuration energies, not zero-temperature isolated Cd-pair binding energies.
No certified total-energy uncertainty follows from an SCF estimated residual.

Conditional spectral bounds are the previously derived positive omitted-measure,
nearby-frame and IEEE models, applied to the newly declared native50Ry host
frame. They exclude Hamiltonian/eigenpair, functional, sampling, cell, FD,
structural and material errors. A tiny conditional interval does not validate
a physical alloy gap. MissingN3 and nonlocal/environment identifiability remain.
