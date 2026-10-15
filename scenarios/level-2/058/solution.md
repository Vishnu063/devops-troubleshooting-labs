# Solution · 058

## Diagnosis supported by supplied evidence

Node storage exhaustion disrupted kubelet and container runtime.

## Investigate

Inspect node conditions, kubelet logs, disk usage, and affected workloads.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Cordon the node, preserve service availability, reclaim safe space or replace the node.

## Verify

Node health recovers or workloads run on healthy replacement capacity.

## Prevent recurrence

Monitor node storage and configure image garbage collection.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
