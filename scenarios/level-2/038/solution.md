# Solution · 038

## Diagnosis supported by supplied evidence

One backend subnet has an incorrect route or firewall path.

## Investigate

Resolve all addresses; test each backend; compare routes and flow logs.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Correct the affected path; remove the unhealthy backend from routing during repair.

## Verify

Repeated tests succeed against every backend.

## Prevent recurrence

Verify connectivity per backend and enforce consistent network configuration.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
