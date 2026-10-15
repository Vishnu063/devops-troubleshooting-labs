# Solution · 024

## Diagnosis supported by supplied evidence

The deployment references a nonexistent image tag.

## Investigate

kubectl describe pod POD; inspect image reference and registry availability

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Deploy the approved existing image tag or digest.

## Verify

The image pulls and the pod becomes ready.

## Prevent recurrence

Promote immutable image references after verifying publication.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
