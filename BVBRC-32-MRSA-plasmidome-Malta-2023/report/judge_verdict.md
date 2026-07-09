# LLM-Judge Verdict — BVBRC-32

**Judge model:** argo:gpt-5.2 (free Argo endpoint; opus-4.8 fell back due to 502 proxy error)

## Per-claim verdicts

**C1. Total isolates carrying plasmids** — **VERIFIED**  
Replication finds 85/88 genomes with ≥1 plasmid replicon (96.6%). While the denominator differs (paper 94 vs repl 88), within the BioProject subset the key qualitative point (“~90%+ carry plasmids; 3 are plasmid-free”) is reproduced, including exactly **3 plasmid-free** in the sequenced set.

**C2. Number of distinct replicase superfamily types detected** — **PARTIAL**  
All **7** superfamilies reported by the paper are detected, matching the central claim. However, replication also detects an additional type (Inc18), which could reflect database/version/threshold differences or classification differences. That doesn’t negate the paper’s claim, but it prevents a strict “exact match.”

**C3. Most common replicase type = RepL** — **VERIFIED**  
RepL is the most common in both, with very similar counts (paper 63 vs repl ~66–67 depending on locus/genome counting). Direction and dominance are reproduced.

**C4. 2nd/3rd most common types** — **PARTIAL**  
Replication confirms RepA_N and Rep_1 are high-frequency, but Rep_3 appears comparable or higher in the replication depending on whether counting loci or genomes. Because the paper’s specific rank ordering (RepA_N then Rep_1) is not cleanly reproduced under the replication’s counting scheme, this is only partial support. (This is also sensitive to the major methodological substitution: “plasmid molecules” vs “replicon loci/genome carriage.”)

**C5. Rarest types (Rep_2 n=2, PriCT_1 n=1)** — **VERIFIED**  
Exact match for these rare categories.

**C6. Dominant plasmid-borne resistance = RepL/ermC small plasmid in ~63 isolates** — **PARTIAL**  
Replication strongly supports the core idea that **erm(C)** is common and largely plasmid-associated and that **RepL** is the dominant small-plasmid type. But it does **not** reproduce the paper’s specific pairing/count (“ermC on a RepL plasmid in 63 isolates”): replication reports **erm(C) in 67 genomes** and does not explicitly demonstrate RepL–ermC co-localization on the same reconstructed plasmid (only “plasmid contig” association). Given the paper’s plasmid reconstruction/curation vs draft-contig inference, this is supportive but not a full reproduction of the exact claim.

**C7. 74% (140/189) of plasmids carry resistance genes** — **NOT-REPRODUCED**  
Replication cannot reproduce this quantitative claim because it (i) does not reconstruct/count plasmid molecules (paper: 189 plasmids), and (ii) screens only AMR genes (plus qac) while omitting the paper’s heavy-metal gene accounting that contributes to the “resistance gene” numerator. The replication’s ~47% figure is not directly comparable and is substantially lower; even as a “lower bound,” it does not verify the paper’s stated proportion.

**C8. Rare plasmid-borne AMR genes present (tetK/L, aadD, mupA, ermB, lnuB, cat, aacA-aphD)** — **VERIFIED**  
All listed genes are detected in the replication dataset, consistent with the paper’s qualitative claim that these occur on plasmids (though exact plasmid assignments are not reconstructed).

**C9. Biocide resistance qacA plasmids identified** — **VERIFIED**  
qacA/qacB detected in 5 genomes and located on plasmid contigs, supporting the claim that plasmids harbor qacA.

**C10. All isolates are MRSA (mecA+)** — **VERIFIED**  
mecA found in 88/88 genomes in the replication set.

---

## Overall verdict: **PARTIAL REPLICATION**

The replication robustly reproduces the paper’s central qualitative plasmidomic landscape findings (high plasmid carriage; presence of the same 7 rep superfamilies; RepL dominance; rare rep types; broad AMR gene repertoire; mecA in all isolates; qac genes on plasmid contigs). However, two key limitations prevent a “strong” replication:

1. **Major method substitution**: the paper’s curated **per-plasmid** reconstruction/counting (189 plasmids) is replaced by **replicon-locus/contig-based** inference, which affects claims about plasmid counts and plasmid-level gene carriage rates.
2. **C7 not reproduced** and **C6 only partially reproduced** due to lack of plasmid reconstruction and incomplete resistance-gene category matching (heavy-metal genes not systematically screened).

So the replication supports much of the landscape and frequency structure, but does not fully reproduce the paper’s plasmid-level quantitative conclusions.
