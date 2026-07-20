# Priority-partner outreach and response-ingestion decision

**Date:** 2026-07-20  
**Issue:** #165  
**Parent landscape:** Issue #163 / PR #164  
**Parent feasibility package:** Issue #161 / PR #162

## Decision

The five priority public candidates now have reviewable first-contact drafts and a machine-readable response-ingestion contract.

The committed initial state is:

```text
candidate drafts ready                 5
approved to send                       0
external messages sent                 0
responses received                     0
conditional role recommendations       0
confirmed role recommendations         0
feasibility updates authorized         0
```

No organization has been contacted by this tranche.

## Why event evidence is required

A draft, an internal discussion, and an external message are different provenance events. The response contract therefore retains a chronological event log.

`approved_to_send` requires:

- an explicit approval evidence identifier;
- an intended public professional recipient identifier;
- a dated internal approval event.

`sent` requires:

- the approval evidence;
- a dated external-message event;
- an external-message evidence identifier preserving the actual sent content.

A response cannot be recorded before an evidenced sent event.

## Response classes

```text
unanswered
unsupported_verbal
written_conditional
written_confirmed
written_blocked
```

An unsupported verbal response can be retained as a note but cannot support a role or gate recommendation.

A written conditional response requires:

- dated response evidence;
- an accountable contact identifier;
- at least one role assessment;
- explicit unresolved assumptions.

A written confirmed response requires:

- complete documentary fields for every candidate role;
- evidence for every applicable hard gate;
- no unresolved assumptions.

A written blocked response requires evidence supporting the blocked role assessment.

## Separation from feasibility authority

A response record produces recommendations, not controlling readiness.

Even a complete written-confirmed response does not automatically edit:

```text
data/templates/hgcdte_paired_gap_feasibility_template.json
```

Promotion of a role or gate requires a separate reviewed repository change that cites the response evidence and reruns the PR #162 readiness audit.

## Draft boundary

The outreach drafts:

- use placeholders for sender identity and professional contact information;
- do not store private recipient details;
- request technical feasibility evidence rather than self-certification;
- distinguish the two-specimen pilot from the full experiment;
- promise no funding, access, publication, authorship, or schedule;
- preserve the non-negotiable scientific gates.

## Authorized conclusions

- Five candidate-specific drafts are ready for user review.
- A sent-message and response provenance chain is executable.
- Written responses can be classified without manually weakening the feasibility gates.
- Conditional and blocked responses can be retained even when the collaboration remains `not_ready`.

## Unauthorized conclusions

- No external message has been sent.
- No sender identity, affiliation, or recipient is assumed.
- No facility is endorsed.
- No role or gate is confirmed.
- No feasibility package is automatically modified.
- No cost, schedule, funding, publication, or access promise is made.

## Program consequence

The next action is human review of sender identity, affiliation, recipients, and wording. After explicit approval, each sent message must be recorded with its evidence identifier. Incoming written responses can then be ingested into the template and audited before any feasibility update is proposed.
