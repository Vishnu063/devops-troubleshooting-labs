# Solution · 067

## Diagnosis supported by supplied evidence

The application does not refresh rotated credentials.

## Investigate

Inspect rotation status, secret version stages, application cache behavior, and auth errors.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Refresh credentials using the application's supported mechanism and repair rotation integration.

## Verify

New connections authenticate after rotation without exposing credentials.

## Prevent recurrence

Exercise rotation end to end and define cache refresh behavior.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
