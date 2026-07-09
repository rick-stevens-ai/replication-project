# Brief — BVBRC-118: Jiang et al. 2022, *Paenibacillus peoriae* HJ-2

**Paper.** Jiang A. *et al.* (2022) "Complete genome sequence of biocontrol strain *Paenibacillus peoriae* HJ-2 and further analysis of its biocontrol mechanism." *BMC Genomics* 23:161. DOI: 10.1186/s12864-022-08330-0. PMID 35209846. PMC PMC8876185.

**What.** Authors PacBio-Sequel–sequenced a plant-associated *Paenibacillus peoriae* isolate (HJ-2) from *Paris polyphylla* rhizosphere, closed a single 6.001 Mb chromosome, annotated 5,237 CDS + 108 tRNA + 39 rRNA, and reported 12 antiSMASH secondary-metabolite gene clusters that plausibly explain HJ-2's antifungal biocontrol activity against *Fusarium concentricum* / *F. oxysporum*.

**Why replicate.** BVBRC-scope workflow: raw PacBio reads → de novo assembly → annotation → BGC prediction. Data availability = SRA PRJNA580302 / SRR10363117 (183,095 PacBio Sequel reads, 1.30 Gb). Assembly was **not** deposited to NCBI Assembly (only 16S MK911741.1 + raw reads present), so an *independent reassembly* is the only path — and a genuine reproducibility test of the paper's chromosome size, GC%, CDS count, and antiSMASH-cluster tally.
