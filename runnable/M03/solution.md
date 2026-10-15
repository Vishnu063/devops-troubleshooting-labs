# Repair reference M03

Compare `broken.json` with `fixed.json`; explain why every changed field matters. The reference is one valid repair, not an instruction to bypass the incident investigation.

```bash
kubectl --context kind-devops-labs apply -f runnable/M03/fixed.json
kubectl --context kind-devops-labs -n devops-lab-m03 rollout status deployment/web --timeout=120s
python3 lab.py check M03
python3 lab.py down M03
```

For 033, allow the monitoring system to complete fresh scrapes. For 081, wait for both Deployments to become ready. Cloud and supplied-evidence snapshots can differ from these deliberately small local analogues.

## Independent faults

An insufficient memory limit kills startup; an unrelated Service selector breaks routing even after the process survives.

Repair just one first and confirm that recovery still fails.
