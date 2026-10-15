# Solution · 037

## Diagnosis supported by supplied evidence

Backup I/O competes with application storage.

## Investigate

vmstat 1; iostat -xz 1; correlate storage metrics and scheduled jobs

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Throttle or reschedule the backup and address underlying storage limits.

## Verify

Application latency and disk wait return to baseline.

## Prevent recurrence

Load-test backup impact and monitor storage latency.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
