# Progressive hints · 059

<details><summary>Hint 1 · Narrow the investigation</summary>

Compare the observed failure against the component's declared configuration and recent changes. Separate the user-visible symptom from the failing dependency.

</details>

<details><summary>Hint 2 · Useful checks</summary>

Inspect HPA conditions, metrics API, container requests, and current CPU metrics.

These are investigation prompts. Substitute actual lab resource names; uppercase names are placeholders.

</details>

<details><summary>Hint 3 · Likely cause</summary>

Utilization-based HPA cannot calculate its target without resource requests.

</details>
