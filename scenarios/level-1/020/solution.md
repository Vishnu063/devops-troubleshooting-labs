# Solution · 020

## Diagnosis supported by supplied evidence

The published target port is incorrect.

## Investigate

docker port CONTAINER; docker logs CONTAINER; inspect port mappings

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Recreate the container with the host port mapped to the actual listener.

## Verify

A request through the published loopback port returns the expected body.

## Prevent recurrence

Test published ports from outside the container.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
