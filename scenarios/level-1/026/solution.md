# Solution · 026

## Diagnosis supported by supplied evidence

The Deployment references a Secret that was never provisioned.

## Investigate

kubectl describe pod POD; kubectl get secrets; inspect secretKeyRef names and keys

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Provision the intended Secret through the approved secret workflow or fix the reference.

## Verify

Container starts and receives the expected setting without exposing it in logs.

## Prevent recurrence

Validate required configuration references before rollout.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
