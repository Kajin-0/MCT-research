# Paired HgCdTe collaboration feasibility and pilot handoff

Version: 1.0  
Feasibility ID: `hgcdte_paired_gap_feasibility_v1`  
Parent protocol: `hgcdte_paired_gap_2x2x2_v1`  
Controlling issue: #161

## 1. Purpose

This document converts the paired HgCdTe gap-acquisition protocol into an external collaboration readiness process.

It answers three different questions:

1. Can the proposed organizations perform and document the required work?
2. Can the complete specimen and data flow be demonstrated on a bounded logistics pilot?
3. Has a measured pre-screening pool produced an audit-grade eight-specimen design?

These questions are deliberately separated. A laboratory may be technically capable while the collaboration is not ready. A logistics pilot may succeed while the five-parameter experiment remains scientifically blocked.

## 2. Readiness states

```text
not_ready
capability_review_complete
logistics_pilot_ready
logistics_pilot_complete
prescreening_ready
full_experiment_ready
```

The repository audit calculates the highest achieved state. No state is assigned from verbal assurances alone.

## 3. Collaboration roles

The package requires accountable ownership for:

```text
material provider
composition and thickness metrology
Hall and carrier-state metrology
vacancy-sensitive metrology
absorption acquisition
magneto-optical acquisition
analysis
long-term data archive
```

One organization may hold multiple roles. Each role still receives a separate role record so responsibility, evidence, restrictions, and unresolved assumptions remain explicit.

## 4. Capability evidence

For every role, record:

- accountable owner, organization, and contact identifiers;
- status: `unknown`, `conditional`, `confirmed`, or `blocked`;
- evidence records or prior demonstrations;
- accepted specimen dimensions, thickness, substrate, mounting, and surface constraints;
- any destructive, contacting, coating, annealing, polishing, or state-altering step;
- calibration or process plan;
- native-data and metadata formats;
- processing-code and covariance availability when applicable;
- throughput and turnaround;
- shipping, storage, chain-of-custody, and environmental constraints;
- raw-data, publication, intellectual-property, and confidentiality restrictions;
- cost-estimate status;
- every unresolved assumption.

A confirmed role must contain complete documentation and evidence. A conditional or blocked role must name the unresolved condition.

## 5. Cross-cutting pilot gates

The logistics pilot cannot begin until all thirteen gates are confirmed with evidence:

```text
two composition-level specimens are available
independent composition capability reaches sigma_x <= 0.0015
sample temperature capability covers 6 K and 300 K
sample-temperature uncertainty meets the parent protocol
carrier state is quantitative and uncertainty-bearing
vacancy proxy is quantitative and uncertainty-bearing
paired areas can be co-registered
no irreversible processing occurs between paired modalities
native data and SHA-256 records will be released
calibration and extraction covariance will be released
at least two native technical repeats are available
pre/post state drift will be measured
data and publication rights are compatible
```

A gate marked confirmed without evidence fails closed.

## 6. Stage 0: capability review

No specimens move during Stage 0.

The review should resolve:

1. specimen geometry compatibility across all laboratories;
2. whether Hall contacts, coatings, mounting, or polishing alter the optical state;
3. whether the same registered area can be used by both optical modalities;
4. whether the reported temperature is the sample temperature rather than controller setpoint;
5. whether native files, calibration files, software versions, residuals, and covariance can be released;
6. whether data-rights or publication restrictions conflict with the repository provenance contract;
7. shipping order, storage environment, custody records, and damage inspection;
8. realistic throughput, turnaround, and cost status;
9. the owner of final package assembly and long-term archive.

A capability review may be complete while still containing conditional or blocked roles. Completion means the constraints are known, not that execution is authorized.

## 7. Stage 1: logistics pilot

### 7.1 Design

```text
2 physical specimens
x 2 paired modalities
x 2 temperature blocks
= 8 primary observations
```

The two specimens span the two composition levels. They use one achieved carrier state and one achieved vacancy state.

### 7.2 What the pilot validates

- chain of custody and specimen survivability;
- mounting and orientation repeatability;
- registered-area transfer between laboratories;
- sample-temperature control and uncertainty;
- field, spectral, intensity, and thickness calibration transfer;
- native-file delivery, hashing, parsing, and archive ingestion;
- technical repeatability;
- pre/post carrier and vacancy-state stability;
- absence of irreversible processing between paired measurements;
- analysis-code execution on partner-generated native files.

