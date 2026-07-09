# Attempt Log — BVBRC-57 (Kang et al. 2020, P. psychrotolerans/oryzihabitans CS51)

Analyst: Ollie (OpenClaw subagent). Date: 2026-07-02. Compute: local + uicgpu (8×A100 node; conda envs bvbrc14 / bvbrc28).

1. **Candidate selection.** Read WAVE_BRIEF_2026-07-01.md + BVBRC-17 exemplar. Walked BVBRC_TOPUP85 ranks 43+. Rank 43 (Kang 2020, *P. psychrotolerans* CS51, PMID 32182882, 58 cites, *Microorganisms*) = highest-ranked genuinely-new candidate: no Pseudomonas non-aeruginosa in the existing BVBRC-01..56 set; clean single-genome BV-BRC Comprehensive Genome Analysis workflow; OA. Skipped rank 44 (Hyun2020 pangenomics — overlaps BVBRC-12 Hyun2020). Picked it → BVBRC-57.

2. **Paper retrieval.** Europe PMC core search (S2-free) → PMC7142416, CC-BY, OA. Pulled full-text XML (`fullTextXML`, 200 KB). Extracted all numeric claims + the GenBank accession **CP021645** from the Data Availability statement.

3. **Accession resolution.** eutils esearch/esummary on CP021645 → assembly **GCF_006384975.1** (GCA_006384975.1), organism recorded by NCBI as ***Pseudomonas oryzihabitans*** strain CS51 (taxid 47885) — a reclassification vs the paper's *P. psychrotolerans*. Chromosome length 5,364,174 bp (matches paper exactly).

4. **Genome download.** NCBI Datasets REST v2alpha (no auth) → FASTA + protein.faa + GFF + CDS. Local genome stats (Python): 1 contig, 5,364,174 bp, GC 64.71%, 4837 genes / 4846 CDS / 4714 proteins, 15 rRNA, 67 tRNA. All match paper.

5. **Functional gene detection (RefSeq PGAP GFF grep + evidence file).** Confirmed copper homeostasis (Cop system), cobalt-zinc-cadmium/heavy-metal efflux (DmeF CDF, heavy-metal P-type ATPase, two-component sensor/regulator, ZntB), nickel (urease + Co/Ni efflux), auxin/IAA (trpAB, PRAI, anthranilate synthase/dioxygenase, TrpC), nitrate/nitrite (nitrate reductase, NirB/NirD), phosphate-specific (PstSCAB), sulfate (CysTWZ + ABC).

6. **uicgpu setup.** ssh uicgpu + `source ~/env.sh` (proxy). Found existing conda envs **bvbrc14** (amrfinder 4.2.7, abricate, mlst 2.33.1, blast) and **bvbrc28** (datasets 18.32.0, prokka, fastANI, roary). No new env build needed. Copied CS51.fna + protein.faa up.

7. **AMR / specialty genes.** AMRFinderPlus (`--plus`) → **no acquired AMR genes** (expected for environmental PGPR). abricate: CARD 4 hits (rsmA/arnA/MexF efflux/intrinsic, 81-86% id), resfinder/plasmidfinder/ncbi 0, VFDB 30 hits (all core chemotaxis/flagellar/pili genes — not true virulence). **bacmet2 (metal/biocide DB): 239 hits**; high-confidence (≥50% id) include copABCD/copRS, cadR, dmeF, chrAB (chromate), arsC (arsenate), NikBCDE, mntP/mntR, mexAB/mexEF-oprM.

8. **MLST.** `mlst` → no scheme call (P. oryzihabitans has no PubMLST scheme; paper did not do MLST either).

9. **Pan-genome.** Downloaded 8 additional public *P. oryzihabitans* complete genomes (RefSeq) + CS51. fastANI vs CS51: PRS08-11306 (GCF_001913135.1) = 94.09% (highest); all others 88-89% (below 95% species cutoff → taxonomy genuinely ambiguous). prokka-annotated all 9 (Pseudomonas), ran roary (-i 90). **Core (99-100%) = 2790, pan = 10444.** Accumulation curves: core monotone 4777→2790, pan monotone 4777→10444 (open pan-genome) — reproduces paper Fig 6 shape. Accessory tree: CS51 sister to PRS08-11306 (the paper's closest reference).

10. **Core-count nuance.** Paper's 2122 core genes was computed vs a CROSS-SPECIES outgroup set (P. syringae, P. putida, P. psychrotolerans PRS08, P. aeruginosa), shrinking the core. Our conspecific set → larger core (2790). Qualitative claim reproduced; exact count is method/genome-set dependent → not numerically reproduced (honest PARTIAL on C14).

11. **LLM-judge.** Argo gpt-5.2 (free, localhost:44497) scored the full claims table: coverage 100%, agreement 93%, **VERDICT REPLICATED**.

## What worked
- Exact match on every reported genome statistic (size, GC, rRNA, tRNA).
- All paper functional-gene categories independently confirmed via two orthogonal annotations (PGAP + bacmet2/CARD/VFDB).
- Pan-genome shape + phylogenetic placement reproduced.

## What did not fully reproduce
- Exact core-gene count (2122): different by design (cross-species vs conspecific comparison; BPGA vs roary). Not a contradiction.
- No MLST call (no scheme exists) — non-issue.

## Notable extra finding
- NCBI has reclassified CS51 from *P. psychrotolerans* to *P. oryzihabitans*; even other "*P. oryzihabitans*" genomes are only ~89% ANI to CS51, so its precise species assignment remains open.
