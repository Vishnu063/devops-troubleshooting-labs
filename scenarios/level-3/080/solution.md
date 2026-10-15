# Solution · 080

## Diagnosis supported by supplied evidence

Recovery needs capacity that the namespace quota disallows.

## Investigate

Inspect ResourceQuota usage, pod requests, failed events, and obsolete workloads.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Remove genuinely obsolete allocations or approve appropriate quota with underlying capacity available.

## Verify

Recovery pods are admitted and service availability returns.

## Prevent recurrence

Reserve recovery headroom and monitor quota consumption.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
