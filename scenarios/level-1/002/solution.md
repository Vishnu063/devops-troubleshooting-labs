# Solution · 002

## Diagnosis supported by supplied evidence

A new worker release introduced a CPU-heavy loop.

## Investigate

top -H; ps -eo pid,pcpu,comm --sort=-pcpu; compare release timestamps

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Capture profiling evidence, then roll back the faulty worker or stop its retry loop.

## Verify

CPU and latency return to baseline under representative traffic.

## Prevent recurrence

Profile expensive paths and bound retries.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
