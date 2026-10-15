# Solution · 065

## Diagnosis supported by supplied evidence

The private subnet has no intended outbound path.

## Investigate

Inspect subnet association, routes, NAT status, public-subnet IGW route, and NACLs.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Restore the approved egress route or use required service endpoints where suitable.

## Verify

Required outbound destinations work while unsolicited inbound access stays blocked.

## Prevent recurrence

Test subnet routing and consider ongoing NAT costs before provisioning.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
