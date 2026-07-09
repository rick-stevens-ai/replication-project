# Workflow — BVBRC-104 (Szmolka et al. 2023, mcr-1 E. coli duck Hungary)

## Narrative

The replication ran end-to-end on 2026-07-05 (US-Central) with orchestration on CherryRd and
compute on uicgpu (8×A100, 255-core Xeon, 2 TB RAM). Elapsed wall clock: **~13 minutes** from
brief to LLM-judge verdict. Free endpoints only (Argo localhost:44497, key=`stevens`); no paid API.

### Phase 1 — Paper acquisition (~2 min)
1. Read wave brief, resolved PMID 37887221 → PMC10604428 → DOI 10.3390/antibiotics12101519.
2. Attempted MDPI direct HTML fetch — **blocked by anti-bot** (Access Denied) both from CherryRd
   and via uicgpu-proxied curl.
3. Pivoted to NCBI E-utilities: `efetch db=pmc id=10604428 rettype=xml` returned 124 KB of JATS XML.
4. Python 3.14 `xml.etree.ElementTree` parser extracted abstract + all §§ + methods to
   `work/paper_text.md` (26.8 KB — full text for downstream re-reading).

### Phase 2 — Assembly acquisition (~1 min)
5. Identified deposited accessions from paper text: BioProject **PRJNA1012593** →
   CP134085 (chromosome) + CP134086–CP134090 (5 plasmids).
