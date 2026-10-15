# Solution · 013

## Diagnosis supported by supplied evidence

Competing edits require a deliberate combined change.

## Investigate

git status; git diff --cc; git show :2:app.conf; git show :3:app.conf

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Resolve the intended behavior, remove conflict markers, test, and complete the merge.

## Verify

Git has no unmerged entries and the combined configuration passes checks.

## Prevent recurrence

Keep changes focused and coordinate shared configuration edits.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
