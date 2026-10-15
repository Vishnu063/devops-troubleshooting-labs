# Runnable Kubernetes lab 025

Requires Docker, kubectl, and a local kind cluster named `devops-labs`. Use [setup](../../docs/LABS.md).

```bash
python3 lab.py up 025
kubectl --context kind-devops-labs -n devops-lab-025 get pods
kubectl --context kind-devops-labs -n devops-lab-025 get events --sort-by=.metadata.creationTimestamp
python3 lab.py check 025
```

Investigate the running resources and repair them with kubectl. The initial check should fail. `up` restores the original workload specification; use `down` followed by `up` for a clean reset including auxiliary resources.

The grader checks the expected Deployment and a request through the Service (startup-file case 023 checks the mounted file instead). A successful grader is a training check, not a complete production test.

[Repair reference — spoilers](solution.md) · [Incident brief](../../scenarios/level-1/025/README.md)