### 7.3 What the pilot cannot establish

The pilot has only one carrier level and one vacancy level. It does not identify:

- a carrier-state coefficient;
- a vacancy-state coefficient;
- carrier-vacancy separation;
- the full local five-parameter model;
- a universal material-gap equation;
- a corrected absorption edge.

A successful pilot changes logistics readiness, not material-law authority.

## 8. Pilot sequence

A predeclared sequence should minimize uncontrolled state change. The default is:

```text
incoming inspection and specimen imaging
300 K composition/thickness and state baseline
low-temperature absorption and magneto-optical acquisition
300 K absorption and magneto-optical acquisition
300 K state-metrology repeat
archive assembly and independent hash verification
```

The optical order may be randomized or reversed when predeclared. Any contact, coating, polishing, anneal, or remounting step is recorded. Irreversible processing between paired modalities fails the pilot.

## 9. Pilot completion gates

The logistics pilot is complete only when:

```text
completed specimens                    = 2
completed primary observations          = 8
minimum native technical repeats       >= 2
same-area pairing                        pass
sample-temperature gates                 pass
native-data transfer                     pass
calibration/covariance transfer          pass
pre/post state-drift gate                pass
irreversible processing detected         false
unresolved pilot failure records         none
```

An incomplete observation or missing native file is not replaced by a derived plot or summary table.

## 10. Stage 2: pre-screening pool

The full experiment is selected from a measured candidate pool.

Before selection, every candidate must have:

- independent composition and uncertainty;
- carrier polarity, density, mobility, and uncertainty;
- quantitative vacancy proxy and uncertainty;
- processing and parent-wafer lineage;
- geometry compatible with both optical modalities.

The selection algorithm is frozen before choosing the final eight. The goal is to obtain:

```text
2 composition levels
x 2 achieved carrier levels
x 2 achieved vacancy levels
= 8 selected specimens
```

The final selection must satisfy, at both temperature blocks:

```text
maximum sigma_x                         <= 0.0015
one carrier polarity                    required
carrier low/high separation             >= 3 combined sigma
vacancy low/high separation             >= 3 combined sigma
abs(carrier-vacancy correlation)        <= 0.5
specimen IDs and processing histories   frozen
```

A nominal process matrix that fails these measured gates is not relabeled into compliance.

## 11. Stage 3: full experiment

Only `full_experiment_ready` authorizes execution of the parent protocol:

```text
8 specimens
x 2 modalities
x 2 temperature blocks
= 32 primary observations
```

The complete requirements in `protocols/hgcdte_paired_gap_acquisition_protocol.md` remain controlling. This handoff adds feasibility and staging; it does not relax any scientific gate.

## 12. Partner response format

Partners should return the machine-readable template plus supporting evidence identifiers. Sensitive commercial details may be stored outside the public scientific record when the repository retains:

- a stable evidence identifier;
- the responsible owner;
- status and date;
- the exact capability or restriction supported;
- whether independent verification is available.

The audit does not require publication of confidential prices or contacts. It does require an explicit status and traceable evidence.

## 13. Go/no-go rules

### Capability-review no-go

- any required role remains unknown;
- geometry compatibility is unresolved;
- state-altering steps are undeclared;
- raw-data or covariance release is refused;
- data or publication rights conflict with provenance requirements.

### Logistics-pilot no-go

- any role or pilot gate is conditional or blocked;
- same-area registration is unavailable;
- only controller setpoint, not sample temperature, is reported;
- technical repeats are fewer than two;
- irreversible processing is required between paired modalities.

### Full-experiment no-go

- the logistics pilot is incomplete;
- the pre-screening plan is not frozen;
- fewer than eight specimens pass the measured design gates;
- composition uncertainty exceeds `0.0015`;
- carrier polarity changes within a temperature block;
- carrier or vacancy separation is below three combined sigma;
- carrier-vacancy correlation exceeds `0.5` in magnitude.

## 14. Repository artifacts

```text
data/templates/hgcdte_paired_gap_feasibility_template.json
tools/audit_hgcdte_paired_gap_feasibility.py
data/derived/hgcdte_paired_gap_feasibility_reference_audit.json
tests/test_hgcdte_paired_gap_feasibility.py
```

The empty planning template is expected to audit as `not_ready`. A partner package is promoted only by changing documented statuses and adding traceable evidence; the audit logic and scientific thresholds remain fixed.
