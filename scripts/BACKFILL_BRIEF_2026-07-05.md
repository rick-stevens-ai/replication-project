# Replication 8-Artifact BACKFILL Brief — 2026-07-05 (Rick)

You are backfilling ONE existing paper-replication directory so it meets the 8-artifact standard
(`REPLICATION_DIR_STANDARD_2026-07-05.md`). You are given the target dir path + the paper's arXiv
id / DOI / title (from the wave record). DO NOT re-run the original simulation unless there is no
existing report at all. Work from what was actually done + re-reading the paper.

## Rick's explicit requirements (2026-07-05) — these are the point of the exercise
- **Review what was actually done and include a genuine CRITIQUE** in both the report and the failure
  analysis. Do not rubber-stamp. Call out weak evidence, shortcuts, unverified claims, tolerance
  hand-waving, missing controls, and anything the original run glossed over.
- **RE-READ THE PAPER when writing the open questions.** The 5 open questions will be used later to
  open new research work, so they must be TRULY OPEN, important, non-superficial problems — grounded
  in (a) what the paper leaves unresolved and (b) what THIS replication surfaced. Make a real effort
  to identify problems that are genuinely still open. Each question gets concrete next steps.

## Free endpoints only (Argo localhost:44497 key=stevens). Never paid APIs.

## Steps
1. **Read the target dir**: existing REPORT.md, evidence/, code, logs, verdict. Understand what was
   claimed, what was actually run, and how strong the evidence is.
2. **Ensure item 1 (PDF)**: if `paper.pdf` missing, fetch from arXiv (https://arxiv.org/pdf/<id>) or
   DOI. Symlink/copy to `<dir>/paper.pdf`.
3. **Ensure items 2 & 3 (Marker .md / Nougat .mmd)**: FIRST try to pull from the central Eagle
   corpus. The parse manifests live on Polaris/Eagle:
   - SCOUT: `/eagle/projects/AuroraGPT/stevens/scout_corpus/{md,mmd}/<sha256>.{md,mmd}`
   - OSTI: `/eagle/projects/AuroraGPT/stevens/osti_marker/...`
   Resolve by sha256 (given in QC200 TODO) or by title match. Copy resolved files into
   `<dir>/extraction/marker.md` and `<dir>/extraction/nougat.mmd`. If not in the corpus and the PDF
   is present, you MAY run `pdftotext` as a marker.md fallback and note it; Nougat requires GPU so if
   unavailable, write `extraction/nougat.mmd` with a header noting "pending central Nougat parse" +
   the sha256 so a later corpus sweep can fill it. Do NOT block the whole backfill on Nougat.
4. **RE-READ the paper** (marker.md / nougat.mmd / pdftotext). This grounds items 4-8.
5. **Item 4 — `report/REPORT.tex`**: very detailed, section-by-section LaTeX. Sections: Paper summary;
   Claims table (C1..Cn, type/testable?/tested?); Method (numbered, tools+versions+commands);
   Results-vs-paper (tables); **per-claim what-worked / what-didn't**; **Critique of the replication**
   (honest assessment of evidence strength, shortcuts, gaps); Verdict + justification; Open Questions.
   Compile to `report/REPORT.pdf` with pdflatex if available (don't block if latex missing — leave .tex).
6. **Item 5 — `report/open_questions.json`** = list of exactly 5 objects
   `{"q":..., "basis":..., "next_steps":...}`. Heavy-duty, important, TRULY OPEN (see requirements
   above). Also put a matching `## Open Questions` (Q1..Q5) section in REPORT.tex.
7. **Item 6 — `report/workflow.md`**: comprehensive workflow narrative; enumerated tools+codes+versions
   used; estimate of work done (compute time, wall-clock, runs, LOC, agent steps).
8. **Item 7 — `report/artifacts_summary.md`**: inventory of every artifact + trace (files, URLs,
   accessions, sizes/checksums where easy).
9. **Item 8 — `report/failure_analysis.md`**: honest failure analysis — what failed, root cause,
   workarounds, residual gaps, what's needed to close them, plus the critique of evidence strength.
10. **Append** the 5 questions to the corpus: write `<dir>/report/open_questions.json` (the rollup
    script harvests these later; don't edit the master file yourself).

## Final line
BACKFILL_RESULT dir=<path> paper=<id> items_added=<list> nougat=<pulled|pending|na> verdict_kept=<V> one_line=<summary>
