# Solution · 095

## Diagnosis supported by supplied evidence

The pod's Kubernetes identity is not authorized as intended.

## Investigate

Inspect workload identity configuration, service-account bindings, active principal, and resource policy.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Correct the intended workload identity binding and scoped resource access.

## Verify

The workload accesses its required resource without a downloaded service-account key.

## Prevent recurrence

Validate identity bindings and resource IAM together.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
