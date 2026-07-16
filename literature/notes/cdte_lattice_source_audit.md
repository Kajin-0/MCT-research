# CdTe lattice-source audit

## Status

The physical lattice gate remains open. No lattice value is authorized by this note.

## Primary acquisition targets

1. M. G. Williams, R. D. Tomlinson, and M. J. Hampshire, *Solid State Communications* **7**, 1831-1832 (1969), DOI `10.1016/0038-1098(69)90296-8`.
   - X-ray lattice parameters and linear thermal expansion from 20 to 420 degrees C.
   - The accessible abstract prints an expansion polynomial.
   - The full article is required to verify the absolute lattice values, temperature reference, calibration, and uncertainty.

2. T. F. Smith and G. K. White, *Journal of Physics C* **8**, 2031-2042 (1975), DOI `10.1088/0022-3719/8/13/012`.
   - Primary low-temperature capacitance-dilatometer measurements for CdTe below 30 K and from 57 to 90 K.
   - Full numerical curves or tables and uncertainty are required before integrating a room-temperature anchor toward 0 K.

3. R. D. Horning and J.-L. Staudenmann, *Physical Review B* **34**, 3970-3979 (1986), DOI `10.1103/PhysRevB.34.3970`.
   - Single-crystal X-ray measurements over approximately 8-360 K.
   - The full article must be inspected to determine whether it supplies a traceable absolute lattice anchor or only thermal-vibration information.

## Decision

The Williams plus Smith-White pair is the leading candidate chain for an absolute room-temperature anchor plus low-temperature expansion. Horning-Staudenmann is a cross-check until its numerical lattice content is audited.

Keep `ready_for_execution=false`. Do not populate the CdTe A0 run specification from the commonly quoted 6.482 Angstrom value or from abstract-only information.

Close the gate only after owner PDFs are hashed and exact primary-source locations establish:

- absolute lattice value;
- measurement temperature;
- specimen and method details;
- uncertainty or a defensible bound;
- low-temperature expansion integral;
- propagated uncertainty for the derived 0 K value.
