# Solution · 082

## Diagnosis supported by supplied evidence

Git remains authoritative and self-healing restores its declared state.

## Investigate

Inspect application sync policy, Git desired state, audit events, and timeline.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Commit the approved fix to Git; use an explicit temporary reconciliation pause only when required.

## Verify

The fix persists after reconciliation and application health recovers.

## Prevent recurrence

Document emergency GitOps procedures and reconcile temporary changes.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
