# Solution · 007

## Diagnosis supported by supplied evidence

The job depends on an interactive-shell PATH.

## Investigate

crontab -l; command -v aws; inspect cron mail and environment

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Set an explicit PATH or executable path and required nonsecret environment settings.

## Verify

Run with a minimal environment, then confirm the next scheduled backup.

## Prevent recurrence

Test scheduled jobs outside interactive shells.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
