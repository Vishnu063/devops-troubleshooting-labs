# Solution · 052

## Diagnosis supported by supplied evidence

Liveness kills the application before initialization completes.

## Investigate

Compare startup logs, probe timing, restart timestamps, and pod events.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Use an appropriate startup probe and retain a meaningful liveness check.

## Verify

The pod completes startup and no longer restarts during normal initialization.

## Prevent recurrence

Measure startup time and test probes on cold starts.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
