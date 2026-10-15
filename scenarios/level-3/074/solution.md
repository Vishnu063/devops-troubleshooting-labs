# Solution · 074

## Diagnosis supported by supplied evidence

The promoted image includes a vulnerable dependency.

## Investigate

Inspect affected package, fixed version, runtime exposure, and scanner evidence.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Upgrade or rebuild the dependency and retest; use only a documented approved exception if warranted.

## Verify

Rescan the exact release digest and run application regression checks.

## Prevent recurrence

Scan immutable artifacts and track remediation deadlines.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
