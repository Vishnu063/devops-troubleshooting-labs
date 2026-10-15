# Solution · 064

## Diagnosis supported by supplied evidence

A shell task reports changes without checking actual state.

## Investigate

Run a second playbook pass; inspect changed tasks and handler triggers.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Use an idempotent template or module and notify handlers only on real change.

## Verify

A second unchanged run reports no changes and performs no restart.

## Prevent recurrence

Require idempotency checks for configuration playbooks.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
