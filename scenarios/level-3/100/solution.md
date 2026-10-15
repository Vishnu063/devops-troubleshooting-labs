# Solution · 100

## Diagnosis supported by supplied evidence

Backup creation was tested but recovery dependencies were not.

## Investigate

Inspect restore errors, backup integrity, key access, recovery identity, and measured elapsed time.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore required key access through approved recovery controls, then repeat a complete isolated restore.

## Verify

Application and data checks pass; measured recovery time and data loss meet stated objectives.

## Prevent recurrence

Run scheduled restore drills including identity, keys, networking, and application startup.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
