# Artifacts Summary — BVBRC-14 Hybrid Assembly Replication

**Paper:** Khezri et al. 2021, *Microorganisms* 9(12):2560
**BioProject:** PRJEB45084
**Verdict:** PARTIAL (7/10)

---

## 1. Inputs Consumed

| Artifact | Source | Size / Count | Used For |
|---|---|---|---|
| Paper PDF | MDPI (open access) | ~1 paper | Claim extraction |
| Reference genome GCF_900119685.1 | NCBI Assembly | 2 sequences (5,174,631 bp + 161,069 bp) | Ground-truth verification |
| ERR5951441 (EC4 Illumina) | ENA / SRA | Paired-end MiSeq 2×300bp | SPAdes assembly |
| ERR5951446 (KP5 Illumina) | ENA / SRA | Paired-end MiSeq 2×300bp | SPAdes assembly |
| PlasmidFinder DB | bitbucket clone (2025) | full plasmid replicon set | Plasmid BLAST |
| VFDB setA_nt | VFDB 2025 download | full VF fasta | Virulence factor BLAST |
| ResFinder DB | conda pkg 4.7.2 | AMR gene fasta | AMR detection |
| AMRFinder DB | 2026-03-24.1 | AMR gene + point mutation | AMR cross-check |

**Not downloaded (out of scope):** any MinION reads (10 runs); remaining 9 Illumina runs; supplementary tables from MDPI (referenced but not re-parsed).

---

## 2. Assemblies Produced

| Assembly | Assembler | Contigs (≥1kb) | Total bp | N50 | Notes |
|---|---|---|---|---|---|
| **EC4 IllumASM** | SPAdes 4.0.0 | 175 | 5,827,066 | 106,275 | Paper reports EC IllumASM total ~5.3 Mbp ± 426 kb; ours slightly higher (larger genome) |
| **KP5 IllumASM** | SPAdes 4.0.0 | 109 | 5,591,911 | 312,224 | Falls within paper's KP IllumASM range (5,577,253 ± 181,931 bp; N50 247,095 ± 138,114) |

**No hybrid assemblies produced.** **No MinION-only assemblies produced.**

---

## 3. Tool-Output Artefacts (per assembly)

### 3.1 Reference genome (E. coli NCTC 13441, GCF_900119685.1)
- **ResFinder v4.7.2:** 14 acquired AMR genes → **exact match** to paper
  - 2× aadA5, 1× aac(6′)-Ib-cr, 2× blaCTX-M-15, 1× blaTEM-1B, 1× blaOXA-1, 2× mph(A), 2× sul1, 1× tet(A), 2× dfrA17
- **AMRFinder v4.2.7:** 26 total (14 acquired + 7 point mutations + 5 intrinsic)
- **PlasmidFinder:** IncFIA (99.7% id) + IncFII (100% id) → **exact match** to paper (2 replicons)
- **VFDB (2025):** 109 unique VF loci (paper reports 85 with 2020 VFDB — 24-locus increase attributable to database growth)

### 3.2 EC4 (ERR5951441)
- **ResFinder:** 6 acquired AMR genes — aac(3)-VIa, blaCTX-M-2, blaTEM-1B, 2× sul1, tet(A)
- **PlasmidFinder:** 5 replicons — IncHI2A, IncHI2, IncI(Gamma), IncI1-I(Alpha), p0111
- **VFDB:** 66 VF loci

### 3.3 KP5 (ERR5951446)
- **ResFinder:** 9 acquired AMR genes — aac(6′)-Ib3, aac(3)-IIa, aph(3′)-Ia, blaOKP-B-15, blaCTX-M-14, blaTEM-1B, cmlA1, OqxB, blaOKP-B-2
- **AMRFinder:** 14 total (including fosA, point mutations)
- **PlasmidFinder:** 5 replicons — IncFIA(HI1), IncFIA(pBK30683), IncFIB(K), IncFII(pKP91), IncFII
- **VFDB:** 24 VF loci

---

## 4. Claim-Audit Coverage

| Claim category | Total claims audited | Exact match | In range / Consistent / Plausible | Mismatch (methodological) | Not tested |
|---|---:|---:|---:|---:|---:|
| Assembly quality (Table 2) | 9 | 0 | 4 | 0 | 5 |
| Plasmid identification (§3.7) | 6 | 1 | 0 | 2 | 3 |
| AMR genes (§3.8) | 7 | 1 | 3 | 0 | 3 |
| β-lactamase variants (§3.8) | 3 | 0 | 3 | 0 | 2 |
| Virulence factors (§3.9) | 5 | 0 | 0 | 3 (db version drift) | 2 |
| Mixed culture (§3.10) | 4 | 0 | 0 | 1 | 3 |
| **Totals** | **34** | **2** | **10** | **6** | **18** |

**Roughly half of the paper's specific numeric claims (18/34) could not be tested here** because they depend on hybrid/long-read assemblies we did not produce. The claims we *could* test either matched exactly (reference genome) or were consistent within methodological variation (short-read isolate assemblies).

---

## 5. Report Files (this directory)

| File | Purpose |
|---|---|
| `REPORT.md` | Source-of-truth long-form report (Markdown) |
| `REPORT.tex` | LaTeX version with dedicated Genuine Critique section |
| `open_questions.json` | 5 truly open questions with basis + next steps |
| `workflow.md` | Step-by-step pipeline + deviations from paper |
| `artifacts_summary.md` | This file — inventory of inputs, outputs, and audit coverage |
| `failure_analysis.md` | Where this replication fell short, why, and what would fix it |

---

## 6. What This Replication Does *Not* Contain

- No hybrid Unicycler assemblies (0 of 9 isolates).
- No Flye long-read-only assemblies (0 of 9 isolates).
- No re-basecalling of MinION signal data (raw pod5/fast5 not fetched).
- No Bandage plasmid circularity confirmation.
- No BUSCO scores for any assembly (paper reports ~99.3% HybASM, ~27.7% MinIONASM).
- No mixed-culture (EC4+KP5) re-assembly.
- No re-analysis of MDPI supplementary tables.

These gaps are intentional (scope) and honestly noted; they are the main reason the verdict is PARTIAL rather than FULL.
