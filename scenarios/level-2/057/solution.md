# Solution · 057

## Diagnosis supported by supplied evidence

An invalid image prevents the new ReplicaSet from becoming ready.

## Investigate

kubectl rollout status deployment/APP; inspect ReplicaSets, pod events, and rollout history

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore the approved previous image or deploy a validated replacement.

## Verify

Rollout completes and all serving replicas use the intended image.

## Prevent recurrence

Verify artifact existence and rehearse rollbacks.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