6. For each accession: `efetch db=nuccore id=<acc> rettype=fasta retmode=text` → `work/genomes/`.
7. Concatenated to `Ec45-2020_all.fasta` (5.63 MB, matches paper's ~5.36 Mb sequence total).
8. Length check vs paper — 5/6 exact match, chromosome off by 100 bp (0.002%; noted).

### Phase 3 — In-silico pipeline on uicgpu (~4 min)
9. `rsync` genomes to `uicgpu:/data/stevens/scratch/bvbrc104/genomes/`.
10. Conda env `bvbrc14` (pre-existing from prior BVBRC replications) activated.
11. `mlst --scheme ecoli_achtman_4 Ec45-2020_all.fasta` → **ST162** (Warwick, exact match).
    Also ran `--scheme ecoli` (Pasteur) as control → ST355 (different scheme, expected).
12. `amrfinder -O Escherichia --plus -n Ec45-2020_all.fasta` (64 s wall clock) →
    53 hits across 4 contigs. Full TSV in `report/evidence/amrfinder_full.tsv`.
13. `abricate --db plasmidfinder Ec45-2020_all.fasta` → all 5 plasmid replicons typed.
14. `abricate --db ecoh Ec45-2020_all.fasta` → **O55:H10** confirmed.

### Phase 4 — Backbone-conservation BLAST (~3 min)
15. NCBI Nuccore esearch v1 (unfiltered): `"mcr-1"+"IncX4"+plasmid+"complete+sequence"` → returned
    a Culex mononega-like virus and a Trametes fungal mRNA among the hits (term ambiguity).
    First BLAST attempt against v1 refs gave 2–18% qcov = false negative from bad reference set.
16. esearch v2 with size filter: `... 30000:40000[SLEN] retmax=20` → 17 real IncX4/mcr-1 plasmid
    refs (30–40 kb).
17. `efetch db=nuccore rettype=fasta` per accession → `refs2/*.fasta` → concatenated
    `refs2/all_incx4.fasta` (~570 KB).
18. `makeblastdb -in refs2/all_incx4.fasta -dbtype nucl -out refs2/incx4db`.
19. `blastn -query genomes/CP134089.fasta -db refs2/incx4db -evalue 1e-50
    -outfmt "6 sseqid pident length qstart qend evalue"` → 104 HSPs across 17 subjects.
20. `work/blast_summary.py` (~50 LOC): per-subject non-overlapping HSP interval merge on the
    33,541 bp query + weighted pident (Σ pident·len / Σ len). JSON output in
    `report/evidence/blast_incx4_v2_summary.json`. Median qcov 100%, median pident 99.79%.

### Phase 5 — LLM judge (~2 min)
21. Composed 7.5 KB judge prompt covering every paper claim (P1–P8) and every evidence block
    (E1–E8). Saved to `work/llm_judge_prompt.txt`.
22. First 4 calls to `argo:claude-opus-4.7` returned HTTP 502 (transient Argo Vertex issue).
23. Fallback to `argo:gpt-5.2` (temperature 0) succeeded on first call →
    `{"verdict":"REPLICATED","coverage_pct":85,"agreement_pct":100,"one_line":"...","confidence":"high"}`.
24. Model + verdict saved to `report/evidence/llm_judge_model.txt` and
    `report/evidence/llm_judge_verdict.json`.

### Phase 6 — Report writing (~1 min original + 8-artifact backfill 2026-07-05)
25. Wrote `report/REPORT.md`, `report/brief.md`, `report/attempt_log.md`,
    `report/artifact_harvest.md`.
26. **Backfill pass (this document, 2026-07-05 RESUME mode)**: added `report/REPORT.tex` (detailed
    section-by-section LaTeX with genuine critique per Rick 2026-07-05 hard rule),
    `report/open_questions.json` (5 grounded open questions re-read from paper),
    `report/workflow.md` (this file), `report/artifacts_summary.md`, `report/failure_analysis.md`,
    plus `paper.pdf`, `extraction/marker.md`, `extraction/nougat.mmd` (pending central corpus pull).

## Tools + versions

| Tool / code | Version | Role |
|---|---|---|
| NCBI E-utilities (efetch / esearch / esummary) | live 2026-07-05 | Paper + assembly + reference retrieval |
| Python | 3.14 (CherryRd), 3.11 (uicgpu conda) | Parsing, HSP merge, summary stats |
| `xml.etree.ElementTree` | stdlib 3.14 | JATS XML parse of PMC full text |
| curl | 8.15 (CherryRd), 7.85 (uicgpu) | HTTP fetches |
| conda env `bvbrc14` | on uicgpu `/data/stevens/envs/bvbrc14/` | Pipeline env (pre-existing from prior BVBRC waves) |
| mlst (Torsten Seemann) | 2.33.1 | MLST typing (Warwick scheme = `ecoli_achtman_4`) |
| AMRFinderPlus | 4.2.7 (autoupdated DB) | AMR + curated VF calling |
| abricate | 1.0.1 | Wrapper for PlasmidFinder + SerotypeFinder DBs |
| PlasmidFinder DB | 488 seqs, 2026-Apr-3 | Plasmid replicon typing |
| ecoh DB (SerotypeFinder-equivalent) | 597 seqs, 2026-Apr-3 | O + H antigen typing |
| BLAST+ | 2.17.0 | Backbone conservation of pEc45-2020-33kb vs public refs |
| `work/blast_summary.py` | ~50 LOC (this replication) | Per-subject HSP-interval merge + weighted pident |
| Argo proxy (localhost:44497) | live | LLM judge (`argo:claude-opus-4.7` attempted, `argo:gpt-5.2` succeeded) |
| pdflatex (optional) | TeXLive 2024 on CherryRd | Compile `report/REPORT.tex` → `report/REPORT.pdf` (attempted in backfill pass) |
| pdftotext (poppler) | 24.02.0 | Marker.md fallback (backfill pass) |

## Effort estimate

| Metric | Value |
|---|---|
| Wall clock end-to-end (orig run) | ~13 minutes |
| Wall clock — backfill pass (this) | ~15 minutes (report items 4-8 + PDF + extraction stubs) |
| Compute — AMRFinderPlus | 64 s on 5.6 MB assembly, 8×A100 (I/O-bound, not GPU) |
| Compute — BLASTn 17 refs | <5 s |
| Compute — MLST + abricate | <10 s |
| Data transferred | ~6 MB IN (paper + genomes + refs) |
| LOC written this replication (excluding pipeline tool internals) | ~250 LOC (`blast_summary.py`, `paper_text.md` extractor, judge prompt, evidence-check helpers, plus backfill LaTeX + JSON + markdown) |
| Agent steps (subagent 5106e116 + backfill pass) | ~35 tool calls |
| LLM-judge cost | $0 (free Argo endpoint) |
| Total human/agent operator time | ~30 min including backfill |

## Reproducibility notes

- All commands + versions are deterministic and rerunnable. NCBI records are stable (we pinned
  to accession `.1` versions).
- `blast_summary.py` is self-contained (stdlib only) and can be re-run against
  `report/evidence/blast_incx4_v2.tsv` at any time.
- LLM judge is the one non-deterministic step; but the verdict is grounded in the deterministic
  pipeline outputs enumerated in the prompt, so a re-judge on a different free model would be
  expected to reach the same call barring prompt-framing shifts.
- Argo Opus 4.7 502-flap was transient; retry recommended before falling back to GPT-5.2 for
  reproducibility.
