# Runnable Docker lab 021

Requires Docker Engine and Docker Compose v2. Ports bind to loopback with a dynamically assigned host port.

```bash
python3 lab.py up 021
docker compose -p devopslab021 -f .lab-state/021/compose.json ps -a
docker compose -p devopslab021 -f .lab-state/021/compose.json logs
python3 lab.py check 021
```

Edit `.lab-state/021/compose.json`, then rerun `up` to reconcile your changes. `up` preserves an existing workspace. Use `down` to remove containers and the workspace, then `up` for a clean reset.

[Repair reference — spoilers](solution.md)
