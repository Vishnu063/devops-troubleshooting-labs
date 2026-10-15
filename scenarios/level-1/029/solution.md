# Solution · 029

## Diagnosis supported by supplied evidence

Bucket listing permission does not grant access to objects.

## Investigate

Inspect caller identity, object ARN, role policy, bucket policy, and encryption requirements.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Grant the required object action on the scoped object prefix; preserve explicit restrictions.

## Verify

The same identity reads the intended object and remains denied outside scope.

## Prevent recurrence

Test permissions using the application's real identity.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
