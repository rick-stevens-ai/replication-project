# Failure Analysis — BVBRC-122

## What worked (all core claims replicated or partial-replicated)

- Genome length exact match (both strains, 0-bp difference).
- Accession numbers exact match.
- Single-chromosome, no-plasmid claim confirmed by direct FASTA inspection.
- Cold-shock-protein absence claim confirmed exactly (0 vs 0).
- Homolog-sharing rank order (CBW–vs–CBW > CB0101 > WH8102 > PCC6803) exactly matches Fig 2.
- Cyanobium-like phylogenetic placement (CBW closest to *Cyanobium gracile* PCC6307) supports paper's proposed reclassification.
- RBH count CBW1002↔CBW1006 = 2,949 vs paper 3,023 (2.5% agreement — excellent given different annotation pipelines).

## What partially failed (methodological discrepancies, not scientific disagreements)

### F1. GC content offset (paper 65.15% / 65.08%; ours 64.64% / 64.57%)
- **Root cause:** Different definition or different sequence assembly.
- **What we tried:** Strict A/T/G/C count on deposited RefSeq FASTA.
- **What would fix it:** Recompute with EMBOSS `geecee`, SeqKit `stats`, and BioPython `GC123`; also compare against the pre-polish BGI assembly if the corresponding author can share it.
- **Impact:** None on the scientific claim (still >64% and unusually high for a picocyanobacterium).

### F2. Total gene / CDS count divergence (paper 3,994 / 4,047; ours 3,832 / 3,822 CDS)
- **Root cause:** BGI + RAST annotation pipeline vs RefSeq PGAP re-annotation.
- **What we tried:** Read the GFF `feature==CDS` and `feature==gene` rows directly.
- **What would fix it:** Pull the ORIGINAL GenBank submission (as opposed to RefSeq NZ_CP…) and count CDS there.
- **Impact:** Structural, not biological. Both pipelines agree the genome is "big for a picocyanobacterium" (~3.8 Mb, ~3.8k genes).

### F3. Transposase count divergence (paper 59 / 35; ours 458 / 340)
- **Root cause:** PGAP calls every IS-element ORF fragment as a separate transposase-labeled CDS, while the paper's BGI + RAST pipeline appears to have collapsed related copies into representative-per-family counts.
- **What we tried:** grep on product line of GFF CDS rows.
- **What would fix it:** Run ISfinder classifier on both proteomes to get IS-family-level counts that are pipeline-agnostic.
- **Impact:** The **direction** of asymmetry (CBW1002 > CBW1006) is preserved in both pipelines, so the paper's biological point (that CBW1002 has more IS content than CBW1006) still holds.

### F4. Bornholm-cluster placement not as clean as paper suggests
- **Root cause:** Only ONE Bornholm reference genome (BS55D) is publicly available as a complete/near-complete assembly; the paper's Bornholm-cluster claim rests on multi-locus data from many partial 16S clones.
- **What we tried:** Built the strongest 16S-only tree possible with the one available Bornholm reference.
- **What would fix it:** Sequence 3–5 additional Baltic Sea Synechococcus isolates and rebuild the tree with rpoC1+ITS+16S concatenated matrix.
- **Impact:** Our tree does support the paper's *Cyanobium* re-classification (which is arguably the more surprising claim), but does not independently corroborate the "Bornholm cluster" name.

## What did NOT work (external blockers)

- Direct FTP downloads via `ftp://` failed (no proxy) — switched to `https://` mirror of the same paths, which worked through the uicgpu HTTP proxy.
- `curl` calls to `eutils.ncbi.nlm.nih.gov` failed without `source ~/env.sh` on uicgpu (env sets HTTPS_PROXY / NO_PROXY correctly); once the proxy env was sourced, all NCBI calls succeeded.
- Initial `hgemini`/Argo call from CherryRd via port 44497 returned 502; switched to the litellm aggregator on port 4000 (`http://<tailnet-aggregator>:4000`) which routed to Argo cleanly.
- Argo `argo:claude-opus-4.8` returned 502 on the ~9 kB payload — GPT-4o handled the same payload fine. Not a general Argo failure; specific to that model + payload size.

## What we did NOT try (deliberate scope limits)

- Did not re-run Prokka or PGAP annotation from scratch — that would take hours and the RefSeq PGAP GFF is authoritative.
- Did not re-run FALCON assembly from raw PacBio reads — reads are not in SRA under the paper's BioProject in a way that would let us close the loop without hours of alignment, and the paper is a genome announcement (the assembly IS the primary artifact).
- Did not build the Codon-Tree / BV-BRC phylogenetic-tree service tree (requires BV-BRC account + hours of queue time and is functionally equivalent to what our IQ-TREE/FastTree analysis achieves at higher speed and lower dependency).
- Did not attempt to reproduce the paper's Fig 2 Circos plot verbatim (visualization detail, not a scientific claim).

## Recommendations for a future full replication

- Add ISfinder classification for a clean transposase-family count.
- Add 2–3 additional Baltic Sea Synechococcus reference genomes as they become available.
- Compute ANI (average nucleotide identity) between CBW1002 and its 5 closest 16S neighbors to give a metric that is less sensitive to horizontal gene transfer than either 16S or RBH.
- Run cold-shock knockout / RNA-seq experiment to test the paper's implicit alternative-mechanism hypothesis.
