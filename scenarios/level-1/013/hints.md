# Progressive hints · 013

<details><summary>Hint 1 · Narrow the investigation</summary>

Compare the observed failure against the component's declared configuration and recent changes. Separate the user-visible symptom from the failing dependency.

</details>

<details><summary>Hint 2 · Useful checks</summary>

git status; git diff --cc; git show :2:app.conf; git show :3:app.conf

These are investigation prompts. Substitute actual lab resource names; uppercase names are placeholders.

</details>

<details><summary>Hint 3 · Likely cause</summary>

Competing edits require a deliberate combined change.

</details>
