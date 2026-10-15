# Solution · 046

## Diagnosis supported by supplied evidence

A mutable tag allowed artifact selection to drift.

## Investigate

Compare build SHA, image digest, deployment manifest, and registry metadata.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Deploy the intended immutable digest and record it in release metadata.

## Verify

Running image digest matches the validated build.

## Prevent recurrence

Promote the same immutable artifact through environments.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
