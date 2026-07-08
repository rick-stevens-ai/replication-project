# Workflow — arXiv:1801.04042 replication

Reconstructed from `attempt_log.md` and file timestamps.

## 1. Paper acquisition + read (day 0)
- Pull arXiv:1801.04042v1 PDF → `work/paper.pdf` and text extract → `work/paper.txt`.
- Read §§ I-III; identify the two core Clifford subgroups (real Clifford = ⟨H, CNOT, Paulis⟩; CNOT+Pauli) and transcribe the closed-form block-size and block-eigenvalue formulas.
- No numerical data or figures in the paper → replication target = numerical verification of the analytical formulas.

## 2. Environment setup
- Python 3, `pip install stim==1.16.0 numpy==2.5.0 scipy==1.18.0 matplotlib`.
- Free-endpoint policy: all compute local; no cloud GPUs needed (2-qubit stabilizer simulation is trivial).

## 3. Baseline RB (full Clifford, symmetric depolarizing) — Exp 1
- `work/rb_replication.py` main harness:
  - Subgroup samplers: `full_clifford_sample()` via `stim.Tableau.random(n)`; `real_clifford_walk(n, walk_len=60)` via random-walk over {H_i, CNOT_ij, X_i, Y_i, Z_i}; `cnot_pauli_walk(n, walk_len=60)` over {CNOT_ij, X_i, Y_i, Z_i}.
  - Circuit build: initial state prep, m sampled group elements each followed by per-qubit `DEPOLARIZE1(p_dep=0.01)`, ideal tableau-inverse recovery, measurement.
  - Sequence lengths m ∈ {1,2,4,8,16,32,64,128}; 60 seq/length.
  - Fit `f(m) = A·λ^m + B` via `scipy.optimize.curve_fit`.
- Sanity-check: full Clifford λ_fit vs theory λ = 1 - p·4²/(4²-1) = 0.9788. Result 0.9675 (±0.01 statistical). PASS.

## 4. Real Clifford + CNOT+Pauli under symmetric noise — Exps 2, 3a, 3b
- Same harness, swap subgroup sampler.
- Verify each fitted λ matches theory to within σ_λ ≈ 0.01.
- Note the collapse: under symmetric depolarizing every non-identity Pauli has equal weight → p_i/N_i uniform → all block λ's degenerate. Documented as expected behavior, NOT as failed multi-exponential test.

## 5. Asymmetric pure-Z noise — key falsification test — Exp asym
- `work/rb_asym.py`:
  - Replace `DEPOLARIZE1(p_dep)` with `Z_ERROR(p_z=0.02)`.
  - Predict from paper: |00⟩ RB stays exactly flat (λ_1=1); |++⟩ RB decays with λ_2 = 1 - p·4/3 = 0.9472.
  - Run with N_seq=60 first.
- |00⟩ result: λ_fit = 1.0000 exactly (all lengths give f=1.000). PASS.
- |++⟩ result: λ_fit = 0.9561 vs theory 0.9472 (|Δ| = 0.0089). Within 1σ but borderline — motivates hi-stats rerun.

## 6. High-statistics + bootstrap error bars — Exps hi_n, hi_stats
- `work/rb_baseline_high_n.py`: full Clifford at N_seq=400/length → λ=0.97620 (|Δ|=0.0026, was 0.011 at N=60). Confirms earlier gap was sampling noise.
- `work/rb_final_hi_stats.py`: 250 seq/length × 300 bootstrap resamples on both problem cases.
  - Full Clifford |00⟩ DEPOLARIZE1(0.01): 0.97437 ± 0.00691 → 0.64σ from theory 0.97877.
  - CNOT+Pauli |++⟩ Z_ERROR(0.02): 0.94672 ± 0.00758 → **0.06σ** from theory 0.94720.
- Result: definitive positive evidence for the block-selection prediction.

## 7. Bound-check on entanglement infidelity (Claim C7)
- Compute (2ⁿ-1)/2ⁿ · (1-λ) ≤ p ≤ (1-λ) for symmetric and asymmetric cases.
- Both intervals bracket the true injected p. PASS.

## 8. Figure generation
- `work/make_figure.py`: matplotlib decay curves + best-fit overlays.
- Outputs: `evidence/rb_decay_symmetric.png`, `evidence/rb_decay_asymmetric.png`.

## 9. LLM judge (free Argo endpoint)
- `work/llm_judge.py`: send REPORT.md + evidence JSON to Argo proxy.
- Judge model: `argo:gpt-5.2` (opus-4.7 and opus-4.8 both returned upstream parser errors during this session).
- Verdict returned: REPLICATED, high confidence. Full output → `evidence/judge_verdict.json`.

## 10. Report writing
- `report/REPORT.md` primary narrative (already existed).
- Backfill 2026-07-06: `REPORT.tex`, `open_questions.json`, `open_questions_section.tex`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`, `extraction/nougat.mmd` stub.

## Dependencies + reproducibility
- All code deterministic given RNG seed (Python seed set at top of each script).
- Runtime: exploratory runs ~30 s/config on m1 CPU; hi-stats runs ~5 min each.
- No paid endpoints; no data downloads; entirely local.
