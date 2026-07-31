# Decision record: R04/R05 partner contact readiness

**Date:** 2026-07-31  
**Controlling issue:** #398  
**Predecessor:** #395 and PR #397

## Decision

```text
CONTACT_READY_NOT_SENT
```

## Question

Are the highest-value external routes sufficiently verified and narrowly specified to support outbound archive and measurement-feasibility requests without overstating evidence access or partner commitment?

## Evidence reviewed

- merged R04/R05 evidence specification and public-data audit;
- official article and current group pages for the 2025 near-critical HgCdTe quantum-well series;
- official University of Würzburg staff and MBE-group pages;
- official Oak Ridge CNMS STM capability, staff, proposal-type, and proposal-submission pages;
- official Argonne CNM STM scientific-contact and 2026 proposal-schedule pages;
- official journal issue and DOI route for the 2012 HgCdTe STM/STS study.

## Findings

1. The near-critical specimen group has a current public corresponding/group-lead route.
2. ORNL CNMS has current public STM/STS staff routes and an off-cycle Rapid Access mechanism, but HgCdTe acceptance and preparation remain unverified.
3. Argonne CNM lists relevant UHV STM/STS and cryo-STM capabilities and a concrete October 30, 2026 proposal deadline, but the scientific-contact emails are protected on the public page and must be reached through the official page or portal.
4. The Würzburg MBE team provides a credible retained-material and growth-provenance route.
5. The 2012 HgCdTe STM/STS article remains scientifically relevant, but a current direct author route was not verified.
6. No outbound message has been sent, no response exists, and no archive or measurement commitment has been obtained.

## Implementation

The contact-readiness tranche adds:

- `data/validation/r04_r05_partner_campaign.json`;
- `src/mct_research/r04_r05_partner_campaign.py`;
- `tests/test_r04_r05_partner_campaign.py`;
- `research/programs/spatial_disorder/r04_r05_partner_contact_packets.md`;
- `research/programs/spatial_disorder/r04_r05_partner_campaign_status.md`.

The executable validator rejects:

- contact-ready records that contain sent timestamps or outcomes;
- outreach status without a reviewed sender identity and at least one sent route;
- data-ingestion status without a qualifying concrete commitment;
- facility capability treated as a measurement commitment;
- missing official sources or source-verification dates;
- follow-up schedules that violate the frozen 7-day and 14-day protocol.

## Why outreach was not sent

The sender identity and organizational representation are unresolved repository inputs. Sending also requires final review of recipient choice, message text, publication/proprietary intent, and ability to enter user or data-sharing agreements.

The repository therefore records readiness without fabricating action.

## Authorized next state

```text
OUTREACH_IN_PROGRESS
```

only after explicit sender and recipient review and successful transmission of at least one packet.

## Rejected alternatives

- recording messages as sent merely because drafts exist;
- treating current facility capability pages as sample acceptance;
- opening PR3 ingestion without a concrete archive or written commitment;
- substituting additional R05 simulation for external evidence;
- claiming that no direct route to the 2012 authors means the archive does not exist.

## Claim boundary

This decision establishes a verified, bounded contact package. It establishes no partner relationship, data access, specimen availability, material acceptance, measured covariance, spectroscopy result, or R05 physical activation.
