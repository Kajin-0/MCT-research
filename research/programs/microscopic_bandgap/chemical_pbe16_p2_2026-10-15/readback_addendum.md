# Prospective readback unit correction — 2026-10-15 05:31UTC

Original readback assertion FAILED; immutable source and exception evidence
retained. Native SCF/owner completed successfully, not yet scientifically
qualified. NO host rerun and no changed scientific tolerance.

QE7.5 PW/src/pw_restart_new.f90:1027–1031 passes tpiba*bg to
Modules/io_base.f90 write_wfc; io_base:123 writes b1 as HDF5 bg1 attribute.
Thus HDF5 B = (2*pi/alat)*XML dimensionless reciprocal vectors =
2*pi*inverse(physical direct cell).T. The original B/alat assertion used
incorrect units. New science_units_v2.py changes ONLY that physical-unit
identity and independently checks it against BOTH XML basis and direct cell,
with the same1e-10 tolerance. No native/source/occupations were changed.

Qualify retained host read-only under this corrected explicitly new readback
scope, including ALL original charge/Gram/Td/Gamma/degeneracy criteria. Only
if this passes may a fresh Cd-only acquisition use the exact same PBE physics
and original pair resource thresholds. Old readback exception is not relabeled.
