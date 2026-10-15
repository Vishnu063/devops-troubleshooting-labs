"""Shared runtime registry, including additional compound incidents."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUNTIMES=json.loads((ROOT/'data/runtimes.json').read_text())
RUNNABLE={i:r for i,r in RUNTIMES.items() if i.isdigit()}
COMPOUNDS=json.loads((ROOT/'data/compounds.json').read_text())
SYMPTOMS={
 '005':'Requests fail when the application reads its working data.',
 '006':'The newly deployed server does not stay running.',
 '010':'The application responds inside its container but users cannot reach it.',
 '012':'The public entry point returns gateway errors after a release.',
 '013':'Two approved configuration changes cannot be merged automatically.',
 '019':'The application exits immediately after release.',
 '020':'The application is running but its published entry point does not respond.',
 '021':'Requests no longer return the expected application document.',
 '023':'The application repeatedly restarts after release.',
 '024':'The new application instances never start.',
 '025':'The new workload never reaches serving capacity.',
 '026':'New application instances cannot complete startup.',
 '027':'Application instances look healthy, but requests through the entry point fail.',
 '033':'Application metrics have stopped appearing in the monitoring system.',
 '040':'The latest release introduced a regression; restore behavior while preserving shared history.',
 '049':'The application reports dependency errors when processing requests.',
 '050':'The workload keeps terminating during initialization.',
 '051':'Application instances are running but never enter service.',
 '052':'The application cannot finish initializing before it restarts.',
 '054':'The workload cannot find an internal dependency.',
 '056':'The application cannot start with its required persistent storage.',
 '057':'The new release does not complete and needs a recovery decision.',
 '080':'Replacement workloads are rejected during recovery.',
 '081':'Users report intermittent failures although application instances look healthy.',
 **{c['id']:c['symptom'] for c in COMPOUNDS}
}
