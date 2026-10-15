# Runnable Docker lab 019

Requires Docker Engine and Docker Compose v2. Ports bind to loopback with a dynamically assigned host port.

```bash
python3 lab.py up 019
docker compose -p devopslab019 -f .lab-state/019/compose.json ps -a
docker compose -p devopslab019 -f .lab-state/019/compose.json logs
python3 lab.py check 019
```

Edit `.lab-state/019/compose.json`, then rerun `up` to reconcile your changes. `up` preserves an existing workspace. Use `down` to remove containers and the workspace, then `up` for a clean reset.

[Repair reference — spoilers](solution.md)
