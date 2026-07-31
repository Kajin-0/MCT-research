# R04/R05 partner contact packets

**Controlling issue:** #398  
**Predecessor:** #395 and PR #397  
**Campaign state:** `CONTACT_READY_NOT_SENT`  
**Source verification date:** 2026-07-31

## Use boundary

These packets are prepared but have not been sent. Before outbound contact:

1. select and verify the sender identity and organization;
2. recheck the recipient route;
3. remove any request that the sender is not prepared to support;
4. decide whether the work will be open/publication-oriented or proprietary;
5. record the sent timestamp only after successful transmission.

Preparing a packet is not evidence access, facility acceptance, a measurement commitment, or R05 reactivation.

## Frozen scientific request

The campaign seeks one real route to a matched evidence package containing:

```text
near-critical HgCdTe specimen state
local mass or convertible composition covariance
measured spatial transfer function
local low-energy spectroscopy
measured energy-resolution kernel
same-specimen or quantitatively justified same-population linkage
raw data and calibration metadata
```

The immediate request is feasibility and archive inventory. It is not a request for endorsement of the random-mass interpretation.

---

## Packet P1 — near-critical HgCdTe specimen and archive

**Recipient:** Dr. Tobias Kießling  
**Organization:** University of Würzburg, Experimental Physics III / Institute for Topological Insulators  
**Verified public route:** `tobias.kiessling@uni-wuerzburg.de`  
**Basis:** corresponding author and group lead for the 2025 HgCdTe quantum-well phase-diagram study

### Subject

Archived HgCdTe quantum-well material and local-characterization feasibility

### Draft

Dear Dr. Kießling,

I am evaluating whether a near-critical Hg1-xCdxTe specimen can support a quantitative comparison between a spatially correlated local-gap model and a matched scalar local-gap mixture. Your 2025 Physical Review Materials study is the strongest public source I found for a controlled near-critical HgCdTe quantum-well series with structural, magneto-optical, and k.p characterization.

I am not asking you to endorse that model. I am trying to determine whether a defensible matched dataset could be assembled from retained material or archived records.

Could you indicate whether any of the following are available for the samples in that study, or for closely related sister chips?

- persistent specimen identifiers and sample-level composition and thickness calibration;
- raw XRD, XRR, magneto-optical, and related calibration records;
- retained wafers or sister chips suitable for external cryogenic STM/STS;
- local Cd-composition maps, EDX spectrum images, or other spatially resolved chemical data;
- a documented basis for treating sister chips or adjacent wafer regions as exchangeable;
- surface-preparation constraints that would affect tunneling spectroscopy.

The key quantities would be a local mass or composition variance, a correlation length after instrument-response correction, and a low-energy spectroscopy record from the same specimen population with a measured energy-resolution kernel. A wafer-average composition tolerance would not be used as a local fluctuation variance.

A brief inventory or referral to the appropriate growth, microscopy, or spectroscopy colleague would be sufficient at this stage. Any unpublished information would remain private unless an explicit data-sharing or collaboration arrangement were established.

Best regards,

[Sender identity]
[Organization]
[Contact information]

### Minimum useful response

At least one of:

- retained sample or sister-chip availability;
- identifiable archive with raw structural or spectroscopy records;
- local-composition data availability;
- named internal contact for growth or metrology;
- explicit statement that material or records are no longer available.

### Outcome mapping

```text
archive inventory supplied              -> DATA_ARCHIVE_EXISTS
retained material and measurement path  -> NEW_MEASUREMENT_POSSIBLE
only mean parameters or partial records -> PARTIAL_DATA_ONLY
records/material not retained           -> DATA_NOT_RETAINED
```

### Official sources

- `https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.9.054602`
- `https://www.physik.uni-wuerzburg.de/en/research-groups/kiessling-group/team/dr-tobias-kiessling/`

---

## Packet P2 — ORNL CNMS STM/STS feasibility

**Primary recipients:** Dr. An-Ping Li and Dr. Saban Hus  
**Verified public routes:** `APLI@ORNL.GOV`, `HUSSM@ORNL.GOV`  
**Organization:** Center for Nanophase Materials Sciences, Oak Ridge National Laboratory

### Subject

Feasibility of cryogenic HgCdTe STM/STS with registered composition metrology

### Draft

Dear Dr. Li and Dr. Hus,

I am screening user-facility routes for a bounded proof-of-concept measurement on near-critical HgCdTe. The scientific question requires spatially registered low-energy tunneling spectroscopy and local composition or gap covariance from the same specimen or a quantitatively justified sister specimen.

Before preparing a proposal, could you advise on the following feasibility points?

