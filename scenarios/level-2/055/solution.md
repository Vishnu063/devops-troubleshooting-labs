# Solution · 055

## Diagnosis supported by supplied evidence

The permitted source selector excludes the intended caller.

## Investigate

Inspect policies, namespace and pod labels, ports, and CNI policy support.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Allow the intended client selector and required port while retaining isolation.

## Verify

Approved client connects; an unapproved client remains blocked.

## Prevent recurrence

Test both allowed and denied network paths.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
