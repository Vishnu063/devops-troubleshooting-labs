# Solution · 003

## Diagnosis supported by supplied evidence

An unbounded work queue exhausts host memory.

## Investigate

free -m; journalctl -k; ps -eo pid,rss,comm --sort=-rss

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Reduce concurrency, bound the queue, and restart or roll back the leaking worker.

## Verify

Memory stabilizes and queued work continues without kernel kills.

## Prevent recurrence

Load-test memory behavior and alert on sustained growth.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
