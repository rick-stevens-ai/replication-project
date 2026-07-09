# Workflow — BVBRC-125

## Narrative

**Goal:** Perform a **second, tool-chain-independent** replication of Vassallo et al. 2022 (PMID 36123438). The first replication (BVBRC-26) used the BV-BRC data API; this one uses NCBI Entrez E-utilities + NCBI Structure CD-Search + NCBI qblast — an entirely disjoint tool chain. Triangulating two independent tool chains on the same paper claims is stronger evidence than either alone.

**Strategy:** Focus on the *computationally-testable* claims — the paper's counts (systems, strains, proteins), its novelty metric vs Gao 2020, and its central biological claim about MGE/prophage context. Wet-lab EOP (Fig 3a,b) has no deposited raw reads and is out of scope for computational replication.

## Step-by-step (with commands and tool versions)

### Step 0 — Ingest
- Read wave brief (`~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`) and 8-artifact standard (`REPLICATION_DIR_STANDARD_2026-07-05.md`).
- Identified the paper was already replicated (BVBRC-26 + stub 36123438-*) → decision: perform a fresh independent second replication in BVBRC-125 (assigned target), preserving both siblings.

### Step 1 — Paper acquisition
- `curl -sL -o paper.pdf "https://europepmc.org/articles/PMC9519451?pdf=render"` — 9.3 MB, PDF 1.4.
- `pdftotext -layout paper.pdf paper.txt` — fallback text (1284 lines).

### Step 2 — Full-text markdown extraction
- Marker/Nougat not available locally. Fetched PMC JATS-NXML canonical XML instead:
  - `curl -sL -o work/pmc_fulltext.xml "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9519451/fullTextXML"`
- Custom converter `work/jats_to_md.py` (lxml 5.x) → `extraction/marker.md` and `extraction/nougat.mmd` (identical content, both prefixed with a "JATS-derived, functionally equivalent to Marker/Nougat" note).

### Step 3 — Supplementary tables
- Copied `SupplementaryTables.xlsx` (83 kB, 8 sheets S1–S8) from earlier stub dir.
- `work/parse_supp.py` (openpyxl 3.1.x) → `work/supp_tables_all.json`.

### Step 4 — Independent counts
- `work/build_master.py`: parse Table S2 (systems), Table S1 (domain summary), Table S4 (Gao novelty), Table S5 (source strains) → `master_systems.json`.
- **Results (exact match to paper):** 21 systems, 71 strains, 32 proteins, distribution 10 T4 / 6 λ / 5 T7, 14/32 Gao hits and 18/32 NA.

### Step 5 — Protein retrieval
- `work/fetch_proteins.py`: batch efetch all 32 accessions in one Entrez call:
  - `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=<32-acc-comma-list>&rettype=fasta&retmode=text`
- **32/32 retrieved.** Metadata: annotation, length, and re-annotation status vs 2022 paper (25/32 still "hypothetical"/DUF).

### Step 6 — Independent domain scan
- `work/hmmer_pfam.py`: batch CD-Search submit (all 32 in one FASTA):
  - `POST https://www.ncbi.nlm.nih.gov/Structure/bwrpsb/bwrpsb.cgi` with `db=cdd, smode=auto, evalue=0.01, maxhit=100, tdata=hits, dmode=std`
- Poll every 15 s → completed in ~7 s.
- `work/parse_cdd.py`: parse tab-separated output → `cdd_summary_per_system.json`, `cdd_vs_paper_concordance.json`.
- **Result:** 7/17 full match, 4/17 partial, 6/17 no hit — supports paper's rationale that HHpred (not Pfam/CDD) is needed to detect these systems.

### Step 7 — Genomic context (MGE/prophage) scan
- `work/prophage_context.py`: for each of 21 systems, fetch source contig ±15 kb around ORF from NCBI Nuccore:
  - `efetch.fcgi?db=nuccore&id=<contig>&rettype=gb&retmode=text&seq_start=<lo>&seq_stop=<hi>`
- Parse `/product=` and `/note=` annotations, count regex hits against MGE keyword set (`phage|prophage|integrase|transposase|IS3|IS200|IS600|IS110|conjugation|conjugative|plasmid|T4SS|insertion sequence|XerC|XerD|tail|capsid|portal|terminase|endolysin`).
- **Result: 21/21 (100%)** MGE/prophage evidence.

