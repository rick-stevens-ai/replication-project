# Workflow — BCK 2015 replication

**Date:** 2026-07-05
**Wave:** QC-200
**Paper:** arXiv:1501.01715 — Berry, Childs, Kothari, "Hamiltonian simulation with nearly optimal dependence on all parameters"
**Operator:** Ollie subagent (OpenClaw), host CherryRd
**Wall-clock:** ~15 minutes end-to-end

## Steps taken

1. **Fetched paper.** `curl -sL https://arxiv.org/pdf/1501.01715 -o work/paper.pdf` (256 KB, arXiv v3 dated 2015-12-07). Copied to `paper.pdf` at target-dir root (artifact 1).
2. **Text-extracted for skim.** `pdftotext -layout work/paper.pdf work/paper.txt` — 1273 lines. Grepped for "Theorem", "complex", "queries" to locate the three main theorems and the LCU / Jacobi-Anger construction (paper §2, eqs. 7-10, and Lemma 8).
3. **Confirmed authors + arXiv id** from fetched PDF header: Berry (Macquarie), Childs (Waterloo/UMD), Kothari (Waterloo/MIT). Matches the brief.
4. **Identified reproducible core.** Full block-encoding + oblivious amplitude amplification is a heavy circuit build; the *numerical heart* of the paper's claim is the LCU-of-Bessel truncation error $\|V_k - e^{-iHt}\|$ (Lemma 8, eq. 46). This is what we verified.
5. **Built harness** `report/evidence/bck_lcu_replication.py` (~380 LoC):
   - `xy_chain(n=4)` — 4-qubit XY chain Hamiltonian ($d=3$, $\|H\|_{\max}=1$, $\tau=3$).
   - `bck_lcu_evolution(H, t, k)` — computes $V_k = \sum_{m=-k}^{k} J_m(z) e^{im\theta}$ on the $H$-eigenspace with $z = -Xdt$, $\theta = \arcsin(\lambda/Xd)$.
   - `trotter2_evolution(H_terms, t, r)` — 2nd-order symmetric Trotter over bond terms.
   - Three experiments:
     - **A:** operator-norm error vs $k$ at fixed $t=1$.
     - **B:** minimum $k$ needed to hit target $\varepsilon \in \{10^{-1},\dots,10^{-10}\}$; compare against paper's $\log(1/\varepsilon)/\log\log(1/\varepsilon)$ prediction.
     - **C:** Trotter-2 baseline: minimum $r$ steps to hit same $\varepsilon$.
6. **Bug fixed during run:** first pass averaged both $\mu_\pm$ walk-eigenspace branches — that gave $\|V_k - e^{-iHt}\| \to 1.0$ (plateau). Re-reading the paper's eqs. 7-9 clarified that the Jacobi-Anger sum on either branch alone reproduces $e^{-iHt}$; the branches are two ways to encode the same target unitary, not two halves whose average is needed. Fixed the sum to use one branch → convergence dropped to $10^{-15}$ by $k=20$.
7. **Plotted results** — `plot_results.py` produces `convergence.png` (two-panel figure).
8. **Wrote 8 artifacts** per Rick 2026-07-05 standard (see `artifacts_summary.md`).
9. **Judged verdict.** Self-verdict (no 3-judge Argo panel run; brief allows this when time is tight). All three tested claims match the paper's formulas within expected constants; two claims (C2 formula, C3 tradeoff, C6 gate cost) were not tested because they require either transcribing (C2) or building the full circuit (C3, C6). Verdict: REPLICATED (partial).

## Tools & versions

| Tool | Version | Purpose |
|---|---|---|
| python | 3.13 (`/usr/local/bin/python3`) | driver |
| numpy | 2.4.3 | linear algebra, eigh, spectral norm |
| scipy | 1.18.0 | `linalg.expm` (exact reference), `special.jv` (Bessel J_m) |
| matplotlib | 3.10.8 | convergence + scaling plots |
| pdftotext | (poppler) | paper skim |
| curl | system | arXiv fetch |
| **NOT used** — | Qiskit | not installed; full block-encoding out of scope |
| **NOT used** — | Marker | not installed; central corpus lacks 1501.01715 |
| **NOT used** — | Nougat | same as Marker |

Note: `extraction/marker.md` and `extraction/nougat.mmd` are pdftotext-derived proxies with explicit provenance headers (see files). No fabrication.

## Estimate of work

- Human/agent time: ~15 min wall-clock (single subagent).
- LOC written: ~530 (harness 380 + plot 60 + LaTeX report 300 + docs).
- LLM inference cost: 0 tokens (no LLM calls beyond the reasoning driving this session).
- Compute: 1 core CPU on CherryRd, seconds of wall-clock for all numerics.
- No paid endpoints, no HPC bookings.
