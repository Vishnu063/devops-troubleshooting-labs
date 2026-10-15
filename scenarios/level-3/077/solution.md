# Solution · 077

## Diagnosis supported by supplied evidence

Eviction would violate the workload's disruption budget.

## Investigate

Inspect PDB allowed disruptions, ready replicas, rollout health, and drain events.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore or add healthy replicas, then retry the drain; change the budget only with an availability review.

## Verify

Drain completes without losing the required healthy capacity.

## Prevent recurrence

Align maintenance capacity, replica count, and disruption budgets.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
