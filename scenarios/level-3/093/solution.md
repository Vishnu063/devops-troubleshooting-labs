# Solution · 093

## Diagnosis supported by supplied evidence

The active kubelet identity lacks registry pull access.

## Investigate

Inspect kubelet identity, registry scope, role assignments, and image-pull events.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Assign the appropriate scoped pull permission for the registry's configured authorization mode.

## Verify

A new pod pulls the intended image using the active cluster identity.

## Prevent recurrence

Validate registry integration after identity changes.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
