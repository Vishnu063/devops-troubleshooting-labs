# Solution · 040

## Diagnosis supported by supplied evidence

A released configuration change removed a required timeout.

## Investigate

git log --oneline; git show COMMIT; compare deployment timestamp and errors

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Revert the faulty change through the release process; preserve shared branch history.

## Verify

The reverted release passes checks and production error rate recovers.

## Prevent recurrence

Test boundary values and keep rollback artifacts available.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
