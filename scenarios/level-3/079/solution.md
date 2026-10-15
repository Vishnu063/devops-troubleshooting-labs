# Solution · 079

## Diagnosis supported by supplied evidence

Manifests use an API removed from the upgraded cluster.

## Investigate

Inspect cluster version, discovery, manifests, and API deprecation reports.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Migrate manifests and required fields to a supported API; validate against the target version.

## Verify

Resources apply and routing works on the upgraded cluster.

## Prevent recurrence

Scan deprecated APIs and rehearse upgrades in advance.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
