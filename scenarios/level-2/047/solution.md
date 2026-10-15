# Solution · 047

## Diagnosis supported by supplied evidence

A multi-component release stopped after updating only some components.

## Investigate

Inspect stage logs, release manifest, component versions, and compatibility.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore a known compatible version set or complete the approved compatible rollout.

## Verify

Every component matches the release manifest and end-to-end requests succeed.

## Prevent recurrence

Use compatibility checks and explicit release recovery steps.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
