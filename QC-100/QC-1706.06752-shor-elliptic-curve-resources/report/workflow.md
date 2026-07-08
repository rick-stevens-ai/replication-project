# Workflow — Replication of Roetteler et al. 2017 (arXiv:1706.06752)

**Set:** QC-100 &nbsp;|&nbsp; **Paper:** Roetteler, Naehrig, Svore, Lauter — ECDLP-Shor resource estimates
**Verdict:** REPLICATED
**Backfill date:** 2026-07-06

---

## 0. Environment / tools

- macOS on CherryRd, Python 3.14.6 for stdlib work, `venv` at `work/venv/` for Qualtran.
- Free endpoints only. No paid API calls. No simulator runs on paid HPC.
- Tool versions pinned in `report/evidence/tool_versions.txt`: `qualtran 0.7.0`, `cirq-core 1.7.0`, `sympy 1.14.0`, `numpy 2.5.0`.

## 1. Scaffold the target directory

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100
mkdir -p QC-1706.06752-shor-elliptic-curve-resources/{paper,report/evidence,work,code,data,extraction}
cd QC-1706.06752-shor-elliptic-curve-resources
```

Sub-directories:
- `paper/` — the PDF as-fetched.
- `report/` — `REPORT.md`, `REPORT.tex`, `open_questions.*`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`, `evidence/`.
- `work/` — scratch: raw pdftotext output, `venv/` for Qualtran install.
- `code/` — scripts (kept minimal, ~3 files).
- `data/` — CSV of Table 2 ground truth.
- `extraction/` — nougat / marker-style stubs for downstream OSTI-style pipelines (created during backfill).

## 2. Fetch and extract the paper

```bash
cd work
curl -sL -o paper.pdf https://arxiv.org/pdf/1706.06752
cp paper.pdf ../paper/1706.06752_roetteler_ecdlp.pdf
pdftotext paper.pdf paper.txt          # 2,239 lines
grep -n "Table\|Toffoli\|qubits" paper.txt
```

Manually transcribe Table 2 (7 rows) into `data/roetteler_2017_table2.csv`:
```
n_bits,qubits,toffoli,toffoli_depth,sim_time_s
110,1014,9.44e9,8.66e9,273
160,1466,2.97e10,2.73e10,711
192,1754,5.30e10,4.86e10,1149
224,2042,8.43e10,7.73e10,1881
256,2330,1.26e11,1.16e11,3848
384,3484,4.52e11,4.15e11,17003
521,4719,1.14e12,1.05e12,42888
```

Extract the two headline formulas by pdftotext + `grep`:
- Qubits: `9n + 2⌈log₂ n⌉ + 10` (Section 5.2)
- Toffoli: `(448·log₂ n + 4090)·n³` (abstract + Section 5.2)

## 3. Analytic reconstruction (pure Python)

Author `code/analytic_reconstruction.py` implementing:
1. Qubit closed form `9n + 2·ceil(log2(n)) + 10`.
2. Toffoli closed form `(448·log2(n) + 4090) * n**3`.
3. Toffoli "from primitives": `2n * (4·inv + 2·squ_Mont + 4·mul_Mont)` with paper's Table 1 primitive formulas.
4. Row-by-row comparison against `data/roetteler_2017_table2.csv`.

Run:
```bash
python3 code/analytic_reconstruction.py > report/evidence/analytic_reconstruction.stdout.txt
```

Persist full numeric output to `report/evidence/analytic_reconstruction.json`
(JSON array of 7 row-dicts).

## 4. Qualtran cross-check

```bash
python3 -m venv work/venv
source work/venv/bin/activate
pip install --only-binary=:all: qualtran
```

Author `code/qualtran_symbolic.py`:
- Import `qualtran.bloqs.cryptography.ecc.FindECCPrivateKey`.
- Import `QECGatesCost`, `get_cost_value`.
- Instantiate at symbolic `n = sympy.Symbol('n', integer=True, positive=True)` with concrete `mod=251` (so the QROM specializer runs), window sizes 4.
- Compute cost expression symbolically, substitute `n ∈ {110,…,521}`, sum `toffoli + and_bloq`.
- Persist to `report/evidence/qualtran_symbolic.json`.

Also try `code/qualtran_crosscheck.py` at concrete curve parameters; this fails on `ECAddR`'s QROM specialization at symbolic `n` (kept for provenance).

## 5. Interpretation and verdict

Compare closed-form vs.\ Table 2 (max 2.18%, mean 1.00%) → C2 replicated.
Reconstruct leading coefficient 224 from Table 1 primitives → C3 replicated.
Diagnose primitives-vs-fit gap (C5) as fit-captured bookkeeping ops.
Cross-check Litinski/Qualtran gives ~170× smaller (C6) → consistent with follow-on windowing claim.

Verdict: REPLICATED — analytical resource-count paper, formulas + Table 2 reproduced.

## 6. Backfill artifacts (2026-07-06)

The original run produced `REPORT.md`, `data/`, `code/`, `report/evidence/`. Backfill added:
- `report/REPORT.tex` — LaTeX version with honest Critique section.
- `report/open_questions.json` — 5-question bare JSON list.
- `report/open_questions_section.tex` — LaTeX version of same, `\input`ed by REPORT.tex.
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — inventory.
- `report/failure_analysis.md` — honest critique.
- `extraction/nougat.mmd` — stub for downstream OSTI-style processing.

## 7. Reproduce

See `REPORT.md` §6 for the exact reproduction commands. Expected outputs are
bit-identical for the pure-Python reconstruction and stable to within
floating-point rounding for Qualtran.
