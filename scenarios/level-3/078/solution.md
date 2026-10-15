# Solution · 078

## Diagnosis supported by supplied evidence

The volume topology is incompatible with the replacement node.

## Investigate

Inspect PVC, PV node affinity, CSI events, node zones, and workload scheduling.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Schedule compatible capacity or perform a supported data-preserving storage migration.

## Verify

Volume attaches and existing data is readable and writable.

## Prevent recurrence

Plan storage topology and test rescheduling behavior.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
