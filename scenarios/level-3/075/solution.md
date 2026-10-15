# Solution · 075

## Diagnosis supported by supplied evidence

The hotfix does not meet the configured quality criteria.

## Investigate

Inspect the exact failing gate condition, new-code diff, and test report import.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Add meaningful regression coverage or correct report integration; follow explicit emergency policy if necessary.

## Verify

The relevant regression test and quality gate pass for the hotfix commit.

## Prevent recurrence

Prepare an auditable emergency release process.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
