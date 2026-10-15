# Solution · 073

## Diagnosis supported by supplied evidence

A credential was committed and must be treated as compromised.

## Investigate

Identify the key owner and exposure window; inspect CloudTrail without printing credentials.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Immediately revoke or disable the exposed credential, replace dependent access, investigate usage, then clean history appropriately.

## Verify

The old key fails; intended workloads use new scoped access; suspicious activity is assessed.

## Prevent recurrence

Use workload identities, secret scanning, and pre-commit detection.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
