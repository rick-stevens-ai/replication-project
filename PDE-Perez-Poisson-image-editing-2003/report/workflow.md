# Workflow — Pérez, Gangnet, Blake (2003) "Poisson Image Editing" replication

Chronological, actually-executed steps. Machine-verifiable via `work/run.log`,
`report/evidence/results.json`, and `report/evidence/c1_boundary_gradient_match.json`.

## 0. Setup
- Free-endpoint policy: all LLM-judge calls to Argo (`localhost:44497`, key `stevens`).
- Local CPU only; total wall-clock a few seconds end-to-end.
- Fixed RNG seed `np.random.default_rng(0)` for bit-for-bit reproducibility.

## 1. Paper acquisition + equations
- Paper PDF at `work/poisson_paper.pdf` (SHA-256 prefix `2f62b451`).
- LLM extraction tools failed on the two-column SIGGRAPH layout →
  fell back to `pdftotext` for equation extraction.
- Captured target equations: (6)–(7) discretization, (11) seamless
  guidance, (13) mixed-gradient guidance.

## 2. Implementation
- `work/poisson_editing.py`: builds sparse SPD system per eq. (7) from
  scratch, solves with `scipy.sparse.linalg.spsolve`.
  - `solve_poisson_region(dest, src, mask, mode)` — single channel;
    modes: `"seamless"`, `"mixed"`, `"membrane"`.
  - `solve_poisson_rgb(...)` — per-channel wrapper.
- Direct sparse LU differs in **solver** from the paper's GS+SOR /
  V-cycle multigrid but is the identical **discretization**; both converge
  to the same numerical solution up to floating-point roundoff.

## 3. Test-scene generation
Fully synthetic, deterministic under seed 0:
1. **Disk-in-gradient** (`200 × 280`, `|Ω| = 5,013 px`).
   Destination = smooth RGB ramp + mild noise. Source = tan background
   with bright orange textured disk (`R~230, G~120, B~60` inside).
2. **Text-on-stripes** (`180 × 260`, `|Ω| = 30,800 px`).
   Destination = high-contrast sinusoidal-sign stripes.
   Source = plain background with several dark horizontal bars.

## 4. Experiments (three modes per scene)
Driver: `work/run_experiments.py`.
1. Naive paste (baseline).
2. Seamless clone (v = ∇g, eq. 11).
3. Mixed clone (eq. 13).
4. Membrane (v = 0) on the disk scene — solver correctness sanity check.

## 5. Claim-specific verifiers
- **C1** — `work/verify_c1_correct.py`. For every boundary edge
  `(p ∈ Ω, q ∉ Ω)`, compute:
  - `edited_jump = edited[p] − dest[q]`
  - `source_jump = src[p] − src[q]`
  - `naive_jump  = src[p] − dest[q]`
  Compare `|edited − src_grad|` vs. `|naive − src_grad|` per channel.
  Emit `evidence/c1_boundary_gradient_match.json`.
- **C2** — `run_experiments.py` experiment 2. Membrane solve; compute
  `Δf` at strict interior of Ω; report max/mean per channel.
- **C3** — `run_experiments.py` experiment 3. Total `Σ|∇f|` inside Ω
  for {dest_original, src_original, seamless_edit, mixed_edit}.

## 6. Figures
`work/make_comparison_figure.py` emits per-scene 5-panel
`dest | src | naive | seamless | mixed` PNGs plus the raw scene and
result images (`01_dest.png` … `08_mixed_text_on_stripes.png`) into
`report/evidence/`.

## 7. LLM-judge scoring (independent referees)
- `work/llm_judge.py`: send exact numeric evidence + rubric to three Argo
  models. No regex; parse JSON response only.
- Referees: `argo:gpt-4.1`, `argo:gemini-2.5-pro`, `argo:claude-sonnet-4.6`.
- Full prompt in `evidence/llm_judge_prompt.txt`; per-model verdict JSONs
  in `evidence/llm_judge_response_argo_*.json`.
- All three returned `"overall_verdict": "REPLICATED"`.

## 8. Report + verdict
- Numeric tables assembled into `report/REPORT.md`.
- Verdict: **REPLICATED** across C1, C2, C3; C4 out of scope for a
  minimal reproduction.

## Exact reproduction commands (from `work/`)
```
python3 run_experiments.py            # main experiments + C2 + C3
python3 verify_c1_correct.py          # C1 boundary-gradient test
python3 make_comparison_figure.py     # 5-panel comparison figures
python3 llm_judge.py                  # LLM referee scoring
```
