# Solution · 089

## Diagnosis supported by supplied evidence

The application retains stale database connections or DNS results.

## Investigate

Inspect failover events, endpoint resolution from the app, pool behavior, and retry logs.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Refresh connections through the supported client mechanism and use bounded backoff with correct DNS handling.

## Verify

New connections reach the writer and a representative transaction succeeds.

## Prevent recurrence

Exercise failover and configure client reconnection behavior.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
