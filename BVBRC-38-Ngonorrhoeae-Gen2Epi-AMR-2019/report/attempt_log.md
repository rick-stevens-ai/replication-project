# Attempt Log — BVBRC-38 (Gen2Epi), 2026-07-01

Chronological log of the independent replication.

1. **Dedup + brief.** `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "gonorrhoeae|gen2epi|neisseria"` → no existing dir. Read WAVE_BRIEF + BVBRC-17 exemplar REPORT.md.

2. **Paper located (OA).** Europe PMC search → Gen2Epi = PMC6398234 / PMID 30832565 / DOI 10.1186/s12864-019-5542-3, BMC Genomics 2019, OA=Y. Pulled full text XML (`gen2epi_fulltext.xml`, 116 KB). Extracted abstract, all Methods steps, Tables 1–3, and data-availability section.

3. **Claims identified.** C1 assemble reads→full scaffolds (Table 1 stats); C2 auto NG-MLST/NG-MAST typing (Table 2); C3 auto NG-STAR AMR-determinant detection. Data used: 1484 samples across 4 studies; the **WHO 2016 reference panel** (11 strains F,G,K,L,M,N,O,P,X,Y,Z, ref 17 = Unemo 2016) has finished public genomes → chosen as the tractable replication target.

4. **Genome download.** Mapped the 11 WHO strains to PRJEB14020 assembly accessions via ENA `result=assembly`. NCBI Datasets REST returned only README (no FASTA staged for these GCAs); fell back to **ENA browser FASTA API** (`/ena/browser/api/fasta/<GCA>`) — worked. Also pulled FA1090 reference (GCA/GCF_000006845.1) + annotation (CDS/protein/GFF via NCBI Datasets). `fetch_genomes.py`.
   - zsh assoc-array + word-split bugs cost two iterations; rewrote as a Python downloader.

5. **NG-MLST typing (C2).** Downloaded 7 housekeeping-locus allele FASTAs (1036–1397 alleles each) + the 18,488-row ST profile table from pubMLST. `mlst_typing.py`: makeblastdb per genome, blastn allele sets, pick exact (100%id/100%len) allele per locus, map 7-allele vector → ST. All 11 strains typed with full 7/7 profiles (e.g. WHO_Y=ST1901, WHO_K/X/Z=ST7363, WHO_F=ST10934).

6. **AMR determinant detection (C3).** pubMLST NG-STAR alleles downloadable for mtrR/porB/ponA/gyrA/parC/23S but NOT penA (curated in separate NG-STAR DB) and no NG-STAR profile CSV. Decision: do **direct resistance-mutation detection** (the biological substance of the AMR claim) using FA1090 reference genes as BLAST queries. `extract_refgenes.py` pulled penA(PBP2/FtsI)/gyrA/parC/ponA(PBP1)/mtrR/porB from FA1090 CDS + 23S rRNA from genome coords. `amr_detect.py`: blastn ref gene → genome, extract best-hit region, translate, read canonical codons.
   - **Bug + fix:** WHO_F penA showed 220 aa diffs but 99.66% nt id — a 1-bp indel frameshift inflated the protein-diff count. Switched the penA mosaic call to **nucleotide identity** (<96% = mosaic), which cleanly separates mosaic (K,X,Y,Z ~87–88%) from non-mosaic (99%+). Added a BLOSUM62 global protein alignment to map penA codon positions robustly around indels.

7. **23S rRNA copies.** `rrna23S_azithro.py`: blastn 23S ref → each genome, count full-length copies. All 11 genomes → **4 copies** (correct for N. gonorrhoeae's 4 rRNA operons).

8. **Assembly stats (C1, part 1).** `genome_stats.py`: contigs/length/GC/N50 per WHO genome. Median longest 2,172,826 bp, GC 52.52% — matches Table 1 WHO column (2,167,463 / 52.64%).

9. **Ground-truth validation.** Fetched Unemo 2016 (PMC5079299) Table 1 phenotypes (web_fetch, no paid tools). Confirmed: WHO_F pan-susceptible (→ our wt penA, no QRDR); WHO_X(H041)/Y(F89)/Z(A8806) ceftriaxone-resistant (→ our mosaic penA). Biology validated.

10. **LLM judge #1 (free Argo gpt-5.2).** Verdict PARTIAL (cov 6/10, agr 8/10): flagged that raw-read assembly wasn't independently rerun and mtrR/porB weren't shown.

11. **End-to-end de-novo assembly (C1, part 2).** Local SPAdes broke (Py3.14 distutils) + no trimmer. Moved to **uicgpu** (per brief). Created conda env `/data/stevens/envs/bvbrc38` (spades 4.3.0, fastp 1.3.6, blast 2.17) — first attempt failed on DNS (needed `source ~/env.sh` for the <lan-host>:3128 proxy), succeeded on retry. Downloaded WHO_F Illumina reads **ERR5860304** (1.31M pairs) from ENA. Ran fastp Q15 → SPAdes `--careful -k 21,33,55,77,99,127` (paper's params). Result: 2,197,379 bp, GC 52.30%, **99.96% genome fraction vs WHO_F ref**.

12. **Closed the Gen2Epi loop.** `denovo_type_amr.py`: NG-MLST + penA on the de-novo assembly → **ST 10934 + non-mosaic penA, identical to the finished WHO_F reference**. Raw reads → assembly → correct typing+AMR linkage.

13. **LLM judge #2 (free Argo gpt-5.2).** With end-to-end assembly + all-7-loci AMR added: **Verdict REPLICATED (cov 8/10, agr 9/10)**. Only Ragout scaffolding + panel-wide QUAST misassembly metrics not reproduced.

14. **Report written.** Conservative canonical verdict recorded as PARTIAL (strong / near-REPLICATED) given single-strain assembly scope; judge's REPLICATED opinion noted.

**Endpoint discipline:** No `pdf`/`image` paid tools. Full text via Europe PMC XML + web_fetch. LLM judge via free Argo (gpt-5.2). No overwrite of sibling dirs.
