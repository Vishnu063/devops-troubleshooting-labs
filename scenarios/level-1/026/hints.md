# Progressive hints · 026

<details><summary>Hint 1 · Narrow the investigation</summary>

Compare the observed failure against the component's declared configuration and recent changes. Separate the user-visible symptom from the failing dependency.

</details>

<details><summary>Hint 2 · Useful checks</summary>

kubectl describe pod POD; kubectl get secrets; inspect secretKeyRef names and keys

These are investigation prompts. Substitute actual lab resource names; uppercase names are placeholders.

</details>

<details><summary>Hint 3 · Likely cause</summary>

The Deployment references a Secret that was never provisioned.

</details>
