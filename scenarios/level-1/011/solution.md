# Solution · 011

## Diagnosis supported by supplied evidence

Automatic renewal stopped running.

## Investigate

openssl s_client -connect HOST:443 -servername HOST; inspect renewal logs and timers

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Renew through the configured issuer and reload the TLS terminator after validating configuration.

## Verify

A new connection presents a valid chain and correct hostname.

## Prevent recurrence

Monitor expiry and test renewal routinely.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
