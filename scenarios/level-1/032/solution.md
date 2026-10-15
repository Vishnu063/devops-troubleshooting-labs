# Solution · 032

## Diagnosis supported by supplied evidence

The inventory specifies the wrong SSH user.

## Investigate

ansible-inventory --host HOST; ssh -vvv; inspect remote_user and key selection

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Set the intended user and approved key in inventory or connection settings.

## Verify

ansible HOST -m ping succeeds and privilege escalation is explicit.

## Prevent recurrence

Test inventory connection settings before running changes.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
