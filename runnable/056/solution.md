# Repair reference 056

Compare `broken.json` with `fixed.json` and explain why each changed field matters.

PVC storageClassName is immutable after creation. Delete only this lab Deployment and unbound lab PVC before applying the replacement. This lab PVC contains no production data.

```bash
kubectl --context kind-devops-labs -n devops-lab-056 delete deployment web
kubectl --context kind-devops-labs -n devops-lab-056 delete pvc web-data
```

```bash
kubectl --context kind-devops-labs apply -f runnable/056/fixed.json
kubectl --context kind-devops-labs -n devops-lab-056 rollout status deployment/web --timeout=120s
python3 lab.py check 056
python3 lab.py down 056
```

For 052, the native lab models startup timing specifically; the supplied evidence drill covers the same probe design problem. Registry access and image downloads must work before interpreting image-related failures.