1. Does CNMS accept Hg-containing HgCdTe chips under its current safety and contamination controls?
2. Is there a viable UHV preparation route for HgCdTe, such as controlled cleavage, etching, sputter/anneal treatment, or vacuum transfer, without destroying the relevant surface electronic structure?
3. Can an STM/STS system provide spatially indexed topography and dI/dV data with an experimentally characterized effective energy-resolution kernel near the exploratory 1-2 meV scale?
4. Can raw spectroscopy, topography, calibration, and instrument-setting files be exported?
5. Could the STM workflow be coordinated with a registered adjacent-region or sister-chip STEM-EDX, APT, or other composition-mapping measurement through CNMS?
6. Would a limited Rapid Access proposal be an appropriate route for an initial material-acceptance and surface-preparation feasibility test?

The initial experiment would not claim a random-mass effect. Its decision criterion is whether local composition variance and correlation length can be estimated after spatial-transfer correction and whether the measured spectroscopy kernel preserves a predeclared difference between two matched models.

A written feasibility response identifying suitable instruments, staff contacts, and any sample restrictions would be sufficient for the current gate.

Best regards,

[Sender identity]
[Organization]
[Contact information]

### Minimum useful response

- written HgCdTe material-acceptance statement;
- identified STM instrument and preparation route;
- expected data export and calibration availability;
- recommendation of Rapid Access, General User, proprietary, or infeasible route;
- identified complementary microscopy contact.

### Outcome mapping

```text
specific feasible experiment and access route -> NEW_MEASUREMENT_POSSIBLE
some capabilities but decisive gap remains    -> PARTIAL_DATA_ONLY
HgCdTe not accepted                           -> MATERIAL_NOT_ACCEPTED
registered same-population workflow impossible -> SAME_POPULATION_INFEASIBLE
```

### Current proposal information

The official CNMS pages state that General User calls occur in May and October. The audited page did not yet post the exact fall 2026 deadline. CNMS also describes off-cycle Rapid Access proposals for limited, time-sensitive, proof-of-concept work.

### Official sources

- `https://www.ornl.gov/group/scanning-tunneling-microscopy`
- `https://www.ornl.gov/group/scanning-tunneling-microscopy/staff`
- `https://www.ornl.gov/content/4-probe-scanning-tunneling-microscopy`
- `https://www.ornl.gov/facility/cnms/for-users/proposal-types`
- `https://www.ornl.gov/facility/cnms/for-users/write-and-submit-proposal`

---

## Packet P3 — Argonne CNM cryogenic STM/STS feasibility

**Scientific contacts:** Nathan Guisinger and Jeffrey Guest  
**Organization:** Center for Nanoscale Materials, Argonne National Laboratory  
**Verified route:** CNM scientific-contact page and User Portal; the public email addresses are Cloudflare-protected and are not reproduced in the campaign record

### Subject

CNM feasibility inquiry: HgCdTe cryogenic STS and measured instrument kernels

### Draft

Dear Dr. Guisinger and Dr. Guest,

I am evaluating a CNM user proposal for a near-critical HgCdTe proof-of-concept experiment. CNM publicly lists UHV STM, STS, cryo-STM, and low-temperature scanning-probe capabilities that appear relevant, but material compatibility and surface preparation are the decisive unknowns.

Could you advise whether CNM could support a workflow with the following requirements?

- acceptance of a small HgCdTe chip under current safety and contamination controls;
- a defensible UHV surface-preparation or transfer route;
- spatially indexed low-energy dI/dV mapping;
- an experimentally measured effective energy-resolution kernel, rather than nominal temperature or modulation settings alone;
- raw topography, spectroscopy, calibration, and metadata export;
- registered complementary composition or chemical mapping on the same chip or a documented sister region.

The goal is to determine whether a local composition or signed-gap covariance and a low-energy DOS observable can be compared against two models using the same one-point mass distribution and the same measurement kernel. The initial work would be a feasibility and identifiability test, not a material-physics claim.

If the project appears feasible, I would appreciate guidance on the appropriate scientific contact and whether the October 30, 2026 General User deadline is the correct route.

Best regards,

[Sender identity]
[Organization]
[Contact information]

### Minimum useful response

- material-acceptance and preparation assessment;
- instrument and staff recommendation;
- expected energy/spatial calibration deliverables;
- proposal-route recommendation;
- complementary composition-metrology path.

### Current proposal information

The official CNM user pages list:

```text
call opens: 2026-10-02
deadline:   2026-10-30 11:59 PM CT
```

### Official sources

- `https://cnm.anl.gov/pages/scientific-contacts`
- `https://cnm.anl.gov/group/Quantum-and-Energy-Materials`
- `https://cnm.anl.gov/pages/user-information`
- `https://cnm.anl.gov/pages/user-quick-start-guide`

---

## Packet P4 — Würzburg HgCdTe growth and retained material routing

**Recipients:** Prof. Karl Brunner and Prof. Grzegorz Karczewski  
**Verified public routes:** `brunner@uni-wuerzburg.de`, `karcz@physik.uni-wuerzburg.de`  
**Use condition:** send after the primary corresponding-author contact responds or explicitly routes the request

