# Repair reference 081

Compare `broken.json` with `fixed.json`; explain why every changed field matters. The reference is one valid repair, not an instruction to bypass the incident investigation.

```bash
kubectl --context kind-devops-labs apply -f runnable/081/fixed.json
kubectl --context kind-devops-labs -n devops-lab-081 rollout status deployment/web --timeout=120s
python3 lab.py check 081
python3 lab.py down 081
```

For 033, allow the monitoring system to complete fresh scrapes. For 081, wait for both Deployments to become ready. Cloud and supplied-evidence snapshots can differ from these deliberately small local analogues.
