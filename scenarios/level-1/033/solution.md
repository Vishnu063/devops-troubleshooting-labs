# Solution · 033

## Diagnosis supported by supplied evidence

The scrape target uses the wrong port.

## Investigate

Inspect /targets, scrape error, target configuration, and direct metrics response.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Correct the scrape address and reload validated configuration.

## Verify

up becomes 1 and expected metrics are collected.

## Prevent recurrence

Add configuration validation and scrape availability alerts.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
