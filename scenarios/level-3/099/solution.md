# Solution · 099

## Diagnosis supported by supplied evidence

A shared DNS dependency causes failures across otherwise healthy services.

## Investigate

Build a dependency timeline; compare healthy and failing paths; test resolution from each tier.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore the shared resolver or activate the tested alternative; avoid unrelated restarts.

## Verify

Critical user journeys recover across all affected services.

## Prevent recurrence

Map shared dependencies and rehearse their failure modes.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
