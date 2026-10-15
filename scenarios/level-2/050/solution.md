# Solution · 050

## Diagnosis supported by supplied evidence

The container's memory limit is below its startup requirement.

## Investigate

kubectl describe pod POD; kubectl logs POD --previous; inspect memory metrics and limits

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Set a measured sufficient limit and investigate abnormal growth rather than increasing indefinitely.

## Verify

The container survives startup and representative load without additional OOM kills.

## Prevent recurrence

Profile memory and validate limits under load.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
