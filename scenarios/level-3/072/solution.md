# Solution · 072

## Diagnosis supported by supplied evidence

Session state is tied to the old application instances.

## Investigate

Compare cookie handling, session storage, backend routing, and drain behavior.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Use compatible shared session storage or the tested session-preserving migration approach.

## Verify

Existing sessions survive the switch and rollback test.

## Prevent recurrence

Design session compatibility and connection draining before cutover.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
