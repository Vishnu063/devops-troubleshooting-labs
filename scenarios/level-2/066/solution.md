# Solution · 066

## Diagnosis supported by supplied evidence

Aggregate application pools exceed database connection capacity.

## Investigate

Inspect DB connections, application replica count, pool limits, and query duration.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Bound pools, remove leaks, and reduce concurrency; scale only when justified.

## Verify

Connection waits fall and requests succeed under representative load.

## Prevent recurrence

Budget connections across replicas and alert on saturation.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
