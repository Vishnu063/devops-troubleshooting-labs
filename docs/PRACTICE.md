# Practice method

1. Pick a case: `python3 lab.py random --level 2`.
2. Read its brief. State user impact and what changed before choosing commands.
3. Rank three hypotheses. For each, name an observation that would disprove it.
4. Inspect supplied evidence or start its native lab. Keep a timeline of observations.
5. Choose the smallest evidence-supported repair and explain rollback conditions.
6. Verify recovery from the user's path, then check recurrence signals.
7. Compare the separate solution and write your incident report.
8. Record elapsed time, hints, and a self-assessed score.

## Interview answer structure

“I would confirm impact and recent changes, then inspect X to distinguish A from B. If the evidence shows Y, I would apply Z with this rollback condition. I would verify the user request and monitor these signals before closing the incident.”

Describe what commands prove. A list of commands without interpretation is not a complete diagnosis.

## Ten-point rubric

| Area | Points | Evidence required |
| --- | --- | --- |
| Scope and impact | 0–2 | Affected users, timeframe, recent changes, severity |
| Investigation | 0–2 | Ranked hypotheses, useful checks, interpreted results |
| Root cause | 0–2 | Cause supported by evidence; alternatives considered |
| Recovery | 0–2 | Minimal repair, availability/data risk, rollback decision |
| Verification and prevention | 0–2 | User-path check, stability signals, targeted prevention |

For each row: 0 = missing; 1 = partial; 2 = specific and justified. Scores are self-assessment, separate from automated native lab checks.

## Difficulty modes

| Mode | Rules |
| --- | --- |
| Guided | Evidence plus progressive hints; no time pressure |
| Interview | Explain initial approach before reading the evidence; use the level time target |
| Hard | No hints or solution; time-box diagnosis and recovery; state disconfirming evidence |
| Incident commander | Hard mode plus a 60-second stakeholder update and explicit rollback decision |

The catalog title reveals a symptom. Supplied evidence may strongly narrow the cause; for more realistic uncertainty, have a partner reveal observations one at a time. There is no hidden autonomous incident engine or automatic interview scoring.

## Explain your experience honestly

Use “I reproduced and resolved this in a lab” for practice work. Distinguish it from an incident you personally handled at work. Terraform cases can demonstrate project knowledge without implying production Terraform experience.

## CLI sessions and repeatable faults

Use [timed hidden sessions](SESSIONS.md) for a symptom-first brief, hint tracking, optional level gates, and recorded elapsed time. Use `python3 lab.py reset ID` to repeat a native fault. [Compound incidents](../COMPOUNDS.md) add two independent failures outside the final 100.

A hidden session hides the catalog title, not the local source files or resource identifiers. Root-cause reasoning and interview scores remain self-assessed. Native recovery is checked behaviorally.
