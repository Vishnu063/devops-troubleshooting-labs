# Solution · 027

## Diagnosis supported by supplied evidence

The Service selects the wrong labels.

## Investigate

kubectl get svc SERVICE -o yaml; kubectl get pods --show-labels; kubectl get endpointslices

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Correct the Service selector to the intended stable application label.

## Verify

EndpointSlices contain ready pod addresses and an in-cluster request succeeds.

## Prevent recurrence

Test routing as part of deployment verification.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
