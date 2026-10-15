# Agent handoff and repository guardrails

This repository is a portfolio of distinct HgCdTe research programs, not a single flagship publication. Start at `README.md`, `research/portfolio_state.md`, and `research/contribution_registry.md`. Do not conflate R01–R07 or treat a program-specific stop as a repository-wide policy.

## R07: microscopic zero-temperature band inversion

**MANDATORY FIRST READ before doing R07 work**: `research/programs/microscopic_bandgap/SUCCESSOR_HANDOFF.md`, then `research/programs/microscopic_bandgap/state.md` (current state is near its top), then the latest linked `decision.md`, `handoff_ledger.md`, `verification` records, and any research source/owner protocol applicable to the proposed work. The handoff is navigation, not a replacement for verified numerical evidence.

The ultimate R07 objective is a predictive, nonempirical, analytically interpretable microscopic theory of the **signed Hg1-xCdxTe Gamma6/Gamma8 inversion and zero-temperature critical composition x_c**, derived from chemical substitution, electronic structure, disorder and local environments with justified physical/numerical uncertainty. A new simulation, a Gaussian spectral centroid, an inverse-resolvent ordering or a projected operator trace is not automatically a signed physical bandgap, an inversion mass, or a physical x_c.

Priority order: **new falsifiable physics -> analytical derivation/identifiability -> indispensable targeted computation -> independent validation and prior-art comparison**. Distinguish chemical average from disorder fluctuation self-energy without double counting; justify the physical/topological inversion criterion before using m(x_c)=0. Do not claim generic disorder-dependent bandgap, SQS, ACE, or Kane/SCBA results as new inventions.

**Research integrity**: Never silently relax a prospectively frozen gate, retry a failed native unit, promote refused output, infer missing material error from conditional arithmetic intervals, discard negative results, or fit the target x_c from empirical alloy-gap coefficients. Document calculated/proved-under-assumptions/conjectured/refused distinctly. Read primary prior art and compare claim by claim before using “novel”.

**Execution safety**: Work only on the existing R07 research branch unless the user authorizes otherwise. Protect main, the stock QE and dirty DFT trees, original 16-atom 352-band HSE target, private raw evidence, other tmux sessions (notably Calcura), original failed runs, and account credentials. For a new native MPI job require a fresh, predeclared science/owner/resource protocol with verified source/PP/ELF and socket length; prior native jobs typically used 12 GiB cgroup memory, zero cgroup swap, 12 tasks, measured wall deadline and host RAM/disk floors. Inspect the actual latest protocols: past resource success is not blanket admission. Do not start compute merely because it is possible. No modifications to old frozen experiments to make them pass.

**Continuity**: A successor must inspect `git status --short --branch` and `git log` before acting, preserve any in-progress/untracked research directory, check the existing `research` tmux Codex session, and determine whether model access is exhausted. Do not interrupt an active scientifically authorized computation. Commit and push only verified, scoped R07 milestones to the existing research branch and use already configured authorized credentials. Large native data may be retained off-repo with hashes. Do not state that raw off-repo packets are available on GitHub merely because their manifests are.

Always write a successor-readable decision note showing what physical inference becomes possible, what remains unidentifiable, and what observation or calculation would falsify the proposed next step.
