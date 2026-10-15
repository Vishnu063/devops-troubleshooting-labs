# Contributing

Keep the final 100 case IDs and level boundaries stable. Improve an existing case before proposing a new catalog entry. Explain whether your contribution is an evidence drill or an executable fault.

1. Edit `data/incidents.json` for case content.
2. Keep evidence synthetic, plausible, and free of real identities or credentials.
3. For native labs, include broken configuration, an independently useful repair, live recovery checks, prerequisites, and cleanup.
4. Avoid host-level failure injection, paid cloud provisioning, and changes outside the dedicated lab boundary.
5. Regenerate documents and run checks:

```bash
python3 scripts/build_docs.py
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
```

For a native lab change, prove the original fault fails grading and the repaired lab passes. Include actual output and runtime versions in your PR. Do not label a supplied-evidence exercise as an executed cloud deployment.

Solutions belong in separate files. Briefs should state impact and goals without handing over the repair. Tests must verify recovery behavior rather than just the existence of a resource.

Use the issue templates for broken labs or improvements. Do not include secrets or confidential incident logs.

Runtime assignments live in `data/runtimes.json`; the extra compound catalog is `data/compounds.json`. Preserve all original 100 IDs and level boundaries. New compound incidents must stay outside that catalog.

For runtime changes, CI must observe the intended fault, verify recovery with repeated checks, reset to the original failure, and clean up. A compound must also reject an incomplete repair. Session changes must retain honest distinctions between self-assessed explanations and native recovery verification.

Regenerate per-lab CI steps after runtime registry changes with `python3 scripts/build_workflow.py`. This keeps every executable scenario visible as its own step while reusing one Docker runner and one local Kubernetes cluster.
