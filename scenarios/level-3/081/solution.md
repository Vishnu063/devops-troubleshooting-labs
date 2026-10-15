# Solution · 081

## Diagnosis supported by supplied evidence

Mixed pod versions expose incompatible serving ports during rollout.

## Investigate

Compare EndpointSlices, pod versions, named ports, and per-endpoint requests.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore compatible serving configuration and remove the faulty version through a controlled rollout.

## Verify

Every endpoint responds and repeated Service requests succeed.

## Prevent recurrence

Keep stable port contracts across rolling releases.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
