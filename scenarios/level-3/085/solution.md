# Solution · 085

## Diagnosis supported by supplied evidence

Provider behavior changed during an unreviewed dependency upgrade.

## Investigate

Compare lock files, provider versions, changelog, schema behavior, and plans.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore the tested constraint or migrate deliberately and review the resulting plan.

## Verify

The chosen provider produces the intended plan and passes environment validation.

## Prevent recurrence

Commit the lock file and review provider upgrades separately.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
