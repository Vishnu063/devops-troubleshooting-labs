# Solution · 039

## Diagnosis supported by supplied evidence

Backend requests stall waiting for database connections.

## Investigate

Correlate proxy upstream timings, app traces, DB pool metrics, and slow queries.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Relieve the database bottleneck and bound application concurrency; tune timeouts only with evidence.

## Verify

Representative load completes within the latency objective without growing queues.

## Prevent recurrence

Monitor dependency saturation and apply backpressure.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
