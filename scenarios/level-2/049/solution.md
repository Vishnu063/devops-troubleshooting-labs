# Solution · 049

## Diagnosis supported by supplied evidence

localhost points to the application container rather than its database.

## Investigate

Inspect network membership, DB hostname, DNS resolution, and application logs.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Use the database service name on the shared application network.

## Verify

The application completes a real database query.

## Prevent recurrence

Test service discovery within the deployment network.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
