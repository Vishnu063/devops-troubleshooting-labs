# Solution · 045

## Diagnosis supported by supplied evidence

The service connection identity lacks the required deployment role.

## Investigate

Inspect connection identity, subscription scope, role assignment, and failed action.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Grant the minimum appropriate role at the required scope through the approval process.

## Verify

The deployment succeeds and unrelated scopes remain inaccessible.

## Prevent recurrence

Version and review deployment identity permissions.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
