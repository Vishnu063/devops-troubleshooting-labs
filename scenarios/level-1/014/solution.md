# Solution · 014

## Diagnosis supported by supplied evidence

The automation credential is invalid.

## Investigate

Inspect credential source, token expiry, repository access, and remote URL without printing secrets.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Replace the credential through the approved secret store with minimum repository permissions.

## Verify

Clone succeeds from the same automation identity.

## Prevent recurrence

Use scoped credentials with rotation and expiry monitoring.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
