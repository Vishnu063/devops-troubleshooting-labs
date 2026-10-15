# Solution · 023

## Diagnosis supported by supplied evidence

The startup command requires a configuration file that is not mounted.

## Investigate

kubectl describe pod POD; kubectl logs POD --previous; inspect command and volumes

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Provide the expected configuration mount or correct the startup path.

## Verify

Restart count stops increasing and the application stays available.

## Prevent recurrence

Validate startup dependencies in an integration environment.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
