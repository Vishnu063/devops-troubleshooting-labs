# Solution · 068

## Diagnosis supported by supplied evidence

Deployments are not serialized or protected against stale promotion.

## Investigate

Compare deployment timestamps, commit SHAs, environment locks, and stage logs.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Serialize environment changes and reject stale releases; restore the intended artifact.

## Verify

A concurrency test leaves the newest approved release active.

## Prevent recurrence

Use environment concurrency controls and immutable release metadata.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
