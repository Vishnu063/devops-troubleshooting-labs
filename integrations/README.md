# Disposable ecosystem acceptance

Reuse CloudLaunch's real application, Platform's monitoring configuration and Ops Pilot's existing Triage engine. AI is disabled. This is a local development lab, never a production failure injector.

## Setup and run

Keep the five checkouts as siblings. Use their existing checkouts; no worktree is needed. Install Python 3.12, local Docker with Compose, and the application requirements. Install Ops Pilot and its pinned Triage dependency into `ecosystem-venv`; for cross-repository development install both editable checkouts with `--no-deps` after build prerequisites are installed. Platform's hash-locked requirements must be installed separately from CloudLaunch's range-based requirements.

Supply trusted Prometheus 3.7.0, promtool, Alertmanager 0.28.1 and amtool binaries in a private tools directory. One reproducible source is the official `prom/prometheus:v3.7.0` and `prom/alertmanager:v0.28.1` Docker images: pull, create a stopped container, copy `/bin/{prometheus,promtool}` or `/bin/{alertmanager,amtool}`, and remove only that temporary container. Docker verifies image layers; record resolved image digests. Do not disable TLS or checksum verification. Managed cloud builds mount the existing system CA using BuildKit's `proxy_ca` secret; no CA or credential is embedded in the application image.

```sh
/path/to/ecosystem-venv/bin/python integrations/ecosystem_lab.py \
  --workspace /absolute/parent/of/checkouts --tools /absolute/monitoring-tools \
  --output /absolute/private/evidence --allow-disposable-failure
```

The explicit flag authorizes the runner's fixed disposable policy: create a uniquely named local project, stop only its app, create a restart proposal, assert unapproved execution is refused, approve and run that exact plan, verify HTTP/database recovery, and clean up its project. It does not authorize production remediation. Normal dashboard users still approve and execute separately. Without the flag, nothing is deployed. `--skip-build` reuses only an image tagged with the current build-input hash; it is useful after a diagnosis that does not change app sources. No service is started by default just by installing a project. The lab Compose file has an `ecosystem-lab` profile; the runner enables only that explicit profile.

The runner binds monitoring and Pilot to loopback and publishes app/database ports only on loopback. It saves private results and removes its temporary ingress token on exit. A successful run must show the expected starting failure, real alert firing, delivery, evidence, approval refusal, approved repair, verified recovery and resolved alert. `result.json` reports incomplete steps as failures; it never turns an unavailable service into a pass. Inspect private logs locally; redact before sharing.

## Scenario reuse matrix

These scenarios reuse existing lab graders; Kubernetes and Jenkins scenarios are not claimed as integrated Docker-flow tests. Each linked lab includes its native injection, diagnostics, repair, repeated recovery checks and cleanup.

| Failure | Setup / injection | Expected alert and evidence | Diagnosis and safe remediation | Verification / cleanup |
| --- | --- | --- | --- | --- |
| App container stopped | Run `ecosystem_lab.py` above; it stops its app | Actual `CloudLaunchApplicationDown`, stopped ID, failed HTTP and bounded log signatures | Existing Triage stopped-container rule; explicit lab-only approved restart | Container identity + two HTTP successes + DB readiness + actual alert resolution; automatic project cleanup |
| Health endpoint failure | Ops Pilot existing `test_real_restart_with_wrong_application_endpoint_is_not_success` disposable Docker test | Failed HTTP while container is running | Do not confuse running with recovery; repair the endpoint/config separately | Test requires `needs_attention`; its own cleanup removes only labelled test containers |
| CrashLoopBackOff | `python lab.py up 023` in the dedicated kind context | Pod state/events; optional kube-state-metrics restart alert when scraped | [023](../runnable/023/README.md) existing diagnosis and reviewed startup repair | `python lab.py check 023 --samples 5`; `python lab.py down 023` |
| ImagePullBackOff | `python lab.py up 024` | Image pull errors in deployment-owned events; alert requires Kubernetes monitoring | [024](../runnable/024/README.md); review image/registry settings, no blind restart | Existing repeated grader; `python lab.py down 024` |
| Missing environment/config | `python lab.py up 026` | Missing configuration reference and pod events | [026](../runnable/026/README.md); repair only lab configuration | Existing grader; `python lab.py down 026` |
| Failed rollout | `python lab.py up 057` | Stalled deployment generation/replicas/events | [057](../runnable/057/README.md); review template and rollout; separate authorization for rollback | Existing rollout/service grader; `python lab.py down 057` |
| Resource exhaustion | `python lab.py up 050` | Runtime OOMKilled, limits and events; restart rule requires kube-state-metrics | [050](../runnable/050/README.md); bound resources, diagnose memory growth | Existing grader; `python lab.py down 050`; never exhaust host memory |
| Broken service config | `python lab.py up 027` | Service selector differs from pod labels; workload may still be running | [027](../runnable/027/README.md); repair only lab selector | Existing service-path grader; `python lab.py down 027` |
| Jenkins deployment failure | Existing [017 evidence drill](../scenarios/level-1/017/README.md), or disposable Jenkins job with no Docker permission | Jenkins failure evidence; optional deployment-failed event, never a fabricated successful deployment | Review agent socket authorization; do not make socket world writable | Rerun only disposable job; remove only that job/agent. Compose-only acceptance does not establish controller execution; the separate recorded Jenkins builds do |
| Failed recovery verification | Existing real Ops Pilot Docker test named above | Container restart succeeds, wrong HTTP endpoint still fails | Leave incident `needs_attention`; no repeated repair or automatic rollback | Test asserts failed application verification and consumed approval; labelled cleanup |

Run Ops Pilot's existing real Docker safety tests with `OPS_PILOT_DOCKER_LAB=1 python -m unittest discover -s tests -p test_docker_lab.py -v`. Kubernetes labs require their explicit isolated context and namespace. Their setup does not connect production by default.

## Resources and limits

App and database each have a 192 MiB memory limit and 0.5 CPU quota. Monitoring binaries are temporary host processes; their combined peak memory is not inferred from container limits. The measured app snapshot and elapsed time are in `result.json`. This does not demonstrate that all five projects, Jenkins, Grafana and Kubernetes fit in 8 GB. No model or cluster is started. Existing node-exporter/cAdvisor/kube-state-metrics must be separately configured for resource/restart alert rules. No resource alert is claimed verified unless its controlled failure is exercised.

CloudLaunch includes an optional `integrations/Jenkinsfile.ecosystem` wrapper for this exact runner. A local Compose acceptance result does not establish that a Jenkins controller executed it. Pass optional `--grafana-home /path/to/trusted/grafana` to verify authenticated six-panel provisioning and live Prometheus datasource queries. This flag is disabled by default and starts Grafana only for the test. That API-level validation passed; browser visual acceptance remains unrun because the Chromium CDN is blocked. Grafana dashboard JSON is provided by Platform; alert history is limited by Prometheus retention and is not an immutable incident database. Logs remain bounded Triage signatures; Grafana does not store logs.
