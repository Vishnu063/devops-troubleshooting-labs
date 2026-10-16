"""Offline setup checks and curated practice paths; never starts infrastructure."""
import shutil
import sys

TRACKS = {
    'git': ('Start here: no containers needed', ['013', '040']),
    'docker': ('Application startup, access, and dependencies', ['006', '010', '012', '033', '049']),
    'kubernetes': ('Startup, scheduling, configuration, and traffic', ['023', '024', '025', '026', '027', '051', '054']),
    'advanced': ('Rollout recovery and multiple independent faults', ['057', '080', '081', 'M01', 'M02', 'M03']),
}
REQUIRES = {
    'evidence': (), 'git': ('git',), 'docker': ('docker',),
    'kubernetes': ('docker', 'kind', 'kubectl'),
}


def doctor(runtime):
    print(f'Setup check: {runtime} (local executable checks only)')
    ready = sys.version_info >= (3, 10)
    print(f"{'OK' if ready else 'MISSING'} Python 3.10+")
    for name in REQUIRES[runtime]:
        found = shutil.which(name)
        print(f"{'OK' if found else 'MISSING'} {name}")
        ready = ready and bool(found)
    if runtime in ('docker', 'kubernetes'):
        print('MANUAL: docker info and docker compose version must succeed.')
        print('Image downloads need registry access. This check does not contact Docker or a cluster.')
    if runtime == 'kubernetes':
        print('MANUAL: use only the dedicated kind-devops-labs context; see docs/LABS.md.')
    print('Executable checks passed; runtime readiness is not verified.' if ready else
          'Install missing tools, then repeat this check. Evidence practice needs only Python.')
    return 0 if ready else 2


def track(name, select, runtimes):
    title, ids = TRACKS[name]
    print(f'{name.title()} practice path — {title}')
    print('Work in order. No labs have been started and no solutions are shown.')
    for ident in ids:
        case = select(ident)
        print(f"{ident}  L{case['level']}  {case['title']}  [{runtimes[ident]}]")
    first = ids[0]
    runtime = runtimes[first]
    print(f'\nCheck setup: python3 lab.py doctor --runtime {runtime}')
    print(f'Read brief:  python3 lab.py show {first}')
    print(f'Start fault: python3 lab.py up {first}')
    print(f'Check fix:   python3 lab.py check {first}')
    print(f'Clean up:    python3 lab.py down {first}')
    print('Read docs/START_HERE.md for the first-lab walkthrough.')
    return 0
