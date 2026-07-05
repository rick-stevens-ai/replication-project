# QC-100 Replication Wave Brief — 2026-07-03

You are doing ONE independent replication of ONE quantum-computing paper for QC-100.

## Why QC is tractable
QC-100 papers are almost all **classically simulable on CPU** with open tools (Qiskit / Cirq / Stim / PennyLane / OpenFermion / PyMatching). No HPC/GPU gate for the small-instance reproductions. Aim to ACTUALLY RUN a real simulation reproducing a headline number, not just spot-check — per Rick's 2026-07-03 standard.

## Hard rules
- **Free endpoints only** for any LLM inference (Argo localhost:44497 key=stevens). NEVER paid APIs.
- **Real simulation only.** Install the open tool, run the actual circuit/algorithm at a small-but-faithful instance size, compare to the paper's reported number. No fabricated results.
- **LLM-judge scoring** for the final verdict, never regex.
- Write ONLY inside your assigned target dir. Preserve any existing sibling dirs.
- Don't end your turn until report/REPORT.md exists with a verdict.

## Anti-timeout strategy (follow exactly)
1. Resolve + read the paper: fetch arXiv (https://arxiv.org/abs/<id> and /pdf/<id>) into work/, pdftotext, skim (~2-3 min). Extract the headline claim(s) + the ONE most-checkable number.
2. Install the sim tool (pip --user into a venv) and RUN a small real instance reproducing that number (e.g. VQE ground-state energy for H2/LiH; QAOA MAX-CUT ratio on a small graph; Stim logical error rate at small distance; RB decay; QV pass/fail at small width). Keep instance size low so it finishes in minutes.
3. Compare reported vs your value → MATCH/MISMATCH with tolerance.
4. Save real outputs to report/evidence/ (JSON/CSV + the circuit/code).
5. Write report/REPORT.md (mirror ~/Dropbox/REPLICATE-PROJECT/BVBRC-17-Ecoli-B2-IBD-metabolic-2018/report/REPORT.md): paper summary, claims table (C1..Cn: type/testable?/tested?), numbered Method (exact commands + tool versions), Results-vs-paper table, Verdict + justification.
6. **MANDATORY — Open Questions.** End REPORT.md with a section `## Open Questions` containing **exactly 5 NEW open research questions** that arose from doing THIS replication (not generic ones copied from the paper's own "future work"). Ground each in what you actually observed/ran: gaps between the paper and your result, things the paper left unspecified, follow-on experiments the reproduction suggests, sensitivity/scaling questions, methodological ambiguities. Number them Q1..Q5, each 1-3 sentences. Also write them as a machine-readable file `report/open_questions.json` = a JSON list of 5 objects `{"q": "<question>", "basis": "<what in the replication prompted it>"}`. This feeds the cross-project open-questions corpus, so make them specific and non-trivial.
7. 3-judge Argo panel only if time remains; else self-verdict.

## MANDATORY 8-artifact completion bar (Rick 2026-07-05 — see REPLICATION_DIR_STANDARD_2026-07-05.md)
Before printing WAVE_RESULT, the target dir MUST contain all 8:
1. `paper.pdf` (original PDF)
2. `extraction/marker.md` (Marker parse; pull from central corpus if parsed, else run Marker)
3. `extraction/nougat.mmd` (Nougat parse; pull from central corpus if parsed, else run Nougat)
4. `report/REPORT.tex` (very detailed section-by-section LaTeX report: what worked / what didn't per claim; compile to REPORT.pdf when possible)
5. `report/open_questions.json` (5 heavy-duty, non-superficial open questions, each `{q,basis,next_steps}`) + `## Open Questions` in the report
6. `report/workflow.md` (comprehensive workflow + list of tools/codes with versions + estimate of work done)
7. `report/artifacts_summary.md` (inventory of all artifacts + traces)
8. `report/failure_analysis.md` (honest failure analysis / friction / residual gaps)
Evidence + code go under `report/evidence/`; downloaded data + intermediates under `work/`.

## Verdict vocab
REPLICATED (headline number reproduced within tolerance on real sim) · PARTIAL (some claims reproduced) · SPOT-CHECK (code/method verified, small demo, not full claim) · NO-GO (data/code unavailable) · CONTRADICTED · BLOCKED · FAILED.

## Final line
WAVE_RESULT set=QC-100 paper=<arxiv_id> verdict=<V> dir=<path> one_line=<summary>
