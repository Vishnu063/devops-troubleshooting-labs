# Solution · 019

## Diagnosis supported by supplied evidence

The container startup requires an omitted environment variable.

## Investigate

docker ps -a; docker logs CONTAINER; docker inspect CONTAINER

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Supply the required nonsecret runtime configuration and recreate the container.

## Verify

Container stays running and returns a successful health response.

## Prevent recurrence

Validate required runtime settings before release.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
