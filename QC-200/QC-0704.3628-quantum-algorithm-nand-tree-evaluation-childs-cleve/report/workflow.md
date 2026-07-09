# Workflow — replication of arXiv:0704.3628 (Ambainis, NAND tree)

## Narrative

1. **Fetch paper.** `curl` the arXiv PDF into the target dir. Verified 21-page PDF (281 KB).
2. **Verify author + title from the fetched PDF.** The subagent task text guessed "Childs, Cleve, Jordan, Yeung"; pdftotext of page 1 revealed the actual author is **Andris Ambainis** (single author, University of Waterloo). Title verified: *"A nearly optimal discrete query quantum algorithm for evaluating NAND formulas."*
3. **Skim key sections.** Read Sec 1 (context: FGG breakthrough, Childs et al. discrete conversion, Ambainis's improvement to O(√N) exactly optimal), Sec 3.2 (algorithm: tree + tail, Hermitian H, U₁=2P_kerH−I, U₂=oracle, ψ_start on even tail sites, phase estimation on W=U₂U₁), and Theorem 3 (the two-case success guarantee).
4. **Design real simulation.** Statevector linear algebra with numpy only. Complete balanced binary tree of depth n has all-ones H edge weights. Build T' with BFS-indexed tree vertices [0..2^(n+1)−2] and appended tail [2^(n+1)−1..2^(n+1)−2+t]. Compute ker(H) via np.linalg.eigh, |ψ_start''> = P_ker sum(|even tail>) normalised, U₁ = 2P_ker − I, U₂ diag(±1). Textbook phase estimation on W = U₂U₁ sampled exactly by eigendecomposition (no register truncation error, so scaling artefacts are purely due to 2^m register-size).
5. **Smoke test at n=2 (N=4).** Hand-verified that eigenphases and overlaps match Theorem 3: x=0000 gives 100% overlap on θ=0 eigenstate; x=1111 gives ±π/3 phases.
6. **Bipartite parity issue at odd n.** First sweep (n=2,3,4,5) failed at n=3,5 with ||P_ker ψ_start||=0. Root-caused: T' is bipartite; when tree bipartition is dominated by the leaf-side (odd n), no color-0-supported vector lies in ker(H). Restricted to even n and documented in `report/failure_analysis.md`.
7. **Full sweep.** n ∈ {2,4,6,8}, N ∈ {4,16,64,256}, 60 trials each (balanced 30 T=0 / 30 T=1 via accept-reject), C=5 majority-vote shots, m = ceil(log2(4·√N)) phase-register bits. Runtime 95 s wall on CherryRd.
8. **Classical baseline.** Snir/Saks-Wigderson randomised query LB N^0.7537... computed for the same N grid.
9. **Empirical scaling fit.** Linear regression log(queries) vs log(N) → slope 0.528 (0.518 excluding n=2), consistent with paper's 0.5.
10. **Verdict + write-up.** REPLICATED. Wrote REPORT.tex (very detailed, section-by-section), open_questions.json (5 non-superficial), this workflow.md, artifacts_summary.md, failure_analysis.md.

## Tools + versions

| Tool / library | Version | Purpose |
|----------------|---------|---------|
| Python | 3.13 | Runtime |
| NumPy | 2.4.3 | Linear algebra: eigh, eig, matmul, RNG |
| SciPy | 1.18.0 | (available but not directly needed; eigh via numpy sufficed) |
| PyMuPDF (`fitz`) | 1.27.2.3 | Extraction surrogate for Marker (page-boundary text extraction) |
| `pdftotext` | Poppler-provided | Extraction surrogate for Nougat (`-layout` reflow) |
| `curl` | macOS system | Fetching paper PDF |
| Argo LLM proxy | localhost:44497 | *Not used* for this replication — pure classical simulation, no LLM inference needed for the science. |

**No paid endpoints used.** No quantum hardware. No GPU. All reproducible on any laptop with Python + numpy.

## Code (all in `report/evidence/`)

| File | LOC | Purpose |
|------|-----|---------|
| `nand_tree_walk.py` | ~330 | Tree/tail construction, U₁/U₂/ψ_start build, textbook PE sampled exactly, balanced-input scaling harness. |
| `classical_baseline.py` | ~55 | Snir randomised query lower bound N^0.7537... side-by-side vs empirical quantum queries. |
| `scaling_results.json` | (data) | 60-trial-per-N sweep results, seed 20260705. |
| `classical_vs_quantum.json` | (data) | Baseline table. |

## Effort estimate

- **Wall clock (agent):** ~30 min end-to-end (paper fetch → skim → design → build → smoke → debug parity → full sweep → write-up).
- **Compute:** 95 s (single-threaded numpy on a MacBook-class CPU). Zero GPU/HPC used.
- **Human/agent steps:** ~15 tool calls (fetch, pdftotext, mkdir, write nand_tree_walk.py, 3 sanity Python one-liners, one debug edit, full sweep run, classical baseline run, one aggregation Python one-liner, 5 write calls for REPORT/QA/workflow/etc.).
- **LOC written by agent:** ~385 lines of Python (evidence code) + ~1400 lines of documentation (LaTeX report + 4 markdown docs + open questions).
- **Runs executed:** 6 total (2 smoke tests, 1 parity-debug, 2 full sweeps — one before and one after switching to balanced sampling, plus 1 classical-baseline run).
- **External API calls:** 1 (arXiv PDF fetch via curl). No LLM calls.
