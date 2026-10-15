# Solution · 094

## Diagnosis supported by supplied evidence

The new authorization model lacks an equivalent assignment for the application.

## Investigate

Inspect vault authorization mode, active managed identity, role or policy scope, and audit logs.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore narrowly scoped secret access using the vault's active authorization model.

## Verify

The application retrieves its required secret while unrelated identities stay denied.

## Prevent recurrence

Review identity permissions when migrating access models.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
