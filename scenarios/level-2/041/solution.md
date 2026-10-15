# Solution · 041

## Diagnosis supported by supplied evidence

Agents have different toolchains.

## Investigate

Compare java -version, environment, agent image, and dependency cache.

Correlate timestamps and recent changes. A similar symptom in a real environment can have a different cause.

## Recovery

Pin the required toolchain and route builds to the compatible environment.

## Verify

A clean build passes on every eligible agent.

## Prevent recurrence

Use versioned agent images and reproducible builds.

## Interview follow-ups

- What evidence would invalidate this diagnosis?
- What availability or data risk does the repair introduce?
- How would you roll back if verification fails?
- What would you tell the incident commander in 60 seconds?

Use [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.
