# Runnable lab 051

Level 2 · kubernetes · [Incident brief](../../scenarios/level-2/051/README.md)

Prerequisites and isolation: [local setup](../../docs/LABS.md). Hidden practice: [sessions](../../docs/SESSIONS.md).

```bash
python3 lab.py up 051
python3 lab.py check 051
```

Investigate **namespace devops-lab-051**. The first check must fail once setup has completed. Registry downloads and image startup can create unrelated early failures; inspect actual logs and events.

```bash
kubectl --context kind-devops-labs -n devops-lab-051 get pods,svc
kubectl --context kind-devops-labs -n devops-lab-051 get events --sort-by=.metadata.creationTimestamp
```

Repair live resources using kubectl. `up` reapplies the broken resources but does not remove auxiliary resources from an earlier repair. `reset` gives a clean namespace.

## Verify, repeat, clean up

```bash
python3 lab.py check 051 --samples 5 --interval 1
python3 lab.py reset 051
# The original fault should be present again.
python3 lab.py check 051
python3 lab.py down 051
```

The grader makes repeated checks and rejects restarts or container replacement during its observation window. Kubernetes checks use the workload and Service path; case 081 additionally probes every ready endpoint. Docker 033 queries actual scrape results; 049 performs a real database write/read round trip. See [verification limits](../../docs/LABS.md).

[Repair reference — spoilers](solution.md)
