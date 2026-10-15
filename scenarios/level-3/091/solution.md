# Solution · 091

## Diagnosis supported by supplied evidence

The database security group blocks the Lambda execution path.

## Investigate

Inspect function VPC settings, security-group references, DB port, flow logs, and connection timing.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Allow the required database port from the function's security group and confirm subnet reachability.

## Verify

A bounded invocation completes a real database operation.

## Prevent recurrence

Test the function-to-database path after network changes.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
