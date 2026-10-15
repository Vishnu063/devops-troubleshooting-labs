# Solution · 021

## Diagnosis supported by supplied evidence

A bind mount hides files bundled in the image.

## Investigate

docker inspect CONTAINER; inspect host mount directory and container listing

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Mount the intended populated directory or remove the unnecessary mount.

## Verify

The expected document is visible and served through the published port.

## Prevent recurrence

Validate mount contents and avoid accidental path overlays.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
