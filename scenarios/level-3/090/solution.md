# Solution · 090

## Diagnosis supported by supplied evidence

Cached records from before the cutover have not expired.

## Investigate

Compare authoritative and recursive answers, previous TTL, old endpoint health, and change time.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Keep the old path compatible through cache expiry; repair incorrect authoritative records if present.

## Verify

Queries and user requests converge after the relevant cache windows.

## Prevent recurrence

Lower TTL ahead of planned cutovers and retain a rollback path.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
