# Solution · 059

## Diagnosis supported by supplied evidence

Utilization-based HPA cannot calculate its target without resource requests.

## Investigate

Inspect HPA conditions, metrics API, container requests, and current CPU metrics.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Set measured CPU requests and confirm metrics availability.

## Verify

HPA computes utilization and scales under a bounded load test.

## Prevent recurrence

Validate autoscaling prerequisites with each workload.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
