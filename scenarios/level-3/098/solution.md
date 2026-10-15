# Solution · 098

## Diagnosis supported by supplied evidence

The ingestion backend is throttling and collector buffers are exhausted.

## Investigate

Inspect collector errors, queue size, backend availability, rate limits, and source timestamps.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore ingestion capacity, reduce unnecessary volume, and recover buffered logs where possible.

## Verify

A new identifiable event reaches search and ingestion lag returns to normal.

## Prevent recurrence

Monitor ingestion lag and bound noisy log sources.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
