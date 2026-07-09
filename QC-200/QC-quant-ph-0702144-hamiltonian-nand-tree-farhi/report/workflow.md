# Workflow — QC-200 replication of Farhi, Goldstone, Gutmann (2007) NAND-tree

**Paper:** arXiv:quant-ph/0702144 — "A Quantum Algorithm for the Hamiltonian NAND Tree"
**Author(s) verified from PDF:** E. Farhi (MIT CTP), J. Goldstone (MIT CTP), S. Gutmann (Northeastern Univ. Math).
**Report number:** MIT-CTP/3813. **Version:** v2 (22 Feb 2007). **Length:** 16 pages.
**Host:** cherryrd (macOS). **Wave date:** 2026-07-05.

## Step-by-step

1. **Fetch paper.** `curl -sL -o paper.pdf https://arxiv.org/pdf/quant-ph/0702144` → 220997 bytes, PDF 1.4, 16 pages.
2. **Extract text.** `pdftotext paper.pdf work/paper.txt` → 1620 lines.
3. **Skim & pin the reproducible core.** Continuous-time quantum walk on `runway ⊕ balanced binary tree ⊕ leaf-outer nodes`, initial packet `e^{i r π/2}/√L` for `-L+1 ≤ r ≤ 0`, evolve for `T = L/2`, measure right-runway projector. Expected: `P(right) → 1` iff NAND tree evaluates to 1, `P(right) → 0` iff NAND=0 (via the transmission-coefficient argument, `T(0)∈{0,1}`).
4. **Surrogate parse artefacts (extraction/):** Marker & Nougat are not installed on cherryrd and the central corpus has no pre-parsed copy for this arXiv id. Wrote `extraction/marker.md` and `extraction/nougat.mmd` as clearly-labelled surrogate parses derived from `work/paper.txt`, with equations reformatted and figures represented as placeholders.
5. **Main quantum-walk sim** — `report/evidence/nand_tree_qwalk.py`:
   - `build_graph(bits, n, M)`: builds vertex set (runway sites `-M..M` + tree levels `0..n` + `N=2^n` outer nodes) and edge list; only leaf↔outer edges depend on `bits`.
   - `hamiltonian(G)`: returns `H = -A(G)` as sparse CSC.
   - `initial_state(G, L)`: paper's packet on the runway.
   - `evolve_and_measure(bits, n, L, extra_M_factor=2.5)`: `ψ_T = expm_multiply(-i H (L/2)) ψ_0` (`scipy.sparse.linalg.expm_multiply`), returns `(P_right, P_left, P_tree+outer, dim, wall_seconds)`.
   - `sweep(n, L)`: iterates over all `2^N` boolean inputs.
   - `decision_check(rows)`: computes min-P₁ − max-P₀ gap and accuracy under midpoint threshold.
   - `nand_tree_value(bits)`: bottom-up ground truth.
   - Ran sweeps for `n=2, L∈{4,8,16,32}` and `n=3, L∈{8,16,32,64,96}`.
6. **Packet moments** — `report/evidence/verify_packet_moments.py`: verified `<H>=0` and `<H²>=5/L` (paper Eqs. 2.12–2.13) exactly for L ∈ {8,16,32,64}, both n=2 and n=3.
7. **Scaling + classical baseline** — `report/evidence/scaling_and_classical.py`:
   - Quantum scaling: finds min L to achieve 100% sweep accuracy at each n.
   - Classical randomized alpha-beta NAND evaluator with NAND short-circuiting and randomized child order (Snir 1985 / Saks-Wigderson 1986). Exhaustive over 2^N inputs for n≤3, random-sample 2000 inputs for n∈{4..7}, 50-200 trials each. Reports avg queries vs N^0.7538.
8. **Write REPORT.tex** — full section-by-section report with paper summary, claims table (C1-C6), method, results-vs-paper, verdict, and open-questions section.
9. **Compile REPORT.pdf** via `pdflatex -halt-on-error REPORT.tex` (two passes for TOC / cross-refs if any).
10. **Report artifacts:** `open_questions.json`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`.

## Tools & versions

| Tool | Version | Where |
|---|---|---|
| python3 | 3.13.9 | `/usr/local/bin/python3` |
| numpy | 2.4.3 | pip |
| scipy | 1.18.0 | pip (uses `sparse.linalg.expm_multiply`, Krylov, machine precision) |
| pdftotext | Poppler 25.x | homebrew |
| pdflatex | TeX Live 2025 | (system TeXLive) |
| marker | *(not installed)* | surrogate parse used |
| nougat | *(not installed)* | surrogate parse used |
| Argo LLM proxy | localhost:44497, key=stevens | free; used only during initial skim consulting (0-turn cost) |

## Work estimate

- Fetch + skim + core-fact extraction: ~5 min.
- Coding the graph builder, Hamiltonian, packet, evolution wrapper, sweep, decision check: ~15 min.
- Debug (n=3 needed larger L than sqrt(N) to reach 100% accuracy; identified and pushed L up to 96): ~5 min.
- Classical baseline + scaling scan (including one debug cycle around `2^(2^n)` blowup for n≥5): ~10 min.
- Extraction artefacts (marker.md, nougat.mmd surrogates): ~5 min.
- REPORT.tex + open_questions + workflow + artifacts_summary + failure_analysis: ~15 min.
- LaTeX compile + fix warnings: ~5 min.

**Total wall time: ~1 hour** (mostly subagent-side wall clock, real thinking/coding time on the same order).

## Compute footprint

- All compute local on cherryrd CPU. No GPU. No calls to any paid API.
- Peak memory well under 1 GB (largest sparse H for `n=3, L=96, M=240` has dim = 481 + 15 + 8 = 504, trivial).
- Total CPU wall time for all simulations: ~30 s.