### Subject

Retained HgCdTe QW material and local composition metrology

### Draft

Dear Prof. Brunner and Prof. Karczewski,

I was referred to the molecular-beam-epitaxy group while assessing whether retained near-critical Hg1-xCdxTe quantum-well material could support matched local-composition and tunneling-spectroscopy measurements.

The immediate question is inventory, not model interpretation. Could you indicate whether retained parent wafers or sister chips exist for the 2025 HgCdTe quantum-well phase-diagram series or a closely related series, and whether the following records are available?

- sample identifiers and growth logs;
- sample-level Cd composition and thickness calibration;
- wafer-position or sister-chip relationships;
- local chemical maps or raw EDX spectrum images;
- surface caps, preparation history, and constraints for external STM/STS;
- a quantitative basis for treating separate chips as exchangeable.

The data requirement is stricter than nominal composition uniformity: the analysis needs local variance and an identifiable correlation length after instrument-response correction. If local mapping has not been performed, retained material plus a traceable specimen-splitting plan could still be useful.

Best regards,

[Sender identity]
[Organization]
[Contact information]

### Official source

- `https://www.physik.uni-wuerzburg.de/en/ep3/research/molecular-beam-epitaxy/group-members/`

---

## Packet P5 — archived 2012 HgCdTe STM/STS routing request

**Recipient route:** journal editorial or institutional routing to Qing-Yu Wang, Xiu-Rong Ren, Mao-Sen Li, De-Zheng Xu, Zi-Xuan Gao, or Fang-Xing Zha  
**Direct current author route:** unresolved  
**Status:** `ROUTE_UNRESOLVED_NOT_SENT`

### Subject

Author contact request for archived data from 2012 HgCdTe STM/STS study

### Routing draft

Dear Editorial Office,

I am seeking a current contact route for an author of the article “Scanning tunneling spectra for the etched surface of p-type HgCdTe,” Journal of Infrared and Millimeter Waves 31, 222-225 (2012), DOI 10.3724/SP.J.1010.2012.00222.

The request concerns possible archived raw STM/STS and topography data and is not a request to reproduce copyrighted article content. Would you please forward this message to a corresponding author or provide an appropriate institutional contact?

Best regards,

[Sender identity]
[Organization]
[Contact information]

### Author-facing request

Dear Dr. [Author],

I am evaluating whether archived data from your 2012 HgCdTe STM/STS study could support a quantitative surface-systematics and spatial-variance analysis. Your article is particularly relevant because it explicitly reports tip-induced band bending and pit-associated in-gap states.

Do any of the following records remain available?

- spatially indexed raw I(V) or dI/dV curves;
- registered topography and pit masks;
- temperature, bias/current setpoint, modulation amplitude and frequency;
- tip material and conditioning records;
- exact specimen composition, thickness, growth method, conductivity type, carrier density, and mobility;
- etch timing, transfer atmosphere, and elapsed time before UHV insertion;
- repeated spectra or retained sample material.

A simple archive inventory or confirmation that the records are no longer retained would resolve the present feasibility gate. No unpublished data would be redistributed without explicit permission.

Best regards,

[Sender identity]
[Organization]
[Contact information]

### Official sources

- `https://journal.sitp.ac.cn/hwyhmb/hwyhmben/article/issue/2012_31_3`
- `https://doi.org/10.3724/SP.J.1010.2012.00222`

---

## Response ledger rules

For every route record:

```text
message_status = NOT_SENT | SENT | FOLLOW_UP_SENT | CLOSED
sent_at        = ISO-8601 timestamp only after successful transmission
outcome        = one allowed outcome only after a substantive response or completed follow-up protocol
evidence_commitment = concrete inventory or written commitment only
```

Facility capability pages are not commitments. A positive informal reply without specimen, instrument, raw-data, or calibration detail is `PARTIAL_DATA_ONLY`.

## Follow-up templates

### Seven-day follow-up

Dear [Recipient],

I am following up once on the HgCdTe archive/measurement feasibility request below. A brief yes/no response or referral would be sufficient. The immediate question is whether an identifiable specimen and a credible route to both local composition covariance and low-energy spectroscopy exist.

Best regards,

[Sender identity]

### Closure request after prior engagement

Dear [Recipient],

Thank you for the earlier response. To close the feasibility record, could you confirm whether the unresolved item below is available, unavailable, or requires a formal proposal?

[One unresolved decisive item]

No further follow-up will be sent after this clarification.

Best regards,

[Sender identity]

## Campaign stop rule

Do not infer access from silence, a capability webpage, a publication figure, or a general statement of interest. Do not begin PR3 ingestion until one route supplies a concrete archive inventory or written new-measurement commitment sufficient to instantiate `r04_r05_matched_evidence_v1`.
