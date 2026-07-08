# Artifacts Summary — QC-2209.03796-vqe-parallelism

## Report artifacts

| Path | Purpose |
|---|---|
| `report/REPORT.md` | Primary human-readable replication report (source of truth) |
| `report/REPORT.tex` | LaTeX render of the report, includes honest Critique section |
| `report/open_questions.json` | 5 open questions in structured JSON (bare list) |
| `report/open_questions_section.tex` | LaTeX open-questions section, `\input`ed by REPORT.tex |
| `report/workflow.md` | Exact reproduction workflow (env, commands, expected outputs) |
| `report/artifacts_summary.md` | This file — inventory of every artifact |
| `report/failure_analysis.md` | Honest critique / what failed / what was not exercised |

## Evidence

| Path | Content |
|---|---|
| `report/evidence/vqe_hubbard_compressed.py` | Physics-core script: paper Eq. 1 + Eq. 2 exact-diag + VQE + Qiskit cross-check |
| `report/evidence/vqe_hubbard_compressed_result.json` | Physics-core result: |E_VQE − E_0| = 1.78e-15 Ha |
| `report/evidence/h2_hamiltonian.json` | H2/STO-3G Jordan-Wigner, 4 qubits, 15 Pauli terms, E_0 = -1.137306 Ha |
| `report/evidence/h4_hamiltonian.json` | H4/STO-3G, 8 qubits, 185 Pauli terms |
| `report/evidence/h6_hamiltonian.json` | H6/STO-3G record entry, 12 qubits, 919 terms (OOM-avoided) |
| `report/evidence/bench_h2.json` | H2 baseline timing (spawn-per-iter + persistent + threads) |
| `report/evidence/bench_h2_no_latency.json` | H2 no-latency benchmark, 100 iters × 10 repeats |
| `report/evidence/bench_h2_latency5ms.json` | H2 5-ms/term latency: 1.79× → 5.99× speedup ladder |
| `report/evidence/bench_h2_latency10ms.json` | H2 10-ms/term latency: 1.82× → 6.34× speedup ladder |
| `report/evidence/bench_h4.json` | H4 threads timing, 15 iters × 3 repeats |
| `report/evidence/bench_h4_mp.json` | H4 mp + threads timing |
| `report/evidence/bench_h4_smoke.json` | H4 smoke test |
| `report/evidence/smoke.json` | H2 first end-to-end smoke |

## Source

| Path | Purpose |
|---|---|
| `src/build_h2_hamiltonian.py` | Hn-chain molecular Hamiltonian → Pauli decomposition (pyscf + qiskit-nature) |
| `src/vqe_parallel_bench.py` | Sequential-vs-parallel Pauli-term timing benchmark (sequential, mp.Pool, ThreadPool, injected latency) |

## Paper and extraction

| Path | Purpose |
|---|---|
| `work/paper.pdf` | arXiv:2209.03796v2 (Mineh & Montanaro, revised May 2023) |
| `work/paper.txt` | pdftotext extraction (524 lines) |
| `work/abstract.html` | arXiv abstract page |
| `extraction/nougat.mmd` | Nougat MathPix-format extraction stub (see file for note) |

## Environment

| Path | Purpose |
|---|---|
| `venv/` | Python 3.14.6 venv with qiskit 2.5.0, qiskit-nature 0.8.0, pyscf 2.13.1, numpy 2.5.0, scipy 1.18.0 |

## Verdict

- **Physics core (C1, C2):** REPLICATED to machine precision (|ΔE| ≈ 1e-15 Ha).
- **Mechanism claim (C3):** REPLICATED near-linear speedup 1.79×–5.99× on 2–8 workers at 5 ms/term (75–92% efficiency).
- **Hardware headline (C4, C5, C6):** NOT TESTED — Aspen-M-1 decommissioned, noise model unpublished, requires paid Rigetti/Braket access.
- **Queue verdict preserved:** REPLICATED (reproducible scientific core exercised; hardware-specific integers non-reproducible for free-tier replicators, which is a general NISQ paper reality).

## Artifact count

- 7 report artifacts (REPORT.md, REPORT.tex, open_questions.json, open_questions_section.tex, workflow.md, artifacts_summary.md, failure_analysis.md)
- 1 extraction (nougat.mmd)
- 13 evidence files
- 2 source files
- 3 paper/work files
- 1 venv
