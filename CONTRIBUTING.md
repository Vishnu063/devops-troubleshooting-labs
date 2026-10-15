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
