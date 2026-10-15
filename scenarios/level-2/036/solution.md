# Solution · 036

## Diagnosis supported by supplied evidence

The filesystem has exhausted inodes.

## Investigate

df -i; inspect file counts in the specific cache directory

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Remove expired cache files in bounded batches under the retention policy.

## Verify

New file creation succeeds and inode consumption remains stable.

## Prevent recurrence

Bound cache file counts and monitor inode use.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
