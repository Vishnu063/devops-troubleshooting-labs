# Solution · 087

## Diagnosis supported by supplied evidence

The shared database bottleneck cannot be solved by adding application instances.

## Investigate

Correlate instance metrics, request traces, database waits, and scaling events.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Relieve the database bottleneck and bound incoming concurrency; avoid unbounded instance growth.

## Verify

Latency improves under load without escalating connection pressure.

## Prevent recurrence

Scale on bottleneck-aware metrics and enforce backpressure.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
