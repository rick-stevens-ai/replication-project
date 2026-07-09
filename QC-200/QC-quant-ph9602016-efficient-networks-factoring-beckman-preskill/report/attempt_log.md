# Attempt log — 2026-07-06 (chronological)

## 12:10 CDT — Task received
Subagent under X-100 wave. Assigned paper: quant-ph/9602016 (Beckman-Chari-Devabhaktuni-Preskill 1996), Efficient networks for quantum factoring. Target dir: `QC-200/QC-quant-ph9602016-efficient-networks-factoring-beckman-preskill/`.

Read `WAVE_BRIEF_2026-07-01.md`. Confirmed rules: free endpoints only (Argo/Sophia/CELS), real replication, LLM-judge scoring, 8-artifact bar (paper.pdf, extraction/marker.md, extraction/nougat.mmd, report/REPORT.tex, report/REPORT.md with Open Questions, report/open_questions.json, report/workflow.md, report/artifacts_summary.md, report/failure_analysis.md).

## 12:11 — Fetch paper
`curl -sL https://arxiv.org/pdf/quant-ph/9602016 -o paper.pdf` → 490,992 B PDF v1.4, 56 pp. `pdftotext -layout` → 2,976 lines of clean text.

## 12:12 — Locate testable claims
Grep for "38\|Toffoli\|N = 15\|K = 4" identified Sec. VII (pp. 42-45) as the concrete testable core:
- Eq. (7.3): lookup table for 7^a mod 15
- Eq. (7.5): explicit EXP_N(7,15) network
- Eq. (7.6): complexity [6, 0, 4]
- Headline: 38 laser pulses on Cirac-Zoller ion trap, 6 storage qubits.

## 12:13 — Check for pre-parsed extractions
`find ~/Dropbox/REPLICATE-PROJECT/PARSED_CORPUS -iname "*9602016*"` → 0 hits. Have to produce marker.md / nougat.mmd from scratch.

## 12:14 — Check for marker / nougat tools
Local: `which marker nougat` → not found. uicgpu: `ssh uicgpu 'which marker nougat'` → also not found. Fallback: pdftotext + Markdown wrap with provenance header.

## 12:14 — Set up Qiskit venv
`python3 -m venv .venv && pip install qiskit qiskit-aer numpy sympy` → qiskit 2.5.0, qiskit-aer 0.17.2.

## 12:15 — Write `shor_n15.py`
Three functions:
1. `paper_expn_x7_n15()` — builds Eq. (7.5) exactly, right-to-left algebraic → left-to-right physical ordering.
2. `verify_lookup_table()` — for each a ∈ {0,1,2,3}, apply EXP_N to |a⟩|0⟩ and check output = |a⟩|7^a mod 15⟩.
3. `factor_15_paper_special_purpose()` — full 6-qubit "factor 15" circuit with QFT_2 and measurement.
4. `general_shor_n15_qpe()` — independent Kitaev-Shor QPE with 8 counting + 4 target qubits, using controlled-permutation for x^{2^j} mod 15.

## 12:16 — First run
Step 1 (lookup): all 4 rows match Eq. (7.3). ✓
Step 2 (special-purpose): y ∈ {0,1,2,3} distribution: 2020/1926/2046/2008 out of 8000. r=4 recovered. Factors {3,5}. ✓
Step 3 (generic Shor): peaks at y ∈ {0,64,128,192}, all near-equal (~2000 shots each). r=4 from y=64, factors {3,5}. ✓

## 12:17 — N=21 sanity extension
`shor_n21.py` — same generic Shor QPE.
- N=21, x=2: r=6 recovered from y=43 (256/6 ≈ 42.67), factors {3,7}. ✓
- N=21, x=4: r=3 (odd, correctly no factor via this base). ✓

## 12:17 — Resource count comparison
`resource_counts.py` — Qiskit `count_ops()` on the Eq. (7.5) build: {x: 6, ccx: 4}. Paper Eq. (7.6): [6, 0, 4]. **Exact match.**

Cirac-Zoller pulse budget under paper's App. A cost model:
  30 (EXP_N: 6·1 + 0·3 + 4·6) + 2 (superposition H) + 6 (QFT_2 L(2L-1)) = 38 pulses. Matches paper's headline exactly.

## 12:17 — Extraction production
`make_extractions.py` — `pdftotext paper.pdf -` output wrapped with section-heading regex (`I. INTRODUCTION AND SUMMARY` → `## I. INTRODUCTION AND SUMMARY`), split into marker.md and nougat.mmd (both 138 KB) with provenance banners.

## 12:20 — LLM-judge scoring — first attempt
`llm_judge.py` with `argo:claude-opus-4.8` via `localhost:44497`. All 4 retries: HTTP 502 Bad Gateway. (Sanity check: `pong` prompt works fine — issue seems payload-size / model-specific.)

## 12:23 — LLM-judge — second attempt
Switched to aggregator `<tailnet-aggregator>:4000` (per TOOLS.md), still `argo:claude-opus-4.8`. Same 502.

## 12:25 — LLM-judge — success
Switched judge model to `argo:gpt-5.4`. First attempt succeeded, ~10s. Parsed JSON verdict:
```
{"per_claim": {"C1"..."C6": all REPRODUCED},
 "overall_verdict": "REPLICATED",
 "one_line": "All six tested Sec. VII N=15 claims are directly supported by the provided simulator evidence."}
```
Written to `report/evidence/llm_judge_verdict.json`.

## 12:26 — Stage evidence
`cp work/*.{py,log,json} report/evidence/` — 8 files.

## 12:27 — Write reports
- `report/REPORT.md`: paper summary, 10-row claims table (C1..C10), 10-step Method, per-section Results vs paper, Open Questions Q1..Q5.
- `report/REPORT.tex`: same content in LaTeX for the required "very detailed section-by-section" TeX artifact.
- `report/open_questions.json`: 5 heavy-duty questions with {q, basis, next_steps}.
- `report/workflow.md`: 16-stage table, tool inventory, effort estimate.
- `report/artifacts_summary.md`: 8-artifact checklist with paths.
- `report/failure_analysis.md`: 3 friction points (F1..F3), all worked around.
- `report/brief.md`: 1-paragraph what/why/result.
- `report/artifact_harvest.md`: URLs + SHA-256 checksums.

## 12:32 — Verification
All 8 required artifacts present. Verdict: REPLICATED.
