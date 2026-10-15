# Repair reference M02

Compare `broken.json` with `fixed.json`; explain why every changed field matters. The reference is one valid repair, not an instruction to bypass the incident investigation.

```bash
kubectl --context kind-devops-labs apply -f runnable/M02/fixed.json
kubectl --context kind-devops-labs -n devops-lab-m02 rollout status deployment/web --timeout=120s
python3 lab.py check M02
python3 lab.py down M02
```

For 033, allow the monitoring system to complete fresh scrapes. For 081, wait for both Deployments to become ready. Cloud and supplied-evidence snapshots can differ from these deliberately small local analogues.

## Independent faults

An impossible CPU request prevents scheduling; an incorrect readiness path excludes the application after scheduling is repaired.

Repair just one first and confirm that recovery still fails.
