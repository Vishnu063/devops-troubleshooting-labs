# Solution · 054

## Diagnosis supported by supplied evidence

The pod bypasses cluster DNS configuration.

## Investigate

Inspect pod dnsPolicy, /etc/resolv.conf, DNS lookup results, and CoreDNS logs.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Use the appropriate cluster DNS policy for the workload.

## Verify

The pod resolves the intended Service and connects to it.

## Prevent recurrence

Validate pod DNS settings in deployment review.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
