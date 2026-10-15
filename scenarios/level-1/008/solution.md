# Solution · 008

## Diagnosis supported by supplied evidence

The current client address is outside the SSH allow rule.

## Investigate

ssh -vvv; inspect instance address, route, and security group source

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Update the approved narrow source rule or use the established private access path.

## Verify

The authorized client connects; unrelated sources remain blocked.

## Prevent recurrence

Prefer managed access and document changing client addresses.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
