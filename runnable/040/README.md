# Runnable lab 040

Level 2 · git · [Incident brief](../../scenarios/level-2/040/README.md)

Prerequisites and isolation: [local setup](../../docs/LABS.md). Hidden practice: [sessions](../../docs/SESSIONS.md).

```bash
python3 lab.py up 040
python3 lab.py check 040
```

Investigate **.lab-state/040/repo**. The first check must fail once setup has completed. Registry downloads and image startup can create unrelated early failures; inspect actual logs and events.

```bash
git -C .lab-state/040/repo status
git -C .lab-state/040/repo log --all --oneline --graph
```

Repair and commit the configuration while preserving the existing history. This disposable repository has no remote.

## Verify, repeat, clean up

```bash
python3 lab.py check 040 --samples 5 --interval 1
python3 lab.py reset 040
# The original fault should be present again.
python3 lab.py check 040
python3 lab.py down 040
```

The grader makes repeated checks and rejects restarts or container replacement during its observation window. Kubernetes checks use the workload and Service path; case 081 additionally probes every ready endpoint. Docker 033 queries actual scrape results; 049 performs a real database write/read round trip. See [verification limits](../../docs/LABS.md).

[Repair reference — spoilers](solution.md)
