# Solution · 006

## Diagnosis supported by supplied evidence

The previous worker was not stopped before starting its replacement.

## Investigate

ss -ltnp; systemctl status orders; ps -fp PID

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Identify the owning service; stop the obsolete instance through its supervisor.

## Verify

Exactly one intended listener exists and the health endpoint responds.

## Prevent recurrence

Use one supervisor and an explicit deployment handover.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
