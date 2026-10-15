# Repair reference 027

Compare `broken.json` with `fixed.json` and explain why each changed field matters.

```bash
kubectl --context kind-devops-labs apply -f runnable/027/fixed.json
kubectl --context kind-devops-labs -n devops-lab-027 rollout status deployment/web --timeout=120s
python3 lab.py check 027
python3 lab.py down 027
```

For 052, the native lab models startup timing specifically; the supplied evidence drill covers the same probe design problem. Registry access and image downloads must work before interpreting image-related failures.
