# Repair reference 021

Compare the broken and fixed Compose files before using this reference.

```bash
cp runnable/021/fixed.json .lab-state/021/compose.json
python3 lab.py up 021
python3 lab.py check 021
python3 lab.py down 021
```
