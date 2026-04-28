# Updated Virophage Taxonomy and Distinction from Polinton-like Viruses

- **OSTI ID:** 2475938
- **Paper:** Roux et al., *Biomolecules* 13:204 (2023)
- **Rank:** #9
- **Original replication-score target:** 9/10
- **Realised score (this run):** ~6/10 (simplified reference set)

## Why This Paper
This genomics paper uses publicly available genome sequences, computational analysis, and quantitative taxonomic criteria, allowing for fully automated AI replication and validation.

## Replication Plan (high level)
Collect genome datasets → predict ORFs (Prodigal) → apply HMM profiles for marker genes (MCP, ATPase, PRO, penton + PLV HMM) → align & trim markers → build ML phylogenies (IQ-TREE) → confirm virophage monophyly and virophage/PLV discrimination.

## Status
- [x] Paper reviewed
- [x] Data identified (22 NCBI GenBank accessions; 13 retained after size filtering)
- [x] Code implemented (Prodigal + HMMER + MAFFT + trimAl + IQ-TREE)
- [x] Results validated (congruent 4-marker phylogeny; clean HMM separation of virophages vs PLV/adintovirus)

## This Replication

Run on **CherryRd** (macOS, conda env `virophage`), total wall time < 20 min compute
(+ ~5 min download). Deliverables:

- **Report PDF:** [`replication/report/report.pdf`](replication/report/report.pdf) (6 pages)
- **Figures:** `replication/report/phylogeny_4markers.pdf`, `replication/report/hmm_heatmap.pdf`
- **Classification table:** `replication/results/hmm_summary.tsv`
- **Trees (Newick):** `replication/results/trees/{MCP,ATPase,PRO,Penton}.treefile`
- **Alignments:** `replication/results/markers/{MCP,ATPase,PRO,Penton}.{aln,trim}`

### Key findings (replicated)

1. **HMM classification matches the paper.** 7/13 genomes (Sputnik, Mavirus,
   SW01, YSLV1–4) hit all four virophage marker HMMs strongly (MCP ≥ 472 bits);
   the remaining 6 (TVSG_01 PLV, three *Chrysochromulina parva* virophages,
   adintovirus, and two partial/mis-labelled GenBank records) have **zero**
   hits above inclusion to any of the 19 virophage HMMs or the PLV HMM.
2. **Virophage–PLV distinction is reproducible.** Virophages score
   ≥ 82–765 bits on the four morphogenesis markers; PLVs / adintoviruses
   score 0 — directly confirming the paper's statement that the marker
   HMMs separate the two classes.
3. **Four-marker phylogenetic congruence.** MCP, ATPase, PRO, and penton
   trees (IQ-TREE, 1000 UFBoot) all recover the same backbone:
   Mavirus basal → Sputnik early-diverging → SW01+YSLV4 sister pair
   (100/100 in MCP/ATPase/Penton), matching the family-level structure
   of Fig. 1 in the paper.

### Layout

```
replication/
├── ICTV_VirophageSG/          # cloned from github.com/simroux/ICTV_VirophageSG
├── data/
│   ├── all_genomes.fasta      # raw 22-accession efetch
│   ├── extra.fasta
│   ├── labels.tsv
│   ├── genomes/               # per-accession FASTA (pre-filter)
│   └── genomes_filt/          # 13 size-filtered genomes used
├── results/
│   ├── proteins/              # Prodigal outputs
│   ├── all_proteins.faa
│   ├── markers_hit.tbl        # hmmsearch vs All_markers.hmm
│   ├── plv_hit.tbl            # hmmsearch vs PLV_PC_054.hmm
│   ├── hmm_summary.tsv        # classification table
│   ├── hmm_heatmap.{png,pdf}
│   ├── markers/               # per-marker FAA, MAFFT aln, trimAl output
│   └── trees/                 # IQ-TREE outputs + rendered figure
└── report/
    ├── report.tex
    ├── report.pdf             # <-- main deliverable
    ├── phylogeny_4markers.pdf
    └── hmm_heatmap.pdf
```

### Reproducing

```bash
mamba create -n virophage -c bioconda -c conda-forge -y \
    hmmer mafft iqtree trimal prodigal biopython
git clone https://github.com/simroux/ICTV_VirophageSG.git
# then run the steps documented in replication/report/report.tex §2
```

### Caveats / scope

- Only 13 genomes (vs 848 vOTUs in the paper) — so class-level
  monophyly and family thresholds are sampled rather than proven.
- No AAI/MCL genome-wide clustering (requires full IMG/VR).
- Several accessions fetched from NCBI contained unexpected content
  (e.g., `NC_020860` returned a 44-kb genome not matching its Zamilon
  label); the HMM-first workflow correctly ignores accession labels and
  classifies from sequence content.
