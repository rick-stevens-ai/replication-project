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

## CONTEXT DIET (mandatory — read this FIRST before any exploration)
DO NOT read raw sequence/data files into context. Specifically avoid:
- Anything in `work/` that is `.fna`, `.fa`, `.fasta`, `.gb`, `.gbk`, `.gff`, `.vcf`, `.bam`, `.sam`, `.bed`, or `.tsv` >50KB. These are megabytes of raw genome data that will burn 300-500K input tokens for zero writing value.
- Any file `>200KB` in general unless it's the extraction/marker.md or the paper.pdf.
- `.DS_Store` and other Mac metadata.

DO read (and ONLY these) for context grounding:
- `report/REPORT.md` (the existing summary) — this is your primary source
- `extraction/marker.md` if present (paper text)
- `extraction/nougat.mmd` if present + non-stub
- Small summary files in `report/` like `attempt_log.md`, `artifact_harvest.md`
- A `head -50` of `work/analysis_output.txt` if you need to sanity-check numbers

Budget: total input context should stay under 100K tokens. If you exceed 200K input tokens on read-in, you have already failed the run. Prior failures at 344K and 466K input tokens were caused by ingesting raw .gb/.fna files from `work/`.

## RESUME MODE + REPORT-FIRST (mandatory ordering to survive timeouts)
Subagent runs get cut around 4-5 minutes with high probability. The failure pattern: agent spends first ~4 min chasing PDF/extraction, then hits a ceiling before writing items 4-8 (the highest-value deliverables). To survive this, follow this ORDER STRICTLY:

1. First, `ls` the target dir. Note which of the 8 artifacts already exist. SKIP those.
2. **WRITE items 4-8 (report/REPORT.tex, report/open_questions.json, report/workflow.md, report/artifacts_summary.md, report/failure_analysis.md) FIRST**, before any PDF-fetch or extraction attempt. Read the existing REPORT.md + any evidence in the dir + any already-present extraction/marker.md to ground the write. If no marker.md exists, use the existing REPORT.md as the paper summary source — the paper's identity is in there.
3. After all 5 report items are on disk, THEN attempt paper.pdf fetch (90s cap). If it fails, write `paper.pdf.MISSING.md` marker noting source + why fetch failed and move on. Do not retry.
4. THEN attempt extraction/marker.md + extraction/nougat.mmd. Fallback to pdftotext or a labeled stub if tools/PDF unavailable.

This ordering means even a 4-minute timeout leaves all 5 valuable report items on disk.

### WRITE ONE FILE AT A TIME + CHECKPOINT (proven 2026-07-05)
Do NOT batch all 5 writes into one final "write everything in parallel" tool block — if the run
terminates before that block executes, ALL work is lost (this failure mode killed 3 consecutive
backfill attempts on BVBRC-103). Instead: call the write tool SEPARATELY for each of the 5 files,
most-valuable-first (REPORT.tex, then open_questions.json, then the 3 md files). After each write,
print `wrote <filename>` as a checkpoint. This pattern succeeded on BVBRC-37 (4m24s) and BVBRC-39
(4m19s) at ~4 min each after the same dirs' "parallel" attempts had failed.

### When REPORT.md is already rich, this is a PURE-WRITE task
If `report/REPORT.md` already contains the full narrative (paper summary, claims, methods, results,
verdict), you do NOT need to fetch the PDF, re-run analysis, or read `work/` at all. Read ONLY
`report/REPORT.md` + `extraction/marker.md` (if tiny), then write the 5 files grounded entirely in
REPORT.md. Do not fabricate numbers not in REPORT.md; where REPORT.md is silent, state qualitatively.

You still must RE-READ the paper (using whatever is available: existing REPORT.md, marker.md, or the abstract from a metadata lookup) before writing the 5 open questions. The questions must be truly OPEN, important, non-superficial problems for future new work — each with concrete next_steps.

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
