# Solution · 053

## Diagnosis supported by supplied evidence

The Ingress references the wrong Service port.

## Investigate

Inspect ingress description, controller logs, Service ports, and direct Service access.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Reference the Service's exposed port and validate routing configuration.

## Verify

A request with the correct host and path succeeds through the controller.

## Prevent recurrence

Integration-test ingress, Service, and pod ports together.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
