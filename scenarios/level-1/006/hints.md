# Progressive hints · 006

<details><summary>Hint 1 · Narrow the investigation</summary>

Compare the observed failure against the component's declared configuration and recent changes. Separate the user-visible symptom from the failing dependency.

</details>

<details><summary>Hint 2 · Useful checks</summary>

ss -ltnp; systemctl status orders; ps -fp PID

These are investigation prompts. Substitute actual lab resource names; uppercase names are placeholders.

</details>

<details><summary>Hint 3 · Likely cause</summary>

The previous worker was not stopped before starting its replacement.

</details>
