# Artifacts Summary — quant-ph/9903071 replication

Paper: **Mosca & Ekert, "The Hidden Subgroup Problem and Eigenvalue Estimation on a Quantum Computer"** (1998), arXiv:quant-ph/9903071.

## Inventory (with SHA-256 prefix and size in bytes)

| SHA-256 (16) | Bytes | Path | Purpose |
|---|---|---|---|
| ba9fe1f7a7a31a01 | 46,365 | `extraction/marker.md` | Marker-slot text extraction (pdftotext fallback; Marker not on host) |
| 3fff9c019269ff0f | 36,630 | `extraction/nougat.mmd` | Nougat-slot extraction (pdftotext fallback; Nougat not on host) |
| 2e211c8099ed8898 | 201,723 | `paper.pdf` | Original arXiv PDF (v1, 20 Mar 1999, 16 pp.) |
| a5618038a2b85111 | 247,441 | `report/REPORT.pdf` | Compiled LaTeX report (5 pp.) |
| dfc85253ea91ba23 | 13,259 | `report/REPORT.tex` | LaTeX replication report (source) |
| 1fa9e4afb49e2243 | 16,813 | `report/evidence/results.json` | Full JSON output of the reproducer with 9 pass/fail checks |
| aba9c8dbe3753e34 | 4,561 | `report/open_questions.json` | Five heavy-duty open questions with next_steps |
| 6b8ee5cbb837729c | 3,645 | `report/workflow.md` | Workflow + tool versions + effort estimate |
| 3870e19f07ed0d65 | 46,005 | `work/paper.txt` | `pdftotext -layout` dump for skimming |
| b27acfb3faf382e5 | 19,188 | `work/qpe_and_hsp.py` | Self-contained Qiskit reproducer (Exp. 1–3) |

## URLs and provenance

- Source PDF: <https://arxiv.org/pdf/quant-ph/9903071> — fetched 2026-07-05 via `curl` from CherryRd.
- Qiskit venv reused from sibling: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0301141-shor-discrete-log-elliptic-curves-proos-zalka/venv`.
- No datasets required (algorithmic reproduction).

## Traces / logs

- Run trace: `report/evidence/results.json` contains for each of 3 experiments
  the full distributions, top-5/top-N outcomes, exact errors, and per-check
  pass/fail with detail strings.
- LaTeX compile log (auto-generated): `report/REPORT.log` (kept if useful; not
  required by the standard).
- The reproducer prints one PASS/FAIL line per check to stdout; captured pass rate
  is **9/9**.

## Reproduction summary

- Command (single line):
  `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0301141-shor-discrete-log-elliptic-curves-proos-zalka/venv/bin/python work/qpe_and_hsp.py`
- Wall-clock: ~5 s statevector.
- Outputs written to `report/evidence/results.json`.

## Verdict artifact

- Final verdict: **REPLICATED** (see `report/REPORT.tex` §7).
- Machine-readable pass rate: 9/9 checks in `results.json` field `verdict_score`.
