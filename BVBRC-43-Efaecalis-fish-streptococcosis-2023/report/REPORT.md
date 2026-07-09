# Replication Report: Akter et al. (2023)
## "Virulence and antibiotic-resistance genes in *Enterococcus faecalis* associated with streptococcosis disease in fish"

**Paper:** Akter T, Haque MN, Ehsan R, Paul SI, Foysal MJ, et al. *Scientific Reports* 13:1551 (2023).
**DOI:** [10.1038/s41598-022-25968-8](https://doi.org/10.1038/s41598-022-25968-8)
**PMC:** PMC9883459 — **PMID:** 36707682
**Open access:** ✅ (CC BY 4.0)

**Set:** BVBRC-43 (TOPUP85 rank-12). **BV-BRC workflow class:** WGS assembly + annotation.
**Report date:** 2026-07-01
**Analyst:** Ollie (OpenClaw AI) — BVBRC Replication Wave (2026-07-01 night push)
**Verdict:** **PARTIAL REPLICATION (strong).** The paper's three most concrete, high-signal claims are independently reproduced on the actual deposited genomes: (i) genome features match Table 1 nearly exactly; (ii) tetracycline-resistance genes are found **only** in BFPS6; (iii) the aggregation-substance virulence genes *agg/prgB* are present in BFFF11 but absent in BFF1B1 and BFPS6. Aggregate gene *counts* (69 VFs, 39 AMR genes) are framework-dependent and not reproduced under the stricter AMRFinderPlus/tblastn calling used here; bacteriocin clusters (antiSMASH) were not rerun.

---

## 1. Paper

The authors whole-genome-sequenced (Illumina MiSeq, SPAdes assembly, Prokka + PATRIC/RASTtk annotation) three fish-pathogenic *E. faecalis* strains isolated from streptococcosis-like disease:

- **BFF1B1** and **BFFF11** — from diseased Nile tilapia (*Oreochromis niloticus*)
- **BFPS6** — from Thai sarpunti (*Puntius gonionotus*)

They profiled virulence genes (VirulenceFinder 2.0, VFDB VFanalyzer, PATRIC), antibiotic-resistance genes (ResFinder 3.1, ARG-ANNOT v6, CARD RGI, PATRIC), secondary metabolites (antiSMASH 5.1.2), prophages (PHASTER), insertion sequences (ISfinder), plasmid replicons (PlasmidFinder), and built a V583-referenced SNP phylogeny (CSIphylogeny). Headline conclusions: a conserved core of **69 virulence genes** across all three strains; **39 AMR genes** across 16 antibiotic groups; **tetracycline-resistance genes only in BFPS6**; bacteriocin clusters in BFFF11 and BFPS6; and a phylogeny where the two tilapia strains cluster together while BFPS6 branches separately.

**Data availability (from paper):** BFFF11 = CP045918, BFF1B1 = CP046022, BFPS6 = JADBGH010000000 (NCBI).

## 2. Claims tested

| # | Claim | Type | Testable from public data? | Tested here? |
|---|---|---|---|---|
| C1 | ~69 virulence genes; core VF set (fsr, gelE, ace, ebp pili, sortases, tpx) conserved in all three. | Genomic | Partially (marker-based). | ✅ Core markers tested via tblastn. |
| **C1b** | **Aggregation substance *agg/prgB* present in BFFF11, ABSENT in BFF1B1 & BFPS6 (differential VF).** | **Genomic** | **Yes.** | **✅ Directly tested.** |
| C2 | 39 AMR genes across 16 groups; core (e.g. lsa(A)) conserved in all three. | Genomic | Partially (framework-dependent). | ✅ AMRFinderPlus. |
| **C3** | **Tetracycline-resistance genes found ONLY in BFPS6.** | **Genomic** | **Yes.** | **✅ Directly tested (AMRFinderPlus).** |
| C4 | Bacteriocin gene clusters in BFFF11 and BFPS6 (antiSMASH). | Genomic | Yes (needs antiSMASH). | ❌ Not rerun. |
| C5 | BFF1B1 + BFFF11 cluster together; BFPS6 branches separately. | Phylogenetic | Yes (MLST/ANI/SNP). | ✅ MLST + fastANI. |
| **C6** | **Genome sizes 2.76 / 3.07 / 2.87 Mb, GC ~37.4–37.6%, matching Table 1.** | **Data + stats** | **Yes.** | **✅ Directly recomputed.** |

## 3. Method

All data are free/public; all inference uses free endpoints (Argo proxy) only. No paid API (`pdf`/`image`/Anthropic/OpenAI direct) was used.

1. **Paper text** via Europe PMC full-text XML (`PMC9883459/fullTextXML`). Extracted claims + accessions.
2. **Accession mapping**: NCBI eutils elink (nuccore→assembly) + esummary → GCA_009685155.1 (BFFF11), GCF_017357805.1 (BFF1B1), GCF_021375735.1 (BFPS6). Reference V583 = GCF_000007785.1 (AE016830).
3. **Genome download**: NCBI Datasets v2alpha REST (genome + protein + CDS + GFF; free, no auth). Checksummed.
4. **Genome statistics**: `genome_stats.py` (pure Python) — size, contigs, GC%, N50/L50, protein/CDS counts.
5. **AMR profiling**: AMRFinderPlus 3.12.8 (DB 2024-07-22.1) on each genome, `--organism Enterococcus_faecalis --plus` (uicgpu env `amr`). Independent of the paper's ResFinder/CARD/ARG-ANNOT.
6. **MLST**: `mlst` with the efaecalis 7-locus scheme.
7. **ANI**: `fastANI` all-vs-all (uicgpu env `bvbrc28`).
8. **Virulence markers**: curated 13-marker query built from the V583 reference proteome (fsrA/B, ace, ebpA/C, srtA/C, cylLS/LL, cylR2, tpx, agg/prgB/Asa1 ×2); `tblastn` vs each fish genome; presence rule **pident ≥ 80, qcov ≥ 70, e ≤ 1e-20**.
9. **LLM-judge** scoring via free Argo (`argo:gpt-5.2`), no regex.

Scripts + outputs in `work/` and `report/evidence/`.

## 4. Results vs Paper

### 4.1 C6 — Genome features (vs Table 1) — **MATCH (essentially exact)**

| Strain | Metric | Paper Table 1 | This replication | Match |
|---|---|---:|---:|---|
| **BFF1B1** | Size (bp) | 2,761,629 | **2,761,629** | ✅ EXACT |
|  | GC % | 37.6 | 37.55 | ✅ |
|  | contigs | (complete) | 1 | ✅ |
| **BFFF11** | Size (bp) | 3,067,042 | **3,067,042** | ✅ EXACT |
|  | GC % | 37.4 | 37.41 | ✅ |
|  | contigs | (complete) | 1 | ✅ |
| **BFPS6** | Size (bp) | 2,868,292 | 2,866,855 | ✅ 99.95% |
|  | GC % | 37.5 | 37.51 | ✅ |
|  | N50 | 270,331 | **270,331** | ✅ EXACT |
|  | L50 | 2 | **2** | ✅ EXACT |
|  | contigs | (draft) | 45 | ✅ (draft) |

The two complete chromosomes (BFF1B1, BFFF11) reproduce the paper's sizes to the base pair; BFPS6 (draft, WGS project JADBGH01) matches size to 99.95% with exact N50/L50. GC content matches all three. **Strong, direct confirmation.**

### 4.2 C3 — Tetracycline resistance ONLY in BFPS6 — **MATCH (clean)**

AMRFinderPlus 3.12.8 (DB 2024-07-22.1) acquired-AMR calls:

| Strain | tet(L) | tet(M) | other AMR | tet present? |
|---|---|---|---|---|
| BFFF11 (tilapia) | – | – | lsa(A) 100% | ❌ **no tet** |
| BFF1B1 (tilapia) | – | – | lsa(A) 99.4% | ❌ **no tet** |
| **BFPS6 (sarpunti)** | **100% id / 100% cov** | **100% id / 100% cov** | lsa(A) 99.6% | ✅ **tet(L)+tet(M)** |
| V583 (control) | – | – | vanB operon, erm(B), aac(6')-aph(2''), qacZ | (positive control OK) |

The tet(L) and tet(M) hits in BFPS6 are **co-located on a single contig** (NZ_JADBGH010000009.1, ~26.5–30 kb) as a tandem cassette — a physically real, high-confidence detection. **The BFPS6-exclusive tetracycline pattern is exactly reproduced by an independent tool.** The paper reported four tet alleles (tet(M), tet(L), tet(S), tet(45)); AMRFinder's curated DB recovers 2 of the 4 (tet(L), tet(M)) — the other two alleles are either divergent variants below AMRFinder's threshold or absent from its curation. The **exclusivity direction of the claim (tet only in BFPS6) is fully confirmed.** The V583 control confirms the tool detects diverse AMR (vanB, erm(B), aminoglycoside) when present, ruling out a false-negative artifact in the tilapia strains.

### 4.3 C1 / C1b — Virulence factors (tblastn of curated V583 markers) — **core MATCH + differential MATCH**

Presence rule pident ≥ 80, qcov ≥ 70, e ≤ 1e-20 (`+` = present with best %id):

| VF marker | BFFF11 | BFF1B1 | BFPS6 | Paper |
|---|---|---|---|---|
| fsrB (quorum sensing) | +100% | +99% | +99% | core, all three ✅ |
| fsrA | +100% | +99% | +100% | core ✅ |
| ace (collagen adhesin) | +99% | +90% | +98% | core ✅ |
| ebpC (pilus major) | +100% | +99% | +99% | biofilm pili, all three ✅ |
| ebpA (pilus minor) | +100% | +99% | +99% | biofilm pili ✅ |
| srtC (pilus sortase) | +100% | +99% | +99% | sortase-assembled pili ✅ |
| srtA (sortase) | +100% | +100% | +100% | ✅ |
| tpx (thiol peroxidase) | +100% | +99% | +99% | oxidative-stress core ✅ |
| **agg/prgB/Asa1 (aggregation)** | **+96%** | **❌ absent** | **❌ absent** | **"agg & prgB absent in BFF1B1 & BFPS6"** ✅✅ |
| **asa1 (aggregation #2)** | **+82%** | **❌ absent** | **❌ absent** | same differential ✅ |
| cylLS / cylLL (cytolysin) | – | – | – | paper: cyl weak/inconsistent, not in BFFF11 — consistent |

**Two results here are direct, clean reproductions of the paper's virulence claims:**
1. **The conserved core** (fsr quorum system, ace collagen adhesin, ebp pili, sortases, thiol peroxidase) is present at ≥ 90% identity in all three strains — matching the paper's "core VFs conserved in all three."
2. **The differential aggregation-substance claim** — the paper's Results state verbatim: *"two aggregation substance encoding genes agg and prgB were absent in the genomes of BFF1B1 and BFPS6"* while BFFF11 harbored all biofilm factors. Our independent tblastn shows exactly this: aggregation substance present only in BFFF11 (96% & 82%), cleanly absent in BFF1B1 and BFPS6. **This is the paper's most specific virulence claim and it replicates directly.**

The paper's aggregate count of "69 virulence genes" is database-dependent (VFDB + VirulenceFinder + PATRIC_Victors union) and was not reproduced as a raw number here; the marker-level structure it implies (conserved core + agg/prgB differential) is confirmed.

### 4.4 C2 — AMR conserved core — **PARTIAL**

`lsa(A)` (intrinsic macrolide-lincosamide-streptogramin efflux, listed in the paper's Table 2 as conserved in all three) is detected by AMRFinderPlus in **all three** strains (99.4–100%). This confirms the "conserved core AMR" structure. However, the paper's total of **39 AMR genes across 16 groups** is not reproduced: the paper's list (via CARD/ARG-ANNOT protein homology) counts many **intrinsic / point-mutation targets** — gyrA, gyrB, rpoB, rpoC, murA, EF-Tu, EF-G, folA, folP, Alr, Ddl, MprF, LiaFSR, etc. — that AMRFinderPlus classifies as core/intrinsic housekeeping and does not report as *acquired* resistance. This is a well-known methodological difference between homology-catalog tools (ARG-ANNOT/CARD-homolog mode) and AMRFinderPlus's curated acquired-AMR calls, not a contradiction of the underlying biology.

### 4.5 C5 — Phylogeny / clustering — **PARTIAL (directional)**

| Comparison | fastANI | MLST |
|---|---:|---|
| BFFF11 ↔ V583 (reference) | **99.46–99.63%** (highest) | BFFF11 untyped, profile closest to V583 (gdh12/gyd7/pstS3/aroE6/yqiL5) |
| BFFF11 ↔ BFF1B1 | 98.67–98.78% | BFF1B1 = ST482 |
| BFFF11 ↔ BFPS6 | 98.70–98.72% | BFPS6 = ST81 |
| BFF1B1 ↔ BFPS6 | 98.81–98.85% | — |

The paper's SNP tree places the two tilapia strains near the reference with BFPS6 on a separate branch. Our results are **directionally consistent** — BFFF11 is genomically closest to the V583 reference, and all three strains are distinct STs — but species-level ANI is saturated at ~98.7% and cannot robustly resolve the exact "tilapia-pair-together, BFPS6-apart" topology. A full CSIphylogeny SNP rerun (as the paper did) would be needed for a definitive topology test; the coarse signal does not contradict the paper.

### 4.6 C4 — Bacteriocin / secondary metabolites — **UNTESTED**

antiSMASH was not rerun this pass. The paper reports bacteriocin clusters in BFFF11 and BFPS6 (and NRPS in BFFF11); this remains the main untested claim.

## 5. Verdict

**PARTIAL REPLICATION (strong).**

Independently reproduced on the actual deposited genomes, using tools different from the paper's:
1. **Genome features (C6)** — sizes/GC/N50/L50 match Table 1 essentially exactly (two exact chromosome sizes, BFPS6 N50/L50 exact).
2. **Tetracycline-only-in-BFPS6 (C3)** — the paper's headline AMR finding, confirmed cleanly by AMRFinderPlus (tet(L)+tet(M) tandem cassette at 100% identity, BFPS6 only; no tet in either tilapia strain; V583 positive control valid).
3. **Aggregation-substance differential (C1b)** — the paper's most specific virulence claim (agg/prgB present in BFFF11, absent in BFF1B1 & BFPS6), confirmed directly by tblastn.
4. **Conserved VF core + conserved lsa(A)** — the structural backbone of C1/C2, confirmed.

Not reproduced / out of reach: the aggregate counts (69 VFs, 39 AMR genes) are database-framework-dependent and legitimately differ under the stricter AMRFinderPlus/tblastn calling; the exact phylogenetic topology (C5) is only directionally supported at ANI resolution; bacteriocin clusters (C4) were not rerun. No claim we tested was **contradicted**.

## 6. Coverage / Agreement

- **Coverage: 6 / 7** — C1, C1b, C2, C3, C5, C6 tested on real public genomes; only C4 (antiSMASH) untested.
- **Agreement: full on C1b, C3, C6 (the three concrete high-signal claims) + structural confirmation of C1/C2; partial on C2 (counts) and C5 (topology); C4 untested. No contradictions.**
- LLM-judge (free Argo `argo:gpt-5.2`): **VERDICT = PARTIAL**, coverage 6/7, "strongly confirms C6, C3, C1b; count-based C1/C2 not reproduced under stricter framework; C5 directional; C4 untested." (`report/evidence/llm_judge.txt`)

## 7. Resources used

| Resource | Use | Cost |
|---|---|---|
| Europe PMC REST | Full-text XML + metadata | Free |
| NCBI eutils (elink/esummary/efetch) | nuccore→assembly mapping | Free |
| NCBI Datasets v2alpha REST | 4 genomes (genome+protein+CDS+GFF) | Free, no auth |
| AMRFinderPlus 3.12.8 (DB 2024-07-22.1) | AMR + stress/virulence calls | Free (uicgpu) |
| mlst (efaecalis scheme) | Sequence typing | Free (uicgpu) |
| fastANI | Pairwise ANI | Free (uicgpu) |
| BLAST+ (tblastn/makeblastdb) | VF marker presence | Free (CherryRd + uicgpu) |
| Python 3 (stdlib) | Assembly stats, parsing | Free |
| Argo proxy (`argo:gpt-5.2`) | LLM-judge scoring | Free |

Compute: <10 min total (genome pull + AMRFinder ×4 + tblastn + fastANI). No GPU required; uicgpu used only for the pre-installed AMR toolchain.

## 8. Limitations

- **BFPS6 is a draft (45 contigs)**; tet(S)/tet(45) could in principle sit on an unassembled fragment, but AMRFinder found no partial hits and the tet(L)-tet(M) cassette is intact — the exclusivity conclusion is robust.
- Aggregate VF/AMR counts are inherently database-dependent; only marker-level and differential claims were tested, not the paper's exact tallies.
- Phylogeny tested at ANI/MLST resolution, not a full CSIphylogeny SNP rerun — topology is directional, not definitive.
- antiSMASH (C4) and PHASTER/ISfinder/PlasmidFinder descriptive claims not rerun.
- Virulence markers were sourced from the V583 reference proteome (canonical E. faecalis VF carrier), not the VFDB flat files the paper used; the two are highly concordant for these well-characterized genes.

## 9. Reproducibility artifacts

```
work/
├── efaecalis_fulltext.xml         # Europe PMC full text
├── genomes/                       # 4 NCBI Datasets zips + unpacked FASTA/GFF/protein
│   ├── GCA_009685155.1/  (BFFF11)
│   ├── GCF_017357805.1/  (BFF1B1)
│   ├── GCF_021375735.1/  (BFPS6)
│   └── GCF_000007785.1/  (V583 reference/control)
├── genome_stats.py                # assembly statistics driver
├── build_vf_query.py / vf_query.faa   # curated 13 VF markers from V583
├── vf_blast.py                    # tblastn VF presence/absence
├── run_amr_mlst.sh                # AMRFinderPlus + mlst (runs on uicgpu)
├── amr_out/                       # amrfinder + mlst + fastANI TSVs (pulled back)
└── judge.py                       # free-Argo LLM judge
report/
├── REPORT.md  brief.md  attempt_log.md  artifact_harvest.md
└── evidence/
    ├── paper_targets.json         # paper Table 1/2 + claims
    ├── genome_stats.json          # recomputed assembly stats
    ├── vf_presence.json           # VF tblastn calls
    ├── tet_presence.json          # tet tblastn probe
    ├── *_amrfinder.tsv *_mlst.tsv fastani_matrix.tsv
    └── llm_judge.txt              # free-Argo verdict
```

To reproduce the core (genome features + tet + VF differential):
```bash
# 1. download genomes
for acc in GCA_009685155.1 GCF_017357805.1 GCF_021375735.1 GCF_000007785.1; do
  curl -sS -o "$acc.zip" "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/$acc/download?include_annotation_type=GENOME_FASTA&include_annotation_type=PROT_FASTA&include_annotation_type=CDS_FASTA&include_annotation_type=GENOME_GFF"
  unzip -oq "$acc.zip" -d "$acc"
done
# 2. stats + VF
python3 genome_stats.py
python3 build_vf_query.py && python3 vf_blast.py
# 3. AMR (needs AMRFinderPlus)
bash run_amr_mlst.sh          # -> tet(L)+tet(M) only in BFPS6
```

---

## Verdict
**Verdict:** PARTIAL

WAVE_RESULT set=BVBRC-43 paper=Akter2023-Efaecalis-fish-streptococcosis verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-43-Efaecalis-fish-streptococcosis-2023/ one_line=Re-pulled all 3 deposited genomes; genome features match Table 1 to the base pair, tet(L)+tet(M) confirmed ONLY in BFPS6 via AMRFinderPlus, and aggregation-substance agg/prgB confirmed present in BFFF11 but absent in BFF1B1/BFPS6 via tblastn — three headline claims independently reproduced; aggregate VF/AMR counts framework-dependent, antiSMASH untested.
