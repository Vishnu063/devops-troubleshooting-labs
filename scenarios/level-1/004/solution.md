# Solution · 004

## Diagnosis supported by supplied evidence

Application logs grew without rotation.

## Investigate

df -h; du -xhd1 /var; systemctl status logrotate.timer

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Preserve required incident evidence; rotate the specific log and restore rotation.

## Verify

Space remains available while new logs are written.

## Prevent recurrence

Test rotation and alert before exhaustion.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
