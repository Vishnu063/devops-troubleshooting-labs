# Solution · 035

## Diagnosis supported by supplied evidence

A running process still holds an open deleted file.

## Investigate

df -h; du -xhd1 /var; lsof +L1

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Rotate properly or gracefully restart the owning process after preserving evidence.

## Verify

The file descriptor closes, disk space returns, and the service stays healthy.

## Prevent recurrence

Configure application-aware log rotation.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
