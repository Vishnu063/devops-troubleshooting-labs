# Run local faults

Run commands from the repository root. First read the incident brief with `python3 lab.py show ID`.

## Lab inventory

| Runtime | IDs | Prerequisites |
| --- | --- | --- |
| Git | 013, 040 | Git and Python 3.10+ |
| Docker | 019, 020, 021 | Docker Engine, Compose v2, image registry access |
| Kubernetes | 023, 024, 025, 026, 027, 050, 051, 052, 056, 057 | Docker, kind, kubectl, image registry access |

The remaining 85 cases are supplied-evidence investigations. They have no infrastructure setup or automated repair grader.

## Git

`up` creates an isolated repository under `.lab-state/ID/repo`. No remote is configured. Repair it using normal Git commands. The grader expects a clean committed result. Case 013 must preserve TIMEOUT=60 from the feature branch and RETRIES=5 from main in a merge commit. Case 040 must preserve history while restoring TIMEOUT=30 and RETRIES=3 through a new commit.

## Docker

Use a development machine with Docker available. Labs bind HTTP ports to loopback; Docker assigns the host port. `up` prints the editable Compose workspace. It preserves existing edits, so rerun it after changing that file.

```bash
python3 lab.py up 020
docker compose -p devopslab020 -f .lab-state/020/compose.json ps -a
docker compose -p devopslab020 -f .lab-state/020/compose.json logs
python3 lab.py check 020
```

A cold image download can take time. Establish registry access before interpreting application faults. The grader makes a real HTTP request through the published port and checks the expected nginx page. It does not merely check that a container exists.

## Kubernetes

Use a dedicated local kind cluster. Install current compatible Docker, kind, and kubectl versions using their official documentation. Allow several GiB of memory and enough disk space for the node and images; actual requirements depend on your system. Run one lab at a time on a small machine.

```bash
kind create cluster --name devops-labs --wait 120s
kubectl --context kind-devops-labs get nodes
python3 lab.py up 027
kubectl --context kind-devops-labs -n devops-lab-027 get pods,svc
python3 lab.py check 027
```

The CLI explicitly targets `kind-devops-labs` and checks expected node names. It never chooses your current kubectl context implicitly. Use this only with the dedicated local kind cluster. Each lab owns one labelled namespace. Checks require the expected Deployment to be available and usually make a real HTTP request through its Service. Case 023 checks its required configuration; 056 also checks volume writes.

Pod startup and image downloads take time. Inspect the events rather than interpreting every early failure as the intended fault. After repair, wait for readiness before grading:

```bash
kubectl --context kind-devops-labs -n devops-lab-027 rollout status deployment/web --timeout=120s
python3 lab.py check 027
```

Case 056 requires kind's `standard` StorageClass. Check `kubectl --context kind-devops-labs get storageclass`. Its repair replaces only the unbound disposable lab claim because storageClassName cannot be changed in place.

## Reset and cleanup

```bash
python3 lab.py down 027
# Wait for namespace deletion before recreating the same Kubernetes lab.
python3 lab.py up 027
```

- Git cleanup deletes only the selected lab repository.
- Docker cleanup removes only the selected Compose project and its workspace.
- Kubernetes cleanup requests deletion of the selected labelled namespace, including its disposable claims. Persistent-volume cleanup also depends on its StorageClass reclaim policy.
- Kubernetes `up` reapplies the broken workload but does not remove auxiliary resources from an earlier repair. Use `down`, wait for namespace deletion, then `up` for a full reset.
- Practice scores in `.practice/` survive lab cleanup.

After all Kubernetes labs are finished:

```bash
kind delete cluster --name devops-labs
```

## Solutions and limits

Each runnable folder has a separate `solution.md` and reference repair. Opening the fixed manifest reveals the fault. In hard mode, use only live inspection until you have written your diagnosis.

These are intentionally small fault reproductions. A passing grader validates the listed local behavior; production recovery also requires impact checks, dependency health, data integrity, and an observation window. Do not run these faults in shared or production environments.
