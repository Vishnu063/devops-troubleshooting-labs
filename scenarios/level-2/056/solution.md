# Solution · 056

## Diagnosis supported by supplied evidence

The requested storage class is unavailable.

## Investigate

kubectl describe pvc CLAIM; kubectl get storageclass; inspect provisioner events

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Select an available suitable class or install the approved provisioner in the lab.

## Verify

The claim binds and the workload can read and write its mounted volume.

## Prevent recurrence

Validate storage classes and provisioning before rollout.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
