# Repair reference 052

Compare `broken.json` with `fixed.json` and explain why each changed field matters.

```bash
kubectl --context kind-devops-labs apply -f runnable/052/fixed.json
kubectl --context kind-devops-labs -n devops-lab-052 rollout status deployment/web --timeout=120s
python3 lab.py check 052
python3 lab.py down 052
```

For 052, the native lab models startup timing specifically; the supplied evidence drill covers the same probe design problem. Registry access and image downloads must work before interpreting image-related failures.
