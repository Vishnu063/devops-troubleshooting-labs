# Runnable Docker lab 020

Requires Docker Engine and Docker Compose v2. Ports bind to loopback with a dynamically assigned host port.

```bash
python3 lab.py up 020
docker compose -p devopslab020 -f .lab-state/020/compose.json ps -a
docker compose -p devopslab020 -f .lab-state/020/compose.json logs
python3 lab.py check 020
```

Edit `.lab-state/020/compose.json`, then rerun `up` to reconcile your changes. `up` preserves an existing workspace. Use `down` to remove containers and the workspace, then `up` for a clean reset.

[Repair reference — spoilers](solution.md)
