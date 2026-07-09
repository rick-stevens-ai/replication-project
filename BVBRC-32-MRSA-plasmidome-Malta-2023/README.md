# BVBRC-32 — MRSA Plasmidome (Malaysia, 2023)

**Paper:** Al-Trad et al. 2023, "The Plasmidomic Landscape of Clinical Methicillin-Resistant
*Staphylococcus aureus* Isolates from Malaysia", *Antibiotics* 12(4):733.
DOI 10.3390/antibiotics12040733 · PMID 37107095 · PMCID PMC10135026 (OA).

> **Note:** task brief said "Malta" — the real paper is **Malaysia**. Dir name kept for ledger continuity.

## Status: PARTIAL–to–STRONG REPLICATION (judge: PARTIAL) — reproducibility GOOD

Independent re-analysis of the study's **own 88 public GenBank genomes** (BioProject
PRJNA722830) using the **same CGE reference databases** (PlasmidFinder / ResFinder /
DisinFinder) run via direct BLASTn at default thresholds.

### Reproduced
- 85/88 genomes carry plasmids; exactly **3 plasmid-free** (paper: 3 sequenced plasmid-free).
- **All 7** replicase superfamilies (RepL, Rep_trans, Rep_1, Rep_2, Rep_3, RepA_N, PriCT_1).
- **RepL dominant** (n=66–67; paper 63); rare types **exact** (Rep_2=2, PriCT_1=1).
- **erm(C) in 67 genomes, 66 plasmid-borne** → the paper's headline RepL/ermC signal (paper: 63).
- **mecA 88/88** (all MRSA); rare plasmid AMR genes all found (tetK/L, aadD, mupA, ermB, cat).
- **qacA/B biocide plasmids** in 5 genomes.

### Not reproduced
- 74% (140/189) resistance-per-plasmid proportion (unit mismatch: curated plasmid molecules +
  heavy-metal operons vs draft-contig replicon loci + AMR-only DB → repl. ~47% lower bound).
- Heavy-metal operon sub-counts (cadAC/cadDX/mer/ars/cop) — not screened (no dedicated DB).

## Layout
```
paper/    fulltext.xml, paper_text.txt (from PMC OA)
work/     download + BLAST pipeline scripts, CGE DBs (plasmidfinder_db, resfinder_db, disinfinder_db),
          genomes/ (88 assemblies), *_results/ raw BLAST outputs
data/     accessions.txt (88 GCA), rep + AMR summary JSONs
analysis/ replicon_loci.tsv, amr_hits.tsv (per-genome hit tables)
report/   REPORT.md (full analysis), judge_verdict.md (LLM-judge)
```

## Reproduce
```bash
cd work
datasets download genome accession --inputfile gca_accessions.txt --include genome --filename genomes.zip
(cd genomes && unzip -o -q ../genomes.zip)
python3 run_plasmidfinder_blast.py      # rep typing (raw)
python3 dedup_replicons.py              # collapse to replicon loci -> summary_dedup.json
python3 run_resfinder_blast.py          # AMR genes
```
DBs: `git clone https://bitbucket.org/genomicepidemiology/{plasmidfinder_db,resfinder_db,disinfinder_db}.git`

## Data provenance
- Genomes: NCBI BioProject **PRJNA722830** (88 GCA assemblies), downloaded 2026-07-01 via NCBI Datasets.
- Paper full text: Europe PMC PMC10135026 fullTextXML.
- Reference DBs: CGE genomicepidemiology bitbucket (PlasmidFinder / ResFinder / DisinFinder).
