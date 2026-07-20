# Paired HgCdTe gap-acquisition protocol

Version: 1.0  
Protocol ID: `hgcdte_paired_gap_2x2x2_v1`  
Controlling issue: #141

## 1. Purpose

This protocol converts the validated local HgCdTe identifiability design into an executable multi-laboratory acquisition plan.

The experiment is designed to separate five terms at each temperature block:

```text
latent intercept
latent composition slope
absorption-class offset
carrier-state contribution
vacancy-state contribution
```

It is not a new band-gap equation. It does not assume that an absorption edge is a direct, method-free observation of the latent material gap.

## 2. Core design

The audit-grade core contains eight physical specimens:

```text
2 composition levels
x 2 carrier-density levels
x 2 vacancy-proxy levels
= 8 specimens
```

Each specimen receives both measurement modalities at both temperature blocks:

```text
8 specimens
x 2 modalities
x 2 temperatures
= 32 primary gap observations
```

The temperature blocks are:

```text
low-temperature block   target 6.0 K
room-temperature block  target 300.0 K
```

The same specimen IDs are retained across both blocks. The same registered area is used for the paired absorption and magneto-optical measurements within a temperature block.

## 3. Claim boundary

A completed audit-grade package supports a local five-parameter observation-model analysis within the achieved specimen states.

It does not:

- prove that the five-term model is physically complete;
- define a universal material-gap equation;
- define a universal absorption correction;
- make one vacancy-sensitive method universal;
- establish cross-laboratory transfer;
- turn nominal processing labels into measured physical states.

## 4. Collaboration roles

The data package identifies one accountable owner for each role:

1. material provider;
2. composition and thickness metrology laboratory;
3. Hall and defect-state laboratory;
4. absorption laboratory;
5. magneto-optical laboratory;
6. analysis owner;
7. long-term data archive.

One organization may hold multiple roles. Every role still receives a distinct identifier in the machine-readable package.

## 5. Specimen-state realization

### 5.1 Planning labels are not analysis covariates

The nominal low/high labels define the acquisition matrix only. The final analysis uses measured continuous values.

A process label such as "Hg-rich anneal" or "low carrier" is not sufficient evidence of an achieved state.

### 5.2 Composition levels

The planning targets are:

```text
composition low   x = 0.24
composition high  x = 0.30
```

The coded composition used in the local model is:

```text
x_code = (x_measured - 0.27) / 0.03
```

Required composition uncertainty:

```text
target sigma_x        <= 0.0010
hard maximum sigma_x <= 0.0015
```

The composition method must be independent of the optical edge being studied. WDS or calibrated electron microprobe analysis is a suitable primary route. A second method may be retained as a consistency check, but it does not replace a quantified primary uncertainty.

### 5.3 Carrier factor

The carrier factor uses `log10(|carrier density|)` measured at each temperature block.

All eight core specimens must have the same carrier polarity within a temperature block. A mixture of n-type and p-type specimens introduces a categorical physical change that is not represented by the five-parameter model.

The achieved low and high carrier groups must be separated by at least three combined standard uncertainties.

Preferred state realization uses a carrier-control mechanism that is as independent as practicable from the vacancy-control mechanism. Acceptable approaches include controlled doping, reversible electrostatic control, or selection from a pre-screened material pool. The protocol does not prescribe one universal fabrication route.

### 5.4 Vacancy factor

The vacancy factor must be a quantitative vacancy-sensitive observable with:

- numerical value;
- uncertainty;
- units;
- method identifier;
- calibration identifier;
- defined orientation, with larger coded value corresponding to the declared high-vacancy state.

Positron annihilation spectroscopy is one possible direct-sensitive method. A different calibrated proxy is acceptable when its mechanism, sensitivity, and transfer uncertainty are documented.

Anneal history, carrier type, resistance, or a verbal process label alone is not an acceptable vacancy proxy.

The achieved low and high vacancy groups must be separated by at least three combined standard uncertainties.

### 5.5 Carrier-vacancy aliasing gate

Within each temperature block, the achieved carrier and vacancy covariates must satisfy:

```text
abs(correlation) <= 0.5
```

If this gate fails, carrier and vacancy contributions remain operationally aliased. The package may still be scientifically useful, but it is not audit-grade for the declared five-term decomposition.

### 5.6 Pre-screening pool

The eight-specimen core should normally be selected from a larger pre-screening pool.

Recommended sequence:

1. prepare or obtain candidate coupons at both composition levels;
2. measure composition, carrier state, and vacancy proxy;
3. select the eight coupons that best span the full factorial while minimizing carrier-vacancy correlation;
4. freeze specimen IDs and processing histories;
5. begin paired optical acquisition only after the achieved design passes the preliminary audit.

Do not force a failed material pool into the nominal factorial by relabeling specimens.

## 6. Specimen lineage and handling

Each specimen record includes:

