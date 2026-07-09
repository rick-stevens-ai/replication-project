# Workflow — BVBRC-84 replication

## 0. Slot + brief reconciliation
- Wave brief labeled BVBRC-84 as **Unicycler / SPAdes** (short-read / hybrid assembler).
- Paper actually used **HGAP v.3** on PacBio RSII long reads.
- Decision: keep the paper's assembler as canonical (HGAP v.3), record the brief mismatch, and do **not** force a Unicycler/SPAdes re-run on long-read-only data.

## 1. Paper acquisition
1. `esummary db=pubmed id=37970500` → confirm title, authors, journal, year.
2. `efetch db=pubmed id=37970500 rettype=abstract retmode=text` → abstract.
3. `efetch db=pmc id=PMC10640944 rettype=xml` → full text XML → `work/paper.xml`.
4. Extract deposited accessions from paper text: BioProject **PRJNA766157**, BioSample **SAMN21619988**, GenBank **CP084221.1**, RefSeq **NZ_CP084221.1**, Assembly **GCF_022810665.1**.

## 2. Sequence + metadata pull (pass 1: E-utilities)
1. `efetch db=nuccore id=CP084221.1 rettype=fasta` → `work/CP084221.fasta` (2.23 MB).
2. `efetch db=nuccore id=CP084221.1 rettype=gb` → `work/CP084221.gb` (5.12 MB, includes PGAP embedded annotation + LOCUS topology).
3. `efetch db=nuccore id=NZ_CP084221.1 rettype=gb` → `work/NZ_CP084221.gb` (RefSeq CON).
4. NCBI Datasets v2 annotation_report → `work/annot_report.json` (RefSeq 2026 counts).
5. `esearch db=sra term=SAMN21619988` → **count=0** → raw reads absent, C12 blocked.

## 3. Paper-source annotation pull (BV-BRC / PATRIC)
1. `/genome/?eq(strain,7409N31)&select(...)` → `work/bvbrc_genome.json` → genome_id `33959.595`, length 2198442, GC 35.00943, CDS 2235, tRNA 112, rRNA 24, contigs 1, platform PacBio RSII, method "HGAP v.3".
2. `/genome_feature/?and(eq(genome_id,33959.595),eq(annotation,PATRIC))&facet(feature_type)` → CDS=2235, tRNA=112, rRNA=24, misc_RNA=3.
3. `/subsystem/?and(eq(genome_id,33959.595),eq(class,Carbohydrates))&facet(subclass)` → 30 entries: di/oligosaccharides=12, C-1 compounds=9, amino sugars=7, monosaccharides=2.

## 4. Direct compute from FASTA
- Length: `len(seq)` = **2,198,442 bp** — matches paper exactly.
- GC: `(G+C)/total` = **35.0094%** → 35.01 — matches paper exactly.
- Base composition: A=718528, T=710252, G=387900, C=381762, N=0.

## 5. LLM-judge
1. Payload → `work/BVBRC-84-judge.json` (Argo endpoint).
2. Try `argo:claude-opus-4.7` → upstream 502; try `argo:claude-opus-4.8` → upstream 502 (Argo/Anthropic response-shape bug on this specific payload).
3. Fallback `argo:gpt-5.2` → structured JSON verdict → `report/evidence/llm_judge.json`.
4. Judge output: 9 EXACT, 2 WITHIN-DRIFT (C3, C11), 1 GATED (C12); overall **PARTIAL**. Human reviewer agrees.

## 6. Independent reproduction pass (2026-07-03)
1. Fresh download via **NCBI Datasets CLI v18.25.1**: `datasets download genome accession GCF_022810665.1`.
2. Recompute length, GC, base composition from scratch (`indep_reproduce.py`).
3. Ab initio CDS calls: **prodigal V2.60** single mode → 2,147 CDS.
4. Ab initio rRNA calls: **barrnap 0.9 --kingdom bac** → 36 rRNA (12 × 5S + 12 × 16S + 12 × 23S).
5. Safety / probiotic screening: **abricate 1.4.0** across CARD, NCBI AMRFinder, ResFinder, VFDB, PlasmidFinder — 0 hits in all 5.
6. Re-query BV-BRC PATRIC + RefSeq faceting live → identical counts as pass 1.

## 7. Verdict decision
- **PARTIAL**, upheld.
- All deposited product-level claims exact or within-drift.
- Process claim (HGAP reassembly, C12) blocked by absent SRA raw reads.
- Qualitative claim (C11) inventory-supported, not functionally validated.
- Additional independent findings (not in paper): PATRIC undercounts 23S rRNA (paper's 24 is faithful to PATRIC but biologically incomplete — barrnap + RefSeq PGAP both find 36); genome is AMR/VF/plasmid-free.

## 8. Write-up + artifact packaging
- `report/REPORT.md` — long-form Markdown report (source of truth for this backfill).
- `report/REPORT.tex` — LaTeX version + GENUINE CRITIQUE section.
- `report/brief.md`, `report/attempt_log.md`, `report/artifact_harvest.md` — provenance trio.
- `report/evidence/llm_judge.json` — Argo verdict.
- `report/evidence/independent_reproduction/` — pass-2 tree (comparison.md, indep_summary.json, tool_versions.txt, code, downloads).
