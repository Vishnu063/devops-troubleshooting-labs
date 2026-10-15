# Solution · 025

## Diagnosis supported by supplied evidence

A resource request exceeds every node's allocatable capacity.

## Investigate

kubectl describe pod POD; kubectl describe nodes; inspect resource requests

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Set a measured feasible request; add capacity only when the requirement is real.

## Verify

Pod schedules and retains adequate resources under load.

## Prevent recurrence

Validate requests against available node sizes.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
