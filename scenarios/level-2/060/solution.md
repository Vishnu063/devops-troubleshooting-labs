# Solution · 060

## Diagnosis supported by supplied evidence

Values do not match the chart's expected structure.

## Investigate

helm lint CHART; helm template RELEASE CHART -f values.yaml; inspect values schema

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Correct the value type and validate rendered resources before upgrading.

## Verify

Rendering succeeds and the upgraded release becomes healthy.

## Prevent recurrence

Maintain a values schema and run chart validation in CI.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
