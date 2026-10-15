# Solution · 018

## Diagnosis supported by supplied evidence

The event filter excludes the active branch.

## Investigate

Inspect workflow location, YAML, event, branch filters, and changed paths.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Correct the branch filter and push a qualifying change.

## Verify

A workflow run is created for the expected event.

## Prevent recurrence

Test event filters when renaming branches.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
