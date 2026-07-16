# First-principles decision memos

Every expensive calculation branch must have a decision memo before production execution.

A memo must state:

- the unresolved physical quantity;
- competing hypotheses;
- minimum required accuracy;
- expected information gained;
- approximate and measured computational cost;
- the smallest convergence ladder;
- the result that stops deeper computation;
- the gate to the next material or method.

Machine-readable companions preserve authorization state and hard-stop conditions for tests and later automation. A planning estimate never authorizes production computation by itself.

Current memo:

- `cdte_fixed_volume_thermal_moment_pilot.md`
- `cdte_fixed_volume_thermal_moment_pilot.json`
