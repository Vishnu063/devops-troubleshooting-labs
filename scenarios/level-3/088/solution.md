# Solution · 088

## Diagnosis supported by supplied evidence

The application has a single-zone failure domain.

## Investigate

Inspect subnet placement, load balancer targets, dependency topology, and regional health.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Recover using the tested multi-zone or disaster-recovery procedure with healthy dependencies.

## Verify

Requests succeed with the affected zone unavailable and data checks pass.

## Prevent recurrence

Spread critical tiers across failure domains and rehearse zone loss.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
