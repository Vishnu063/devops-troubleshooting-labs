# Solution · 097

## Diagnosis supported by supplied evidence

Alert routing configuration directs the alert away from the on-call receiver.

## Investigate

Inspect firing state, labels, routing tree, silences, inhibition, and delivery logs.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Correct the intended route and receiver configuration; test an end-to-end notification.

## Verify

The correct receiver gets firing and resolved test notifications.

## Prevent recurrence

Run periodic end-to-end alert-delivery tests.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
