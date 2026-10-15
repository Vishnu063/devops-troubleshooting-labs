# Solution · 076

## Diagnosis supported by supplied evidence

The node group has reached its configured scaling ceiling.

## Investigate

Inspect autoscaler events, group limits, quotas, pending requests, and subnet addresses.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Adjust approved capacity limits or reduce unnecessary demand after checking quota and cost.

## Verify

A suitable node joins and pending workloads schedule.

## Prevent recurrence

Capacity-plan autoscaling bounds and alert before exhaustion.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
