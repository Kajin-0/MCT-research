# Evidence verification and reproducibility

Run from the MCT research root:

```sh
python3 research/programs/microscopic_bandgap/public_optical_intake_2026-10-15/verify_intake.py
```

This is a small offline consistency/preservation check. It validates source IDs,
URLs, the eight-query ledger, all five candidate refusals, zero accepted raw
datasets/analyses, the UNSENT draft marker, local links and the allowed edit
scope. Twenty frozen source/evidence files, AGENTS included, are hash-checked.
The entire old SUCCESSOR_HANDOFF content is checked for byte-preservation after
removing only this phase's added section. Dirty DFT's tracked diff and stock QE
hash must match the prior accepted manifest. It performs no native run, spectrum
fit, synthetic proof, download or contact. See [verification.json](verification.json).

Independent primary cross-checks used in the actual web intake:

- Teppe publisher's attachment index was followed to the six-page PDF; its
  captions/notes distinguish S5's plotted 77 K series from low-T field maps and
  identify the Hall plot as a figure. Data availability/correspondence were
  checked in the article. No table of raw per-field scans was recovered.
- Orlita publisher's supplement was independently recovered from its article
  link and compared with author-manuscript sample/method text. It is not a
  calibrated assay/raw-spectrum archive.
- Institutional author bibliography independently supplies the HAL article
  identifiers; inaccessible HAL/API inventories were retained as unknown.
  Public repository exclusions were based on material/observable metadata;
  their numerical archives were not downloaded or interpreted.

Remote files were inspected using native web PDF/HTML extraction, not stored
or redistributed. PDF screenshots returned textual references in this tool;
no independent visual/embedded-object/binary inspection or file checksum is
claimed. Publisher attachment descriptions and readable contents support the
classification **no raw bundle located**, not an exhaustive theorem about all
PDF objects or external/unindexed files. Publication, audit and access dates
are separated in [sources.json](sources.json); search-engine relative ages do
not substitute for primary publication dates. No network check is repeated by
the offline verifier, and mutable web pages are not asserted immutable.

PASS of this verifier is **not** PASS of data intake, calibration, permission,
material validation, scientific model eligibility or physical x_c. The intake
decision is NO-GO. Missing calibration/assay/line-adapter errors remain unknown.
