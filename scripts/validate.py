"""Check catalog completeness, native lab references, and local Markdown links."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_docs import RUNNABLE

def validate():
    errors=[]
    cases=json.loads((ROOT/'data/incidents.json').read_text())
    if [c['id'] for c in cases]!=[f'{i:03}' for i in range(1,101)]:errors.append('Catalog IDs must be ordered 001–100 exactly once.')
    for c in cases:
        expected=1 if int(c['id'])<=34 else 2 if int(c['id'])<=67 else 3
        if c['level']!=expected:errors.append(f"Wrong level: {c['id']}")
        for key in ['title','evidence','cause','checks','fix','verify','prevent']:
            if not c.get(key):errors.append(f"Missing {key}: {c['id']}")
        folder=ROOT/f"scenarios/level-{c['level']}/{c['id']}"
        for name in ['README.md','evidence.md','hints.md','solution.md']:
            if not (folder/name).exists():errors.append(f'Missing {folder/name}')
    for i,runtime in RUNNABLE.items():
        names=['README.md','solution.md']+(['broken.json','fixed.json'] if runtime!='git' else [])
        for name in names:
            p=ROOT/'runnable'/i/name
            if not p.exists():errors.append(f'Missing native asset {p}')
            elif p.suffix=='.json':json.loads(p.read_text())
    for path in ROOT.rglob('*.md'):
        if '.lab-state' in path.parts:continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text()):
            if '://' in target or target.startswith(('#','mailto:')):continue
            target=target.split('#')[0]
            if target and not (path.parent/target).exists():errors.append(f'Broken link in {path.relative_to(ROOT)}: {target}')
    for error in errors:print(error)
    if not errors:print(f'PASS: 100 cases, {len(RUNNABLE)} native labs, complete casebooks, and local Markdown links.')
    return bool(errors)
if __name__=='__main__':sys.exit(validate())
