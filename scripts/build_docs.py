"""Generate navigable casebooks from the reviewed incident catalog."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from registry import RUNNABLE,RUNTIMES,COMPOUNDS
def build():
    cases=json.loads((ROOT/'data/incidents.json').read_text())
    catalog=['# The final 100 scenarios','', 'Every case has a supplied-evidence drill. Cases marked **Runnable** also have a reproducible local fault. Cloud cases do not provision infrastructure.','', '| ID | Level | Incident | Practice / prerequisites | Target |','| --- | --- | --- | --- | --- |']
    progress=['# Practice checklist','','Copy this file into your own notes or track attempts with `python3 lab.py record`. Checking a box is self-assessment, not proof of a lab repair.','']
    for c in cases:
        folder=f"scenarios/level-{c['level']}/{c['id']}"
        p=ROOT/folder;p.mkdir(parents=True,exist_ok=True)
        native=RUNNABLE.get(c['id'])
        mode=f'Runnable {native} lab + evidence drill' if native else 'Evidence drill'
        intro=f"# {c['id']} · {c['title']}\n\nLevel {c['level']} · {c['minutes']} minute target · {mode}\n\n[Catalog](../../../CATALOG.md) · [Practice guide](../../../docs/PRACTICE.md)\n\n## Incident brief\n\nYou are on call. Investigate this incident, restore the intended behavior, and explain how you verified recovery. The title describes the symptom, not necessarily the root cause.\n\n## Your assignment\n\n1. Record impact, recent changes, and three ranked hypotheses.\n2. Open [evidence](evidence.md), then request any missing evidence explicitly.\n3. Write your next commands and explain what each result would prove.\n4. Propose the smallest justified repair, rollback, and verification.\n5. Complete an [incident report](../../../templates/incident-report.md).\n\n## Practice modes\n\nStart a timed hidden session with `python3 lab.py session start --hidden --level {c['level']}`. [Session commands](../../../docs/SESSIONS.md).\n\n- Guided: use the [three progressive hints](hints.md).\n- Interview: explain your approach aloud before opening evidence.\n- Hard: use a timer, no hints, and state evidence that would disprove your diagnosis.\n- Incident commander: give a 60-second update and a recovery decision before proposing a fix.\n\n"
        if native:
            intro+=f"## Run the fault locally\n\nPrerequisites and isolation: [lab setup](../../../docs/LABS.md).\n\n```bash\npython3 lab.py up {c['id']}\npython3 lab.py check {c['id']}\n# Investigate and repair the workspace printed by up.\npython3 lab.py check {c['id']}\npython3 lab.py down {c['id']}\n# Repeat from the original broken state:\npython3 lab.py reset {c['id']}\n```\n\nThe initial check should fail. Read the native lab's instructions at [runnable/{c['id']}](../../../runnable/{c['id']}/README.md).\n\n"
        else:
            intro+="## Evidence drill\n\nUse the supplied snapshot as an incident investigation. No infrastructure is created. Write commands you would run in an authorized environment; do not execute production changes as part of this exercise.\n\n"
        intro+="## Finish\n\nCompare your evidence-based answer against the [separate solution](solution.md) only after attempting the case. More than one valid recovery path may exist. Explain your assumptions.\n"
        (p/'README.md').write_text(intro)
        (p/'evidence.md').write_text(f"# Supplied evidence · {c['id']}\n\nThese are synthetic training observations, not captured production logs. Native lab output may differ; investigate the live output when using a runnable lab.\n\n```text\n{c['evidence']}\n```\n\nWhat does this establish? What remains unknown? Ask for the smallest additional observation that distinguishes your top two hypotheses.\n")
        (p/'hints.md').write_text(f"# Progressive hints · {c['id']}\n\n<details><summary>Hint 1 · Narrow the investigation</summary>\n\nCompare the observed failure against the component's declared configuration and recent changes. Separate the user-visible symptom from the failing dependency.\n\n</details>\n\n<details><summary>Hint 2 · Useful checks</summary>\n\n{c['checks']}\n\nThese are investigation prompts. Substitute actual lab resource names; uppercase names are placeholders.\n\n</details>\n\n<details><summary>Hint 3 · Likely cause</summary>\n\n{c['cause']}\n\n</details>\n")
        (p/'solution.md').write_text(f"# Solution · {c['id']}\n\n## Diagnosis supported by supplied evidence\n\n{c['cause']}\n\n## Investigate\n\n{c['checks']}\n\nCorrelate timestamps and recent changes. A similar symptom in a real environment can have a different cause.\n\n## Recovery\n\n{c['fix']}\n\n## Verify\n\n{c['verify']}\n\n## Prevent recurrence\n\n{c['prevent']}\n\n## Interview follow-ups\n\n- What evidence would invalidate this diagnosis?\n- What availability or data risk does the repair introduce?\n- How would you roll back if verification fails?\n- What would you tell the incident commander in 60 seconds?\n\nUse [the scoring rubric](../../../docs/PRACTICE.md) to assess your answer.\n")
        catalog.append(f"| {c['id']} | {c['level']} | [{c['title']}]({folder}/README.md) | {'**Runnable** · '+native if native else 'Evidence · Python only'} | {c['minutes']} min |")
        progress.append(f"- [ ] {c['id']} — {c['title']}")
    (ROOT/'CATALOG.md').write_text('\n'.join(catalog)+'\n')
    (ROOT/'PROGRESS.md').write_text('\n'.join(progress)+'\n')
if __name__=='__main__':build()
