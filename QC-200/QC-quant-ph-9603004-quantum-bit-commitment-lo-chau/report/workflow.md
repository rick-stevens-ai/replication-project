# Workflow — QC-200 replication of Lo & Chau (arXiv:quant-ph/9603004)

Independent numerical reproduction of the Lo–Chau impossibility proof for
quantum bit commitment. This paper is a **proof paper**: no algorithm to
execute, but the argument's mathematical core (Uhlmann/HJW unitary that
lets Alice cheat undetectably in any perfectly-concealing scheme) can be
demonstrated numerically to machine precision using Qiskit statevector
plus `qiskit.quantum_info`.

## Tools & versions
| Tool | Version | Role |
|---|---|---|
| Python | 3.14.0 | Runtime |
| Qiskit | 2.5.0 | Statevector construction, partial trace, DensityMatrix, state_fidelity |
| NumPy | 2.4.3 | Reshape/SVD/polar for the cheating unitary U_A |
| SciPy | 1.18.0 | Available (unused in critical path) |
| Matplotlib | (auto) | Trade-off figure |
| poppler `pdftotext` | Homebrew | Fallback marker/nougat extraction |
| pdflatex (TeX Live 2026-03-01) | current | REPORT.tex → REPORT.pdf |
| curl | system | Fetch arXiv PDF |

**LLM usage**: none. All numerics are computed live, all prose is
hand-authored by the subagent, no Argo/LLM inference is in the numeric
loop or in scoring. (Free Argo endpoint would have been available if
needed for a 3-judge panel; the numerics are exact so a panel adds no
information.)

## Steps executed (in order)

1. **Fetch paper**
   ```
   curl -sL -o work/paper.pdf https://arxiv.org/pdf/quant-ph/9603004
   cp work/paper.pdf paper.pdf
   pdftotext work/paper.pdf work/paper.txt          # for reading
   pdftotext -layout work/paper.pdf work/paper_layout.txt   # for marker.md
   pdftotext -raw    work/paper.pdf work/paper_raw.txt      # for nougat.mmd
   ```
   Authors verified from the fetched PDF: **Hoi-Kwong Lo & H. F. Chau**,
   Institute for Advanced Study (later BRIMS/HP Labs and HK U.).

2. **Skim paper** (`work/paper.txt`, ~2 min). Extracted the reproducible
   core: two claims (perfect-concealing ⇒ U_A exists; ε-concealing ⇒
   P_cheat ≥ 1 − O(√ε)) plus the BB84 EPR-attack motivating example.

3. **Set up sim environment**
   ```
   python3 -m venv work/.venv
   source work/.venv/bin/activate
   pip install qiskit numpy scipy matplotlib
   ```
   Verified `import qiskit; qiskit.__version__ == '2.5.0'` and that
   `qiskit.quantum_info.{Statevector, DensityMatrix, partial_trace,
   state_fidelity}` all load.

4. **Author the replication script**
   `report/evidence/lo_chau_replication.py` (≈500 LOC).
   Three parts:
   - **PART 1 (C1, C2, ideal)** — 3-qubit GHZ / +/− protocol; verify
     ρ_B_0 = ρ_B_1; construct U_A on 4-dim Alice space via SVD of
     Y = M0 M1†; check unitarity and (U_A⊗I)|Ψ_0⟩ = |Ψ_1⟩.
   - **PART 2 (C3, non-ideal)** — 2-qubit Bell-like family
     |Ψ_b(θ)⟩; analytic F(ρ_B_0,ρ_B_1) = sin² 2θ; Uhlmann optimum
     P_cheat = F; 41-point sweep θ ∈ [0.05, π/2 − 0.05]; write CSV.
   - **PART 3 (C4, sanity)** — BB84 one-Bell-pair concealing check;
     verify ρ_B = I/2 to 10⁻¹⁶; Alice-outcome probabilities 0.5/0.5.

5. **Debug** — hit two issues:
   - a leftover dead line in the SVD-alignment helper that
     `matmul`-failed on shape (4,2)·(2,4); resolved by rewriting
     `unitary_via_polar_decomposition` to use the direct Uhlmann-optimal
     formula `U_A = Vhy† Uy†` from SVD of `Y = M0 M1†`.
   - Qiskit 2.5.0 has renamed some paths since older code snippets; used
     the modern `qiskit.quantum_info` API throughout.

6. **Run** end-to-end (< 3 s):
   ```
   python3 report/evidence/lo_chau_replication.py > report/evidence/run.log
   ```
   Outputs: `results.json`, `tradeoff_curve.csv`, `run.log`.

7. **Plot**
   ```
   python3 report/evidence/plot_tradeoff.py
   ```
   Writes `report/evidence/tradeoff_curve.png` (2-panel: linear + log-log).

8. **Write LaTeX report** `report/REPORT.tex` (5 pages) with claims table,
   methods, results-vs-paper table, verdict, and the mandatory 5 open
   questions section. Compile:
   ```
   cd report && pdflatex -interaction=nonstopmode REPORT.tex   # x2
   ```
   → `report/REPORT.pdf` (5 pages, 329 KB).

9. **Write extractions** (marker.md, nougat.mmd) as pdftotext fallbacks —
   same convention as sibling QC-200 directories where marker/nougat
   weren't installed; extractions are byte-faithful to the original PDF's
   text stream.

10. **Write open_questions.json** (5 heavy-duty items with `q`, `basis`,
    `next_steps` — machine-readable per REPLICATION_DIR_STANDARD).

11. **Write this workflow.md**, `artifacts_summary.md`, `failure_analysis.md`.

12. **Final verdict**: **REPLICATED** — all 4 numerically-testable claims
    reproduced to machine precision.

## Estimated effort
- Paper fetch + read: ~5 min
- Environment setup: ~1 min (qiskit install)
- Replication script authoring: ~15 min
- Debug: ~3 min (one shape bug, one dead-code artifact)
- Run + plot: <10 s wall clock
- Report/tex/pdf: ~10 min
- Extractions + companion docs: ~5 min
- **Total wall-clock: ~40 min** (single subagent turn)
- **Compute cost: <1 CPU-second**; no GPU; no LLM inference; no paid endpoints

## Directory layout produced
```
QC-quant-ph-9603004-quantum-bit-commitment-lo-chau/
├── paper.pdf                          # original arXiv PDF (105 KB)
├── extraction/
│   ├── marker.md                      # pdftotext -layout fallback
│   └── nougat.mmd                     # pdftotext -raw fallback
├── work/
│   ├── paper.pdf, paper.txt           # working copies
│   ├── paper_layout.txt, paper_raw.txt
│   └── .venv/                         # local qiskit venv
└── report/
    ├── REPORT.tex, REPORT.pdf         # compiled 5-page report
    ├── REPORT.aux, REPORT.log, REPORT.out
    ├── open_questions.json            # 5 heavy-duty Q's
    ├── workflow.md                    # this file
    ├── artifacts_summary.md
    ├── failure_analysis.md
    └── evidence/
        ├── lo_chau_replication.py     # main script
        ├── plot_tradeoff.py           # figure script
        ├── results.json               # all numerics
        ├── tradeoff_curve.csv         # 41-point sweep
        ├── tradeoff_curve.png         # figure
        └── run.log                    # stdout of the run
```
