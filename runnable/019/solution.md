# Repair reference 019

Compare the broken and fixed Compose files before using this reference.

```bash
cp runnable/019/fixed.json .lab-state/019/compose.json
python3 lab.py up 019
python3 lab.py check 019
python3 lab.py down 019
```
