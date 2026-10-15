# Solution · 084

## Diagnosis supported by supplied evidence

An apply completed only part of the desired graph.

## Investigate

Inspect apply logs, current state, actual cloud resources, and a fresh plan.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Reconcile observed resources through supported import or configuration fixes; never blindly edit state JSON.

## Verify

A reviewed follow-up apply converges and the final plan has no unexpected changes.

## Prevent recurrence

Use smaller changes, reliable backends, and recoverable deployment procedures.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
