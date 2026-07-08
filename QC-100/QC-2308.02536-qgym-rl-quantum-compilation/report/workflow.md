# Workflow — QC-2308.02536 (qgym) Replication

## 1. Paper acquisition + extraction
- Downloaded arXiv 2308.02536v1 PDF.
- Ran nougat on the PDF to produce `extraction/nougat.mmd` (Markdown-math dump of paper body). Cross-checked against the arXiv HTML rendering for section III.B (the PoC) and Figs 3 + 4.
- Identified the paper as a **software-framework paper** with a single quantitative PoC (Scheduling env, vanilla PPO, 10^5 steps, Figs 3-4). Extracted the four testable claims (H1 mechanism, H2 training dynamics, H3 outcome, C4 software works).

## 2. Environment setup (free / local CPU only)
- Created a local venv on macOS with Python 3.11.15.
- Pip-installed the authors' own `qgym 0.3.1` (from PyPI, the repo QuTech-Delft/qgym), plus `qiskit 2.4.2`, `stable-baselines3 2.4.1`, `torch 2.2.2` (CPU wheel), `gymnasium 1.3.0`, `numpy 1.26.4`.
- Verified: `import qgym; qgym.envs.Scheduling(...)` constructs cleanly; `reset(options={...})` accepts a fixed circuit; `step` runs; SB3 `PPO("MultiInputPolicy", env)` compiles a policy without error. This settles C4.

## 3. H1 — deterministic mechanism (Fig. 3B vs 3C)
- Built the Fig. 3A circuit as `qgym.Gate` objects: `x(0,0)`, `cnot(0,1)`, `measure(0,0)`, `measure(1,1)`, with gate durations `{x:1, cnot:2, measure:10}` cycles.
- Built two `CommutationRulebook`s:
  - `default_rules=False` (no commutation) — mirrors Fig. 3B's ALAP-without-commutation baseline.
  - `default_rules=True` + explicit X<->CNOT-on-control rule — mirrors Fig. 3C's commutation-aware schedule.
- For each rulebook: called `rulebook.make_blocking_matrix(circuit)`, then ran an ALAP list-scheduler (back-to-front, honoring qubit occupancy + non-commuting predecessors) to compute schedule length.
- Saved blocking matrices + lengths to `report/evidence/commutation_mechanism.json`.
- Result: 23 vs 13 cycles → matches the paper's directional claim (commutation ⇒ strictly shorter). H1 REPRODUCED.

## 4. H2/H3 — vanilla PPO PoC training
- Built `qgym.envs.Scheduling` with `MachineProperties`: 3 qubits, gate set `{prep:1, x:2, y:2, z:1, h:2, cnot:4, measure:10}`, `max_gates=5`, `BasicCircuitGenerator` for random ≤5-gate circuits.
- Rewarder: default `BasicRewarder` — its defaults `illegal=-5, cycle=-1, gate=0` **exactly match the paper**.
- Trained `PPO("MultiInputPolicy", env)` for 10^5 steps, seed 20260703, `n_steps=2048, batch_size=64, n_epochs=10, lr=3e-4, gamma=0.99, ent_coef=0.01` (SB3 defaults + small entropy). Callback recorded per-episode length + reward; bucketed into 10 deciles for a Fig-4-style plot.
- Evaluated the trained agent on 50 held-out circuits (seeds 20261703..20261752) inside the same qgym env against a greedy-legal-first ALAP baseline policy — **same seeds ⇒ same 50 circuits for both policies**.
- Saved training-curve deciles + eval metrics to `report/evidence/scheduling_results.json`.
- Rendered `report/evidence/training_curves.png` mirroring paper Fig. 4A/B.
- Result: length 21.5 → 6.8 (−68%), reward −38.3 → −2.9 (+92%), PPO mean = ALAP mean = 2.66 cycles at 100% completion. H2 + H3 REPRODUCED.

## 5. Companion Routing run (transparency, not evidence)
- Also trained PPO on `qgym.envs.Routing` with a 5-qubit path coupling map vs Qiskit `SabreSwap`/`BasicSwap`. PPO did not converge to completing episodes at the training budget, so its swap counts are non-completion artifacts. Kept in `report/evidence/routing_results.json` for transparency; explicitly excluded from the verdict.

## 6. Earlier failed run (kept for provenance)
- A first pass with `n_steps=256, n_epochs=4` (SB3 legacy PoC settings) collapsed into a degenerate cycle-advancing policy (episode length exploded 39 → 1885). The paper does not report `n_steps`, so both readings of "vanilla" are defensible; SB3's own defaults were used for the primary run. Judge panel (`judge_panel.json`, `judge3.txt`) was run against this failing config — kept for provenance.

## 7. Judgment + report
- Aggregated numeric evidence and cross-checked against paper Figs 3, 4 and the headline claim in Sec. III.B/IV.
- Wrote `report/REPORT.md`, then produced the 7-artifact bundle (`REPORT.tex`, `open_questions.json`, `open_questions_section.tex`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`, `extraction/nougat.mmd`).
- Verdict: **REPLICATED** — headline exercised on real qgym simulation.
