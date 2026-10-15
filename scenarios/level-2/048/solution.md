# Solution · 048

## Diagnosis supported by supplied evidence

The image architecture does not match the deployment host.

## Investigate

Inspect image platform metadata, build platform, and host architecture.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Build and publish the required architecture or a tested multi-platform image.

## Verify

The image starts on the actual target architecture.

## Prevent recurrence

Validate platform support in CI before promotion.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
