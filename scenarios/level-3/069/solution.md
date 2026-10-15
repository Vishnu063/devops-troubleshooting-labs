# Solution · 069

## Diagnosis supported by supplied evidence

A destructive migration removed compatibility with the previous application.

## Investigate

Inspect migration history, schema diff, app errors, and supported version matrix.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Choose a tested forward fix or compatible schema recovery; protect data before changes.

## Verify

Both required application paths and data integrity checks succeed.

## Prevent recurrence

Use expand-contract migrations and rehearse recovery.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
