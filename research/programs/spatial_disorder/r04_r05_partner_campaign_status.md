# R04/R05 partner campaign status

**Controlling issue:** #398  
**Predecessor decision:** `PARTNER_DATA_REQUIRED`  
**Current decision:** `CONTACT_READY_NOT_SENT`  
**Record date:** 2026-07-31

## Current state

The public-data stage is complete. No qualifying matched record was found, and no external partner has yet committed data, material, instrument time, or a registered measurement workflow.

A bounded contact-readiness package now exists for:

1. the corresponding/group lead for the 2025 near-critical HgCdTe quantum-well series;
2. Oak Ridge CNMS cryogenic STM/STS staff and proposal routes;
3. Argonne CNM cryogenic STM/STS scientific contacts and the next posted proposal deadline;
4. the Würzburg Hg-based MBE and retained-material team;
5. journal/institutional routing for the 2012 HgCdTe STM/STS archive.

## Source-verified operational facts

### Würzburg near-critical specimen route

The 2025 Physical Review Materials article identifies Tobias Kießling as the contact author. The current University of Würzburg group page identifies him as a group leader and provides a public institutional email.

This route has the highest decision value because it may connect near-critical specimen state, archived structural and magneto-optical data, retained material, and growth provenance.

### Oak Ridge CNMS

The official CNMS pages list:

- atomic-resolution imaging and electronic density-of-states mapping;
- temperatures from approximately 40 mK to 300 K across the STM group;
- UHV and in-situ preparation capabilities;
- public contacts for An-Ping Li and Saban Hus;
- General User calls in May and October;
- off-cycle Rapid Access proposals for limited proof-of-concept studies.

The exact fall 2026 General User deadline was not posted on the audited call page as of 2026-07-31. It must not be invented from historical cycles.

### Argonne CNM

The official CNM pages list UHV STM, STS, cryo-STM, Createc LT-STM, and related scanning-probe capabilities. The scientific-contact page identifies Nathan Guisinger for UHV STM, STS, and cryo-STM and Jeffrey Guest for STM and group leadership.

The official 2026 proposal schedule lists:

```text
call opens: 2026-10-02
deadline:   2026-10-30 11:59 PM CT
```

The public contact emails are Cloudflare-protected on the audited page, so the campaign record preserves the official contact-page and User Portal route rather than guessing an address.

### Archived 2012 HgCdTe STM/STS

The article and journal issue page establish material-specific STM/STS and the relevant tip-induced band-bending and pit-state systematics. A current direct author route was not verified. This packet remains `ROUTE_UNRESOLVED_NOT_SENT` and requires journal or institutional routing.

## Why outreach is not yet recorded

The repository cannot infer or select the sender identity. Outbound messages also require final review of:

- sender name and organization;
- open/publication-oriented versus proprietary intent;
- recipient selection;
- whether the sender can support specimen handling, user agreements, and publication obligations;
- final message text.

No message has been sent. No `sent_at`, response outcome, or evidence commitment is recorded.

## Gate status

```text
verified contact routes:       PASS
route-specific request packets: PASS
follow-up and stop rules:       PASS
sender identity:                UNSET
outbound contact authorized:    NO
partner response:               NONE
archive or measurement commitment: NONE
data ingestion:                BLOCKED
R05 material activation:       BLOCKED
```

## Next decision

After explicit sender/recipient review, the campaign may transition to:

```text
OUTREACH_IN_PROGRESS
```

It may transition to `GO_PARTNER_DATA_INGESTION` only after a route supplies a concrete archive inventory or written new-measurement commitment sufficient to instantiate the merged evidence schema.

## Unsupported interpretations

This state does not mean:

- a partner has agreed to collaborate;
- a facility accepts HgCdTe;
- a nominal instrument capability satisfies the measured-kernel gate;
- retained material exists;
- local covariance or low-energy DOS has been measured;
- R05 is reactivated.
