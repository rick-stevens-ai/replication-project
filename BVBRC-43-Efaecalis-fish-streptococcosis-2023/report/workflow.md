# Workflow: Akter 2023 (BVBRC-43) Replication

**Paper:** Akter et al., *Scientific Reports* 13:1551 (2023). DOI 10.1038/s41598-022-25968-8.
**Set:** BVBRC-43. **Class:** WGS assembly + annotation.
**Verdict:** PARTIAL REPLICATION (strong).

All steps use only free public data + free endpoints (Argo proxy). No paid API was used.

## Stage 0 — Paper ingest
- Pull full-text XML from Europe PMC: `PMC9883459/fullTextXML` → `work/efaecalis_fulltext.xml`.
- Extract Table 1 (genome features), Table 2 (AMR groups), and Results-section verbatim claims (esp. "agg and prgB were absent in BFF1B1 and BFPS6") → `report/evidence/paper_targets.json`.

## Stage 1 — Accession mapping
- Paper accessions: BFFF11 = CP045918, BFF1B1 = CP046022, BFPS6 = JADBGH010000000.
- NCBI eutils elink (nuccore → assembly) + esummary to resolve assembly accessions:
  - BFFF11 → **GCA_009685155.1**
  - BFF1B1 → **GCF_017357805.1**
  - BFPS6  → **GCF_021375735.1**
- Positive control (V583, AE016830): **GCF_000007785.1**.

## Stage 2 — Genome pull (NCBI Datasets v2alpha REST, free, no auth)
For each of the 4 assemblies:
```
curl -sS -o "$acc.zip" \
  "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/$acc/download?include_annotation_type=GENOME_FASTA&include_annotation_type=PROT_FASTA&include_annotation_type=CDS_FASTA&include_annotation_type=GENOME_GFF"
unzip -oq "$acc.zip" -d "$acc"
```
Outputs land under `work/genomes/<accession>/`. Checksums recorded.

## Stage 3 — Genome statistics (C6 → Table 1 test)
- `work/genome_stats.py` (pure-Python stdlib): parses FASTA per assembly and emits size, contig count, GC%, N50, L50, CDS/protein counts → `report/evidence/genome_stats.json`.
- Compared numerically against paper Table 1.

## Stage 4 — AMR profiling (C2/C3 test)
- Run on uicgpu (env `amr`, AMRFinderPlus 3.12.8, DB 2024-07-22.1):
  ```
  amrfinder -n <fna> --organism Enterococcus_faecalis --plus -o <strain>_amrfinder.tsv
  ```
- Tool independent of paper's ResFinder/CARD/ARG-ANNOT (deliberate: independent verification).
- V583 included as positive control (must recover vanB, erm(B), aac(6')-aph(2''), qacZ).
- Outputs pulled back → `report/evidence/<strain>_amrfinder.tsv`.

## Stage 5 — MLST + ANI (C5 test)
- `mlst <fna> --scheme efaecalis` → `report/evidence/<strain>_mlst.tsv`.
- `fastANI --ql list.txt --rl list.txt -o fastani_matrix.tsv` all-vs-all across the 4 assemblies.

## Stage 6 — Virulence markers (C1 / C1b test)
- `work/build_vf_query.py`: extract 13 curated markers from the V583 proteome — fsrA, fsrB, ace, ebpA, ebpC, srtA, srtC, cylLS, cylLL, cylR2, tpx, agg/prgB, asa1 → `work/vf_query.faa`.
- `work/vf_blast.py`: `makeblastdb` per fish genome (nucl), then `tblastn` with vf_query.faa.
- Presence rule (locked before running): **pident ≥ 80 AND qcov ≥ 70 AND e ≤ 1e-20**.
- Outputs → `report/evidence/vf_presence.json`, plus separate `tet_presence.json` targeted probe.

## Stage 7 — Scoring and judge
- Hand-computed match table (paper vs replication) written into `REPORT.md` §4.
- Free-Argo LLM-judge (`argo:gpt-5.2`) via `work/judge.py`: sees the evidence bundle only, emits verdict + coverage + brief rationale → `report/evidence/llm_judge.txt`.

## Stage 8 — Report
- Human summary → `report/REPORT.md`.
- LaTeX report → `report/REPORT.tex`.
- Attempt log, artifact harvest, brief, failure analysis → sibling files in `report/`.

## Dependencies (verified free)
- Europe PMC REST, NCBI eutils, NCBI Datasets v2alpha REST.
- AMRFinderPlus 3.12.8 (DB 2024-07-22.1), mlst, fastANI, BLAST+ (uicgpu env, CherryRd).
- Python 3 stdlib.
- Argo proxy (`argo:gpt-5.2`) — free endpoint, `Authorization: Bearer stevens`.

## Compute
Total wall time <10 minutes across all four genomes. No GPU required; uicgpu used only because the AMR toolchain is pre-installed there.

## Reproduce (quickstart)
```
for acc in GCA_009685155.1 GCF_017357805.1 GCF_021375735.1 GCF_000007785.1; do
  curl -sS -o "$acc.zip" "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/$acc/download?include_annotation_type=GENOME_FASTA&include_annotation_type=PROT_FASTA&include_annotation_type=CDS_FASTA&include_annotation_type=GENOME_GFF"
  unzip -oq "$acc.zip" -d "$acc"
done
python3 genome_stats.py
python3 build_vf_query.py && python3 vf_blast.py
bash run_amr_mlst.sh   # tet(L)+tet(M) should appear ONLY on BFPS6
```

## Scope explicitly OUT (see failure_analysis.md)
- antiSMASH bacteriocin/NRPS rerun (C4).
- PHASTER prophage inventory.
- PlasmidFinder replicon typing (relevant to BFPS6 tet cassette context).
- ISfinder IS-element inventory.
- Full CSIphylogeny SNP tree (C5 tested only at ANI/MLST resolution).
- Any wet-lab phenotype confirmation.
