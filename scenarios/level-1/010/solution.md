# Solution · 010

## Diagnosis supported by supplied evidence

The application listens only on loopback.

## Investigate

ss -ltnp; curl -v http://127.0.0.1:8080; inspect bind settings

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Bind to the intended private interface or place the approved reverse proxy in front.

## Verify

Requests work through the intended entry point without exposing unnecessary ports.

## Prevent recurrence

Make bind addresses explicit in configuration.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
