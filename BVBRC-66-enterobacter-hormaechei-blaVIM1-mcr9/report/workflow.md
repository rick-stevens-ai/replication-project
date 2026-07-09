# Workflow — BVBRC-66 (Sadek 2020, *E. hormaechei* blaVIM-1 + mcr-9)

**Session:** single cron-spawned Ollie subagent (session bb00cf8a), 2026-07-02, on CherryRd (macOS 25.3).
**Compute:** local only; no cluster jobs, no paid endpoints, no external LLM other than free Argo proxy for the final judge pass.
**Runtime:** minutes (isolate is ~5 Mb).

---

## Stage 0 — Paper resolution

1. Fetch paper metadata from DOI `10.3390/pathogens9090687` → PMID 32842587, PMC PMC7558541, CC BY 4.0 open access.
2. Read the abstract + methods sections to extract the testable claim list (see `REPORT.md §2`).
3. Register 7 claims (C1–C7) with types (metadata / genomic / phenotypic) and scoring rules.

## Stage 1 — Isolate discovery

1. `esearch -db biosample -query "Sadek Enterobacter hormaechei"` → single hit **SAMN14534668** (strain EGYMCRVIM, collected 2017-07-15 at Qena, Egypt, from beef burger).
2. `elink` biosample → bioproject → assembly → nuccore → 5 complete replicons **CP053190–CP053194** (RefSeq assembly `GCF_013265685.1`).
3. Inspect GenBank headers for assembly provenance: CP053191.1 declares `hybrid assembler Unicycler v. 0.4.7`, `165.0x coverage`, `Oxford Nanopore` — matches paper's Illumina + Nanopore hybrid claim.

## Stage 2 — Genome download & BLAST DB build

1. `efetch -db nuccore -id CP053190.1,CP053191.1,CP053192.1,CP053193.1,CP053194.1 -format fasta` → 5 FASTA files, 5,188,211 bp total.
2. Confirm replicon sizes match paper (270,915 bp for pMS-37a ≈ paper's "270.9 kb").
3. `makeblastdb -dbtype nucl` for (a) each replicon separately and (b) the combined genome.

## Stage 3 — MLST (PubMLST *E. cloacae* complex, 7 loci)

1. Pull full allele set from `rest.pubmlst.org/db/pubmlst_ecloacae_seqdef/schemes/1`:
   - dnaA (772 alleles), fusA (560), gyrB (809), leuS (967), pyrG (734), rplB (388), rpoB (521); total 4,751 alleles.
2. Pull the 3,292-row ST profile table.
3. `blastn` at **strict 100% id / 100% qcov** against the chromosome (CP053190.1) — the correct MLST call rule (any tie-breaking is a bug).
4. Lookup called profile in the ST table.
5. **Called: dnaA=67, fusA=20, gyrB=19, leuS=45, pyrG=45, rplB=4, rpoB=32 → ST279** (matches paper exactly).

## Stage 4 — AMR gene detection (ResFinder)

1. Download HEAD of ResFinder from Bitbucket (`all.fsa`).
2. `blastn` against the combined-genome DB at **90% id / 60% qcov** (tightened from ResFinder default 80/60 for cleaner best-hit calls).
3. Region-cluster the raw 151 hits by genomic coordinate; keep best-hit-per-locus (max pident, then max qcov). Reduces to 10 loci.
4. Assign locus→replicon by contig id. See `REPORT.md §4.1` for the 8 pMS-37a AMR genes (all confirmed).

## Stage 5 — Plasmid Inc typing (PlasmidFinder)

1. Download HEAD of PlasmidFinder (`enterobacteriales.fsa`).
2. `blastn` at 90/60 against each of the 4 plasmids individually.
3. Assign best Inc-group hit. pMS-37a → **IncHI2 + IncHI2A at 100% id, 100% qcov** (matches paper's "IncHI2/pMLST1").

## Stage 6 — *mcr-9* flanking IS elements

1. Fetch IS canonicals: **V00609.1** (IS1, 768 bp, *E. coli*) and **MK479294.1** (IS903 tnpA region, 1,209 bp).
2. `blastn` at 80/30 against pMS-37a (CP053191.1).
3. Filter hits to within ±20 kb of the *mcr-9* CDS (positions 134,319–135,941, minus strand).
4. **Result:** IS903 at 87.6% id, 133 bp upstream (5'); IS1 at 99.87% id, 4 bp downstream (3'). Both flanking hits match the paper's model.

## Stage 7 — *qseB / qseC* regulator search

1. Fetch **NP_417497.1** (E. coli K-12 QseB, ~219 aa) and **NP_417498.1** (E. coli K-12 QseC, ~449 aa) as protein FASTA.
2. `tblastn` at e ≤ 1e-5 against (a) pMS-37a only and (b) whole genome, to separate plasmid-borne from chromosomal.
3. **Result:**
   - pMS-37a: no *qseB* hit; only one weak *qseC* paralog (27% id, e=1e-16) — effectively **absent**, as paper claims.
   - Chromosome (CP053190.1): bona-fide *qseB* (80.7% id, 218 aa) and *qseC* (69.5% id, 449 aa) near position 3.93 Mb — expected, and provides the trans-regulation open question.

## Stage 8 — LLM judge (final verdict)

1. Compile the full claim-vs-evidence table into `report/evidence/summary.json`.
2. POST to Argo proxy `http://127.0.0.1:44497/v1/chat/completions`, `Bearer stevens` (free per standing rule).
3. Attempt Claude Opus 4.8 (3× 502), then Opus 4.7 (3× 502), then fall back to **Claude Sonnet 4.6** — succeeds first try.
4. Prompt asks for 0–3 per-claim score, an overall verdict from a fixed vocabulary {REPLICATED, PARTIALLY_REPLICATED, NOT_REPLICATED, NOT_ATTEMPTED}, and a one-line summary.
5. Store JSON at `report/evidence/llm_judge.json`.

## Stage 9 — Reporting

1. Write `report/REPORT.md` (markdown, human-readable, full claim table + method + verdict).
2. Backfill on request:
   - `report/REPORT.tex` — detailed LaTeX version with dedicated GENUINE CRITIQUE section.
   - `report/open_questions.json` — 5 truly open biological/mechanistic questions the paper did not answer and this replication cannot answer.
   - `report/workflow.md` — this document.
   - `report/artifacts_summary.md` — inventory of downloaded databases, references, deposited assemblies, and derived files.
   - `report/failure_analysis.md` — enumeration of where this replication is weak, what failed, and what would strengthen it.

---

## Reproducibility notes

- All command paths, database HEAD versions, and BLAST thresholds are documented above; a rerun should be byte-deterministic against the deposited replicons (CP053190–CP053194.1) and reproducible against the same PubMLST/ResFinder/PlasmidFinder HEADs (with the standard caveat that these DBs update over time — snapshot the DB with the run).
- The LLM-judge pass is **not** deterministic (LLM sampling); the score table underlying it is. The judge output is stored as an ancillary, not an arbiter.
- No wet-lab work; no cluster jobs; no paid API calls.
