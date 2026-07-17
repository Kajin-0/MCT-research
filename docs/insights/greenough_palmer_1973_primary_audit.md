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

## Sample quality and measurement

Greenough and Palmer report the first thermal-expansion measurement on **single-crystal** CdTe rather than hot-pressed or generic polycrystalline material. Their samples were:

- grown by a modified Bridgman method;
- plates with large `(110)` faces;
- orientation-checked by Laue x-ray;
- reported free of visible strain and twinning;
- constrained to a maximum possible deviation from equiatomic composition of about `0.01%`.

The linear expansion coefficient was measured along `[100]` with a strain gauge, comparing the CdTe sample against Spectrosil B quartz.

Reported controls and uncertainties:

- resistance readings every `0.3 K`;
- temperature held to approximately `+/-0.01 K` at each reading;
- five-reading averaging, reducing relative alpha error to about `3%`;
- calibrated gold-iron/chromel thermocouple;
- absolute temperature accuracy approximately `+/-0.25 K`;
- fitted temperature-interval accuracy approximately `+/-0.02 K`.

## Published thermal-expansion scope

A one-day diagnostic rendering in workflow run `29620272465` was used to inspect the actual printed axes before attempting digitization.

The result corrects the earlier acquisition-stage assumption:

- Figure 4 publishes `alpha(T)` only from `50 K` to `100 K`;
- Figure 5 publishes fractional lattice change only from approximately `60 K` to `91 K`, referenced to `90 K`;
- no numerical table is printed;
- no graphical `100-293 K` thermal-expansion curve is printed.

The article states broad experimental coverage, but the printed thermal-expansion evidence is restricted to the low-temperature anomaly region. The source therefore cannot supply the missing `90-293 K` integral from the article as published.

## Low-temperature physical features

- `alpha(T)` crosses zero at `63.7 K`;
- a sharp anomaly peaks at `79.0 +/- 0.1 K`;
- the anomaly was reproduced in another sample cleaved from a different boule;
- some runs showed hysteresis above and below the anomaly.

The paper tentatively attributes the anomaly to an abrupt change in ionicity. That interpretation is not required for the provenance decision.

## Gate decision

### Passed

- primary article acquired and hashed;
- single-crystal morphology accepted;
- sample orientation and composition provenance accepted;
- measurement uncertainty and temperature metrology identified;
- Greenough-Palmer accepted as the primary source for the `50-100 K` single-crystal anomaly.

### Failed as the high-temperature bridge

Greenough-Palmer does **not** expose the required `90-293 K` numerical or graphical data. Digitizing Figures 4 and 5 would recover only low-temperature behavior and cannot close the controlling high-temperature bridge.

The temporary figure-rendering workflow and script were therefore removed. Continuing to digitize this paper now would be a depth-first detour with low marginal value.

### Remaining controlling task

Acquire and hash either:

1. Bagot, Granger, and Rolland 1993, DOI `10.1002/pssb.2221770205`, if it publishes the required full-range CdTe data; or
2. another primary CdTe source with numerical or graphical expansion data spanning approximately `90-293 K` and adequate morphology/uncertainty provenance.

Then propagate that source to the Williams `293.15 K` absolute lattice anchor. Return to the Greenough-Palmer anomaly only if the final uncertainty becomes sensitive to the low-temperature integral.

## Program consequence

The source-acquisition effort produced a useful negative result: Greenough-Palmer resolves morphology and the low-temperature anomaly, but it was incorrectly prioritized as the missing high-temperature bridge. The A0 blocker remains primary `90-293 K` data, with Bagot now the leading acquisition target.
