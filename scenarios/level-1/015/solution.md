# Solution · 015

## Diagnosis supported by supplied evidence

The new agent does not contain the configured build tool.

## Investigate

Inspect agent labels, tool configuration, and PATH in the failing stage.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Select the intended agent or provision the pinned toolchain.

## Verify

The original build completes on a clean agent.

## Prevent recurrence

Version the build environment and validate agent capabilities.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
