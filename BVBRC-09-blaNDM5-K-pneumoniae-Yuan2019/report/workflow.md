# Workflow — Yuan et al. 2019 Replication (BVBRC-09)

## 1. Narrative

**Objective:** independently verify the in-silico claims of Yuan et al. 2019 (blaNDM-5 on IncX3 plasmid in a ST29/K54 hypervirulent K. pneumoniae SCNJ1 isolate) using open tools and public sequence data.

**Two-phase execution:**

- **Phase 1 (2026-05-10, main-workflow host):** primary claim verification for MLST, capsular typing, AMR gene detection, virulence gene detection, plasmid characterization, and pairwise BLAST comparisons against pNDM_MGR194, pLVPK, pL22-1. Phylogenies deferred because CSI Phylogeny requires the CGE web server and OrthoFinder requires substantial CPU.
- **Phase 2 (2026-05-10 continuation, chiatta00 JLSE node):** the two phylogeny reconstructions (60-genome ST29 tree via Parsnp→Gubbins→RAxML-NG, and 231-plasmid IncX3 tree via Mash→NJ) that Phase 1 flagged NOT_REPLICATED. Ran on chiatta00 (128 cores, 2.1 TB RAM). Gateway session closed at ~40 min; final sync was manual.
- **Backfill (2026-07-05, this session):** meet the 8-artifact standard — fetch paper PDF, generate Marker/Nougat placeholder extractions, write LaTeX report, 5 open questions, workflow, artifacts summary, failure analysis. NO re-run of genomic analysis; grounded in the existing REPORT.md + evidence + a re-read of the paper.

**Data flow:**

```
NCBI RefSeq (GCF_008320705.1)
  ├─ SCNJ1_chromosome.fasta (NZ_CP174529.1, 5,191,370 bp)
  ├─ SCNJ1_pVir.fasta       (NZ_CP174530.1, 211,858 bp)
  └─ SCNJ1_pNDM5.fasta      (NZ_CP174531.1, 45,255 bp)

SCNJ1_complete.fasta ──┬──► Kleborate v3.1.3        ──► MLST=ST29, K=54, virulence_score=4
                       ├──► ABRicate + ResFinder    ──► blaNDM-5, blaSHV-187, oqxA/B, fosA6
                       ├──► ABRicate + PlasmidFinder──► IncX3 on pNDM5; repB_KLEB_VIR on pVir
                       └──► ABRicate + VFDB         ──► ybt, ent, mrk, iuc, iro clusters

SCNJ1_pNDM5.fasta      + pNDM_MGR194 (KF220657) ──► BLASTn ──► 100% cov / 99.99% id
SCNJ1_pVir.fasta       + pLVPK      (NC_005249)  ──► BLASTn ──► 94% cov / 99.58% id
SCNJ1_pVir.fasta       + pL22-1     (NZ_CP031258)──► BLASTn ──► 99% cov / 99.73% id

59 ST29 K. pneumoniae assemblies from NCBI + SCNJ1
  ──► Parsnp v2.1.5 (core-genome alignment)
  ──► Gubbins v3.4.3 (recombination filtering, 368,803 bp masked)
  ──► RAxML-NG v2.0.1 (GTR+G, 100 bootstraps)
  ──► 55-tip ML tree, SCNJ1 closest to GCA_003286975 (33 SNPs), SCLZ15-011 4th closest (53 SNPs)

231 IncX3 plasmids (paper Table S4 + pNDM5-SCNJ1 as MK715437)
  ──► Mash v2.3 sketch (k=21, s=1000)
  ──► 53,361 pairwise distances
  ──► Biopython DistanceTreeConstructor (NJ)
  ──► 231-tip NJ tree, pNDM5-SCNJ1 clusters with KP776609 (0.000072), AP018141 (0.000119)
```

---

## 2. Tools and versions (complete inventory)

| Tool | Version | Role | Endpoint |
|---|---|---|---|
| Kleborate | 3.1.3 | MLST, K/O typing, virulence & resistance scoring | local |
| ABRicate | 1.4.0 | AMR / virulence / plasmid gene detection | local |
| ResFinder DB | 2026 snapshot | AMR gene database | via ABRicate |
| VFDB | 2026 snapshot | virulence gene database | via ABRicate |
| PlasmidFinder DB | 2026 snapshot | replicon typing database | via ABRicate |
| BLAST+ (blastn) | 2.16.0 | pairwise plasmid comparisons | local |
| Biopython | 1.87 | sequence statistics, NJ tree construction | local Python |
| Parsnp | 2.1.5 | core-genome alignment, 60 genomes | chiatta00 |
| Gubbins | 3.4.3 | recombination filtering | chiatta00 |
| RAxML-NG | 2.0.1 | ML phylogeny (GTR+G, 100 bootstraps) | chiatta00 |
| Mash | 2.3 | k-mer distance estimation (IncX3) | chiatta00 |
| OrthoFinder | 2.5.5 | protein orthogroup clustering (Phase 2) | chiatta00 |
| MAFFT | 7.520 | MSA (via OrthoFinder pipeline) | chiatta00 |
| FastTree | 2.1.11 | species-tree inference (OrthoFinder pipeline) | chiatta00 |
| Prodigal | 2.6.3 | protein prediction on plasmids | local |
| NCBI Datasets CLI | 18.25.1 | genome/sequence download | local |
| pdftotext (poppler) | system | PDF text extraction (Marker fallback) | local (backfill) |
| curl | 8.x | PDF fetch | local (backfill) |

