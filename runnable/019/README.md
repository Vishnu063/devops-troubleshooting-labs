# Runnable lab 019

Level 1 · docker · [Incident brief](../../scenarios/level-1/019/README.md)

Prerequisites and isolation: [local setup](../../docs/LABS.md). Hidden practice: [sessions](../../docs/SESSIONS.md).

```bash
python3 lab.py up 019
python3 lab.py check 019
```

Investigate **.lab-state/019/compose.json and assets**. The first check must fail once setup has completed. Registry downloads and image startup can create unrelated early failures; inspect actual logs and events.

```bash
docker compose -p devopslab019 -f .lab-state/019/compose.json ps -a
docker compose -p devopslab019 -f .lab-state/019/compose.json logs
```

Edit the workspace Compose file or assets, then rerun `up`. Existing files are preserved. For mounted configuration changes, recreate the service or use the application's supported reload operation. The actual application and dependency run in containers; Linux cases reproduce the failure class inside an isolated container rather than modifying the host.

## Verify, repeat, clean up

```bash
python3 lab.py check 019 --samples 5 --interval 1
python3 lab.py reset 019
# The original fault should be present again.
python3 lab.py check 019
python3 lab.py down 019
```

The grader makes repeated checks and rejects restarts or container replacement during its observation window. Kubernetes checks use the workload and Service path; case 081 additionally probes every ready endpoint. Docker 033 queries actual scrape results; 049 performs a real database write/read round trip. See [verification limits](../../docs/LABS.md).

[Repair reference — spoilers](solution.md)
