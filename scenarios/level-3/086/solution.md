# Solution · 086

## Diagnosis supported by supplied evidence

The workload identity trust does not match the pod's service account.

## Investigate

Inspect service account, identity association or federation setup, role trust, and caller identity.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Correct the intended identity binding and narrowly scoped trust conditions.

## Verify

The pod assumes the intended role and performs only required actions.

## Prevent recurrence

Test identity from the actual workload after deployment.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
