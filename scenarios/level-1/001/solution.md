# Solution · 001

## Diagnosis supported by supplied evidence

A required environment file was removed during deployment.

## Investigate

systemctl status orders; journalctl -u orders -n 50; systemctl cat orders

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore the approved environment file with restricted permissions, then restart the service.

## Verify

Service active; local health endpoint and external request succeed.

## Prevent recurrence

Validate required files before deployment.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
