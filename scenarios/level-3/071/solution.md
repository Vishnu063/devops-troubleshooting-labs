# Solution · 071

## Diagnosis supported by supplied evidence

The canary release is incompatible with a subset of production data.

## Investigate

Compare metrics by version and cohort; inspect traces and representative records.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Stop promotion, route traffic away from the canary, and fix compatibility.

## Verify

Affected cohorts succeed and canary-specific error metrics recover.

## Prevent recurrence

Use representative data and explicit canary abort criteria.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
