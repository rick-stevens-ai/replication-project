# Artifacts summary

Files produced by this replication (target dir
`~/Dropbox/REPLICATE-PROJECT/PDE-Buzbee-Dorr-George-Golub-Poisson-irregular-1970/`):

## Top-level
- `paper.pdf` — 1,340,222 B — LA-4553-MS (SIAM J. Numer. Anal. 8(4), 1971) from OSTI 4060961.

## `extraction/`
- `marker.md` — 66 KB — pdftotext -layout extraction of paper.pdf, with header identifying this as a marker/nougat fallback (neither tool was available on the compute host).
- `nougat.mmd` — 5 KB — stub with LaTeX-format section headings, key equations, and Table 1 verbatim; includes central-corpus manifest pointer for future real Nougat parse.

## `report/`
- `REPORT.md` — full narrative report with paper summary, claims table, method, results-vs-paper tables, verdict + justification, and Open Questions Q1..Q5.
- `REPORT.tex` — LaTeX version, section-by-section, of the same content.
- `brief.md` — one-paragraph what/why.
- `attempt_log.md` — chronological build log (including the sign-bug fix).
- `artifact_harvest.md` — every artifact pulled with URL + size + checksum.
- `workflow.md` — workflow diagram + tools/versions + effort estimate.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — where things went wrong, why, and what to trust.
- `open_questions.json` — exactly 5 items, each `{q, basis, next_steps}`.

## `report/evidence/`
- `table1_rectangle_hole_evidence.json` — machine-readable results for the 4 paper-Table-1 configs.
- `mms_convergence_evidence.json` — MMS convergence rates on Region 2 for N in {16, 32, 64, 128}.
- `lshape_splitting_evidence.json` — L-shape splitting results for N in {16, 32, 64, 128}.
- `rectangle_hole_run.log`, `mms_run.log`, `lshape_run.log` — raw stdout captures.

## `work/`
- `capacitance_solver.py` — main solver (imbedding + capacitance-matrix on rectangle-with-hole).
- `mms_convergence.py` — driver for the O(h^2) convergence study.
- `lshape_splitting.py` — L-shape splitting implementation (paper §5).
- `diagnose.py` — small utility used to diagnose the initial sign-of-Laplacian bug.
- `paper.txt` — raw pdftotext output (input to `extraction/marker.md`).
- `unpaywall.json` — Unpaywall API response for the DOI (returned no OA
  locations directly, but S2 knew about the OSTI copy).
- `run.log`, `mms_run.log`, `lshape_run.log` — matching duplicates of the
  evidence logs (kept during development).
- `evidence.json`, `mms_convergence.json`, `lshape_evidence.json` —
  originals before copy to `report/evidence/`.
