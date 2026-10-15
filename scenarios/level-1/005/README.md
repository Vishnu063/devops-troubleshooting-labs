# 005 · Linux: File permissions

Level 1 · 20 minute target · Runnable docker lab + evidence drill

[Catalog](../../../CATALOG.md) · [Practice guide](../../../docs/PRACTICE.md)

## Incident brief

You are on call. Investigate this incident, restore the intended behavior, and explain how you verified recovery. The title describes the symptom, not necessarily the root cause.

## Your assignment

1. Record impact, recent changes, and three ranked hypotheses.
2. Open [evidence](evidence.md), then request any missing evidence explicitly.
3. Write your next commands and explain what each result would prove.
4. Propose the smallest justified repair, rollback, and verification.
5. Complete an [incident report](../../../templates/incident-report.md).

## Practice modes

Start a timed hidden session with `python3 lab.py session start --hidden --level 1`. [Session commands](../../../docs/SESSIONS.md).

- Guided: use the [three progressive hints](hints.md).
- Interview: explain your approach aloud before opening evidence.
- Hard: use a timer, no hints, and state evidence that would disprove your diagnosis.
- Incident commander: give a 60-second update and a recovery decision before proposing a fix.

## Run the fault locally

Prerequisites and isolation: [lab setup](../../../docs/LABS.md).

```bash
python3 lab.py up 005
python3 lab.py check 005
# Investigate and repair the workspace printed by up.
python3 lab.py check 005
python3 lab.py down 005
# Repeat from the original broken state:
python3 lab.py reset 005
```

The initial check should fail. Read the native lab's instructions at [runnable/005](../../../runnable/005/README.md).

## Finish

Compare your evidence-based answer against the [separate solution](solution.md) only after attempting the case. More than one valid recovery path may exist. Explain your assumptions.
