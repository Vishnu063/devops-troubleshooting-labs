# Solution · 009

## Diagnosis supported by supplied evidence

The application hostname has no DNS record.

## Investigate

dig app.example.test; dig @authoritative-server app.example.test

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Create or restore the correct record in the authoritative zone.

## Verify

Authoritative and recursive queries resolve; HTTP succeeds with the hostname.

## Prevent recurrence

Validate DNS records before publishing links.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
