# Your first troubleshooting lab

Start with Git. It runs locally, needs no cloud account, and teaches the full workflow: observe a failure, investigate, repair, and verify.

## 1. Check your setup

From the repository root:

```bash
python3 lab.py doctor --runtime git
python3 lab.py track git
```

The checker looks for Python and executable files. It does not install tools or prove that Docker or Kubernetes is usable. Windows users should run runnable labs in WSL2; evidence drills can be read on any platform with Python 3.10+.

## 2. Open the brief and create the fault

```bash
python3 lab.py show 013
python3 lab.py up 013
python3 lab.py check 013
```

Fresh `up` first confirms a matching live fault and prints **READY: expected fault confirmed**. **The first recovery check is supposed to fail.** A failing check alone is not proof that the intended fault exists. If setup reports **NOT READY** or **Lab error**, investigate setup before treating it as the exercise. The lab prints an isolated repository path; this is where you work. Your own repository and global Git settings are not the repair target.

For an existing workspace, run `python3 lab.py verify-fault 013 --wait 120` to confirm the fault, or `python3 lab.py reset 013` to discard changes and recreate it. Existing Git/Docker workspaces are preserved when `up` is repeated, so applying a repair does not trigger a new broken-state check.

## 3. Investigate before changing anything

In the printed lab repository, use `git status`, `git diff`, and `git log --oneline --all --graph`. Explain which changes must survive the repair. Make the repair inside that lab repository, then return to the troubleshooting-labs root.

Need help? Reveal one hint at a time:

```bash
python3 lab.py hint 013 --step 1
python3 lab.py hint 013 --step 2
```

## 4. Verify and clean up

```bash
python3 lab.py check 013
python3 lab.py record 013 --score 7 --minutes 20 --hints 2
python3 lab.py down 013
```

Replace the example score, minutes, and hint count with your own. Recording a score is self-assessment, not a certification. `down` removes this lab's workspace; save any notes elsewhere first. If the check still fails, inspect the lab instructions and your changes before resetting. `reset` discards the repair and recreates the fault.

## Choose the next path

| Path | Command | What to expect |
| --- | --- | --- |
| Git | `python3 lab.py track git` | Merge recovery and safe shared-history recovery |
| Docker | `python3 lab.py track docker` | Startup, exposed ports, proxying, monitoring, dependencies |
| Kubernetes | `python3 lab.py track kubernetes` | Workload startup, scheduling, configuration, traffic |
| Advanced | `python3 lab.py track advanced` | Recovery decisions, intermittent failures, compound incidents |

Paths recommend an order; they do not gate access or award completion. For Docker and Kubernetes, read [runtime setup and isolation](LABS.md) before starting. Check daemon access and Compose separately: an installed executable alone is insufficient.

## No containers available?

```bash
python3 lab.py show 001
python3 lab.py evidence 001
```

Write your hypotheses and verification plan, then compare against the separate solution. All 100 scenarios support this evidence mode; 24 also have executable local faults.

## Something went wrong?

- **Python not found:** install Python 3.10+; some systems use `python` instead of `python3`.
- **No matching cases:** use `python3 lab.py list` to inspect supported IDs and filters.
- **Docker permission or connection error:** confirm `docker info` works in your current terminal. Do not change host permissions blindly.
- **Wrong Kubernetes context:** stop and follow [LABS.md](LABS.md); use the dedicated local kind cluster.
- **Failed recovery check:** read the observations, inspect live state, and verify your hypothesis. Do not copy a fixed manifest merely to obtain a pass.

Report reproducible problems using the repository's bug template. Include your OS, tool versions, case ID, command, and redacted output.

