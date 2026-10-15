# Solution · 063

## Diagnosis supported by supplied evidence

The actual resource differs from its declared configuration.

## Investigate

terraform plan; inspect configuration diff and audited resource changes

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Decide whether to codify the approved change or restore the declared state through review.

## Verify

A fresh reviewed plan shows only intended changes.

## Prevent recurrence

Manage emergency changes with reconciliation and audit.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
