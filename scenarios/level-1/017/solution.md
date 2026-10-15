# Solution · 017

## Diagnosis supported by supplied evidence

The running agent identity lacks approved Docker access.

## Investigate

id; stat /var/run/docker.sock; inspect agent process group membership

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Use a dedicated authorized builder; if socket access is approved, update group membership and restart the agent.

## Verify

Docker access succeeds as the agent identity without changing socket permissions globally.

## Prevent recurrence

Treat Docker socket access as privileged and isolate builders.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
