# Artifacts summary — quant-ph/0702144 replication

Directory: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0702144-hamiltonian-nand-tree-farhi/`

## Top-level

| Path | Bytes | What it is |
|---|---|---|
| `paper.pdf` | 220997 | Original arXiv PDF, `quant-ph/0702144v2` (fetched 2026-07-05). |
| `extraction/marker.md` | ~11 KB | Surrogate Marker parse (labelled as such in header). |
| `extraction/nougat.mmd` | ~7.7 KB | Surrogate Nougat parse (labelled as such in header). |
| `work/paper.txt` | ~40 KB | `pdftotext` extraction. |
| `work/scaling_stdout.log` | ~1 KB | stdout of the scaling+classical scan. |
| `report/REPORT.tex` | ~16 KB | Full LaTeX report with claims table, method, results, verdict, open questions. |
| `report/REPORT.pdf` | (compiled) | Compiled PDF of REPORT.tex. |
| `report/open_questions.json` | ~4 KB | 5 new open questions each with `{q, basis, next_steps}`. |
| `report/workflow.md` | ~4.6 KB | End-to-end workflow, tool versions, work estimate. |
| `report/artifacts_summary.md` | this file. | |
| `report/failure_analysis.md` | ~4 KB | Honest failure analysis / friction / residual gaps. |

## Code artifacts (`report/evidence/`)

| Path | What |
|---|---|
| `nand_tree_qwalk.py` | Main sim: graph builder, `H = -A(G)`, initial packet, `expm_multiply` evolution, sweep across all `2^N` boolean inputs, decision-rule accuracy. |
| `nand_tree_results.json` | Full sweep results: per-input `(bits, truth, P_right, P_left, P_other, dim)` for `(n,L)` ∈ `{(2,4),(2,8),(2,16),(2,32),(3,8),(3,16),(3,32),(3,64),(3,96)}`. |
| `verify_packet_moments.py` | Verifies paper Eqs. 2.12–2.13: `<H>=0`, `<H²>=5/L`. |
| `packet_moments.json` | Output; exact matches at `L ∈ {8,16,32,64}` for both `n=2,3`. |
| `scaling_and_classical.py` | (A) Quantum: min L for 100% sweep accuracy at n=2,3. (B) Classical Snir/Saks-Wigderson randomized evaluator, n∈{2..7}. |
| `scaling_and_classical_results.json` | Full JSON of both scans. |

## Trace summary (headline numbers)

* Quantum sweep, n=2 (N=4), L=32, M=80: 100% accuracy on all 16 inputs, gap `Δ P(right) = 0.657`.
* Quantum sweep, n=3 (N=8), L=96, M=240: 100% accuracy on all 256 inputs, gap `Δ P(right) = 0.788`.
* Packet moment check: `<H²> = 5/L` reproduced to 6 decimal places for `L ∈ {8,16,32,64}`.
* Classical randomized average queries: n=2→2.64, n=3→3.78, n=4→6.87, n=5→9.34, n=6→17.32, n=7→21.32 (vs `N^0.7538 ≈ 2.84, 4.79, 8.08, 13.63, 22.99, 38.76`).

## Provenance

All code by the QC-200 subagent, 2026-07-05, on cherryrd. Deterministic:
- No RNG in the quantum sim (dense/sparse deterministic linear algebra).
- Classical baseline seeded `Random(0xC0FFEE ^ n)`.
- LaTeX built by TeX Live pdflatex.

No paid API calls. Argo (free) was available but not needed for the replication itself.
