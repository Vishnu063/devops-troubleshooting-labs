# DevOps Troubleshooting Labs

**100 incidents. Three difficulty levels. Diagnose first. Prove the recovery.**

Practice the failures DevOps engineers investigate across Linux, networking, Git, CI/CD, Docker, Kubernetes, AWS, Azure, GCP, Terraform, GitOps, security, and observability.

[Browse all 100 cases](CATALOG.md) · [Start practicing](docs/PRACTICE.md) · [Run a local fault](docs/LABS.md) · [Track progress](PROGRESS.md)

## Start in one minute

Requires Python 3.10+ and Git. The evidence drills need no Python packages, Docker, or cloud account.

```bash
git clone https://github.com/Vishnu063/devops-troubleshooting-labs.git
cd devops-troubleshooting-labs
python3 lab.py list --level 1
python3 lab.py show 023
python3 lab.py evidence 023
```

Write your diagnosis and recovery plan before opening hints or solutions.

```bash
python3 lab.py hint 023 --step 1
python3 lab.py hint 023 --step 2
python3 lab.py solution 023
python3 lab.py record 023 --score 7 --minutes 20 --hints 2
python3 lab.py progress
```

## Choose your challenge

| Level | Cases | Focus | Suggested time |
| --- | --- | --- | --- |
| 1 | 001–034 | Find the failing component and repair the immediate fault | 20 minutes |
| 2 | 035–067 | Correlate symptoms across deployments and dependencies | 35 minutes |
| 3 | 068–100 | Protect availability and data during complex recovery | 50 minutes |

Difficulty is a training guide. Real incidents can cross these boundaries.

```bash
python3 lab.py random --level 3
python3 lab.py list --tool Kubernetes
python3 lab.py list --runnable
```

**Make it harder:** set a timer, avoid hints, rank three hypotheses, explain what would disprove each, and give a 60-second incident update. The investigation should be difficult; finding the instructions should be easy.

## What you can practice today

- **100 supplied-evidence drills:** incident brief, concrete training observations, progressive hints, diagnosis, recovery guidance, verification, and prevention.
- **15 runnable local labs:** 2 Git, 3 Docker, and 10 Kubernetes faults, each with a recovery grader and cleanup.
- **Interview practice:** explain commands, tradeoffs, rollback, and user impact; use the [10-point rubric](docs/PRACTICE.md).
- **Local history:** record repeated attempts, elapsed time, hints, and self-assessed scores.
- **Contribution workflow:** issue templates, contribution guidance, and automated repository and native lab checks.

Evidence drills are synthetic case studies, not interactive cloud deployments. Native labs reproduce a specific fault; they are not complete replicas of a production platform. Each case is clearly labelled in the catalog. Cloud provisioning is not included.

## Run your first actual fault

No Docker required for this Git exercise:

```bash
python3 lab.py up 013
# Investigate the disposable repository at .lab-state/013/repo.
python3 lab.py check 013
# Resolve and commit the merge, preserving both intended changes.
python3 lab.py check 013
python3 lab.py down 013
```

The first check should fail. For Docker and Kubernetes prerequisites and exact isolation boundaries, read [local lab setup](docs/LABS.md). Nothing provisions paid cloud services.

## Coverage

| Area | Tools and services |
| --- | --- |
| Systems and traffic | Linux, SSH, DNS, TLS, Nginx, network routing |
| Source and delivery | Git, Jenkins, GitHub Actions, GitLab CI, Azure DevOps |
| Containers and GitOps | Docker, Kubernetes, Helm, Argo CD |
| Infrastructure | Terraform, Ansible |
| AWS | EC2, VPC, ALB, Auto Scaling, S3, IAM, RDS, Route 53, Lambda, EKS, Secrets Manager |
| Azure and GCP | AKS, ACR, Key Vault, GKE, Cloud Build, Artifact Registry, workload identities |
| Security and operations | Trivy, Snyk, SonarQube, Prometheus, Grafana, Alertmanager, ELK, Loki, incident response, disaster recovery |

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md). The [catalog](data/incidents.json) is the source of truth; regenerate casebooks with `python3 scripts/build_docs.py`.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
```

[Security reporting](SECURITY.md) · [MIT license](LICENSE)
