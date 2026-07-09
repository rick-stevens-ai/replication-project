# Workflow — OSTI 3020556 Replication

**Paper:** Powis et al 2026, *Plasma Sources Sci. Technol.* **35** 025002.
**DOI:** 10.1088/1361-6595/ae3985 · **OSTI:** 3020556
**Domain:** accelerator_plasma (priority rank 3)
**Strategy:** Analytic-core replication of the CSHI spoke-frequency prediction (Eq.4 of Ref [93], Powis 2018, arXiv:1805.04438). Full 2D PIC benchmark (C6) is out of scope for a <25-min efficient replication.

---

## Stage 1 — Target harvest

1. `ssh uicgpu` to reach a free-endpoint host.
2. `source ~/env.sh` (proxy config for OSTI reachability).
3. Fetch OA PDF:
   ```
   curl -sL https://www.osti.gov/servlets/purl/3020556 -o /tmp/osti_3020556.pdf
   ```
4. Compute MD5 (`be1c310a…`) and record in `work/artifact_harvest.md`.
5. Verify PDF is digital (no OCR required) — `pdftotext` produces clean text.

## Stage 2 — Extract testable claims

1. Read the target PDF (`pdftotext` → text; scan Table 1, Sec 3, and any equation invoking CSHI theory).
2. Enumerate testable claims into a claims table (C1–C6):
   - Analytic scalar predictions (C1, C5)
   - PIC measurement (C2)
   - Parameter self-consistency (C3)
   - Scaling laws (C4)
   - Full-PIC reproducibility (C6, marked out-of-scope)
3. Identify the paper's supporting reference for the analytic formula → Ref [93].

## Stage 3 — Resolve the formula source

1. Search arXiv API for Powis 2018 Simon–Hoh spoke prediction → hit arXiv:1805.04438.
2. Download: `curl -sL https://arxiv.org/pdf/1805.04438 -o /tmp/ref93.pdf`.
3. Compute MD5 (`6f7769ad…`).
4. Extract Eqs. 3–4:
   ```
   ω_s,th = √(e Eᵣ Lₙ / mᵢ) · k         (Eq.3)
   f_s,th = (1/(π R0)) · √(e Eᵣ Lₙ / mᵢ) (Eq.4, k = 2/R0)
   ```

## Stage 4 — Reimplement in Python

1. Write `work/replicate_spoke.py`:
   - Standard SI constants (`e`, `m_e`).
   - Table 1 inputs: `m_i = 7291.712 * m_e`; `E_r = 100 V/m`; `L_n = 7.1e-3 m`; `R_0 = 25e-3 m` (domain half-width).
   - Compute Eq.4 → `f_s_th`.
   - Compute characteristic velocity `√(eEᵣLₙ/mᵢ)`.
   - Compute theory/measured ratio (53 / 43.2).
   - Compute E×B kinematic cross-check: `v_ExB = E_r / B`, `f = v_ExB/(2πR_0)`.
   - Verify He-4 mass consistency: `7291.712 * m_e → amu` (should = 4.000).
   - Back-solve R_0 that would give exactly 53.00 kHz.
   - Compute Ar-40 frequency by `1/√m_i` scaling (C4).
2. Run: `python3 work/replicate_spoke.py`.
3. Emit `report/evidence/evidence_spoke.json` with every reproduced number.

## Stage 5 — Cross-check with LLM judge

1. Write `work/judge.py` — Argo `argo:gpt-5.2` at `http://127.0.0.1:44497/v1` (free endpoint), temp 0.
2. Feed the judge: (a) paper's claims table, (b) our reimplemented values.
3. Ask judge to score agreement_pct, verdict, coverage, justification.
4. Save `report/evidence/judge_result.json`.

## Stage 6 — Write the report

1. Draft `report/REPORT.md`:
   - §1 Paper summary
   - §2 Claims table
   - §3 Method (data sources, tools, commands, parameters)
   - §4 Results-vs-paper table with match column
   - §5 LLM-judge verdict block
   - §6 Evidence files
   - §7 Conclusion + verdict line
   - Trailing `WAVE_RESULT` line.
2. Verdict decision rule: REPLICATED iff (analytic scalar within ±5%) AND (theory/measured ratio matches) AND (scaling law verified) AND (LLM judge ≥ 80%). All satisfied here.

## Stage 7 — Backfill (this stage)

Convert REPORT.md into the standard artifact bundle:
- `REPORT.tex` (LaTeX with dedicated GENUINE CRITIQUE section)
- `open_questions.json` (5 open scientific questions)
- `workflow.md` (this file)
- `artifacts_summary.md`
- `failure_analysis.md`

## Conventions used

- **Endpoints:** free only (Argo local proxy :44497). No paid API calls.
- **PDFs:** MD5-tagged for provenance.
- **Evidence:** every reproduced number lands in `report/evidence/*.json`, not just prose.
- **Honesty:** C6 (full PIC) explicitly marked not-attempted; back-solved R_0 flagged as internally-consistent-not-independent.
- **Single-writer:** `report/` is the canonical output directory; `work/` is scratch.
