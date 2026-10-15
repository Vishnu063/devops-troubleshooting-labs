# Compound incidents

Three additional runnable challenges. The final 100 IDs and levels remain unchanged. Each has **two independent faults**. Fixing only one must fail recovery checks.

| ID | Brief | Runtime | Target |
| --- | --- | --- | --- |
| M01 | [Checkout unavailable](runnable/M01/README.md) | Docker + kind + kubectl | 60 min |
| M02 | [Unstable order worker](runnable/M02/README.md) | Docker + kind + kubectl | 60 min |
| M03 | [Intermittent release outage](runnable/M03/README.md) | Docker + kind + kubectl | 60 min |

```bash
python3 lab.py session start --hidden --compound
python3 lab.py session up
python3 lab.py session check
```

For spoilers, open the separate solution in the selected native lab folder.
