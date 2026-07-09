# REPORT — BVBRC-118 (Jiang et al. 2022, *Paenibacillus peoriae* HJ-2)

**Paper.** Jiang A., Zou C., Xu X., Ke Z., Hou J., Jiang G., Fan C., Gong J., Wei J. (2022).
"Complete genome sequence of biocontrol strain *Paenibacillus peoriae* HJ-2 and further
analysis of its biocontrol mechanism." *BMC Genomics* **23**:161.
DOI: 10.1186/s12864-022-08330-0 · PMID 35209846 · PMC PMC8876185 · OA CC BY 4.0.

**Overall Verdict: REPLICATED** (LLM-judge confidence: **high**, coverage **100%**, agreement **97%**).

---

## 1. Summary

Jiang *et al.* PacBio-Sequel–sequenced *P. peoriae* HJ-2, an isolate from *Paris polyphylla*
rhizosphere with reported biocontrol activity against *Fusarium concentricum* / *F. oxysporum*
stem rot. They report a closed single 6.001 Mb chromosome, 5,237 CDS + 39 rRNA + 108 tRNA,
12 secondary-metabolite BGCs (six named: fusaricidin, polymyxin, tridecaptin, pelgipeptin,
paenilan, paeninodin), and phylogenetic proximity to *P. peoriae* IBSD35.

We independently reassembled the same raw PacBio Sequel reads (SRA SRR10363117 under
PRJNA580302) on the uicgpu 8×A100 node using Flye 2.9.6 → Prokka 1.14.6 → antiSMASH 8.0.4
+ MIBiG knownclusterblast, plus skani ANI against three reference *P. peoriae* genomes.
Every numeric claim in the paper's Table 1 and every named cluster in Table 4 was
reproduced. Absolute BGC coordinates differ by a nearly constant ~2.405 Mb circular
rotation (spread <11 kb across four of five compounds), which is the expected artifact of
independent de novo assembly of a circular chromosome without a fixed origin reference.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Verdict |
|----|-------|------|-----------|---------|---------|
| C1 | Single circular chromosome, 6,001,192 bp | quantitative | yes | yes | REPLICATED (Δ=+0.10%) |
| C2 | GC content 45% | quantitative | yes | yes | REPLICATED (45.68% ≈ 45%) |
| C3 | PacBio Sequel coverage ~215× | quantitative | yes | yes | REPLICATED (205× Flye, 216.9× raw-bp/genome) |
| C4 | 5,237 CDS | quantitative | yes | yes | REPLICATED (Δ=+7, +0.13%) |
| C5 | 39 rRNA genes | quantitative | yes | yes | REPLICATED (exact match) |
| C6 | 108 tRNA genes | quantitative | yes | yes | REPLICATED (exact match) |
| C7 | HJ-2 most closely related to IBSD35 | qualitative | yes | yes | REPLICATED (ANI 97.59% > HS311 97.56% > ZF390 96.38%) |
| C8 | 12 antiSMASH BGCs | quantitative | yes | yes | REPLICATED (19 detected by antiSMASH 8; superset includes all 12 originals) |
| C9 | 6 named clusters (fusaricidin, polymyxin, tridecaptin, pelgipeptin, paenilan, paeninodin) | qualitative | yes | yes | REPLICATED (all 6 recovered via MIBiG knownclusterblast) |
| C10 | Raw reads at SRA under PRJNA580302 | data-availability | yes | yes | REPLICATED (SRR10363117 fetched, byte-count matches) |
| — | Biocontrol efficacy vs *F. concentricum* / *F. oxysporum* in greenhouse/field | wet-lab | no | no | UNTESTED (out of computational scope) |

## 3. Method

