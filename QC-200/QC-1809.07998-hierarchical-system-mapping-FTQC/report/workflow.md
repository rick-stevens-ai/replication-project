# Workflow: independent replication of arXiv:1809.07998

**Paper:** Hwang & Choi (2018), *Hierarchical System Mapping for Large-Scale Fault-Tolerant Quantum Computing*, arXiv:1809.07998v1, 4 pages, ETRI.
**Replication host:** CherryRd (macOS Darwin 25.3.0, x86_64), Python 3 (system), matplotlib.
**Wall time:** ~25 minutes (fetch → REPORT.tex).
**Compute cost:** trivial (single-thread, seconds).

## Pipeline (numbered)

1. **Fetch.** `curl -sL -o paper.pdf https://arxiv.org/pdf/1809.07998` (143 KB, 4 pages).
2. **Text extraction.** `pdftotext paper.pdf work/paper.txt` → 522 lines. Verified authors (Yongsoo Hwang, Byung-Soo Choi, ETRI Daejeon) and title (`Hierarchical System Mapping for Large-Scale Fault-Tolerant Quantum Computing`). The `"1 "` prefix in the source TSV is confirmed OCR/page-number artifact — the real title begins with `Hierarchical`, matching the brief's expectation.
3. **Extract headline claims** from the text:
   - Table 1: Shor-128/256/512 QASM sizes, non-modular {1.7 TB, 14.2 TB, 39.0 TB} vs modular {23.5 MB, 88.1 MB, 338.6 MB}.
   - Fig 2: mapping wall-clock, non-mod {1.8e6, 1.5e7, 1.3e8} s vs modular {1.2e2, 5.9e2, 3.3e3} s. Shor-512: 1500 days → 1 hour.
   - Table 2: Shor-4/8/16 qubits & SWAPs, non-mod vs hierarchical.
   - Sec 1 p.2: for N calls to K-gate module, non-mod = K·N instructions, modular = K + N. Ratio → K asymptotically.
4. **Marker & Nougat parses.**
   - Neither is installed on CherryRd (`marker_single`, `nougat` not on PATH; `pip install marker-pdf` requires 3-4 GB torch download not attempted in the time budget).
   - Fallback: normalize `pdftotext` output into structured Markdown (`extraction/marker.md`, 11 KB) and Nougat-style `.mmd` with LaTeX-friendly math (`extraction/nougat.mmd`, 8.8 KB), both with explicit provenance headers stating the tool substitution. Section anchors, tables, and equations preserved.
5. **Design reproduction.** The paper's exact Table 1/Fig 2 numbers need ScaffCC (Scaffold compiler, LLVM-based, not currently installed) + a 128 GB RAM machine to build a 39 TB non-modular Shor-512 QASM. That's out of scope for a CPU-minutes replication. We instead reproduce (a) the *analytic* scaling identity K·N vs K+N with a toy Toffoli module, and (b) a small surface-code + magic-state footprint model per the QC wave brief that instantiates the same hierarchical / cached-module / bus-reuse spirit.
6. **Implement `report/evidence/repro.py`.**
   - **Part A (QASM scaling):** compute non_modular = K·N, modular = K + N, ratio = K·N/(K+N) for N ∈ {1, 5, 10, 45, 100, 1e3, 1e4, 1e5, 1e6}, K = 6 CNOT + 2 H + 7 T = 15 (Toffoli primitive count per Nielsen & Chuang Fig 4.9).
   - **Part B (surface-code footprint):** d = 5, 2 d² = 50 physical qubits per patch, 11 d² = 275 per 15-to-1 factory, 10 d = 50 code cycles per T-state, lattice surgery = d cycles. Two mappings:
     - *Naive flat:* one factory per T-gate (worst-case), Cliffords + T-injections serial, factory prep in parallel.
     - *Hierarchical:* pool of F ∈ {1..8} factories (choose F minimizing footprint) running continuously, T-injections pipelined, Cliffords overlap with factory prep.
   - Circuit sizes tested: 1, 5, 10, 45 Toffolis (45 ≈ a 5-qubit adder per QC brief note).
7. **Run.** `python3 report/evidence/repro.py` (~1 second). Emits: `qasm_scaling.csv`, `footprint.csv`, `summary.json`, `provenance.txt`, `footprint.png` (matplotlib, log-scale footprint + reduction %).
8. **Verdict determination.** QC brief rubric: `REPLICATED if hierarchical mapping shows measurable footprint reduction across multiple circuit sizes`. Result: 48%, 85.5%, 92.2%, 98.2% reduction at 1, 5, 10, 45 Toffolis → REPLICATED (mechanism + scaling). SPOT-CHECK for the exact Shor-128/256/512 headline numbers (out of reach on this host).
9. **Write REPORT.tex** with the full claim table, method, results, verdict, and 5 open questions (also stored in `report/open_questions.json`).
10. **Write failure_analysis.md and artifacts_summary.md.**

## Tools + versions (verified this run)

| Tool | Version | Role | Verified |
|------|---------|------|----------|
| `curl` | macOS system | Fetch arXiv PDF | ✓ |
| `pdftotext` | Poppler (Homebrew) | PDF → text | ✓ (522 lines out) |
| Python | 3 (system) | Repro script | ✓ (provenance.txt) |
| `matplotlib` | as installed | Footprint plot | ✓ (footprint.png present) |
| `pdflatex` | TeX Live (Homebrew) | Build REPORT.pdf | attempted |
| Marker | not installed | (fallback) | ✗ pdftotext-normalized |
| Nougat | not installed | (fallback) | ✗ pdftotext-normalized |
| ScaffCC | not installed | Exact Shor QASM | ✗ (Table 1/Fig 2 exact reproduction out of scope) |
| Argo LLM | localhost:44497 (`stevens`) | Optional judge | not used (self-verdict per brief) |

## What worked
- Analytic K·N → K + N scaling reproduced exactly (Part A).
- Surface-code footprint model shows monotone reduction across 4 sizes (Part B).
- Full 8-artifact deliverable within the wave-brief spec.

## What did not / partial
- Exact Table 1 / Fig 2 numeric reproduction (see failure_analysis.md).
- Marker + Nougat parses substituted with pdftotext-normalizations.

## Estimated effort
| Stage | Time |
|-------|------|
| Fetch + skim + claims extraction | ~5 min |
| Design + code repro.py           | ~8 min |
| Run + inspect outputs            | ~1 min |
| Write REPORT.tex + companions    | ~10 min |
| **Total wall time**              | **~25 min** |