- wafer ID;
- coupon ID;
- growth method and run ID;
- composition location on the parent wafer;
- complete processing history;
- anneal history;
- passivation state;
- contact state;
- storage environment and duration;
- handling events between laboratories;
- thickness and lateral-uniformity record.

No irreversible processing is allowed between the paired absorption and magneto-optical measurements within a temperature block.

If contacts, coatings, or mounting changes are unavoidable, the pairing is broken unless the change is explicitly modeled and independently validated.

## 7. State assignment: same specimen or witness

Carrier and vacancy measurements should be performed on the same physical coupon whenever geometry and instrumentation permit.

A witness coupon is acceptable only when the package records:

- witness specimen ID;
- parent-wafer and spatial relationship;
- assignment basis;
- transfer uncertainty record;
- evidence that the witness and optical coupon share the relevant processing history.

The transfer uncertainty must be propagated into the state covariance. A witness assignment without quantified transfer uncertainty fails closed.

## 8. Temperature blocks

### 8.1 Low-temperature block

```text
target temperature                 6.0 K
maximum absolute deviation         0.2 K
maximum reported temperature sigma 0.1 K
```

### 8.2 Room-temperature block

```text
target temperature                 300.0 K
maximum absolute deviation         0.5 K
maximum reported temperature sigma 0.2 K
```

The measured sample temperature and uncertainty are stored for every observation. Controller setpoint alone is insufficient.

### 8.3 Stability sequence

Recommended sequence:

```text
300 K baseline state metrology
low-temperature paired acquisition
300 K paired acquisition
300 K state-metrology repeat
```

A different sequence is acceptable when predeclared. The final state check remains required.

The default state-drift gate is:

```text
pre/post Hall fractional change <= 0.10
```

A laboratory may adopt a tighter gate before acquisition. It may not loosen the gate after seeing the result.

## 9. Measurement order and technical replication

Within each temperature block, the 16 primary observation slots are randomized. The machine template contains a deterministic planning order that may be replaced by a predeclared laboratory-specific randomization before data collection.

Technical replicate target:

```text
target     3 native acquisitions per primary observation
hard floor 2 native acquisitions per primary observation
```

Technical repeats estimate repeatability. They do not increase the count of independent physical specimens.

Reference or calibration measurements should be interleaved at a declared cadence. The cadence and any drift correction are fixed before edge extraction.

## 10. Co-registered paired areas

For each specimen and temperature block, both modalities use one declared `measurement_area_id`.

The package records:

- area coordinates or fiducial reference;
- beam or spot dimensions;
- orientation;
- local thickness;
- local composition information when available.

If the two modalities cannot interrogate the same area, the spatial transfer uncertainty must be added explicitly. The core template treats unequal area IDs as a failed pairing.

## 11. Absorption acquisition

The absorption package preserves native transmission, reflection, or ellipsometric data sufficient to reconstruct the reported absorption spectrum.

Required records include:

- instrument and detector IDs;
- spectral axis calibration;
- intensity or ellipsometric calibration;
- background and reference records;
- sample thickness and uncertainty;
- optical geometry, angle, and polarization;
- spectral resolution;
- temperature record;
- raw native file and SHA-256;
- processing code commit;
- fit window and exclusions;
- extraction covariance.

The spectral range must bracket the onset and extend into a stable higher-absorption region. Boundary-limited fits remain boundary-limited and are not promoted as identified edges.

### 11.1 Complete edge ensemble

The absorption analysis returns every admissible candidate under the repository contract, including:

- free and fixed fractional-power fits;
- source-domain Kane-region candidates where valid;
- fixed operational thresholds;
- exclusions and boundary flags;
- model-family, threshold, and combined envelopes;
- coordinate and calibration sensitivity.

No single candidate is selected as a corrected or production edge.

For the five-parameter experiment, the model is fitted separately for every admissible absorption candidate. The reported carrier, vacancy, and class-offset terms are therefore coefficient envelopes across observation definitions.

## 12. Magneto-optical acquisition

The magneto-optical package preserves the complete field- and energy-dependent native data used to infer the calibrated gap estimate.

Required records include:

- instrument and magnet IDs;
- magnetic-field calibration and polarity;
- field sweep sequence and direction;
- spectral calibration and resolution;
- temperature record;
- polarization and optical geometry;
- transition assignments;
- model family and parameter conventions;
- fit window and exclusions;
- fit covariance and residual diagnostics;
- raw native file and SHA-256;
- processing code commit.

The field range and transition model must be sufficient for the declared fit and must be fixed before comparing material-gap equations.

The magneto-optical estimate retains residual method uncertainty. It is not labeled a method-free latent gap.

## 13. Machine-readable data package

The repository template is:

```text
data/templates/hgcdte_paired_gap_acquisition_template.json
```

The audit tool is:

```text
tools/audit_hgcdte_paired_gap_acquisition.py
```

The template contains:

