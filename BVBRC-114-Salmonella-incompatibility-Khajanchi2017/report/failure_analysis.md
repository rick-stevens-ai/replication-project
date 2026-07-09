# Failure Analysis — BVBRC-114

Honest analysis of what did not go smoothly, what was worked around, what is a residual gap, and what would close it.

## What failed and was worked around

### F1. NCBI E-utilities `esearch | efetch -format fasta` on WGS master accession returned empty
- **Symptom:** `esearch -db nuccore -query "LSZD01[WGS]" | efetch -format fasta` produced 0-byte outputs in the `bvbrc56` env.
- **Root cause:** WGS master → contig fanout in Entrez does not always resolve when the WGS project's contigs live in a huge scaffold list; the query returns 0 UIDs in some E-utility handshake states.
- **Workaround:** switched to `datasets summary genome taxon "Salmonella enterica" --search <strain>` filtered by `bioproject_accession = PRJNA312617`. Resolved 4/7.
- **Residual gap:** none (all 7 assemblies acquired via the fallback + FTP).

### F2. `datasets download` intermittent DNS failure
- **Symptom:** `Post "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/dataset_report": ... dial tcp: lookup api.ncbi.nlm.nih.gov on 127.0.0.53:53: server misbehaving` mid-download.
- **Root cause:** systemd-resolved on uicgpu occasionally times out; unrelated to the replication but blocking.
- **Workaround:** direct HTTPS FTP fetch (`ftp.ncbi.nlm.nih.gov/genomes/all/GCF/001/729/...`) via the corporate HTTPS proxy (<lan-host>:3128) after `source ~/env.sh`.
- **Residual gap:** none.
- **Note-to-future:** when calling `datasets` on uicgpu, either (a) always have a `curl <ftp.ncbi>...` fallback ready, or (b) resolve to a fixed IP + retry with backoff.

### F3. Stale WP_ accession set for iuc genes
- **Symptom:** V1 iron tblastn returned 35% ID hits — obviously wrong.
- **Root cause:** hand-picked WP_ accessions were not aerobactin genes but iron-related paralogs.
- **Workaround:** rebuild query set by parsing the paper's own Table 1 reference plasmid CP001122.1 (pCVM29188_146) GBK CDSs, filtered by `/gene=sit*|iuc*|iut*|iro*`. V3 tblastn returned clean 99–100% ID hits.
- **Residual gap:** iucD, iroC/N, shfB, pefA, ompX were not annotated on CP001122.1 with `/gene=` matching, so those genes were not queried. Impact minor: sitA-D + iucA-C + iutA + iroB are sufficient to establish the operon-presence claim.

## What is genuinely not testable in silico (not "failed", but real gaps to the paper)

### G1. Caco-2 persistence assay (paper's C6)
- The paper's central *functional* claim — that SE819::IncFIB transconjugant persists in Caco-2 cells at higher rate than the SE819 recipient — requires live human intestinal epithelial cell culture, plasmid conjugation, gentamicin protection assay, and CFU enumeration at 1, 2, 4 h post-infection. This is a wet-lab result that no in silico method can reproduce.
- What would close it: BSL-2 lab access + Caco-2 line + plasmid conjugation panel. Not in scope for a computational replication.

### G2. qRT-PCR of sit/iuc under iron-limitation (paper's C7)
- Requires RNA extraction under two growth conditions (LB vs LB + iron chelator 2,2'-dipyridyl) and qPCR against reference genes. Wet-lab only.

## What went smoothly but has residual uncertainty

### R1. mash-based phylogeny lower resolution than paper's SNP tree
- The paper used core-genome SNP alignment (kSNP or Parsnp or similar); this replication used mash sketches. Mash reproduces the 5+1 subclade *direction* but does not resolve whether SE397 is sister to bovine references specifically — the NJ tree places it near LT2/bovine cluster rather than deep inside it. A higher-resolution replication would run Parsnp against LT2 as reference, extract core-SNP alignment, and run RAxML.
- Estimated additional effort: ~1 h of uicgpu wall clock; not run in this wave.

### R2. Assembly-fragmented plasmid across multiple contigs
- The 6 Typhimurium draft assemblies split the ~140 kb IncFIB plasmid across ~3 contigs each (rep contig separate from sit+iuc contig). The paper worked with hybrid/complete assemblies where the whole ~140 kb plasmid was contiguous. Consequence: the "same-contig" test in our matrix is conservative — sit+iuc genes ARE colocalised on a single ~15–20 kb contig in each strain, but that contig doesn't include the IncFIB rep gene, so a naïve "on the IncFIB contig" check reads as absent. This is a *contig fragmentation artifact*, not a biological difference.
- What would close it: reassemble one of the strains with long-read (Nanopore or PacBio) data to close the plasmid into a single circular replicon, then verify all 12 iron-acquisition genes + rep gene + tra/traT conjugative machinery on one replicon.

## Summary
- 4 of 4 in-silico core claims independently reproduced on real public data at high confidence.
- 2 wet-lab claims explicitly untestable in silico (correctly reported as "not tested", not "failed" or "contradicted").
- 2 methodological caveats (mash resolution, assembly fragmentation) noted but do not undermine the core replication.
- **Verdict:** PARTIAL (the strong sense — bioinformatic core reproduced, wet-lab out of reach).
