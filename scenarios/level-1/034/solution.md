# Solution · 034

## Diagnosis supported by supplied evidence

The dashboard filters on a stale label.

## Investigate

Check query inspector, time range, data source, and metric labels.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Update the query or dashboard variable to the intended labels.

## Verify

Panels return data across an appropriate time range.

## Prevent recurrence

Version dashboards with metric-label changes.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
