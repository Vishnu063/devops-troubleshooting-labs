# DevOps Troubleshooting Labs: reviewer guide

100 evidence investigations, 24 runnable standard labs, and three additional compound incidents.

## Start the review

Demonstrate a failing Git lab, repair it, verify recovery, and explain why supplied evidence differs from a live fault.

| Source | Review focus |\n| --- | --- |\n| [lab.py](lab.py) | Implementation, assumptions, and operational boundaries |\n| [.github/workflows/validate.yml](.github/workflows/validate.yml) | Triggers, credentials, failure handling, and deploy conditions |\n| [scripts/build_docs.py](scripts/build_docs.py) | Implementation, assumptions, and operational boundaries |\n| [scripts/build_workflow.py](scripts/build_workflow.py) | Triggers, credentials, failure handling, and deploy conditions |\n| [scripts/ci_native.py](scripts/ci_native.py) | Implementation, assumptions, and operational boundaries |\n| [scripts/native.py](scripts/native.py) | Implementation, assumptions, and operational boundaries |

## First demonstration

From a checked-out repository, start with:

```bash
python3 lab.py doctor --runtime git
python3 lab.py track git
```

The doctor and track commands only print checks and guidance. Follow the first-lab guide for an actual failing-state and repair demonstration.

## A useful interview walkthrough

1. State the problem and the specific part you implemented or changed.
2. Open the source above and follow one request, release, or failure from start to finish.
3. Show a reproducible result, including an actual failure and the observation that confirms recovery.
4. Explain one tradeoff and one limitation. Distinguish a local test from a live deployment.

## Evidence and limits

This guide is based on the default-branch source inspected on 16 October 2026. It is a source review, not a fresh deployment or a certification of every feature. Existing CI runs and tests should be checked at the commit being demonstrated. Do not present screenshots, inherited code, planned features, or old README statements as proof of a current deployment.
