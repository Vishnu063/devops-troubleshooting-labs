# Solution · 043

## Diagnosis supported by supplied evidence

The OIDC subject does not match the IAM trust policy.

## Investigate

Compare workflow permissions, issuer, audience, branch or environment subject, and role trust.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Use the approved protected branch or environment; narrow any required trust-policy change.

## Verify

Only intended workflow subjects assume the role and complete the scoped AWS action.

## Prevent recurrence

Test OIDC trust conditions; avoid broad wildcard subjects.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
