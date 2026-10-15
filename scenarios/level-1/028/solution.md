# Solution · 028

## Diagnosis supported by supplied evidence

The instance security group lacks ingress from the load balancer on the target port.

## Investigate

Inspect listener, target-group port, instance SG, and ALB SG.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Allow the target port from the ALB security group only.

## Verify

ALB health checks and requests succeed.

## Prevent recurrence

Manage SG rules and target ports together.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
