# Workflow — Lubich (2008) splitting-methods replication

**Paper:** C. Lubich, *On splitting methods for Schrödinger–Poisson and cubic nonlinear Schrödinger equations*, Math. Comp. 77(264), 2141–2153 (2008). DOI: 10.1090/S0025-5718-08-02101-7.
**Run date:** 2026-07-05
**Verdict:** REPLICATED

## Stage 0 — Paper acquisition

- Fetched author preprint `speq.pdf` (169616 B, md5 `608e48c81bd247f3d8beef9b420d68cb`) from `https://na.uni-tuebingen.de/pub/lubich/papers/speq.pdf`.
- The AMS journal URL was Cloudflare-gated; the preprint mirror on the author's Tübingen page is the same PDF and is openAccess per S2 flag.
- Text extraction via `pdftotext -layout` (poppler shipped with macOS Homebrew).

## Stage 1 — Reading & claims extraction

- Manually read the 13-page paper (no figures, no tables, no numerical experiments; pure theory).
- Extracted the six testable claims C1–C6 (see REPORT.md §2 and the claims table in REPORT.tex):
  - C1: Schrödinger–Poisson L² error = O(τ²) (Thm 2.1)
  - C2: Schrödinger–Poisson H¹ error ≤ O(τ) upper bound (Thm 2.1)
  - C3: cubic NLS L² error = O(τ²) (Thm 7.1)
  - C4: cubic NLS H² error ≤ O(τ) upper bound (Thm 7.1)
  - C5: Exact L² norm conservation (composition of two unitary flows)
  - C6: Explicit + time-reversible structure (verified via free-Schrödinger plane-wave test)

## Stage 2 — Design of the replication

- Paper is on R³. Paper explicitly says *"Our arguments would apply similarly to problems with periodic boundary conditions and in lower space dimension."* → chose 1D periodic [0, 2π) with Fourier-spectral discretisation for tractability and exactness of the free-Schrödinger step.
- Chose four problems: cubic NLS × 2 signs, Schrödinger–Poisson × 2 signs.
- Chose τ set {1/50, 1/100, 1/200, 1/400, 1/800} so each halving gives one order-doubling in the rate estimate; all commensurate with τ_ref = 1/32000 so no interpolation is needed at the reference.
- Chose the reference solution as Strang-at-τ_ref (standard practice for smooth-data PDE convergence studies).

## Stage 3 — Implementation (`work/lubich_splitting.py`)

- Python 3.14.6 + NumPy stdlib install.
- Free-Schrödinger half step in Fourier space: `ψ̂ ← exp(-iτ/2·k²) ψ̂`.
- Potential step pointwise: `ψ ← exp(-iτ·V[ψ]) ψ`, with
  - cubic NLS: `V[ψ] = ±|ψ|²`
  - Schrödinger–Poisson: `V̂[k] = ±ρ̂[k]/k²` (k≠0), `V̂[0]=0`, IFFT, take real part.
- Norms:
  - `‖·‖_L² = √(Σⱼ |uⱼ|² · dx)`
  - `‖·‖_{Hᵐ}² = Σ_{j=0..m} ‖∂ˣʲ u‖_{L²}²`, derivatives spectral.

## Stage 4 — Convergence runs

- Single-core local run on assistant's mac, 13.7 s wall.
- Output: `work/convergence_results.json` (numerical rates) + tabular print.
- Nothing heavy enough to need uicgpu.

## Stage 5 — Sanity checks

- Free-Schrödinger plane-wave: `ψ₀ = exp(3ix)`, exact solution `ψ(x,1) = exp(3ix - 9i)`. Ran full Strang loop with V=0 at τ=0.01, T=1, N=64. Error `4.4·10⁻¹⁴` (machine precision) → confirms free-step implementation is exact and Strang wrapping is correct.
- Mass drift on all 4 physics problems: ≤ 1.2·10⁻¹³ across all τ (grows ~sqrt(N_steps) from round-off, as expected for a unitary scheme).

## Stage 6 — Plotting

- `work/make_plot.py` produced `evidence/convergence_plot.png` — log-log of ‖e‖_L² and ‖e‖_Hᵐ vs τ for all 4 problems with slope-2 reference line. All series parallel to slope 2 over 4½ decades.

## Stage 7 — LLM judge

- `work/llm_judge.py`.
- Endpoint: Argo proxy `http://127.0.0.1:44497/v1/chat/completions` (FREE).
- Intended model: `argo:claude-opus-4.8`, then `argo:claude-opus-4.7` — both returned 502 at run time (upstream Argo flake).
- Fell back to `argo:claude-sonnet-4.6`.
- Judge got: paper's exact claims + our full JSON of observed orders and mass drifts.
- Judge output: `report/evidence/llm_judge_output.md`.
- Judge verdict: REPLICATED, matching human-authored verdict.

## Stage 8 — Reporting

- Wrote `report/REPORT.md` (this repo's canonical human-facing report).
- Backfill (this stage): produced REPORT.tex, open_questions.json, workflow.md (this file), artifacts_summary.md, failure_analysis.md.

## Reproduce commands

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Lubich-splitting-Schrodinger-Poisson-cubic-NLS-2008/work
python3 lubich_splitting.py       # 13.7 s wall
python3 make_plot.py
python3 llm_judge.py
```