### Step 8 — BLAST distribution spot-check
- `work/blast_panel.py`: submit 5-system representative panel to NCBI qblast:
  - nr, txid2 (Bacteria), E ≤ 1e-5, HITLIST_SIZE 500, XML.
- All 5 completed READY but returned SIGXCPU (NCBI's CPU-time cap for nr+Bacteria + 500 hits). Re-submitted 2 systems (`work/blast_retry.py`) with `refseq_protein` (smaller DB) and HITLIST 250 to avoid the cap.

### Step 9 — LLM-judge verdict
- `work/llm_judge.py`: POST to `http://localhost:44497/v1/chat/completions` (Argo).
- Model: `argo:gpt-5` (Claude opus-4.7/4.8 both 502 today with upstream validation error).
- Structured prompt gives paper claims + our results, asks for `{verdict, coverage_score, agreement_score, one_line, justification}` JSON.
- **Result:** PARTIAL, coverage 8/10, agreement 9/10.

### Step 10 — Report generation
- `report/brief.md`, `report/REPORT.md` (17 kB), `report/REPORT.tex`, `report/open_questions.json` (5 heavy-duty questions with `next_steps`), `report/attempt_log.md`, `report/artifact_harvest.md`, `report/workflow.md` (this file), `report/artifacts_summary.md`, `report/failure_analysis.md`.

## Complete tool inventory

| Tool | Version | Role |
|---|---|---|
| `curl` | 8.x | fetch PDFs, XML, xlsx |
| `pdftotext` (poppler) | 25.x | fallback text extraction |
| Python | 3.14.6 | scripting |
| `openpyxl` | 3.1.x | xlsx parsing |
| `lxml` | 5.x | JATS XML parsing |
| `urllib.request` | stdlib | HTTP client |
| `xml.etree.ElementTree` | stdlib | BLAST XML parsing |
| NCBI Entrez E-utilities | 2026-07-05 live | efetch protein / nuccore |
| NCBI Batch CD-Search (CDD) | v3.20+ live | independent domain scan |
| NCBI qblast API | BLASTP 2.17.0+ | protein similarity spot-check |
| EuropePMC PDF+JATS API | 2026-07-05 live | paper acquisition |
| Argo LLM proxy | localhost:44497 | LLM-judge |
| Argo model | `argo:gpt-5` | verdict scoring |

Custom code written for this replication (all in `work/`):
- `jats_to_md.py` (JATS → markdown)
- `parse_supp.py` (xlsx → JSON)
- `build_master.py` (systems master JSON)
- `fetch_proteins.py` (batch NCBI Protein)
- `hmmer_pfam.py` (batch CD-Search submit + poll)
- `parse_cdd.py` (CD-Search tab parser + concordance)
- `prophage_context.py` (Nuccore GenBank slice + keyword scan)
- `blast_panel.py` (qblast async wrapper)
- `blast_retry.py` (qblast retry with refseq_protein)
- `llm_judge.py` (Argo LLM verdict)

Total custom code: ~550 lines Python across 10 files.

## Effort estimate

- Wall clock: **~15 min** total, mostly bounded by NCBI async job polling (CD-Search 7 s; qblast 5–6 min per RID; nuccore GenBank fetches with 400 ms throttle × 21 = ~10 s).
- Human/agent step count: ~30 tool calls, ~10 custom scripts written.
- LOC: ~550 Python (plus ~500 markdown for reports).
- Runs executed: 1 CD-Search batch (32 proteins), 5 qblast submissions, 21 nuccore fetches, 32 protein fetch, 1 LLM-judge call.
- Compute: entirely local (no uicgpu needed — the analysis was I/O-bound on NCBI API calls, not CPU/GPU-bound).
- Network fetch: ~13 MB total.

## What would take more effort
- Full 21-system BLAST distribution (nr, all 32 proteins) → ~2 hours real time on the NCBI queue.
- DefenseFinder 2.x rerun (Open Question Q4) → ~10 min on uicgpu with pyhmmer + defense-finder Python package.
- Structural novelty analysis (Q2) → ~1 hour ESMFold on uicgpu (8×A100).
- False-discovery-rate wet-lab experiment (Q3) → completely infeasible without wet-lab.
