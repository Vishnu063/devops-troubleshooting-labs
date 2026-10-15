# Solution · 005

## Diagnosis supported by supplied evidence

A deployment changed ownership of the writable directory.

## Investigate

id app; namei -l /srv/orders/cache; stat /srv/orders/cache

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore ownership for the application directory and grant only required access.

## Verify

A write succeeds as the application user; unrelated paths stay restricted.

## Prevent recurrence

Preserve ownership during deployment; avoid chmod 777.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
