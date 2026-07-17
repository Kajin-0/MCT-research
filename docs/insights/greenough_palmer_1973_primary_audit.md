# Greenough-Palmer 1973 primary CdTe source audit

## Source identity

R. D. Greenough and S. B. Palmer, “The elastic constants and thermal expansion of single-crystal CdTe,” *Journal of Physics D: Applied Physics* **6**, 587-592 (1973), DOI `10.1088/0022-3727/6/5/315`.

The publicly archived six-page PDF was acquired reproducibly in GitHub Actions run `29620068138` and validated against title, author, experimental-method, and result markers.

```text
SHA-256: 3f6a2a39b2047d3d00c375a7441068ba88712429719b5826318876230bf46781
Size:    2,232,984 bytes
Pages:   6
ETag:    "df0e24879acf099a58d419de47b82311"
```

The PDF and extracted full text were deleted before artifact upload. Only digest and validation metadata were preserved.

## Why this source is materially stronger than the existing bridge proxies

Greenough and Palmer report the first thermal-expansion measurement on **single-crystal** CdTe rather than hot-pressed or generic polycrystalline material. Their samples were:

- grown by a modified Bridgman method;
- plates with large `(110)` faces;
- orientation-checked by Laue x-ray;
- reported free of visible strain and twinning;
- constrained to a maximum possible deviation from equiatomic composition of about `0.01%`.

This removes the morphology-transfer objection that limits Browder and Ballard as an execution source.

## Thermal-expansion measurement

The linear expansion coefficient was measured along `[100]` with a strain gauge, comparing the CdTe sample against Spectrosil B quartz.

Reported controls and uncertainties:

- resistance readings every `0.3 K`;
- temperature held to approximately `+/-0.01 K` at each reading;
- five-reading averaging, reducing relative alpha error to about `3%`;
- calibrated gold-iron/chromel thermocouple;
- absolute temperature accuracy approximately `+/-0.25 K`;
- fitted temperature-interval accuracy approximately `+/-0.02 K`.

## Reported physical features

- `alpha(T)` crosses zero at `63.7 K`;
- a sharp anomaly peaks at `79.0 +/- 0.1 K`;
- the anomaly was reproduced in another sample cleaved from a different boule;
- some runs showed hysteresis above and below the anomaly;
- Figure 4 reports `alpha(T)`;
- Figure 5 reports fractional lattice change along `[100]`, referenced to `90 K`.

The paper tentatively attributes the anomaly to an abrupt change in ionicity, but this interpretation is not required for the lattice bridge.

## Gate decision

### Passed

- primary article acquired;
- exact source bytes identified by SHA-256;
- single-crystal morphology accepted;
- sample orientation and composition provenance accepted;
- measurement uncertainty and temperature metrology identified.

### Still open

The numerical expansion data are plotted rather than tabulated. Therefore acquisition does not by itself select an execution lattice constant.

The remaining bounded task is:

1. digitize Figure 4 or Figure 5;
2. use the other figure as an integral consistency check;
3. propagate the reported approximately `3%` relative alpha uncertainty and temperature uncertainty to the Williams room-temperature absolute lattice anchor;
4. test whether the narrow `79 K` anomaly has a material effect on the `0-293 K` integrated lattice change.

Until those steps pass, `execution_lattice_constant_angstrom` must remain unset and A0 execution readiness must remain false.

## Program consequence

The A0 blocker has narrowed from **missing primary single-crystal evidence** to **one graphical-data recovery and uncertainty-propagation task**. No proxy model expansion or first-principles calculation is justified before that task is completed.