**Not used** (because no GPU / no central corpus hit in this backfill session):
- Marker (canonical PDF→Markdown)
- Nougat (canonical PDF→MMD)

---

## 3. Command-line summary (representative, not exhaustive)

Phase 1 / 2 commands are preserved as file artifacts under `analysis/` (implicit through file naming). Representative:

```bash
# Genome pull
datasets download genome accession GCF_008320705.1

# Kleborate
kleborate --assemblies SCNJ1_complete.fasta --preset kpsc --outdir analysis/kleborate

# ABRicate
abricate --db resfinder      SCNJ1_complete.fasta > analysis/abricate_resfinder.tsv
abricate --db vfdb           SCNJ1_complete.fasta > analysis/abricate_vfdb.tsv
abricate --db plasmidfinder  SCNJ1_complete.fasta > analysis/abricate_plasmidfinder.tsv

# BLAST comparisons
makeblastdb -in pNDM_MGR194.fasta -dbtype nucl -out analysis/pNDM_MGR194_db
blastn -query SCNJ1_pNDM5.fasta -db analysis/pNDM_MGR194_db -outfmt '6 qseqid sseqid pident length qcovs' \
  > analysis/blast_pNDM5_vs_MGR194.txt

# Phase 2 phylogeny
parsnp -g reference.gbk -d ST29_genomes/ -o analysis/phylogeny/st29
run_gubbins.py --prefix st29_gubbins parsnp.xmfa
raxml-ng --all --msa st29_gubbins.filtered_polymorphic_sites.fasta \
  --model GTR+G --seed 42 --bs-trees 100 --prefix st29_final

# Phase 2 IncX3
mash sketch -k 21 -s 1000 -o incx3.msh IncX3_plasmids/*.fasta
mash dist incx3.msh incx3.msh > mash_distances_v2.tab
# NJ tree constructed via Biopython DistanceTreeConstructor
```

Backfill:
```bash
# PDF fetch
curl -sSL --http1.1 -A "Mozilla/5.0 ..." \
  -o paper.pdf "https://aricjournal.biomedcentral.com/counter/pdf/10.1186/s13756-019-0596-1.pdf"

# sha256
shasum -a 256 paper.pdf
# → 204f058d324790ee989f89629bd54778c6712df94f51129a69b52a70c7e27906

# Central corpus lookup (Polaris login-01)
ssh polaris-01 'ls /eagle/projects/AuroraGPT/stevens/scout_corpus/{md,mmd}/<sha256>.*'
# → no hit → pdftotext fallback

pdftotext -layout paper.pdf extraction/marker.md
# Nougat pending: extraction/nougat.mmd is placeholder stub with sha256 for later corpus sweep.
```

---

## 4. Effort estimate

| Category | Estimate |
|---|---|
| Phase 1 wall-clock | ~1.5 hours (data pull ~15 min; Kleborate + ABRicate + BLAST + report writing) |
| Phase 2 wall-clock | ~40 min chiatta00 (128-core Parsnp + Gubbins + RAxML-NG + Mash) before session-close; small amount of manual sync afterward |
| Backfill wall-clock (this session) | ~45 min (PDF fetch, Marker fallback, LaTeX report + 5 open questions + workflow + artifacts summary + failure analysis) |
| Total wall-clock | ~3 hours across three sessions |
| Compute time | Phase 1 ~30 min single-node CPU; Phase 2 ~35 min 128-core CPU (~75 CPU-hours equivalent); backfill negligible (<1 CPU-min) |
| Agent steps | Phase 1 ~30 tool calls; Phase 2 ~10 tool calls; backfill ~15 tool calls; total ~55 |
| LOC written | ~0 novel code (all off-the-shelf tools + curl + pdftotext); shell command lines ~50; JSON/markdown/tex ~800 lines across report artifacts |
| Runs executed | Phase 1: 3 ABRicate runs, 1 Kleborate, 3 BLASTs, Prodigal. Phase 2: 1 Parsnp, 1 Gubbins, 1 RAxML-NG, 1 Mash sketch + 1 Mash dist, 1 Biopython NJ, 1 OrthoFinder. Backfill: 1 PDF fetch, 1 pdftotext. |
| Human time | Rick: 0 (fully agent-driven); Ollie / Kukla / gateway agent: as above |
| Free-endpoint LLM calls | Reasoning + writing: all via Argo localhost:44497 (Claude Opus family) — no paid API used |

---

## 5. Reproducibility notes

- All input FASTA files are public (NCBI RefSeq GCF_008320705.1, plus KF220657/NC_005249/NZ_CP031258 for comparators, plus the 59 ST29 accessions and 230 IncX3 accessions in the paper's Tables S2/S4).
- Tools are open-source; versions logged above.
- Complete command lines for Phase 2 are captured only in summary form (log-loss at session close). To fully reproduce Phase 2, use the commands in section 3 above with default parameters plus `--bs-trees 100` for RAxML-NG bootstrap; Gubbins default settings (max 10 iterations, no min-SNPs threshold override).
- Reference for the paper's Supplementary Table S4 (IncX3 plasmid list) requires pulling the .docx from https://static-content.springer.com (search PMC6701021 supplementary).
- Central Marker/Nougat parse: pending — sha256 = `204f058d324790ee989f89629bd54778c6712df94f51129a69b52a70c7e27906`.
