# The final 100 scenarios

Every case has a supplied-evidence drill. Cases marked **Runnable** also have a reproducible local fault. Cloud cases do not provision infrastructure.

| ID | Level | Incident | Practice / prerequisites | Target |
| --- | --- | --- | --- | --- |
| 001 | 1 | [Linux: Service stopped](scenarios/level-1/001/README.md) | Evidence · Python only | 20 min |
| 002 | 1 | [Linux: High CPU](scenarios/level-1/002/README.md) | Evidence · Python only | 20 min |
| 003 | 1 | [Linux: Out of memory](scenarios/level-1/003/README.md) | Evidence · Python only | 20 min |
| 004 | 1 | [Linux: Disk full](scenarios/level-1/004/README.md) | Evidence · Python only | 20 min |
| 005 | 1 | [Linux: File permissions](scenarios/level-1/005/README.md) | **Runnable** · docker | 20 min |
| 006 | 1 | [Linux: Port occupied](scenarios/level-1/006/README.md) | **Runnable** · docker | 20 min |
| 007 | 1 | [Linux: Cron environment](scenarios/level-1/007/README.md) | Evidence · Python only | 20 min |
| 008 | 1 | [SSH: Cannot connect](scenarios/level-1/008/README.md) | Evidence · Python only | 20 min |
| 009 | 1 | [DNS: IP works, hostname fails](scenarios/level-1/009/README.md) | Evidence · Python only | 20 min |
| 010 | 1 | [Networking: Local only](scenarios/level-1/010/README.md) | **Runnable** · docker | 20 min |
| 011 | 1 | [TLS: Certificate expired](scenarios/level-1/011/README.md) | Evidence · Python only | 20 min |
| 012 | 1 | [Nginx: Bad gateway](scenarios/level-1/012/README.md) | **Runnable** · docker | 20 min |
| 013 | 1 | [Git: Merge conflict](scenarios/level-1/013/README.md) | **Runnable** · git | 20 min |
| 014 | 1 | [Git: Private clone fails](scenarios/level-1/014/README.md) | Evidence · Python only | 20 min |
| 015 | 1 | [Jenkins: Tool missing](scenarios/level-1/015/README.md) | Evidence · Python only | 20 min |
| 016 | 1 | [Jenkins: Job queued](scenarios/level-1/016/README.md) | Evidence · Python only | 20 min |
| 017 | 1 | [Jenkins: Docker denied](scenarios/level-1/017/README.md) | Evidence · Python only | 20 min |
| 018 | 1 | [GitHub Actions: No trigger](scenarios/level-1/018/README.md) | Evidence · Python only | 20 min |
| 019 | 1 | [Docker: Immediate exit](scenarios/level-1/019/README.md) | **Runnable** · docker | 20 min |
| 020 | 1 | [Docker: Published port fails](scenarios/level-1/020/README.md) | **Runnable** · docker | 20 min |
| 021 | 1 | [Docker: Mounted files unreadable](scenarios/level-1/021/README.md) | **Runnable** · docker | 20 min |
| 022 | 1 | [Registry: Authentication error](scenarios/level-1/022/README.md) | Evidence · Python only | 20 min |
| 023 | 1 | [Kubernetes: CrashLoopBackOff](scenarios/level-1/023/README.md) | **Runnable** · kubernetes | 20 min |
| 024 | 1 | [Kubernetes: ImagePullBackOff](scenarios/level-1/024/README.md) | **Runnable** · kubernetes | 20 min |
| 025 | 1 | [Kubernetes: Pending pod](scenarios/level-1/025/README.md) | **Runnable** · kubernetes | 20 min |
| 026 | 1 | [Kubernetes: Missing configuration](scenarios/level-1/026/README.md) | **Runnable** · kubernetes | 20 min |
| 027 | 1 | [Kubernetes: Service selector mismatch](scenarios/level-1/027/README.md) | **Runnable** · kubernetes | 20 min |
| 028 | 1 | [AWS EC2: Security group blocks app](scenarios/level-1/028/README.md) | Evidence · Python only | 20 min |
| 029 | 1 | [AWS S3: Access denied](scenarios/level-1/029/README.md) | Evidence · Python only | 20 min |
| 030 | 1 | [AWS ALB: Unhealthy target](scenarios/level-1/030/README.md) | Evidence · Python only | 20 min |
| 031 | 1 | [Terraform: Init backend failure](scenarios/level-1/031/README.md) | Evidence · Python only | 20 min |
| 032 | 1 | [Ansible: Host unreachable](scenarios/level-1/032/README.md) | Evidence · Python only | 20 min |
| 033 | 1 | [Prometheus: Target down](scenarios/level-1/033/README.md) | **Runnable** · docker | 20 min |
| 034 | 1 | [Grafana: No data](scenarios/level-1/034/README.md) | Evidence · Python only | 20 min |
| 035 | 2 | [Linux: Deleted files retain space](scenarios/level-2/035/README.md) | Evidence · Python only | 35 min |
| 036 | 2 | [Linux: Inodes exhausted](scenarios/level-2/036/README.md) | Evidence · Python only | 35 min |
| 037 | 2 | [Linux: Slow with normal CPU](scenarios/level-2/037/README.md) | Evidence · Python only | 35 min |
| 038 | 2 | [Networking: Intermittent connection failure](scenarios/level-2/038/README.md) | Evidence · Python only | 35 min |
| 039 | 2 | [Nginx: Peak-time timeout](scenarios/level-2/039/README.md) | Evidence · Python only | 35 min |
| 040 | 2 | [Git: Faulty production commit](scenarios/level-2/040/README.md) | **Runnable** · git | 35 min |
| 041 | 2 | [Jenkins: Agent inconsistency](scenarios/level-2/041/README.md) | Evidence · Python only | 35 min |
| 042 | 2 | [Jenkins: Upgrade regression](scenarios/level-2/042/README.md) | Evidence · Python only | 35 min |
| 043 | 2 | [GitHub Actions: AWS federation denied](scenarios/level-2/043/README.md) | Evidence · Python only | 35 min |
| 044 | 2 | [GitLab CI: Runner mismatch](scenarios/level-2/044/README.md) | Evidence · Python only | 35 min |
| 045 | 2 | [Azure DevOps: Service connection denied](scenarios/level-2/045/README.md) | Evidence · Python only | 35 min |
| 046 | 2 | [CI/CD: Wrong artifact deployed](scenarios/level-2/046/README.md) | Evidence · Python only | 35 min |
| 047 | 2 | [CI/CD: Partial deployment](scenarios/level-2/047/README.md) | Evidence · Python only | 35 min |
| 048 | 2 | [Docker: Local works, server fails](scenarios/level-2/048/README.md) | Evidence · Python only | 35 min |
| 049 | 2 | [Docker: Database unreachable](scenarios/level-2/049/README.md) | **Runnable** · docker | 35 min |
| 050 | 2 | [Kubernetes: OOMKilled](scenarios/level-2/050/README.md) | **Runnable** · kubernetes | 35 min |
| 051 | 2 | [Kubernetes: Readiness failure](scenarios/level-2/051/README.md) | **Runnable** · kubernetes | 35 min |
| 052 | 2 | [Kubernetes: Liveness restarts](scenarios/level-2/052/README.md) | **Runnable** · kubernetes | 35 min |
| 053 | 2 | [Kubernetes: Ingress routing failure](scenarios/level-2/053/README.md) | Evidence · Python only | 35 min |
| 054 | 2 | [Kubernetes: Internal DNS failure](scenarios/level-2/054/README.md) | **Runnable** · kubernetes | 35 min |
| 055 | 2 | [Kubernetes: NetworkPolicy blocked traffic](scenarios/level-2/055/README.md) | Evidence · Python only | 35 min |
| 056 | 2 | [Kubernetes: PVC pending](scenarios/level-2/056/README.md) | **Runnable** · kubernetes | 35 min |
| 057 | 2 | [Kubernetes: Stalled rollout](scenarios/level-2/057/README.md) | **Runnable** · kubernetes | 35 min |
| 058 | 2 | [Kubernetes: Node NotReady](scenarios/level-2/058/README.md) | Evidence · Python only | 35 min |
| 059 | 2 | [Kubernetes: HPA not scaling](scenarios/level-2/059/README.md) | Evidence · Python only | 35 min |
| 060 | 2 | [Helm: Invalid upgrade values](scenarios/level-2/060/README.md) | Evidence · Python only | 35 min |
| 061 | 2 | [Argo CD: Sync failure](scenarios/level-2/061/README.md) | Evidence · Python only | 35 min |
| 062 | 2 | [Terraform: State locked](scenarios/level-2/062/README.md) | Evidence · Python only | 35 min |
| 063 | 2 | [Terraform: Infrastructure drift](scenarios/level-2/063/README.md) | Evidence · Python only | 35 min |
| 064 | 2 | [Ansible: Non-idempotent playbook](scenarios/level-2/064/README.md) | Evidence · Python only | 35 min |
| 065 | 2 | [AWS VPC: Private subnet egress fails](scenarios/level-2/065/README.md) | Evidence · Python only | 35 min |
| 066 | 2 | [AWS RDS: Connections exhausted](scenarios/level-2/066/README.md) | Evidence · Python only | 35 min |
| 067 | 2 | [AWS Secrets Manager: Rotation failure](scenarios/level-2/067/README.md) | Evidence · Python only | 35 min |
| 068 | 3 | [CI/CD: Concurrent deployments](scenarios/level-3/068/README.md) | Evidence · Python only | 50 min |
| 069 | 3 | [CI/CD: Schema rollback incompatible](scenarios/level-3/069/README.md) | Evidence · Python only | 50 min |
| 070 | 3 | [Deployment: Rolling update downtime](scenarios/level-3/070/README.md) | Evidence · Python only | 50 min |
| 071 | 3 | [Deployment: Canary errors](scenarios/level-3/071/README.md) | Evidence · Python only | 50 min |
| 072 | 3 | [Deployment: Blue-green session failure](scenarios/level-3/072/README.md) | Evidence · Python only | 50 min |
| 073 | 3 | [Security: Exposed AWS credentials](scenarios/level-3/073/README.md) | Evidence · Python only | 50 min |
| 074 | 3 | [DevSecOps: Critical vulnerability](scenarios/level-3/074/README.md) | Evidence · Python only | 50 min |
| 075 | 3 | [SonarQube: Hotfix gate fails](scenarios/level-3/075/README.md) | Evidence · Python only | 50 min |
| 076 | 3 | [Kubernetes: Autoscaler cannot expand](scenarios/level-3/076/README.md) | Evidence · Python only | 50 min |
| 077 | 3 | [Kubernetes: Drain blocked](scenarios/level-3/077/README.md) | Evidence · Python only | 50 min |
| 078 | 3 | [Kubernetes: Volume attach conflict](scenarios/level-3/078/README.md) | Evidence · Python only | 50 min |
| 079 | 3 | [Kubernetes: Removed API after upgrade](scenarios/level-3/079/README.md) | Evidence · Python only | 50 min |
| 080 | 3 | [Kubernetes: Quota blocks recovery](scenarios/level-3/080/README.md) | **Runnable** · kubernetes | 50 min |
| 081 | 3 | [Kubernetes: Healthy pods, intermittent failure](scenarios/level-3/081/README.md) | **Runnable** · kubernetes | 50 min |
| 082 | 3 | [Argo CD: Emergency fix reverted](scenarios/level-3/082/README.md) | Evidence · Python only | 50 min |
| 083 | 3 | [Terraform: Database replacement proposed](scenarios/level-3/083/README.md) | Evidence · Python only | 50 min |
| 084 | 3 | [Terraform: Partial apply inconsistent](scenarios/level-3/084/README.md) | Evidence · Python only | 50 min |
| 085 | 3 | [Terraform: Provider upgrade changes plan](scenarios/level-3/085/README.md) | Evidence · Python only | 50 min |
| 086 | 3 | [AWS EKS: Workload identity denied](scenarios/level-3/086/README.md) | Evidence · Python only | 50 min |
| 087 | 3 | [AWS Auto Scaling: More nodes, still slow](scenarios/level-3/087/README.md) | Evidence · Python only | 50 min |
| 088 | 3 | [AWS: Availability Zone failure](scenarios/level-3/088/README.md) | Evidence · Python only | 50 min |
| 089 | 3 | [AWS RDS: Failover reconnection fails](scenarios/level-3/089/README.md) | Evidence · Python only | 50 min |
| 090 | 3 | [AWS Route 53: Cutover inconsistent](scenarios/level-3/090/README.md) | Evidence · Python only | 50 min |
| 091 | 3 | [AWS Lambda: Private database timeout](scenarios/level-3/091/README.md) | Evidence · Python only | 50 min |
| 092 | 3 | [Azure AKS: Upgrade stalled](scenarios/level-3/092/README.md) | Evidence · Python only | 50 min |
| 093 | 3 | [Azure ACR: Image pulls denied](scenarios/level-3/093/README.md) | Evidence · Python only | 50 min |
| 094 | 3 | [Azure Key Vault: Secret access lost](scenarios/level-3/094/README.md) | Evidence · Python only | 50 min |
| 095 | 3 | [GCP GKE: Cloud access denied](scenarios/level-3/095/README.md) | Evidence · Python only | 50 min |
| 096 | 3 | [GCP Cloud Build: Publish denied](scenarios/level-3/096/README.md) | Evidence · Python only | 50 min |
| 097 | 3 | [Monitoring: Alert never delivered](scenarios/level-3/097/README.md) | Evidence · Python only | 50 min |
| 098 | 3 | [ELK / Loki: Logs disappear](scenarios/level-3/098/README.md) | Evidence · Python only | 50 min |
| 099 | 3 | [Incident response: Shared dependency failure](scenarios/level-3/099/README.md) | Evidence · Python only | 50 min |
| 100 | 3 | [Disaster recovery: Restore misses target](scenarios/level-3/100/README.md) | Evidence · Python only | 50 min |
