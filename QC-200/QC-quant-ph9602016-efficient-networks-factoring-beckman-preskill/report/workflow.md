# Workflow — QC-quant-ph9602016 replication

## One-line
Rebuilt the paper's Sec. VII N=15 special-purpose factoring circuit gate-for-gate in Qiskit, ran it on a statevector simulator, cross-checked with a generic 12-qubit Shor QPE, and had a free-endpoint LLM judge score six per-claim reproductions.

## Stages

| # | Stage | Tool / codebase | Command | Notes |
|---|-------|-----------------|---------|-------|
| 1 | Read wave brief | shell | `cat ~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md` | Rules: free endpoints, real replication, LLM-judge, 8-artifact bar |
| 2 | Set up target dir | shell | `mkdir -p <TARGET>/{work,report/evidence,extraction}` | Do NOT overwrite siblings |
| 3 | Fetch paper | `curl` | `curl -sL https://arxiv.org/pdf/quant-ph/9602016 -o paper.pdf` | 490 KB, 56 pp. |
| 4 | Text extraction | `pdftotext` (poppler) | `pdftotext paper.pdf work/paper.txt` | marker/nougat not installed locally or on uicgpu — fallback to pdftotext with Markdown/mmd wrapping |
| 5 | Identify claims | manual grep + read | `grep -n "38\|Toffoli\|N = 15" work/paper.txt` | Six concrete Sec. VII claims (C1-C6) extracted |
| 6 | Build Qiskit env | Python venv | `python3 -m venv .venv && pip install qiskit qiskit-aer numpy sympy` | qiskit 2.5.0, qiskit-aer 0.17.2 |
| 7 | Implement Eq. (7.5) | Qiskit | `work/shor_n15.py::paper_expn_x7_n15` | Right-to-left algebraic → left-to-right physical ordering |
| 8 | Verify lookup Eq. (7.3) | AerSimulator statevector | `python work/shor_n15.py` → Step 1 | 4/4 rows deterministic match |
| 9 | Run "factor 15" full circuit | AerSimulator statevector | `python work/shor_n15.py` → Step 2 | 6 qubits, 8000 shots, y ∈ {0,1,2,3} near-uniform, r=4, factors {3,5} |
| 10 | Generic Shor QPE (independent) | AerSimulator statevector | `python work/shor_n15.py` → Step 3 | 12 qubits (8 counting + 4 target), peaks at y ∈ {0,64,128,192}, r=4, factors {3,5} |
| 11 | N=21 sanity extension | AerSimulator statevector | `python work/shor_n21.py` | x=2 → r=6, factors {3,7}; x=4 → r=3 (odd, correct no-factor) |
| 12 | Gate-count vs Eq. (7.6) | Qiskit `count_ops()` | `python work/resource_counts.py` | Match: [6,0,4] paper = [6,0,4] ours |
| 13 | Cirac-Zoller pulse budget | manual + Qiskit counts | idem | 30 + 2 + 6 = 38 pulses, exact match |
| 14 | LLM-judge scoring | Argo aggregator (free) | `JUDGE_MODEL=argo:gpt-5.4 python work/llm_judge.py` | `overall_verdict = REPLICATED` |
| 15 | Stage evidence | shell | `cp work/*.{py,log,json} report/evidence/` | 8 files |
| 16 | Write REPORT.md, REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md | editor | — | 8-artifact bar |

## Tool / code inventory
- Python 3.14, Qiskit 2.5.0, qiskit-aer 0.17.2, numpy, sympy.
- `pdftotext` (poppler).
- Argo LLM proxy: `argo:gpt-5.4` via aggregator `http://<tailnet-aggregator>:4000/v1` (free per Rick's standing rule).
- Host: CherryRd (macOS 25.3.0, x86_64). No GPU used — problem size is trivial.
- All code in `work/*.py` (mirrored to `report/evidence/`).

## Effort estimate

| Phase | Time |
|-------|------|
| Read brief + set up dir + fetch paper | 3 min |
| Read Sec. VII, identify testable claims | 8 min |
| Build Qiskit venv | 2 min |
| Implement `paper_expn_x7_n15`, `factor_15_paper_special_purpose`, `general_shor_n15_qpe` | 15 min |
| Debug (lookup table verification, register order) | 3 min |
| N=21 extension | 4 min |
| Gate/pulse counting | 5 min |
| Argo endpoint troubleshoot (44497 → 4000, opus-4.8 → gpt-5.4) | 5 min |
| Write REPORT.md + REPORT.tex + open_questions.json + workflow.md + artifacts_summary.md + failure_analysis.md | 15 min |
| **Total** | **~60 min** |

Compute: negligible. Statevector sim of a 12-qubit circuit runs in <100 ms on any laptop.

## What made this go fast
- The paper's Sec. VII is unusually explicit — Eq. (7.5) is a literal gate list you can transcribe. No reverse-engineering required.
- The special-purpose N=15 network was designed to be tiny (6 qubits) precisely so that it could be demonstrated on 1996-era hardware. That also makes it trivial on 2026-era simulators.
- Qiskit's `AerSimulator` needs zero infrastructure — pip install and go.

## What would take longer if extended
- The full Sec. VI general-purpose EXP_N network (open Q1) would need ~1-2 days of Qualtran + resource-counting work to independently reproduce the 72K³ / 396K³ coefficients.
- A modern-ion-trap re-derivation (open Q2) would need a proper Sørensen-Mølmer cost table and possibly conversation with a trapped-ion experimentalist.
