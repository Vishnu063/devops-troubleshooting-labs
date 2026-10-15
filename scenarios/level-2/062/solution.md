# Solution · 062

## Diagnosis supported by supplied evidence

Another active Terraform process owns the state.

## Investigate

Inspect lock owner, CI runs, backend details, and active apply status.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Wait for or safely stop the owning operation; unlock only after proving the lock is stale.

## Verify

One writer acquires the lock and the plan completes.

## Prevent recurrence

Serialize applies per state; never blindly force-unlock.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
