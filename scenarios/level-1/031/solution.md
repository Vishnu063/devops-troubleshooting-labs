# Solution · 031

## Diagnosis supported by supplied evidence

Terraform uses an incorrect backend identity.

## Investigate

Inspect backend configuration, active identity, state location, and access policy.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Use the approved environment identity and backend configuration.

## Verify

Initialization accesses the intended backend without copying production state locally.

## Prevent recurrence

Separate environment credentials and backend configuration.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
