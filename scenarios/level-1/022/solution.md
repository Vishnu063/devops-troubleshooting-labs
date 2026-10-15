# Solution · 022

## Diagnosis supported by supplied evidence

The client authenticated against the wrong registry hostname.

## Investigate

Inspect image reference, registry hostname, credential helper, and credential scope.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Authenticate to the exact target using short-lived credentials and minimum permissions.

## Verify

A push and a pull by the deployment identity succeed.

## Prevent recurrence

Centralize registry identity configuration.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
