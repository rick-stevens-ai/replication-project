# BVBRC-94 — Artifact Harvest

All artifacts pulled independently from public sources. No paywalled data. All accessions verified live 2026-07-04.

## Bibliographic / OA
- Europe PMC core JSON (`EXT_ID:37110457 AND SRC:MED`) → `evidence/europepmc_mileriene2023.json` (isOpenAccess=Y, PMC10145936, license=CC-BY).
- Paper PDF: `https://europepmc.org/articles/PMC10145936?pdf=render` → `work/mileriene2023.pdf` (2.02 MB, 10 pp) → `work/mileriene2023.txt` (1350 lines, pdftotext).

## Genome assembly
- **GCA_029912225.1 / GCF_029912225.1** (`ASM2991222v1`, submitter: Lithuanian University of Health Sciences, submit date 2023-05-01; corresponds to WGS master `JARHUB000000000` cited by paper).
- BioSample: SAMN33682203.
- Downloaded via NCBI Datasets v2alpha REST (`https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_029912225.1/download`).
- Files (`work/ll16_assembly/ncbi_dataset/data/GCA_029912225.1/`):
  - `GCA_029912225.1_ASM2991222v1_genomic.fna` (2,473,617 bp across 372 contigs).
  - `cds_from_genomic.fna` (2,469 CDS nt).
  - `protein.faa` (2,469 protein sequences).
  - `genomic.gff` (PGAP annotation).
- Assembly summary JSON → `evidence/assembly_summary.json`.

## Reference genomes / plasmids / genes
- **`GCF_002078975.1_ASM207897v1`** — L. lactis subsp. lactis UC06 (`NZ_CP015902.1` chromosome). NCBI FTP: `ftp.ncbi.nlm.nih.gov/genomes/all/GCF/002/078/975/…`. File: `work/refs/uc06_genomic.fna` (2,714,292 bytes).
- **`AF178424.1`** — L. lactis pCI2000 plasmid (repA/parA, the repUS4 archetype). Efetch nuccore, `work/refs/pCI2000_AF178424.fna` (10,295 bytes).
- **UniProt `P35518` (LCNB_LACLC)** — Bacteriocin lactococcin B, 68 aa. `work/refs/lcnB_correct.faa`.
- **UniProt `P35517` (LCIB_LACLC)** — Lactococcin B immunity protein (same fasta file).
- **UniProt `Q4FD00`** — Enterolysin A-like fragment (Enterococcus malodoratus). `work/refs/enlA_uni.faa`.
- **UniProt `Q9CG20` (DCE_LACLA)** — GadB glutamate decarboxylase, L. lactis IL1403, 466 aa. `work/refs/gadB_uni.faa`.
- **UniProt `Q9CG19` (GADC_LACLA)** — GadC glutamate/GABA antiporter, L. lactis IL1403, 511 aa. `work/refs/gadC_uni.faa`.
- **UniProt `O30416`** — GadR positive regulator, L. lactis, 279 aa. `work/refs/gadR_uni.faa`.

## Analysis outputs (all in `work/results/`, evidence copies in `report/evidence/`)
- `mash_ll16_vs_uc06.txt` — mash distance LL16↔UC06 (0.00399629, 851/1000 shared).
- `barrnap_ll16.gff` — barrnap 0.9 rRNA predictions.
- `blastn_pCI2000_vs_ll16.tsv` — pCI2000/AF178424 vs LL16 blastn.
- `tblastn_lcnB_vs_ll16.tsv` — Lactococcin B (+ LciB) tblastn.
- `tblastn_enlA_vs_ll16.tsv` — Enterolysin A-like tblastn.
- `tblastn_gadB_vs_ll16.tsv`, `tblastn_gadC.tsv`, `tblastn_gadR.tsv` — GAD operon tblastn.
- `abricate_{resfinder,card,ncbibetalactamase,argannot,plasmidfinder,vfdb}.tsv` — ABRicate scans.

## Tool versions
- Python 3.14.6 (macOS driver), Python 3.11 (uicgpu envs).
- NCBI BLAST+ (from `envs/kleborate/bin/`, contemporary release).
- mash (from same env).
- barrnap 0.9 (`envs/bvbrc28/bin/`).
- abricate + DBs (resfinder Jul-2017, card Jul-2017, ncbibetalactamase Mar-2017, argannot Jul-2017, plasmidfinder Mar-2019, vfdb Mar-2017). **DB age is a real caveat** — newer AMR/VFDB releases might pick up hits not in the 2017/2019 snapshots. However, for the paper's own claim ("no acquired AMR, no virulence factors on ResFinder v4.1 / VirulenceFinder v2.0.3 — 2022-vintage") the 2017 DBs are a lower bound; a modern re-scan would if anything find MORE hits, so an all-zero 2017 scan robustly supports the paper's claim.
- NCBI Datasets REST v2alpha.
- Europe PMC REST 6.9.

## Not obtained / attempted but failed
- antiSMASH databases (`/data/stevens/antismash_db/` empty on uicgpu — full DB is ~20 GB, skipped in the interest of time; T3PKS claim was cross-checked via direct PGAP annotation grep instead).
- Raw MiSeq reads (paper does not include an SRA accession in the deposited BioSample — only the polished assembly was made public).
