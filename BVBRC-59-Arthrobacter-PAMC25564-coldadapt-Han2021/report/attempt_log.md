# Attempt Log — BVBRC-59

1. Read WAVE_BRIEF_2026-07-01.md + BVBRC-22 exemplar. Confirmed verdict vocabulary + output structure.
2. Selected candidate from BVBRC_TOPUP85 ranks 46+. Rank 47 = *Arthrobacter* sp. PAMC25564 (cold adaptation / CAZymes, Han et al. 2021, BMC Genomics, PMID 34078272). Dedup: distinct from BVBRC-22 (*Arthrobacter* SRS-W-1-2016, uraniferous soil) — different strain + different biology. Not a tool/db paper. OA confirmed (PMC8171050).
3. Created target dir BVBRC-59-Arthrobacter-PAMC25564-coldadapt-Han2021 (next free after BVBRC-58).
4. Pulled OA full text XML from Europe PMC (165 KB). Extracted claims: genome length 4,170,970 bp; GC 66.74%; 3,829 genes (3,613 CDS, 147 pseudo, 15 rRNA, 51 tRNA); 108 CAZymes via dbCAN2 (33 GH, 45 GT, 23 CE, 5 AA, 2 CBM, 0 PL); glycogen/trehalose CAZyme families (GH1, GH13/GH13_11/GH13_26, GH65, GH77, CBM48).
5. Resolved focal accession CP039290.1 → assembly GCA_004798705.1 / GCF_004798705.1.
6. Downloaded genome FASTA. Computed length=4,170,970 (EXACT), GC=66.71% (Δ0.03 vs paper).
7. Datasets annotation: RefSeq re-annotation (2024) drifted (3,863/3,718/75). ORIGINAL GenBank annotation (2019-04-11) = EXACT match on all six primary counts (3,829/3,613/147/69 non-coding). Feature table: rRNA=15, tRNA=51 (EXACT).
8. Downloaded proteome (3,613 proteins — matches paper). Staged to uicgpu.
9. No conda/hmmer on uicgpu base; found antismash env with HMMER 3.4 + diamond + prodigal.
10. bcb.unl.edu dead (cyberattack); got dbCAN-HMMdb-V9 from pro.unl.edu (99 MB HMMER3). hmmpress OK.
11. hmmscan 3,613 proteins vs dbCAN-HMMdb-V9, 16 CPU (~4 min). Applied dbCAN canonical hmmscan-parser filter (E<1e-15 if aln>80aa else 1e-5; HMM coverage>0.35; overlap>0.5 resolution).
12. Result: 102 CAZyme proteins; GH 34, GT 43, CE 16, AA 5, CBM 9, PL 0. Total & GH/GT/AA/PL close to paper (108/33/45/5/0). CE/CBM shift attributable to dbCAN version (V9 vs V8) + HMMER-only vs dbCAN2 3-tool overview.
13. Confirmed ALL glycogen/trehalose signature families present: GH1, GH13 (7 subfamilies incl. GH13_11, GH13_26), GH65 (trehalose phosphorylase), GH77, CBM48. Matches paper Table 2.
14. Verified 6 comparator accessions resolve to real complete public genomes (comparative dataset real).
15. LLM judge (Argo gpt-5.2) scored claims vs results.