- eight specimen records;
- two temperature-state records per specimen;
- 32 primary observation slots;
- nominal planning codes;
- achieved-state fields;
- calibration and covariance fields;
- technical-replicate targets;
- measurement order;
- raw-data provenance.

A completed package changes:

```text
status: planning_template -> completed_package
observation status: planned -> complete
```

All native-data hashes use lowercase SHA-256.

## 14. Achieved-covariate coding

At each temperature block, carrier and vacancy codes are constructed from the achieved group means.

For a measured factor `z`:

```text
z_center = (mean_high + mean_low) / 2
z_scale  = (mean_high - mean_low) / 2
z_code   = (z - z_center) / z_scale
```

Carrier coding uses:

```text
z = log10(|carrier density|)
```

Vacancy coding uses the declared calibrated vacancy-proxy value.

The final design matrix therefore reflects the actual specimen states rather than the nominal labels.

## 15. Local analysis model

For one temperature block:

```text
y_MO  = b0 + bx*x_code + error_MO

y_ABS = b0 + bx*x_code
              + b_abs
              + b_carrier*n_code
              - b_vacancy*v_code
              + error_ABS
```

The minus sign on the vacancy term is a declared coefficient convention. It does not assume the physical direction of the effect.

The paired difference is:

```text
y_ABS - y_MO
  = b_abs + b_carrier*n_code - b_vacancy*v_code + paired_error
```

The fit uses measured covariates and the complete measurement covariance. Nominal low/high labels are never substituted for missing physical measurements.

## 16. Required diagnostics

Per temperature block:

```text
observation count             = 16
parameter count               = 5
design rank                   = 5
residual degrees of freedom   >= 8
condition number              <= 5
maximum leverage              <= 0.5
carrier separation            >= 3 combined sigma
vacancy separation            >= 3 combined sigma
abs(carrier-vacancy corr.)    <= 0.5
single carrier polarity       required
processing between modalities forbidden
```

For the nominal balanced factorial, the expected diagnostics are:

```text
rank                 5/5
residual DOF         11
condition number     2.6180339887
maximum leverage     0.4375
```

## 17. Leave-one-specimen-out stability

The analysis repeats the complete fit eight times per temperature and observation definition, withholding both modalities for one physical specimen on each fold.

Required reporting includes:

- coefficient range across folds;
- predicted paired residual for the held-out specimen;
- rank and condition number for every training fold;
- influence and leverage by specimen;
- sign stability of carrier and vacancy terms;
- absorption-model dependence of every coefficient.

A nominal full-data coefficient is not treated as identified when its sign or magnitude is dominated by one specimen.

## 18. Stop rules

Stop the audit-grade analysis and report the failure mode when any of the following occurs:

- fewer than eight unique physical specimens;
- an incomplete factorial state;
- missing paired modality;
- unequal co-registered area IDs within a pair;
- composition uncertainty above `0.0015`;
- mixed carrier polarity in a temperature block;
- carrier or vacancy separation below three combined sigma;
- absolute carrier-vacancy correlation above `0.5`;
- rank below 5;
- condition number above 5;
- maximum leverage above 0.5;
- processing between paired modalities;
- state drift above the predeclared limit;
- missing native data, calibration, SHA-256, method, software commit, or covariance;
- fewer than two technical replicates;
- temperature outside the declared block gate.

A failed gate does not justify changing the model, deleting a specimen, or relabeling a state after inspection.

## 19. Strengthening tiers

### Tier 1: core audit-grade design

Eight specimens, one laboratory lineage, two modalities, and two temperature blocks.

### Tier 2: external holdout

Add at least one new specimen per composition that was not used to define carrier or vacancy group centers.

### Tier 3: cross-laboratory transfer

Repeat the protocol with independently grown material and at least one independently calibrated measurement laboratory.

Only Tier 3 can begin to support cross-source transfer claims.

## 20. Collaboration acceptance checklist

Before specimen shipment:

- [ ] all seven collaboration roles assigned;
- [ ] composition and state pre-screening complete;
- [ ] eight specimens selected without relabeling;
- [ ] preliminary audit passes rank, conditioning, leverage, separation, and correlation gates;
- [ ] specimen lineage records frozen;
- [ ] measurement areas and fiducials defined;
- [ ] temperature sequence fixed;
- [ ] measurement order randomized and frozen;
- [ ] calibration cadence fixed;
- [ ] native formats and archive paths agreed;
- [ ] covariance and transfer-uncertainty formats agreed;
- [ ] absorption candidate ensemble fixed;
- [ ] magneto-optical model conventions fixed;
- [ ] stop rules accepted by every laboratory.

Before analysis release:

- [ ] 32 primary observations complete;
- [ ] all native files hash-bound;
- [ ] all calibration IDs resolvable;
- [ ] all technical replicate gates pass;
- [ ] same-area pairing verified;
- [ ] pre/post state drift passes;
- [ ] completed audit reports audit-grade status;
- [ ] leave-one-specimen-out report complete;
- [ ] claim boundary included in every result summary.