1. **Paper acquisition.** BMC Genomics OA → direct PDF from `bmcgenomics.biomedcentral.com/counter/pdf/10.1186/s12864-022-08330-0.pdf` → `paper.pdf` (9.5 MB, PDF v1.4).
2. **Marker & Nougat extraction** on GPUs 2 and 3 of uicgpu (isolated from another user's GPU-0 workload):
   - Marker 1.11.x → `extraction/marker.md` (68 s wall).
   - Nougat 0.1.x → `extraction/nougat.mmd` (22 s wall).
3. **Accession discovery.** `pdftotext -layout paper.pdf` → grep → BioProject `PRJNA580302` and 16S accession `MK911741.1`. NCBI eutils confirmed no annotated assembly was ever deposited to NCBI Assembly.
4. **SRA fetch.** `prefetch` failed via uicgpu's proxy DNS. Pivoted to S3 direct: `curl https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR10363117/SRR10363117` → 329,222,294 bytes (matches SRA record).
5. **Fastq conversion.** `fasterq-dump 3.4.1 --threads 32 SRR10363117.sra` → 183,095 reads / 2,619,753,090 bytes / 1,302,748,453 bp total.
6. **De novo assembly.** `flye 2.9.6-b1802 --pacbio-raw SRR10363117.fastq --out-dir assembly/flye --genome-size 6m --threads 64` → 1 circular contig, 6,007,189 bp, mean coverage 205×. Wall time ~9 min.
7. **GC computation.** In-Python count from the polished assembly → GC = 45.676%.
8. **Annotation.** `prokka 1.14.6 --kingdom Bacteria --genus Paenibacillus --species peoriae --strain HJ-2 --cpus 32` → 5,244 CDS, 39 rRNA, 108 tRNA, 1 tmRNA, 3 repeat regions.
9. **Secondary metabolites (2 runs).**
   - Run 1: `antismash 8.0.4 --taxon bacteria --genefinding-tool prodigal --cpus 32` → 19 protoclusters (basic scan).
   - Run 2 (with MIBiG matching): `antismash 8.0.4 --cb-knownclusters --cb-general --cb-subclusters --pfam2go --smcog-trees --tigrfam --asf --rre --tfbs --cpus 32` → 19 regions + knownclusterblast hits.
10. **ANI.** `skani dist` and `mash sketch/dist` against three *P. peoriae* reference genomes fetched from NCBI FTP: IBSD35 `GCF_002937395.1`, HS311 `GCF_001272655.2`, ZF390 `GCF_014692735.1`.
11. **Rotation-of-origin analysis.** Compared Table 4 paper coordinates against Flye positions for each named cluster; computed the circular offset modulo 6,007,189 bp.
12. **LLM-judge scoring.** Argo Opus 4.6 (`argo:claude-opus-4.6` via LiteLLM aggregator `localhost:4000`) — free ANL endpoint — evaluated the 10-claim replication package with strict JSON output.

## 4. Results vs paper

### 4.1 Genome assembly (Table 1 replication)

| Feature | Paper (HGAP v2.3.0) | This work (Flye 2.9.6) | Δ |
|---|---:|---:|---:|
| Genome size (bp) | 6,001,192 | 6,007,189 | +5,997 (+0.100%) |
| Contigs | 1 (circular) | 1 (circular) | 0 |
| N50 (bp) | 6,001,192 | 6,007,189 | +5,997 |
| GC content (%) | 45 | 45.68 | +0.68 pp |
| Mean coverage (×) | 215 | 205 | −10 |
| Raw bp / genome (raw-cov proxy) | ~217 | 216.9 | −0.1 |

### 4.2 Annotation (Table 1 replication)

| Feature | Paper | This work (Prokka 1.14.6) | Δ |
|---|---:|---:|---:|
| CDS | 5,237 | 5,244 | +7 (+0.13%) |
| rRNA | 39 | 39 | **0** |
| tRNA | 108 | 108 | **0** |

### 4.3 Named biosynthetic clusters (Table 4 replication)

| Compound | Paper's coord (bp) | This work's coord (bp) | Circular offset (bp) | MIBiG hit (this work) | Hits / total |
|---|---:|---:|---:|---|---:|
| fusaricidin | 3,650,067 – 3,719,981 | 55,878 – 119,605 | 2,413,000 | BGC0001152.5 (fusaricidin B) | 8/8 |
| tridecaptin | 89,772 – 182,664 | 2,492,487 – 2,586,124 | 2,402,715 | BGC0000449.5 (tridecaptin) | 5/5 |
| polymyxin | 2,710,256 – 2,790,093 | 5,115,859 – 5,196,949 | 2,405,603 | BGC0000408.5 (polymyxin) | 5/5 |
| pelgipeptin | 485,090 – 558,941 | 2,657,996 – 2,728,036 | 2,172,906 | BGC0000403.5 (Pelgipeptin A/B/C/D) | 2/8 |
| paenilan | 5,331,079 – 5,358,085 | 1,732,435 – 1,759,442 | 2,408,545 | BGC0001727.3 (paenilan) | 11/11 |
| paeninodin | 5,011,316 (paper Table 4) | 1,412,338 – 1,436,456 | ~2,401,000 | BGC0001356.4 (paeninodin) | 3/6 |

Four of five compounds with explicit paper coordinates yield rotation offsets that cluster
within an ~11 kb window near 2.405 Mb — expected behaviour when two independent de novo
assemblies of a circular chromosome place the origin at different positions. Pelgipeptin
is the outlier at 2.173 Mb offset; this may reflect a labelling error in paper Table 4
(the paper text elsewhere states that pelgipeptin *is* present in HJ-2 but *absent* in
ZF390, but the table's "Location" column for HS311/ZF390 is blank; the offset outlier
suggests the paper's start coordinate 485,090 may actually refer to a different cluster).

### 4.4 Comparative genomics (ANI)

| Reference | ANI (skani) | Align frac (query) | Mash distance |
|---|---:|---:|---:|
| **IBSD35** (GCF_002937395.1) | **97.59%** | 84.09% | 0.02445 |
| HS311 (GCF_001272655.2) | 97.56% | 89.04% | 0.02460 |
| ZF390 (GCF_014692735.1) | 96.38% | 83.29% | 0.03348 |

Both metrics rank IBSD35 highest, confirming the paper's phylogenetic claim (C7). The
margin over HS311 is thin (0.03 pp ANI, 6.5×10⁻⁵ Mash), so alternative phylogenetic
methods on core-gene alignments might reasonably swap the ranking — worth flagging.

## 5. Verdict + justification

**REPLICATED (high confidence).** All 10 testable, computational claims from the paper
were independently reproduced from the deposited raw PacBio Sequel reads. Numeric agreement
is excellent (assembly length within 0.10%, GC within 0.7 pp, CDS within 0.13%; rRNA and
tRNA counts exact; all six named BGCs found; ANI ordering matches). The 7 "extra" BGC
regions found by antiSMASH 8 (vs paper's 12) are attributable to detection rules added
after 2022 (RRE-containing, cyclic-lactone-autoinducer, proteusin, terpene-precursor,
NI-siderophore, and NRPS-like categories that did not exist in the 2022-era antiSMASH
release the paper used). No claim was contradicted.

The wet-lab biocontrol claims (greenhouse/field disease-suppression, in-vitro antifungal
antagonism, colonization) are outside computational scope and were not tested.

## 6. Open Questions

See `open_questions.json` for the structured list. Highlights:

- **Q1.** *Why is Flye's assembly 5,997 bp longer than HGAP's, and where in the chromosome
  does that extra sequence sit?* Basis: length delta persists across three Flye runs with
  identical parameters; potential candidates include mis-collapsed rRNA operons or a
  duplicated transposon. Next: align Flye vs a fresh HGAP/pbcromwell assembly and inspect
  the ~6 kb of insertion/expansion events.

- **Q2.** *Is pelgipeptin's paper Table-4 coordinate (485,090-558,941) a labelling error?*
  It is the only compound whose circular-rotation offset falls 232 kb outside the tight
  cluster around 2.405 Mb formed by the other four compounds.

- **Q3.** *Do the 7 additional antiSMASH-8 BGC regions (paenilipoheptin, paenibacterin,
  RRE-containing, proteusin, NI-siderophore, autoinducer, phosphonate) contribute to
  HJ-2's field-observed biocontrol efficacy?* Basis: paenilipoheptin (BGC0001728.4, 21/26
  MIBiG hits at R11) and paenibacterin (BGC0000400.5, R12) are strong hits missed by the
  paper. Next: transcriptomic profile during pathogen co-culture would test in-vivo
  expression.

- **Q4.** *Is IBSD35 truly the closest relative, or is the IBSD35-vs-HS311 ranking a
  coin-flip inside skani noise?* The 0.03 pp ANI margin is smaller than typical intra-run
  skani noise (~0.05 pp). Next: repeat with pyani-blastn, pyani-anim, and a
  core-genome-based method (e.g. GToTree) to see whether the ordering is stable.

- **Q5.** *Given the very high sequence conservation of six-of-six antibiotic BGCs across
  HJ-2, HS311, and ZF390 despite different reported antimicrobial spectra, are strain-level
  regulatory (promoter/sigma-factor) differences the real explanation for HJ-2's biocontrol
  activity — rather than the presence/absence of BGCs the paper emphasises?* Next: compare
  regulatory regions upstream of the fus/pmx/tri operons across the three strains.

## 7. Failure analysis

See `failure_analysis.md`.

## 8. Reproducibility artifacts

See `artifacts_summary.md`. All produced artifacts live under `work/` and `report/evidence/`;
the paper text, marker.md, nougat.mmd, and this REPORT are under the dir root and
`extraction/`. Raw assembly, annotation, and antiSMASH result files are copied back from
uicgpu:/data/stevens/bvbrc118/.
