# Solution · 096

## Diagnosis supported by supplied evidence

The build identity lacks write access to the target repository.

## Investigate

Inspect the build's service account, repository location, image path, and IAM denial.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Grant only the required repository write permission to the actual build identity.

## Verify

The same build publishes its artifact and downstream deployment can pull it.

## Prevent recurrence

Declare build identities and repository permissions explicitly.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
