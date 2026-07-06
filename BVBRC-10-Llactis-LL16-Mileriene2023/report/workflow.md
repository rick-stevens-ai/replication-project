# Workflow: Milerienė et al. (2023) — *L. lactis* LL16 Replication

Three sequential passes, each independently reproducible, culminating in
an independent-reproduction validation on 2026-07-03.

## Timeline

| Pass | Date | Executor | Cost | Key outputs |
|---|---|---|---|---|
| Pass-1 | 2026-05-10 | OpenClaw pipeline | $0 | `REPORT.pass1.md`, initial claim table (34 claims, 21 VERIFIED / 7 PARTIAL / 6 NOT_TESTED / 0 CONTRADICTED) |
| Re-pass | 2026-06-23 | OpenClaw pipeline (Argo Opus 4.7, free) | $0 | `REPORT.md`, `annotation_mining.json`, skani + FastANI, MinCED default + loose |
| Independent reproduction | 2026-07-03 | OpenClaw subagent, no reuse of prior outputs | $0 | `report/evidence/independent_reproduction/` (fresh downloads, fresh code, 29/29 headline metrics reproduced) |

## Pipeline stages (canonical order)

### Stage 1 — Genome acquisition
```
datasets download genome accession GCF_029912225.1
efetch -db nucleotide -id AE005176.1 -format fasta > IL1403.fna
```

- LL16 assembly: `GCF_029912225.1` (RefSeq) / `GCA_029912225.1` (GenBank) — byte-identical, 372 contigs, 2,473,617 bp.
- IL1403 reference (for ANI): `AE005176.1` (GenBank).

### Stage 2 — Genome statistics
- **Driver:** `code/repass/mine_annotations.py` (re-pass) or `report/evidence/independent_reproduction/code/genome_stats.py` (independent).
- Reads FASTA with BioPython; computes contig count, total length, GC content, N50.
- Independent recompute EXACT-matched: 372 contigs, 2,473,617 bp, 35.55% GC.

### Stage 3 — PGAP annotation mining
- Regex over the PGAP GFF3 product field, sweeping every functional category claimed in the paper.
- **Categories:** adhesion (eno, fibronectin-binding, EPS, TPI, sortase, ATP synthase, EF-Tu, LPXTG); acid/bile tolerance (ATP synthase, LDH, GlcN-6-P deaminase, CTP synthase, CFA synthase, BSH); stereospecific L-LDH vs. D-LDH; chaperones (GroES/GroEL, DnaK/J, GrpE, cold-shock); vitamins B1/B2/B6/B7/B9; tryptophan biosynthesis; GAD (gadB, gadC); IS transposases by family; lactose operon (lacA-D, lacG, β-gal, PTS); enzymes (α-amylase, lipase, protease, xylanase, HtrA); plasmid RepB.
- Output: `results/repass/annotation_mining.json`.

### Stage 4 — Average Nucleotide Identity
```
skani dist LL16.fna IL1403.fna > skani_LL16_vs_IL1403.tsv
fastANI -q LL16.fna -r IL1403.fna -o fastani_LL16_vs_IL1403.tsv
```

- skani 0.3.2 → 98.70% ANI (align_fraction_ref 0.80, query 0.77).
- FastANI 1.33 → 98.24% ANI (533/643 fragments mapped).
- Both within 0.5 pp of the paper's OrthoANI 98.73%.

### Stage 5 — CRISPR array detection
```
minced LL16.fna minced_default.crisprs minced_default.gff
minced -minNR 2 -minRL 20 -maxRL 50 -minSL 20 -maxSL 60 LL16.fna minced_loose.crisprs minced_loose.gff
```

- Default thresholds → 0 canonical arrays.
- Loose thresholds → 16 candidate regions, most below canonical 23-bp DR length.
- PGAP separately annotates Cas2 on contig 069 (confirming a CRISPR-Cas system exists, even without a canonical array recovered from the deposited draft).

### Stage 6 — Safety screening (independent-repro only)
```
abricate --db resfinder     LL16.fna > abricate_resfinder_LL16.tsv     # 0 acquired AMR
abricate --db card          LL16.fna > abricate_card_LL16.tsv          # 1 intrinsic (lmrD)
abricate --db vfdb          LL16.fna > abricate_vfdb_LL16.tsv          # 0 virulence
abricate --db plasmidfinder LL16.fna > abricate_plasmidfinder_LL16.tsv # 0 (DB scope: Enterobacteriaceae)
```

- Cross-check for AMR / virulence / plasmid replication genes.
- Prodigal V2.60 (meta mode) as an orthogonal third gene caller → 2,594 CDS (converges with PGAP's 2,511 and paper's Prokka 2,878 within ~10%).

### Stage 7 — Report synthesis
- Per-claim verdict assignment (VERIFIED / PARTIAL / NOT_TESTED / CONTRADICTED) into the master 36-row table.
- Coverage and Agreement computed on both raw-fraction and 9-point-scale bases.
- Limitations section explicitly enumerates the 6+ web-only tool blockers.

## Method substitutions

| Paper method | Replication substitute | Reason |
|---|---|---|
| SPAdes v3.15.3 | NCBI-deposited assembly | Same reads; NCBI may filter contamination |
| Prokka v1.14.6 | NCBI PGAP | Different pipeline; annotates same genes under sometimes-different names |
| OrthoANI (web) | skani 0.3.2 + FastANI 1.33 | Two FOSS k-mer ANI estimators |
| ResFinder v4.2 (web) | PGAP keyword search + abricate/ResFinder DB | Conservative substitute |
| VirulenceFinder v2.0.3 (web) | PGAP keyword search + abricate/VFDB | Conservative substitute |
| CRISPRCasFinder (web) | MinCED 0.4.2 (FOSS) | FOSS CRISPR array detector |
| PathogenFinder / BAGEL4 / antiSMASH / KEGG BlastKOALA / RAST / MobileElementFinder | NOT RUN | Web-only or database-scope-restricted; enumerated as blockers |

## Reproducibility invariants

1. **Deterministic re-runs.** Every stage above is a pure function of the input FASTA (and, for ANI, the IL1403 reference). No random seeds; no LLM calls in the compute path.
2. **Same accession, same result.** GCF_029912225.1 and GCA_029912225.1 are byte-identical; either yields identical downstream metrics.
3. **Two-tool ANI redundancy.** Any single-ANI-tool answer is cross-checked with a second FOSS estimator before promoting a claim to VERIFIED.
4. **Independent-reproduction cross-check.** Full pipeline was independently re-run on 2026-07-03 with independent code paths; 29/29 headline metrics matched (23 EXACT, 6 MATCH-within-convention, 0 CONTRADICTED).
5. **No paid API calls.** Argo Opus 4.7 (free) was used only for the report-synthesis phase; the compute path itself is 100% local FOSS.
