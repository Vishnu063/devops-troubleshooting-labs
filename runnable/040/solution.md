# Repair reference 040

```bash
git -C .lab-state/040/repo revert --no-edit HEAD
python3 lab.py check 040
python3 lab.py down 040
```
