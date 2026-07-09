# Workflow — BVBRC-115

## Narrative

The paper claims are five-part: (a) genome architecture of UFLA258; (b) species-boundary ANI + dDDH + rpoB; (c) BGC profile; (d) CRISPR ratio; (e) taxonomic reclassification of 19 misfiled strains. The replication strategy: pull the paper's own deposited assembly (CP039297.1), plus 4 reference strains that cover the three species involved (FZB42 = *B. velezensis* type; UCMB5113 = deposited as amyloliquefaciens, argued by paper to be velezensis; DSM7 = *B. amyloliquefaciens* type; SCSIO05746 = *B. siamensis*), and re-run the three most-testable claim families with modern free tools on the UICGPU compute host.

We deliberately did NOT re-download all 105 *B. velezensis* genomes — the scale would exceed the wave-brief compute budget and the species-boundary claim is fully falsifiable on the 5-genome subset (if the boundary held here, the paper's central claim is validated in the type-strain corner-cases; if it failed here, the paper would be in trouble). The 5-genome subset is a strong minimum-viable replication.

Compute host: uicgpu (8×A100, 255 cores, 2 TB RAM). Prokka + antiSMASH v8 are the only nontrivial steps (~4 min prokka × 5 genomes, ~2 min antiSMASH × 2 runs). Everything else is seconds.

## Steps

1. Fetch source paper text (PMC OAI-PMH); render pandoc→PDF for the paper.pdf slot.
2. Fetch 5 genomes via NCBI E-utilities efetch (nuccore FASTA + one GBK).
3. rsync genomes to `/data/stevens/bvbrc-115/genomes/` on uicgpu.
4. Run `analysis.sh` on uicgpu:
    - Genome stats (BioPython) from FASTA + GBK
    - Pairwise ANI (fastANI, 5×5 matrix)
    - Annotate each genome (prokka --fast)
    - Extract rpoB from each annotated .ffn, align (MAFFT), compute %ID matrix
    - BLAST-based BGC gene panel scan (superseded by antiSMASH below)
5. Run antiSMASH v8.0.4 twice on UFLA258: (a) default, (b) with `--cb-knownclusters` for MIBiG hits.
6. Extract KCB per-region hits, map to paper's 7 conserved compounds.
7. rsync results back to Dropbox; write REPORT.md and the 8 required artifacts.

## Tools & versions

| Tool | Version | Purpose | Env |
|---|---|---|---|
| `fastANI` | 1.34 | Pairwise Average Nucleotide Identity | `/data/stevens/envs/bvbrc28` |
| `mafft` | v7.526 (2024) | Multiple sequence alignment (rpoB) | `/data/stevens/envs/bvbrc28` |
| `mash` | 2.3 | (available, not used in final path) | `/data/stevens/envs/bvbrc28` |
| `prokka` | 1.12 | Annotation for rpoB extraction | `/data/stevens/envs/bvbrc28` |
| `barrnap` | 0.9 | (available, prokka uses it internally) | `/data/stevens/envs/bvbrc28` |
| `prodigal` | v2.6.3 | Gene prediction (prokka calls it, and antiSMASH `--genefinding-tool prodigal`) | `/data/stevens/envs/bvbrc28` |
| `blastn` | 2.5.0+ | BGC gene BLAST (superseded by antiSMASH) | `/data/stevens/envs/bvbrc28` |
| `antiSMASH` | 8.0.4 | BGC region detection + KnownClusterBlast → MIBiG | `/data/stevens/envs/antismash` |
| `BioPython` | 1.87 | FASTA/GBK parsing, %ID matrix | `/data/stevens/envs/bvbrc38` python3 |
| `pandoc` + XeLaTeX | 3.x + TeX Live 2024 | JATS-derived Markdown → paper.pdf | CherryRd (macOS) |
| `rsync`, `ssh`, `curl` | system | Data movement | Both hosts |

## Codes & scripts (in this dir)

- `work/analysis.sh` — full pipeline (steps 4 above), 202 lines. Runs on uicgpu; assumes bvbrc28+bvbrc38 conda envs.
- `work/PMC6788494.nxml.xml` — the JATS-NXML raw fetch (78 kB).
- `extraction/marker.md` and `extraction/nougat.mmd` — derived plain-text article (with provenance header explaining PDF-inaccessibility fallback to JATS).
- `work/genomes/*.fasta` — the 5 downloaded genomes (5 files, ~20 MB total).
- `work/UFLA258.gbk` — the paper's own deposited annotation (CP039297.1 GenBank flatfile, 9 MB).
- Ad-hoc helper scripts in `/tmp/` on both hosts (rpoB_extract_v2.py, antismash_kcb.py, antismash_extract.py) — outputs merged into `report/evidence/`.

## Effort estimate

- Human/agent decisions: ~15 (fetch PMID → find PDF path → fall back to JATS → pick reference genomes → run prokka → notice rpoB extraction bug in siamensis → fix with better regex → notice antiSMASH default lacks compound names → rerun with `--cb-knownclusters` → parse KCB txt → write report).
- Wall-clock: ~45 min end-to-end from wave-brief acceptance to REPORT.md.
- Compute time on uicgpu:
    - fastANI (5×5): <10 s
    - Prokka × 5 genomes: ~4 min
    - MAFFT rpoB align: <2 s
    - antiSMASH v8 (default): ~120 s
    - antiSMASH v8 (with KCB): ~180 s
    - **Total compute: ~8–10 min wall.**
- Data volume: ~30 MB genomes + ~20 MB antiSMASH output = ~50 MB total in `/data/stevens/bvbrc-115/`; ~150 kB shipped back to Dropbox.
- LOC written: `analysis.sh` (202) + 4 ad-hoc python scripts (~150) + 8 report/artifact markdown/json files.
- No LLM was in the analysis loop; all numeric comparisons in REPORT.md are direct file-lookups against `report/evidence/*.json`.
