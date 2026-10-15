# Solution · 012

## Diagnosis supported by supplied evidence

The proxy points to the wrong upstream port.

## Investigate

nginx -t; inspect error log; ss -ltnp; curl upstream directly

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Correct the upstream port, validate configuration, then reload.

## Verify

Both direct upstream and proxied requests succeed.

## Prevent recurrence

Smoke-test proxy-to-upstream connectivity during release.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
