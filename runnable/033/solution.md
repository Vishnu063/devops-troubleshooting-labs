# Repair reference 033

Compare `broken.json` with `fixed.json`; explain why every changed field matters. The reference is one valid repair, not an instruction to bypass the incident investigation.

```bash
cp runnable/033/fixed.json .lab-state/033/compose.json
python3 lab.py up 033
python3 lab.py check 033
python3 lab.py down 033
```

For 033, allow the monitoring system to complete fresh scrapes. For 081, wait for both Deployments to become ready. Cloud and supplied-evidence snapshots can differ from these deliberately small local analogues.
