# Collaboration-ready paired HgCdTe gap protocol

Date: 2026-07-19  
Controlling issue: #141

## Question

Can the validated `2 x 2 x 2` local identifiability design be converted into a fail-closed acquisition contract that a multi-laboratory collaboration can execute without confusing nominal process labels with achieved physical states?

## Core design

```text
2 measured composition levels
x 2 measured carrier-density levels
x 2 measured vacancy-proxy levels
= 8 physical specimens

8 specimens x 2 paired modalities x 2 temperature blocks
= 32 primary gap observations
```

The paired modalities are magneto-optical and absorption-derived gap estimates. Both modalities are applied to the same physical specimen and one co-registered area within each temperature block.

The temperature targets are 6 K and 300 K.

## Controlling model

At one temperature block:

```text
y_MO  = b0 + bx*x_code + error_MO

y_ABS = b0 + bx*x_code
              + b_abs
              + b_carrier*n_code
              - b_vacancy*v_code
              + error_ABS
```

The model is a local identifiability device, not a universal physical correction.

The final composition, carrier, and vacancy codes are computed from measured continuous values. Nominal low/high labels remain planning metadata only.

## Machine contract

The package adds:

- `protocols/hgcdte_paired_gap_acquisition_protocol.md`;
- `data/templates/hgcdte_paired_gap_acquisition_template.json`;
- `tools/audit_hgcdte_paired_gap_acquisition.py`;
- `data/derived/hgcdte_paired_gap_protocol_reference_audit.json`;
- focused tests for planning, completed, and fail-closed cases.

The template contains exactly eight specimen records and 32 primary observation slots.

## Planning-template result

For both temperature blocks, the nominal balanced design has:

```text
observation count             16
parameter count               5
design rank                   5
residual degrees of freedom   11
condition number              2.6180339887
maximum leverage              0.4375
carrier-vacancy correlation   0.0
```

The template passes the declared planning contract.

## Physical-state gates

### Composition

```text
planning targets       x = 0.24 and x = 0.30
target sigma_x         <= 0.0010
hard maximum sigma_x   <= 0.0015
```

The composition method must be independent of the optical edge.

### Carrier

The carrier factor uses `log10(|carrier density|)` measured at each temperature block. All eight core specimens must retain one carrier polarity within a block.

The achieved carrier low/high levels must be separated by at least three combined standard uncertainties.

### Vacancy

The vacancy factor requires a quantitative, calibrated, uncertainty-bearing vacancy-sensitive observable. Process history or carrier density alone is not a vacancy measurement.

The achieved vacancy low/high levels must be separated by at least three combined standard uncertainties.

### Aliasing

```text
abs(correlation(carrier_code, vacancy_code)) <= 0.5
```

A failed correlation gate blocks separate carrier and vacancy interpretation.

## Pairing and provenance gates

The completed package requires:

- both modalities on every specimen at every temperature;
- one co-registered measurement-area ID for each paired observation;
- no irreversible processing between paired modalities;
- pre/post state-drift check no larger than the predeclared limit;
- at least two technical replicates, with three as the target;
- measured sample temperature and uncertainty;
- native raw-data URI, format, and SHA-256;
- calibration IDs;
- extraction method and software commit;
- covariance and complete analysis-record URIs;
- same-specimen state assignment or a witness ID plus transfer-uncertainty record.

## Fail-closed tests

The focused test suite verifies:

- complete planning inventory and factorial states;
- deterministic planning diagnostics;
- a synthetic completed package that passes every gate;
- missing paired observations;
- composition uncertainty above the hard maximum;
- mixed carrier polarity;
- processing between paired modalities;
- carrier-vacancy aliasing;
- invalid raw-data hashes;
- unequal co-registered measurement areas;
- witness assignment without transfer uncertainty.

## Decision

Authorized:

- use the protocol and template as the collaboration handoff for acquiring observation-class-controlled HgCdTe evidence;
- require measured continuous covariates rather than nominal process labels;
- require one carrier polarity within the core local model;
- reject carrier/vacancy separation when achieved factors are correlated above the declared gate;
- fit the local model separately across the complete absorption-edge candidate ensemble;
- report coefficient envelopes and leave-one-specimen-out stability;
- add external holdout and cross-laboratory tiers after the eight-specimen core is complete.

Not authorized:

- treat a planning label as a measured carrier or vacancy state;
- use anneal history as a vacancy proxy without a calibrated measurement;
- mix n-type and p-type specimens in the five-parameter core;
- select one absorption candidate as a corrected material gap;
- interpret a failed design by deleting or relabeling specimens after inspection;
- claim external transfer from the eight-specimen single-lineage core;
- treat the local five-parameter model as physically complete.

## Consequence

The next material-law advance is now experimentally specified rather than computationally open-ended. Further unpaired historical tables cannot replace this acquisition. The highest-value external action is to identify collaborators and a pre-screening pool capable of satisfying the composition, state-separation, correlation, pairing, and provenance gates.
