# Solution · 051

## Diagnosis supported by supplied evidence

The readiness probe checks a nonexistent endpoint.

## Investigate

Inspect probe configuration, pod events, and direct endpoint responses.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Use a meaningful implemented readiness endpoint with suitable timing.

## Verify

Pods become ready and the Service successfully routes requests.

## Prevent recurrence

Test probe semantics with the application release.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
