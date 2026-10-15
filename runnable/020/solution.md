# Repair reference 020

Compare the broken and fixed Compose files before using this reference.

```bash
cp runnable/020/fixed.json .lab-state/020/compose.json
python3 lab.py up 020
python3 lab.py check 020
python3 lab.py down 020
```
