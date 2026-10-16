# DevOps Troubleshooting Labs

[Reviewer walkthrough](INTERVIEW.md) · [Portfolio](https://github.com/Vishnu063/Vishnu063/blob/main/PORTFOLIO.md)

**100 scenarios. Three difficulty levels. Real faults, hidden incidents, and proof of recovery.**

[All 100 scenarios](CATALOG.md) · [Compound incidents](COMPOUNDS.md) · [Local lab setup](docs/LABS.md) · [Timed sessions](docs/SESSIONS.md) · [Practice method](docs/PRACTICE.md)

## New here?

Start with [your first lab](docs/START_HERE.md): a local Git incident with an expected failing check, room to investigate, and a recovery check. No cloud account or containers needed.

```bash
python3 lab.py doctor --runtime git
python3 lab.py track git
```

Already comfortable with Git? Choose `track docker`, `track kubernetes`, or `track advanced`. Paths print an ordered practice plan; they do not start resources. The setup checker checks local executables only.

## Pick your practice

| Mode | Available now | What you do |
| --- | --- | --- |
| Evidence investigations | All 100 scenarios | Interpret synthetic evidence and defend your recovery plan |
| Runnable scenarios | **24 of the 100** | Repair actual isolated Git, Docker, or Kubernetes failures |
| Compound incidents | **3 additional runnable labs** | Diagnose two independent faults; one repair is insufficient |
| Hidden timed sessions | All cases and compounds | Start from symptoms, track time and hints, record the result |

The final 100 IDs and Level 1/2/3 boundaries remain unchanged. **76 scenarios are evidence-only.** Cloud cases do not provision resources. Local faults reproduce a specific failure class rather than an entire production platform.

## Start in one minute

Requires Git and Python 3.10+. Evidence drills need no Python packages, Docker, or cloud account.

```bash
git clone https://github.com/Vishnu063/devops-troubleshooting-labs.git
cd devops-troubleshooting-labs
python3 lab.py list --level 1
python3 lab.py show 023
python3 lab.py evidence 023
```

Investigate first. Hints and solutions are separate:

```bash
python3 lab.py hint 023 --step 1
python3 lab.py solution 023
```

## Ready for a challenge?

```bash
python3 lab.py session start --hidden --runnable --level 1
python3 lab.py session up
python3 lab.py session status
python3 lab.py session check
python3 lab.py session finish --score 8
```

Docker or Kubernetes prerequisites depend on the randomly chosen runtime. Add `--tool Git` for a no-Docker session. Hidden briefs omit the title and case ID; inspection paths and source files remain readable. The timer includes setup time and does not remove resources automatically. See [session rules and limits](docs/SESSIONS.md).

## Levels and prerequisites

| Level | Cases | Investigation focus | Target |
| --- | --- | --- | --- |
| 1 | 001–034 | Identify the immediate failure and repair it | 20 min |
| 2 | 035–067 | Correlate deployment and dependency problems | 35 min |
| 3 | 068–100 | Recover while protecting availability and data | 50 min |
| Compound | M01–M03 | Diagnose multiple independent failures | 60 min |

| Runtime | Required tools | Runnable scenarios |
| --- | --- | --- |
| Git | Git + Python | 013, 040 |
| Docker | Docker Engine + Compose v2 + Python | 005, 006, 010, 012, 019, 020, 021, 033, 049 |
| Kubernetes | Docker + kind + kubectl + Python | 023–027, 050–052, 054, 056, 057, 080, 081; plus M01–M03 |

Registry access is required for image downloads. Kubernetes labs use only the dedicated local `kind-devops-labs` context. No command provisions paid cloud services.

## Run, verify, reset

```bash
python3 lab.py up 013
# Investigate .lab-state/013/repo and resolve the merge.
python3 lab.py check 013
python3 lab.py reset 013
python3 lab.py down 013
```

A check should fail in the original broken state. Networked checks make repeated requests and reject restarts or container replacement during the observation window. Special checks cover monitoring scrape results, a database write/read round trip, persistent-volume writes, workload DNS, and every ready endpoint in the mixed-version incident.

```bash
python3 lab.py check 081 --samples 5 --interval 1
python3 lab.py list --runnable
python3 lab.py list --compound
python3 lab.py random --level 3
```

Short local checks do not replace a production stability window or full data-integrity validation.

## Build a practice record

```bash
python3 lab.py progress
python3 lab.py session path
python3 lab.py session start --level 2 --unlock --hidden
```

Optional unlocking requires three qualifying distinct completions at the previous level. Native sessions must pass their recovery check; all explanation scores are self-assessed. Omit `--unlock` for unrestricted practice. Use the [incident report template](templates/incident-report.md) to document your reasoning.

## Coverage

| Area | Technologies |
| --- | --- |
| Systems and traffic | Linux, SSH, DNS, TLS, Nginx, routing |
| Delivery | Git, Jenkins, GitHub Actions, GitLab CI, Azure DevOps |
| Containers and GitOps | Docker, Kubernetes, Helm, Argo CD |
| Infrastructure | Terraform, Ansible |
| AWS | EC2, VPC, ALB, Auto Scaling, S3, IAM, RDS, Route 53, Lambda, EKS, Secrets Manager |
| Azure and GCP | AKS, ACR, Key Vault, GKE, Cloud Build, Artifact Registry, workload identity |
| Security and operations | Trivy, Snyk, SonarQube, Prometheus, Grafana, Alertmanager, ELK, Loki, incident response, recovery |

## Contribute and validate

The [catalog](data/incidents.json) and [runtime registry](data/runtimes.json) are the source of truth. Read [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
python3 scripts/build_docs.py
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
```

CI checks repository integrity, original faults, incomplete compound repairs, repeated recovery checks, reset, and cleanup on disposable environments.

[Security reporting](SECURITY.md) · [MIT license](LICENSE)
