"""Generate per-lab CI steps without starting a separate cluster for each case."""
from pathlib import Path
from registry import RUNTIMES
ROOT=Path(__file__).resolve().parents[1]
HEADER='''name: Validate drills and runnable labs
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: labs-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  repository:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python3 -m unittest discover -s tests -v
      - run: python3 scripts/validate.py
      - name: Generated files stay in sync
        run: |
          python3 scripts/build_docs.py
          python3 scripts/build_workflow.py
          git diff --exit-code
'''
COMMON='''    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
'''
CLUSTER='''      - name: Install pinned kind binary
        run: |
          curl -fsSLo kind https://kind.sigs.k8s.io/dl/v0.27.0/kind-linux-amd64
          chmod +x kind
          sudo mv kind /usr/local/bin/kind
      - name: Create disposable cluster
        run: kind create cluster --name devops-labs --wait 120s
'''
FOOTER='''      - name: Collect Kubernetes diagnostics on failure
        if: failure()
        run: |
          kubectl --context kind-devops-labs get pods -A -o wide || true
          kubectl --context kind-devops-labs get events -A --sort-by=.metadata.creationTimestamp || true
      - name: Delete disposable cluster
        if: always()
        run: kind delete cluster --name devops-labs
'''
def build():
 text=HEADER
 for runtime,timeout in [('docker',20),('kubernetes',35)]:
  text+=f'  {runtime}:\n    runs-on: ubuntu-latest\n    timeout-minutes: {timeout}\n'+COMMON
  if runtime=='kubernetes':text+=CLUSTER
  for i in sorted(k for k,v in RUNTIMES.items() if v==runtime):
   text+=f'      - name: "{i} — fault, repair, stability, reset"\n        run: python3 scripts/ci_native.py {runtime} --id {i}\n'
  if runtime=='kubernetes':text+=FOOTER
 (ROOT/'.github/workflows/validate.yml').write_text(text)
if __name__=='__main__':build()
