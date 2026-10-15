# Solution · 042

## Diagnosis supported by supplied evidence

The agent runtime is incompatible with the upgraded controller requirements.

## Investigate

Inspect controller and agent versions, startup errors, and supported upgrade path.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Upgrade the agent runtime using the supported path or restore the tested controller version.

## Verify

Agents reconnect and a representative pipeline succeeds.

## Prevent recurrence

Rehearse upgrades with compatibility checks and backups.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
