# Run local faults

Run commands from the repository root. Read a case with `python3 lab.py show ID`, or use a [hidden session](SESSIONS.md) to avoid its title.

## Lab inventory

| Runtime | IDs | Prerequisites |
| --- | --- | --- |
| Git | 013, 040 | Git and Python 3.10+ |
| Docker | 005, 006, 010, 012, 019, 020, 021, 033, 049 | Docker Engine, Compose v2, registry access |
| Kubernetes | 023–027, 050–052, 054, 056, 057, 080, 081 | Docker, kind, kubectl, registry access |
| Additional compounds | M01–M03 | Same Kubernetes prerequisites |

There are **24 runnable scenarios out of the final 100**, plus three compound incidents. The remaining **76** are supplied-evidence investigations with no infrastructure setup or automated repair grader. A local analogue can reproduce the same failure class with a smaller application or dependency than the supplied case study.

## Git

`up` creates an isolated repository under `.lab-state/ID/repo`, without a remote. The grader requires a clean committed result and verifies that the baseline commits remain ancestors of HEAD.

- 013: preserve TIMEOUT=60 from feature and RETRIES=5 from main in a merge commit.
- 040: restore TIMEOUT=30 and RETRIES=3 through a new commit while preserving existing history.

Git checks are a single repository-state validation; networked stability sampling does not apply.

## Docker

Published HTTP ports bind to loopback, with Docker assigning the host port. `up` prints an editable workspace. Compose settings and files under its `assets/` directory are preserved on repeated `up` calls.

```bash
python3 lab.py up 012
docker compose -p devopslab012 -f .lab-state/012/compose.json ps -a
docker compose -p devopslab012 -f .lab-state/012/compose.json logs
python3 lab.py check 012
```

After editing Compose settings, rerun `up`. For a mounted configuration edit, use the application's supported reload or recreate the service:

```bash
docker compose -p devopslab012 -f .lab-state/012/compose.json up -d --force-recreate
```

Cold image downloads can take time. Establish registry access before interpreting failures. Linux cases 005 and 006 reproduce actual file-permission and port-conflict failures inside containers, leaving the host unchanged. Case 049 uses Redis as its actual database dependency rather than the generic database in the supplied evidence.

## Kubernetes

Use only a dedicated local kind cluster. Install compatible Docker, kind, and kubectl versions using their official instructions. Allow several GiB of memory and sufficient disk for the node and images; run one lab at a time on a small machine.

```bash
kind create cluster --name devops-labs --wait 120s
kubectl --context kind-devops-labs get nodes
python3 lab.py up 027
kubectl --context kind-devops-labs -n devops-lab-027 get pods,svc
python3 lab.py check 027
```

The CLI explicitly selects `kind-devops-labs`, requires kind node provider IDs and expected node names, and checks namespace ownership before modifying an existing namespace. It does not use your current context implicitly. This is an accident-prevention boundary for a local practice environment, not a security sandbox against a hostile cluster administrator.

Each case owns one labelled namespace. Compound namespace suffixes are lowercase, for example `devops-lab-m01`. The checker requires the expected Deployment(s) to be available and usually sends traffic through the Service.

```bash
kubectl --context kind-devops-labs -n devops-lab-027 rollout status deployment/web --timeout=120s
python3 lab.py check 027
```

Special cases:

- 023: checks the required mounted startup configuration.
- 054: checks DNS resolution from the affected workload as well as the Service request path.
- 056: writes and reads a marker in the mounted volume. Requires kind's `standard` StorageClass. The repair replaces only its disposable unbound claim because storageClassName cannot be changed in place.
- 080: reproduces quota admission failure using a BestEffort pod quota; the evidence drill uses CPU quota. The common investigation is admission rejection during recovery.
- 081: requires both Deployments and probes every ready Service endpoint, preventing one healthy replica from masking an incompatible endpoint.

## Stronger recovery checks

```bash
python3 lab.py check 081 --samples 5 --interval 1
```

Defaults are three checks one second apart. `--samples` accepts 1–10; `--interval` accepts 0–10 seconds. The check rejects changes in container identity, start time, or restart count during the observation window. Kubernetes observes pod identities and restart counts in its lab namespace. Wait for an intended rollout to settle before grading.

Docker 033 checks both the real Prometheus `up` result and a known scraped metric. Docker 049 performs an actual Redis write/read round trip on each application request. Volume and database checks use disposable training data; they do not certify all data integrity or prove durability across infrastructure loss. The local observation window is short and does not replace production monitoring.

## One-command reset and cleanup

```bash
python3 lab.py reset 027
python3 lab.py down 027
```

Reset removes the selected lab, waits for Kubernetes namespace deletion when needed, and recreates the original broken state. It does not reset practice history. In a session it also preserves the original timer, hints, and reveal status.

- Git cleanup deletes only its disposable lab repository and baseline metadata.
- Docker cleanup removes its Compose project, project volumes, and workspace.
- Kubernetes cleanup requests deletion of its labelled namespace, including disposable claims. Volume reclamation follows the StorageClass policy.
- Kubernetes `up` alone reapplies the broken specification but may retain auxiliary repair resources. Use `reset` for a clean start.
- If namespace deletion exceeds the reset wait, inspect termination and retry after it finishes.
- `.practice/` history survives cleanup. Sessions do not remove resources automatically when time expires or when you finish.

After all Kubernetes practice:

```bash
kind delete cluster --name devops-labs
```

## Solutions and verification in CI

Each native folder includes a separate `solution.md` and reference repair. Opening the fixed configuration reveals the fault. In hard mode, inspect live state first.

CI verifies original faults, successful repairs, repeated checks, reset back to a broken state, and cleanup. For compound incidents it additionally applies an incomplete repair and verifies that recovery still fails. Cloud cases remain synthetic evidence drills; these tests do not execute real cloud incidents.
